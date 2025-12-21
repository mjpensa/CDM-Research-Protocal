# Bayesian Update: Post-Tier 1 Evidence: ING Group N.V.

**Bank:** ING Group N.V.
**Phase:** 4 - Other European
**Date:** 2025-12-21

---

## Prior Probability

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| P(ARCHITECT) | 0.15 | European Tier 2 bank, no prior CDM signals |
| P(PRAGMATIST) | 0.85 | Default assumption per protocol |

## Tier 1 Evidence Summary

No Tier 1 evidence found.

## Likelihood Ratio Calculation

```
Combined LR = 1.0 (no evidence)
```

## Posterior Calculation

Using Bayes' theorem:

```
P(ARCHITECT|E) = P(E|ARCHITECT) × P(ARCHITECT) / P(E)

Where:
- P(E|ARCHITECT) = 0.3 (low - architects usually have Tier 1 evidence)
- P(E|PRAGMATIST) = 0.9 (high - pragmatists often lack Tier 1 evidence)
- P(ARCHITECT) = 0.15
- P(PRAGMATIST) = 0.85

LR = P(E|ARCHITECT) / P(E|PRAGMATIST) = 0.3 / 0.9 = 0.33

Posterior odds = Prior odds × LR
Prior odds = 0.15 / 0.85 = 0.176
Posterior odds = 0.176 × 0.33 = 0.058

P(ARCHITECT|E) = 0.058 / (1 + 0.058) = 0.055 ≈ 5.5%
```

## Updated Probabilities

| Metric | Value |
|--------|-------|
| P(ARCHITECT) | 0% |
| P(PRAGMATIST) | 1% |
| Confidence | 0% |

## Key Insights

N/A

---

*Proceeding to Tier 2.*
