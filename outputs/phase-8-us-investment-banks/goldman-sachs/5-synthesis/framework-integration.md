# Framework Integration: Goldman Sachs

**Bank**: Goldman Sachs Group, Inc.
**Phase**: 8 (US Investment Banks)
**Date**: 2025-12-21

---

## Integration Summary

| Field | Value |
|-------|-------|
| **Bank ID** | goldman-sachs |
| **Classification** | PRAGMATIST |
| **Subtype** | Ecosystem |
| **Confidence** | 70% |
| **Maturity Score** | 2 |

---

## Framework Placement

```
┌─────────────────────────────────────────────────────────────────┐
│                    CDM ADOPTION FRAMEWORK                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ARCHITECT (Native)     │  Production CDM usage                 │
│  Maturity: 5           │  JPMorgan                              │
│                        │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  ARCHITECT (Active)    │  Pilot/POC stage                       │
│  Maturity: 3           │                                        │
│                        │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  PRAGMATIST            │  Vendor-enabled or ecosystem           │
│  Maturity: 2           │  ◄─── Goldman Sachs (Ecosystem)        │
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

## PRAGMATIST (Ecosystem) Characteristics

Goldman Sachs exhibits classic PRAGMATIST (Ecosystem) characteristics:

| Characteristic | Goldman Sachs Evidence |
|---------------|------------------------|
| CDM contribution | Legend platform, FX options model |
| Industry leadership | FINOS member, FO SIG co-leader |
| Technical capability | Legend development proves capability |
| Production deployment | Not confirmed |
| Deployment language | "Investing to implement" |

---

## Phase 8 US Investment Bank Comparison

| Bank | Classification | Confidence | Key Differentiator |
|------|---------------|------------|-------------------|
| JPMorgan | ARCHITECT (Native) | 95% | "Primary mechanism" + maintainer |
| **Goldman Sachs** | **PRAGMATIST (Ecosystem)** | **70%** | **Legend + "investing to implement"** |
| Morgan Stanley | TBD | - | Research pending |
| Citigroup | TBD | - | Research pending |
| Bank of America | TBD | - | Research pending |

---

## Ecosystem Contribution Analysis

### Goldman Sachs Contributions to CDM Ecosystem

| Contribution | Impact |
|--------------|--------|
| Legend platform | Enables cross-bank CDM collaboration |
| FX options model | Accepted into CDM standard |
| CDM pilot leadership | Deutsche Bank, Morgan Stanley, RBC |
| FO SIG co-leadership | Governance role with ISDA |
| Banking Tech Award | Industry recognition |

### Contribution vs Deployment Distinction

| Type | Goldman Sachs | JPMorgan |
|------|---------------|----------|
| Platform contribution | Legend (major) | None specified |
| Model contribution | FX options | None specified |
| Production deployment | None confirmed | Multi-jurisdictional DRR |
| Maintainer status | None | Nick Moger |

Goldman Sachs leads in contribution; JPMorgan leads in deployment.

---

## G-SIB Cohort Position

Goldman Sachs is part of the G-SIB digital derivatives reporting project:

| G-SIB Participant | Confirmed Status |
|-------------------|------------------|
| JPMorgan | ARCHITECT (Native) |
| **Goldman Sachs** | **PRAGMATIST (Ecosystem)** |
| Bank of America | Research pending |
| Citigroup | Research pending |
| Deutsche Bank | ARCHITECT (estimated) |
| BNP Paribas | ARCHITECT (estimated) |

---

## JSON Extract

```json
{
  "bank_id": "goldman-sachs",
  "bank_name": "Goldman Sachs Group, Inc.",
  "classification": "PRAGMATIST",
  "subtype": "Ecosystem",
  "confidence": 0.70,
  "maturity_score": 2,
  "phase": 8,
  "cohort": "us_investment_banks",
  "flags": [
    "legend_platform_contributor",
    "finos_platinum_member",
    "cdm_model_contributor",
    "g_sib_drr_project",
    "drr_investment_confirmed",
    "potential_architect_upgrade"
  ],
  "key_contribution": "Legend platform open-sourced to FINOS",
  "deployment_status": "investing_to_implement"
}
```

---

## Upgrade Pathway

Goldman Sachs has clear pathway to ARCHITECT status:

### Requirements for ARCHITECT Upgrade
1. DRR production deployment announcement
2. "Primary mechanism" or equivalent language
3. Multi-jurisdictional coverage claim

### Likely Timeline
12-18 months based on:
- Active DRR investment
- G-SIB project participation
- Strong technical foundation

### Monitoring Indicators
- Goldman Sachs regulatory filings
- FINOS announcements
- Trade press coverage
- Conference presentations

---

*Framework integration under CDM Research Protocol v2.3*
