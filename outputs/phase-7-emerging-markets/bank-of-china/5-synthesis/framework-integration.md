# Framework Integration: Bank of China

**Bank**: Bank of China Limited
**Phase**: 7 (Emerging Markets)
**Date**: 2025-12-21

---

## Classification Summary

| Field | Value |
|-------|-------|
| Bank ID | bank-of-china |
| Classification | UNKNOWN |
| Subtype | NAFMII Framework |
| Confidence | 40% |
| Maturity Score | 0 |
| Evidence Count | 2 |

---

## Framework Mapping

```
UNKNOWN ────────────────────────────────────────────────────────────────┐
  │                                                                      │
  ├── NAFMII Framework     : ICBC, [BOC], (CCB, ABC expected)            │ ◄── HERE
  ├── No Evidence          : (various)                                   │
  └── Research Incomplete  : (not applicable)                            │
```

---

## Integration Data

```json
{
  "bank_id": "bank-of-china",
  "classification": "UNKNOWN",
  "subtype": "NAFMII Framework",
  "confidence": 0.40,
  "maturity_score": 0,
  "region": "Asia",
  "subregion": "China",
  "derivatives_relevance": "Medium",
  "key_finding": "Cohort with ICBC - operates in NAFMII framework, separate from ISDA CDM",
  "evidence_freshness": "current",
  "flags": ["nafmii_framework", "chinese_big_four_cohort"],
  "future_triggers": ["hkma_drr_2025"]
}
```

---

## Export Data

```csv
bank_id,bank_name,phase,classification,subtype,confidence,maturity,region,evidence_count
bank-of-china,Bank of China Limited,7,UNKNOWN,NAFMII Framework,40,0,Asia,2
```

---

## Chinese Big Four Cohort

| Bank | Classification | Status |
|------|---------------|--------|
| ICBC | UNKNOWN | Complete |
| Bank of China | UNKNOWN | Complete |
| CCB | Expected UNKNOWN | Next |
| ABC | Expected UNKNOWN | Queued |

---

*Framework integration completed under CDM Research Protocol v2.3*
