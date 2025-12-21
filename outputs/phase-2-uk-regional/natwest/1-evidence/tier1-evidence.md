# Tier 1 Evidence: NatWest Group plc

**Bank**: NatWest Group plc
**Date**: 2025-12-20
**Evidence Count**: 2 items

---

## Summary

NatWest Group has **limited Tier 1 CDM-specific evidence**. The bank participated in the UK FCA/Bank of England Digital Regulatory Reporting (DRR) pilot in 2018-2019, which utilized ISDA CDM 2.0. However, this evidence is now 5+ years old (historical). More recently, NatWest has demonstrated significant open-source capability through co-maintaining FINOS Fluxnova, but this project is NOT CDM-related.

**Key Pattern**: NatWest has FINOS open-source capability but is NOT contributing to CDM projects.

---

## Evidence Items

### NW-001: UK FCA/BoE DRR Pilot Participation (2018-2019)

**Source**: https://www.fca.org.uk/innovation/regtech/digital-regulatory-reporting

**Tier**: 1 (Official Regulatory Source)

**Claim Type**: pilot_or_poc

**Date**: 2019-02-01

**Excerpt**:
> "In 2018 and 2019, the 2 UK regulators collaborated with 7 banks to complete 2 pilots. The banks were Barclays, Credit Suisse, HSBC, Lloyds, Nationwide, NatWest and Santander."

**Direction**: SUPPORTS_ARCHITECT

**Quality Assessment**:
- **Authority**: HIGH (official FCA source)
- **Recency**: Historical (5+ years old)
- **Specificity**: Specific (names NatWest explicitly)

**Caveats**:
- Evidence is from 2018-2019, now 5+ years old
- Pilot participation does not indicate production deployment
- No evidence of continued engagement after pilot completion
- FCA DRR pilot identified gaps and challenges; unclear if NatWest addressed them

**Likelihood Ratio**: 2.0 (regulatory_pilot_historical)

**Product Scope**: IRS (Interest Rate Swaps), CDS (Credit Default Swaps)

**Jurisdiction Scope**: UK

---

### NW-002: FINOS Fluxnova Co-Maintainer (Non-CDM)

**Source**: https://www.finos.org/press/finos-launches-fluxnova-with-fidelity-investments-natwest-group-deutsche-bank-and-capital-one-an-open-source-orchestration-platform-to-scale-process-automation

**Tier**: 1 (Official FINOS Source)

**Claim Type**: open_source_contribution

**Date**: 2025-10-21

**Excerpt**:
> "Fluxnova is a new open source orchestration platform developed under FINOS governance and co-maintained by Fidelity, NatWest Group, Deutsche Bank, Capital One and BMO."

**Direction**: NEUTRAL (NOT CDM-related)

**Quality Assessment**:
- **Authority**: HIGH (official FINOS announcement)
- **Recency**: Current (October 2025)
- **Specificity**: Specific (names James McLeod as Head of Open Source)

**Caveats**:
- **Fluxnova is NOT CDM** - it is a process orchestration platform
- Demonstrates FINOS open-source capability but NOT CDM adoption
- Creates "FINOS Paradox": capable of contributing to FINOS projects but NOT contributing to CDM

**Likelihood Ratio**: 1.2 (finos_contributor_non_cdm)

**Key Individual**: James McLeod, Head of Open Source, FINOS Gold Member Representative

**Product Scope**: None (process orchestration)

**Jurisdiction Scope**: None

---

## Informative Absences

### FINOS CDM Contributor Search

**Queries Executed**:
- `site:finos.org NatWest CDM contributor`
- `site:github.com/finos/common-domain-model NatWest`
- `NatWest ISDA CDM contribution`

**Results Reviewed**: 10+

**Null Type**: NO_RESULTS

**Informative Absence**: YES

**Implication**: Despite being a FINOS Gold Member and co-maintaining Fluxnova, NatWest is NOT contributing to FINOS CDM projects. This creates a significant informative absence pattern - the bank has demonstrated FINOS capability but deliberately NOT in CDM.

---

## Tier 1 Assessment

### Evidence Quality
- **High-Authority Sources**: 2/2 items from official sources (FCA, FINOS)
- **Temporal Distribution**: 1 historical (2019), 1 current (2025)
- **Claim Types**: 1 pilot_or_poc, 1 open_source_contribution (non-CDM)

### Key Insights

1. **Historical CDM Engagement**: NatWest participated in UK DRR pilot using CDM 2.0, but this was 5+ years ago
2. **FINOS Paradox**: Active FINOS contributor (Fluxnova) but NOT contributing to CDM
3. **No Recent CDM Signals**: Zero official CDM announcements, press releases, or production evidence since 2019
4. **Open Source Capability**: Demonstrates technical capability for open-source collaboration but not applying it to CDM

### Probability Impact

The Tier 1 evidence presents a **mixed but ultimately negative** signal:
- Positive: Historical pilot participation (2019)
- Negative: No continuation after pilot
- Negative: FINOS capability without CDM application
- Negative: Zero recent CDM evidence

**Expected Impact on P(ARCHITECT)**: Neutral to slightly negative

---

## Questions for Tier 2

1. Has NatWest been mentioned in industry press regarding CDM adoption since 2019?
2. Are there vendor announcements linking NatWest to CDM solutions?
3. Did the DRR pilot lead to any follow-through reported in trade press?
4. What is NatWest's approach to EMIR Refit compliance?

---

*Tier 1 evidence gathering complete. Proceeding to Bayesian update.*
