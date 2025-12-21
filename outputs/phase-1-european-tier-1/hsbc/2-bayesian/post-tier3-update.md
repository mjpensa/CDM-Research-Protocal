# Bayesian Update: Post-Tier 3 Evidence

**Bank**: HSBC Holdings plc
**Date**: 2025-12-20
**Prior P(ARCHITECT) (post-Tier 2)**: 27%

---

## Tier 3 Evidence Summary

| ID | Evidence | Direction | LR |
|----|----------|-----------|-----|
| (null) | No FINOS CDM contributor found | SUPPORTS_PRAGMATIST | 0.8 |
| (null) | No CDM involvement in general searches | SUPPORTS_PRAGMATIST | 0.85 |
| (null) | No CDM job postings (2024-2025) | SUPPORTS_PRAGMATIST | 0.85 |
| (null) | No Risk.net CDM coverage (unlike Barclays) | SUPPORTS_PRAGMATIST | 0.9 |

## Null Results Analysis

All Tier 3 searches returned null results:
- **FINOS Contributor Status**: HSBC not listed as contributor to FINOS CDM projects
- **General CDM Searches**: No results in comprehensive CDM/ISDA/model searches
- **CDM Hiring Signals**: No CDM-specific job postings found in 2024-2025
- **Press Coverage**: Risk.net covers HSBC derivatives leadership but never mentions CDM

These are **informative absences** - if HSBC were implementing CDM, at minimum we would expect hiring signals given their scale.

## Likelihood Ratio Calculation

**Combined LR (Tier 3)** = 0.8 × 0.85 × 0.85 × 0.9 = **0.518**

## Posterior Calculation

```
Prior odds (post-Tier 2) = 0.27 / 0.73 = 0.370
Posterior odds = 0.370 × 0.518 = 0.192
Posterior P(ARCHITECT) = 0.192 / (1 + 0.192) = 0.161 = 16.1%
```

## Final Probability

| Metric | Value |
|--------|-------|
| **P(ARCHITECT)** | 16% |
| **P(PRAGMATIST)** | 84% |
| **Direction of Movement** | Decreased (27% → 16%) |

## Cumulative Evidence Summary

| Tier | Combined LR | Running Product |
|------|-------------|-----------------|
| Prior | - | 0.333 (odds) |
| Tier 1 | 1.4 | 0.466 |
| Tier 2 | 0.765 | 0.357 |
| Tier 3 | 0.518 | 0.185 |

**Final Odds**: 0.185
**Final P(ARCHITECT)**: 16%

## Evidence Quality Summary

| Tier | Positive Evidence | Negative/Absent Evidence |
|------|-------------------|-------------------------|
| Tier 1 | DRR Pilot 2018-2019 | DTCC traditional EMIR approach |
| Tier 2 | None | Calypso traditional platform, €22.2T no CDM mention |
| Tier 3 | None | No FINOS, no hiring, no press, no general CDM mention |

## Confidence Assessment

- **Final Confidence**: 50%
- **Confidence Cap Applied**: 95% (highest tier is Tier 1 official sources)
- **Limiting Factors**:
  - DRR pilot is 5+ years old with documented conclusion phase
  - Multiple informative absences across Tier 2-3
  - No recent signals of CDM engagement
  - Traditional regulatory and technology approach documented

---

*All tiers complete. Proceeding to adversarial challenge.*
