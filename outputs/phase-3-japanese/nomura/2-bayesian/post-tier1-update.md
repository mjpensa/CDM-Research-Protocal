# Post-Tier 1 Bayesian Update: Nomura Holdings, Inc.

## Prior Probability
**P(ARCHITECT) = 0.20**
**P(PRAGMATIST) = 0.80**

**Rationale for Prior:**
- Nomura is a major Japanese securities firm with significant derivatives operations
- Japanese banks have historically adopted international derivatives standards more slowly than European/US peers
- Limited public evidence of Japanese banks pursuing CDM leadership (except through infrastructure like JSCC)
- Base rate for major Japanese investment banks: ~20% ARCHITECT probability

---

## Tier 1 Evidence Summary
**Evidence Items Found:** 0
**Null Results:** 2 (highly informative)

**Key Null Results:**
1. No official CDM announcements from Nomura
2. No FINOS/open source CDM contributions

---

## Likelihood Ratio Analysis

### Evidence: Absence of Official CDM Announcements (Informative Null)
**LR = 0.5** (absence of evidence weakly supports PRAGMATIST)

**Reasoning:**
If Nomura were pursuing ARCHITECT strategy, we would expect to see official communications about CDM adoption in annual reports, regulatory filings, or press releases. Major strategic technology initiatives are typically publicized. The complete absence of official CDM messaging suggests no strategic CDM program.

**Impact:**
- P(ARCHITECT | no announcements) = 0.5 × likelihood it would be silent if ARCHITECT
- P(PRAGMATIST | no announcements) = 1.0 × likelihood it would be silent if PRAGMATIST

---

### Evidence: No FINOS CDM Contributions (Informative Null)
**LR = 0.4** (absence of open source activity supports PRAGMATIST)

**Reasoning:**
Banks pursuing ARCHITECT strategies typically contribute to open source CDM development through FINOS. The absence of Nomura contributions to FINOS CDM projects is informative. It suggests Nomura is not investing in CDM standards development or building open source CDM expertise.

**Impact:**
Stronger evidence against ARCHITECT than the previous null result, as open source contribution is a distinguishing characteristic of ARCHITECT banks.

---

## Bayesian Update Calculation

**Starting Prior:**
- P(ARCHITECT) = 0.20
- P(PRAGMATIST) = 0.80

**Combined Likelihood Ratio for Tier 1 Null Results:**
LR_combined = 0.5 × 0.4 = 0.20

**Posterior Calculation:**
- P(ARCHITECT | Tier 1 evidence) = P(ARCHITECT) × LR / normalization
- Unnormalized: 0.20 × 0.20 = 0.04
- P(PRAGMATIST | Tier 1 evidence) = P(PRAGMATIST) × (1/LR)
- Unnormalized: 0.80 × (1/0.20) = 0.80 × 5 = 4.0

**Normalization:** 0.04 + 4.0 = 4.04

**Post-Tier 1 Posterior:**
- P(ARCHITECT) = 0.04 / 4.04 = **0.01 (1%)**
- P(PRAGMATIST) = 4.0 / 4.04 = **0.99 (99%)**

---

## Interpretation

The Tier 1 null results significantly reduce the probability that Nomura is pursuing an ARCHITECT strategy. The posterior probability of ARCHITECT drops from 20% to 1%, driven by the informative absence of official CDM communications and open source contributions.

However, the 99% PRAGMATIST classification is premature. The null results indicate "not ARCHITECT" but do not distinguish between:
1. PRAGMATIST (using CDM through vendors/infrastructure)
2. OBSERVER (minimal CDM engagement)
3. UNKNOWN (no CDM involvement at all)

Tier 2 evidence is needed to determine the specific classification within the non-ARCHITECT category.

---

## Proceeding to Tier 2

**Key Questions for Tier 2:**
1. Is there indirect evidence of CDM exposure through infrastructure (CCPs, utilities)?
2. Does trade press indicate vendor relationships or CDM implementation plans?
3. Are there ecosystem signals suggesting Nomura is preparing for CDM requirements?

**Expected Impact:**
Tier 2 evidence will likely refine the classification from "not ARCHITECT" to a specific PRAGMATIST or OBSERVER sub-category. The JSCC clearing relationship will be key evidence in this determination.
