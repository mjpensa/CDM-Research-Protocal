# Pre-Mortem Analysis: Citigroup Inc.

**Bank:** Citigroup Inc.
**Phase:** 8 - US Investment Banks
**Date:** 2025-12-21

---

## Research Objective

Assess Citigroup Inc.'s CDM/DRR adoption maturity.

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

## Search Strategy

### Tier 1 (Official Sources)
- Bank official website, annual reports
- ISDA.org, FINOS.org
- Regulatory filings

### Tier 2 (Industry Sources)
- Risk.net, Waters Technology
- Trade press coverage
- Vendor announcements

### Tier 3 (Signal Sources)
- Job postings
- LinkedIn profiles
- Conference presentations

## Key Hypotheses to Test

N/A

## Decision Points

1. After Tier 1: If P(ARCHITECT) < 20% or > 80%, consider early classification
2. After Tier 2: Assess if Tier 3 signals will add value
3. After Tier 3: Proceed to adversarial challenge

## Null Hypothesis Reminder

Assume Citigroup Inc. is PRAGMATIST until evidence proves otherwise.

---
