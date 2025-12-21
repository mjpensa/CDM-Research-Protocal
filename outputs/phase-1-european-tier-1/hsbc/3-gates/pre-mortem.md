# Pre-Mortem Analysis: HSBC Holdings PLC

**Bank:** HSBC Holdings PLC
**Phase:** 1 - European Tier 1
**Date:** 2025-12-21

---

## Research Objective

**Primary Goal**: Validate DRR pilot participation and assess current CDM adoption status

**Key Questions**:
1. Did HSBC's 2018-2019 DRR pilot participation lead to production CDM deployment?
2. Is HSBC currently engaged with ISDA CDM or FINOS CDM projects?
3. How did HSBC address EMIR Refit (April 2024) - via CDM or traditional platforms?
4. What is HSBC's technology strategy for derivatives reporting given €22.2T clearing volume?
5. Are there hidden CDM investments given HSBC's scale and DRR history?

## Potential Failure Modes

### 2.1 False Positive Risks (Wrongly classifying as ARCHITECT)

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Pilot Graduation Assumption** | DRR pilot participation might be misinterpreted as ongoing CDM commitment | Require post-2019 evidence for continued engagement |
| **Scale Inference** | Large derivatives player might be assumed to have advanced technology | Verify technology claims with actual platform documentation |
| **Regulatory Response Conflation** | EMIR compliance may be mistaken for CDM adoption | Distinguish between traditional compliance and CDM-based approaches |
| **Vendor Proxy Overreach** | Vendor partnerships may imply CDM without evidence | Require explicit CDM mentions in vendor relationships |

### 2.2 False Negative Risks (Wrongly classifying as PRAGMATIST)

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Silent Post-Pilot Development** | HSBC may have continued CDM work after 2019 pilot without public announcement | Search for hiring signals, LinkedIn activity, GitHub contributions |
| **Subsidiary Fragmentation** | CDM work may be isolated in specific business units | Search major HSBC divisions separately |
| **International Variations** | UK pilot may not represent global HSBC CDM strategy | Check US, Asia, Europe for separate CDM initiatives |
| **Delayed Announcement Pattern** | HSBC may publish DRR updates after regulatory deadlines | Search Q2-Q4 2024 materials post-EMIR deadline |

### 2.3 Evidence Quality Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Paywall Barriers** | Risk.net, Waters Tech may block detailed technology coverage | Use archive.org, public summaries, Google Scholar |
| **Official Website Staleness** | EMIR page may not represent current technology decisions | Cross-check with recent annual reports, SEC filings |
| **Vendor Marketing Inflation** | Vendor press releases may overstate HSBC relationships | Require HSBC confirmation for claimed partnerships |

## Search Strategy

### Tier 1 (Official Sources)
- HSBC official news/press releases on DRR, CDM, regulatory reporting
- ISDA member/working group contributor status
- FINOS.org CDM contributor searches
- GitHub finos/common-domain-model contributor listings
- UK FCA/BoE DRR pilot final reports and participants
- HSBC annual reports 2023/2024 for CDM, DRR, regulatory technology mentions
- SEC filings mentioning derivatives technology strategy

### Tier 2 (Industry Sources)
- Risk.net HSBC CDM/DRR coverage
- Waters Technology derivatives technology coverage
- Financial News London regulatory reporting technology
- ISDA conference speaker searches
- Vendor announcements (Regnology, AxiomSL, Delta Capita, others) mentioning HSBC
- FCA/EBA regulatory reporting guidance documents mentioning participants

### Tier 3 (Signal Sources)
- LinkedIn job postings for CDM, ISDA model, DRR positions
- LinkedIn profiles of HSBC derivatives technology staff
- GitHub activity from HSBC contributors
- Patent filings related to CDM or regulatory reporting

## Key Hypotheses to Test

N/A

## Decision Points

After each evidence tier, evaluate:
1. **Probability Update**: How does evidence change P(ARCHITECT)?
2. **Confidence Level**: Is evidence sufficient for classification?
3. **Continue/Skip**: Does probability exceed 80% in either direction?

## Null Hypothesis Reminder

Assume HSBC Holdings PLC is PRAGMATIST until evidence proves otherwise.

---
