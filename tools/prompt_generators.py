"""
CDM Research Protocol - Prompt Generators v1.0

Pure string formatting functions for generating research prompts.
NO API dependencies - these are standalone prompt templates.

Extracted from research_executor.py for Claude Code compatibility.

Usage:
    from prompt_generators import (
        generate_evidence_prompt,
        generate_bayesian_prompt,
        generate_adversarial_prompt,
        generate_synthesis_prompt
    )

    prompt = generate_evidence_prompt(bank_config, tier=1)
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import load_bayesian_tables, load_decision_thresholds


@dataclass
class ResearchContext:
    """
    Research context for prompt generation.

    NOTE: All probability values use 0-1 scale (not 0-100).
    """
    bank_id: str
    bank_name: str
    phase: int
    probability_architect: float  # 0-1 scale
    probability_pragmatist: float  # 0-1 scale
    classification: Optional[str] = None
    sub_classification: Optional[str] = None
    confidence: Optional[int] = None
    evidence_count: int = 0
    highest_tier: int = 0
    adversarial_verdict: Optional[str] = None

    @property
    def probability_architect_pct(self) -> float:
        """Get probability as percentage."""
        return self.probability_architect * 100

    @property
    def probability_pragmatist_pct(self) -> float:
        """Get probability as percentage."""
        return self.probability_pragmatist * 100


def generate_evidence_prompt(bank_config: Dict[str, Any], tier: int, prior_evidence: str = "") -> str:
    """
    Generate prompt for evidence gathering.

    Args:
        bank_config: Bank configuration from manifest
        tier: Evidence tier (1, 2, or 3)
        prior_evidence: Evidence from previous tiers (for context)

    Returns:
        Complete evidence gathering prompt
    """
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


def generate_bayesian_prompt(context: ResearchContext, new_evidence: str, tier: int) -> str:
    """
    Generate prompt for Bayesian probability update.

    Args:
        context: Research context with current probabilities
        new_evidence: Evidence found in current tier
        tier: Current tier number

    Returns:
        Complete Bayesian update prompt
    """
    # Convert 0-1 probabilities to percentages for display
    p_arch = context.probability_architect_pct
    p_prag = context.probability_pragmatist_pct

    # Load confidence caps
    thresholds = load_decision_thresholds()
    caps = thresholds.get('confidence_caps', {})
    tier_cap = caps.get(f'tier{tier}_only', 95 if tier == 1 else 75 if tier == 2 else 50)

    prompt = f"""# Bayesian Probability Update - Post Tier {tier}

## Current State
- **Bank**: {context.bank_name}
- **Prior P(ARCHITECT)**: {p_arch:.1f}%
- **Prior P(PRAGMATIST)**: {p_prag:.1f}%
- **Evidence items so far**: {context.evidence_count}

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
- Prior Odds: {p_arch:.1f} / {p_prag:.1f} = {context.probability_architect / max(context.probability_pragmatist, 0.01):.2f}
- Combined LR: [your calculation]
- Posterior Odds: [calculation]
- **Posterior P(ARCHITECT)**: [X]%
- **Posterior P(PRAGMATIST)**: [100-X]%

### Flags
- [ ] Extreme LR detected (>100 or <0.01)
- [ ] Evidence independence concern
- [ ] Confidence cap applies (Tier {tier} max = {tier_cap}%)
"""

    return prompt


def generate_adversarial_prompt(context: ResearchContext, all_evidence: str) -> str:
    """
    Generate prompt for adversarial challenge.

    Args:
        context: Research context with classification
        all_evidence: All evidence gathered across tiers

    Returns:
        Complete adversarial challenge prompt
    """
    p_arch = context.probability_architect_pct

    prompt = f"""# Adversarial Challenge

## Your Role
You are a skeptical reviewer. Your job is to find weaknesses in the current classification and try to prove it WRONG.

## Current Assessment
- **Bank**: {context.bank_name}
- **Provisional Classification**: {context.classification} ({context.sub_classification})
- **Confidence**: {context.confidence}%
- **P(ARCHITECT)**: {p_arch:.1f}%
- **Evidence Items**: {context.evidence_count}

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


def generate_synthesis_prompt(context: ResearchContext, all_outputs: Dict[str, str]) -> str:
    """
    Generate prompt for final synthesis.

    Args:
        context: Research context with final probabilities
        all_outputs: Dictionary of all stage outputs

    Returns:
        Complete synthesis prompt
    """
    prompt = f"""# Final Synthesis - {context.bank_name}

## Your Task
Create the final research assessment for {context.bank_name}.

## Current State
- **P(ARCHITECT)**: {context.probability_architect_pct:.1f}%
- **Classification**: {context.classification} ({context.sub_classification})
- **Confidence**: {context.confidence}%
- **Evidence Items**: {context.evidence_count}
- **Adversarial Verdict**: {context.adversarial_verdict}

## Required Outputs

You MUST create these files in order:

### 1. confidence-calibration.md (CREATE FIRST)
Follow the 6-step confidence calibration process:
1. Maximum by Tier (what's our tier cap?)
2. Corroboration Adjustment (how many sources?)
3. Contradiction Adjustment (any conflicts?)
4. Adversarial Adjustment (verdict impact?)
5. Coherence Check (consistent with peers?)
6. Final Calculation

### 2. assessment.md
Create the full assessment with all 19 sections from the template.
Ensure the confidence value MATCHES what you calculated in step 1.

### 3. framework-integration.md
Quick-copy formats for client deliverables.

## Evidence Summary
"""

    for stage, content in all_outputs.items():
        if content:
            # Truncate for prompt size
            truncated = content[:2000] + "..." if len(content) > 2000 else content
            prompt += f"\n### {stage}\n{truncated}\n"

    prompt += """

## Instructions
1. Read templates/per-bank-output.md for the required assessment structure
2. Read templates/confidence-calibration-output.md for the calibration process
3. Create confidence-calibration.md FIRST
4. Use the calculated confidence in assessment.md
5. Ensure all 19 sections are complete

Now generate the final synthesis.
"""

    return prompt


def generate_gate_prompt(context: ResearchContext, gate_number: int, tier_evidence: str) -> str:
    """
    Generate prompt for reasoning gate.

    Args:
        context: Research context
        gate_number: Gate number (1, 2, or 3)
        tier_evidence: Evidence from corresponding tier

    Returns:
        Complete reasoning gate prompt
    """
    p_arch = context.probability_architect_pct

    thresholds = load_decision_thresholds()
    skip_threshold = thresholds.get('skip_to_adversarial', 80)

    prompt = f"""# Reasoning Gate {gate_number}

## Current State
- **Bank**: {context.bank_name}
- **P(ARCHITECT)**: {p_arch:.1f}%
- **Evidence Items**: {context.evidence_count}
- **Highest Tier Searched**: {context.highest_tier}

## Evidence from Tier {gate_number}
{tier_evidence}

## Decision Points

### 1. Skip Decision
Should we skip remaining tiers and proceed to adversarial?

**Skip Criteria**:
- P(ARCHITECT) >= {skip_threshold}% (very likely ARCHITECT)
- P(ARCHITECT) <= {100 - skip_threshold}% (very likely PRAGMATIST)

Current probability: {p_arch:.1f}%
Skip threshold: {skip_threshold}%

**Decision**: [SKIP / CONTINUE]
**Reasoning**: [why]

### 2. Evidence Delta Assessment
How much did Tier {gate_number} change our understanding?

- Prior P(ARCHITECT): [before tier {gate_number}]%
- Posterior P(ARCHITECT): {p_arch:.1f}%
- Delta: [change]%

Is this delta meaningful (>5%) or marginal (<5%)?

### 3. Observable Implications Test
What should we expect to see next if our classification is correct?

If ARCHITECT:
- [ ] We should find [specific evidence] in Tier {gate_number + 1}
- [ ] We should NOT find [specific evidence]

If PRAGMATIST:
- [ ] We should find [specific evidence] in Tier {gate_number + 1}
- [ ] We should NOT find [specific evidence]

### 4. Contradiction Check
Are there any contradictions in the evidence so far?

- [ ] No contradictions detected
- [ ] Minor contradictions (can be explained)
- [ ] Major contradictions (require resolution)

## Output

### Gate {gate_number} Decision
**Proceed to**: [Tier {gate_number + 1} / Adversarial / Block for Review]
**Confidence in Decision**: [High / Medium / Low]
**Key Reasoning**: [1-2 sentences]
"""

    return prompt
