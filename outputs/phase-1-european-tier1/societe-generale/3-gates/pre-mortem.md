# Société Générale - Pre-Mortem Analysis

## Bank Profile
- **Name**: Société Générale S.A.
- **Headquarters**: Paris, France
- **Type**: G-SIB, Universal Bank
- **Derivatives Exposure**: Significant (major European dealer)
- **Regulatory Environment**: ESMA, AMF, EMIR Refit

## Prior Probability
**P(Architect) = 35%** (base rate for European Tier 1 banks)

## Pre-Search Failure Modes

### Failure Mode 1: Conflating SG CIB Technology with CDM
**Risk**: Société Générale's Corporate & Investment Banking (CIB) division has extensive technology initiatives. Risk of conflating general "digital transformation" or "data modernization" with specific CDM adoption.

**Mitigation**: Require explicit CDM/ISDA/FINOS mentions, not just "data standards" or "digitization."

### Failure Mode 2: French Language Sources
**Risk**: Key evidence may be in French (AMF filings, French trade press, internal announcements). English searches may miss relevant signals.

**Mitigation**: Include French keywords in searches (e.g., "modèle de domaine commun", "réglementation EMIR").

### Failure Mode 3: Overweighting Regnosys/Vendor Announcements
**Risk**: Regnosys (CDM tooling vendor) may claim "European bank" clients without naming them. Risk of assuming SG is a client without confirmation.

**Mitigation**: Require bank confirmation of vendor relationships, not just vendor claims.

### Failure Mode 4: ISDA Membership vs CDM Adoption
**Risk**: Société Générale is certainly an ISDA member for derivatives documentation. Risk of conflating ISDA membership with CDM working group participation.

**Mitigation**: Distinguish between ISDA membership (universal for derivatives dealers) and CDM-specific engagement (working groups, contributions).

### Failure Mode 5: BNP Paribas Confusion
**Risk**: BNP Paribas is the most prominent French bank in CDM adoption. Risk of attributing BNP evidence to SG or conflating French bank coverage.

**Mitigation**: Carefully verify bank names in all evidence. Multiple French banks may appear together in CDM discussions.

## Key Research Questions

1. **EMIR Refit Response**: How is SG addressing EMIR Refit? CDM-based or traditional approach?
2. **FINOS/Legend Engagement**: Did SG participate in any FINOS/Legend pilots like Deutsche Bank?
3. **Vendor Relationships**: Any announced partnerships with CDM vendors (Regnosys, Triad, etc.)?
4. **Working Group Participation**: Is SG represented in ISDA CDM working groups?
5. **Internal Technology Initiatives**: Any public statements about CDM from SG's technology leadership?

## Expected Evidence Patterns

### If ARCHITECT:
- Named in FINOS/ISDA CDM press releases
- Speaking at CDM events (CDM Showcase, FINOS events)
- Job postings requiring CDM skills
- Vendor partnership announcements
- Technology blog posts about CDM implementation

### If PRAGMATIST:
- Absent from CDM participant lists
- General regulatory reporting focus without CDM specificity
- Traditional vendor relationships (Bloomberg, Ion, etc.)
- No CDM job postings
- Silence on CDM despite BNP Paribas activity

## Bias Watchlist

1. **Proximity Bias**: BNP Paribas' strong CDM engagement may create expectation that other French banks follow
2. **Authority Bias**: SG's size and sophistication may suggest CDM adoption even without evidence
3. **Recency Bias**: Recent EMIR Refit deadline may create urgency narratives without evidence
4. **Confirmation Bias**: Finding any technology mention and interpreting it as CDM-related

---
*Pre-Mortem Complete*
*Prior: 35% P(Architect)*
*Ready for Tier 1 Evidence Gathering*
