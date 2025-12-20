# Confidence Calibration Output Template

## Purpose

This template documents the per-bank confidence calculation. It provides an audit trail for how the final confidence percentage was determined, ensuring calibration consistency across banks.

**CRITICAL**: This file MUST be created BEFORE assessment.md. The confidence value in assessment.md MUST match the value calculated here.

---

## Template: confidence-calibration.md

**Location**: `outputs/phase-[N]/[bank_id]/5-synthesis/confidence-calibration.md`

---

```markdown
# Confidence Calibration: [BANK NAME]

**Date**: [YYYY-MM-DD]
**Analyst**: [Name/ID]
**Prior Assessment**: [Reference to previous assessment if exists]

---

## 1. Classification Summary

| Field | Value |
|-------|-------|
| **Posture** | [ARCHITECT / PRAGMATIST / UNKNOWN] |
| **Variant** | [Native / Leader / Follower / Vendor-Dependent / etc.] |
| **Bayesian Posterior** | [X]% P(Architect) |

---

## 2. Evidence Tier Assessment

### Highest Tier Present

| Tier | Evidence Count | Key Sources |
|------|----------------|-------------|
| Tier 1 (Official) | [N] | [List key sources] |
| Tier 2 (Industry) | [N] | [List key sources] |
| Tier 3 (Indirect) | [N] | [List key sources] |

**Highest Tier**: Tier [1/2/3]
**Maximum Confidence Cap**: [95/75/50/35]%

---

## 3. Calibration Calculation

### Step 1: Maximum by Tier

| Factor | Value |
|--------|-------|
| Highest evidence tier present | Tier [N] |
| Maximum confidence cap | [X]% |

### Step 2: Corroboration Adjustment

| Factor | Count | Adjustment |
|--------|-------|------------|
| Independent sources supporting classification | [N] | [+10/+5/0/-10]% |
| 3+ independent sources | +10% | |
| 2 independent sources | +5% | |
| 1 source only | +0% | |
| Uncorroborated | -10% | |

**Corroboration Adjustment**: [+/-X]%

### Step 3: Contradiction Assessment

| Factor | Status | Adjustment |
|--------|--------|------------|
| Contradictions detected | [Yes/No] | |
| Resolution status | [Resolved/Unresolved/None] | |
| No contradictions | +0% | |
| Minor contradiction (resolved) | -5% | |
| Significant contradiction (resolved) | -10% | |
| Unresolved contradiction | -15% to -25% | |

**Contradiction Adjustment**: [+/-X]%

**If contradictions exist, reference**: `3-gates/contradiction-resolution.md`

### Step 4: Adversarial Survival

| Factor | Result | Adjustment |
|--------|--------|------------|
| Adversarial challenge outcome | [See 4-adversarial/verdict.md] | |
| Strengthened by challenge | +5% | |
| Unchanged | +0% | |
| Weakened but maintained | -5% | |
| Required revision | -10% | |

**Adversarial Adjustment**: [+/-X]%

### Step 5: Coherence Check

| Factor | Status | Adjustment |
|--------|--------|------------|
| Consistent with anchor banks | [Yes/No] | |
| Consistent with peer banks | [Yes/No] | |
| Fully consistent | +5% | |
| Minor inconsistency (explained) | +0% | |
| Inconsistency requiring explanation | -5% | |
| Significant incoherence | -10% | |

**Coherence Adjustment**: [+/-X]%

### Step 6: Final Calculation

```
Starting Maximum (Tier [N]):           [X]%
+ Corroboration Adjustment:           [+/-X]%
+ Contradiction Adjustment:           [+/-X]%
+ Adversarial Adjustment:             [+/-X]%
+ Coherence Adjustment:               [+/-X]%
----------------------------------------
Raw Calculated Confidence:             [X]%

Floor (minimum 20%):                   [X]%
Ceiling (maximum 95%):                 [X]%
----------------------------------------
FINAL CONFIDENCE:                      [X]%
```

---

## 4. Betting Test

The betting test validates calibration by checking if you would actually bet at the implied odds.

| Confidence | Implied Odds | Bet Structure |
|------------|--------------|---------------|
| [Final]% | [Y]:1 | I risk $[Y] to win $1 if right |

**Question**: If someone offered me a bet at [Y]:1 odds that this classification is correct, would I take it?

**Answer**: [Yes/No]

**If No**: Adjusted confidence should be [X]% based on odds I would actually accept.

**Betting Test Passed**: [YES/NO]

---

## 5. Confidence Rationale

[2-3 sentences explaining why this confidence level is appropriate for this bank. Reference specific evidence quality, corroboration, and any limiting factors.]

Example:
> "Confidence is set at 72% based on strong Tier 2 evidence from multiple trade press sources, but capped below the Tier 1 maximum of 95% because no official bank announcement confirms CDM adoption. The betting test confirms willingness to give 2.5:1 odds, consistent with stated confidence."

---

## 6. What Would Change Confidence

### To Increase Confidence

| Evidence Type | Potential Impact |
|---------------|------------------|
| [Description of evidence needed] | +[X]% |
| [Description of evidence needed] | +[X]% |

### To Decrease Confidence

| Evidence Type | Potential Impact |
|---------------|------------------|
| [Description of disconfirming evidence] | -[X]% |
| [Description of disconfirming evidence] | -[X]% |

---

## 7. Cross-Bank Consistency Check

Compare confidence with similar banks in this phase:

| Bank | Highest Tier | # Sources | Confidence | Consistent? |
|------|--------------|-----------|------------|-------------|
| [This Bank] | Tier [N] | [X] | [X]% | - |
| [Peer Bank 1] | Tier [N] | [X] | [X]% | [Yes/No] |
| [Peer Bank 2] | Tier [N] | [X] | [X]% | [Yes/No] |

**Consistency Assessment**: [Pass/Fail]

If inconsistent, explain:
[Why this bank's confidence differs from peers with similar evidence profiles]

---

## 8. Validation Checklist

Before finalizing this confidence calibration:

- [ ] Maximum confidence matches tier cap from CLAUDE.md Section 7
- [ ] All adjustments are justified with specific references
- [ ] Betting test was honestly answered
- [ ] Rationale explains the confidence level clearly
- [ ] Cross-bank consistency was checked
- [ ] Final confidence is between 20% and 95%
- [ ] This file was created BEFORE assessment.md

---

## Metadata

| Field | Value |
|-------|-------|
| Template Version | 1.0 |
| Created | [YYYY-MM-DD] |
| Last Updated | [YYYY-MM-DD] |
| Methodology Reference | methodology/confidence-calibration.md |
```

---

## Usage Notes

1. **Timing**: Create this file at the START of the Synthesis stage, before writing assessment.md
2. **Cross-Reference**: The confidence value here MUST be copied exactly to assessment.md
3. **Updates**: If confidence changes during synthesis, update BOTH files
4. **Validation**: run_pipeline.py will check that confidence values match

---

## Integration with Workflow

This output is created during **Stage 14: Synthesis** per docs/workflow.md.

**Inputs Required**:
- evidence.json (trust_metrics from trust_audit)
- 2-bayesian/post-tier*-update.md (Bayesian posterior)
- 4-adversarial/verdict.md (adversarial outcome)
- 3-gates/contradiction-resolution.md (if exists)

**Outputs Dependent on This File**:
- 5-synthesis/assessment.md (must copy confidence value)
- Final_Report.md (uses confidence in summary)

---

_Template Version: 1.0_
_Last Updated: 2025-12-20_
