# Bayesian Update: Post-Tier 3

**Bank**: Banco Santander S.A.
**Phase**: 5 (Spanish)
**Date**: 2025-12-21

---

## Prior (Post-Tier 2)

| Classification | Prior |
|---------------|-------|
| ARCHITECT | 2% |
| PRAGMATIST | 67% |
| OBSERVER | 26% |
| UNKNOWN | 5% |

---

## Tier 3 Evidence Summary

| Search Target | Result | Direction |
|--------------|--------|-----------|
| CDM job postings | None found | Negative (no active build) |
| LinkedIn CDM activity | None found | Neutral (may be policy) |
| Employee blogs/newsletters | None found | Neutral |
| GitHub personal accounts | None found | Negative |

---

## Tier 3 Null Analysis

**Complete absence of Tier 3 signals** across all categories:

1. **No CDM job postings**: Santander is not actively hiring for CDM capability. This suggests no sustained investment post-DRR pilot.

2. **No LinkedIn advocacy**: No visible CDM thought leadership from Santander employees. Could be corporate policy, but notable absence.

3. **No personal GitHub CDM work**: No Santander employees contributing to CDM in personal capacity.

---

## Likelihood Ratios

### ARCHITECT Hypothesis
- P(No CDM jobs | ARCHITECT) = 0.2 (ARCHITECTs typically hiring)
- P(No LinkedIn | ARCHITECT) = 0.4 (Some are quiet)
- **Combined**: 0.08

### PRAGMATIST Hypothesis
- P(No CDM jobs | PRAGMATIST) = 0.7 (Not building internally)
- P(No LinkedIn | PRAGMATIST) = 0.7 (Expected)
- **Combined**: 0.49

### OBSERVER Hypothesis
- P(No CDM jobs | OBSERVER) = 0.95 (Expected)
- P(No LinkedIn | OBSERVER) = 0.9 (Expected)
- **Combined**: 0.855

---

## Posterior Calculation

| Classification | Prior | Likelihood | Unnormalized | Posterior |
|---------------|-------|------------|--------------|-----------|
| ARCHITECT | 0.02 | 0.08 | 0.0016 | 1% |
| PRAGMATIST | 0.67 | 0.49 | 0.328 | 62% |
| OBSERVER | 0.26 | 0.855 | 0.222 | 32% |
| UNKNOWN | 0.05 | 0.5 | 0.025 | 5% |

**Total**: 0.5766
**Normalization Factor**: 1.73

---

## Final Posterior

| Classification | Posterior |
|---------------|-----------|
| ARCHITECT | 1% |
| **PRAGMATIST** | **62%** |
| OBSERVER | 32% |
| UNKNOWN | 5% |

---

## Classification Decision

### Primary Classification: **PRAGMATIST**
### Subtype: **Ecosystem**
### Confidence: **55%**
### Maturity Score: **2**

---

## Rationale

1. **UK DRR pilot participation (2022)** establishes CDM ecosystem engagement, differentiating from OBSERVER.

2. **Dated evidence with no follow-through** prevents higher confidence. The 35-month-old evidence with no recent signals suggests engagement has not been sustained.

3. **CFTC enforcement action** suggests reporting infrastructure challenges that CDM could address, but no evidence Santander is pursuing CDM solution.

4. **Absence of FINOS contribution, job postings, and recent CDM signals** rules out ARCHITECT classification.

5. **Ecosystem subtype** is appropriate - participated in regulatory pilot but no internal build or vendor relationship identified.

---

## Confidence Breakdown

| Factor | Impact |
|--------|--------|
| Tier 2 maximum (75%) | Cap |
| Freshness penalty (0.5) | -20% |
| Single source concern | -5% |
| CFTC enforcement | -5% |
| Tier 3 absence | -5% |
| **Final Confidence** | **55%** |

---

## Peer Comparison (DRR Pilot Cohort)

| Bank | Classification | Confidence |
|------|---------------|------------|
| Barclays | ARCHITECT (Follower) | 85% |
| HSBC | PRAGMATIST (Vendor) | 70% |
| NatWest | PRAGMATIST (Ecosystem) | 60% |
| Lloyds | PRAGMATIST (Ecosystem) | 58% |
| Credit Suisse | N/A (absorbed by UBS) | - |
| **Santander** | **PRAGMATIST (Ecosystem)** | **55%** |

Santander's classification aligns with the middle of the DRR pilot cohort - engaged but not leading.
