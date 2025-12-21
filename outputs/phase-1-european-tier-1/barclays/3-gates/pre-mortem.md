# Pre-Mortem Analysis: Barclays PLC

**Bank:** Barclays PLC
**Phase:** 1 - European Tier 1
**Date:** 2025-12-21

---

## Research Objective

**Primary Goal**: Validate or refute Barclays' ARCHITECT classification for CDM adoption

**Key Questions**:
1. Has Barclays demonstrated practical CDM usage or prototypes?
2. Is Lee Braine's advocacy backed by technical implementation work?
3. Has Barclays contributed to FINOS CDM development?
4. Are DerivHack hackathons evidence of genuine CDM commitment vs marketing?
5. What is the current status of CCP prototype mentioned in 2021?

## Potential Failure Modes

### 2.1 False Positive Risks (Wrongly classifying as ARCHITECT)

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Marketing Inflation** | Barclays may be publicizing prototypes as more mature than they are | Carefully distinguish prototype/POC claims from production claims |
| **Thought Leadership Bias** | Lee Braine's public advocacy may exceed internal implementation | Require independent technical evidence, not just executive quotes |
| **Hackathon Overstatement** | DerivHack may be conference/promotional events rather than R&D initiatives | Verify hackathon output and follow-through |
| **Vendor Proxy Confusion** | Barclays may be using CDM vendor tools while claiming internal capability | Require evidence of in-house CDM development vs vendor usage |

### 2.2 False Negative Risks (Wrongly classifying as PRAGMATIST)

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Silent Production** | Barclays may have moved to production after POC phase | Search for recent announcements and hiring signals |
| **Subsidiary Fragmentation** | CDM work may be in specific business units (Barclays Capital, Barclays Treasury) | Search subsidiary announcements separately |

### 2.3 Evidence Quality Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Stale Prototypes** | 2021 CCP prototype may have been abandoned | Require evidence that prototype evolved to pilot or production |
| **FINOS Platform Bias** | FINOS hosting doesn't guarantee production deployment | Require independent production evidence |

## Search Strategy

### Tier 1 (Official Sources)
- Barclays official news/press releases
- FINOS.org CDM documentation (Barclays contributions)
- GitHub finos/common-domain-model (Barclays contributors)
- Barclays Annual Report 2023/2024 (CDM mentions)
- Investor presentations (technology strategy)
- FINOS Open Source Summit presentations

### Tier 2 (Industry Sources)
- Risk.net CDM coverage mentioning Barclays
- Waters Technology derivatives technology coverage
- Financial News London reporting
- Conference presentations (ISDA, FINOS, AITE)
- Vendor announcements mentioning Barclays

### Tier 3 (Signal Sources)
- LinkedIn job postings (CDM, derivatives infrastructure)
- LinkedIn profiles of Barclays derivatives technology team
- Patent filings related to CDM
- Blog posts from Barclays employees

## Key Hypotheses to Test

N/A

## Decision Points

After each evidence tier, evaluate:
1. **Probability Update**: How does evidence change P(ARCHITECT)?
2. **Confidence Level**: Is evidence sufficient for classification?
3. **Sub-Classification**: Is Barclays ARCHITECT-Native (production) or ARCHITECT-Follower (pilot)?

## Null Hypothesis Reminder

Assume Barclays PLC is PRAGMATIST until evidence proves otherwise.

---
