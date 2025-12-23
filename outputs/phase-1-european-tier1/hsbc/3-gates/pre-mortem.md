# HSBC - Pre-Mortem Analysis

## Bank Profile

| Attribute | Value |
|-----------|-------|
| **Bank** | HSBC Holdings plc |
| **Headquarters** | London, UK (with major Hong Kong presence) |
| **Type** | Universal Bank (global, Asia-focused) |
| **G-SIB Status** | Yes |
| **Key Regulators** | FCA, PRA, HKMA, SEC |
| **Prior P(Architect)** | 35% |

## Key Research Questions

1. Is HSBC a FINOS member?
2. Has HSBC contributed to CDM or participated in ISDA working groups?
3. How is HSBC handling EMIR Refit and other regulatory reporting (CDM-based vs traditional)?
4. Given HSBC's Asia focus, is there CDM engagement in Asian jurisdictions?

## Pre-Mortem: Potential Failure Modes

### Failure Mode 1: Asia Reporting Priority
**Risk**: HSBC may focus on Asian regulatory reporting (HKMA, MAS) rather than EU/UK EMIR
**Mitigation**: Search for both EU/UK and Asia-Pacific CDM/DRR engagement

### Failure Mode 2: Vendor-Mediated Adoption
**Risk**: HSBC may use CDM through vendor without direct visibility
**Mitigation**: Check HSBC relationships with Regnosys, Refinitiv, Bloomberg

### Failure Mode 3: FINOS Under Subsidiary Name
**Risk**: HSBC may be a FINOS member under subsidiary name
**Mitigation**: Search for "HSBC" AND "HSBC Global Banking" AND "HBAP" on FINOS site

### Failure Mode 4: Regulatory vs Commercial Focus
**Risk**: CDM engagement may be regulatory-only without commercial strategy
**Mitigation**: Search investor materials for technology strategy

## Expected Evidence Locations

| Source Type | Expected Yield | Priority |
|------------|----------------|----------|
| FINOS membership page | Medium | HIGH |
| ISDA member directory | High | HIGH |
| HSBC investor relations | Low | MEDIUM |
| Risk.net/Waters Technology | Medium | MEDIUM |
| LinkedIn job postings | Medium | LOW |

## Search Strategy

### Tier 1 Searches (Official)
1. "HSBC FINOS member CDM Common Domain Model"
2. "HSBC ISDA CDM working group derivatives"
3. "HSBC EMIR Refit regulatory reporting CDM 2024"
4. "HSBC Digital Regulatory Reporting DRR"
5. "HSBC derivatives technology Regnosys"

### Tier 2 Searches (Trade Press)
1. "HSBC derivatives technology Risk.net 2024"
2. "HSBC regulatory reporting Waters Technology"
3. "HSBC EMIR compliance vendor"

### Tier 3 Searches (Signals)
1. "HSBC CDM jobs LinkedIn"
2. "HSBC ISDA regulatory reporting engineer"

## Null Hypothesis

HSBC is assumed to be a **PRAGMATIST** until evidence proves otherwise. As a UK G-SIB with global derivatives operations, some CDM awareness is expected, but active engagement is unproven.

---
*Pre-Mortem Analysis Complete*
*Generated: 2025-12-21*
