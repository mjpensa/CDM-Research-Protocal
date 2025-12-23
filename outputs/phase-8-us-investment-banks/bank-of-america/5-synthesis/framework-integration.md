# Framework Integration: Bank of America

**Bank**: Bank of America Corporation
**Phase**: 8 (US Investment Banks)
**Date**: 2025-12-21

---

## Integration Summary

| Field | Value |
|-------|-------|
| **Bank ID** | bank-of-america |
| **Classification** | OBSERVER |
| **Subtype** | G-SIB Participant |
| **Confidence** | 55% |
| **Maturity Score** | 1 |

---

## Framework Placement

```
┌─────────────────────────────────────────────────────────────────┐
│  ARCHITECT (Native)     │  JPMorgan                             │
│  Maturity: 5           │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  PRAGMATIST            │  Goldman Sachs, Morgan Stanley         │
│  Maturity: 2           │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  OBSERVER              │  Citigroup, Bank of America            │
│  Maturity: 1           │                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## JSON Extract

```json
{
  "bank_id": "bank-of-america",
  "bank_name": "Bank of America Corporation",
  "classification": "OBSERVER",
  "subtype": "G-SIB Participant",
  "confidence": 0.55,
  "maturity_score": 1,
  "phase": 8,
  "cohort": "us_investment_banks",
  "flags": [
    "g_sib_drr_project",
    "fourth_largest_otc_dealer"
  ]
}
```

---

## Phase 8 Complete

All five US investment banks processed:
- JPMorgan: ARCHITECT (Native) - Production CDM/DRR
- Goldman Sachs: PRAGMATIST (Ecosystem) - Legend contributor
- Morgan Stanley: PRAGMATIST (Ecosystem) - Morphir contributor
- Citigroup: OBSERVER - G-SIB participant
- Bank of America: OBSERVER - G-SIB participant

---

*Framework integration under CDM Research Protocol v2.3*
