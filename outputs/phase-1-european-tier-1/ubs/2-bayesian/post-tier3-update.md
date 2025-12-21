# Bayesian Update: Post-Tier 3 Evidence

**Bank**: UBS Group AG
**Date**: 2025-12-20
**Prior P(ARCHITECT) (post-Tier 2)**: 10%

---

## Tier 3 Evidence Summary

| ID | Evidence | Direction | LR |
|----|----------|-----------|-----|
| (null) | No CDM-related job postings found | SUPPORTS_PRAGMATIST | 0.75 |
| (null) | No current UBS CDM activity on LinkedIn | NEUTRAL | 0.95 |

## Null Results Analysis

Tier 3 searches for hiring signals and LinkedIn profiles returned null results:
- **Job Postings**: No CDM, DRR, or ISDA model positions advertised at UBS (integration-focused hiring only)
- **LinkedIn**: No visible CDM implementation activity by UBS staff

**Interpretation**: If UBS were planning post-2026 CDM restart, we would expect preliminary hiring signals or LinkedIn activity. The absence of such signals suggests either (a) integration remains all-consuming even in planning, or (b) post-integration CDM strategy is undecided.

## Likelihood Ratio Calculation

**Combined LR (Tier 3)** = 0.75 × 0.95 = **0.71**

## Posterior Calculation

```
Prior odds (post-Tier 2) = 0.10 / 0.90 = 0.111
Posterior odds = 0.111 × 0.71 = 0.079
Posterior P(ARCHITECT) = 0.079 / (1 + 0.079) = 0.073 = 7.3%
```

## Final Probability

| Metric | Value |
|--------|-------|
| **P(ARCHITECT)** | 7% |
| **P(PRAGMATIST)** | 93% |
| **Direction of Movement** | Decreased (10% → 7%) |

## Cumulative Evidence Summary

| Tier | Combined LR | Running Posterior |
|------|-------------|------------------|
| Prior | - | 10% |
| Tier 1 | 0.9 | 9% |
| Tier 2 | 1.17 | 10% |
| Tier 3 | 0.71 | 7% |

**Final Posterior P(ARCHITECT)**: 7%
**Final Posterior P(PRAGMATIST)**: 93%

## Evidence Quality Summary

| Tier | Positive Evidence | Negative/Absent Evidence |
|------|-------------------|-------------------------|
| Tier 1 | 2020 DAML pilot (Vinay Srinivas) | Integration consuming all capacity through 2026 |
| Tier 2 | Credit Suisse CDM capability (Sunil Challa) | Derivatives award with no CDM mention; no evidence of post-merger CDM strategy |
| Tier 3 | None | No job postings; no LinkedIn activity |

## Confidence Assessment

- **Final Confidence**: 60%
- **Confidence Cap Applied**: 75% (highest tier is Tier 2)
- **Limiting Factors**:
  - Tier 1 positive evidence (2020 pilot) is historical (5+ years old)
  - Tier 2 inherited capability may not survive integration or be relevant to UBS strategy
  - No current evidence of CDM work; all signals point to integration-constrained present
  - High probability space is PRAGMATIST (93%), not ARCHITECT

## Strategic Implication

UBS exhibits a unique pattern: **PRAGMATIST with historical and inherited capability**. Unlike Deutsche Bank (pure regulatory-driven PRAGMATIST) or other non-participants, UBS:
- Has demonstrated CDM engagement capability (2020 pilot)
- Acquired CDM-aware talent (Credit Suisse)
- But is currently blocked by integration constraints

**Reassessment Recommendation**: Q1 2027, when integration capacity should free up. At that point, determine whether UBS restarts CDM initiatives or continues pragmatist approach.

---

*All tiers complete. Proceeding to Reasoning Gates.*
