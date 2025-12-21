# Tier 1 Evidence: Lloyds Banking Group plc

**Bank**: Lloyds Banking Group plc
**Date**: 2025-12-20
**Evidence Count**: 1 item

---

## Summary

Lloyds Banking Group has **minimal Tier 1 CDM-specific evidence**. The bank participated in the UK FCA/Bank of England Digital Regulatory Reporting (DRR) pilot in 2018-2019, which utilized ISDA CDM 2.0. However, this evidence is now 5+ years old (historical), and there is NO other Tier 1 evidence of CDM engagement.

**Key Pattern**: Lloyds engaged with CDM during the pilot phase but has shown no continuation since.

---

## Evidence Items

### LBG-001: UK FCA/BoE DRR Pilot Participation (2018-2019)

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
- **Specificity**: Specific (names Lloyds explicitly)

**Caveats**:
- Evidence is from 2018-2019, now 5+ years old
- Pilot participation does not indicate production deployment
- No evidence of continued engagement after pilot completion
- FCA DRR pilot Phase 2 identified gaps and challenges; unclear if Lloyds addressed them

**Likelihood Ratio**: 2.0 (regulatory_pilot_historical)

**Product Scope**: IRS (Interest Rate Swaps), CDS (Credit Default Swaps)

**Jurisdiction Scope**: UK

---

## Informative Absences

### FINOS CDM Contributor Search

**Queries Executed**:
- `site:finos.org Lloyds CDM contributor`
- `site:github.com/finos/common-domain-model Lloyds`
- `Lloyds ISDA CDM contribution`

**Results Reviewed**: 10+

**Null Type**: NO_RESULTS

**Informative Absence**: YES

**Implication**: Lloyds is NOT listed as a FINOS CDM contributor. Unlike NatWest (which contributes to Fluxnova), Lloyds has no visible FINOS engagement at all.

---

### Official CDM Announcements

**Queries Executed**:
- `site:lloydsbankinggroup.com CDM`
- `site:lloydsbankinggroup.com "Common Domain Model"`
- `site:lloydsbankinggroup.com ISDA derivatives`

**Results Reviewed**: 15+

**Null Type**: NO_RESULTS

**Informative Absence**: YES

**Implication**: No official announcements about CDM adoption, pilot continuation, or production deployment since 2019.

---

## Tier 1 Assessment

### Evidence Quality
- **High-Authority Sources**: 1/1 from official source (FCA)
- **Temporal Distribution**: 1 historical (2019), 0 current
- **Claim Types**: 1 pilot_or_poc

### Key Insights

1. **Historical Pilot Engagement Only**: Lloyds participated in UK DRR pilot using CDM 2.0, but this was 5+ years ago
2. **No FINOS Engagement**: Unlike some peers (NatWest, Deutsche Bank), Lloyds has no FINOS participation
3. **No Recent CDM Signals**: Zero official CDM announcements, press releases, or production evidence since 2019
4. **Retail Banking Focus**: As primarily retail/commercial bank, limited derivatives exposure may reduce CDM priority

### Probability Impact

The Tier 1 evidence presents a **weak positive** signal that is undermined by age and lack of continuation:
- Positive: Historical pilot participation (2019)
- Negative: 5+ years of silence since pilot
- Negative: No FINOS engagement
- Negative: Zero recent CDM evidence

**Expected Impact on P(ARCHITECT)**: Neutral to slightly positive (historical evidence only)

---

## Questions for Tier 2

1. Has Lloyds been mentioned in industry press regarding CDM adoption since 2019?
2. Are there vendor announcements linking Lloyds to CDM solutions?
3. Did the DRR pilot lead to any follow-through reported in trade press?
4. What is Lloyds approach to EMIR Refit compliance?

---

*Tier 1 evidence gathering complete. Proceeding to Bayesian update.*
