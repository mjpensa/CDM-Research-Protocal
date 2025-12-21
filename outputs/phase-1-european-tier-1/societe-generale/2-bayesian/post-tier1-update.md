# Bayesian Update: Post-Tier 1 Evidence

**Bank**: Société Générale
**Date**: 2025-12-20
**Prior P(ARCHITECT)**: 35%

---

## Tier 1 Evidence Summary

| ID | Evidence | Direction | LR |
|----|----------|-----------|-----|
| SG-002 | EMIR Refit compliance page (standard regulatory info) | NEUTRAL | 1.0 |
| (null) | No FINOS CDM contribution | NEUTRAL/NEG | 0.85 |
| (null) | No ISDA CDM contributor listing | NEUTRAL/NEG | 0.90 |

## Combined LR (Tier 1) = 1.0 × 0.85 × 0.90 = **0.765**

## Posterior Calculation

```
Prior odds = 0.35 / 0.65 = 0.538
Posterior odds = 0.538 × 0.765 = 0.412
Posterior P(ARCHITECT) = 0.412 / (1 + 0.412) = 0.29 = 29%
```

## Updated: P(ARCHITECT) = 29%

Tier 1 informative absences decrease probability - no FINOS/ISDA CDM involvement despite BNP Paribas peer being in production.

---

*Proceeding to Tier 2.*
