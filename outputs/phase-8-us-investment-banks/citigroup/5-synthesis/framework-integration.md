# Framework Integration: Citigroup

**Bank**: Citigroup Inc.
**Phase**: 8 (US Investment Banks)
**Date**: 2025-12-21

---

## Integration Summary

| Field | Value |
|-------|-------|
| **Bank ID** | citigroup |
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
│  OBSERVER              │  ◄─── Citigroup (G-SIB Participant)    │
│  Maturity: 1           │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  UNKNOWN               │                                        │
│  Maturity: 0           │                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## JSON Extract

```json
{
  "bank_id": "citigroup",
  "bank_name": "Citigroup Inc.",
  "classification": "OBSERVER",
  "subtype": "G-SIB Participant",
  "confidence": 0.55,
  "maturity_score": 1,
  "phase": 8,
  "cohort": "us_investment_banks",
  "flags": [
    "g_sib_drr_project",
    "finos_member",
    "no_production_claims",
    "no_major_contribution"
  ]
}
```

---

*Framework integration under CDM Research Protocol v2.3*
