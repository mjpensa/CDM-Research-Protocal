# Bayesian Update: Post-Tier 1 - ING Group

**Bank:** ING Group
**Phase:** 4 - European Tier 2
**Update Date:** 2025-12-20

---

## Prior Probability

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| P(ARCHITECT) | 0.15 | European Tier 2 bank, no prior CDM signals |
| P(PRAGMATIST) | 0.85 | Default assumption per protocol |

## Tier 1 Evidence Summary

| Evidence ID | Description | Direction | Likelihood Ratio |
|-------------|-------------|-----------|------------------|
| *None* | No Tier 1 evidence found | N/A | N/A |

## Null Result Impact

**Informative Absence:** The lack of Tier 1 evidence is itself informative.

- ING is not listed as FINOS member
- No CDM contributors from ING on GitHub
- No ISDA CDM working group participation
- No official CDM announcements

**Likelihood Ratio for Null Result:** 0.7
- Banks pursuing CDM would likely have Tier 1 signals
- Absence weakly supports PRAGMATIST hypothesis

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

| Parameter | Prior | Posterior | Change |
|-----------|-------|-----------|--------|
| P(ARCHITECT) | 0.15 | 0.055 | -0.095 |
| P(PRAGMATIST) | 0.85 | 0.945 | +0.095 |

## Decision

**Continue to Tier 2 search** - Null results from Tier 1 do not preclude Tier 2 evidence.
