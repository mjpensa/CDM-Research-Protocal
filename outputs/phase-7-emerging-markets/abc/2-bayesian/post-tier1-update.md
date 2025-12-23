# Bayesian Update: Post-Tier 1 - ABC

**Bank**: Agricultural Bank of China Limited
**Phase**: 7 (Emerging Markets)
**Date**: 2025-12-21

---

## Prior Probability

| Classification | Prior | Rationale |
|---------------|-------|-----------|
| ARCHITECT | 5% | Possible but unlikely for Chinese state bank |
| PRAGMATIST | 15% | Some vendor adoption possible |
| OBSERVER | 20% | Possible ISDA membership |
| UNKNOWN | 60% | High prior - Chinese Big Four cohort pattern established |

**Prior Reasoning**: ICBC, Bank of China, and CCB all classified as UNKNOWN due to NAFMII framework. ABC expected to follow same pattern.

---

## Tier 1 Evidence Summary

| Evidence | Finding |
|----------|---------|
| ISDA CDM involvement | None found |
| FINOS membership | None found |
| DRR participation | None found |
| Regulatory filings | None with CDM references |

---

## Likelihood Assessment

**P(Evidence | ARCHITECT)**: 0.01
- If ABC were an ARCHITECT, we would expect FINOS membership, CDM commits, or ISDA DRR participation
- Complete absence strongly disconfirms ARCHITECT

**P(Evidence | PRAGMATIST)**: 0.05
- Some CDM-aware vendor relationship would be visible
- No such evidence found

**P(Evidence | OBSERVER)**: 0.10
- Would expect ISDA working group mentions
- None found at Tier 1

**P(Evidence | UNKNOWN)**: 0.95
- Null result is highly consistent with UNKNOWN
- Matches cohort pattern exactly

---

## Posterior Calculation

Using Bayes' theorem with normalization:

| Classification | Prior | Likelihood | Unnormalized | Posterior |
|---------------|-------|------------|--------------|-----------|
| ARCHITECT | 0.05 | 0.01 | 0.0005 | 0.8% |
| PRAGMATIST | 0.15 | 0.05 | 0.0075 | 12.3% |
| OBSERVER | 0.20 | 0.10 | 0.0200 | 32.8% |
| UNKNOWN | 0.60 | 0.95 | 0.5700 | **93.4%** |

**Normalization constant**: 0.6100

---

## Posterior Probability

| Classification | Posterior |
|---------------|-----------|
| ARCHITECT | 0.8% |
| PRAGMATIST | 12.3% |
| OBSERVER | 32.8% |
| **UNKNOWN** | **93.4%** |

---

## Update Summary

- **Prior (UNKNOWN)**: 60%
- **Posterior (UNKNOWN)**: 93.4%
- **Shift**: +33.4 percentage points
- **Bayes Factor**: 15.8 (strong evidence for UNKNOWN)

The null Tier 1 result strongly confirms the cohort pattern. ABC operates in the NAFMII framework like other Chinese Big Four banks.

---

*Bayesian update under CDM Research Protocol v2.3*
