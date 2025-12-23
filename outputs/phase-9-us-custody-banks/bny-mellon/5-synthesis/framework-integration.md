# Framework Integration: BNY Mellon

**Bank**: Bank of New York Mellon
**Phase**: 9 (US Custody Banks)
**Date**: 2025-12-21

---

## Integration Summary

| Field | Value |
|-------|-------|
| **Bank ID** | bny-mellon |
| **Classification** | OBSERVER |
| **Subtype** | FINOS Platinum Member |
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
│  OBSERVER              │  Citigroup, Bank of America, BNY Mellon│
│  Maturity: 1           │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  UNKNOWN               │  State Street                          │
│  Maturity: 0           │                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## JSON Extract

```json
{
  "bank_id": "bny-mellon",
  "bank_name": "Bank of New York Mellon",
  "classification": "OBSERVER",
  "subtype": "FINOS Platinum Member",
  "confidence": 0.55,
  "maturity_score": 1,
  "phase": 9,
  "cohort": "us_custody_banks",
  "flags": [
    "finos_platinum_member",
    "custody_bank_business_model",
    "cftc_reporting_enforcement"
  ]
}
```

---

## Phase 9 Complete

All US custody banks processed:
- State Street: UNKNOWN - No CDM relevance to custody business
- BNY Mellon: OBSERVER - FINOS Platinum Member, no CDM work

---

## All Phases Complete

| Phase | Banks | Classifications |
|-------|-------|-----------------|
| 1-4 | 12 European banks | Various |
| 5 | 2 Spanish banks | Various |
| 6 | 2 Deep dives | Various |
| 7 | 5 Emerging markets | Various |
| 8 | 5 US Investment Banks | 1 ARCHITECT, 2 PRAGMATIST, 2 OBSERVER |
| 9 | 2 US Custody Banks | 1 OBSERVER, 1 UNKNOWN |

---

*Framework integration under CDM Research Protocol v2.3*
