# Tier 1 Evidence: Deutsche Bank AG

**Date**: 2025-12-21
**Tier**: 1 (Official Sources)
**Evidence Count**: 3

---

## Evidence Summary

| ID | Claim Type | Date | Direction | Source Authority |
|----|------------|------|-----------|------------------|
| DB-001 | pilot_or_poc | 2021-01 | SUPPORTS_ARCHITECT | HIGH |
| DB-002 | open_source_contribution | 2021-01 | SUPPORTS_ARCHITECT | HIGH |
| DB-003 | membership_or_participation | 2021-08 | SUPPORTS_ARCHITECT | HIGH |

---

## DB-001: FINOS Legend Pilot Participation

**Claim**: Deutsche Bank participated in the FINOS Legend Studio 6-month pilot (2020-2021) to prototype interbank collaborative data modeling, specifically to build FX Options extensions to the CDM

**Source**: [FINOS Legend Case Study 2021](https://www.finos.org/hubfs/FINOS/assets/FINOS%20Legend%20Case%20Study%202021.pdf)

**Excerpt**:
> Leading investment banks including Deutsche Bank, Morgan Stanley and RBC Capital Markets participated in a six-month pilot using a shared version of Legend, hosted on FINOS infrastructure in the public cloud, to prototype interbank collaborative data modeling and standardization, particularly to build extensions to the Common Domain Model (CDM).

**Quality Assessment**:
- Authority: HIGH (FINOS official publication)
- Recency: HISTORICAL (2021, >3 years old)
- Specificity: SPECIFIC (named participants, specific outcome)

**Caveats**:
- Pilot from 2020-2021 is historical evidence
- Temporal weight: 0.3 (>3 years old)
- Need to verify continued engagement post-pilot

---

## DB-002: FX Options CDM Contribution

**Claim**: Deutsche Bank's FX Options extensions (specifically the Averaging Model) from the Legend pilot were proposed into the CDM, accepted, and integrated into a public CDM release

**Source**: [FINOS Legend Case Study 2021](https://www.finos.org/hubfs/FINOS/assets/FINOS%20Legend%20Case%20Study%202021.pdf)

**Excerpt**:
> The FX option extensions, specifically the Averaging Model used in the CDM, modeled collaboratively by the pilot group financial institutions participants using Legend, were proposed into the CDM and have since been accepted, released and integrated into a recent release to the public.

**Quality Assessment**:
- Authority: HIGH (FINOS official publication)
- Recency: HISTORICAL (2021)
- Specificity: SPECIFIC (named contribution accepted into CDM)

**Caveats**:
- One-time contribution without evidence of sustained engagement
- No evidence of Deutsche Bank using CDM internally
- Contribution demonstrates capability, not production adoption

---

## DB-003: Russell Green FINOS Board Vice Chairman

**Claim**: Russell Green (MD, Head of Group Architecture) elected as FINOS Board Vice Chairman in August 2021, advocating for CDM and data modeling collaboration

**Source**: [FINOS Press Release](https://www.finos.org/press/technology-leaders-from-goldman-sachs-and-deutsche-bank-elected-finos-new-governing-board-chairs-as-open-source-collaboration-expands-further-across-financial-services)

**Excerpt**:
> John Madsen, chief architect for technology at Goldman Sachs, became FINOS board chairman and Russell Green, head of cloud architecture at Deutsche Bank, became the new vice chairman.

**Named Individual**: Russell Green, MD, Head of Cloud Architecture

**Quality Assessment**:
- Authority: HIGH (FINOS official announcement)
- Recency: HISTORICAL (August 2021)
- Specificity: SPECIFIC (named individual, specific role)

**Caveats**:
- FINOS board role indicates governance engagement
- Does not confirm CDM technical implementation
- Does not confirm production usage

---

## Null Results (Tier 1)

### CDM Production Deployment
- **Queries**: "Deutsche Bank CDM production deployment 2023 2024"
- **Results**: No relevant results found
- **Implication**: No evidence of production deployment. Legend pilot was exploratory only.

### Post-2021 CDM Activity
- **Queries**: "Deutsche Bank CDM 2022", "Deutsche Bank CDM 2023"
- **Results**: No relevant results found
- **Implication**: 3+ year gap since pilot suggests it did not lead to production adoption.

### EMIR Refit CDM Approach
- **Queries**: "Deutsche Bank EMIR Refit CDM 2024"
- **Results**: No Deutsche Bank-specific CDM approach found
- **Implication**: Deutsche Bank likely used traditional methods for EMIR Refit compliance.

---

## Tier 1 Assessment

**Positive Signals**:
1. Confirmed FINOS Legend pilot participation (2020-2021)
2. Accepted FX Options contribution to CDM (Averaging Model)
3. Named MD-level executive (Russell Green) in FINOS leadership

**Negative Signals**:
1. All evidence is historical (>3 years old)
2. No evidence of post-2021 CDM activity
3. No production deployment announced
4. No EMIR Refit CDM approach found

**Preliminary Direction**: SUPPORTS_ARCHITECT for historical engagement, but temporal weighting significantly reduces confidence. Pattern suggests exploration without production follow-through.
