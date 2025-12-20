# Goldman Sachs Group, Inc. — CDM/DRR Research

## Bank Profile

| Attribute | Value |
|-----------|-------|
| **Full Name** | Goldman Sachs Group, Inc. |
| **Bank ID** | goldman-sachs |
| **Headquarters** | New York, USA |
| **Region** | North America (USA) |
| **Business Model** | Global investment bank |
| **Derivatives Relevance** | Very High — major derivatives dealer |
| **Primary Regulator** | Federal Reserve/SEC/CFTC |
| **Execution Tier** | A (Full Protocol) |

---

## Research Objective

**Primary Goal:** Assess if Goldman Sachs is following JPMorgan CDM path

**Framework Claim:** None established — discovery research

**Critical Context:** Goldman Sachs is one of the world's premier derivatives dealers. With JPMorgan in CDM production, the question is whether Goldman is:
1. Building similar capability (potential ARCHITECT)
2. Following via vendor path (PRAGMATIST)
3. Taking different strategic approach

**Hypothesis to Test:** Goldman Sachs as major derivatives dealer is likely ARCHITECT candidate

**Key Questions:**
1. Is Goldman Sachs building internal CDM capability?
2. Are there ISDA/FINOS contributions from Goldman Sachs?
3. How is Goldman Sachs addressing CFTC Rewrite?
4. Is there evidence of CDM pilot or production planning?
5. Is Goldman following, leading, or diverging from JPMorgan?

---

## Prior Probability Assessment

### Baseline Prior
- Goldman Sachs is derivatives-dominant investment bank
- Base P(ARCHITECT) = 25% (standard for derivatives-heavy banks)

### Contextual Adjustments

**Adjustment 1:** Derivatives Dominant
- Goldman Sachs is one of world's largest derivatives dealers
- Adjustment: +15% to P(Architect)
- Rationale: Derivatives dominance increases CDM relevance

**Adjustment 2:** US Peer in Production (JPMorgan)
- JPMorgan CDM production creates peer pressure
- Adjustment: +10% to P(Architect)
- Rationale: Competitive dynamics may drive similar investment

**Adjustment 3:** Technology Culture
- Goldman known for technology investment and proprietary systems
- Adjustment: +5% to P(Architect)
- Rationale: Internal build culture more likely

### Adjusted Priors
- **P(ARCHITECT) = 40%**
- P(PRAGMATIST) = 60%
- Prior Odds (Architect : Pragmatist) = 0.67

---

## Known Evidence

| Evidence | Source | Implication |
|----------|--------|-------------|
| JPMorgan (peer) in CDM production | Official announcement | Potential peer pressure |
| Major derivatives dealer | Industry position | High CDM relevance |
| Strong technology culture | Industry reputation | Internal build more likely |

---

## Pre-Mortem Analysis

### Failure Mode 1: Quiet Progress
**Hypothesis:** Goldman may be building CDM capability without public announcement (competitive secrecy).
- Probability this applies: 35%
- Mitigation: Search for indirect signals (hiring, vendor relationships, conference mentions)
- Implication: May need to infer from signals rather than official sources

### Failure Mode 2: Alternative Approach
**Hypothesis:** Goldman may be taking different technical approach (not standard CDM but achieving similar goals).
- Probability this applies: 20%
- Mitigation: Search for derivatives technology modernization that isn't labeled CDM
- Implication: Classification nuance needed

### Failure Mode 3: Vendor Strategy
**Hypothesis:** Goldman may be outsourcing CDM connectivity while maintaining proprietary core systems.
- Probability this applies: 25%
- Mitigation: Search for vendor relationships for regulatory reporting
- Implication: Would classify as PRAGMATIST despite derivatives dominance

### Anticipated Difficulty: MODERATE-HIGH
- Goldman is notoriously secretive about technology strategy
- May require significant inference from indirect signals

---

## Search Strategy

### Tier 1 Searches: Official Sources

**SEARCH 1.1:** Goldman Sachs "Common Domain Model" OR CDM production pilot
**SEARCH 1.2:** site:goldmansachs.com CDM OR "derivatives reporting" OR "regulatory technology"
**SEARCH 1.3:** site:isda.org "Goldman Sachs" CDM
**SEARCH 1.4:** site:finos.org "Goldman Sachs"
**SEARCH 1.5:** Goldman Sachs annual report 2024 "regulatory reporting" derivatives

### Reasoning Gate 1
[Complete standard Gate 1 assessment]

---

### Tier 2 Searches: Industry Sources

**SEARCH 2.1:** Goldman Sachs CDM 2024 2025 derivatives technology
**SEARCH 2.2:** Goldman Sachs CFTC reporting technology modernization
**SEARCH 2.3:** site:risk.net "Goldman Sachs" CDM OR derivatives reporting
**SEARCH 2.4:** site:waterstechnology.com "Goldman Sachs" derivatives technology
**SEARCH 2.5:** Goldman Sachs ISDA working group participation
**SEARCH 2.6:** Goldman Sachs derivatives technology transformation 2024

### Reasoning Gate 2
[Complete standard Gate 2 assessment]

---

### Tier 3 Searches: Indirect Signals

**SEARCH 3.1:** Goldman Sachs CDM job posting hiring
**SEARCH 3.2:** Goldman Sachs regulatory reporting technology partner vendor
**SEARCH 3.3:** Goldman Sachs derivatives operations technology investment
**SEARCH 3.4:** Goldman Sachs post-trade technology
**SEARCH 3.5:** [Named individual] Goldman Sachs CDM (if identified)

### Reasoning Gate 3
[Complete standard Gate 3 assessment]

---

## Observable Implications

### If ARCHITECT (Building CDM):
- [ ] ISDA/FINOS participation evidence
- [ ] CDM job postings
- [ ] Conference presentations on CDM/DRR
- [ ] Named individuals involved in CDM work
- [ ] Pilot or production announcements

### If PRAGMATIST (Vendor Path):
- [ ] Vendor partnership announcements
- [ ] Outsourced regulatory reporting evidence
- [ ] No CDM-specific hiring
- [ ] Focus on other technology priorities

---

## Adversarial Search Requirements

### Testing for ARCHITECT:
**ADVERSARIAL A1:** Goldman Sachs CDM "no plans" OR "not pursuing" OR "vendor solution"
**ADVERSARIAL A2:** Goldman Sachs derivatives reporting outsource vendor
**ADVERSARIAL A3:** Goldman Sachs CDM delayed postponed

### Testing for PRAGMATIST:
**ADVERSARIAL P1:** Goldman Sachs CDM production pilot announcement 2024 2025
**ADVERSARIAL P2:** Goldman Sachs FINOS contribution commit
**ADVERSARIAL P3:** Goldman Sachs CDM governance leadership ISDA

---

## Classification Decision Tree

```
Is there evidence of CDM production or pilot?
├── YES → ARCHITECT-Native or Leader
│   └── Check for: Announcement, timeline, scope
└── NO → Is there evidence of CDM capability building?
    ├── YES → ARCHITECT-Follower
    │   └── Check for: ISDA/FINOS contribution, hiring, named individuals
    └── NO → Is there evidence of vendor/outsource path?
        ├── YES → PRAGMATIST (Vendor-dependent)
        │   └── Check for: Vendor announcements, outsourcing
        └── NO → Insufficient evidence
            └── Classify based on balance of signals
```

---

## Peer Comparison

| Peer | Classification | Goldman Comparison Point |
|------|----------------|-------------------------|
| JPMorgan | ARCHITECT-Native | Primary US peer - in production |
| Morgan Stanley | TBD | Co-assess in Phase 8 |
| BNP Paribas | ARCHITECT-Native | European benchmark |
| Deutsche Bank | PRAGMATIST | Similar size, different approach |

---

## Output Requirements

Save outputs to:
- `outputs/phase-8-us-investment-banks/goldman-sachs/1-evidence/`
- `outputs/phase-8-us-investment-banks/goldman-sachs/2-bayesian/`
- `outputs/phase-8-us-investment-banks/goldman-sachs/3-gates/`
- `outputs/phase-8-us-investment-banks/goldman-sachs/4-adversarial/`
- `outputs/phase-8-us-investment-banks/goldman-sachs/5-synthesis/`

---

## Time Budget

| Activity | Est. Time |
|----------|-----------|
| Tier 1 searches + Gate 1 | 60 min |
| Tier 2 searches + Gate 2 | 60 min |
| Tier 3 searches + Gate 3 | 45 min |
| Adversarial challenge | 45 min |
| Synthesis | 30 min |
| **Total** | **~4-4.5 hours** |

---

## Success Criteria

1. [ ] Classification determined (ARCHITECT vs PRAGMATIST)
2. [ ] If ARCHITECT, sub-classification determined
3. [ ] JPMorgan peer comparison documented
4. [ ] Technology strategy direction understood
5. [ ] CFTC Rewrite response assessed
