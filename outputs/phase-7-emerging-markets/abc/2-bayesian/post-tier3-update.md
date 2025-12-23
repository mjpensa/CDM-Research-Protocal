# Bayesian Update: Post-Tier 3 - ABC

**Bank**: Agricultural Bank of China Limited
**Phase**: 7 (Emerging Markets)
**Date**: 2025-12-21

---

## Prior Probability (Post-Tier 2)

| Classification | Prior |
|---------------|-------|
| ARCHITECT | 0.02% |
| PRAGMATIST | 1.1% |
| OBSERVER | 9.3% |
| UNKNOWN | 89.6% |

---

## Tier 3 Evidence Summary

**Status**: Not Searched

Per cohort pattern established by ICBC, Bank of China, and CCB research:
- Tier 3 signals (job postings, LinkedIn) are structurally irrelevant for Chinese Big Four banks
- NAFMII framework means CDM-related hiring signals would not exist
- Resource allocation prioritized for banks where Tier 3 could change classification

---

## Likelihood Assessment

**P(Null Evidence | ARCHITECT)**: 0.99
- No change - ARCHITECT already effectively ruled out

**P(Null Evidence | PRAGMATIST)**: 0.95
- No change - PRAGMATIST highly unlikely

**P(Null Evidence | OBSERVER)**: 0.90
- No change - OBSERVER possible but unverified

**P(Null Evidence | UNKNOWN)**: 0.99
- Expected result for NAFMII framework bank

---

## Posterior Calculation

With null evidence, likelihoods are near-uniform, producing minimal update:

| Classification | Prior | Likelihood | Unnormalized | Posterior |
|---------------|-------|------------|--------------|-----------|
| ARCHITECT | 0.0002 | 0.99 | 0.000198 | 0.02% |
| PRAGMATIST | 0.011 | 0.95 | 0.01045 | 1.1% |
| OBSERVER | 0.093 | 0.90 | 0.0837 | 8.5% |
| UNKNOWN | 0.896 | 0.99 | 0.88704 | **90.4%** |

**Normalization constant**: 0.9814

---

## Final Posterior Probability

| Classification | Posterior |
|---------------|-----------|
| ARCHITECT | 0.02% |
| PRAGMATIST | 1.1% |
| OBSERVER | 8.5% |
| **UNKNOWN** | **90.4%** |

---

## Cumulative Update Summary

| Stage | UNKNOWN Probability |
|-------|---------------------|
| Prior | 60.0% |
| Post-Tier 1 | 93.4% |
| Post-Tier 2 | 89.6% |
| **Post-Tier 3** | **90.4%** |

---

## Classification Decision

**Classification**: UNKNOWN
**Subtype**: NAFMII Framework
**Confidence**: 40% (capped per tier/evidence constraints)
**Maturity Score**: 0

**Rationale**: ABC is part of the Chinese Big Four cohort. All four banks operate under NAFMII framework for domestic derivatives, which is structurally separate from ISDA CDM. ABC's explicit ISDA membership claim is notable but does not translate to CDM adoption.

---

*Bayesian update under CDM Research Protocol v2.3*
