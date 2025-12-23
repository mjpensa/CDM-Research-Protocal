# Framework Integration: Morgan Stanley

**Bank**: Morgan Stanley
**Phase**: 8 (US Investment Banks)
**Date**: 2025-12-21

---

## Integration Summary

| Field | Value |
|-------|-------|
| **Bank ID** | morgan-stanley |
| **Classification** | PRAGMATIST |
| **Subtype** | Ecosystem |
| **Confidence** | 65% |
| **Maturity Score** | 2 |

---

## Framework Placement

```
┌─────────────────────────────────────────────────────────────────┐
│                    CDM ADOPTION FRAMEWORK                       │
├─────────────────────────────────────────────────────────────────┤
│  ARCHITECT (Native)     │  JPMorgan                             │
│  Maturity: 5           │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  PRAGMATIST            │  Goldman Sachs (Legend)                │
│  Maturity: 2           │  ◄─── Morgan Stanley (Morphir)         │
├────────────────────────┼────────────────────────────────────────┤
│  OBSERVER              │                                        │
│  Maturity: 1           │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  UNKNOWN               │                                        │
│  Maturity: 0           │                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## US Investment Bank Pattern

| Bank | Classification | Contribution Type |
|------|---------------|-------------------|
| JPMorgan | ARCHITECT (Native) | Production deployment |
| Goldman Sachs | PRAGMATIST (Ecosystem) | Platform (Legend) |
| Morgan Stanley | PRAGMATIST (Ecosystem) | Framework (Morphir) |

**Pattern**: US investment banks show strong FINOS contribution but only JPMorgan has confirmed production CDM/DRR usage.

---

## JSON Extract

```json
{
  "bank_id": "morgan-stanley",
  "bank_name": "Morgan Stanley",
  "classification": "PRAGMATIST",
  "subtype": "Ecosystem",
  "confidence": 0.65,
  "maturity_score": 2,
  "phase": 8,
  "cohort": "us_investment_banks",
  "flags": [
    "morphir_contributor",
    "legend_pilot_participant",
    "finos_platinum_member",
    "regtech_collaboration"
  ],
  "key_contribution": "Morphir business logic framework"
}
```

---

*Framework integration under CDM Research Protocol v2.3*
