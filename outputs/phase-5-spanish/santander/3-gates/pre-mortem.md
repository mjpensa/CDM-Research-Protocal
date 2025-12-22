# Pre-Mortem Analysis: Santander

**Bank**: Banco Santander S.A.
**Phase**: 5 (Spanish)
**Date**: 2025-12-21

---

## 1. Research Objective

Assess Santander's positioning relative to ISDA Common Domain Model (CDM) and Digital Regulatory Reporting (DRR) initiatives, with focus on:
- FINOS membership or CDM contribution activity
- ISDA governance participation
- EMIR Refit (April 2024) response strategy
- Vendor relationship patterns

## 2. Prior Probability Assessment

**Starting Assumption**: PRAGMATIST (per protocol null hypothesis)

**Adjustments**:
- European regulatory pressure (EMIR Refit): +5%
- Medium derivatives relevance (retail banking focus): -5%
- No known prior CDM evidence: 0%

**Adjusted Prior**: 35% probability of any CDM engagement above OBSERVER level

## 3. Potential Failure Modes

### 3.1 False Positive Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| Vendor marketing conflation | Santander may be cited in vendor press releases without actual CDM adoption | Require bank-side confirmation for Tier 1/2 claims |
| FINOS membership confusion | Santander may participate in non-CDM FINOS projects (Waltz, Legend, Fluxnova) | Verify specific CDM repository contributions |
| Retail banking noise | Digital transformation coverage may be misread as derivatives technology | Focus searches on derivatives-specific terms |
| Spanish language barrier | English searches may miss Spanish-language technical announcements | Include Spanish terms in search queries |

### 3.2 False Negative Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| Latin American focus obscuring EU work | Coverage may emphasize LatAm retail over EU derivatives | Search specifically for EU regulatory compliance |
| Internal-only initiatives | CDM work may be underway but not publicized | Check job postings for signals |
| Vendor-mediated adoption | CDM engagement via vendor may not mention "CDM" | Search for known CDM vendors (Murex, Calypso, REGnosys) |

### 3.3 Structural Research Challenges

| Challenge | Impact | Approach |
|-----------|--------|----------|
| Decentralized structure | Santander operates as federation of country banks | Search both "Santander" and "Banco Santander" |
| Investment banking scale | Santander CIB is smaller than universal bank peers | Calibrate expectations for derivatives focus |
| Privacy norms | European banks may not publicize technology choices | Weight trade press over corporate announcements |

## 4. Search Strategy Calibration

### Tier 1 Targets (High Authority)
1. FINOS CDM GitHub contributor list
2. ISDA Board membership list
3. ISDA CDM steering committee
4. Regulatory filings mentioning CDM/DRR

### Tier 2 Targets (Medium Authority)
1. Risk.net / Waters Technology coverage
2. EMIR Refit vendor announcements citing Santander
3. Conference presentations (ISDA events, Sibos)
4. CFTC swap dealer registration (for US operations)

### Tier 3 Targets (Low Authority)
1. Job postings: "CDM", "ISDA", "derivatives reporting"
2. LinkedIn profiles of Santander derivatives technology staff
3. Spanish financial technology press

## 5. Classification Thresholds

| Classification | Evidence Required |
|---------------|-------------------|
| ARCHITECT | Production usage OR pilot + FINOS contribution |
| PRAGMATIST (ISDA Governance) | ISDA Board without FINOS CDM |
| PRAGMATIST (Ecosystem) | FINOS member without CDM contribution |
| PRAGMATIST (Vendor) | Vendor relationship for derivatives reporting |
| PRAGMATIST (Traditional) | Active derivatives, no CDM signals |
| OBSERVER | Membership/participation only |
| UNKNOWN | No verified evidence |

## 6. Red Flags to Watch

- Claims of "CDM production" without corroboration
- Vendor-only evidence without bank confirmation
- Evidence older than 18 months without recent follow-up
- Conflation with non-CDM FINOS projects

## 7. Expected Outcome Distribution

Based on Phase 4 patterns and Santander's profile:

| Classification | Probability |
|---------------|-------------|
| ARCHITECT | 5% |
| PRAGMATIST (any type) | 55% |
| OBSERVER | 25% |
| UNKNOWN | 15% |

---

*Pre-mortem completed. Proceeding to Tier 1 evidence collection.*
