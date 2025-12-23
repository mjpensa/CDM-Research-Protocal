# Framework Integration: Pictet

**Bank**: Pictet Group
**Phase**: 6 (Deep Dives)
**Date**: 2025-12-21

---

## Classification Summary

| Field | Value |
|-------|-------|
| Bank ID | pictet |
| Classification | ARCHITECT |
| Subtype | Native |
| Confidence | 90% |
| Maturity Score | 5 |
| Evidence Count | 4 |

---

## Framework Mapping

```
ARCHITECT ──────────────────────────────────────────────────────────┐
  │                                                                  │
  ├── Native (Production)      : BNP Paribas, JPMorgan, [PICTET]     │ ◄── HERE
  ├── Active (Pilot + Build)   : Deutsche Bank (expected)            │
  └── Follower (Contribution)  : Barclays, Standard Chartered        │
```

---

## Integration Data

```json
{
  "bank_id": "pictet",
  "classification": "ARCHITECT",
  "subtype": "Native",
  "confidence": 0.90,
  "maturity_score": 5,
  "region": "Europe",
  "subregion": "Switzerland",
  "derivatives_relevance": "Low",
  "key_evidence": "CDM/DRR production usage confirmed alongside BNP/JPMorgan",
  "evidence_freshness": "current",
  "flags": []
}
```

---

## Export Data

```csv
bank_id,bank_name,phase,classification,subtype,confidence,maturity,region,evidence_count
pictet,Pictet Group,6,ARCHITECT,Native,90,5,Europe,4
```

---

*Framework integration completed under CDM Research Protocol v2.3*
