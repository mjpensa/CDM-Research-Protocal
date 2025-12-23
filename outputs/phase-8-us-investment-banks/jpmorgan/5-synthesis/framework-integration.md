# Framework Integration: JPMorgan

**Bank**: JPMorgan Chase & Co.
**Phase**: 8 (US Investment Banks)
**Date**: 2025-12-21

---

## Integration Summary

| Field | Value |
|-------|-------|
| **Bank ID** | jpmorgan |
| **Classification** | ARCHITECT |
| **Subtype** | Native |
| **Confidence** | 95% |
| **Maturity Score** | 5 |

---

## Framework Placement

```
┌─────────────────────────────────────────────────────────────────┐
│                    CDM ADOPTION FRAMEWORK                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ARCHITECT (Native)     │  Production CDM usage                 │
│  Maturity: 5           │  ◄─── JPMorgan (First US Bank)        │
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
│  Maturity: 0           │                                        │
│                        │                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## ARCHITECT (Native) Cohort

JPMorgan joins the ARCHITECT (Native) cohort:

| Bank | Region | Key Evidence |
|------|--------|--------------|
| Deutsche Bank | Europe | Early ISDA CDM leader |
| BNP Paribas | Europe | FINOS sponsor |
| Pictet | Europe | Private banking pioneer |
| **JPMorgan** | **US** | **First US bank, FINOS maintainer** |

### Cohort Characteristics

All ARCHITECT (Native) banks share:
1. **Production CDM usage** confirmed by official sources
2. **FINOS/ISDA involvement** at contributor or maintainer level
3. **Multi-jurisdictional** regulatory reporting scope
4. **Industry leadership** through advocacy and contribution

---

## US Investment Bank Benchmark

JPMorgan establishes the benchmark for Phase 8:

| Factor | JPMorgan Standard |
|--------|-------------------|
| Production usage | CDM/DRR as "primary mechanism" |
| Governance | FINOS maintainer appointment |
| Scope | Multi-jurisdiction (ASIC, MAS, EMIR, CFTC) |
| Recognition | FINOS 'Adoption Achiever' award |
| Advocacy | ISDA webinars, CDM Showcase |

### Implications for Peer Banks

| Bank | Expected Comparison |
|------|---------------------|
| Goldman Sachs | G-SIB project participant - may approach JPMorgan level |
| Morgan Stanley | Unclear - research needed |
| Citigroup | G-SIB project participant - may approach JPMorgan level |
| Bank of America | G-SIB project participant - may approach JPMorgan level |

---

## Evidence Quality Comparison

| Metric | JPMorgan | Typical ARCHITECT |
|--------|----------|-------------------|
| Tier 1 items | 5 | 2-3 |
| Tier 2 items | 2 | 1-2 |
| Source types | 4 | 2-3 |
| Contradictions | 0 | 0-1 |
| Confidence | 95% | 80-90% |

JPMorgan has the strongest evidence profile of any bank in this research.

---

## Research Protocol Impact

### Benchmark Establishment

JPMorgan's classification establishes:
1. **ARCHITECT (Native) definition** - production CDM with governance contribution
2. **US bank capability proof** - demonstrates US banks can achieve highest classification
3. **Evidence standard** - sets bar for what constitutes definitive evidence

### Cohort Analysis Implications

For remaining Phase 8 banks:
- G-SIB project participation suggests Goldman, Citi, BofA may be ARCHITECT candidates
- JPMorgan's first-mover claim implies others are not yet "primary mechanism" users
- Peer comparison will reference JPMorgan benchmark

---

## JSON Extract

```json
{
  "bank_id": "jpmorgan",
  "bank_name": "JPMorgan Chase & Co.",
  "classification": "ARCHITECT",
  "subtype": "Native",
  "confidence": 0.95,
  "maturity_score": 5,
  "phase": 8,
  "cohort": "us_investment_banks",
  "flags": [
    "production_cdm_usage",
    "first_us_bank_drr_primary",
    "finos_cdm_maintainer",
    "finos_adoption_achiever_award",
    "multi_jurisdiction_drr"
  ],
  "benchmark_status": true,
  "key_person": "Nick Moger (Executive Director, first sell-side CDM maintainer)"
}
```

---

## Cross-Reference

### Related Analyses

| Bank | Relationship |
|------|--------------|
| Goldman Sachs | G-SIB project co-participant |
| Citigroup | G-SIB project co-participant |
| Bank of America | G-SIB project co-participant |
| Deutsche Bank | G-SIB project co-participant |
| BNP Paribas | ARCHITECT cohort peer |

### Vendor Ecosystem

| Vendor | Relationship |
|--------|--------------|
| REGnosys | CDM tooling provider |
| TradeHeader | DRR implementation partner |

---

*Framework integration under CDM Research Protocol v2.3*
