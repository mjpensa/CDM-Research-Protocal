# Bayesian Update: Post-Tier 3 - ING Group

**Bank:** ING Group
**Phase:** 4 - European Tier 2
**Update Date:** 2025-12-20

---

## Prior Probability (Post-Tier 2)

| Parameter | Value |
|-----------|-------|
| P(ARCHITECT) | 0.026 |
| P(PRAGMATIST) | 0.974 |

## Tier 3 Evidence Summary

| Evidence ID | Description | Direction | Likelihood Ratio |
|-------------|-------------|-----------|------------------|
| *None* | No Tier 3 evidence found | N/A | N/A |

## Null Result Impact

**Final Informative Absence:**

- No CDM-related job postings at ING
- No LinkedIn profiles indicating CDM work at ING
- No hiring signals for ISDA/FINOS expertise

**Likelihood Ratio for Tier 3 Null Result:** 0.85
- Hiring signals would indicate intent even without production
- Absence confirms non-adoption trajectory

## Posterior Calculation

```
LR = P(E|ARCHITECT) / P(E|PRAGMATIST) = 0.5 / 0.9 = 0.56

Prior odds = 0.026 / 0.974 = 0.027
Posterior odds = 0.027 × 0.56 = 0.015

P(ARCHITECT|E) = 0.015 / (1 + 0.015) = 0.015 ≈ 1.5%
```

## Final Probabilities

| Parameter | Prior | Post-T1 | Post-T2 | Post-T3 |
|-----------|-------|---------|---------|---------|
| P(ARCHITECT) | 0.15 | 0.055 | 0.026 | 0.015 |
| P(PRAGMATIST) | 0.85 | 0.945 | 0.974 | 0.985 |

## Evidence Trajectory

```
ARCHITECT Probability: 15% → 5.5% → 2.6% → 1.5%
                        ↓       ↓       ↓
                      -63%    -53%    -42%
```

The probability of ARCHITECT classification has declined 90% from prior through evidence collection.

## Classification Threshold Check

Per `config/decision-thresholds.json`:
- ARCHITECT threshold: P > 0.65
- PRAGMATIST threshold: P > 0.65
- Current P(PRAGMATIST): 0.985 ✓ Exceeds threshold

## Decision

**Proceed to Adversarial Challenge** - Strong evidence for PRAGMATIST, but must validate with adversarial review.

However, given complete absence of evidence, classification may be **UNKNOWN** rather than PRAGMATIST, as we cannot positively confirm pragmatist behaviors (vendor usage, traditional platforms, etc.) - only the absence of architect behaviors.
