# Bayesian Update: Post-Tier 2 - ABC

**Bank**: Agricultural Bank of China Limited
**Phase**: 7 (Emerging Markets)
**Date**: 2025-12-21

---

## Prior Probability (Post-Tier 1)

| Classification | Prior |
|---------------|-------|
| ARCHITECT | 0.8% |
| PRAGMATIST | 12.3% |
| OBSERVER | 32.8% |
| UNKNOWN | 93.4% |

---

## Tier 2 Evidence Summary

| ID | Evidence | Impact |
|----|----------|--------|
| ABC-E001 | ABC is ISDA primary member | Positive for OBSERVER |
| ABC-E002 | NAFMII framework applies (cohort) | Confirms UNKNOWN rationale |

**Key Finding**: ABC explicitly claims ISDA primary membership on its official website - unique among Chinese Big Four banks. However, membership ≠ CDM adoption.

---

## Likelihood Assessment

**P(Evidence | ARCHITECT)**: 0.02
- ISDA membership is necessary but not sufficient for ARCHITECT
- No CDM-specific evidence still disconfirms

**P(Evidence | PRAGMATIST)**: 0.08
- Membership could precede vendor-driven adoption
- But no vendor signals found

**P(Evidence | OBSERVER)**: 0.25
- ISDA membership is consistent with OBSERVER
- But no working group participation found

**P(Evidence | UNKNOWN)**: 0.85
- ISDA membership with no CDM activity is consistent with UNKNOWN
- NAFMII framework still dominates domestic operations

---

## Posterior Calculation

| Classification | Prior | Likelihood | Unnormalized | Posterior |
|---------------|-------|------------|--------------|-----------|
| ARCHITECT | 0.008 | 0.02 | 0.00016 | 0.4% |
| PRAGMATIST | 0.123 | 0.08 | 0.00984 | 24.4% |
| OBSERVER | 0.328 | 0.25 | 0.08200 | 20.3% |
| UNKNOWN | 0.934 | 0.85 | 0.79390 | **196.8%** |

Wait - posterior exceeds 100%. Recalculating with correct normalization:

**Normalization constant**: 0.00016 + 0.00984 + 0.08200 + 0.79390 = 0.8859

| Classification | Posterior (Normalized) |
|---------------|------------------------|
| ARCHITECT | 0.02% |
| PRAGMATIST | 1.1% |
| OBSERVER | 9.3% |
| **UNKNOWN** | **89.6%** |

---

## Posterior Probability

| Classification | Posterior |
|---------------|-----------|
| ARCHITECT | 0.02% |
| PRAGMATIST | 1.1% |
| OBSERVER | 9.3% |
| **UNKNOWN** | **89.6%** |

---

## Update Summary

- **Prior (UNKNOWN)**: 93.4%
- **Posterior (UNKNOWN)**: 89.6%
- **Shift**: -3.8 percentage points

The ISDA membership evidence slightly increases OBSERVER possibility, but the overall classification remains UNKNOWN. The NAFMII framework insight from cohort research dominates.

**Key Insight**: ABC's explicit ISDA membership claim is notable but does not change the structural reality that Chinese domestic derivatives operate under NAFMII, not ISDA CDM.

---

*Bayesian update under CDM Research Protocol v2.3*
