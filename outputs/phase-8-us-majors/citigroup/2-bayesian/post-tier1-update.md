# Post-Tier 1 Bayesian Update: Citigroup Inc.

**Research Phase**: 8 (US Major Banks)
**Bank**: Citigroup Inc.
**Date**: 2025-12-21

---

## Prior Probability

**Null Hypothesis**: PRAGMATIST (Traditional)
- Prior P(ARCHITECT) = 0.30
- Prior P(PRAGMATIST) = 0.65
- Prior P(OBSERVER) = 0.05

**Rationale**: As a G16 derivatives dealer and major US bank, Citigroup faces significant regulatory reporting obligations (CFTC Rewrite, EMIR Refit). Base rate suggests moderate probability of CDM adoption.

---

## Tier 1 Evidence Impact

### Evidence Collected
- **Count**: 0 Tier 1 evidence items
- **Sources**: No official bank announcements, no regulatory filings mentioning CDM, no ISDA publications listing Citigroup CDM usage

### Likelihood Ratios
Given the absence of Tier 1 evidence for a major derivatives dealer:
- **P(No Tier 1 | ARCHITECT)** = 0.05 (very unlikely for true architects)
- **P(No Tier 1 | PRAGMATIST)** = 0.40 (moderately likely - may use CDM via vendors quietly)
- **P(No Tier 1 | OBSERVER)** = 0.80 (highly likely)

### Bayesian Update Calculation

Using Bayes' theorem:
- **P(ARCHITECT | No Tier 1)** = (0.30 × 0.05) / [(0.30 × 0.05) + (0.65 × 0.40) + (0.05 × 0.80)]
- **P(ARCHITECT | No Tier 1)** = 0.015 / [0.015 + 0.26 + 0.04] = 0.015 / 0.315 = 0.048 (4.8%)

- **P(PRAGMATIST | No Tier 1)** = (0.65 × 0.40) / 0.315 = 0.26 / 0.315 = 0.825 (82.5%)

- **P(OBSERVER | No Tier 1)** = (0.05 × 0.80) / 0.315 = 0.04 / 0.315 = 0.127 (12.7%)

---

## Posterior Probability

After Tier 1 research:
- **P(ARCHITECT)** = 0.05 (down from 0.30)
- **P(PRAGMATIST)** = 0.83 (up from 0.65)
- **P(OBSERVER)** = 0.13 (up from 0.05)

**Interpretation**: The complete absence of Tier 1 evidence significantly reduces the probability that Citigroup is an ARCHITECT. The probability shifts toward PRAGMATIST or OBSERVER.

---

## Confidence Adjustment

- **Maximum confidence after Tier 1**: Cannot exceed 35% (no Tier 1 evidence, relying on inference)
- **Direction**: Evidence absence suggests traditional approach or very quiet vendor-based adoption

---

## Next Steps

Proceed to Tier 2 research focusing on:
1. Trade press mentions of Citigroup derivatives technology modernization
2. Vendor partnership announcements (Murex, Calypso, etc.)
3. Conference presentations by Citigroup technology leaders
4. FINOS community engagement beyond membership

---

**Methodology**: Bayesian inference following Tetlock superforecasting principles
