# Post-Tier 2 Bayesian Update: Citigroup Inc.

**Research Phase**: 8 (US Major Banks)
**Bank**: Citigroup Inc.
**Date**: 2025-12-21

---

## Prior Probability (Post-Tier 1)

- P(ARCHITECT) = 0.05
- P(PRAGMATIST) = 0.83
- P(OBSERVER) = 0.13

---

## Tier 2 Evidence Impact

### Evidence Collected
- **Count**: 1 Tier 2 evidence item
- **Source**: FINOS membership confirmation (ecosystem participation)
- **Claim Type**: Membership/participation (but not CDM-specific)

### Specific Evidence
1. **FINOS Hackathon Sponsor (Oct-Nov 2024)**
   - Hosted first FINOS-supported hackathon in India
   - General FINOS engagement, not CDM-focused
   - Tier 2 evidence (trade press coverage)

### Likelihood Ratios
Given FINOS membership but no CDM contribution:
- **P(FINOS member, no CDM | ARCHITECT)** = 0.10 (unlikely - architects typically contribute to CDM)
- **P(FINOS member, no CDM | PRAGMATIST)** = 0.30 (moderate - ecosystem engagement without deep commitment)
- **P(FINOS member, no CDM | OBSERVER)** = 0.70 (likely - passive participation)

### Bayesian Update Calculation

- **P(ARCHITECT | Evidence)** = (0.05 × 0.10) / [(0.05 × 0.10) + (0.83 × 0.30) + (0.13 × 0.70)]
- **P(ARCHITECT | Evidence)** = 0.005 / [0.005 + 0.249 + 0.091] = 0.005 / 0.345 = 0.014 (1.4%)

- **P(PRAGMATIST | Evidence)** = (0.83 × 0.30) / 0.345 = 0.249 / 0.345 = 0.722 (72.2%)

- **P(OBSERVER | Evidence)** = (0.13 × 0.70) / 0.345 = 0.091 / 0.345 = 0.264 (26.4%)

---

## Posterior Probability

After Tier 2 research:
- **P(ARCHITECT)** = 0.01 (down from 0.05)
- **P(PRAGMATIST)** = 0.72 (down from 0.83)
- **P(OBSERVER)** = 0.26 (up from 0.13)

**Interpretation**: FINOS membership suggests ecosystem awareness, but the absence of CDM-specific contribution shifts probability toward OBSERVER classification. The bank is engaged in fintech open source community but not actively building on CDM.

---

## Confidence Calibration

- **Tier 2 evidence only**: Maximum confidence capped at 75% per protocol
- **Single source concern**: FINOS membership from one source
- **Actual confidence**: ~50% given limited evidence and absence of corroboration

---

## Classification Trajectory

The evidence pattern suggests:
1. **Not ARCHITECT**: No production usage, no pilot, no code contribution
2. **Questionable PRAGMATIST**: No vendor proxy signals, no implementation evidence
3. **Likely OBSERVER**: Ecosystem member without technical engagement

**Preliminary Classification**: OBSERVER (Ecosystem-Engaged)

---

## Next Steps

Proceed to Tier 3 research focusing on:
1. LinkedIn profiles mentioning CDM work at Citigroup
2. Job postings for CDM-related positions
3. Conference speaker mentions
4. GitHub personal profiles of Citigroup employees

---

**Methodology**: Bayesian inference following Tetlock superforecasting principles
