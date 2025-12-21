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
        get_maturity_weights,
        get_domain_credibility,
        get_author_credibility,
        get_bank_relationships,
        load_source_credibility
    )
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

# Import relationship analyzer
try:
    from relationship_analyzer import RelationshipAnalyzer
    RELATIONSHIP_ANALYZER_AVAILABLE = True
except ImportError:
    RELATIONSHIP_ANALYZER_AVAILABLE = False

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


def check_consistency_flags(json_path: str, data: dict) -> tuple[list, list]:
    """
    Check for cross-bank consistency issues.

    Uses the ConsistencyChecker to compare this bank's evidence profile
    against known patterns and peer cohorts.

    Args:
        json_path: Path to evidence.json
        data: Parsed evidence data

    Returns:
        Tuple of (flags, warnings)
    """
    flags = []
    warnings = []

    try:
        # Import consistency checker
        from consistency_checker import ConsistencyChecker

        # Determine phase directory from path
        json_path = Path(json_path)
        bank_dir = json_path.parent
        phase_dir = bank_dir.parent
        bank_id = bank_dir.name

        # Initialize checker and generate fingerprint
        checker = ConsistencyChecker()
        fingerprint = checker.generate_fingerprint(data)

        # Store fingerprint in data for future reference
        if 'meta' not in data:
            data['meta'] = {}
        data['meta']['evidence_fingerprint'] = fingerprint.to_dict()

        # Check for consistency issues
        issues = checker.check_bank_consistency(bank_id, phase_dir)

        for issue in issues:
            if issue.severity == "critical":
                flags.append("CONSISTENCY_CRITICAL")
                warnings.append(f"[CONSISTENCY] {issue.issue_type}: {issue.description}")
            elif issue.severity == "warning":
                flags.append("CONSISTENCY_WARNING")
                warnings.append(f"[CONSISTENCY] {issue.issue_type}: {issue.description}")
            else:
                warnings.append(f"[CONSISTENCY INFO] {issue.description}")

        # Check for similar profile divergence specifically
        for issue in issues:
            if issue.issue_type == "SIMILAR_PROFILE_CLASSIFICATION_DIVERGENCE":
                flags.append("SIMILAR_PROFILE_DIVERGENCE")
            elif issue.issue_type == "PEER_OUTLIER_CONFIDENCE":
                flags.append("PEER_OUTLIER")
            elif issue.issue_type == "PEER_OUTLIER_CLASSIFICATION":
                flags.append("PEER_OUTLIER")

    except ImportError:
        # Consistency checker not available - skip
        pass
    except Exception as e:
        warnings.append(f"[CONSISTENCY] Error during consistency check: {str(e)}")

    return flags, warnings


def parse_date(date_str: str | None) -> datetime | None:
    """Parse various date formats commonly found in evidence sources."""
    if not date_str:
        return None

    # Normalize whitespace
    date_str = date_str.strip()

    formats = [
        # ISO formats (most common)
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S%z",
        # Slash variants
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        # Human-readable formats
        "%B %d, %Y",      # December 19, 2025
        "%b %d, %Y",      # Dec 19, 2025
        "%d %B %Y",       # 19 December 2025
        "%d %b %Y",       # 19 Dec 2025
        # Partial dates
        "%B %Y",          # December 2025
        "%b %Y",          # Dec 2025
        "%Y-%m",
        "%Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    # Log unparseable dates for debugging (only if logging at DEBUG level)
    logger.debug(f"Could not parse date: '{date_str}'")
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


def calculate_freshness_with_type_decay(
    date_str: str | None,
    claim_type: str | None = None,
    tier: int = 2
) -> dict:
    """
    Calculate temporal freshness with type-specific decay (Enhancement 5).

    Different evidence types decay at different rates:
    - production_usage: 36-month half-life (very sticky)
    - hiring_signal: 6-month half-life (transient)
    - etc.

    Args:
        date_str: Evidence date string
        claim_type: Type of claim (e.g., 'production_usage', 'hiring_signal')
        tier: Evidence tier (1, 2, or 3)

    Returns:
        dict with age_days, category, weight_multiplier, decay_model
    """
    # Get base freshness
    base_freshness = calculate_freshness(date_str)

    if not claim_type or base_freshness.get('age_days') is None:
        return base_freshness

    # Import decay calculator
    try:
        from config_loader import calculate_evidence_weight, get_evidence_decay_rate

        age_days = base_freshness['age_days']
        age_months = age_days / 30.44  # Average days per month

        # Calculate type-specific weight
        type_weight = calculate_evidence_weight(claim_type, age_months, tier)

        # Get decay parameters for reference
        decay_params = get_evidence_decay_rate(claim_type, tier)

        return {
            "age_days": age_days,
            "age_months": round(age_months, 1),
            "category": base_freshness['category'],
            "weight_multiplier": round(type_weight, 3),
            "decay_model": {
                "claim_type": claim_type,
                "tier": tier,
                "half_life_months": decay_params.get('effective_half_life'),
                "minimum_weight": decay_params.get('minimum_weight')
            }
        }
    except ImportError:
        return base_freshness


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


def get_contradiction_details(items: list[dict], contradictions: list[dict]) -> list[dict]:
    """
    Get detailed information about contradictions for resolution workflow.

    This function enriches the basic contradiction detection with full context
    needed by the Reasoning Gate Agent during Stage 5.5 (Contradiction Resolution).

    Args:
        items: List of evidence items from evidence.json
        contradictions: List of contradictions from detect_contradictions()

    Returns:
        List of enriched contradiction details with full evidence context
    """
    # Build item lookup by ID
    item_lookup = {item.get('id'): item for item in items}

    detailed_contradictions = []

    for contradiction in contradictions:
        item_ids = contradiction.get('item_ids', [])

        # Gather full details for each involved item
        involved_items = []
        for item_id in item_ids:
            item = item_lookup.get(item_id, {})
            involved_items.append({
                'id': item_id,
                'claim': item.get('claim', ''),
                'excerpt': item.get('excerpt', ''),
                'source_url': item.get('source_url', ''),
                'date': item.get('date', ''),
                'tier': item.get('tier', 3),
                'claim_type': item.get('claim_type', 'unknown'),
                'direction': item.get('direction', 'NEUTRAL'),
                'quality_assessment': item.get('quality_assessment', {}),
                'freshness': item.get('freshness', {})
            })

        # Classify contradiction type based on pattern
        description = contradiction.get('description', '').lower()
        if 'dated after' in description or 'timeline' in description:
            contradiction_type = 'TEMPORAL'
        elif 'same url' in description:
            contradiction_type = 'DEFINITIONAL'
        elif 'tier' in description and ('architect' in description or 'pragmatist' in description):
            contradiction_type = 'FACTUAL'
        else:
            contradiction_type = 'FACTUAL'  # Default to factual

        # Determine severity
        severity = contradiction.get('severity', 'medium')
        if not severity:
            # Infer severity from tiers involved
            tiers = [i.get('tier', 3) for i in involved_items]
            if 1 in tiers:
                severity = 'high'
            elif 2 in tiers:
                severity = 'medium'
            else:
                severity = 'low'

        detailed = {
            'contradiction_id': f"CONTRA-{len(detailed_contradictions) + 1:03d}",
            'type': contradiction_type,
            'severity': severity,
            'description': contradiction.get('description', ''),
            'resolution': contradiction.get('resolution', 'unresolved'),
            'resolution_notes': contradiction.get('resolution_notes', ''),
            'involved_items': involved_items,
            'source_a': involved_items[0] if len(involved_items) > 0 else None,
            'source_b': involved_items[1] if len(involved_items) > 1 else None,
            'recommended_action': _recommend_resolution_action(contradiction_type, involved_items)
        }

        detailed_contradictions.append(detailed)

    return detailed_contradictions


def _recommend_resolution_action(contradiction_type: str, involved_items: list[dict]) -> str:
    """
    Recommend a resolution action based on contradiction type and items.

    Args:
        contradiction_type: TEMPORAL, DEFINITIONAL, or FACTUAL
        involved_items: List of involved evidence items

    Returns:
        Recommended action string
    """
    if contradiction_type == 'TEMPORAL':
        # Find most recent item
        dates = [(i.get('id'), i.get('date', '')) for i in involved_items]
        sorted_dates = sorted(dates, key=lambda x: x[1] if x[1] else '', reverse=True)
        if sorted_dates:
            return f"Use most recent source ({sorted_dates[0][0]}), document evolution"
        return "Order sources chronologically, use most recent"

    elif contradiction_type == 'DEFINITIONAL':
        return "Clarify terminology differences, both may be valid simultaneously"

    else:  # FACTUAL
        # Compare tiers
        tiers = {i.get('id'): i.get('tier', 3) for i in involved_items}
        sorted_by_tier = sorted(tiers.items(), key=lambda x: x[1])
        if sorted_by_tier and len(sorted_by_tier) >= 2:
            if sorted_by_tier[0][1] < sorted_by_tier[1][1]:
                return f"Higher-tier source ({sorted_by_tier[0][0]}) should prevail, verify recency"
        return "Manual review required - compare source authority and recency"


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

    # Use centralized config (AUTHORITY_LEVELS loaded at module level from source-authority.json)
    # Keys use underscores: HIGH, MEDIUM_HIGH, MEDIUM, LOW, VERY_LOW

    for item in items:
        url = item.get('source_url', '').lower()
        tier = item.get('tier', 3)
        item_id = item.get('id', 'unknown')

        # Check against known domains using safe matching
        matched = False
        for domain_pattern, (authority, expected_tier) in SOURCE_AUTHORITY.items():
            if is_trusted_domain(url, domain_pattern):
                matched = True
                authority_scores.append(AUTHORITY_LEVELS.get(authority, 0.5))

                # Check tier alignment
                if tier < expected_tier:
                    warnings.append(
                        f"{item_id}: Tier {tier} too high for {domain_pattern} (expected T{expected_tier}+)"
                    )
                elif tier > expected_tier and authority in ["HIGH", "MEDIUM_HIGH"]:
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


def check_enhanced_source_authority(items: list[dict]) -> tuple[float, list[str], dict]:
    """
    Enhanced source authority check using source_credibility.json.
    Returns (enhanced_score, warnings, details).
    """
    if not items or not CONFIG_AVAILABLE:
        return 0.5, [], {}

    warnings = []
    enhanced_scores = []
    details = {
        'domains_checked': [],
        'lr_multipliers_applied': [],
        'vendor_bias_adjustments': []
    }

    source_credibility = load_source_credibility()
    vendor_adjustments = source_credibility.get('vendor_domain_adjustments', {}).get('domains', {})

    for item in items:
        url = item.get('source_url', '')
        item_id = item.get('id', 'unknown')

        # Extract domain
        try:
            parsed = urlparse(url.lower())
            domain = parsed.netloc
            if ':' in domain:
                domain = domain.split(':')[0]
        except Exception:
            domain = ''

        if not domain:
            enhanced_scores.append(0.5)
            continue

        # Check domain credibility
        domain_cred = get_domain_credibility(domain)

        if domain_cred:
            composite = domain_cred.get('composite_score', 0.5)
            lr_mult = domain_cred.get('lr_multiplier', 1.0)

            enhanced_scores.append(composite)
            details['domains_checked'].append({
                'domain': domain,
                'item_id': item_id,
                'composite_score': composite,
                'cdm_coverage_quality': domain_cred.get('cdm_coverage_quality', 'unknown')
            })

            if lr_mult != 1.0:
                details['lr_multipliers_applied'].append({
                    'domain': domain,
                    'item_id': item_id,
                    'multiplier': lr_mult
                })
        else:
            # Check if it's a vendor domain
            vendor_info = vendor_adjustments.get(domain)
            if vendor_info:
                bias_adj = vendor_info.get('bias_adjustment', 0.3)
                enhanced_scores.append(0.5 * (1 - bias_adj))
                details['vendor_bias_adjustments'].append({
                    'domain': domain,
                    'item_id': item_id,
                    'adjustment': bias_adj,
                    'requires_corroboration': vendor_info.get('requires_corroboration', True)
                })
                if vendor_info.get('requires_corroboration'):
                    warnings.append(
                        f"{item_id}: Vendor source ({domain}) requires bank confirmation"
                    )
            else:
                enhanced_scores.append(0.5)

    avg_score = sum(enhanced_scores) / len(enhanced_scores) if enhanced_scores else 0.5
    return round(avg_score, 3), warnings, details


def check_relationship_corroboration(bank_id: str, items: list[dict]) -> tuple[float, list[str], dict]:
    """
    Check if evidence aligns with known relationship pressure.
    Returns (corroboration_rate, warnings, pressure_vector).
    """
    if not bank_id or not RELATIONSHIP_ANALYZER_AVAILABLE:
        return 0.5, [], {}

    warnings = []

    try:
        analyzer = RelationshipAnalyzer()
        metrics = analyzer.calculate_network_metrics(bank_id)
        pressure_vector = metrics.pressure_vector

        # Calculate evidence direction
        architect_evidence = 0
        pragmatist_evidence = 0

        for item in items:
            direction = item.get('direction', '').upper()
            if 'ARCHITECT' in direction:
                architect_evidence += 1
            elif 'PRAGMATIST' in direction:
                pragmatist_evidence += 1

        total = architect_evidence + pragmatist_evidence
        if total == 0:
            return 0.5, [], pressure_vector.to_dict()

        evidence_direction = 'ARCHITECT' if architect_evidence > pragmatist_evidence else 'PRAGMATIST'

        # Check alignment with pressure vector
        aligned = evidence_direction == pressure_vector.net_direction

        if not aligned and pressure_vector.confidence > 0.5:
            warnings.append(
                f"Evidence direction ({evidence_direction}) contradicts "
                f"relationship pressure ({pressure_vector.net_direction})"
            )

        # Calculate corroboration rate based on alignment
        if aligned:
            corroboration_rate = 0.7 + (pressure_vector.confidence * 0.3)
        else:
            corroboration_rate = 0.3 + (1 - pressure_vector.confidence) * 0.2

        return round(corroboration_rate, 3), warnings, pressure_vector.to_dict()

    except Exception as e:
        logger.warning(f"Relationship analysis failed: {e}")
        return 0.5, [], {}


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


# Product weights for coverage analysis
PRODUCT_WEIGHTS = {
    "IRS": 0.35,
    "CDS": 0.25,
    "FX_Forwards": 0.15,
    "FX_Options": 0.05,
    "Equity_Swaps": 0.05,
    "Equity_Options": 0.05,
    "Commodities": 0.05,
    "Structured_Products": 0.02,
    "Repo": 0.02,
    "ETD": 0.01
}


def check_product_coverage(items: list[dict]) -> tuple[dict, list[str]]:
    """
    Check product coverage breadth in evidence.
    Flags narrow product focus that may indicate incomplete research.

    Returns (coverage_metrics, warnings).
    """
    warnings = []

    # Extract products from all evidence items
    products_found = set()
    product_evidence_count = {}

    for item in items:
        product_scope = item.get('product_scope', [])
        if product_scope:
            for product in product_scope:
                products_found.add(product)
                product_evidence_count[product] = product_evidence_count.get(product, 0) + 1

    # Calculate coverage metrics
    total_products = len(PRODUCT_WEIGHTS)
    products_covered = len(products_found)
    coverage_rate = products_covered / total_products if total_products > 0 else 0

    # Calculate regulatory-weighted coverage
    weighted_coverage = sum(
        PRODUCT_WEIGHTS.get(p, 0.05) for p in products_found
    ) / sum(PRODUCT_WEIGHTS.values())

    # Determine if evidence is narrowly focused
    if products_covered == 1 and len(items) > 3:
        warnings.append(
            f"Evidence concentrated in single product: {list(products_found)[0]}"
        )
    elif coverage_rate < 0.3 and len(items) > 5:
        warnings.append(
            f"Narrow product coverage: {products_covered}/{total_products} products"
        )

    # Check if high-weight products are covered
    high_weight_products = ['IRS', 'CDS', 'FX_Forwards']
    covered_high_weight = [p for p in high_weight_products if p in products_found]
    if not covered_high_weight and products_found:
        warnings.append(
            "Evidence missing core products (IRS, CDS, FX_Forwards)"
        )

    metrics = {
        "products_covered": list(products_found),
        "coverage_count": products_covered,
        "total_products": total_products,
        "coverage_rate": round(coverage_rate, 3),
        "weighted_coverage": round(weighted_coverage, 3),
        "product_evidence_counts": product_evidence_count
    }

    return metrics, warnings


def check_cohort_pressure(bank_id: str) -> tuple[dict, list[str]]:
    """
    Check peer cohort pressure for a bank (Enhancement 4).

    Analyzes the bank's position relative to peer cohorts and calculates
    network adoption pressure based on how many peers are ARCHITECT.

    Args:
        bank_id: Bank identifier

    Returns:
        tuple of (metrics_dict, warnings_list)
    """
    warnings = []

    try:
        # Import dynamically to avoid circular imports
        from cohort_threshold_calculator import CohortThresholdCalculator

        calculator = CohortThresholdCalculator()
        pressure_metrics = calculator.calculate_peer_pressure(bank_id)

        # Generate warnings based on pressure level
        if pressure_metrics.pressure_intensity == 'CRITICAL':
            warnings.append(
                f"HIGH_COHORT_PRESSURE: Critical mass of peers ({len(pressure_metrics.peer_architects)}) "
                f"are ARCHITECT - strong pressure to adopt CDM"
            )
        elif pressure_metrics.pressure_intensity == 'HIGH':
            warnings.append(
                f"MODERATE_COHORT_PRESSURE: Above tipping point - "
                f"{pressure_metrics.architect_peer_rate:.0%} of peers are ARCHITECT"
            )

        # Return metrics
        metrics = {
            "bank_id": bank_id,
            "cohorts": pressure_metrics.cohorts,
            "total_peers": pressure_metrics.total_peers,
            "architect_peers": len(pressure_metrics.peer_architects),
            "architect_peer_rate": round(pressure_metrics.architect_peer_rate, 3),
            "pressure_intensity": pressure_metrics.pressure_intensity,
            "estimated_pressure": round(pressure_metrics.estimated_pressure, 3),
            "recommended_adjustment": round(pressure_metrics.recommended_classification_adjustment, 3)
        }

        return metrics, warnings

    except ImportError:
        # Calculator not available
        return {"error": "cohort_threshold_calculator not available"}, []
    except Exception as e:
        return {"error": str(e)}, []


def check_expert_presence(bank_id: str) -> tuple[dict, list[str]]:
    """
    Check for known CDM experts at a bank (Enhancement 6).

    Having architect-level CDM experts is a strong ARCHITECT signal.

    Args:
        bank_id: Bank identifier

    Returns:
        tuple of (metrics_dict, warnings_list)
    """
    warnings = []

    try:
        # Import dynamically to avoid circular imports
        from expert_tracker import ExpertTracker

        tracker = ExpertTracker()
        metrics = tracker.get_bank_experts(bank_id)

        # Generate warnings based on expert presence
        if metrics.architect_count >= 2:
            warnings.append(
                f"STRONG_EXPERT_SIGNAL: {metrics.architect_count} architect-level CDM experts - "
                f"strong ARCHITECT indicator (LR adj: {metrics.recommended_lr_adjustment:.2f}x)"
            )
        elif metrics.architect_count == 1:
            warnings.append(
                f"EXPERT_SIGNAL: Architect-level CDM expert present - "
                f"ARCHITECT indicator (LR adj: {metrics.recommended_lr_adjustment:.2f}x)"
            )
        elif metrics.total_experts > 0:
            warnings.append(
                f"MODERATE_EXPERT_SIGNAL: {metrics.total_experts} CDM practitioner(s) present"
            )

        return {
            "bank_id": bank_id,
            "total_experts": metrics.total_experts,
            "architect_count": metrics.architect_count,
            "contributor_count": metrics.contributor_count,
            "expertise_score": metrics.expertise_score,
            "recommended_lr_adjustment": metrics.recommended_lr_adjustment
        }, warnings

    except ImportError:
        return {"error": "expert_tracker not available"}, []
    except Exception as e:
        return {"error": str(e)}, []


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

    # NEW: Enhanced source authority using source_credibility.json
    enhanced_authority, enhanced_auth_warnings, auth_details = check_enhanced_source_authority(items)

    # NEW: Relationship corroboration check
    bank_id = data.get('bank_id', '')
    rel_corr_rate, rel_corr_warnings, pressure_vector = check_relationship_corroboration(bank_id, items)

    # NEW: Product coverage check
    product_coverage, product_warnings = check_product_coverage(items)

    # Confidence calculation (now includes authority adjustment)
    confidence, confidence_rationale = calculate_confidence(
        items, verification_rate, corroboration_rate, len(contradictions) > 0
    )

    # Apply authority adjustment (use enhanced score if available)
    effective_authority = enhanced_authority if enhanced_authority > 0 else authority_score
    if effective_authority < 0.5:
        confidence = max(20, confidence - 10)
        confidence_rationale += f" | Low authority ({effective_authority:.2f}): -10%"

    # Apply relationship pressure adjustment
    if pressure_vector and rel_corr_rate < 0.4:
        confidence = max(15, confidence - 5)
        confidence_rationale += f" | Relationship contradiction: -5%"

    # --- Generate flags ---
    flags = []
    warnings = list(corr_warnings)  # Copy

    # Add new check warnings
    warnings.extend(authority_warnings)
    warnings.extend(id_dup_warnings)
    warnings.extend(url_dup_warnings)
    warnings.extend(xref_warnings)
    warnings.extend(excerpt_warnings)
    warnings.extend(enhanced_auth_warnings)
    warnings.extend(rel_corr_warnings)
    warnings.extend(product_warnings)

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

    # NEW: Relationship pressure contradiction flag
    if rel_corr_warnings:
        flags.append("RELATIONSHIP_PRESSURE_CONTRADICTION")

    # NEW: Product coverage flag
    if product_warnings:
        flags.append("NARROW_PRODUCT_COVERAGE")

    # Check for deprecated terminology
    deprecated_warnings = check_deprecated_terminology(data)
    if deprecated_warnings:
        warnings.extend(deprecated_warnings)
        flags.append("DEPRECATED_TERMINOLOGY")

    # --- Consistency checking integration ---
    consistency_flags, consistency_warnings = check_consistency_flags(json_path, data)
    flags.extend(consistency_flags)
    warnings.extend(consistency_warnings)

    # --- Build trust metrics ---
    trust_metrics = {
        "overall_confidence": confidence,
        "confidence_rationale": confidence_rationale,
        "source_diversity_score": source_diversity,
        "temporal_health_score": round(temporal_health, 3),
        "corroboration_rate": corroboration_rate,
        "verification_rate": round(verification_rate, 3),
        "authority_score": authority_score,
        "enhanced_authority_score": enhanced_authority,
        "relationship_corroboration_rate": rel_corr_rate,
        "pressure_vector": pressure_vector,
        "excerpt_verification_rate": excerpt_rate,
        "product_coverage": product_coverage,
        "warnings": warnings,
        "flags": flags
    }

    # --- Get detailed contradiction info for resolution workflow ---
    contradiction_details = get_contradiction_details(items, contradictions)

    # --- Update data ---
    data['trust_metrics'] = trust_metrics
    data['contradictions'] = contradictions
    data['contradiction_details'] = contradiction_details  # For Stage 5.5 resolution
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
