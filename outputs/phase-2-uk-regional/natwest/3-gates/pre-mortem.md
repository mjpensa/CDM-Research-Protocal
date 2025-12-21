# Pre-Mortem Analysis: NatWest Group PLC

**Bank:** NatWest Group PLC
**Phase:** 2 - UK Regional
**Date:** 2025-12-21

---

## Research Objective

**Primary Goal**: Assess NatWest Group's CDM adoption status for UK Regional bank classification

**Key Questions**:
1. Did NatWest continue CDM work after 2018-2019 FCA/BoE DRR pilot?
2. Is NatWest contributing to FINOS CDM despite other FINOS participation?
3. How is NatWest addressing EMIR Refit compliance?
4. What is NatWest's derivatives technology strategy?
5. Does NatWest's retail focus reduce CDM priority?

## Potential Failure Modes

### 2.1 False Positive Risks (Wrongly classifying as ARCHITECT)

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Pilot Overweight** | Treating 2018-2019 pilot as evidence of current adoption | Apply temporal decay to historical evidence |
| **FINOS Conflation** | Mistaking Fluxnova participation for CDM work | Verify CDM-specific contributions |
| **UK Regulatory Pressure** | Assuming FCA DRR pilot led to production | Search for post-pilot evidence |
| **Retail Bank Underestimation** | Assuming CIB operations drive CDM adoption | Assess derivatives book size |

### 2.2 False Negative Risks (Wrongly classifying as PRAGMATIST)

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Silent Implementation** | NatWest may not publicize CDM work | Search job postings, LinkedIn, vendor announcements |
| **Subsidiary Fragmentation** | CDM work may be in specific business units | Search NatWest Markets separately |
| **Post-Pilot Quiet Period** | Pilot may have led to internal build | Look for 2020-2025 activity |

### 2.3 Evidence Quality Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Stale Evidence** | 2019 pilot evidence is 5+ years old | Require recent corroboration |
| **Retail Focus Bias** | Coverage may focus on retail operations | Target CIB/derivatives searches |

## Search Strategy

### Tier 1 (Official Sources)
- NatWest official news/press releases
- FCA DRR pilot documentation
- FINOS.org contributor searches
- GitHub finos/common-domain-model contributors
- Annual Report 2023/2024 mentions

### Tier 2 (Industry Sources)
- Risk.net NatWest CDM/DRR coverage
- Waters Technology derivatives technology
- Financial News London coverage
- Vendor announcements (Regnology, AxiomSL, DTCC)

### Tier 3 (Signal Sources)
- LinkedIn job postings (CDM, ISDA, DRR keywords)
- LinkedIn profiles of NatWest Markets employees
- Blog posts from employees

## Key Hypotheses to Test

N/A

## Decision Points

After each evidence tier, evaluate:
1. **Probability Update**: How does evidence change P(ARCHITECT)?
2. **Confidence Level**: Is evidence sufficient for classification?
3. **Continue/Skip**: Does probability exceed 80% in either direction?

## Null Hypothesis Reminder

Assume NatWest Group PLC is PRAGMATIST until evidence proves otherwise.

---
