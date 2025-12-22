# Framework Integration: CCB

**Bank**: China Construction Bank Corporation
**Phase**: 7 (Emerging Markets)
**Date**: 2025-12-21

---

## Classification Summary

| Field | Value |
|-------|-------|
| Bank ID | ccb |
| Classification | UNKNOWN |
| Subtype | NAFMII Framework |
| Confidence | 40% |
| Maturity Score | 0 |
| Evidence Count | 1 |

---

## Framework Mapping

```
UNKNOWN ────────────────────────────────────────────────────────────────┐
  │                                                                      │
  ├── NAFMII Framework     : ICBC, BOC, [CCB], (ABC expected)            │ ◄── HERE
  └── Other                : (various)                                   │
```

---

## Integration Data

```json
{
  "bank_id": "ccb",
  "classification": "UNKNOWN",
  "subtype": "NAFMII Framework",
  "confidence": 0.40,
  "maturity_score": 0,
  "region": "Asia",
  "subregion": "China",
  "key_finding": "Chinese Big Four cohort - NAFMII framework",
  "flags": ["nafmii_framework", "chinese_big_four_cohort"]
}
```

---

## Export Data

```csv
bank_id,bank_name,phase,classification,subtype,confidence,maturity,region,evidence_count
ccb,China Construction Bank Corporation,7,UNKNOWN,NAFMII Framework,40,0,Asia,1
```

---

*Framework integration completed under CDM Research Protocol v2.3*
