# Bayesian Update: Post-Tier 1

**Bank**: Banco Bilbao Vizcaya Argentaria S.A.
**Phase**: 5 (Spanish)
**Date**: 2025-12-21

---

## Prior Probability

| Classification | Prior |
|---------------|-------|
| ARCHITECT | 5% |
| PRAGMATIST | 50% |
| OBSERVER | 30% |
| UNKNOWN | 15% |

**Rationale**: Per protocol null hypothesis with adjustments for:
- European regulatory pressure (EMIR Refit): +5%
- Medium derivatives relevance: -5%
- Known digital innovation leadership: +5%
- Santander precedent: +5%

---

## Tier 1 Evidence Summary

| Evidence ID | Claim | Direction |
|-------------|-------|-----------|
| BBVA-E001 | CFTC/SEC swap dealer registration | Neutral (establishes presence) |
| Null | No FINOS membership | Negative |
| Null | No ISDA Board/CDM governance | Negative |
| Null | No CDM production claims | Negative |

---

## Likelihood Ratios

### ARCHITECT Hypothesis
- P(No FINOS | ARCHITECT) = 0.1
- P(No ISDA Board | ARCHITECT) = 0.5
- **Combined**: 0.05

### PRAGMATIST Hypothesis
- P(No FINOS | PRAGMATIST) = 0.7
- P(No ISDA Board | PRAGMATIST) = 0.8
- **Combined**: 0.56

### OBSERVER Hypothesis
- P(No FINOS | OBSERVER) = 0.95
- P(No ISDA Board | OBSERVER) = 0.95
- **Combined**: 0.90

---

## Posterior Calculation

| Classification | Prior | Likelihood | Unnormalized | Posterior |
|---------------|-------|------------|--------------|-----------|
| ARCHITECT | 0.05 | 0.05 | 0.0025 | 1% |
| PRAGMATIST | 0.50 | 0.56 | 0.28 | 48% |
| OBSERVER | 0.30 | 0.90 | 0.27 | 46% |
| UNKNOWN | 0.15 | 0.1 | 0.015 | 5% |

---

## Post-Tier 1 Posterior

| Classification | Posterior |
|---------------|-----------|
| ARCHITECT | 1% |
| PRAGMATIST | 48% |
| OBSERVER | 46% |
| UNKNOWN | 5% |

---

## Key Insights

1. **Near parity between PRAGMATIST and OBSERVER**: Without CDM-specific evidence, these classifications are nearly equally probable.

2. **ARCHITECT effectively ruled out**: No FINOS membership or governance role makes ARCHITECT highly improbable.

3. **Tier 2 is critical**: Need to find distinguishing evidence between PRAGMATIST and OBSERVER - particularly whether BBVA participated in any CDM pilots.

---

## Decision

**Continue to Tier 2 searches**: Current evidence insufficient to distinguish PRAGMATIST from OBSERVER.
