"""
CDM Forensic Research Engine v2.3 - Trust Audit Tool
Automated trustworthiness assessment implementing methodology checks.

This tool calculates trust metrics and flags issues that require attention:
- Temporal freshness decay
- Source diversity analysis
- Corroboration checking
- Content drift detection
- Contradiction flagging
- Confidence calibration
"""

import json
import sys
import hashlib
import logging
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import urlparse
from collections import Counter, defaultdict
from typing import Any

# Import centralized configuration
try:
    from config_loader import (
        get_confidence_caps,
        get_temporal_thresholds,
        get_valid_claim_types,
        get_source_authority_mapping,
        get_authority_levels,
        get_vendor_domains,
        get_maturity_weights
    )
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

# --- SAFE DOMAIN MATCHING ---
def is_trusted_domain(url: str, domain_pattern: str) -> bool:
    """
    Safely check if URL belongs to a trusted domain.
    Prevents substring attacks like 'finos.org' matching 'malfinos.org'.

    Args:
        url: The URL to check
        domain_pattern: The trusted domain pattern (e.g., 'finos.org', 'github.com/finos')

    Returns:
        True if URL is from the trusted domain, False otherwise
    """
    try:
        parsed = urlparse(url.lower() if url else '')
        hostname = parsed.netloc
        path = parsed.path

        # Remove port if present
        if ':' in hostname:
            hostname = hostname.split(':')[0]

        # Handle patterns that include path (e.g., 'github.com/finos')
        if '/' in domain_pattern:
            domain_part, path_part = domain_pattern.split('/', 1)
            # Check domain matches and path starts with expected prefix
            domain_matches = (hostname == domain_part or hostname.endswith('.' + domain_part))
            path_matches = path.lower().startswith('/' + path_part)
            return domain_matches and path_matches
        else:
            # Simple domain match: exact or subdomain
            return hostname == domain_pattern or hostname.endswith('.' + domain_pattern)
    except Exception:
        return False

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- CONSTANTS ---
# Load from centralized config - FAIL FAST if not available
if not CONFIG_AVAILABLE:
    raise SystemExit("FATAL: config_loader not available - check config/ directory")

try:
    _temporal = get_temporal_thresholds()
    CURRENT_THRESHOLD_DAYS = _temporal['current_days']
    DATED_THRESHOLD_DAYS = _temporal['dated_days']
    MAX_CONFIDENCE_BY_TIER = get_confidence_caps()
    SOURCE_AUTHORITY = get_source_authority_mapping()
    AUTHORITY_LEVELS = get_authority_levels()
    VENDOR_DOMAINS = get_vendor_domains()
    CLAIM_TYPE_WEIGHTS = get_maturity_weights()
    logger.debug("Loaded all configuration from config_loader")
except (KeyError, FileNotFoundError) as e:
    raise SystemExit(f"FATAL: Config error - {e}")

# Tier weights for evidence scoring (not externalized as rarely changed)
TIER_WEIGHTS = {1: 3, 2: 2, 3: 1, 4: 0.5}

# Deprecated classification terms (must use PRAGMATIST instead)
DEPRECATED_TERMS = [
    'NOT ENGAGED',
    'NOT_ENGAGED',
    'NON-ARCHITECT',
    'NON_ARCHITECT',
]


def check_deprecated_terminology(data: dict) -> list:
    """
    Check for deprecated classification terms in evidence data.

    Args:
        data: Evidence data dict

    Returns:
        List of warnings about deprecated terms
    """
    warnings = []
    data_str = json.dumps(data).upper()

    for term in DEPRECATED_TERMS:
        if term.upper() in data_str:
            warnings.append(f"DEPRECATED_TERM: '{term}' found - use PRAGMATIST instead")

    return warnings


def parse_date(date_str: str | None) -> datetime | None:
    """Parse various date formats."""
    if not date_str:
        return None

    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m",
        "%Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str[:len(date_str)], fmt)
        except ValueError:
            continue

    return None


def calculate_freshness(date_str: str | None) -> dict:
    """
    Calculate temporal freshness per methodology.
    Returns category and weight multiplier.
    """
    if not date_str:
        return {
            "age_days": None,
            "category": "unknown",
            "weight_multiplier": 0.5  # Penalize undated evidence
        }

    evidence_date = parse_date(date_str)
    if not evidence_date:
        return {
            "age_days": None,
            "category": "unknown",
            "weight_multiplier": 0.5
        }

    age = datetime.utcnow() - evidence_date
    age_days = age.days

    if age_days < CURRENT_THRESHOLD_DAYS:
        return {
            "age_days": age_days,
            "category": "current",
            "weight_multiplier": 1.0
        }
    elif age_days < DATED_THRESHOLD_DAYS:
        # Linear decay from 1.0 to 0.5 over the dated period
        decay = 0.5 + 0.5 * (DATED_THRESHOLD_DAYS - age_days) / (DATED_THRESHOLD_DAYS - CURRENT_THRESHOLD_DAYS)
        return {
            "age_days": age_days,
            "category": "dated",
            "weight_multiplier": round(decay, 2)
        }
    else:
        return {
            "age_days": age_days,
            "category": "historical",
            "weight_multiplier": 0.25  # Historical = context only
        }


def extract_domain(url: str) -> str:
    """Extract domain from URL for diversity checking."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        # Remove www prefix
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except Exception:
        return "unknown"


def calculate_source_diversity(items: list[dict]) -> float:
    """
    Calculate source diversity score.
    0 = all from single source, 1 = highly diverse.
    """
    if not items:
        return 0.0

    domains = [extract_domain(item.get('source_url', '')) for item in items]
    domain_counts = Counter(domains)

    # Remove 'unknown' from diversity calculation
    domain_counts.pop('unknown', None)

    if not domain_counts:
        return 0.0

    total = sum(domain_counts.values())
    unique = len(domain_counts)

    # Diversity formula: combination of unique ratio and evenness
    unique_ratio = unique / total if total > 0 else 0

    # Herfindahl-Hirschman Index for concentration
    hhi = sum((count / total) ** 2 for count in domain_counts.values())
    evenness = 1 - hhi  # Lower HHI = more even distribution

    # Combined score
    diversity = (unique_ratio + evenness) / 2
    return round(diversity, 3)


def check_corroboration(items: list[dict]) -> tuple[float, list[str]]:
    """
    Check corroboration rate and flag single-source claims.
    Returns (rate, list of warnings).
    """
    if not items:
        return 0.0, []

    warnings = []
    corroborated_count = 0

    # Group claims by similarity (simplified: by claim_type)
    claim_groups = defaultdict(list)
    for item in items:
        claim_type = item.get('claim_type', 'unknown')
        claim_groups[claim_type].append(item)

    for claim_type, group_items in claim_groups.items():
        if len(group_items) >= 2:
            # Check if from different sources
            domains = set(extract_domain(i.get('source_url', '')) for i in group_items)
            if len(domains) >= 2:
                corroborated_count += len(group_items)
            else:
                for item in group_items:
                    warnings.append(f"Single-source claim: {item.get('id')} ({claim_type})")
        else:
            item = group_items[0]
            if item.get('tier') in [1, 2]:  # High-value claims need corroboration
                warnings.append(f"Uncorroborated Tier {item.get('tier')} claim: {item.get('id')}")

    rate = corroborated_count / len(items) if items else 0
    return round(rate, 3), warnings


def detect_contradictions(items: list[dict]) -> list[dict]:
    """
    Detect potential contradictions between evidence items.
    Looks for conflicting claim types for same underlying assertion.
    """
    contradictions = []

    # Check for timeline contradictions
    production_items = [i for i in items if i.get('claim_type') == 'production_usage']
    pilot_items = [i for i in items if i.get('claim_type') == 'pilot_or_poc']

    for prod in production_items:
        prod_date = parse_date(prod.get('date'))
        if not prod_date:
            continue

        for pilot in pilot_items:
            pilot_date = parse_date(pilot.get('date'))
            if not pilot_date:
                continue

            # Contradiction: pilot dated AFTER production
            if pilot_date > prod_date:
                contradictions.append({
                    "item_ids": [prod.get('id'), pilot.get('id')],
                    "description": f"Pilot ({pilot.get('id')}) dated after production ({prod.get('id')})",
                    "resolution": "unresolved",
                    "resolution_notes": ""
                })

    # Check for same URL with different claims
    url_claims = defaultdict(list)
    for item in items:
        url = item.get('source_url', '')
        if url:
            url_claims[url].append(item)

    for url, url_items in url_claims.items():
        if len(url_items) > 1:
            types = set(i.get('claim_type') for i in url_items)
            if len(types) > 1:
                contradictions.append({
                    "item_ids": [i.get('id') for i in url_items],
                    "description": f"Same URL supports different claim types: {types}",
                    "resolution": "unresolved",
                    "resolution_notes": "Review if URL actually supports multiple claims"
                })

    # Check for tier conflicts (Tier 1 vs Tier 2 supporting opposite conclusions)
    tier1_items = [i for i in items if i.get('tier') == 1]
    tier2_items = [i for i in items if i.get('tier') == 2]

    def get_direction(item: dict) -> str:
        """Infer evidence direction from claim content."""
        claim = (item.get('claim', '') + ' ' + item.get('finding', '')).lower()
        if any(kw in claim for kw in ['production', 'live', 'deployed', 'pilot', 'poc', 'proof of concept']):
            return 'ARCHITECT'
        if any(kw in claim for kw in ['no evidence', 'not found', 'no mention', 'absence', 'traditional']):
            return 'PRAGMATIST'
        return 'NEUTRAL'

    tier1_directions = set(get_direction(i) for i in tier1_items) - {'NEUTRAL'}
    tier2_directions = set(get_direction(i) for i in tier2_items) - {'NEUTRAL'}

    if 'ARCHITECT' in tier1_directions and 'PRAGMATIST' in tier2_directions:
        contradictions.append({
            "item_ids": [i.get('id') for i in tier1_items + tier2_items],
            "description": "Tier 1 evidence supports ARCHITECT but Tier 2 contains PRAGMATIST signals",
            "resolution": "unresolved",
            "severity": "medium",
            "resolution_notes": "Higher-authority Tier 1 should generally prevail, but review Tier 2 for recency"
        })
    elif 'PRAGMATIST' in tier1_directions and 'ARCHITECT' in tier2_directions:
        contradictions.append({
            "item_ids": [i.get('id') for i in tier1_items + tier2_items],
            "description": "Tier 1 evidence suggests PRAGMATIST but Tier 2 supports ARCHITECT",
            "resolution": "unresolved",
            "severity": "high",
            "resolution_notes": "Unusual pattern - Tier 2 should not contradict Tier 1. Manual review required."
        })

    return contradictions


def calculate_confidence(
    items: list[dict],
    verification_rate: float,
    corroboration_rate: float,
    has_contradictions: bool
) -> tuple[int, str]:
    """
    Calculate overall confidence per methodology/confidence-calibration.md.
    Returns (confidence_percentage, rationale).
    """
    if not items:
        return 0, "No evidence items"

    valid_items = [
        i for i in items
        if i.get('verification', {}).get('status') in ['verified', 'archived']
    ]

    if not valid_items:
        return 15, "No verified evidence"

    # Step 1: Maximum by tier
    highest_tier = min(i.get('tier', 3) for i in valid_items)
    max_confidence = MAX_CONFIDENCE_BY_TIER.get(highest_tier, 35)

    rationale_parts = [f"Max by Tier {highest_tier}: {max_confidence}%"]

    # Step 2: Corroboration adjustment
    if corroboration_rate >= 0.6:
        corr_adj = 10
    elif corroboration_rate >= 0.3:
        corr_adj = 5
    elif corroboration_rate > 0:
        corr_adj = 0
    else:
        corr_adj = -10

    rationale_parts.append(f"Corroboration ({corroboration_rate:.0%}): {corr_adj:+d}%")

    # Step 3: Contradiction adjustment
    if has_contradictions:
        contra_adj = -15
        rationale_parts.append(f"Contradictions: {contra_adj}%")
    else:
        contra_adj = 0

    # Step 4: Verification adjustment
    if verification_rate >= 0.9:
        verif_adj = 5
    elif verification_rate >= 0.7:
        verif_adj = 0
    elif verification_rate >= 0.5:
        verif_adj = -5
    else:
        verif_adj = -10

    rationale_parts.append(f"Verification ({verification_rate:.0%}): {verif_adj:+d}%")

    # Step 5: Freshness adjustment
    current_count = sum(1 for i in valid_items if i.get('freshness', {}).get('category') == 'current')
    freshness_ratio = current_count / len(valid_items) if valid_items else 0

    if freshness_ratio >= 0.7:
        fresh_adj = 5
    elif freshness_ratio >= 0.4:
        fresh_adj = 0
    elif freshness_ratio > 0:
        fresh_adj = -5
    else:
        fresh_adj = -10

    rationale_parts.append(f"Freshness ({freshness_ratio:.0%} current): {fresh_adj:+d}%")

    # Calculate final with STRICT tier cap enforcement
    # Adjustments can only reduce confidence, never exceed tier cap
    total_adjustments = corr_adj + contra_adj + verif_adj + fresh_adj

    # Cap positive adjustments at 0 to prevent exceeding tier max
    if total_adjustments > 0:
        total_adjustments = 0
        rationale_parts.append("(positive adj capped at tier max)")

    final = max_confidence + total_adjustments
    final = max(20, min(max_confidence, final))  # Floor at 20%, cap at tier max

    rationale = " | ".join(rationale_parts) + f" = {final}%"

    return final, rationale


def detect_content_drift(items: list[dict]) -> list[str]:
    """
    Check for content that changed between verifications.
    Returns list of item IDs with drift.
    """
    drift_items = []

    for item in items:
        content = item.get('content', {})
        if content.get('content_changed'):
            drift_items.append(item.get('id'))

        # Check hash history
        history = content.get('hash_history', [])
        if len(history) > 1:
            hashes = [h.get('hash') for h in history]
            if len(set(hashes)) > 1:
                if item.get('id') not in drift_items:
                    drift_items.append(item.get('id'))

    return drift_items


def generate_provenance_hash(evidence_items: list[dict]) -> str:
    """Generate SHA256 hash of evidence items for tamper detection."""
    # Canonical JSON representation
    canonical = json.dumps(evidence_items, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()


def check_source_authority(items: list[dict]) -> tuple[float, list[str]]:
    """
    Check source authority and tier alignment per methodology.
    Returns (authority_score, list of warnings).
    """
    if not items:
        return 0.0, []

    warnings = []
    authority_scores = []

    authority_values = {"HIGH": 1.0, "MEDIUM-HIGH": 0.8, "MEDIUM": 0.6, "LOW": 0.3, "VERY LOW": 0.1}

    for item in items:
        url = item.get('source_url', '').lower()
        tier = item.get('tier', 3)
        item_id = item.get('id', 'unknown')

        # Check against known domains using safe matching
        matched = False
        for domain_pattern, (authority, expected_tier) in SOURCE_AUTHORITY.items():
            if is_trusted_domain(url, domain_pattern):
                matched = True
                authority_scores.append(authority_values.get(authority, 0.5))

                # Check tier alignment
                if tier < expected_tier:
                    warnings.append(
                        f"{item_id}: Tier {tier} too high for {domain_pattern} (expected T{expected_tier}+)"
                    )
                elif tier > expected_tier and authority in ["HIGH", "MEDIUM-HIGH"]:
                    warnings.append(
                        f"{item_id}: Tier {tier} may be too conservative for {domain_pattern}"
                    )
                break

        # Check for vendor bias using safe matching
        for vendor_domain in VENDOR_DOMAINS:
            if is_trusted_domain(url, vendor_domain):
                if item.get('claim_type') != 'vendor_proxy_signal':
                    warnings.append(
                        f"{item_id}: Vendor source ({vendor_domain}) should be 'vendor_proxy_signal' type"
                    )
                break

        if not matched:
            authority_scores.append(0.5)  # Unknown domain = medium authority

    avg_authority = sum(authority_scores) / len(authority_scores) if authority_scores else 0.5
    return round(avg_authority, 3), warnings


def check_duplicates(items: list[dict]) -> tuple[list[str], list[str]]:
    """
    Check for duplicate IDs and URLs.
    Returns (duplicate_id_warnings, duplicate_url_warnings).
    """
    id_warnings = []
    url_warnings = []

    # Check duplicate IDs
    ids = [item.get('id') for item in items]
    id_counts = Counter(ids)
    for item_id, count in id_counts.items():
        if count > 1:
            id_warnings.append(f"Duplicate ID '{item_id}' appears {count} times")

    # Check duplicate URLs (normalized)
    def normalize_url(url):
        """Normalize URL for comparison."""
        if not url:
            return ""
        url = url.lower().rstrip('/')
        # Remove common tracking params
        for param in ['?utm_', '&utm_', '?ref=', '&ref=']:
            if param in url:
                url = url.split(param)[0]
        return url

    url_to_items = defaultdict(list)
    for item in items:
        normalized = normalize_url(item.get('source_url', ''))
        if normalized:
            url_to_items[normalized].append(item.get('id'))

    for url, item_ids in url_to_items.items():
        if len(item_ids) > 1:
            # This might be intentional (same URL, different claims)
            # Only warn if claim_types are the same
            types = set(
                next((i.get('claim_type') for i in items if i.get('id') == iid), None)
                for iid in item_ids
            )
            if len(types) == 1:
                url_warnings.append(
                    f"Same URL used by {item_ids} with identical claim_type"
                )

    return id_warnings, url_warnings


def validate_cross_references(items: list[dict]) -> list[str]:
    """
    Validate that corroborated_by references point to existing items.
    Returns list of warnings.
    """
    warnings = []
    valid_ids = {item.get('id') for item in items}

    for item in items:
        corroborated_by = item.get('corroborated_by', [])
        if not isinstance(corroborated_by, list):
            corroborated_by = [corroborated_by]

        for ref_id in corroborated_by:
            if ref_id and ref_id not in valid_ids:
                warnings.append(
                    f"{item.get('id')}: corroborated_by references non-existent ID '{ref_id}'"
                )

        contradicts = item.get('contradicts', [])
        if not isinstance(contradicts, list):
            contradicts = [contradicts]

        for ref_id in contradicts:
            if ref_id and ref_id not in valid_ids:
                warnings.append(
                    f"{item.get('id')}: contradicts references non-existent ID '{ref_id}'"
                )

    return warnings


def check_excerpt_verification(items: list[dict]) -> tuple[float, list[str]]:
    """
    Check excerpt verification status from process_evidence.py.
    Returns (verification_rate, warnings).
    """
    warnings = []
    verified_count = 0
    total_with_excerpt = 0

    for item in items:
        excerpt = item.get('excerpt')
        if excerpt and len(excerpt) > 10:
            total_with_excerpt += 1
            excerpt_verified = item.get('content', {}).get('excerpt_verified')

            if excerpt_verified is True:
                verified_count += 1
            elif excerpt_verified is False:
                warnings.append(
                    f"{item.get('id')}: Excerpt not found in source content"
                )

    rate = verified_count / total_with_excerpt if total_with_excerpt > 0 else 1.0
    return round(rate, 3), warnings


def run_trust_audit(json_path: str) -> dict:
    """
    Run full trust audit on evidence file.
    Returns audit results.
    """
    json_path = Path(json_path).resolve()
    logger.info(f"Running trust audit on {json_path}")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load file: {e}")
        return {"error": str(e)}

    items = data.get('evidence_items', [])

    if not items:
        return {
            "error": "No evidence items found",
            "trust_metrics": {
                "overall_confidence": 0,
                "flags": ["NO_EVIDENCE"]
            }
        }

    # --- Calculate freshness for each item ---
    for item in items:
        item['freshness'] = calculate_freshness(item.get('date'))
        item['source_domain'] = extract_domain(item.get('source_url', ''))

    # --- Aggregate metrics ---

    # Verification rate
    verified_count = sum(
        1 for i in items
        if i.get('verification', {}).get('status') in ['verified', 'archived']
    )
    verification_rate = verified_count / len(items) if items else 0

    # Source diversity
    source_diversity = calculate_source_diversity(items)

    # Temporal health
    current_count = sum(1 for i in items if i.get('freshness', {}).get('category') == 'current')
    temporal_health = current_count / len(items) if items else 0

    # Corroboration
    corroboration_rate, corr_warnings = check_corroboration(items)

    # Contradictions
    contradictions = detect_contradictions(items)

    # Content drift
    drift_items = detect_content_drift(items)

    # NEW: Source authority check
    authority_score, authority_warnings = check_source_authority(items)

    # NEW: Duplicate detection
    id_dup_warnings, url_dup_warnings = check_duplicates(items)

    # NEW: Cross-reference validation
    xref_warnings = validate_cross_references(items)

    # NEW: Excerpt verification check
    excerpt_rate, excerpt_warnings = check_excerpt_verification(items)

    # Confidence calculation (now includes authority adjustment)
    confidence, confidence_rationale = calculate_confidence(
        items, verification_rate, corroboration_rate, len(contradictions) > 0
    )

    # Apply authority adjustment
    if authority_score < 0.5:
        confidence = max(20, confidence - 10)
        confidence_rationale += f" | Low authority ({authority_score:.2f}): -10%"

    # --- Generate flags ---
    flags = []
    warnings = list(corr_warnings)  # Copy

    # Add new check warnings
    warnings.extend(authority_warnings)
    warnings.extend(id_dup_warnings)
    warnings.extend(url_dup_warnings)
    warnings.extend(xref_warnings)
    warnings.extend(excerpt_warnings)

    if source_diversity < 0.3:
        flags.append("SINGLE_SOURCE_CLAIM")
        warnings.append(f"Low source diversity: {source_diversity:.2f}")

    if temporal_health < 0.3:
        flags.append("STALE_EVIDENCE")
        warnings.append(f"Most evidence is dated or historical: {temporal_health:.0%} current")

    if verification_rate < 0.5:
        flags.append("UNVERIFIED_URLS")
        warnings.append(f"Low verification rate: {verification_rate:.0%}")

    if contradictions:
        flags.append("CONTRADICTIONS_DETECTED")
        warnings.append(f"{len(contradictions)} contradiction(s) detected")

    highest_tier = min((i.get('tier', 3) for i in items), default=3)
    if highest_tier == 3:
        flags.append("LOW_TIER_ONLY")
        warnings.append("No Tier 1 or Tier 2 evidence found")

    if drift_items:
        flags.append("CONTENT_DRIFT_DETECTED")
        warnings.append(f"Content changed for: {', '.join(drift_items)}")

    if corroboration_rate < 0.3:
        flags.append("MISSING_CORROBORATION")

    # NEW: Add flags for new checks
    if id_dup_warnings:
        flags.append("DUPLICATE_IDS")

    if excerpt_rate < 0.5 and excerpt_warnings:
        flags.append("EXCERPTS_NOT_VERIFIED")

    if authority_warnings:
        flags.append("TIER_AUTHORITY_MISMATCH")

    # Check for deprecated terminology
    deprecated_warnings = check_deprecated_terminology(data)
    if deprecated_warnings:
        warnings.extend(deprecated_warnings)
        flags.append("DEPRECATED_TERMINOLOGY")

    # --- Build trust metrics ---
    trust_metrics = {
        "overall_confidence": confidence,
        "confidence_rationale": confidence_rationale,
        "source_diversity_score": source_diversity,
        "temporal_health_score": round(temporal_health, 3),
        "corroboration_rate": corroboration_rate,
        "verification_rate": round(verification_rate, 3),
        "authority_score": authority_score,
        "excerpt_verification_rate": excerpt_rate,
        "warnings": warnings,
        "flags": flags
    }

    # --- Update data ---
    data['trust_metrics'] = trust_metrics
    data['contradictions'] = contradictions
    data['evidence_items'] = items  # With freshness added

    # Update provenance
    if 'meta' not in data:
        data['meta'] = {}

    previous_hash = data['meta'].get('provenance', {}).get('evidence_hash')
    new_hash = generate_provenance_hash(items)

    data['meta']['provenance'] = {
        "evidence_hash": new_hash,
        "signed_at": datetime.utcnow().isoformat(),
        "previous_hash": previous_hash
    }
    data['meta']['schema_version'] = "2.3"

    # --- Write updated file ---
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # --- Print report ---
    print("\n" + "="*60)
    print(f"TRUST AUDIT REPORT: {data.get('bank_name', 'Unknown')}")
    print("="*60)
    print(f"\nOverall Confidence: {confidence}%")
    print(f"Rationale: {confidence_rationale}")
    print(f"\nMetrics:")
    print(f"  - Source Diversity:   {source_diversity:.2f}")
    print(f"  - Temporal Health:    {temporal_health:.0%}")
    print(f"  - Corroboration Rate: {corroboration_rate:.0%}")
    print(f"  - Verification Rate:  {verification_rate:.0%}")
    print(f"  - Authority Score:    {authority_score:.2f}")
    print(f"  - Excerpt Verified:   {excerpt_rate:.0%}")

    if flags:
        print(f"\nFlags ({len(flags)}):")
        for flag in flags:
            print(f"  - {flag}")

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")

    if contradictions:
        print(f"\nContradictions ({len(contradictions)}):")
        for c in contradictions:
            print(f"  - {c['description']}")

    print("\n" + "="*60)

    return {
        "trust_metrics": trust_metrics,
        "contradictions": contradictions,
        "provenance_hash": new_hash
    }


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python trust_audit.py <path/to/evidence.json>")
        print("       python trust_audit.py --batch <directory>")
        sys.exit(1)

    if sys.argv[1] == '--batch':
        if len(sys.argv) < 3:
            print("Error: --batch requires a directory path")
            sys.exit(1)

        directory = Path(sys.argv[2])
        json_files = list(directory.rglob("evidence.json"))

        print(f"Found {len(json_files)} evidence files")

        results = []
        for json_file in json_files:
            result = run_trust_audit(str(json_file))
            results.append({
                "file": str(json_file),
                "confidence": result.get('trust_metrics', {}).get('overall_confidence', 0),
                "flags": result.get('trust_metrics', {}).get('flags', [])
            })

        # Summary
        print("\n" + "="*60)
        print("BATCH SUMMARY")
        print("="*60)
        for r in sorted(results, key=lambda x: x['confidence'], reverse=True):
            flags_str = ', '.join(r['flags'][:3]) if r['flags'] else 'None'
            print(f"{r['confidence']:3d}% | {r['file']} | {flags_str}")
    else:
        run_trust_audit(sys.argv[1])


if __name__ == "__main__":
    main()
