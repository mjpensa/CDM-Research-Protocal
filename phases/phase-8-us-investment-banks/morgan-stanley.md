# Morgan Stanley — CDM/DRR Research

## Bank Profile

| Attribute | Value |
|-----------|-------|
| **Full Name** | Morgan Stanley |
| **Bank ID** | morgan-stanley |
| **Headquarters** | New York, USA |
| **Region** | North America (USA) |
| **Business Model** | Global investment bank and wealth management |
| **Derivatives Relevance** | Very High — major derivatives dealer |
| **Primary Regulator** | Federal Reserve/SEC/CFTC |
| **Execution Tier** | A (Full Protocol) |

---

## Research Objective

**Primary Goal:** Assess if Morgan Stanley is following JPMorgan CDM path

**Framework Claim:** None established — discovery research

**Critical Context:** Morgan Stanley combines major derivatives dealing with significant wealth management business. This hybrid model may influence CDM strategy differently than pure investment banks. With JPMorgan in CDM production, the question is Morgan Stanley's response.

**Hypothesis to Test:** Morgan Stanley as major derivatives dealer is likely ARCHITECT candidate

**Key Questions:**
1. Is Morgan Stanley building internal CDM capability?
2. Are there ISDA/FINOS contributions from Morgan Stanley?
3. How is Morgan Stanley addressing CFTC Rewrite?
4. Is there evidence of CDM pilot or production planning?
5. Does wealth management focus affect derivatives technology priorities?

---

## Prior Probability Assessment

### Baseline Prior
- Morgan Stanley is derivatives-dominant investment bank with wealth management
- Base P(ARCHITECT) = 25%

### Contextual Adjustments

**Adjustment 1:** Derivatives Dominant (Investment Bank Side)
- Morgan Stanley institutional securities is major derivatives dealer
- Adjustment: +15% to P(Architect)
- Rationale: Derivatives business creates CDM relevance

**Adjustment 2:** US Peer in Production (JPMorgan)
- JPMorgan CDM production creates peer pressure
- Adjustment: +10% to P(Architect)
- Rationale: Competitive dynamics

**Adjustment 3:** Wealth Management Dilution
- E*TRADE acquisition and wealth management growth
- Adjustment: -5% to P(Architect)
- Rationale: Competing technology priorities, less derivatives-focused overall

### Adjusted Priors
- **P(ARCHITECT) = 35%**
- P(PRAGMATIST) = 65%
- Prior Odds (Architect : Pragmatist) = 0.54

---

## Known Evidence

| Evidence | Source | Implication |
|----------|--------|-------------|
| JPMorgan (peer) in CDM production | Official announcement | Potential peer pressure |
| Major derivatives dealer | Industry position | High CDM relevance |
| E*TRADE acquisition | Public knowledge | Wealth management focus growing |

---

## Pre-Mortem Analysis

### Failure Mode 1: Wealth Management Priority
**Hypothesis:** E*TRADE integration and wealth management growth may be consuming technology capacity.
- Probability this applies: 25%
- Mitigation: Search for derivatives-specific technology initiatives
- Implication: May follow vendor path for derivatives despite dealer status

### Failure Mode 2: Following Goldman Not JPMorgan
**Hypothesis:** Morgan Stanley may be watching Goldman Sachs rather than directly following JPMorgan.
- Probability this applies: 20%
- Mitigation: Search for MS-specific timeline and strategy
- Implication: May have longer decision timeline

### Failure Mode 3: Hybrid Approach
**Hypothesis:** Morgan Stanley may use CDM for institutional but vendor for wealth management.
- Probability this applies: 20%
- Mitigation: Search for business-line specific technology strategy
- Implication: Classification nuance needed

### Anticipated Difficulty: MODERATE-HIGH
- Similar to Goldman, Morgan Stanley is relatively secretive
- Hybrid business model complicates analysis

---

## Search Strategy

### Tier 1 Searches: Official Sources

**SEARCH 1.1:** Morgan Stanley "Common Domain Model" OR CDM production pilot
**SEARCH 1.2:** site:morganstanley.com CDM OR "derivatives reporting" OR "regulatory technology"
**SEARCH 1.3:** site:isda.org "Morgan Stanley" CDM
**SEARCH 1.4:** site:finos.org "Morgan Stanley"
**SEARCH 1.5:** Morgan Stanley annual report 2024 "regulatory reporting" derivatives

### Reasoning Gate 1
[Complete standard Gate 1 assessment]

---

### Tier 2 Searches: Industry Sources

**SEARCH 2.1:** Morgan Stanley CDM 2024 2025 derivatives technology
**SEARCH 2.2:** Morgan Stanley CFTC reporting technology modernization
**SEARCH 2.3:** site:risk.net "Morgan Stanley" CDM OR derivatives reporting
**SEARCH 2.4:** site:waterstechnology.com "Morgan Stanley" derivatives technology
**SEARCH 2.5:** Morgan Stanley ISDA working group participation
**SEARCH 2.6:** Morgan Stanley institutional securities technology transformation

### Reasoning Gate 2
[Complete standard Gate 2 assessment]

---

### Tier 3 Searches: Indirect Signals

**SEARCH 3.1:** Morgan Stanley CDM job posting hiring
**SEARCH 3.2:** Morgan Stanley regulatory reporting technology partner vendor
**SEARCH 3.3:** Morgan Stanley derivatives operations technology investment
**SEARCH 3.4:** Morgan Stanley post-trade technology
**SEARCH 3.5:** [Named individual] Morgan Stanley CDM (if identified)

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
- [ ] Institutional Securities specific initiatives

### If PRAGMATIST (Vendor Path):
- [ ] Vendor partnership announcements
- [ ] Outsourced regulatory reporting evidence
- [ ] No CDM-specific hiring
- [ ] Focus on wealth management technology

---

## Adversarial Search Requirements

### Testing for ARCHITECT:
**ADVERSARIAL A1:** Morgan Stanley CDM "no plans" OR "not pursuing" OR "vendor solution"
**ADVERSARIAL A2:** Morgan Stanley derivatives reporting outsource vendor
**ADVERSARIAL A3:** Morgan Stanley technology focus "wealth management" NOT derivatives

### Testing for PRAGMATIST:
**ADVERSARIAL P1:** Morgan Stanley CDM production pilot announcement 2024 2025
**ADVERSARIAL P2:** Morgan Stanley FINOS contribution commit
**ADVERSARIAL P3:** Morgan Stanley CDM governance leadership ISDA

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

| Peer | Classification | Morgan Stanley Comparison Point |
|------|----------------|--------------------------------|
| JPMorgan | ARCHITECT-Native | Primary US peer - in production |
| Goldman Sachs | TBD | Direct competitor comparison |
| UBS | ARCHITECT | Similar hybrid model (investment + wealth) |
| Pictet | ARCHITECT-Native | Wealth management comparison |

---

## Output Requirements

Save outputs to:
- `outputs/phase-8-us-investment-banks/morgan-stanley/1-evidence/`
- `outputs/phase-8-us-investment-banks/morgan-stanley/2-bayesian/`
- `outputs/phase-8-us-investment-banks/morgan-stanley/3-gates/`
- `outputs/phase-8-us-investment-banks/morgan-stanley/4-adversarial/`
- `outputs/phase-8-us-investment-banks/morgan-stanley/5-synthesis/`

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
3. [ ] Wealth management impact on strategy assessed
4. [ ] Goldman Sachs / JPMorgan peer comparison documented
5. [ ] CFTC Rewrite response assessed
