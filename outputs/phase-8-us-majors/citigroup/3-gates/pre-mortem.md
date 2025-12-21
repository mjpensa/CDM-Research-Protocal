# Pre-Mortem Analysis: Citigroup Inc.

**Research Phase**: 8 (US Major Banks)
**Bank**: Citigroup Inc.
**Date**: 2025-12-21

---

## Scenario: Research Failure

Imagine it is 6 months from now. The research protocol has classified Citigroup as OBSERVER with 50% confidence, but this classification has proven incorrect.

**What went wrong?**

---

## Potential Failure Modes

### 1. Evidence Blind Spots

**Hidden CDM Implementation**
- Citigroup may be implementing CDM internally without public announcements
- Vendor partnerships (Murex, Calypso) could include CDM modules not disclosed publicly
- Regulatory reporting modernization could be CDM-based but described in generic terms

**Private Consortia Participation**
- May be participating in private CDM working groups not listed on ISDA.org
- Could be part of closed-door pilot programs with regulators
- Engagement in G16 dealer CDM collaboration not publicly documented

**Regional Implementation**
- European operations (Citi Europe) might use CDM for EMIR Refit independently
- Asia-Pacific subsidiaries could have separate CDM initiatives
- Different reporting jurisdictions might have varying CDM adoption

### 2. Classification Errors

**Mistaking Quiet Adoption for Absence**
- Large banks often delay public announcements until production-ready
- Compliance initiatives may be considered confidential business strategy
- Competitive advantage concerns could suppress disclosure

**Over-weighting FINOS Membership**
- FINOS membership might indicate broader CDM interest than captured
- Hackathon sponsorship could be first step in deeper engagement
- Community participation might precede technical contribution by 12-18 months

**Under-weighting Regulatory Pressure**
- CFTC Rewrite compliance deadline (2025) creates strong CDM incentive
- EMIR Refit requirements may necessitate CDM adoption not yet announced
- G-SIB enhanced reporting requirements could drive CDM internally

### 3. Temporal Issues

**Evidence Time Lag**
- CDM implementation decisions made in 2023-2024 may not be public yet
- Pilot programs could be ongoing without external announcement
- Vendor contracts signed but not yet in public procurement databases

**Announcement Delay**
- Major banks often announce technology initiatives only after successful deployment
- PR strategy might delay CDM announcements until measurable outcomes
- Regulatory approval processes could postpone public disclosure

**Conference Season Timing**
- Major derivatives conferences (ISDA AGM, TradeTech) not yet occurred in 2025
- Q4 2024 announcements might emerge in Q1 2025
- Annual report (due March 2025) could contain CDM references not yet published

### 4. Source Authority Errors

**Over-reliance on FINOS as Signal**
- FINOS membership without CDM contribution might still indicate CDM usage
- Other open-source engagement (e.g., internal CDM fork) not captured
- Contribution through third-party consultancies not attributed to Citigroup

**Missing Vendor Channels**
- Vendor case studies might mention "major US bank" without naming Citigroup
- Partnership announcements from vendor side not yet discovered
- Reseller relationships (e.g., Accenture implementing Murex CDM) obscuring bank identity

**Regulatory Filing Gaps**
- CFTC/SEC filings might reference "standardized data models" without using "CDM" term
- European regulatory disclosures (BaFin, FCA) not fully searched
- Industry working group meeting minutes not yet analyzed

### 5. Search Strategy Gaps

**Terminology Variations**
- Citigroup might use internal terms: "Enterprise Data Model," "Derivatives Standard Model"
- Press releases could describe CDM functions without using CDM name
- Job postings might reference "ISDA standards" without explicitly stating CDM

**Geographic Search Bias**
- Focus on US/UK sources might miss European/Asian CDM announcements
- Non-English sources (especially for European operations) not fully explored
- Regional trade press (e.g., Asian Risk, European Financial Services) not exhaustively searched

**Platform Coverage**
- GitHub private repositories not visible
- Internal blogs/knowledge bases not accessible
- Intranet job postings more specific than external postings

---

## Mitigation Strategies

### Pre-Research Actions
1. **Expand Vendor Search**: Query Murex, Calypso, SimCorp for "Citigroup" + "CDM" case studies
2. **Regional Deep Dive**: Search EMIR Refit compliance specifically for Citi Europe
3. **Regulatory Filing Review**: Check recent SEC 10-K/10-Q for "standardized data" or "derivatives reporting modernization"

### During Research
1. **Terminology Variants**: Search for "enterprise data model," "standardized derivatives model," "ISDA standards implementation"
2. **Indirect Signals**: Look for Citi attendance at CDM-focused conferences, even without speaking slots
3. **Vendor Proxy**: Check for Citi employees on LinkedIn mentioning vendor tools with CDM capabilities

### Post-Research Validation
1. **Peer Comparison**: If JPMorgan and Goldman have CDM but Citi doesn't, investigate why (competitive disadvantage would be surprising)
2. **Temporal Follow-up**: Flag for re-research in Q1 2025 after annual report publication
3. **Expert Consultation**: Consider reaching out to ISDA or FINOS for non-public member engagement data

---

## High-Risk Assumptions to Challenge

1. **Assumption**: "No Tier 1 evidence = No CDM usage"
   - **Challenge**: Citigroup might have strategic reasons to avoid publicity
   
2. **Assumption**: "FINOS membership without CDM contribution = Observer only"
   - **Challenge**: Contribution might be planned for future, or happening via proxy

3. **Assumption**: "G16 dealer without CDM is implausible"
   - **Challenge**: Traditional platforms might still be sufficient for current needs

4. **Assumption**: "Exhaustive search = Complete evidence"
   - **Challenge**: Proprietary systems and private agreements inherently invisible

---

## Success Criteria for Validation

Within 6 months, check:
1. **Q1 2025 Earnings Call**: Any mention of derivatives reporting technology
2. **Annual Report (March 2025)**: Technology investments section
3. **ISDA AGM (April 2025)**: Citigroup speaker participation or announcements
4. **FINOS GitHub**: Any new Citigroup contributor activity on CDM repos

If none of these reveal CDM evidence, OBSERVER classification is likely correct.

---

**Purpose**: Identify potential research failures before they occur (Kahneman/Klein pre-mortem technique)
