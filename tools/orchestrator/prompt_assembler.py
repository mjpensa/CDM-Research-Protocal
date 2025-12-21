"""
CDM Research Protocol - Prompt Assembler

Assembles focused prompts for each research stage.
Injects context, prior evidence, and output specifications.

Usage:
    assembler = PromptAssembler()
    prompt = assembler.assemble(stage, bank_config, state)
"""

import json
import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

# Add parent to path for config_loader access
_SCRIPT_DIR = Path(__file__).parent.resolve()
_TOOLS_DIR = _SCRIPT_DIR.parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from config_loader import get_confidence_caps

logger = logging.getLogger(__name__)


@dataclass
class StageContext:
    """Context for prompt assembly."""
    bank_id: str
    bank_name: str
    bank_config: Dict[str, Any]
    current_probability: float
    evidence_counts: Dict[str, int]
    highest_tier: int
    bank_dir: Path
    prior_evidence: List[Dict] = None
    thresholds: Dict[str, Any] = None


class PromptAssembler:
    """
    Assembles stage-specific prompts for Claude Code execution.

    Each prompt includes:
    - Role/context from agent prompt file
    - Current state (probability, evidence counts)
    - Stage-specific inputs
    - Expected output format
    - File paths to write to
    """

    def __init__(self, config_dir: Path = None, outputs_dir: Path = None):
        self.config_dir = config_dir or Path(__file__).parent.parent.parent / "config"
        self.outputs_dir = outputs_dir or Path(__file__).parent.parent.parent / "outputs"
        self.prompts_dir = self.config_dir / "agent-prompts"

        # Load configurations
        self.thresholds = self._load_json(self.config_dir / "decision-thresholds.json")
        self.lr_tables = self._load_json(self.config_dir / "bayesian-lr-tables.json")
        self.checkpoint_rules = self._load_json(self.config_dir / "checkpoint-rules.json")

    def _load_json(self, path: Path) -> dict:
        """Load JSON file."""
        if not path.exists():
            logger.warning(f"Config file not found: {path}")
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_text(self, path: Path) -> str:
        """Load text file."""
        if not path.exists():
            return ""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a section from markdown by heading."""
        import re
        pattern = rf'(?:^|\n)##\s+{re.escape(section_name)}\s*\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def assemble(self, stage: str, ctx: StageContext) -> str:
        """
        Assemble a complete prompt for the stage.

        Args:
            stage: Stage name
            ctx: StageContext with bank and state info

        Returns:
            Complete prompt string
        """
        if stage == "pre_mortem":
            return self._assemble_pre_mortem(ctx)
        elif "evidence" in stage:
            return self._assemble_evidence(stage, ctx)
        elif "bayesian" in stage:
            return self._assemble_bayesian(stage, ctx)
        elif "gate" in stage:
            return self._assemble_gate(stage, ctx)
        elif stage == "adversarial_challenge":
            return self._assemble_adversarial(ctx)
        elif stage == "synthesis":
            return self._assemble_synthesis(ctx)
        else:
            return self._assemble_default(stage, ctx)

    def _assemble_pre_mortem(self, ctx: StageContext) -> str:
        """Assemble pre-mortem analysis prompt."""
        return f'''# Pre-Mortem Analysis: {ctx.bank_name}

## Objective
Before beginning research, identify 4 potential failure modes that could lead to incorrect classification.

## Bank Profile
- **Bank**: {ctx.bank_name} ({ctx.bank_id})
- **Headquarters**: {ctx.bank_config.get("headquarters", "Unknown")}
- **Derivatives Relevance**: {ctx.bank_config.get("derivatives_relevance", "Unknown")}
- **Primary Regulator**: {ctx.bank_config.get("primary_regulator", "Unknown")}
- **Research Objective**: {ctx.bank_config.get("research_objective", {}).get("primary_goal", "")}

## Prior Adjustments
{json.dumps(ctx.bank_config.get("prior_adjustments", {}), indent=2)}

## Your Task

Imagine we complete this research and get the classification WRONG. Document 4 specific ways this could happen:

### Failure Mode 1: False Positive ARCHITECT
How might we incorrectly classify this bank as ARCHITECT when they are actually PRAGMATIST?
- What misleading evidence could we find?
- What confirmation bias traps exist?

### Failure Mode 2: False Negative ARCHITECT
How might we incorrectly classify as PRAGMATIST when they are actually ARCHITECT?
- What evidence might we miss?
- What could obscure genuine CDM work?

### Failure Mode 3: Overconfidence
How might we become overconfident in our classification?
- What weak evidence might we treat as strong?
- What corroboration gaps might we ignore?

### Failure Mode 4: Information Gaps
What critical information is likely unavailable?
- What would we need to know that we can't find?
- How should we handle these gaps?

## Difficulty Assessment
Rate the expected difficulty of this research (1-5) and explain why.

## Success Criteria
Define what "successful research" looks like for this bank.

## Output
Write your analysis to: `{ctx.bank_dir}/3-gates/pre-mortem.md`
'''

    def _assemble_evidence(self, stage: str, ctx: StageContext) -> str:
        """Assemble evidence gathering prompt."""
        tier = int(stage.replace("tier", "").replace("_evidence", ""))

        # Load agent prompt for reference
        agent_prompt = self._load_text(self.prompts_dir / "evidence-gatherer.md")

        # Get prior evidence if tier > 1
        prior_section = ""
        if tier > 1 and ctx.prior_evidence:
            prior_section = f'''
## Prior Evidence (Tiers 1-{tier-1})
Evidence already gathered:
```json
{json.dumps(ctx.prior_evidence[:10], indent=2)}  # First 10 items
```
Total evidence items: {len(ctx.prior_evidence)}
'''

        return f'''# Evidence Gathering - Tier {tier}: {ctx.bank_name}

## Your Role
You are the Evidence Gatherer Agent. Execute web searches, retrieve evidence, and document findings in structured format. Do NOT perform analysis or classification.

## Bank Profile
- **Bank**: {ctx.bank_name} ({ctx.bank_id})
- **Headquarters**: {ctx.bank_config.get("headquarters", "Unknown")}
- **Derivatives Relevance**: {ctx.bank_config.get("derivatives_relevance", "Unknown")}
- **Primary Regulator**: {ctx.bank_config.get("primary_regulator", "Unknown")}

## Research Objective
{ctx.bank_config.get("research_objective", {}).get("primary_goal", "Assess CDM/DRR adoption posture")}

## Key Questions to Investigate
{json.dumps(ctx.bank_config.get("research_objective", {}).get("key_questions", []), indent=2)}

## Current Research State
- **P(Architect)**: {ctx.current_probability:.1%}
- **Evidence collected**: Tier 1={ctx.evidence_counts.get("tier1", 0)}, Tier 2={ctx.evidence_counts.get("tier2", 0)}, Tier 3={ctx.evidence_counts.get("tier3", 0)}
{prior_section}

## Tier {tier} Instructions

{self._get_tier_instructions(tier)}

## Search Strategy

Execute at least 15-20 distinct searches. Use these templates:

{self._get_search_templates(tier, ctx.bank_name)}

## Output Requirements

### 1. Update evidence.json
Path: `{ctx.bank_dir}/evidence.json`

Add new evidence items with this schema:
```json
{{
  "id": "E{tier:03d}X",
  "claim": "Description of what this evidence shows",
  "source_url": "https://...",
  "tier": {tier},
  "claim_type": "one of: production_usage, pilot_or_poc, membership_or_participation, open_source_contribution, vendor_proxy_signal, hiring_signal",
  "date_published": "YYYY-MM-DD if known",
  "excerpt": "Relevant quote from source"
}}
```

### 2. Write tier{tier}-evidence.md
Path: `{ctx.bank_dir}/1-evidence/tier{tier}-evidence.md`

For each evidence item, document:
- Source and URL
- Key claims and excerpts
- Relevance to CDM/DRR posture
- Reliability assessment

### 3. Document null results
Path: `{ctx.bank_dir}/1-evidence/null-results.md`

Document searches that returned no relevant results. This is IMPORTANT for calibration.

## Evidence Quality Checklist
Before completing, verify:
- [ ] At least 15 searches executed
- [ ] All evidence items have valid URLs
- [ ] Null results documented
- [ ] No duplicate evidence
- [ ] Tier assignment is correct for each source

Begin your Tier {tier} evidence gathering now.
'''

    def _get_tier_instructions(self, tier: int) -> str:
        """Get tier-specific instructions."""
        if tier == 1:
            return '''**Tier 1: Official Sources (Definitive Weight)**
Focus on:
- Bank press releases and announcements
- Annual reports, investor presentations
- Regulatory filings
- ISDA/FINOS official announcements naming the bank
- Central bank/regulator announcements

These sources have the highest authority. A single Tier 1 source confirming CDM production is sufficient for high confidence.'''
        elif tier == 2:
            return '''**Tier 2: Industry Sources (Strong Weight)**
Focus on:
- Risk.net, Waters Technology, Financial News articles
- ISDA AGM speaker lists
- FINOS GitHub contributions
- Specialist analyst reports
- Conference proceedings with named speakers

These sources require triangulation. Look for 2-3 independent sources supporting the same claim.'''
        else:
            return '''**Tier 3: Indirect Signals (Moderate Weight)**
Focus on:
- Job postings mentioning CDM/DRR
- LinkedIn profiles of employees
- Vendor announcements claiming bank as client
- Patent filings
- Industry conference attendance

These are weak signals that can support but not establish a classification on their own.'''

    def _get_search_templates(self, tier: int, bank_name: str) -> str:
        """Get tier-specific search templates."""
        if tier == 1:
            return f'''```
"{bank_name}" "Common Domain Model" site:[bank-domain]
"{bank_name}" CDM derivatives technology announcement
"{bank_name}" annual report 2024 "derivatives" "technology"
site:isda.org "{bank_name}" CDM
site:finos.org "{bank_name}"
site:github.com/finos "{bank_name}" CDM
"{bank_name}" "Digital Regulatory Reporting" announcement
"{bank_name}" "EMIR Refit" technology solution
```'''
        elif tier == 2:
            return f'''```
site:risk.net "{bank_name}" CDM
site:waterstechnology.com "{bank_name}" derivatives technology
"{bank_name}" ISDA AGM speaker
"{bank_name}" derivatives conference 2024 speaker
"{bank_name}" CDM pilot production
"{bank_name}" regulatory reporting modernization
"{bank_name}" "Common Domain Model" interview
```'''
        else:
            return f'''```
site:linkedin.com "{bank_name}" "Common Domain Model"
site:linkedin.com "{bank_name}" CDM derivatives
"{bank_name}" CDM job posting
site:careers.{bank_name.lower().replace(" ", "")} CDM
"{bank_name}" vendor partnership derivatives reporting
"{bank_name}" patent derivatives data model
```'''

    def _assemble_bayesian(self, stage: str, ctx: StageContext) -> str:
        """Assemble Bayesian probability update prompt."""
        tier = int(stage.replace("bayesian_", ""))

        return f'''# Bayesian Probability Update - Tier {tier}: {ctx.bank_name}

## Your Task
Calculate the updated P(Architect) after incorporating Tier {tier} evidence.

## Current State
- **Prior P(Architect)**: {ctx.current_probability:.1%}
- **Prior P(Pragmatist)**: {1 - ctx.current_probability:.1%}
- **Prior Odds**: {ctx.current_probability / (1 - ctx.current_probability) if ctx.current_probability < 1 else 99:.3f}

## Evidence Summary
- Tier 1 items: {ctx.evidence_counts.get("tier1", 0)}
- Tier 2 items: {ctx.evidence_counts.get("tier2", 0)}
- Tier 3 items: {ctx.evidence_counts.get("tier3", 0)}
- Null results: {ctx.evidence_counts.get("null", 0)}

## Likelihood Ratio Reference

Use these LR mappings for common evidence types:

| Evidence Type | LR for Architect | Notes |
|---------------|------------------|-------|
| Official production announcement | 15-25 | Very strong signal |
| Pilot/PoC announcement | 5-10 | Strong signal |
| FINOS contribution (commits) | 3-5 | Moderate signal |
| ISDA working group mention | 2-3 | Weak-moderate signal |
| Industry article claiming adoption | 2-4 | Requires verification |
| Job posting mentioning CDM | 1.5-2 | Weak signal |
| Null result (thorough search) | 0.7-0.9 | Weak counter-signal |

## Calculation Steps

1. **List each evidence item with assigned LR**
2. **Check for independence** - Don't double-count correlated evidence
3. **Calculate Combined LR** = LR1 × LR2 × ... × LRn
4. **Calculate Posterior Odds** = Prior Odds × Combined LR
5. **Convert to Probability**: P(A) = Posterior Odds / (1 + Posterior Odds)
6. **Apply confidence cap** based on highest tier:
   - Tier 1 present: max 95%
   - Tier 2 only: max 75%
   - Tier 3 only: max 50%

## Sanity Checks
- [ ] Direction correct? (pro-Architect evidence increases P(A))
- [ ] Magnitude reasonable? (single item shouldn't swing 50+ points)
- [ ] Combined LR in [0.01, 100]? (flag if outside)

## Output Requirements

Write to: `{ctx.bank_dir}/2-bayesian/post-tier{tier}-update.md`

Include:
1. Evidence table with LR assignments
2. Independence assessment
3. Combined LR calculation
4. Posterior probability calculation
5. Sanity check results
6. **Final P(Architect)**: X.X%
7. **Final P(Pragmatist)**: X.X%

Begin your Bayesian analysis now.
'''

    def _assemble_gate(self, stage: str, ctx: StageContext) -> str:
        """Assemble reasoning gate prompt."""
        gate_num = int(stage.replace("gate_", ""))
        skip_threshold = self.thresholds.get("workflow_decisions", {}).get(
            "skip_to_adversarial", {}
        ).get("threshold", 80)

        return f'''# Reasoning Gate {gate_num}: {ctx.bank_name}

## Purpose
Evaluate evidence quality and decide whether to continue to next tier or skip to adversarial.

## Current State
- **P(Architect)**: {ctx.current_probability:.1%}
- **Evidence counts**: T1={ctx.evidence_counts.get("tier1", 0)}, T2={ctx.evidence_counts.get("tier2", 0)}, T3={ctx.evidence_counts.get("tier3", 0)}
- **Highest tier**: {ctx.highest_tier}

## Gate {gate_num} Checks

### 1. Evidence Delta
What new evidence was found in this tier?
- List key findings
- Assess quality and reliability

### 2. Probability Assessment
- Prior P(A): [from previous stage]
- Posterior P(A): {ctx.current_probability:.1%}
- Change: [calculate delta]
- Direction: [toward ARCHITECT / toward PRAGMATIST / unchanged]

### 3. Skip Decision
Threshold for skip: {skip_threshold}%

If P(Architect) > {skip_threshold}% OR P(Architect) < {100-skip_threshold}%:
-> SKIP remaining tiers, proceed to adversarial challenge

Current P = {ctx.current_probability:.1%}
**Decision**: {"SKIP to adversarial" if ctx.current_probability * 100 > skip_threshold or ctx.current_probability * 100 < (100-skip_threshold) else "CONTINUE to next tier"}

{self._get_gate_specific_checks(gate_num)}

## Output Requirements

Write to: `{ctx.bank_dir}/3-gates/gate-{gate_num}.md`

Include all sections above with your analysis.

Conclude with:
- **Gate Decision**: [PROCEED / SKIP]
- **Next Stage**: [tier{gate_num+1}_evidence / adversarial_challenge]
- **Confidence in trajectory**: [Low / Medium / High]

Begin your Gate {gate_num} analysis now.
'''

    def _get_gate_specific_checks(self, gate_num: int) -> str:
        """Get gate-specific checks."""
        if gate_num == 1:
            return '''### 4. Sufficiency Check
- Is Tier 1 evidence sufficient for classification?
- Do we need Tier 2 for corroboration?

### 5. Counterfactual Test
If we classified now, what's the probability we'd reverse after more evidence?'''
        elif gate_num == 2:
            return '''### 4. Observable Implications
Test 3+ of 6 implications for the LEADING hypothesis:

**If ARCHITECT is leading:**
- A1: Official participation in ISDA/FINOS? [Y/N]
- A2: Named individual contributors? [Y/N]
- A3: Public announcements? [Y/N]
- A4: CDM-related job postings? [Y/N]
- A5: Industry recognition as adopter? [Y/N]
- A6: Ecosystem relationships? [Y/N]

**If PRAGMATIST is leading:**
- P1: Vendor dependency? [Y/N]
- P2: Absence from CDM forums? [Y/N]
- P3: Traditional technology focus? [Y/N]
- P4: Compliance-only messaging? [Y/N]
- P5: Utility reliance? [Y/N]
- P6: Peer differentiation? [Y/N]

Count: [X/6] implications confirmed for leading hypothesis'''
        else:
            return '''### 4. Evidence Pattern Assessment
- Is the evidence pattern consistent with classification?
- Are there unexplained gaps or anomalies?

### 5. Trajectory Assessment
- Is the bank moving toward or away from CDM adoption?
- What is the 12-month outlook?'''

    def _assemble_adversarial(self, ctx: StageContext) -> str:
        """Assemble adversarial challenge prompt."""
        leading = "ARCHITECT" if ctx.current_probability > 0.5 else "PRAGMATIST"
        alternative = "PRAGMATIST" if leading == "ARCHITECT" else "ARCHITECT"

        return f'''# Adversarial Challenge: {ctx.bank_name}

## Purpose
Construct the strongest possible counter-argument to stress-test the current classification.

## Current Assessment
- **Leading Hypothesis**: {leading}
- **P(Architect)**: {ctx.current_probability:.1%}
- **Highest Evidence Tier**: {ctx.highest_tier}
- **Evidence counts**: T1={ctx.evidence_counts.get("tier1", 0)}, T2={ctx.evidence_counts.get("tier2", 0)}, T3={ctx.evidence_counts.get("tier3", 0)}

## Adversarial Protocol

### Part 1: Counter-Case Construction
Write the strongest possible argument that {ctx.bank_name} is {alternative}, not {leading}.

Include:
1. Alternative interpretation of existing evidence
2. Evidence that was overlooked or underweighted
3. Structural reasons why our classification might be wrong
4. Historical precedents of similar classification errors

Write to: `{ctx.bank_dir}/4-adversarial/counter-case.md`

### Part 2: Disconfirming Evidence Search
Execute 3 targeted searches specifically designed to find evidence AGAINST the current classification.

Search templates:
```
"{ctx.bank_name}" {alternative.lower()} evidence
"{ctx.bank_name}" NOT CDM derivatives traditional
"{ctx.bank_name}" vendor dependency regulatory reporting
```

Document findings in: `{ctx.bank_dir}/4-adversarial/disconfirming-searches.md`

### Part 3: Steelman the Alternative
If you were FORCED to argue {ctx.bank_name} is {alternative}, what is the single strongest argument?

Write to: `{ctx.bank_dir}/4-adversarial/steelman.md`

### Part 4: Verdict
After adversarial analysis, assess impact on classification:

| Verdict | Meaning | Confidence Adjustment |
|---------|---------|----------------------|
| STRENGTHENED | Counter-case failed, classification more robust | +5% |
| UNCHANGED | Counter-case inconclusive | +0% |
| WEAKENED | Counter-case raised valid concerns | -5% |
| REVISED | Counter-case is compelling, classification should change | -10% and flag for review |

Answer these 5 questions:
1. Did the counter-case reveal genuine weaknesses?
2. Did disconfirming searches find new evidence?
3. Is the steelman argument compelling?
4. Would you bet on this classification at stated odds?
5. What single piece of evidence would most change your mind?

Write verdict to: `{ctx.bank_dir}/4-adversarial/verdict.md`

## Output Summary
Create all 4 files:
1. `4-adversarial/counter-case.md`
2. `4-adversarial/disconfirming-searches.md`
3. `4-adversarial/steelman.md`
4. `4-adversarial/verdict.md`

Begin your adversarial challenge now.
'''

    def _assemble_synthesis(self, ctx: StageContext) -> str:
        """Assemble final synthesis prompt."""
        return f'''# Synthesis: {ctx.bank_name}

## Purpose
Produce the final assessment with confidence calibration and framework integration.

## Current State
- **P(Architect)**: {ctx.current_probability:.1%}
- **Highest Evidence Tier**: {ctx.highest_tier}
- **Evidence counts**: T1={ctx.evidence_counts.get("tier1", 0)}, T2={ctx.evidence_counts.get("tier2", 0)}, T3={ctx.evidence_counts.get("tier3", 0)}

## Step 1: Confidence Calibration

**CRITICAL**: Create confidence-calibration.md FIRST, before assessment.md.

### Calibration Calculation

1. **Maximum by Tier**
   - Tier 1 present: 95% max
   - Tier 2 only: 75% max
   - Tier 3 only: 50% max
   - Inference only: 35% max

   Your max: {self._get_confidence_cap(ctx.highest_tier)}%

2. **Corroboration Adjustment**
   - 3+ independent sources: +10%
   - 2 independent sources: +5%
   - 1 source only: +0%
   - Uncorroborated: -10%

3. **Contradiction Adjustment**
   - No contradictions: +0%
   - Minor (resolved): -5%
   - Significant (resolved): -10%
   - Unresolved: -15% to -25%

4. **Adversarial Adjustment**
   - Strengthened: +5%
   - Unchanged: +0%
   - Weakened: -5%
   - Revised: -10%

5. **Coherence Adjustment**
   - Fully consistent with anchors/peers: +5%
   - Minor inconsistency: +0%
   - Inconsistency requiring explanation: -5%
   - Significant incoherence: -10%

6. **Final Calculation**
   Raw = Max + Corroboration + Contradiction + Adversarial + Coherence
   Final = max(20%, min(95%, Raw))

### Betting Test
At your final confidence, would you bet at the implied odds?
- 90% = 9:1 odds
- 80% = 4:1 odds
- 70% = 2.3:1 odds
- 60% = 1.5:1 odds
- 50% = 1:1 odds

Write to: `{ctx.bank_dir}/5-synthesis/confidence-calibration.md`

## Step 2: Final Classification

Based on probability and evidence quality, determine:

### Classification Options
- **ARCHITECT-Native**: Production usage confirmed (P(A) > 90%, Tier 1 evidence)
- **ARCHITECT-Leader**: Significant contribution, pilot/PoC (P(A) > 75%)
- **ARCHITECT-Follower**: Participation without major contribution (P(A) > 60%)
- **PRAGMATIST-Vendor**: Relies on vendor for CDM (P(A) < 50%)
- **PRAGMATIST-Regulatory**: Compliance-driven only (P(A) < 50%)
- **UNKNOWN**: Insufficient evidence (confidence < 40%)

## Step 3: Assessment Document

Write comprehensive assessment to: `{ctx.bank_dir}/5-synthesis/assessment.md`

Include these sections:
1. Executive Summary (2-3 sentences)
2. Classification and Confidence
3. Evidence Summary by Tier
4. Key Findings
5. Uncertainties and Limitations
6. Comparison to Framework Claims (if any)
7. Recommendations for Follow-up

## Step 4: Framework Integration

Extract quick-copy format to: `{ctx.bank_dir}/5-synthesis/framework-integration.md`

```
| Bank | Classification | Variant | Confidence | Highest Tier | Key Evidence |
|------|---------------|---------|------------|--------------|--------------|
| {ctx.bank_name} | [CLASS] | [VARIANT] | [X]% | {ctx.highest_tier} | [Brief] |
```

## Output Summary
Create all 3 files in order:
1. `5-synthesis/confidence-calibration.md` (FIRST)
2. `5-synthesis/assessment.md`
3. `5-synthesis/framework-integration.md`

Begin your synthesis now.
'''

    def _get_confidence_cap(self, highest_tier: int) -> int:
        """Get confidence cap for tier from centralized config."""
        try:
            caps = get_confidence_caps()  # Returns {1: 95, 2: 75, 3: 50, 4: 35}
            return caps.get(highest_tier, 35)
        except Exception:
            # Fallback if config loading fails
            fallback_caps = {1: 95, 2: 75, 3: 50, 4: 35}
            return fallback_caps.get(highest_tier, 35)

    def _assemble_default(self, stage: str, ctx: StageContext) -> str:
        """Assemble default prompt for unknown stages."""
        return f'''# Stage: {stage}

## Bank: {ctx.bank_name}

Current P(Architect): {ctx.current_probability:.1%}

Please complete the {stage} stage for this bank.
'''

    def get_full_research_prompt(self, bank_config: Dict, phase: int) -> str:
        """
        Generate a complete research prompt for running all stages in sequence.

        This is used for fully automated overnight runs.
        """
        bank_id = bank_config["bank_id"]
        bank_name = bank_config["bank_name"]

        return f'''# Complete CDM/DRR Research: {bank_name}

## Overview
Execute the full research protocol for {bank_name}. Process all stages in sequence, writing outputs to the appropriate files.

## Bank Configuration
```json
{json.dumps(bank_config, indent=2)}
```

## Research Stages

Execute these stages in order:

1. **Pre-Mortem** -> `3-gates/pre-mortem.md`
2. **Tier 1 Evidence** -> `evidence.json`, `1-evidence/tier1-evidence.md`
3. **Bayesian Update 1** -> `2-bayesian/post-tier1-update.md`
4. **Reasoning Gate 1** -> `3-gates/gate-1.md`
5. **Tier 2 Evidence** -> `evidence.json`, `1-evidence/tier2-evidence.md`
6. **Bayesian Update 2** -> `2-bayesian/post-tier2-update.md`
7. **Reasoning Gate 2** -> `3-gates/gate-2.md`
8. **Tier 3 Evidence** -> `evidence.json`, `1-evidence/tier3-evidence.md`
9. **Bayesian Update 3** -> `2-bayesian/post-tier3-update.md`
10. **Reasoning Gate 3** -> `3-gates/gate-3.md`
11. **Adversarial Challenge** -> `4-adversarial/*`
12. **Synthesis** -> `5-synthesis/*`

## Skip Logic
If P(Architect) > 80% or P(Architect) < 20% at any gate, skip remaining evidence tiers and proceed to adversarial challenge.

## Output Directory
All outputs go to: `outputs/phase-{phase}-*//{bank_id}/`

## Starting Prior
P(Architect) = 30% (null hypothesis: PRAGMATIST)

Begin research now.
'''
