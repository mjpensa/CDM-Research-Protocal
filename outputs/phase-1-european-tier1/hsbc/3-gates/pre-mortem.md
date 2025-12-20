# Pre-Mortem Gate: HSBC Holdings PLC

## Analysis Date
2025-12-19

## Research Subject
HSBC Holdings PLC - Phase 1 European Tier 1 Bank
Headquarters: London, United Kingdom (significant Asia focus)
Primary Regulators: FCA/PRA (UK), HKMA (Hong Kong), MAS (Singapore)

---

## Pre-Mortem Analysis

### Scenario: Research Fails to Produce Reliable Classification

**If this research produces an incorrect or unreliable classification of HSBC's CDM engagement, the most likely causes would be:**

#### 1. Misinterpretation of Vendor Relationship Signals

**Risk**: The Delta Capita partnership (January 2025) is a significant signal that could be misinterpreted in either direction.

**Potential Failure Mode A - False Positive for ARCHITECT**:
- Assuming vendor partnership implies internal capability building
- Over-weighting the "strategic partnership" framing
- Conflating Delta Capita's CDM capabilities with HSBC's internal capabilities

**Potential Failure Mode B - False Negative for ARCHITECT**:
- Dismissing vendor partnership as pure outsourcing when it may indicate strategic CDM adoption
- Missing that HSBC may be using vendors to accelerate CDM integration into their stack
- Underestimating the intentionality behind choosing a CDM-native vendor

**Mitigation**: Carefully distinguish between:
- HSBC building internal CDM capability AND using vendors (ARCHITECT)
- HSBC relying purely on vendor for CDM connectivity (PRAGMATIST)

#### 2. Overweighting 2018 DRR Pilot Participation

**Risk**: HSBC participated in the 2018 UK FCA/BoE Digital Regulatory Reporting pilot alongside other major banks.

**Potential Failure Mode**:
- Assuming pilot participation in 2018 means sustained internal CDM capability development
- Not recognizing that pilot participation was collaborative/exploratory rather than leading to internal expertise
- Missing that 6+ years have passed without visible follow-through on internal CDM initiatives

**Mitigation**: Look for evidence of SUSTAINED engagement post-2018, not just the pilot participation itself.

#### 3. Conflating Outsourcing Trend with CDM Non-Engagement

**Risk**: HSBC is actively exploring outsourcing trading operations (e.g., to Citadel Securities, Jane Street).

**Potential Failure Mode**:
- Conflating operational outsourcing with technology strategy
- Assuming outsourcing means no internal technology investment
- Missing that outsourcing operations while retaining technology strategy oversight is common

**Mitigation**: Distinguish between:
- Operational outsourcing (execution, back-office)
- Technology standards adoption (CDM integration architecture)

#### 4. Geographic Complexity Obscuring True Position

**Risk**: HSBC operates across multiple jurisdictions with different regulatory requirements (UK, EU, HK, Singapore).

**Potential Failure Mode**:
- Missing that CDM strategy may differ by region
- Not accounting for Asian regulators (HKMA, MAS) having different CDM adoption timelines
- Assuming London-centric view represents global approach

**Mitigation**: Search explicitly for Asian regulatory context and HSBC's regional technology strategies.

#### 5. Recency Bias Toward Delta Capita Announcement

**Risk**: The Delta Capita announcement (January 2025) is recent and prominent.

**Potential Failure Mode**:
- Over-indexing on one vendor relationship
- Missing other internal initiatives that may exist but aren't publicized
- Not examining the full scope and meaning of the Delta Capita engagement

**Mitigation**: Search for:
- Internal technology programs beyond vendor relationships
- HSBC's overall derivatives technology strategy
- Hiring patterns for CDM-related roles

---

## Prior Probability Assessment

**Starting Prior**: P(ARCHITECT) = 40%

**Components**:
- Base rate for global systemically important banks: 25%
- Derivatives-dominant adjustment: +10% (HSBC is major derivatives dealer)
- Vendor relationship signal: +5% (ambiguous - could indicate strategic CDM adoption or pure outsourcing)

**Key Uncertainty**: Whether Delta Capita represents:
1. Strategic CDM adoption with vendor execution (ARCHITECT)
2. Outsourced compliance without internal capability (PRAGMATIST)

---

## Classification Criteria for This Bank

### ARCHITECT Classification Requires:
1. Evidence of internal CDM capability development (teams, systems, expertise)
2. Strategic use of vendors to augment (not replace) internal capabilities
3. Contribution to CDM ecosystem (ISDA, FINOS, working groups)
4. Sustained engagement since 2018 DRR pilot

### PRAGMATIST (Vendor-dependent) Classification Requires:
1. Vendor-only approach to CDM (no internal capability)
2. Delta Capita providing CDM connectivity as complete solution
3. No visible internal CDM investment or expertise
4. Compliance-driven rather than strategic technology approach

### Critical Evidence to Seek:
1. Internal CDM development teams or projects at HSBC
2. HSBC contributions to ISDA CDM or FINOS CDM working groups
3. Scope of Delta Capita engagement - full solution or component?
4. Post-2018 DRR pilot follow-through
5. Asian regulatory influence on CDM approach

---

## Confirmation Bias Traps to Avoid

1. **Technology Leadership Halo**: HSBC has invested heavily in AI and fintech ventures. Do not assume this extends to CDM specifically.

2. **ISDA Board Presence Conflation**: HSBC has had executives on ISDA board. Do not assume board presence equals CDM capability development.

3. **Pilot Participation Permanence**: DRR pilot in 2018 was collaborative. Do not assume it led to sustained internal capability.

4. **Vendor Partnership Interpretation**: Delta Capita partnership can support either ARCHITECT or PRAGMATIST classification depending on scope.

5. **Size Bias**: HSBC is very large. Do not assume large banks automatically build internal capabilities.

---

## Decision Rules

**Classify as ARCHITECT if**:
- Evidence of internal CDM capability development AND strategic vendor partnership
- Active contribution to CDM standards ecosystem
- Delta Capita engagement scoped as component, not complete solution

**Classify as PRAGMATIST (Vendor-dependent) if**:
- Delta Capita provides complete CDM solution with no internal HSBC capability
- No evidence of internal CDM development since 2018
- Pure compliance-driven approach via vendor outsourcing

**Default to PRAGMATIST if**:
- Evidence is ambiguous
- Cannot distinguish between strategic vs. outsourced vendor relationship
- No clear evidence of internal capability building

---

## Pre-Mortem Complete

Proceeding to Tier 1 Evidence Collection with awareness of these potential failure modes.
