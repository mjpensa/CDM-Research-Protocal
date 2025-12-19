# Barclays PLC — CDM/DRR Research

## Bank Profile

| Attribute | Value |
|-----------|-------|
| **Full Name** | Barclays PLC |
| **Headquarters** | London, UK |
| **Region** | UK |
| **Business Model** | Universal bank with significant investment banking |
| **Derivatives Relevance** | High — major derivatives dealer |
| **Execution Tier** | A (Full Protocol) |

---

## Research Objective

**Primary Goal:** Determine if Barclays is progressing from Follower toward Leader status

**Critical Context:** Barclays is a CONFIRMED CDM contributor (FINOS). The question is not WHETHER they're engaged, but HOW DEEPLY and whether they're moving toward production.

**Starting Position:** ARCHITECT-Follower (baseline established)

**Key Questions:**
1. Is Barclays moving toward production commitment?
2. What is the scope and depth of their FINOS contribution?
3. Have they demonstrated production-grade capabilities?
4. Are they taking governance/leadership roles in CDM ecosystem?
5. What is their UK EMIR response strategy?

---

## Known Evidence (Pre-Research)

| Evidence | Source | Date | Implication |
|----------|--------|------|-------------|
| FINOS contributor | FINOS public records | Ongoing | Confirmed Follower baseline |
| Prototype demonstrated | Industry event | Historical | Technical capability |
| 2018 BOE/FCA DRR pilot participant | UK regulator | 2018 | Early engagement |

**Starting Classification:** ARCHITECT-Follower
**Research Objective:** Determine if upgrade to Leader is warranted

---

## Upgrade Criteria: Follower → Leader

To upgrade Barclays to ARCHITECT-Leader, need evidence of:

| Criterion | Required Evidence | Found? |
|-----------|-------------------|--------|
| Production commitment | Announced production timeline or go-live | [ ] |
| Expanded contribution | Beyond basic FINOS participation | [ ] |
| Governance leadership | Working group chair, steering committee | [ ] |
| Production demonstration | Live system shown, not just prototype | [ ] |
| Public commitment | Executive-level CDM endorsement | [ ] |

**Upgrade threshold:** ≥3 of 5 criteria with Tier 1/2 evidence

---

## Prior Probability Assessment

### Adjusted Priors (Given Known Evidence)

Because Barclays is a CONFIRMED contributor, priors are different:

- P(ARCHITECT-Native) = 10% (would require production confirmation)
- P(ARCHITECT-Leader) = 35% (upgrade from Follower)
- P(ARCHITECT-Follower) = 50% (maintain current position)
- P(PRAGMATIST) = 5% (would require evidence of withdrawal)
- **P(Leader or higher) = 45%**
- **Prior Odds (Leader+ : Follower or below) = 0.82**

---

## Pre-Mortem Analysis

### Failure Mode 1: Contribution Stagnation
**Hypothesis:** FINOS contribution may be historical with no recent activity. "Contributor" status may be outdated.

- Probability this applies: 25%
- Mitigation: Search for recent contribution evidence (2024-2025)
- Implication: If stagnant, maintain Follower but note trajectory as STALLED

### Failure Mode 2: Quiet Progress
**Hypothesis:** Barclays may be progressing toward production without public announcement.

- Probability this applies: 30%
- Mitigation: Search for indirect production signals (hiring, vendor tooling, internal systems mentions)
- Implication: May need to infer trajectory from signals

### Failure Mode 3: UK Regulatory Focus
**Hypothesis:** UK EMIR (September 2024) may have changed Barclays' approach — they may be solving UK-specific requirements differently.

- Probability this applies: 20%
- Mitigation: Search specifically for UK EMIR response
- Implication: UK-specific approach doesn't preclude CDM engagement

### Anticipated Difficulty: MODERATE
- Baseline established, question is trajectory
- UK focus may provide different angle than EU banks

---

## Search Strategy

### Tier 1 Searches: Official Sources

**SEARCH 1.1:** Barclays "Common Domain Model" OR CDM production 2024 2025
**SEARCH 1.2:** Barclays "Digital Regulatory Reporting" announcement pilot
**SEARCH 1.3:** site:finos.org Barclays CDM contribution 2024 2025
**SEARCH 1.4:** Barclays annual report 2024 "regulatory reporting" derivatives
**SEARCH 1.5:** Barclays investor presentation 2024 technology derivatives

### Reasoning Gate 1
[Complete /templates/reasoning-gates.md Gate 1]

---

### Tier 2 Searches: Industry Sources

**SEARCH 2.1:** Barclays CDM production timeline go-live
**SEARCH 2.2:** Barclays "UK EMIR" implementation technology
**SEARCH 2.3:** Barclays ISDA AGM CDM speaker 2024 2025
**SEARCH 2.4:** Barclays Risk.net OR "Waters Technology" CDM 2024
**SEARCH 2.5:** Barclays ISDA working group CDM chair leadership
**SEARCH 2.6:** Barclays derivatives technology transformation

### Reasoning Gate 2
[Complete /templates/reasoning-gates.md Gate 2]

---

### Tier 3 Searches: Indirect Signals

**SEARCH 3.1:** Barclays CDM job posting hiring engineer
**SEARCH 3.2:** Barclays FINOS GitHub contribution commits
**SEARCH 3.3:** Barclays vendor CDM tooling partner
**SEARCH 3.4:** Barclays post-trade technology investment
**SEARCH 3.5:** [Named individual] Barclays CDM (if identified)

### Reasoning Gate 3
[Complete /templates/reasoning-gates.md Gate 3]

---

## Contribution Depth Assessment

### FINOS Contribution Analysis
- [ ] Named in contributor list (baseline confirmed)
- [ ] Specific modules/components contributed
- [ ] Commit frequency and recency
- [ ] Named individuals on commits
- [ ] Working group participation
- [ ] Steering/governance roles

### Contribution Classification
| Level | Evidence | Classification |
|-------|----------|----------------|
| Nominal | Listed as contributor, no recent activity | Follower (stalled) |
| Active | Recent commits, working group participation | Follower (active) |
| Leadership | Governance role, significant code contribution | Leader candidate |

---

## UK Regulatory Context

### Key Milestones
- September 2024: UK EMIR Refit effective
- FCA/BOE: UK-specific reporting requirements
- 2018: Barclays participated in UK DRR pilot

### Research Questions
- How did Barclays address UK EMIR?
- Did UK EMIR accelerate or delay CDM timeline?
- Is UK approach coordinated with EU/global CDM?

---

## Adversarial Search Requirements

### Testing for Upgrade (Leader):

**ADVERSARIAL L1:** Barclays CDM "no production" OR "evaluation only" OR delayed
**ADVERSARIAL L2:** Barclays vendor solution derivatives reporting (outsource signal)
**ADVERSARIAL L3:** Barclays CDM contribution "reduced" OR "paused"

### Testing for Downgrade (Stalled):

**ADVERSARIAL D1:** Barclays CDM production 2025 announcement
**ADVERSARIAL D2:** Barclays FINOS governance leadership 2024 2025
**ADVERSARIAL D3:** Barclays executive CDM commitment speech

---

## Classification Decision Tree

```
Is there evidence of production commitment?
├── YES → ARCHITECT-Leader (upgrade confirmed)
│   └── Check for: Timeline, announcement, executive commitment
└── NO → Is contribution active and expanding?
    ├── YES → ARCHITECT-Follower (active, trajectory: ACCELERATING)
    │   └── Check for: Recent commits, working group, hiring
    ├── SOMEWHAT → ARCHITECT-Follower (stable)
    │   └── Evidence of continued but not expanded engagement
    └── NO → ARCHITECT-Follower (stalled, trajectory: STALLED)
        └── No recent contribution evidence
```

---

## Anchor Points

| Anchor | Fact | Check |
|--------|------|-------|
| FINOS Contributor | Confirmed | Cannot downgrade below Follower without withdrawal evidence |
| 2018 DRR Pilot | Historical | Early engagement established |
| UK EMIR | September 2024 | Must have addressed |
| BNP Production | 2022 | Barclays cannot claim first |
| Standard Chartered | Confirmed contributor | Peer comparison for Follower bar |

---

## Peer Comparison

| Peer | Classification | Barclays Should Be... |
|------|----------------|----------------------|
| BNP Paribas | ARCHITECT-Native | Behind (no production) |
| Standard Chartered | ARCHITECT-Follower | Same tier (both confirmed contributors) |
| HSBC | TBD | Compare UK bank approaches |
| Deutsche Bank | TBD | Compare engagement depth |

---

## Output Requirements

Complete:
1. /templates/per-bank-output.md
2. /templates/framework-integration.md

**Special Output Section:** Upgrade Assessment
- Explicit assessment against 5 upgrade criteria
- Evidence for/against each criterion
- Recommendation: Maintain Follower / Upgrade to Leader

Save to:
- /outputs/phase-1/barclays-assessment.md
- /outputs/phase-1/barclays-integration.md

---

## Time Budget: 4-5 hours (Tier A Full Protocol)

---

## Success Criteria

1. [ ] Contribution depth assessed (not just presence)
2. [ ] Upgrade criteria explicitly evaluated
3. [ ] UK EMIR response documented
4. [ ] Trajectory (accelerating/stable/stalled) determined
5. [ ] Framework integration extract complete with upgrade recommendation
