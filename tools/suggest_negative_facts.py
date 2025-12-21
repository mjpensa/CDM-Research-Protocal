"""
CDM Research Protocol - Negative Facts Suggester v1.0

Post-research analysis tool that examines completed bank research sessions
and suggests additions to knowledge_base/negative_facts.md.

This tool:
- Detects dead-end search patterns from null_results
- Identifies false leads (vendor claims without bank confirmation)
- Tracks jurisdiction-specific patterns
- Calculates time savings estimates
- Supports interactive approval or batch mode

Usage:
    # Analyze single bank (interactive)
    python suggest_negative_facts.py analyze outputs/phase-1/deutsche-bank/ -i

    # Analyze single bank (dry run)
    python suggest_negative_facts.py analyze outputs/phase-1/deutsche-bank/ --dry-run

    # Analyze entire phase
    python suggest_negative_facts.py phase outputs/phase-1-european-tier1/

    # Apply batch suggestions
    python suggest_negative_facts.py apply outputs/state/negative-facts-phase1.json

    # List pending suggestions
    python suggest_negative_facts.py list
"""

import argparse
import json
import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- PATHS ---
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_NEGATIVE_FACTS_PATH = PROJECT_ROOT / "knowledge_base" / "negative_facts.md"
DEFAULT_STATE_DIR = PROJECT_ROOT / "outputs" / "state"

# --- CONFIG LOADER ---
# Try to load thresholds from centralized config, fall back to defaults
try:
    from config_loader import get_temporal_thresholds, get_vendor_domains
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

def _get_suggestion_thresholds() -> dict:
    """Get thresholds for suggestion generation, from config or defaults."""
    defaults = {
        'min_times_tried': 3,
        'min_time_wasted_minutes': 30,
        'min_banks_for_pattern': 2,
        'minutes_per_result_reviewed': 2,
    }

    if CONFIG_AVAILABLE:
        try:
            # Try to get from temporal thresholds config
            temporal = get_temporal_thresholds()
            # These could be added to config in the future
            return defaults
        except Exception:
            pass

    return defaults

# --- THRESHOLDS (loaded from config or defaults) ---
_thresholds = _get_suggestion_thresholds()
MIN_TIMES_TRIED = _thresholds['min_times_tried']
MIN_TIME_WASTED_MINUTES = _thresholds['min_time_wasted_minutes']
MIN_BANKS_FOR_PATTERN = _thresholds['min_banks_for_pattern']
MINUTES_PER_RESULT_REVIEWED = _thresholds['minutes_per_result_reviewed']


# --- DATA CLASSES ---

@dataclass
class NullSearchPattern:
    """A search pattern that yielded no useful results."""
    queries: list
    category: str
    bank_id: str
    null_type: str  # NO_RESULTS, IRRELEVANT, PAYWALLED, OUTDATED_ONLY
    times_tried: int
    informative_absence: bool
    implication: str
    time_wasted_minutes: int = 0


@dataclass
class FalseLead:
    """A pattern that appeared promising but yielded nothing useful."""
    misleading_signal: str
    reality: str
    why_confuses: str
    lesson: str
    banks_affected: list
    time_wasted_minutes: int = 0
    pattern_name: str = ""


@dataclass
class VendorCaution:
    """A vendor claim without bank confirmation."""
    vendor_domain: str
    claim_made: str
    bank_id: str
    requires_corroboration: str
    evidence_id: str


@dataclass
class JurisdictionPattern:
    """A jurisdiction-specific search failure pattern."""
    jurisdiction: str
    pattern_to_avoid: str
    reason: str
    better_approach: str
    banks_affected: list


@dataclass
class Suggestion:
    """A formatted suggestion for negative_facts.md."""
    section: str  # A, B, C, D, E, F, or G
    content: str  # Markdown formatted for that section
    confidence: float  # 0-1, higher = more certain
    source_bank: str
    source_evidence_ids: list = field(default_factory=list)
    pattern_key: str = ""  # For duplicate detection


class NegativeFactsSuggester:
    """
    Post-research analysis tool that suggests additions to negative_facts.md.

    Analyzes completed bank research (evidence.json, status.json) to detect:
    - Dead-end search patterns
    - False leads
    - Jurisdiction patterns
    - Vendor cautions
    - Time savings estimates
    """

    def __init__(self,
                 knowledge_base_path: Optional[Path] = None,
                 state_dir: Optional[Path] = None):
        """
        Initialize the suggester.

        Args:
            knowledge_base_path: Path to negative_facts.md
            state_dir: Path to outputs/state/ for cross-bank tracking
        """
        self.knowledge_base_path = Path(knowledge_base_path or DEFAULT_NEGATIVE_FACTS_PATH)
        self.state_dir = Path(state_dir or DEFAULT_STATE_DIR)
        self.existing_patterns: set = set()
        self._load_existing_patterns()

    def _load_existing_patterns(self):
        """Load existing patterns from negative_facts.md to avoid duplicates."""
        if not self.knowledge_base_path.exists():
            logger.warning(f"Negative facts file not found: {self.knowledge_base_path}")
            return

        content = self.knowledge_base_path.read_text(encoding='utf-8')

        # Extract patterns from tables (| pattern | reason |)
        table_patterns = re.findall(r'\|\s*`?([^|`]+)`?\s*\|', content)
        for p in table_patterns:
            normalized = self._normalize_pattern(p)
            if len(normalized) > 5:  # Skip short/header patterns
                self.existing_patterns.add(normalized)

        # Extract patterns from bullet points (- **Pattern**: ...)
        bullet_patterns = re.findall(r'\*\*Misleading Signal\*\*:\s*(.+)', content)
        for p in bullet_patterns:
            normalized = self._normalize_pattern(p)
            if len(normalized) > 5:
                self.existing_patterns.add(normalized)

        # Extract section headers as patterns
        headers = re.findall(r'###\s+(.+)', content)
        for h in headers:
            normalized = self._normalize_pattern(h)
            if len(normalized) > 3:
                self.existing_patterns.add(normalized)

        logger.debug(f"Loaded {len(self.existing_patterns)} existing patterns")

    def _normalize_pattern(self, pattern: str) -> str:
        """Normalize a pattern for comparison."""
        # Remove bank-specific names, dates, URLs
        normalized = pattern.lower().strip()
        normalized = re.sub(r'\[bank\]', '', normalized)
        normalized = re.sub(r'\d{4}', '', normalized)  # Remove years
        normalized = re.sub(r'https?://\S+', '', normalized)  # Remove URLs
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized

    def _is_duplicate(self, suggestion: Suggestion) -> bool:
        """Check if a suggestion matches an existing pattern."""
        normalized = self._normalize_pattern(suggestion.content)

        # Check exact match
        if normalized in self.existing_patterns:
            return True

        # Check fuzzy match (50%+ word overlap)
        suggestion_words = set(normalized.split())
        for existing in self.existing_patterns:
            existing_words = set(existing.split())
            if len(suggestion_words) >= 3 and len(existing_words) >= 3:
                overlap = suggestion_words & existing_words
                if len(overlap) >= len(suggestion_words) * 0.5:
                    return True

        return False

    def analyze_bank(self, bank_dir: Path) -> list:
        """
        Analyze a completed bank research session.

        Args:
            bank_dir: Path to bank output directory (contains evidence.json)

        Returns:
            List of Suggestion objects
        """
        bank_dir = Path(bank_dir)
        evidence_path = bank_dir / "evidence.json"
        status_path = bank_dir / "status.json"

        if not evidence_path.exists():
            logger.warning(f"evidence.json not found in {bank_dir}")
            return []

        # Load evidence.json with error handling
        try:
            evidence = json.loads(evidence_path.read_text(encoding='utf-8'))
            if not isinstance(evidence, dict):
                logger.error(f"evidence.json is not a valid object in {bank_dir}")
                return []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse evidence.json in {bank_dir}: {e}")
            return []
        except Exception as e:
            logger.error(f"Failed to read evidence.json in {bank_dir}: {e}")
            return []

        # Load optional status.json
        status = {}
        if status_path.exists():
            try:
                status = json.loads(status_path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Could not load status.json: {e}")

        suggestions = []

        # Detect dead-end searches
        dead_ends = self._detect_dead_end_searches(evidence)
        for de in dead_ends:
            suggestion = self._format_dead_end_suggestion(de)
            if suggestion and not self._is_duplicate(suggestion):
                suggestions.append(suggestion)

        # Detect false leads
        false_leads = self._detect_false_leads(evidence, status)
        for fl in false_leads:
            suggestion = self._format_false_lead_suggestion(fl)
            if suggestion and not self._is_duplicate(suggestion):
                suggestions.append(suggestion)

        # Detect jurisdiction patterns
        jurisdiction_patterns = self._detect_jurisdiction_patterns(evidence)
        for jp in jurisdiction_patterns:
            suggestion = self._format_jurisdiction_suggestion(jp)
            if suggestion and not self._is_duplicate(suggestion):
                suggestions.append(suggestion)

        # Detect vendor cautions
        vendor_cautions = self._detect_vendor_cautions(evidence)
        for vc in vendor_cautions:
            suggestion = self._format_vendor_caution_suggestion(vc)
            if suggestion and not self._is_duplicate(suggestion):
                suggestions.append(suggestion)

        # Calculate time savings
        time_suggestion = self._calculate_time_savings(dead_ends, false_leads, evidence)
        if time_suggestion and not self._is_duplicate(time_suggestion):
            suggestions.append(time_suggestion)

        logger.info(f"Generated {len(suggestions)} suggestions for {bank_dir.name}")
        return suggestions

    def _detect_dead_end_searches(self, evidence: dict) -> list:
        """Detect search patterns that repeatedly failed."""
        patterns = []

        null_results = evidence.get('null_results', [])
        search_tracking = evidence.get('search_tracking', {})
        bank_id = evidence.get('bank_id', 'unknown')

        # Build mapping of null result categories
        for nr in null_results:
            category = nr.get('category', 'Unknown')
            queries = nr.get('queries', [])
            results_reviewed = nr.get('results_reviewed', 10)
            informative = nr.get('informative_absence', False)

            # Skip informative absences - they tell us something useful
            if informative:
                continue

            time_wasted = results_reviewed * MINUTES_PER_RESULT_REVIEWED

            # Only flag if exceeds thresholds
            if len(queries) >= MIN_TIMES_TRIED or time_wasted >= MIN_TIME_WASTED_MINUTES:
                patterns.append(NullSearchPattern(
                    queries=queries,
                    category=category,
                    bank_id=bank_id,
                    null_type=nr.get('null_type', 'NO_RESULTS'),
                    times_tried=len(queries),
                    informative_absence=informative,
                    implication=nr.get('implication', ''),
                    time_wasted_minutes=time_wasted
                ))

        return patterns

    def _detect_false_leads(self, evidence: dict, status: dict) -> list:
        """Detect patterns that appeared promising but yielded nothing."""
        false_leads = []
        bank_id = evidence.get('bank_id', 'unknown')
        items = evidence.get('evidence_items', [])

        # Pattern 1: Vendor claims without bank confirmation
        vendor_items = [i for i in items if i.get('claim_type') == 'vendor_proxy_signal']
        confirmed_items = [i for i in items if i.get('claim_type') in
                         ['production_usage', 'pilot_or_poc']]

        for vi in vendor_items:
            vendor_scope = set(vi.get('product_scope', []))
            vendor_jurisdiction = set(vi.get('jurisdiction_scope', []))

            # Check if same scope has bank confirmation
            confirmed = False
            for ci in confirmed_items:
                ci_scope = set(ci.get('product_scope', []))
                ci_jurisdiction = set(ci.get('jurisdiction_scope', []))

                # Handle empty scopes as "unknown" = could match anything
                # If either has empty scope, treat as potential match
                scope_match = (not vendor_scope or not ci_scope or (vendor_scope & ci_scope))
                jurisdiction_match = (not vendor_jurisdiction or not ci_jurisdiction or
                                     (vendor_jurisdiction & ci_jurisdiction))

                # Confirmed if both scope and jurisdiction could match
                if scope_match and jurisdiction_match:
                    confirmed = True
                    break

            if not confirmed:
                # Extract vendor domain from URL
                source_url = vi.get('source_url', '')
                vendor_domain = self._extract_domain(source_url)

                false_leads.append(FalseLead(
                    misleading_signal=f"Vendor claim from {vendor_domain}: {vi.get('claim', '')[:80]}...",
                    reality="Vendor press release; bank has not confirmed CDM usage in this scope",
                    why_confuses="Vendor marketing appears authoritative but may overstate bank's CDM adoption",
                    lesson="Require bank-side confirmation for vendor claims before classifying as production_usage",
                    banks_affected=[bank_id],
                    time_wasted_minutes=30,
                    pattern_name=f"Vendor claim without confirmation ({vendor_domain})"
                ))

        # Pattern 2: Historical pilot without current evidence
        pilot_items = [i for i in items if i.get('claim_type') == 'pilot_or_poc']
        for pi in pilot_items:
            quality = pi.get('quality_assessment', {})
            recency = quality.get('recency', 'current')
            # Check freshness.weight_multiplier (calculated by trust_audit) or fall back to recency
            freshness = pi.get('freshness', {})
            weight_multiplier = freshness.get('weight_multiplier', 1.0)

            # Check if pilot is historical (>3 years old or low weight multiplier)
            if recency == 'historical' or weight_multiplier <= 0.3:
                # Check for current follow-through
                current_items = [i for i in items
                               if i.get('quality_assessment', {}).get('recency') == 'current'
                               and i.get('claim_type') in ['production_usage', 'pilot_or_poc']]

                if not current_items:
                    false_leads.append(FalseLead(
                        misleading_signal=f"Historical pilot: {pi.get('claim', '')[:80]}...",
                        reality="Pilot participation did not lead to current production adoption",
                        why_confuses="Historical pilot activity suggests momentum that may have stalled",
                        lesson="Check for sustained follow-through post-pilot; look for evidence within last 2 years",
                        banks_affected=[bank_id],
                        time_wasted_minutes=45,
                        pattern_name="Historical pilot without follow-through"
                    ))

        # Pattern 3: FINOS non-CDM project participation
        for item in items:
            claim = item.get('claim', '').lower()
            if any(proj in claim for proj in ['fluxnova', 'waltz', 'legend', 'spring bot']):
                if 'cdm' not in claim:
                    project_name = next((p for p in ['Fluxnova', 'Waltz', 'Legend', 'Spring Bot']
                                        if p.lower() in claim), 'FINOS project')
                    false_leads.append(FalseLead(
                        misleading_signal=f"FINOS {project_name} participation",
                        reality=f"{project_name} is NOT CDM; it's a separate FINOS project",
                        why_confuses="Both are FINOS projects; casual searches conflate them",
                        lesson="Verify the specific FINOS project is CDM-related, not just FINOS membership",
                        banks_affected=[bank_id],
                        time_wasted_minutes=20,
                        pattern_name=f"{project_name} != CDM"
                    ))

        return false_leads

    def _detect_jurisdiction_patterns(self, evidence: dict) -> list:
        """Detect jurisdiction-specific search failure patterns."""
        patterns = []
        bank_id = evidence.get('bank_id', 'unknown')
        null_results = evidence.get('null_results', [])

        # Infer jurisdiction from bank name or null results
        jurisdiction_nulls = defaultdict(list)

        bank_name = evidence.get('bank_name', bank_id).lower()

        # Determine primary jurisdiction
        if any(x in bank_name for x in ['ubs', 'credit suisse', 'swiss', 'pictet', 'julius baer']):
            primary_jurisdiction = 'Swiss'
        elif any(x in bank_name for x in ['deutsche', 'commerzbank', 'german']):
            primary_jurisdiction = 'German'
        elif any(x in bank_name for x in ['nomura', 'mufg', 'mizuho', 'smbc', 'daiwa', 'japan']):
            primary_jurisdiction = 'Japanese'
        elif any(x in bank_name for x in ['hsbc', 'barclays', 'lloyds', 'natwest', 'uk']):
            primary_jurisdiction = 'UK'
        else:
            primary_jurisdiction = None

        if primary_jurisdiction:
            # Check for site-restricted search failures
            for nr in null_results:
                queries = nr.get('queries', [])
                for q in queries:
                    q_lower = q.lower()
                    if 'site:' in q_lower:
                        jurisdiction_nulls[primary_jurisdiction].append({
                            'query': q,
                            'category': nr.get('category', ''),
                            'null_type': nr.get('null_type', 'NO_RESULTS')
                        })

        # Generate patterns for jurisdictions with failures
        for jurisdiction, nulls in jurisdiction_nulls.items():
            if len(nulls) >= 2:
                patterns.append(JurisdictionPattern(
                    jurisdiction=jurisdiction,
                    pattern_to_avoid=f"Site-restricted searches for {jurisdiction} banks",
                    reason=f"{len(nulls)} null results from site-restricted searches",
                    better_approach=self._suggest_jurisdiction_alternative(jurisdiction),
                    banks_affected=[bank_id]
                ))

        return patterns

    def _detect_vendor_cautions(self, evidence: dict) -> list:
        """Detect vendor claims that need extra scrutiny."""
        cautions = []
        bank_id = evidence.get('bank_id', 'unknown')
        items = evidence.get('evidence_items', [])

        # Known vendor domains to flag
        vendor_domains = {
            'murex.com': 'Murex platform vendor',
            'calypso.com': 'Calypso platform vendor',
            'finastra.com': 'Finastra platform vendor',
            'deltacapita.com': 'Delta Capita services vendor',
            'regnosys.com': 'REGnosys CDM tooling vendor',
            'opensesafi.com': 'OpenSesame vendor',
        }

        # Claim types that are already appropriately classified (no caution needed)
        valid_claim_types = {'vendor_proxy_signal', 'production_usage', 'pilot_or_poc'}

        for item in items:
            source_url = item.get('source_url', '')
            domain = self._extract_domain(source_url)
            claim_type = item.get('claim_type', '')

            # Only flag if from vendor domain AND not already correctly classified
            if domain in vendor_domains and claim_type not in valid_claim_types:
                # Found vendor domain being treated as non-vendor evidence
                cautions.append(VendorCaution(
                    vendor_domain=domain,
                    claim_made=item.get('claim', '')[:100],
                    bank_id=bank_id,
                    requires_corroboration=f"Bank confirmation of {vendor_domains[domain]} CDM adoption",
                    evidence_id=item.get('id', '')
                ))

        return cautions

    def _calculate_time_savings(self, dead_ends: list, false_leads: list, evidence: dict) -> Optional[Suggestion]:
        """Calculate time savings estimate for this bank's patterns."""
        total_minutes = 0

        for de in dead_ends:
            total_minutes += de.time_wasted_minutes

        for fl in false_leads:
            total_minutes += fl.time_wasted_minutes

        if total_minutes < 30:
            return None

        bank_id = evidence.get('bank_id', 'unknown')
        hours = total_minutes / 60

        # Determine bank type for pattern naming
        bank_name = evidence.get('bank_name', bank_id).lower()
        if 'swiss' in bank_name or any(x in bank_name for x in ['ubs', 'credit suisse', 'pictet']):
            bank_type = "Swiss bank"
        elif 'german' in bank_name or any(x in bank_name for x in ['deutsche', 'commerzbank']):
            bank_type = "German bank"
        elif 'japan' in bank_name or any(x in bank_name for x in ['nomura', 'mufg', 'mizuho', 'smbc']):
            bank_type = "Japanese bank"
        else:
            bank_type = "similar bank"

        content = f"| Dead-end patterns for {bank_type}s | {hours:.1f} hours |"

        return Suggestion(
            section='F',
            content=content,
            confidence=0.7,
            source_bank=bank_id,
            source_evidence_ids=[],
            pattern_key=f"time_savings_{bank_type}"
        )

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        return match.group(1) if match else ''

    def _suggest_jurisdiction_alternative(self, jurisdiction: str) -> str:
        """Suggest alternative search approach for a jurisdiction."""
        alternatives = {
            'Swiss': "Check ISDA/FINOS repos and trade press first; Swiss discretion norms limit public positioning",
            'German': "Include German terms; technical documentation often in German",
            'Japanese': "Check Japanese trade publications or ISDA Asia events; internal work not publicized in English",
            'UK': "Target trade press (Risk.net) specifically; innovation press focuses on retail",
        }
        return alternatives.get(jurisdiction, "Check trade press and official repos")

    # --- FORMATTERS ---

    def _format_dead_end_suggestion(self, pattern: NullSearchPattern) -> Optional[Suggestion]:
        """Format dead-end pattern for Section A."""
        if not pattern.queries:
            return None

        query_example = pattern.queries[0] if pattern.queries else pattern.category
        reason = f"Tried {pattern.times_tried}x with no useful results; {pattern.null_type}"
        alternative = f"Try more specific CDM-focused query or check official sources"

        content = f"| `{query_example}` | {reason} | {alternative} |"

        return Suggestion(
            section='A',
            content=content,
            confidence=min(0.9, 0.5 + pattern.times_tried * 0.1),
            source_bank=pattern.bank_id,
            source_evidence_ids=[],
            pattern_key=self._normalize_pattern(query_example)
        )

    def _format_false_lead_suggestion(self, lead: FalseLead) -> Optional[Suggestion]:
        """Format false lead for Section B."""
        content = f"""
### {lead.pattern_name or 'Discovered Pattern'}

- **Misleading Signal**: {lead.misleading_signal}
- **Reality**: {lead.reality}
- **Why It Confuses**: {lead.why_confuses}
- **Lesson**: {lead.lesson}
- **Banks affected**: {', '.join(lead.banks_affected)}
- **Time wasted**: ~{lead.time_wasted_minutes} minutes
""".strip()

        return Suggestion(
            section='B',
            content=content,
            confidence=0.7,
            source_bank=lead.banks_affected[0] if lead.banks_affected else 'unknown',
            source_evidence_ids=[],
            pattern_key=self._normalize_pattern(lead.misleading_signal)
        )

    def _format_jurisdiction_suggestion(self, pattern: JurisdictionPattern) -> Optional[Suggestion]:
        """Format jurisdiction pattern for Section A (jurisdiction-specific)."""
        content = f"| **{pattern.jurisdiction} banks** | `{pattern.pattern_to_avoid}` | {pattern.reason} | {pattern.better_approach} |"

        return Suggestion(
            section='A',
            content=content,
            confidence=0.6,
            source_bank=pattern.banks_affected[0] if pattern.banks_affected else 'unknown',
            source_evidence_ids=[],
            pattern_key=f"jurisdiction_{pattern.jurisdiction.lower()}"
        )

    def _format_vendor_caution_suggestion(self, caution: VendorCaution) -> Optional[Suggestion]:
        """Format vendor caution for Section E."""
        content = f"| {caution.vendor_domain} | Vendor marketing | {caution.requires_corroboration} |"

        return Suggestion(
            section='E',
            content=content,
            confidence=0.8,
            source_bank=caution.bank_id,
            source_evidence_ids=[caution.evidence_id],
            pattern_key=f"vendor_{caution.vendor_domain}"
        )

    # --- PHASE-LEVEL ANALYSIS ---

    def analyze_phase(self, phase_dir: Path) -> list:
        """
        Analyze all banks in a phase for cross-bank patterns.

        Args:
            phase_dir: Path to phase directory (contains bank subdirectories)

        Returns:
            List of Suggestion objects
        """
        phase_dir = Path(phase_dir)
        all_suggestions = []
        pattern_tracker = defaultdict(list)  # pattern_key -> [bank_ids]

        # First, analyze each bank individually
        for bank_dir in sorted(phase_dir.iterdir()):
            if not bank_dir.is_dir():
                continue

            evidence_path = bank_dir / "evidence.json"
            if not evidence_path.exists():
                continue

            bank_suggestions = self.analyze_bank(bank_dir)

            # Track patterns across banks
            for suggestion in bank_suggestions:
                if suggestion.pattern_key:
                    pattern_tracker[suggestion.pattern_key].append(suggestion.source_bank)

            all_suggestions.extend(bank_suggestions)

        # Identify cross-bank patterns (appear in 2+ banks)
        cross_bank_suggestions = []
        for pattern_key, banks in pattern_tracker.items():
            if len(banks) >= MIN_BANKS_FOR_PATTERN:
                # Create a high-confidence cross-bank suggestion
                cross_bank_suggestions.append(Suggestion(
                    section='G',
                    content=self._format_phase_pattern(pattern_key, banks),
                    confidence=min(0.95, 0.6 + len(banks) * 0.1),
                    source_bank=', '.join(banks),
                    source_evidence_ids=[],
                    pattern_key=f"crossbank_{pattern_key}"
                ))

        # Merge: keep cross-bank versions, remove individual duplicates
        final_suggestions = []
        cross_bank_keys = {s.pattern_key.replace('crossbank_', '') for s in cross_bank_suggestions}

        for s in all_suggestions:
            if s.pattern_key not in cross_bank_keys:
                final_suggestions.append(s)

        final_suggestions.extend(cross_bank_suggestions)

        logger.info(f"Phase analysis: {len(final_suggestions)} suggestions ({len(cross_bank_suggestions)} cross-bank patterns)")
        return final_suggestions

    def _format_phase_pattern(self, pattern_key: str, banks: list) -> str:
        """Format cross-bank pattern for Section G."""
        return f"""
- **{pattern_key.replace('_', ' ').title()}**: Pattern observed in {', '.join(banks)}
  - Confidence: High (observed in {len(banks)} banks)
  - Recommendation: Skip this search pattern for similar banks in future phases
""".strip()

    # --- APPLY SUGGESTIONS ---

    def apply_suggestions(self, suggestions: list, interactive: bool = True) -> int:
        """
        Apply approved suggestions to negative_facts.md.

        Args:
            suggestions: List of Suggestion objects
            interactive: If True, prompt for each suggestion

        Returns:
            Number of suggestions applied
        """
        if not suggestions:
            print("No suggestions to apply.")
            return 0

        if not self.knowledge_base_path.exists():
            logger.error(f"Cannot apply: {self.knowledge_base_path} does not exist")
            return 0

        content = self.knowledge_base_path.read_text(encoding='utf-8')
        applied_count = 0

        # Group suggestions by section
        by_section = defaultdict(list)
        for s in suggestions:
            by_section[s.section].append(s)

        if interactive:
            print("\n" + "=" * 70)
            print("  NEGATIVE FACTS SUGGESTIONS")
            print("=" * 70)

        for section, section_suggestions in sorted(by_section.items()):
            section_name = self._get_section_name(section)

            if interactive:
                print(f"\n[Section {section}: {section_name}]")
                print("-" * 50)

            for i, suggestion in enumerate(section_suggestions, 1):
                if interactive:
                    print(f"\n{i}. Confidence: {suggestion.confidence:.0%}")
                    print(f"   Source: {suggestion.source_bank}")
                    print(f"   Content:")
                    for line in suggestion.content.split('\n'):
                        print(f"      {line}")

                    response = input("\n   Add this suggestion? [Y/n]: ").strip().lower()
                    if response in ['', 'y', 'yes']:
                        content = self._insert_suggestion(content, suggestion)
                        applied_count += 1
                        print("   [Added]")
                    else:
                        print("   [Skipped]")
                else:
                    content = self._insert_suggestion(content, suggestion)
                    applied_count += 1

        if applied_count > 0:
            # Update timestamp
            today = datetime.now().strftime('%Y-%m-%d')
            content = re.sub(
                r'\*\*Last Updated\*\*:\s*\d{4}-\d{2}-\d{2}',
                f'**Last Updated**: {today}',
                content
            )

            self.knowledge_base_path.write_text(content, encoding='utf-8')
            print(f"\n[SUCCESS] Applied {applied_count} suggestions to {self.knowledge_base_path}")

        return applied_count

    def _get_section_name(self, section: str) -> str:
        """Get human-readable section name."""
        names = {
            'A': 'Dead End Search Patterns',
            'B': 'False Leads Registry',
            'C': 'Debunked Claims',
            'D': 'Informative Absences',
            'E': 'Vendor Domain Cautions',
            'F': 'Time Savings Estimates',
            'G': 'Pattern Recognition by Phase',
        }
        return names.get(section, section)

    def _insert_suggestion(self, content: str, suggestion: Suggestion) -> str:
        """Insert a suggestion into the appropriate section of the markdown."""
        section_markers = {
            'A': r'(## A\. Dead End Search Patterns.*?)(\n---|\n## B)',
            'B': r'(## B\. False Leads Registry.*?)(\n---|\n## C)',
            'C': r'(## C\. Debunked Claims.*?)(\n---|\n## D)',
            'D': r'(## D\. Informative Absences.*?)(\n---|\n## E)',
            'E': r'(## E\. Vendor Domain Cautions.*?)(\n---|\n## F)',
            'F': r'(## F\. Time Savings Estimates.*?)(\n---|\n## G)',
            'G': r'(## G\. Pattern Recognition by Phase.*?)(\n---|\n## H)',
        }

        marker = section_markers.get(suggestion.section)
        if not marker:
            logger.warning(f"Unknown section: {suggestion.section}")
            return content

        match = re.search(marker, content, re.DOTALL)
        if match:
            section_content = match.group(1)
            separator = match.group(2)

            # Add suggestion before the separator
            new_section = section_content.rstrip() + '\n\n' + suggestion.content + '\n'
            content = content.replace(section_content, new_section)

        return content

    def save_suggestions_to_file(self, suggestions: list, output_path: Path):
        """Save suggestions to JSON file for batch review."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'generated_at': datetime.now().isoformat(),
            'suggestion_count': len(suggestions),
            'suggestions': [asdict(s) for s in suggestions]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved {len(suggestions)} suggestions to {output_path}")

    def load_suggestions_from_file(self, input_path: Path) -> list:
        """Load suggestions from JSON file."""
        input_path = Path(input_path)

        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        suggestions = []
        for s_data in data.get('suggestions', []):
            suggestions.append(Suggestion(**s_data))

        return suggestions


def print_suggestions(suggestions: list):
    """Print suggestions in a readable format."""
    if not suggestions:
        print("No suggestions found.")
        return

    print("\n" + "=" * 70)
    print(f"  NEGATIVE FACTS SUGGESTIONS ({len(suggestions)} total)")
    print("=" * 70)

    by_section = defaultdict(list)
    for s in suggestions:
        by_section[s.section].append(s)

    section_names = {
        'A': 'Dead End Search Patterns',
        'B': 'False Leads Registry',
        'C': 'Debunked Claims',
        'D': 'Informative Absences',
        'E': 'Vendor Domain Cautions',
        'F': 'Time Savings Estimates',
        'G': 'Pattern Recognition by Phase',
    }

    for section in sorted(by_section.keys()):
        section_suggestions = by_section[section]
        print(f"\n[Section {section}: {section_names.get(section, section)}] ({len(section_suggestions)} suggestions)")
        print("-" * 50)

        for i, s in enumerate(section_suggestions, 1):
            print(f"\n{i}. Confidence: {s.confidence:.0%} | Source: {s.source_bank}")
            for line in s.content.split('\n'):
                if line.strip():
                    print(f"   {line}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Suggest additions to negative_facts.md after bank research"
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Analyze single bank
    analyze_parser = subparsers.add_parser('analyze', help='Analyze completed bank')
    analyze_parser.add_argument('bank_dir', help='Path to bank output directory')
    analyze_parser.add_argument('--interactive', '-i', action='store_true',
                               help='Prompt for approval before adding')
    analyze_parser.add_argument('--dry-run', action='store_true',
                               help='Show suggestions without modifying files')
    analyze_parser.add_argument('--output', '-o', help='Output file for suggestions JSON')

    # Phase-level analysis
    phase_parser = subparsers.add_parser('phase', help='Analyze all banks in phase')
    phase_parser.add_argument('phase_dir', help='Path to phase directory')
    phase_parser.add_argument('--output', '-o',
                             help='Output file for suggestions JSON')
    phase_parser.add_argument('--apply', action='store_true',
                             help='Apply suggestions interactively')

    # Apply suggestions from file
    apply_parser = subparsers.add_parser('apply', help='Apply suggestions from file')
    apply_parser.add_argument('suggestions_file', help='Path to suggestions JSON file')
    apply_parser.add_argument('--all', action='store_true',
                             help='Apply all without prompting')

    # List pending suggestions
    list_parser = subparsers.add_parser('list', help='List pending suggestion files')
    list_parser.add_argument('--state-dir', default=str(DEFAULT_STATE_DIR),
                            help='State directory to search')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    suggester = NegativeFactsSuggester()

    if args.command == 'analyze':
        suggestions = suggester.analyze_bank(Path(args.bank_dir))

        if args.dry_run:
            print_suggestions(suggestions)
        elif args.output:
            suggester.save_suggestions_to_file(suggestions, Path(args.output))
        elif args.interactive:
            suggester.apply_suggestions(suggestions, interactive=True)
        else:
            print_suggestions(suggestions)
            print("\nUse --interactive to apply, --dry-run to preview, or --output to save")

    elif args.command == 'phase':
        suggestions = suggester.analyze_phase(Path(args.phase_dir))

        if args.output:
            suggester.save_suggestions_to_file(suggestions, Path(args.output))

        if args.apply:
            suggester.apply_suggestions(suggestions, interactive=True)
        else:
            print_suggestions(suggestions)
            if not args.output:
                print("\nUse --apply to apply interactively, or --output to save")

    elif args.command == 'apply':
        suggestions = suggester.load_suggestions_from_file(Path(args.suggestions_file))
        count = suggester.apply_suggestions(suggestions, interactive=not args.all)
        print(f"\nApplied {count} suggestions")

    elif args.command == 'list':
        state_dir = Path(args.state_dir)
        if not state_dir.exists():
            print(f"State directory not found: {state_dir}")
            sys.exit(1)

        suggestion_files = list(state_dir.glob("negative-facts-*.json"))
        if not suggestion_files:
            print("No pending suggestion files found.")
        else:
            print(f"Found {len(suggestion_files)} suggestion file(s):")
            for f in sorted(suggestion_files):
                with open(f) as fp:
                    data = json.load(fp)
                    count = data.get('suggestion_count', 0)
                    generated = data.get('generated_at', 'unknown')
                print(f"  - {f.name}: {count} suggestions (generated: {generated})")


if __name__ == "__main__":
    main()
