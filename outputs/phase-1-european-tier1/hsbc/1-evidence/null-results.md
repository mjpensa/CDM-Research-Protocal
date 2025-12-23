# HSBC - Null Results Registry

## Purpose
Document searches that yielded no evidence, as null results can be informative for Bayesian updating.

## Null Results

### 1. FINOS Membership
| Field | Value |
|-------|-------|
| **Category** | Membership |
| **Queries** | site:finos.org HSBC member |
| **Expected if ARCHITECT** | HSBC listed as FINOS member |
| **Actual Result** | HSBC NOT listed at any tier |
| **Null Type** | CONTRADICTORY |
| **Informative Absence** | YES |
| **LR Impact** | 0.6 |

**Implication**: Despite ISDA Board Chair being from HSBC, the bank has not joined FINOS. This suggests CDM/DRR engagement is governance-focused rather than technical.

---

### 2. CDM Contribution
| Field | Value |
|-------|-------|
| **Category** | Open Source |
| **Queries** | HSBC CDM Common Domain Model contribution |
| **Expected if ARCHITECT** | Evidence of CDM contributions or commits |
| **Actual Result** | No contribution evidence found |
| **Null Type** | IRRELEVANT |
| **Informative Absence** | YES |
| **LR Impact** | 0.8 |

**Implication**: ISDA governance role does not translate to CDM technical contributions.

---

### 3. DRR Production 2024
| Field | Value |
|-------|-------|
| **Category** | Production |
| **Queries** | HSBC DRR Digital Regulatory Reporting implementation 2024 |
| **Expected if ARCHITECT** | Announcement of DRR production usage |
| **Actual Result** | Only historical pilot (2018-2019) found |
| **Null Type** | IRRELEVANT |
| **Informative Absence** | YES |
| **LR Impact** | 0.8 |

**Implication**: 5+ years since DRR pilot with no production announcement suggests limited follow-through.

---

### 4. CDM Job Postings
| Field | Value |
|-------|-------|
| **Category** | Hiring Signals |
| **Queries** | HSBC CDM Common Domain Model jobs |
| **Expected if ARCHITECT** | CDM-specific roles |
| **Actual Result** | Standard regulatory reporting jobs only |
| **Null Type** | IRRELEVANT |
| **Informative Absence** | NO |
| **LR Impact** | 1.0 (neutral) |

---

## Summary Impact

| Finding | LR | Confidence Impact |
|---------|----|--------------------|
| No FINOS membership | 0.6 | Significant negative |
| No CDM contribution | 0.8 | Moderate negative |
| No DRR production | 0.8 | Moderate negative |
| No CDM hiring | 1.0 | Neutral |
| **Combined Null LR** | **0.38** | Reduces ARCHITECT probability |

---
*Null Results Registry Complete*
*Generated: 2025-12-21*
