# UBS Group — CDM/DRR Research

## Bank Profile

| Attribute | Value |
|-----------|-------|
| **Full Name** | UBS Group AG |
| **Headquarters** | Zurich, Switzerland |
| **Region** | Europe (Switzerland) |
| **Business Model** | Global wealth manager with significant investment bank |
| **Derivatives Relevance** | High — major derivatives dealer (expanded post-CS acquisition) |
| **Execution Tier** | A (Full Protocol) |

---

## Research Objective

**Primary Goal:** Determine if Credit Suisse integration is consuming all CDM capacity or if UBS has parallel CDM initiatives

**Critical Context:** UBS acquired Credit Suisse in June 2023. Integration projected through 2026, with ~90% complete as of October 2024. This is the largest banking merger in decades.

**Key Questions:**
1. Is there ANY evidence of CDM work despite the integration?
2. Did Credit Suisse have CDM initiatives that UBS inherited?
3. What are FINMA requirements for derivatives reporting?
4. When will integration capacity constraints free up?
5. What is UBS's post-integration technology strategy for derivatives?

---

## Hypothesis to Test

**H-INTEGRATION:** "Credit Suisse integration is consuming all CDM investment capacity through 2026"

- **Confirming evidence:** No CDM announcements, technology focus on integration, explicit statements about post-integration plans
- **Disconfirming evidence:** CDM pilot/production despite integration, inherited CS capability, parallel initiatives

---

## Prior Probability Assessment

### Base Priors
- P(ARCHITECT-Native) = 5%
- P(ARCHITECT-Leader) = 10%
- P(ARCHITECT-Follower) = 15%
- P(PRAGMATIST) = 70%

### Contextual Adjustments

**Adjustment 1:** Major derivatives business
- Combined UBS+CS is massive derivatives dealer
- Adjustment: +10% to P(Architect)

**Adjustment 2:** Credit Suisse integration
- Largest banking integration in decades
- All technology capacity diverted to integration
- Adjustment: +20% to P(Pragmatist)
- Rationale: Capacity constraints override business case

**Adjustment 3:** Swiss regulatory environment
- FINMA is sophisticated but Switzerland not subject to EMIR
- Adjustment: +5% to P(Pragmatist)
- Rationale: Less regulatory pressure than EU peers

**Adjustment 4:** Potential inherited capability
- Credit Suisse may have had CDM work
- Adjustment: +5% to P(Architect)
- Rationale: Unknown CS legacy

### Adjusted Priors (Starting Point)
- P(ARCHITECT-Native) = 4%
- P(ARCHITECT-Leader) = 6%
- P(ARCHITECT-Follower) = 15%
- P(PRAGMATIST) = 75%
- **P(ARCHITECT total) = 25%**
- **Prior Odds (Architect : Pragmatist) = 0.33**

**Note:** Lower Architect prior due to known integration constraints.

---

## Pre-Mortem Analysis

### Failure Mode 1: Integration Noise
**Hypothesis:** All UBS technology coverage focuses on integration, making CDM work invisible even if it exists.

- Probability this applies: 45%
- Mitigation: Search specifically for derivatives technology separate from integration
- Fallback: If integration dominates all coverage, classify as Integration-constrained Pragmatist

### Failure Mode 2: Credit Suisse Gap
**Hypothesis:** Credit Suisse may have had CDM work that transferred to UBS, but we won't find it because CS is no longer a separate entity.

- Probability this applies: 30%
- Mitigation: Search historical CS CDM coverage; search for "inherited" or "legacy" CS systems at UBS
- Red flag: Finding CS CDM work with no indication of continuation

### Failure Mode 3: Swiss Privacy
**Hypothesis:** Swiss banking culture emphasizes discretion; UBS may be engaged without public disclosure.

- Probability this applies: 25%
- Mitigation: Search for indirect signals (ISDA/FINOS participation, job postings)
- Implication: May need to rely on inference more than direct evidence

### Failure Mode 4: False Capacity Assumption
**Hypothesis:** I may assume integration prevents all CDM work, when large banks can pursue multiple priorities.

- Probability this applies: 35%
- Mitigation: Actively search for evidence of CDM despite integration
- Commitment: Don't let integration narrative override actual evidence

### Anticipated Difficulty: MODERATE-DIFFICULT
- Integration narrative may dominate
- Credit Suisse legacy is unknown
- Swiss discretion may limit visibility

---

## Search Strategy

### Tier 1 Searches: Official Sources

**SEARCH 1.1:** UBS "Common Domain Model" OR CDM derivatives 2024 2025
**SEARCH 1.2:** UBS "Digital Regulatory Reporting" ISDA
**SEARCH 1.3:** UBS annual report 2024 "regulatory reporting" derivatives technology
**SEARCH 1.4:** UBS investor presentation 2024 technology transformation
**SEARCH 1.5:** "Credit Suisse" CDM OR "Common Domain Model" (historical, pre-acquisition)

### Reasoning Gate 1
[Complete /templates/reasoning-gates.md Gate 1]

---

### Tier 2 Searches: Industry Sources

**SEARCH 2.1:** UBS integration technology derivatives systems 2024 2025
**SEARCH 2.2:** UBS FINMA derivatives reporting requirements
**SEARCH 2.3:** UBS post-integration technology strategy
**SEARCH 2.4:** UBS ISDA AGM speaker CDM DRR
**SEARCH 2.5:** UBS Risk.net OR "Waters Technology" derivatives 2024
**SEARCH 2.6:** "Credit Suisse" integration UBS derivatives technology

### Reasoning Gate 2
[Complete /templates/reasoning-gates.md Gate 2]

---

### Tier 3 Searches: Indirect Signals

**SEARCH 3.1:** UBS FINOS member contributor
**SEARCH 3.2:** UBS job posting CDM OR DRR OR "regulatory reporting"
**SEARCH 3.3:** UBS vendor derivatives technology partner
**SEARCH 3.4:** UBS derivatives reporting vendor outsource
**SEARCH 3.5:** UBS vs Deutsche Bank vs Barclays derivatives technology comparison

### Reasoning Gate 3
[Complete /templates/reasoning-gates.md Gate 3]

---

## Integration Timeline Context

### Key Dates
| Date | Event | CDM Implication |
|------|-------|-----------------|
| June 2023 | CS acquisition closes | Integration begins |
| October 2024 | ~90% integration complete | Major systems integrated |
| 2025 | Integration continuation | Some capacity returning |
| 2026 | Integration projected complete | Capacity fully available |

### Integration Impact Assessment
- Pre-2024: No expectation of CDM work
- 2024-2025: Limited capacity, only if strategic priority
- 2026+: Capacity available for new initiatives

If evidence of CDM work found, it indicates STRONG commitment (pursuing despite constraints).

---

## Credit Suisse Legacy Analysis

### What to Look For
- Any pre-acquisition CS CDM work
- Whether CS work was continued, paused, or abandoned
- Named individuals who worked on CS derivatives tech now at UBS

### Evidence Interpretation
| CS CDM Evidence | UBS Continuation Evidence | Classification |
|-----------------|---------------------------|----------------|
| None | None | PRAGMATIST (Integration-constrained) |
| Found | None | PRAGMATIST (abandoned CS work) |
| Found | Found | ARCHITECT (inherited and continuing) |
| None | Found | ARCHITECT (new UBS initiative) |

---

## Adversarial Search Requirements

### If Leaning PRAGMATIST (Integration):

**ADVERSARIAL P1:** UBS CDM pilot OR initiative despite integration
**ADVERSARIAL P2:** UBS derivatives technology investment 2024 2025 (not integration)
**ADVERSARIAL P3:** UBS ISDA CDM working group participant

### If Leaning ARCHITECT:

**ADVERSARIAL A1:** UBS CDM "delayed" OR "postponed" OR "post-integration"
**ADVERSARIAL A2:** UBS technology focus integration "derivatives reporting" deprioritized
**ADVERSARIAL A3:** UBS vendor outsource derivatives reporting

---

## Classification Decision Tree

```
Is there evidence of current CDM work (2024-2025)?
├── YES → Is it despite integration constraints?
│   ├── YES → ARCHITECT (strong signal, pursuing despite constraints)
│   └── NO → Cannot determine (unlikely given timeline)
└── NO → Is there evidence of Credit Suisse CDM legacy?
    ├── YES → Was it continued?
    │   ├── YES → ARCHITECT-Follower (inherited capability)
    │   └── NO → PRAGMATIST (abandoned, integration priority)
    └── NO → PRAGMATIST (Integration-constrained)
```

---

## Anchor Points

| Anchor | Fact | Check |
|--------|------|-------|
| CS Acquisition | June 2023 | Integration timeline starts here |
| Integration 90% | October 2024 | Major capacity constraint |
| BNP Production | 2022 | UBS cannot claim earlier |
| FINMA | Swiss regulator | Different from EMIR regime |

---

## Peer Comparison

| Peer | Classification | UBS Should Be... |
|------|----------------|------------------|
| Deutsche Bank | TBD | Similar unless integration explains difference |
| Barclays | ARCHITECT-Follower | Behind if integration constrains |
| SocGen | TBD | Similar derivatives exposure |

---

## Output Requirements

Complete:
1. /templates/per-bank-output.md
2. /templates/framework-integration.md

**Special Output Section:** Credit Suisse Legacy Analysis
- Document any CS CDM evidence found
- Note whether continued or abandoned
- Implications for post-integration UBS

Save to:
- /outputs/phase-1/ubs-assessment.md
- /outputs/phase-1/ubs-integration.md

---

## Time Budget: 4-5 hours (Full Protocol)

---

## Success Criteria

1. [ ] Integration hypothesis tested with evidence
2. [ ] Credit Suisse legacy investigated
3. [ ] Classification accounts for capacity constraints
4. [ ] Post-integration trajectory noted
5. [ ] Framework integration extract complete
