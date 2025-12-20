# Framework Integration: HSBC Holdings PLC

## Research Date
2025-12-19

## Purpose
Integrate HSBC classification into broader CDM research framework and identify implications for Phase 1 analysis.

---

## Classification Summary

| Attribute | Value |
|-----------|-------|
| Bank Name | HSBC Holdings PLC |
| Headquarters | London, United Kingdom |
| Phase | 1 (European Tier 1) |
| Classification | PRAGMATIST (Vendor-dependent) |
| Confidence | Very High (99%+) |
| Prior P(ARCHITECT) | 40% |
| Posterior P(ARCHITECT) | 0.1% |

---

## Framework Position

### CDM Engagement Spectrum

```
ARCHITECT <--|-----|-----|-----|-----|-----|-----|-----|---> PRAGMATIST
             GS    MS    BNP   C     DB    Barc  UBS   HSBC
```

**HSBC Position**: Far right of spectrum - Vendor-dependent PRAGMATIST

### Engagement Archetype

| Archetype | Description | HSBC Fit |
|-----------|-------------|----------|
| ARCHITECT (Building) | Internal CDM development | NO |
| ARCHITECT (Contributing) | CDM ecosystem contribution | NO |
| PRAGMATIST (Informed) | Vendor use with understanding | PARTIAL |
| PRAGMATIST (Vendor-dependent) | Complete vendor outsourcing | **YES** |

**HSBC Archetype**: PRAGMATIST (Vendor-dependent)

HSBC may have some CDM awareness (from DRR pilot, ISDA engagement), but they have chosen to completely outsource CDM capability to Delta Capita.

---

## Phase 1 Context

### European Tier 1 Banks - Emerging Pattern

| Bank | Classification | Approach |
|------|---------------|----------|
| BNP Paribas | ARCHITECT | Internal development |
| Deutsche Bank | ARCHITECT | Internal + ISDA contribution |
| Barclays | ARCHITECT | DerivHack, internal capability |
| UBS | PRAGMATIST | Vendor-oriented |
| Credit Suisse | (Absorbed) | Was DRR participant |
| **HSBC** | **PRAGMATIST** | **Complete vendor outsourcing** |

### Pattern Observation

HSBC represents the clearest example of PRAGMATIST (Vendor-dependent) among European Tier 1 banks:
- Complete outsourcing to CDM-native vendor
- No internal capability building
- Industry governance without technical contribution

---

## Delta Capita Scope - Framework Implications

### Vendor Engagement Types

| Type | Description | HSBC Status |
|------|-------------|-------------|
| Component | Vendor provides specific CDM component | NO |
| Integration | Vendor assists with internal CDM integration | NO |
| Full Solution | Vendor provides complete CDM capability | **YES** |
| Outsourcing | Vendor handles operations using CDM | **YES** |

**HSBC Type**: Full Solution + Outsourcing

Delta Capita provides both the CDM technology (via Fragmos Chain) and the operational capability (confirmation and settlement services). This is the most vendor-dependent engagement type.

---

## DRR Pilot Participation - Framework Implications

### Pilot-to-Implementation Analysis

| Bank | DRR Participant | Post-Pilot Action | Classification |
|------|-----------------|-------------------|----------------|
| Barclays | Yes | DerivHack, internal dev | ARCHITECT |
| HSBC | Yes | **6-year gap, then outsourced** | PRAGMATIST |
| NatWest | Yes | TBD | TBD |
| Lloyds | Yes | TBD | TBD |
| Santander | Yes | TBD | TBD |

**Framework Learning**: Pilot participation alone does not predict ARCHITECT classification. Post-pilot action is the key signal.

---

## Asian Regulatory Context - Framework Implications

### Multi-Jurisdictional Analysis

| Jurisdiction | CDM Status | HSBC Impact |
|--------------|------------|-------------|
| UK (FCA/PRA) | DRR initiative, CDM-friendly | Primary driver |
| EU (ESMA) | EMIR Refit, CDM-aligned | Applicable |
| Hong Kong (HKMA) | ESMA-aligned, no CDM mandate | Neutral |
| Singapore (MAS) | Harmonizing, no CDM mandate | Neutral |

**Framework Learning**: Banks with significant Asian operations (like HSBC) may feel less pressure for CDM adoption because Asian regulators have not mandated CDM. This may contribute to PRAGMATIST classification.

---

## Outsourcing Strategy - Framework Implications

### Outsourcing as Classification Signal

HSBC's broader outsourcing consideration (trading operations to Citadel/Jane Street) is a useful context signal:

| Outsourcing Stance | Likely CDM Classification |
|--------------------|---------------------------|
| Build internally | ARCHITECT |
| Selective outsourcing | ARCHITECT or PRAGMATIST |
| Comprehensive outsourcing | PRAGMATIST |

**Framework Learning**: Banks actively considering operational outsourcing are more likely to be PRAGMATIST for CDM as well. This is a useful screening signal.

---

## ISDA Engagement Analysis

### Governance vs. Technical Contribution

| Engagement Type | CDM Signal | HSBC Status |
|-----------------|------------|-------------|
| Board membership | Weak | Present |
| Board Chair | Weak | Present (temp) |
| CDM working group | Strong | NOT FOUND |
| CDM code contribution | Strong | NOT FOUND |
| CDM publication | Moderate | NOT FOUND |

**Framework Learning**: ISDA board presence is not sufficient for ARCHITECT classification. Technical CDM contribution is required.

---

## Vendor Partnership Classification Matrix

### How to Classify Vendor Relationships

| Vendor Relationship | Classification |
|--------------------|----------------|
| Using vendor to accelerate internal capability | ARCHITECT |
| Using vendor as component in internal architecture | ARCHITECT |
| Using vendor to provide complete solution | PRAGMATIST |
| Outsourcing operations to vendor using CDM | PRAGMATIST |

**HSBC Position**: Outsourcing operations to vendor using CDM = PRAGMATIST

---

## Key Research Questions Answered

### Q1: Is HSBC building internal CDM capability in addition to Delta Capita?
**Answer**: NO - No evidence of internal capability

### Q2: Or is HSBC purely relying on vendor for CDM connectivity?
**Answer**: YES - Complete vendor reliance

### Q3: What is the scope of the Delta Capita engagement?
**Answer**: COMPREHENSIVE - Global confirmation and settlement

### Q4: Did HSBC's 2018 pilot participation lead to sustained internal capability?
**Answer**: NO - 6-year gap followed by outsourcing

### Q5: How do Asian regulatory requirements affect HSBC's approach?
**Answer**: MINIMAL - No CDM mandate in Asian jurisdictions reduces pressure

---

## Calibration Assessment

### Prior Probability Accuracy

| Component | Prior Adjustment | Actual Impact | Calibration |
|-----------|------------------|---------------|-------------|
| Base rate | 25% | Appropriate | Correct |
| Derivatives-dominant | +10% | Overestimated | Too high |
| Vendor relationship | +5% (ambiguous) | Confirmed PRAGMATIST | Correct interpretation |

**Calibration Learning**: Derivatives market dominance does not predict ARCHITECT classification. Banks can be major derivatives dealers while outsourcing CDM capability.

### Posterior Accuracy

**Final P(ARCHITECT)**: 0.1%
**Confidence**: Very High

This is an extreme posterior probability, but the evidence strongly supports it:
1. Direct evidence of comprehensive outsourcing
2. Multiple null results for internal development
3. Consistent pattern with broader strategy

---

## Framework Recommendations

### Based on HSBC Analysis

1. **Add Outsourcing Signal**: Banks with active operational outsourcing strategies should be flagged as more likely PRAGMATIST

2. **Pilot Participation Timeout**: DRR/CDM pilot participation older than 3 years without follow-through should not be weighted positively

3. **Governance vs. Technical Distinction**: Explicitly distinguish ISDA board roles from CDM technical contribution

4. **Multi-Jurisdiction Analysis**: Consider regulatory CDM mandates (or lack thereof) across jurisdictions where bank operates

5. **Vendor Scope Taxonomy**: Classify vendor relationships as Component/Integration/Full Solution/Outsourcing

---

## Cross-Reference Notes

### Related Banks

| Bank | Relationship to HSBC Analysis |
|------|------------------------------|
| Barclays | Also DRR participant; different outcome (ARCHITECT) |
| NatWest | DRR participant; TBD classification |
| Goldman Sachs | ARCHITECT reference case |
| Delta Capita clients | Other banks using Delta Capita may show similar pattern |

### Related Vendors

| Vendor | Role in HSBC Analysis |
|--------|----------------------|
| Delta Capita | Primary CDM provider for HSBC |
| Fragmos Chain | CDM-native technology platform |
| Finastra | Also uses Fragmos Chain (potential comparison) |

---

## Research Protocol Validation

### Protocol Steps Executed

| Step | Status | Notes |
|------|--------|-------|
| Pre-Mortem Gate | Complete | Identified key risks |
| Tier 1 Evidence | Complete | 15+ searches conducted |
| Null Results | Documented | Pattern of absence recorded |
| Bayesian Update | Complete | Probability trajectory documented |
| Gate 1 | Complete | PRAGMATIST classification confirmed |
| Tier 2 | Skipped | Evidence sufficiently conclusive |
| Adversarial Challenge | Complete | Classification survived |
| Synthesis | Complete | 19-section assessment |

### Protocol Effectiveness

The research protocol successfully:
1. Identified Delta Capita outsourcing as key evidence
2. Documented null results pattern
3. Distinguished governance from technical engagement
4. Applied adversarial challenge appropriately
5. Produced high-confidence classification

---

## Final Integration Statement

HSBC Holdings PLC is integrated into the CDM research framework as:

**Classification**: PRAGMATIST (Vendor-dependent)
**Position**: Right edge of engagement spectrum
**Archetype**: Complete vendor outsourcing
**Confidence**: Very High (99%+)

This classification completes the final bank in Phase 1 European Tier 1 analysis.

---

## Phase 1 Summary (European Tier 1)

| Bank | Classification | Confidence |
|------|---------------|------------|
| BNP Paribas | ARCHITECT | High |
| Deutsche Bank | ARCHITECT | High |
| Barclays | ARCHITECT | High |
| UBS | PRAGMATIST | Moderate-High |
| **HSBC** | **PRAGMATIST** | **Very High** |

**Phase 1 Pattern**: European Tier 1 banks show mixed ARCHITECT/PRAGMATIST distribution, with HSBC as the clearest PRAGMATIST example due to complete vendor outsourcing.
