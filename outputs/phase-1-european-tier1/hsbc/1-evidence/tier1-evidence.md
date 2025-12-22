# HSBC - Tier 1 Evidence

## Summary

| Metric | Value |
|--------|-------|
| **Sources Found** | 3 |
| **Direction** | Mixed (governance strong, CDM-specific absent) |
| **Key Finding** | ISDA governance leadership without FINOS membership |

## Evidence Items

### HSBC-001: FCA/BOE DRR Pilot Participation
| Field | Value |
|-------|-------|
| **Claim** | HSBC participated in FCA/BOE Digital Regulatory Reporting pilot phases 1 and 2 (2018-2019) |
| **Source** | [FCA DRR Page](https://www.fca.org.uk/innovation/regtech/digital-regulatory-reporting) |
| **Date** | 2018-2019 |
| **Direction** | SUPPORTS_ARCHITECT |
| **LR** | 3.0 |

**Excerpt**:
> "Two phases of the DRR pilot have been completed, involving collaboration between the FCA, BOE and seven banks: Barclays, Credit Suisse, HSBC, Lloyds, Nationwide, Natwest and Santander."

**Analysis**: HSBC was one of 7 UK banks participating in the original DRR regulatory pilot. This demonstrates early engagement with Digital Regulatory Reporting concepts. However, this is historical (2018-2019) and does not confirm current CDM/DRR production usage.

---

### HSBC-002: ISDA Board Chair
| Field | Value |
|-------|-------|
| **Claim** | Jeroen Krens (HSBC) elected ISDA Board Chair effective January 2025 |
| **Source** | [ISDA Press Release](https://www.isda.org/2024/12/16/isda-board-appoints-new-chair-as-eric-litvack-steps-down-after-10-years/) |
| **Date** | December 2024 |
| **Direction** | SUPPORTS_ARCHITECT |
| **LR** | 4.0 |

**Excerpt**:
> "ISDA announced its Board of Directors elected Jeroen Krens as its new Chair. Krens is Managing Director, COO, Markets & Securities Services at HSBC Bank Plc and has been on the ISDA Board since 2016."

**Analysis**: This is significant - HSBC now holds the top ISDA governance position. However, ISDA Board Chair is a governance/policy role, not necessarily CDM technical engagement. It indicates industry leadership but not CDM adoption.

---

### HSBC-003: NOT a FINOS Member
| Field | Value |
|-------|-------|
| **Claim** | HSBC is NOT listed as a FINOS member at any tier |
| **Source** | [FINOS Members](https://www.finos.org/members) |
| **Date** | December 2024 (verified) |
| **Direction** | CONTRADICTS_ARCHITECT |
| **LR** | 0.6 |

**Excerpt**:
> "FINOS members page lists Platinum (Citi, Goldman Sachs, JP Morgan, UBS), Gold (Deutsche Bank, Lloyds, NatWest), Silver members. HSBC is absent from all tiers."

**Analysis**: Despite having the ISDA Board Chair, HSBC has not joined FINOS. This is a notable pattern - governance leadership in ISDA but no technical engagement in FINOS open source ecosystem.

---

## Tier 1 Aggregate Analysis

| Metric | Value |
|--------|-------|
| **Combined LR** | 3.0 × 4.0 × 0.6 = 7.2 |
| **Posterior P(Architect)** | ~55% (before temporal weighting) |
| **Pattern** | ISDA Governance + Historical DRR Pilot |

**Key Pattern**: HSBC exhibits "Governance Leadership" pattern - high ISDA engagement without FINOS technical participation.

---
*Tier 1 Evidence Complete*
*Generated: 2025-12-21*
