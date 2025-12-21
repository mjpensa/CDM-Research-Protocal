# Example: Gate 1 Skip-to-Adversarial Decision

## Context

After Tier 1 evidence gathering for BNP Paribas. Evaluating whether to skip Tier 2/3 and proceed directly to adversarial review.

## Input State

- **Bank**: BNP Paribas
- **Prior P(Architect)**: 40% (default)
- **Post-Tier 1 P(Architect)**: 87%
- **Skip Threshold**: 80% (from `config/decision-thresholds.json`)

### Tier 1 Evidence Summary

| ID | Finding | Direction | LR |
|----|---------|-----------|-----|
| BNP-001 | Official press release: "CDM in production for EMIR Refit" | ARCHITECT | 200 |
| BNP-002 | Named contributor on FINOS CDM GitHub | ARCHITECT | 12 |
| BNP-003 | Annual report mentions CDM initiative | ARCHITECT | 5 |
| NULL-1 | No pilot-only status found | NEUTRAL | 1.0 |

---

## Gate 1 Required Sections

### 1. Evidence Delta Analysis

| Evidence | Prior Belief | Impact | Post-Tier 1 Belief |
|----------|--------------|--------|-------------------|
| BNP-001: Official production | Expected pilot at best | Very strong shift | Production confirmed |
| BNP-002: FINOS contributor | Expected no contribution | Moderate shift | Active participant |
| BNP-003: Annual report mention | Expected no mention | Weak shift | Strategic priority |

**Net Delta**: +47 percentage points (40% -> 87%)

### 2. Probability Update

```
Prior odds = 0.40 / 0.60 = 0.667
Combined LR = 200 x 12 x 5 = 12,000
Posterior odds = 0.667 x 12,000 = 8,004
P(Architect) = 8,004 / 8,005 = 99.99%

SANITY CHECK TRIGGERED: Combined LR > 1000
Applying LR dampening per methodology...

Dampened LR = sqrt(12,000) x 10 = 1,095
Posterior odds = 0.667 x 1,095 = 730
P(Architect) = 730 / 731 = 99.86%

Applying confidence cap (Tier 1 only = 95%)
Final P(Architect) = 87% (calibrated with recency/specificity adjustments)
```

### 3. Evidence Sufficiency Check

**Question**: Can we classify with confidence exceeding skip threshold (80%)?

| Criterion | Status | Notes |
|-----------|--------|-------|
| P(Architect) > 80% | YES | 87% exceeds threshold |
| Official source confirms production | YES | BNP-001 is definitive |
| Corroboration present | YES | BNP-002 and BNP-003 support |
| No contradictions | YES | Evidence is consistent |
| Recency acceptable | YES | Press release dated 2024 |

**Sufficiency Verdict**: SUFFICIENT for skip decision

### 4. Disconfirmation Test

**What would DISPROVE ARCHITECT classification?**

1. Official statement saying "vendor-only approach"
2. Evidence of CDM project cancellation
3. Retraction of production announcement

**Was it searched?**
- YES: Searched for "BNP Paribas CDM vendor" and "outsource" - no results
- YES: Searched for "BNP Paribas CDM pilot cancelled" - no results

**Disconfirming evidence found?** NO

### 5. Counterfactual Test

**If opposite evidence found, how would assessment change?**

If we found:
- BNP Paribas announces "vendor-managed CDM only" -> Would shift to PRAGMATIST (Vendor-Dependent)
- Press release retracted -> Would require Tier 2 confirmation
- FINOS contribution was one-time, years ago -> Would reduce confidence by ~15%

**Counterfactual impact**: High - evidence is informative, not trivial.

### 6. Mini-Adversarial Check

**Challenge strongest Tier 1 evidence (BNP-001)**:

*Devil's advocate*: The press release could be aspirational. "In production" might mean "in production testing" rather than live trading.

*Counter*: The specific phrase was "CDM implementation for EMIR Refit regulatory reporting now live." This language is unambiguous - "live" indicates operational status, not testing.

*Verdict*: Challenge fails. Evidence stands.

### 7. Gate Clearance

| Check | Status |
|-------|--------|
| All sections complete | YES |
| Probability matches Bayesian file | YES |
| Counterfactual shows evidence informative | YES |
| Mini-adversarial addressed | YES |
| No contradictions flagged | YES |

---

## Skip Decision

**P(Architect) = 87%** > **Skip Threshold = 80%**

**DECISION: SKIP TO ADVERSARIAL**

**Rationale**:
1. Official production announcement from bank (highest-tier evidence)
2. Corroborated by FINOS contribution and annual report
3. No disconfirming evidence found
4. 87% confidence exceeds 80% skip threshold
5. Additional Tier 2/3 searches unlikely to change classification

**Note**: Skipping does NOT skip adversarial review. Adversarial challenge still required before synthesis.

---

## Output Summary

```
Gate 1 Clearance: PASS
Decision: SKIP_TO_ADVERSARIAL
P(Architect): 87%
Classification Leaning: ARCHITECT-Active
Proceed to: Stage 4 (Adversarial Challenge)
Skip: Tier 2, Tier 3, Gate 2, Gate 3
```
