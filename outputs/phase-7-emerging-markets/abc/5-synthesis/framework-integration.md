# Framework Integration: ABC

**Bank**: Agricultural Bank of China Limited
**Phase**: 7 (Emerging Markets)
**Date**: 2025-12-21

---

## Integration Summary

| Field | Value |
|-------|-------|
| **Bank ID** | abc |
| **Classification** | UNKNOWN |
| **Subtype** | NAFMII Framework |
| **Confidence** | 40% |
| **Maturity Score** | 0 |

---

## Framework Placement

```
┌─────────────────────────────────────────────────────────────────┐
│                    CDM ADOPTION FRAMEWORK                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ARCHITECT (Native)     │  Production CDM usage                 │
│  Maturity: 5           │                                        │
│                        │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  ARCHITECT (Active)    │  Pilot/POC stage                       │
│  Maturity: 3           │                                        │
│                        │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  PRAGMATIST            │  Vendor-enabled or ecosystem           │
│  Maturity: 2           │                                        │
│                        │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  OBSERVER              │  Membership/participation              │
│  Maturity: 1           │                                        │
│                        │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  UNKNOWN               │  No verified evidence                  │
│  Maturity: 0           │  ◄─── ABC (NAFMII Framework)          │
│                        │                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Cohort Position

### Chinese Big Four Banks

| Bank | Classification | Subtype | Confidence | Maturity |
|------|---------------|---------|------------|----------|
| ICBC | UNKNOWN | NAFMII Framework | 40% | 0 |
| Bank of China | UNKNOWN | NAFMII Framework | 40% | 0 |
| CCB | UNKNOWN | NAFMII Framework | 40% | 0 |
| **ABC** | **UNKNOWN** | **NAFMII Framework** | **40%** | **0** |

### Cohort Insight

All Chinese Big Four banks share structural characteristics that place them outside the ISDA CDM ecosystem:

1. **Regulatory Framework**: NAFMII (not ISDA) for domestic derivatives
2. **Jurisdictional Scope**: ISDA CDM/DRR does not cover Chinese mainland reporting
3. **Future Pathway**: Hong Kong subsidiaries could trigger adoption via ISDA DRR

---

## Phase 7 Summary

| Bank | Classification | Confidence | Maturity | Status |
|------|---------------|------------|----------|--------|
| DBS | OBSERVER | 55% | 1 | Complete |
| ICBC | UNKNOWN | 40% | 0 | Complete |
| Bank of China | UNKNOWN | 40% | 0 | Complete |
| CCB | UNKNOWN | 40% | 0 | Complete |
| ABC | UNKNOWN | 40% | 0 | Complete |

### Phase 7 Insights

1. **DBS**: Singapore's largest bank, OBSERVER via ISDA Board representation
2. **Chinese Big Four**: All UNKNOWN due to NAFMII framework - structural finding

---

## Evidence Quality

| Metric | Value |
|--------|-------|
| Tier 1 items | 0 |
| Tier 2 items | 2 |
| Tier 3 items | 0 (not searched) |
| Source diversity | 2 unique sources |
| Freshness | Current |
| Contradiction flags | 0 |

---

## Comparison: ABC vs Phase 7 Banks

| Factor | DBS | Chinese Big Four |
|--------|-----|-----------------|
| Jurisdiction | Singapore (MAS) | China (PBoC, CBIRC) |
| Derivatives framework | ISDA compatible | NAFMII mandated |
| CDM relevance | Yes (MAS in DRR scope) | No (China not in scope) |
| ISDA involvement | Board member | Membership only (ABC) |
| Classification | OBSERVER | UNKNOWN |

---

## Integration Notes

### 1. ISDA Membership Anomaly

ABC's explicit ISDA primary membership claim is flagged but does not change classification:
- Membership is necessary but not sufficient for CDM involvement
- No CDM-specific evidence despite membership claim
- Cohort consistency maintained

### 2. Future Monitoring

ABC should be re-assessed when:
- ISDA DRR Hong Kong launches (2025)
- NAFMII-ISDA harmonization announced
- ABC expands international derivatives operations

### 3. Research Efficiency

ABC research leveraged cohort pattern from ICBC/BOC/CCB:
- Tier 3 search skipped (structurally irrelevant)
- Classification validated through independent evidence
- Efficient use of research resources

---

## JSON Extract

```json
{
  "bank_id": "abc",
  "bank_name": "Agricultural Bank of China Limited",
  "classification": "UNKNOWN",
  "subtype": "NAFMII Framework",
  "confidence": 0.40,
  "maturity_score": 0,
  "phase": 7,
  "cohort": "chinese_big_four",
  "flags": [
    "nafmii_framework",
    "chinese_big_four_cohort",
    "isda_member"
  ],
  "future_triggers": [
    "isda_drr_hong_kong_2025",
    "nafmii_isda_harmonization"
  ]
}
```

---

*Framework integration under CDM Research Protocol v2.3*
