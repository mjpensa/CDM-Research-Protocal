# Bayesian Update: Post-Tier 1 Evidence

**Bank**: NatWest Group plc
**Date**: 2025-12-20
**Prior P(ARCHITECT)**: 20%

---

## Tier 1 Evidence Summary

| ID | Evidence | Direction | LR |
|----|----------|-----------|-----|
| NW-001 | UK FCA/BoE DRR Pilot participant (2018-2019) | SUPPORTS_ARCHITECT | 2.0 |
| NW-002 | FINOS Fluxnova co-maintainer (NOT CDM) | NEUTRAL | 1.2 |
| -- | FINOS CDM contributor search (null result) | SUPPORTS_PRAGMATIST | 0.7 |

## Likelihood Ratio Calculation

**Combined LR (Tier 1)** = 2.0 × 1.2 × 0.7 = **1.68**

## Posterior Calculation

```
Prior odds = 0.20 / 0.80 = 0.25
Posterior odds = 0.25 × 1.68 = 0.42
Posterior P(ARCHITECT) = 0.42 / (1 + 0.42) = 0.296 = 29.6%
```

## Updated Probability

| Metric | Value |
|--------|-------|
| **P(ARCHITECT)** | 30% |
| **P(PRAGMATIST)** | 70% |
| **Direction of Movement** | Increased (20% → 30%) |

## Key Insights

1. **Historical Pilot Engagement**: NatWest participated in UK FCA DRR pilot using ISDA CDM 2.0 in 2018-2019
2. **FINOS Paradox**: Demonstrates open-source capability (Fluxnova) but NOT contributing to CDM
3. **Dated Evidence**: Pilot evidence is 5+ years old with no recent follow-up
4. **Capability Without Application**: Has FINOS capability but chooses not to apply it to CDM

## Confidence Assessment

- **Tier 1 Evidence Quality**: Moderate (1 historical pilot + 1 informative absence)
- **Highest Tier Cap**: 95% (Tier 1 present)
- **Applied Confidence**: 40% (historical evidence + informative absence pattern)

---

*Proceeding to Tier 2 evidence gathering.*
