# Bayesian Update: Post-Tier 1 Evidence

**Bank**: HSBC Holdings plc
**Date**: 2025-12-20
**Prior P(ARCHITECT)**: 25%

---

## Tier 1 Evidence Summary

| ID | Evidence | Direction | LR |
|----|----------|-----------|-----|
| HSBC-000 | UK DRR Pilot 2018-2019 using ISDA CDM 2.0 (pilot phase, not production) | SUPPORTS_ARCHITECT | 2.0 |
| HSBC-001 | EMIR REFIT reporting via DTCC Trade Repository (traditional approach) | SUPPORTS_PRAGMATIST | 0.7 |

## Likelihood Ratio Calculation

**Combined LR (Tier 1)** = 2.0 × 0.7 = **1.4**

## Posterior Calculation

```
Prior odds = 0.25 / 0.75 = 0.333
Posterior odds = 0.333 × 1.4 = 0.466
Posterior P(ARCHITECT) = 0.466 / (1 + 0.466) = 0.318 = 31.8%
```

## Updated Probability

| Metric | Value |
|--------|-------|
| **P(ARCHITECT)** | 32% |
| **P(PRAGMATIST)** | 68% |
| **Direction of Movement** | Increased (25% → 32%) |

## Key Insights

1. **DRR Pilot Significance**: HSBC participated in prestigious UK FCA/BoE DRR pilot with CDM 2.0, demonstrating engagement with advanced regulatory reporting
2. **Temporal Limitation**: Pilot ended in 2019 (5+ years old) with no evidence of continued CDM work
3. **Traditional Compliance Path**: HSBC's official EMIR REFIT page documents DTCC Trade Repository approach, not CDM-based reporting
4. **Unresolved Tension**: DRR pilot history suggests capability, but current regulatory approach is traditional

## Confidence Assessment

- **Tier 1 Evidence Quality**: Mixed (positive DRR history, but traditional current approach)
- **Highest Tier Cap**: 95% (Tier 1 present)
- **Applied Confidence**: 50% (pilot is historical; current approach is traditional)

---

*Proceeding to Tier 2 evidence gathering.*
