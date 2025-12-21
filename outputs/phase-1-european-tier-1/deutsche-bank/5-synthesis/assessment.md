# CDM/DRR Assessment: Deutsche Bank AG

**Bank:** Deutsche Bank AG
**Phase:** 1 - European Tier 1
**Date:** 2025-12-21

---

## Executive Summary

Deutsche Bank AG is classified as a **PRAGMATIST (Regulatory-Driven)** with 55% confidence. Despite having demonstrated open-source capability through active FINOS contributions (Fluxnova, Spring Bot, Waltz), Deutsche Bank is NOT contributing to the Common Domain Model (CDM). Evidence suggests a traditional regulatory compliance approach using DTCC for EMIR reporting rather than CDM-based digital regulatory reporting.

**Key Finding**: The framework v20 claim of "Pilot; production expected 2025" cannot be verified and appears to be inaccurate.

## Bank Profile

| Attribute | Value |
|-----------|-------|
| Full Name | Deutsche Bank AG |
| Headquarters | Frankfurt, Germany |
| Primary Regulator | BaFin |
| Derivatives Relevance | High |
| Business Model | Global universal bank with significant investment banking |
| G-SIB Status | Yes |

## Classification Summary

| Metric | Value |
|--------|-------|
| Classification | PRAGMATIST |
| Sub-Classification | Regulatory-Driven |
| P(ARCHITECT) | 17% |
| P(PRAGMATIST) | 83% |
| Confidence | 55% |

## Evidence Inventory

### Tier 1 Evidence (Official Sources)
| ID | Finding | Direction | Quality |
|----|---------|-----------|---------|
| DB-002 | FINOS contributor to Fluxnova, Waltz, Spring Bot - NOT CDM | NEUTRAL | HIGH |
| DB-003 | EMIR reporting via DTCC traditional approach | PRAGMATIST | HIGH |
| DB-005 | Annual reports 2023-2024 no CDM mentions | NEUTRAL | HIGH |

### Tier 2 Evidence (Industry Sources)
| ID | Finding | Direction | Quality |
|----|---------|-----------|---------|
| DB-001 | JWG RegTech Conference DRR panel Nov 2022 | ARCHITECT | MEDIUM |
| DB-004 | Risk.net: patchy CDM adoption industry-wide | NEUTRAL | MEDIUM |

### Tier 3 Evidence (Signal Sources)
No positive evidence found. All searches returned null results.

## Probability Trajectory

```
Prior:       25% ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Post-Tier1:  14% ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Post-Tier2:  20% ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Post-Tier3:  17% █████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

## Bayesian Analysis Summary

| Evidence | Likelihood Ratio | Cumulative Effect |
|----------|-----------------|-------------------|
| FINOS non-CDM contributor | 0.8 | Decreased |
| DTCC traditional reporting | 0.7 | Decreased |
| Annual report silence | 0.9 | Slightly decreased |
| JWG conference 2022 | 1.5 | Increased |
| Industry cost context | 1.0 | Neutral |
| Tier 3 null results | 0.808 | Decreased |

**Net Combined LR**: 0.61 (supports PRAGMATIST)

## FINOS Paradox Analysis

Deutsche Bank's FINOS contribution pattern reveals a **deliberate strategic choice**:

| FINOS Project | Deutsche Bank Role | CDM Relevance |
|---------------|-------------------|---------------|
| Fluxnova | Co-maintainer | None |
| Spring Bot | Original contributor (Rob Moffat) | None |
| Waltz | Lead maintainer (David Watkins) | None |
| **CDM** | **Not contributing** | **Direct** |

**Interpretation**: Deutsche Bank has the capability and willingness to contribute to FINOS open-source projects. Their absence from CDM is a revealed preference, not a capability limitation.

## Regulatory Compliance Assessment

### EMIR Refit (EU) - Deadline: April 29, 2024
| Aspect | Assessment |
|--------|------------|
| Compliance Status | Presumed compliant (no enforcement actions) |
| Compliance Method | Traditional DTCC reporting |
| CDM Involvement | No evidence |
| ISO 20022 Migration | Presumed complete (required for EMIR Refit) |

### UK EMIR - Deadline: September 30, 2024
| Aspect | Assessment |
|--------|------------|
| Applicability | Yes (Deutsche Bank London Branch) |
| Evidence | None found |

## Vendor Relationship Analysis

| Vendor | Relationship | CDM Component |
|--------|--------------|---------------|
| DTCC | Confirmed - EMIR reporting | Unknown (likely no) |
| Regnology | No evidence | N/A |
| REGnosys | No evidence | N/A |
| Delta Capita | No evidence | N/A |

## Counterparty Network Analysis

| CCP | Membership | CDM Status |
|-----|------------|------------|
| LCH | Presumed member | Unknown |
| Eurex | Presumed member | Unknown |
| CME | Presumed member | Unknown |
| JSCC | Unknown | Not applicable (June 2025 deadline) |

## Product Coverage Assessment

| Product | CDM Status | Confidence |
|---------|------------|------------|
| IRS | Unknown | 30% |
| CDS | Unknown | 30% |
| FX Forwards | Unknown | 30% |
| FX Options | Unknown | 30% |
| Equity Derivatives | Unknown | 30% |

## Knowledge Gaps

### GAP-001: CDM Strategy (Priority: 78/100)
- **Question**: What is Deutsche Bank's official CDM strategy?
- **Impact**: High - cannot distinguish between evaluation and deliberate non-adoption
- **Suggested Source**: Head of Derivatives Technology interview

### GAP-002: DTCC CDM Component (Priority: 55/100)
- **Question**: Does DTCC relationship include any CDM capabilities?
- **Impact**: Medium - could shift classification if CDM is embedded in DTCC
- **Suggested Source**: DTCC relationship manager

## Framework Claim Validation

| Claim | Source | Status | Evidence |
|-------|--------|--------|----------|
| "Pilot; production expected 2025" | Framework v20 | **UNVERIFIED** | None found |

**Assessment**: The framework claim appears to be inaccurate. No evidence of pilot or production timeline found across all evidence tiers.

## Competitive Positioning

### Peer Comparison (European G-SIBs)
| Bank | CDM Status | Evidence Quality |
|------|------------|-----------------|
| BNP Paribas | ARCHITECT-Native (production Q3 2022) | Confirmed |
| Barclays | ARCHITECT-Follower (FINOS contributor) | Confirmed |
| HSBC | Under assessment | - |
| Deutsche Bank | PRAGMATIST (Regulatory-Driven) | This assessment |

## Adoption Drivers Analysis

### Pressures TO Adopt CDM
| Driver | Strength | Status |
|--------|----------|--------|
| EMIR Refit deadline | Medium | Passed (April 2024) |
| Peer pressure (BNP Paribas) | Low | Not activating |
| Industry efficiency savings | Low | Not compelling internally |

### Hesitations AGAINST Adoption
| Factor | Strength | Duration |
|--------|----------|----------|
| Regulatory remediation priority | High | Medium-term |
| CDM implementation costs | Medium | Structural |
| Existing DTCC relationship | Medium | Structural |

**Net Assessment**: Hesitations outweigh pressures

## Risk Factors

### Risks to Classification
| Risk | Probability | Impact |
|------|-------------|--------|
| Silent implementation discovered | Low | Would flip to ARCHITECT |
| Vendor CDM partnership announced | Medium | Would shift to PRAGMATIST (Vendor-Dependent) |
| JSCC connectivity requirement | Low | Would create 2025 pressure |

## Forward-Looking Assessment

### Possible Trajectory Scenarios

**Scenario A: Status Quo (60% probability)**
- Continue traditional compliance approach
- No CDM investment through 2025
- Remains PRAGMATIST

**Scenario B: Late Follower (25% probability)**
- CDM adoption after regulatory remediation complete
- Vendor-facilitated implementation 2026+
- Shifts to PRAGMATIST (Vendor-Dependent) then possibly ARCHITECT-Follower

**Scenario C: Silent ARCHITECT (15% probability)**
- Undisclosed internal CDM work emerges
- Classification incorrect - actually ARCHITECT
- Would require significant evidence emergence

## Recommendations

### For Framework Updates
1. **Remove** "Pilot; production expected 2025" claim - cannot be verified
2. **Reclassify** to PRAGMATIST (Regulatory-Driven)
3. **Flag** for re-assessment in Q2 2025 when regulatory capacity may free up

### For Discovery Calls
1. **Target**: Head of Derivatives Technology
2. **Key Questions**:
   - What is Deutsche Bank's CDM strategy?
   - Did the 2022 DRR conference lead to any internal initiatives?
   - Is DTCC relationship including any CDM components?

## Confidence Calibration

| Factor | Effect on Confidence |
|--------|---------------------|
| Consistent evidence pattern | +10% |
| FINOS paradox clear signal | +10% |
| Reliance on informative absences | -10% |
| Dated positive evidence (2022) | -10% |
| No insider sources | -5% |

**Final Confidence**: 55%

## Appendix: Source URLs

1. [FINOS CDM Resources](https://www.finos.org/common-domain-model)
2. [JWG DRR Regcast](https://jwg-it.eu/regcasts/digitizing-derivative-reporting-with-drr/)
3. [Deutsche Bank EMIR Transaction Reporting](https://www.db.com/legal-resources/european-market-infrastructure-regulation/transaction-reporting)
4. [Deutsche Bank Annual Report 2023](https://investor-relations.db.com/files/documents/annual-reports/2024/Annual-Report-2023.pdf)
5. [Risk.net CDM Coverage](https://www.risk.net/risk-management/6512226/patchy-response-to-isdas-back-office-of-the-future)

## Null Results (Informative Absences)

| Category | Implication |
|----------|-------------|
| ISDA CDM Contributor List | Not listed as contributor despite G-SIB status |
| FINOS CDM Contributor | Contributes to other FINOS projects, NOT CDM |
| CDM Job Postings | No hiring signals for CDM implementation |
| Official CDM Announcements | No CDM content on official websites |
| Production/Pilot Announcements | Framework claim unverified |

---

*Assessment complete. Classification: PRAGMATIST (Regulatory-Driven) with 55% confidence.*
