# Framework Integration: ICBC

**Bank**: Industrial and Commercial Bank of China
**Phase**: 7 (Emerging Markets)
**Date**: 2025-12-21

---

## Classification Summary

| Field | Value |
|-------|-------|
| Bank ID | icbc |
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
  ├── NAFMII Framework     : [ICBC], (other Chinese banks expected)      │ ◄── HERE
  ├── No Evidence          : (various)                                   │
  └── Research Incomplete  : (not applicable here)                       │
```

---

## Integration Data

```json
{
  "bank_id": "icbc",
  "classification": "UNKNOWN",
  "subtype": "NAFMII Framework",
  "confidence": 0.40,
  "maturity_score": 0,
  "region": "Asia",
  "subregion": "China",
  "derivatives_relevance": "Medium",
  "key_finding": "Operates in NAFMII framework, structurally separate from ISDA CDM ecosystem",
  "evidence_freshness": "current",
  "flags": ["nafmii_framework", "non_isda_jurisdiction"],
  "future_triggers": ["hkma_drr_2025", "us_operations_expansion"]
}
```

---

## Export Data

```csv
bank_id,bank_name,phase,classification,subtype,confidence,maturity,region,evidence_count
icbc,Industrial and Commercial Bank of China,7,UNKNOWN,NAFMII Framework,40,0,Asia,2
```

---

## Phase 7 Status

| Bank | Classification | Confidence | Status |
|------|---------------|------------|--------|
| DBS | OBSERVER | 55% | Complete |
| ICBC | UNKNOWN | 40% | Complete |
| Bank of China | Pending | - | Next |
| CCB | Pending | - | Queued |
| ABC | Pending | - | Queued |

---

## Chinese Bank Cohort Pattern

Based on ICBC findings, expect other Chinese banks (Bank of China, CCB, ABC) to show similar pattern:
- NAFMII framework mandate
- Strong derivatives capability in domestic market
- Minimal/no ISDA CDM involvement
- UNKNOWN classification likely

This creates a coherent **Chinese bank cohort** with structural framework separation from CDM ecosystem.

---

*Framework integration completed under CDM Research Protocol v2.3*
