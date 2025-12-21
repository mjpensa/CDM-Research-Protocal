# Pre-Mortem Analysis: Deutsche Bank AG

**Date**: 2025-12-20
**Analyst**: Claude Code Research Protocol
**Prior Probability**: P(ARCHITECT) = 25%

---

## 1. Research Objective

**Primary Goal**: Validate 'Pilot; production expected 2025' claim from framework v20

**Key Questions**:
1. Has Deutsche Bank announced any CDM/DRR pilot or production timeline?
2. Is Deutsche Bank contributing to CDM development at ISDA or FINOS?
3. How did Deutsche Bank address EMIR Refit (April 2024)?
4. Are regulatory enforcement priorities consuming technology capacity?
5. What do named individuals say about derivatives technology direction?

---

## 2. Potential Failure Modes

### 2.1 False Positive Risks (Wrongly classifying as ARCHITECT)

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Vendor Conflation** | Mistaking vendor CDM usage for internal capability | Verify whether CDM work is in-house vs outsourced |
| **Pilot Stagnation** | Old pilot announcements that never progressed | Require evidence dated 2024+ for production claims |
| **Press Release Inflation** | Marketing language overstating actual deployment | Triangulate with technical sources (GitHub, job posts) |
| **ISDA Membership ≠ CDM Usage** | ISDA membership doesn't imply CDM adoption | Require specific CDM/DRR evidence |
| **Regulatory Remediation Noise** | AML/sanctions work may dominate tech coverage | Distinguish CDM investment from remediation spend |

### 2.2 False Negative Risks (Wrongly classifying as PRAGMATIST)

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Silent Implementation** | Deutsche Bank may not publicize CDM work | Search job postings, LinkedIn, conference talks |
| **German Language Barrier** | Key announcements may be in German only | Search German sources (BaFin, German press) |
| **Post-EMIR Quiet Period** | Focus may have shifted after April 2024 deadline | Look for Q2-Q4 2024 activity specifically |
| **Subsidiary Fragmentation** | CDM work may be in specific business units | Search DWS, DB Markets, Postbank separately |

### 2.3 Evidence Quality Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Stale Evidence** | Pre-2023 evidence may not reflect current state | Apply temporal decay weights |
| **Single Source Dependency** | Relying on one vendor or press source | Require corroboration from multiple sources |
| **Paywall Barriers** | Risk.net, Waters Tech may block access | Use archive.org, public summaries |

---

## 3. Search Strategy

### Tier 1 (Official Sources)
- Deutsche Bank official news/press releases
- ISDA.org member/contributor searches
- FINOS.org contributor searches
- GitHub finos/common-domain-model contributors
- BaFin regulatory filings
- Annual Report 2023/2024 mentions

### Tier 2 (Industry Sources)
- Risk.net Deutsche Bank CDM/DRR coverage
- Waters Technology Deutsche Bank derivatives technology
- Financial News London Deutsche Bank reporting
- Conference speaker searches (ISDA AGM, FINOS OSFF)
- Vendor announcements mentioning Deutsche Bank

### Tier 3 (Signal Sources)
- LinkedIn job postings (CDM, ISDA, DRR keywords)
- LinkedIn profiles of derivatives technology staff
- Patent filings related to CDM
- Blog posts from Deutsche Bank employees

---

## 4. Key Hypotheses to Test

### H1: Deutsche Bank is in CDM pilot (framework claim)
- **Evidence needed**: Official announcement, conference presentation, or credible trade press confirmation
- **Disconfirming evidence**: Exhaustive search yields no pilot evidence

### H2: Deutsche Bank is building internal CDM capability
- **Evidence needed**: Hiring for CDM roles, FINOS contributions, internal team references
- **Disconfirming evidence**: All CDM activity via vendors only

### H3: Deutsche Bank is using vendor-only approach
- **Evidence needed**: Vendor announcements (Regnology, AxiomSL, Delta Capita) without internal build evidence
- **Disconfirming evidence**: Clear internal CDM team or FINOS contribution

### H4: Regulatory remediation is consuming CDM capacity
- **Evidence needed**: Continued AML/sanctions investment dominating tech budget
- **Disconfirming evidence**: Evidence of CDM investment despite regulatory work

---

## 5. Decision Points

After each evidence tier, evaluate:
1. **Probability Update**: How does evidence change P(ARCHITECT)?
2. **Confidence Level**: Is evidence sufficient for classification?
3. **Continue/Skip**: Does probability exceed 80% in either direction?

---

## 6. Null Hypothesis Reminder

**Default assumption**: Deutsche Bank is PRAGMATIST until evidence proves otherwise.

Extraordinary claims (ARCHITECT-Native, production deployment) require extraordinary evidence.

---

*Pre-mortem complete. Proceeding to Tier 1 evidence gathering.*
