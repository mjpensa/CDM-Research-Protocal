"""
CDM Research Protocol - Research Executor v2.1

IMPORTANT: This tool requires an external Anthropic API key.
For Claude Code extension users (VS Code with Max subscription), use
claude_code_executor.py instead - it works with Claude Code's built-in
WebSearch without needing a separate API key.

This module executes live research by calling the Anthropic API directly.
Designed for automated batch processing scenarios where Claude Code
extension is not available.

Usage:
    # Called by batch_orchestrate.py for external API batch runs
    from research_executor import execute_research

    # Or run standalone (requires ANTHROPIC_API_KEY)
    python tools/research_executor.py --bank deutsche-bank --phase 1
    python tools/research_executor.py --bank deutsche-bank --phase 1 --show-prompts

Requirements:
    pip install anthropic
    ANTHROPIC_API_KEY environment variable

For Claude Code Extension Users:
    Use claude_code_executor.py or run research interactively via Claude Code.
    Claude Code has built-in WebSearch - no external API needed.
"""

import os
import sys
import json
import logging
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict, field

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import (
    load_bank_manifest, get_bank_config, load_decision_thresholds,
    load_bayesian_tables, get_api_model, get_api_retry_config,
    get_api_timeout, load_api_config
)

# State management integration (Phase 3 fix for Issue #2)
from state_manager import UnifiedStateManager
from state_adapter import sync_research_state_to_bank_state, convert_research_state_to_bank_state

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Try to import anthropic
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("anthropic package not installed. Install with: pip install anthropic")


@dataclass
class EvidenceItem:
    """A single piece of evidence found during research."""
    id: str
    claim: str
    source_url: str
    source_date: Optional[str]
    tier: int
    claim_type: str
    excerpt: str
    confidence: int  # 1-10
    supports_architect: bool  # True if supports ARCHITECT, False if supports PRAGMATIST


@dataclass
class ResearchStageResult:
    """Result from a single research stage."""
    stage: str
    success: bool
    output_file: Optional[str]
    evidence_items: List[EvidenceItem]
    probability_update: Optional[float]
    notes: str
    raw_response: Optional[str] = None


@dataclass
class ResearchState:
    """
    Complete state of research for a bank.

    NOTE: All probability values use 0-1 scale (not 0-100).
    For display, format as: f"{prob * 100:.1f}%"
    """
    bank_id: str
    bank_name: str
    phase: int
    probability_architect: float  # 0-1 scale
    probability_pragmatist: float  # 0-1 scale (= 1 - probability_architect)
    classification: Optional[str] = None
    sub_classification: Optional[str] = None
    confidence: Optional[int] = None
    current_stage: str = "initialized"
    evidence_items: List[EvidenceItem] = field(default_factory=list)
    highest_tier: int = 0
    stages_completed: List[str] = field(default_factory=list)
    adversarial_verdict: Optional[str] = None
    trust_flags: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None


class IncrementalEvidenceCheckpointer:
    """
    Saves evidence incrementally during tier collection.

    Category 3 fix: Intra-Stage Checkpointing
    - Uses staging files that survive crashes
    - Checkpoints after EVERY evidence item (per-item granularity)
    - Supports crash recovery to resume from last checkpoint

    Usage:
        checkpointer = IncrementalEvidenceCheckpointer(bank_dir, bank_id, tier)
        checkpointer.add_evidence({"claim": "...", "source_url": "..."})
        checkpointer.finalize()  # After successful tier completion
        checkpointer.cleanup()   # Remove staging file
    """

    def __init__(self, bank_dir: Path, bank_id: str, tier: int):
        """
        Initialize checkpointer for a specific tier.

        Args:
            bank_dir: Bank output directory
            bank_id: Bank identifier
            tier: Evidence tier (1, 2, or 3)
        """
        self.bank_dir = bank_dir
        self.bank_id = bank_id
        self.tier = tier
        self.staging_path = bank_dir / f"evidence.staging.tier{tier}.json"
        self.evidence_items: List[Dict[str, Any]] = []
        self.raw_response: Optional[str] = None

    def add_evidence(self, item: Dict[str, Any]) -> None:
        """
        Add item and checkpoint immediately (per-item granularity).

        Args:
            item: Evidence item dictionary
        """
        self.evidence_items.append(item)
        self._checkpoint()  # Checkpoint after EVERY item

    def set_raw_response(self, response: str) -> None:
        """
        Store raw response and checkpoint.

        Args:
            response: Raw response from Claude API
        """
        self.raw_response = response
        self._checkpoint()

    def _checkpoint(self) -> None:
        """Atomically save current evidence to staging file."""
        data = {
            "bank_id": self.bank_id,
            "tier": self.tier,
            "checkpoint_time": datetime.now(timezone.utc).isoformat(),
            "evidence_items": self.evidence_items,
            "raw_response": self.raw_response,
            "status": "in_progress",
            "item_count": len(self.evidence_items)
        }

        # Atomic write: write to temp, then rename
        temp_path = self.staging_path.with_suffix('.tmp')
        try:
            temp_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
            temp_path.replace(self.staging_path)
        except Exception as e:
            logger.warning(f"Checkpoint write failed: {e}")
            # Don't raise - checkpointing failure shouldn't stop research

    def finalize(self) -> List[Dict[str, Any]]:
        """
        Mark checkpoint as complete and return items.

        Returns:
            List of evidence items collected
        """
        data = {
            "bank_id": self.bank_id,
            "tier": self.tier,
            "checkpoint_time": datetime.now(timezone.utc).isoformat(),
            "evidence_items": self.evidence_items,
            "raw_response": self.raw_response,
            "status": "complete",
            "item_count": len(self.evidence_items)
        }

        temp_path = self.staging_path.with_suffix('.tmp')
        try:
            temp_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
            temp_path.replace(self.staging_path)
        except Exception as e:
            logger.warning(f"Finalize checkpoint failed: {e}")

        return self.evidence_items

    def cleanup(self) -> None:
        """Remove staging file after successful merge to main evidence file."""
        try:
            if self.staging_path.exists():
                self.staging_path.unlink()
                logger.debug(f"Cleaned up staging file: {self.staging_path.name}")
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")

    @classmethod
    def recover_from_crash(cls, bank_dir: Path) -> Dict[int, Dict[str, Any]]:
        """
        Recover evidence from any staging files after a crash.

        Args:
            bank_dir: Bank output directory

        Returns:
            Dict mapping tier -> recovered data (evidence_items, raw_response)
        """
        recovered = {}

        for staging_file in bank_dir.glob("evidence.staging.tier*.json"):
            try:
                data = json.loads(staging_file.read_text(encoding='utf-8'))
                tier = data.get("tier")
                status = data.get("status")

                if tier is not None:
                    item_count = len(data.get("evidence_items", []))
                    logger.info(
                        f"Recovered tier {tier} checkpoint: {item_count} items, "
                        f"status={status}"
                    )
                    recovered[tier] = {
                        "evidence_items": data.get("evidence_items", []),
                        "raw_response": data.get("raw_response"),
                        "status": status,
                        "checkpoint_time": data.get("checkpoint_time")
                    }

            except Exception as e:
                logger.warning(f"Recovery failed for {staging_file.name}: {e}")

        return recovered

    @classmethod
    def get_last_completed_tier(cls, bank_dir: Path) -> int:
        """
        Determine which tier to resume from based on staging files.

        Args:
            bank_dir: Bank output directory

        Returns:
            Last completed tier (0 if none completed, 1-3 if completed)
        """
        recovered = cls.recover_from_crash(bank_dir)

        # Find highest tier with "complete" status
        completed_tiers = [
            tier for tier, data in recovered.items()
            if data.get("status") == "complete"
        ]

        return max(completed_tiers) if completed_tiers else 0


# Global state manager instance (initialized per execution)
_state_manager: Optional[UnifiedStateManager] = None


def _get_state_manager() -> UnifiedStateManager:
    """Get or initialize the global state manager."""
    global _state_manager
    if _state_manager is None:
        _state_manager = UnifiedStateManager(PROJECT_ROOT / "outputs")
    return _state_manager


def _sync_to_state_manager(
    state: ResearchState,
    stage: str,
    validate: bool = True
) -> None:
    """
    Sync ResearchState to UnifiedStateManager.

    Converts ResearchState fields to BankState and saves via state manager.
    This ensures all state changes are validated and atomically written.

    Args:
        state: Current ResearchState from research execution
        stage: Current stage name for probability history tracking
        validate: Whether to run validation (default True)
    """
    try:
        sm = _get_state_manager()

        # Try to load existing BankState to preserve history
        existing = sm.load_bank_state(state.bank_id, state.phase)

        # Sync fields from ResearchState to BankState
        bank_state = sync_research_state_to_bank_state(
            state,
            existing_bank_state=existing,
            stage=stage
        )

        # Save with validation
        sm.save_bank_state(bank_state, validate=validate)

        logger.debug(f"State synced to state manager at stage: {stage}")

    except Exception as e:
        # Log but don't fail - state manager issues shouldn't break research
        logger.warning(f"State manager sync failed: {e}")


class ClaudeResearcher:
    """Handles Claude API interactions for research tasks."""

    def __init__(self, model: str = None):
        """
        Initialize the Claude researcher.

        Args:
            model: Claude model to use. If None, loads from config/api-config.json.
                Options:
                - claude-opus-4-5-20250101 (best quality, recommended)
                - claude-sonnet-4-20250514 (faster, cheaper)
        """
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic package required. Install with: pip install anthropic")

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = anthropic.Anthropic(api_key=api_key)

        # Load configuration from api-config.json
        self.model = model if model else get_api_model()
        retry_config = get_api_retry_config()
        self.max_retries = retry_config.get('max_retries', 3)
        self.retry_delay = retry_config.get('retry_delay_seconds', 5)
        self.exponential_backoff = retry_config.get('exponential_backoff', True)
        self.max_delay = retry_config.get('max_delay_seconds', 60)
        self.timeout = get_api_timeout()

        logger.info(f"ClaudeResearcher initialized with model={self.model}, max_retries={self.max_retries}")

    def research_with_web_search(self, prompt: str, max_tokens: int = 4096) -> str:
        """
        Execute research prompt with web search enabled.

        Args:
            prompt: The research prompt
            max_tokens: Maximum response tokens

        Returns:
            Claude's response text
        """
        for attempt in range(self.max_retries):
            try:
                # Use Claude with web search tool
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    tools=[{
                        "type": "web_search_20250305",
                        "name": "web_search",
                        "max_uses": 10
                    }],
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )

                # Extract text from response
                text_parts = []
                for block in response.content:
                    if hasattr(block, 'text'):
                        text_parts.append(block.text)

                return "\n".join(text_parts)

            except anthropic.RateLimitError:
                if attempt < self.max_retries - 1:
                    logger.warning(f"Rate limited, waiting {self.retry_delay}s...")
                    time.sleep(self.retry_delay)
                    self.retry_delay *= 2  # Exponential backoff
                else:
                    raise
            except anthropic.APIError as e:
                logger.error(f"API error: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise

    def analyze(self, prompt: str, max_tokens: int = 4096) -> str:
        """
        Execute analysis prompt (no web search, just reasoning).

        Args:
            prompt: The analysis prompt
            max_tokens: Maximum response tokens

        Returns:
            Claude's response text
        """
        for attempt in range(self.max_retries):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )

                return response.content[0].text

            except anthropic.RateLimitError:
                if attempt < self.max_retries - 1:
                    logger.warning(f"Rate limited, waiting {self.retry_delay}s...")
                    time.sleep(self.retry_delay)
                    self.retry_delay *= 2
                else:
                    raise
            except anthropic.APIError as e:
                logger.error(f"API error: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise


def generate_evidence_prompt(bank_config: dict, tier: int, prior_evidence: str = "") -> str:
    """Generate prompt for evidence gathering."""
    bank_name = bank_config.get('bank_name', bank_config.get('bank_id'))
    research_obj = bank_config.get('research_objective', {})

    tier_sources = {
        1: """Search ONLY these official sources:
- The bank's official website (investor relations, press releases, technology announcements)
- ISDA.org for any mentions of this bank in CDM/DRR context
- FINOS.org and github.com/finos for contribution history
- Regulatory filings (SEC EDGAR, FCA, BaFin, ESMA as relevant to jurisdiction)
- Official annual reports mentioning CDM, DRR, ISDA, or derivatives reporting""",

        2: """Search these industry sources:
- Risk.net for any articles mentioning this bank and CDM/DRR/derivatives reporting
- Waters Technology for technology coverage
- Financial Times, Bloomberg, Reuters for business press coverage
- Conference presentations (ISDA AGM, FINOS events, Sibos)
- Vendor press releases that mention this bank as a client""",

        3: """Search these signal sources:
- Job postings on the bank's careers site mentioning CDM, ISDA, DRR, or derivatives reporting
- LinkedIn for employees with CDM/ISDA experience at this bank
- Patent filings related to derivatives or trade reporting
- Technical blogs and articles by bank employees
- Industry analyst reports mentioning the bank's derivatives strategy"""
    }

    prompt = f"""# CDM/DRR Evidence Gathering - Tier {tier}

## Your Task
You are a financial technology researcher investigating {bank_name}'s adoption of the ISDA Common Domain Model (CDM) and Digital Regulatory Reporting (DRR) standards.

## Bank Profile
- **Name**: {bank_name}
- **Headquarters**: {bank_config.get('headquarters', 'Unknown')}
- **Primary Regulator**: {bank_config.get('primary_regulator', 'Unknown')}
- **Derivatives Relevance**: {bank_config.get('derivatives_relevance', 'Unknown')}
- **Business Model**: {bank_config.get('business_model', 'Unknown')}

## Research Objective
{research_obj.get('primary_goal', 'Assess CDM/DRR adoption status and classify the bank.')}

## Key Questions to Answer
"""

    for q in research_obj.get('key_questions', ['What is this bank doing with CDM/DRR?']):
        prompt += f"- {q}\n"

    prompt += f"""
## Known Evidence (Starting Point)
"""
    for ev in bank_config.get('known_evidence', []):
        prompt += f"- {ev.get('evidence')}: {ev.get('implication', '')}\n"

    if not bank_config.get('known_evidence'):
        prompt += "- No prior evidence available. Start from scratch.\n"

    prompt += f"""
## Tier {tier} Sources
{tier_sources.get(tier, tier_sources[3])}

## Search Instructions
1. Use web search to find evidence from the sources listed above
2. For each search, try multiple query variations
3. Look for SPECIFIC mentions of: CDM, Common Domain Model, DRR, Digital Regulatory Reporting, ISDA standards, FINOS contribution
4. Also check for: EMIR Refit response, CFTC Rewrite preparation, derivatives reporting modernization

## Evidence Types to Look For
- **production_usage**: Bank is using CDM in live production
- **pilot_or_poc**: Bank has announced or is running a CDM pilot/proof of concept
- **membership_or_participation**: Bank is member of ISDA CDM working groups
- **open_source_contribution**: Bank has contributed code to FINOS CDM repositories
- **vendor_proxy_signal**: Bank's vendor announces CDM support for this client
- **hiring_signal**: Job postings indicate CDM/DRR work

## Output Format
For EACH piece of evidence found, provide:

### Evidence [ID]
- **Source URL**: [exact URL]
- **Source Date**: [YYYY-MM-DD or approximate]
- **Claim Type**: [one of the types above]
- **Finding**: [what you found]
- **Exact Quote**: "[relevant quote from source]"
- **Supports**: [ARCHITECT / PRAGMATIST / NEUTRAL]
- **Confidence**: [1-10, where 10 is highest]
- **Reasoning**: [why this evidence matters]

---

## Also Document Null Results
If you search for something and find NOTHING, document it:
- Search query: "[what you searched]"
- Sources checked: [list]
- Result: No evidence found
- Implication: [what does absence of evidence suggest?]

{f"## Previous Evidence from Earlier Tiers{chr(10)}{prior_evidence}" if prior_evidence else ""}

Now execute your Tier {tier} search and document all findings.
"""

    return prompt


def generate_bayesian_prompt(state: ResearchState, new_evidence: str, tier: int) -> str:
    """Generate prompt for Bayesian probability update."""

    lr_tables = load_bayesian_tables()

    # Convert 0-1 probabilities to percentages for display
    p_arch = state.probability_architect * 100
    p_prag = state.probability_pragmatist * 100

    prompt = f"""# Bayesian Probability Update - Post Tier {tier}

## Current State
- **Bank**: {state.bank_name}
- **Prior P(ARCHITECT)**: {p_arch:.1f}%
- **Prior P(PRAGMATIST)**: {p_prag:.1f}%
- **Evidence items so far**: {len(state.evidence_items)}

## New Evidence from Tier {tier}
{new_evidence}

## Your Task
Calculate the updated probability using Bayesian reasoning.

## Likelihood Ratio Reference
Use these likelihood ratios based on evidence type:

| Evidence Type | If True, LR for ARCHITECT |
|--------------|---------------------------|
| production_usage (confirmed) | 50-100 |
| pilot_or_poc (announced) | 5-15 |
| open_source_contribution | 8-20 |
| membership_or_participation | 2-5 |
| vendor_proxy_signal | 2-4 |
| hiring_signal | 1.5-3 |
| No evidence found (informative absence) | 0.7-0.9 |

## Calculation Steps

1. **List each new evidence item** with its type and your assessed LR

2. **Calculate Combined LR**:
   - If evidence items are independent: Combined LR = LR1 x LR2 x ... x LRn
   - If items from same source, don't double-count (use max LR)

3. **Apply Bayes' Rule**:
   - Prior Odds = P(A) / P(P) = {p_arch:.1f} / {p_prag:.1f}
   - Posterior Odds = Prior Odds x Combined LR
   - Posterior P(A) = Posterior Odds / (1 + Posterior Odds)

4. **Sanity Check**:
   - Is the direction correct? (pro-ARCHITECT evidence should increase P(A))
   - Is the magnitude reasonable? (single piece of Tier 2 evidence shouldn't swing 50 points)
   - Flag if Combined LR > 100 or < 0.01 (extreme, needs review)

## Output Format

### Evidence Summary
| # | Type | Source | LR | Reasoning |
|---|------|--------|----|-----------|
| 1 | ... | ... | ... | ... |

### Calculation
- Prior Odds: {p_arch:.1f} / {p_prag:.1f} = {state.probability_architect / max(state.probability_pragmatist, 0.01):.2f}
- Combined LR: [your calculation]
- Posterior Odds: [calculation]
- **Posterior P(ARCHITECT)**: [X]%
- **Posterior P(PRAGMATIST)**: [100-X]%

### Flags
- [ ] Extreme LR detected (>100 or <0.01)
- [ ] Evidence independence concern
- [ ] Confidence cap applies (Tier {tier} max = {95 if tier == 1 else 75 if tier == 2 else 50}%)
"""

    return prompt


def generate_adversarial_prompt(state: ResearchState, all_evidence: str) -> str:
    """Generate prompt for adversarial challenge."""

    # Convert 0-1 probability to percentage for display
    p_arch = state.probability_architect * 100

    prompt = f"""# Adversarial Challenge

## Your Role
You are a skeptical reviewer. Your job is to find weaknesses in the current classification and try to prove it WRONG.

## Current Assessment
- **Bank**: {state.bank_name}
- **Provisional Classification**: {state.classification} ({state.sub_classification})
- **Confidence**: {state.confidence}%
- **P(ARCHITECT)**: {p_arch:.1f}%
- **Evidence Items**: {len(state.evidence_items)}

## Evidence Gathered
{all_evidence}

## Your Tasks

### 1. Counter-Case Construction
What is the strongest argument AGAINST the current classification?
- Identify 3-4 specific weaknesses in the evidence chain
- What alternative explanation fits the evidence?
- What evidence would we expect to see that we DON'T see?

### 2. Disconfirming Search
Search for evidence that would DISPROVE the current classification:
- If classified ARCHITECT: Search for evidence bank is NOT doing CDM work
- If classified PRAGMATIST: Search for hidden CDM initiatives

Execute at least 2 targeted searches looking for counter-evidence.

### 3. Steel-man the Opposition
Write the strongest possible 3-paragraph argument for the OPPOSITE classification.
Make it compelling enough that a reasonable person might be convinced.

### 4. Verdict
Based on your adversarial analysis:

**SUSTAINED**: The classification holds. Counter-arguments are weak. Confidence adjustment: 0 to +10%

**WEAKENED**: Found some concerning gaps. Classification probably correct but less certain. Confidence adjustment: -5% to -15%

**REVISED**: Found significant counter-evidence. Classification should change. New classification: [specify]

## Output Format

### Counter-Arguments
[Your counter-arguments]

### Disconfirming Search Results
[What you searched for and found/didn't find]

### Steel-man Argument
[3-paragraph argument for opposite classification]

### Verdict
**[SUSTAINED / WEAKENED / REVISED]**
- Confidence adjustment: [+X% / -X% / unchanged]
- Reasoning: [why]
- Final recommendation: [classification] at [confidence]%
"""

    return prompt


def parse_probability_from_response(response: str) -> Optional[float]:
    """Extract posterior probability from Bayesian update response."""
    import re

    # Look for patterns like "Posterior P(ARCHITECT): 65%" or "P(ARCHITECT) = 65%"
    patterns = [
        r'[Pp]osterior\s+[Pp]\s*\(\s*ARCHITECT\s*\)\s*[=:]\s*(\d+(?:\.\d+)?)\s*%',
        r'[Pp]\s*\(\s*ARCHITECT\s*\)\s*[=:]\s*(\d+(?:\.\d+)?)\s*%',
        r'ARCHITECT[:\s]+(\d+(?:\.\d+)?)\s*%',
    ]

    for pattern in patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            return float(match.group(1))

    return None


def parse_verdict_from_response(response: str) -> Tuple[str, int]:
    """Extract verdict and confidence adjustment from adversarial response."""
    import re

    verdict = "SUSTAINED"  # Default
    adjustment = 0

    # Look for verdict
    if "REVISED" in response.upper():
        verdict = "REVISED"
    elif "WEAKENED" in response.upper():
        verdict = "WEAKENED"
    else:
        verdict = "SUSTAINED"

    # Look for confidence adjustment
    adj_patterns = [
        r'[Cc]onfidence\s+adjustment\s*[=:]\s*([+-]?\d+)\s*%',
        r'([+-]\d+)\s*%\s+adjustment',
    ]

    for pattern in adj_patterns:
        match = re.search(pattern, response)
        if match:
            adjustment = int(match.group(1))
            break

    return verdict, adjustment


def create_output_structure(bank_dir: Path):
    """Create the standard output directory structure."""
    subdirs = ['1-evidence', '2-bayesian', '3-gates', '4-adversarial', '5-synthesis', 'snapshots']
    bank_dir.mkdir(parents=True, exist_ok=True)
    for subdir in subdirs:
        (bank_dir / subdir).mkdir(exist_ok=True)


def execute_research(bank_id: str, phase: int,
                     model: str = "claude-opus-4-5-20250101") -> ResearchState:
    """
    Execute complete research pipeline for a bank.

    All research is executed live with Claude API - no simulation mode.

    Args:
        bank_id: Bank identifier
        phase: Phase number
        model: Claude model to use

    Returns:
        ResearchState with complete results
    """
    bank_config = get_bank_config(bank_id)
    if not bank_config:
        raise ValueError(f"Bank config not found: {bank_id}")

    bank_name = bank_config.get('bank_name', bank_id)

    # Determine output directory
    manifest = load_bank_manifest()
    phase_info = manifest.get('phase_summary', {}).get(f'phase_{phase}', {})
    phase_name = phase_info.get('name', f'phase-{phase}').lower().replace(' ', '-')
    bank_dir = PROJECT_ROOT / "outputs" / f"phase-{phase}-{phase_name}" / bank_id

    create_output_structure(bank_dir)

    # Check for crashed/interrupted research to recover (Category 3 fix)
    recovered_data = IncrementalEvidenceCheckpointer.recover_from_crash(bank_dir)
    resume_from_tier = 0

    if recovered_data:
        logger.info(f"Found {len(recovered_data)} staging files from previous run")
        resume_from_tier = IncrementalEvidenceCheckpointer.get_last_completed_tier(bank_dir)
        if resume_from_tier > 0:
            logger.info(f"Resuming from tier {resume_from_tier + 1} (tier {resume_from_tier} completed)")

    # Calculate initial prior
    prior_adj = bank_config.get('prior_adjustments', {})
    base_prior = 30  # Default PRAGMATIST assumption

    if prior_adj.get('derivatives_dominant'):
        base_prior += prior_adj.get('adjustment_pct', 10)
    if prior_adj.get('confirmed_contributor'):
        base_prior += prior_adj.get('contributor_adjustment_pct', 20)
    if prior_adj.get('confirmed_production'):
        base_prior += prior_adj.get('production_adjustment_pct', 30)

    base_prior = min(base_prior, 90)

    # Convert to 0-1 scale for internal representation
    state = ResearchState(
        bank_id=bank_id,
        bank_name=bank_name,
        phase=phase,
        probability_architect=base_prior / 100.0,  # 0-1 scale
        probability_pragmatist=(100 - base_prior) / 100.0  # 0-1 scale
    )

    logger.info(f"\n{'='*60}")
    logger.info(f"RESEARCH: {bank_name}")
    logger.info(f"Prior P(ARCHITECT): {state.probability_architect * 100:.1f}%")
    logger.info(f"{'='*60}")

    # Initialize Claude researcher
    try:
        researcher = ClaudeResearcher(model=model)
        logger.info(f"Claude API initialized with model: {model}")
    except Exception as e:
        logger.error(f"Failed to initialize Claude API: {e}")
        state.errors.append(f"API initialization failed: {e}")
        return state

    # Get skip threshold (convert from percentage to 0-1)
    thresholds = load_decision_thresholds()
    skip_threshold = thresholds.get('skip_threshold_pct', 80) / 100.0

    all_evidence_text = ""

    # Restore evidence from completed tiers (for resume scenarios)
    for tier in range(1, resume_from_tier + 1):
        if tier in recovered_data:
            raw_response = recovered_data[tier].get("raw_response", "")
            if raw_response:
                all_evidence_text += f"\n\n## Tier {tier} Evidence (recovered)\n{raw_response}"
                state.highest_tier = tier
                state.stages_completed.append(f'tier{tier}_evidence')
                state.stages_completed.append(f'bayesian_t{tier}')
                logger.info(f"  Restored tier {tier} evidence from checkpoint")

    # Process each tier
    for tier in [1, 2, 3]:
        # Skip already-completed tiers (from recovery)
        if tier <= resume_from_tier:
            logger.info(f"\n[TIER {tier}] Skipped (already completed)")
            continue

        logger.info(f"\n[TIER {tier}] Evidence Gathering")

        # Check for early exit (0-1 scale comparison)
        if state.probability_architect > skip_threshold:
            logger.info(f"  -> P(ARCHITECT) > {skip_threshold * 100:.0f}%, skipping remaining tiers")
            break
        if state.probability_pragmatist > skip_threshold:
            logger.info(f"  -> P(PRAGMATIST) > {skip_threshold * 100:.0f}%, skipping remaining tiers")
            break

        # Create checkpointer for this tier (Category 3 fix)
        checkpointer = IncrementalEvidenceCheckpointer(bank_dir, bank_id, tier)

        # Check if we have in-progress checkpoint for this tier
        if tier in recovered_data and recovered_data[tier].get("status") == "in_progress":
            previous_response = recovered_data[tier].get("raw_response")
            if previous_response:
                logger.info(f"  Found incomplete checkpoint, using recovered data")
                checkpointer.set_raw_response(previous_response)

        # Generate evidence prompt
        evidence_prompt = generate_evidence_prompt(bank_config, tier, all_evidence_text)

        try:
            # Execute live search
            logger.info(f"  Executing web search...")
            evidence_response = researcher.research_with_web_search(evidence_prompt)

            # Checkpoint the raw response immediately (survives crash)
            checkpointer.set_raw_response(evidence_response)

            # Save raw response to file
            evidence_file = bank_dir / "1-evidence" / f"tier{tier}-evidence.md"
            evidence_file.write_text(f"# Tier {tier} Evidence: {bank_name}\n\n{evidence_response}", encoding='utf-8')
            logger.info(f"  Saved to {evidence_file.name}")

            all_evidence_text += f"\n\n## Tier {tier} Evidence\n{evidence_response}"
            state.highest_tier = tier

            # Finalize checkpoint (marks tier as complete)
            checkpointer.finalize()

        except Exception as e:
            logger.error(f"  Error in Tier {tier}: {e}")
            state.errors.append(f"Tier {tier} error: {e}")
            # Note: checkpoint file is preserved for recovery on restart
            continue

        state.stages_completed.append(f'tier{tier}_evidence')

        # Sync state after evidence gathering
        _sync_to_state_manager(state, f'tier{tier}_evidence')

        # Bayesian update
        logger.info(f"\n[BAYESIAN] Post-Tier {tier} Update")

        bayesian_prompt = generate_bayesian_prompt(state, all_evidence_text, tier)

        try:
            bayesian_response = researcher.analyze(bayesian_prompt)

            # Parse probability (returns 0-100, convert to 0-1)
            new_prob = parse_probability_from_response(bayesian_response)
            if new_prob is not None:
                state.probability_architect = new_prob / 100.0  # Convert to 0-1
                state.probability_pragmatist = 1.0 - state.probability_architect
                logger.info(f"  Updated P(ARCHITECT): {state.probability_architect * 100:.1f}%")

            # Save response
            bayesian_file = bank_dir / "2-bayesian" / f"post-tier{tier}-update.md"
            bayesian_file.write_text(f"# Bayesian Update: Post Tier {tier}\n\n{bayesian_response}", encoding='utf-8')

        except Exception as e:
            logger.error(f"  Bayesian error: {e}")
            state.errors.append(f"Bayesian T{tier} error: {e}")

        state.stages_completed.append(f'bayesian_t{tier}')

        # Sync state after Bayesian update
        _sync_to_state_manager(state, f'bayesian_t{tier}')

    # Determine provisional classification (thresholds in 0-1 scale)
    if state.probability_architect > 0.50:
        state.classification = "ARCHITECT"
        if state.probability_architect > 0.80:
            state.sub_classification = "Leader"
        elif state.probability_architect > 0.65:
            state.sub_classification = "Follower"
        else:
            state.sub_classification = "Follower"
    else:
        state.classification = "PRAGMATIST"
        if state.probability_pragmatist > 0.80:
            state.sub_classification = "Traditional"
        else:
            state.sub_classification = "Wait-and-See"

    # Calculate provisional confidence
    if state.highest_tier == 1:
        max_conf = 95
    elif state.highest_tier == 2:
        max_conf = 75
    else:
        max_conf = 50

    prob_distance = abs(state.probability_architect - 50)
    state.confidence = min(int(prob_distance * 1.5 + 40), max_conf)

    # Adversarial challenge
    logger.info(f"\n[ADVERSARIAL] Challenge")

    adversarial_prompt = generate_adversarial_prompt(state, all_evidence_text)

    try:
        adversarial_response = researcher.research_with_web_search(adversarial_prompt)

        # Parse verdict
        verdict, adjustment = parse_verdict_from_response(adversarial_response)
        state.adversarial_verdict = verdict
        state.confidence = max(0, min(100, state.confidence + adjustment))

        logger.info(f"  Verdict: {verdict}, Adjustment: {adjustment:+d}%")

        # Save response
        verdict_file = bank_dir / "4-adversarial" / "verdict.md"
        verdict_file.write_text(f"# Adversarial Verdict: {bank_name}\n\n{adversarial_response}", encoding='utf-8')

    except Exception as e:
        logger.error(f"  Adversarial error: {e}")
        state.errors.append(f"Adversarial error: {e}")
        state.adversarial_verdict = "SUSTAINED"

    state.stages_completed.append('adversarial')
    state.completed_at = datetime.now(timezone.utc).isoformat()

    # Sync final state to state manager (Issue #2 fix)
    _sync_to_state_manager(state, 'adversarial')

    # Clean up staging files after successful completion (Category 3 fix)
    for tier in [1, 2, 3]:
        staging_cleanup = IncrementalEvidenceCheckpointer(bank_dir, bank_id, tier)
        staging_cleanup.cleanup()
    logger.debug("Cleaned up all evidence staging files")

    # Also save legacy status.json for backward compatibility
    status_file = bank_dir / "status.json"
    status_file.write_text(json.dumps(asdict(state), indent=2, default=str), encoding='utf-8')

    logger.info(f"\n{'='*60}")
    logger.info(f"COMPLETE: {bank_name}")
    logger.info(f"Classification: {state.classification} ({state.sub_classification})")
    logger.info(f"Confidence: {state.confidence}%")
    logger.info(f"P(ARCHITECT): {state.probability_architect * 100:.1f}%")
    logger.info(f"Adversarial: {state.adversarial_verdict}")
    logger.info(f"{'='*60}\n")

    return state


def main():
    import argparse

    parser = argparse.ArgumentParser(description="CDM Research Executor - Live Research Only")
    parser.add_argument('--bank', required=True, help="Bank ID to research")
    parser.add_argument('--phase', type=int, required=True, help="Phase number")
    parser.add_argument('--model', default="claude-opus-4-5-20250101",
                        help="Claude model (default: claude-opus-4-5-20250101)")
    parser.add_argument('--show-prompts', action='store_true', help="Print generated prompts without executing")

    args = parser.parse_args()

    if args.show_prompts:
        bank_config = get_bank_config(args.bank)
        if bank_config:
            print("\n" + "="*70)
            print("TIER 1 EVIDENCE PROMPT")
            print("="*70)
            print(generate_evidence_prompt(bank_config, tier=1))
        return

    state = execute_research(
        args.bank,
        args.phase,
        model=args.model
    )

    print(json.dumps(asdict(state), indent=2, default=str))


if __name__ == "__main__":
    main()
