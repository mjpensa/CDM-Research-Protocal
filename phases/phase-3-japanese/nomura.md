# Nomura Holdings — CDM/DRR Research

## Bank Profile

| Attribute | Value |
|-----------|-------|
| **Full Name** | Nomura Holdings, Inc. |
| **Headquarters** | Tokyo, Japan |
| **Region** | Japan |
| **Business Model** | Largest Japanese investment bank/securities firm |
| **Derivatives Relevance** | High — significant global derivatives business |
| **Execution Tier** | B (Standard Protocol) |

---

## Research Objective

**Primary Goal:** Determine if Nomura is building CDM capability in response to JSCC production

**Critical Context:** JSCC (Japan Securities Clearing Corporation) went live with CDM in June 2025. Nomura clears through JSCC, creating structural connectivity requirement.

**Key Questions:**
1. How is Nomura responding to JSCC CDM production?
2. Is Nomura building internal CDM capability or relying on connectivity wrapper?
3. What is named leadership saying about derivatives technology direction?
4. What is JFSA regulatory pressure specifically requiring?

---

## JSCC Forcing Function Analysis

### The Structural Pressure
- JSCC went live June 27, 2025 (first CCP in CDM production globally)
- Banks clearing through JSCC face CDM connectivity requirements
- Nomura is a major JSCC clearing member
- This creates infrastructure-led adoption pressure distinct from regulatory mandate

### Key Question
Is Nomura:
- **(A) Building internal CDM capability** → ARCHITECT
- **(B) Implementing connectivity layer/wrapper only** → PRAGMATIST (Infrastructure-driven)
- **(C) Relying on vendor for JSCC connectivity** → PRAGMATIST (Vendor-dependent)

---

## Prior Probability Assessment

### Base Priors with JSCC Adjustment
- P(ARCHITECT) = 35% (elevated due to JSCC pressure)
- P(PRAGMATIST) = 65%
- Prior Odds = 0.54

### Contextual Factors
- Largest Japanese investment bank — high derivatives exposure
- JSCC production creates immediate pressure
- Japanese financial institutions tend to follow infrastructure leads
- But may implement minimum viable connectivity rather than full CDM

---

## Pre-Mortem Analysis (Abbreviated)

### Primary Failure Mode
JSCC connectivity may not require full CDM adoption — Nomura may implement a translation layer rather than native CDM capability. Evidence of "JSCC connectivity" does not automatically mean "ARCHITECT classification."

### Mitigation
Distinguish between:
- "Connected to JSCC" (minimum requirement)
- "Building CDM-native infrastructure" (ARCHITECT signal)

---

## Search Strategy

### Tier 1 Searches

**SEARCH 1.1:** Nomura "Common Domain Model" OR CDM 2024 2025
**SEARCH 1.2:** Nomura "Digital Regulatory Reporting" ISDA
**SEARCH 1.3:** Nomura JSCC CDM connectivity implementation
**SEARCH 1.4:** Nomura annual report 2024 derivatives technology
**SEARCH 1.5:** site:nomura.com CDM OR "regulatory reporting"

### Abbreviated Reasoning Gate 1
[Complete abbreviated gate after Tier 1]

---

### Tier 2 Searches

**SEARCH 2.1:** Nomura JFSA derivatives reporting technology
**SEARCH 2.2:** Nomura CFTC swap reporting approach
**SEARCH 2.3:** "Yutaka Nakajima" Nomura ISDA (known executive)
**SEARCH 2.4:** Nomura ISDA AGM Tokyo 2024 speaker
**SEARCH 2.5:** Nomura derivatives clearing Japan infrastructure
**SEARCH 2.6:** Nomura post-trade technology investment

### Abbreviated Reasoning Gate 2
[Complete abbreviated gate after Tier 2]

---

### Tier 3 Searches

**SEARCH 3.1:** Nomura FINOS member contributor
**SEARCH 3.2:** Nomura vendor derivatives technology partner
**SEARCH 3.3:** Nomura job posting CDM OR DRR
**SEARCH 3.4:** Nomura vs MUFG vs Mizuho derivatives technology

### Abbreviated Reasoning Gate 3
[Complete abbreviated gate after Tier 3]

---

## Adversarial Check (Abbreviated)

After preliminary classification, complete /templates/adversarial-checks.md (Abbreviated version):

- Counter-argument construction
- Single targeted disconfirming search
- Confidence adjustment

---

## JSCC Response Classification

| Response Type | Evidence Pattern | Classification |
|---------------|------------------|----------------|
| Building CDM-native infrastructure | Internal CDM initiative, contribution to standard, production plans | ARCHITECT-Follower |
| Implementing full CDM for competitive advantage | CDM beyond JSCC requirement, leadership signaling | ARCHITECT-Leader |
| Minimum JSCC connectivity | Connectivity announcements only, no broader CDM | PRAGMATIST (Infrastructure-driven) |
| Vendor-mediated connectivity | Third-party handling JSCC interface | PRAGMATIST (Vendor-dependent) |
| No visible response | No evidence despite JSCC requirement | UNKNOWN (concerning) |

---

## Peer Comparison (Japanese Banks)

After research, compare:

| Bank | Classification | JSCC Response | Confidence |
|------|---------------|---------------|------------|
| Nomura | [TBD] | [TBD] | [TBD] |
| MUFG | [TBD - Phase 3.2] | [TBD] | [TBD] |
| Mizuho | [TBD - Phase 3.3] | [TBD] | [TBD] |
| SMBC | [TBD - Phase 3.4] | [TBD] | [TBD] |

**Pattern Check:** Do Japanese banks show cohort behavior in JSCC response?

---

## Anchor Points

| Anchor | Fact | Check |
|--------|------|-------|
| JSCC | Production June 2025 | Nomura must have some connectivity response |
| BNP/JPM | Production before JSCC | Nomura cannot claim first |
| JFSA rules | Updated April 2024 | Regulatory context |

---

## Output Requirements

Complete:
1. /templates/per-bank-output.md (can abbreviate some sections for Tier B)
2. /templates/framework-integration.md

Save to:
- /outputs/phase-3/nomura-assessment.md
- /outputs/phase-3/nomura-integration.md

---

## Time Budget: 2-3 hours (Tier B Standard Protocol)

| Pass | Activity | Est. Time |
|------|----------|-----------|
| Pre-Research | Quick pre-mortem | 10 min |
| Pass 2 | All searches + abbreviated gates | 60-75 min |
| Pass 3 | Synthesis | 25-30 min |
| Adversarial | Abbreviated challenge | 15-20 min |
| Pass 5 | Quick cross-validation | 10 min |
| Pass 6 | Output | 20 min |
| **Total** | | **2-3 hours** |

---

## Success Criteria

1. [ ] JSCC response type determined
2. [ ] Classified with ≥50% confidence
3. [ ] Abbreviated adversarial completed
4. [ ] Comparable to other Japanese banks (consistency check pending Phase 3 completion)
5. [ ] Framework integration extract complete
