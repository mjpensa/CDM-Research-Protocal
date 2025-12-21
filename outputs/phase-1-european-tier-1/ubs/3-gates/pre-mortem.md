# Pre-Mortem Analysis: UBS Group AG

**Bank:** UBS Group AG
**Phase:** 1 - European Tier 1
**Date:** 2025-12-21

---

## Research Objective

**Primary Goal**: Determine whether UBS is adopting CDM despite being in the midst of the largest M&A integration in financial services history

**Key Questions**:
1. Is the 2020 DAML pilot evidence of ongoing CDM engagement, or historical artifact?
2. Did UBS continue Credit Suisse's CDM work after the March 2023 acquisition?
3. Is technology capacity genuinely consumed through 2026, or is that estimate conservative?
4. Will UBS restart CDM initiatives post-integration, or pivot to traditional approaches?
5. Are there hidden signals of CDM planning within integration project work?

## Potential Failure Modes

### 2.1 False Positive Risks (Wrongly classifying as ARCHITECT)

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Pilot Stagnation** | 2020 DAML pilot looked promising but never matured | Require evidence of continued engagement post-2020 |
| **Integration Narrative Bias** | Assume all capacity is integration-consumed without verification | Look for any CDM signals despite integration workload |
| **Inherited Capability Overweighting** | Credit Suisse CDM work may not survive integration or cultural integration | Verify post-merger continuation explicitly |
| **Missing Hidden Work** | CDM work could be hidden in integration sub-projects | Check merger integration documentation for CDM components |
| **Vendor Proxy Conflation** | Assuming vendor CDM tools = UBS internal CDM capability | Distinguish UBS-built vs vendor-provided CDM |

### 2.2 False Negative Risks (Wrongly classifying as PRAGMATIST)

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Silent Pilot** | UBS may be running CDM work quietly during integration chaos | Look for hiring, conference presence, GitHub activity |
| **Post-Integration Planning** | UBS may be planning CDM restart for 2027+ without public signals | Check for strategic hiring in 2024-2025 for future capability |
| **Binned Capability** | Credit Suisse CDM team members may be retained (binned) for post-2026 restart | Search for Sunil Challa and other CS CDM staff at UBS |
| **Infrastructure Continuity** | Integration may preserve Credit Suisse's CDM infrastructure even if not actively used | Look for infrastructure investment, not just explicit CDM projects |

### 2.3 Evidence Quality Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Stale Evidence** | 2020 evidence is 5 years old; integration pressure is recent | Balance old positive with recent constraint evidence |
| **Integration Timeline Assumption** | "Through 2026" estimate may shift based on progress | Check for updated integration timelines (Q4 2024+) |
| **Suint Evidence Gaps** | Credit Suisse CDM status unclear - did it pause or cease? | Search for Credit Suisse CDM continuity evidence |

## Search Strategy

### Tier 1 (Official Sources)
- UBS investor relations for CDM/DRR mentions
- UBS annual report 2024 and H1 2024 earnings calls
- ISDA.org member directory or CDM working group participant lists
- FINOS.org CDM contributor search
- GitHub finos/common-domain-model contributors from UBS
- Press releases on integration status and technology capacity allocation

### Tier 2 (Industry Sources)
- Risk.net: UBS derivatives technology coverage (especially post-merger)
- Waters Technology: UBS CDM or integration technology coverage
- Financial News London: UBS derivatives tech strategy
- Conference speaker searches (ISDA AGM 2024, FINOS OSFF 2024)
- Vendor announcements mentioning UBS and CDM (Axoni, Symbiont, DTCC)
- Merger & Integration analyst reports mentioning CDM/regulatory tech

### Tier 3 (Signal Sources)
- LinkedIn job postings: UBS CDM, DRR, ISDA model positions
- LinkedIn profiles: Sunil Challa, Vinay Srinivas, other CDM staff
- GitHub commits: UBS employees contributing to CDM
- Patent filings related to CDM or regulatory reporting
- Substack/blogs from UBS technology staff on CDM

## Key Hypotheses to Test

N/A

## Decision Points

After each evidence tier, evaluate:
1. **Probability Update**: Does evidence change P(ARCHITECT)?
2. **Integration Constraint Confirmation**: Is the constraint genuinely binding, or can some CDM work proceed?
3. **Continue/Skip**: Can we classify UBS as PRAGMATIST (Integration-Constrained) and move to synthesis, or does probability exceed thresholds?

## Null Hypothesis Reminder

Assume UBS Group AG is PRAGMATIST until evidence proves otherwise.

---
