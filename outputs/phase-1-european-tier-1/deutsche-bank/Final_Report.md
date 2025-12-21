# CDM/DRR Research Report: Deutsche Bank AG

**Classification:** PRAGMATIST (Regulatory-Driven)
**Confidence:** 55%
**Date:** 2025-12-21
**Phase:** 1 - European Tier 1

---

## Executive Summary

Deutsche Bank AG is classified as a **PRAGMATIST (Regulatory-Driven)** with 55% confidence. Despite having demonstrated open-source capability through active FINOS contributions (Fluxnova, Spring Bot, Waltz), Deutsche Bank is NOT contributing to the Common Domain Model (CDM). Evidence suggests a traditional regulatory compliance approach using DTCC for EMIR reporting rather than CDM-based digital regulatory reporting.

**Key Finding:** The framework v20 claim of "Pilot; production expected 2025" **cannot be verified** and appears to be inaccurate.

---

## Classification Summary

| Metric | Value |
|--------|-------|
| Classification | PRAGMATIST |
| Sub-Classification | Regulatory-Driven |
| P(ARCHITECT) | 17% |
| P(PRAGMATIST) | 83% |
| Confidence | 55% |

---

## Evidence Summary

### Tier 1 Evidence (3 items)

| ID | Finding | Direction |
|----|---------|-----------|
| DB-002 | FINOS contributor to Fluxnova, Waltz, Spring Bot - NOT CDM | NEUTRAL |
| DB-003 | EMIR reporting via DTCC traditional approach | PRAGMATIST |
| DB-005 | Annual reports 2023-2024 no CDM mentions | NEUTRAL |

### Tier 2 Evidence (2 items)

| ID | Finding | Direction |
|----|---------|-----------|
| DB-001 | JWG RegTech Conference DRR panel Nov 2022 | ARCHITECT |
| DB-004 | Risk.net: patchy CDM adoption industry-wide | NEUTRAL |

### Tier 3 Evidence

No Tier 3 evidence found. All searches returned null results.

---

## The FINOS Paradox

Deutsche Bank's FINOS contribution pattern reveals a **deliberate strategic choice**:

| FINOS Project | Deutsche Bank Role | CDM Relevance |
|---------------|-------------------|---------------|
| Fluxnova | Co-maintainer | None |
| Spring Bot | Original contributor | None |
| Waltz | Lead maintainer | None |
| **CDM** | **Not contributing** | **Direct** |

**Interpretation:** Deutsche Bank has the capability and willingness to contribute to FINOS open-source projects. Their absence from CDM is a revealed preference, not a capability limitation.

---

## Probability Trajectory

```
Prior:       25%
Post-Tier1:  14%
Post-Tier2:  20%
Post-Tier3:  17%
```

---

## Framework Claim Validation

| Claim | Source | Status |
|-------|--------|--------|
| "Pilot; production expected 2025" | Framework v20 | **UNVERIFIED** |

**Recommendation:** Remove claim from framework - no supporting evidence found.

---

## Recommendations

### For Framework Updates

1. **Remove** "Pilot; production expected 2025" claim
2. **Reclassify** to PRAGMATIST (Regulatory-Driven)
3. **Flag** for re-assessment in Q2 2025

### For Discovery Calls

- **Target:** Head of Derivatives Technology
- **Key Question:** Is Deutsche Bank actively evaluating or implementing CDM?

---

## Source URLs

1. [FINOS CDM Resources](https://www.finos.org/common-domain-model)
2. [JWG DRR Regcast](https://jwg-it.eu/regcasts/digitizing-derivative-reporting-with-drr/)
3. [Deutsche Bank EMIR Reporting](https://www.db.com/legal-resources/european-market-infrastructure-regulation/transaction-reporting)
4. [Deutsche Bank Annual Report 2023](https://investor-relations.db.com/files/documents/annual-reports/2024/Annual-Report-2023.pdf)
5. [Risk.net CDM Coverage](https://www.risk.net/risk-management/6512226/patchy-response-to-isdas-back-office-of-the-future)

---

*Report generated: 2025-12-21*
*Classification: PRAGMATIST (Regulatory-Driven) at 55% confidence*
