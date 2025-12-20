# Citigroup Inc. — CDM/DRR Research

## Bank Profile

| Attribute | Value |
|-----------|-------|
| **Full Name** | Citigroup Inc. |
| **Bank ID** | citigroup |
| **Headquarters** | New York, USA |
| **Region** | North America (USA) |
| **Business Model** | Global universal bank |
| **Derivatives Relevance** | High |
| **Primary Regulator** | OCC/Federal Reserve/SEC/CFTC |
| **Execution Tier** | B (Abbreviated Protocol) |

---

## Research Objective

**Primary Goal:** Assess Citigroup CDM positioning

**Framework Claim:** None established — discovery research

**Critical Context:** Citigroup is a global universal bank with significant but not dominant derivatives business. Unlike Goldman Sachs or Morgan Stanley, Citigroup has broader retail and commercial banking operations. The question is whether the derivatives business justifies internal CDM investment or if vendor path is more likely.

**Hypothesis to Test:** Citigroup may follow vendor path despite derivatives exposure given universal bank model

**Key Questions:**
1. Is Citigroup building internal CDM capability?
2. Are there ISDA/FINOS contributions from Citigroup?
3. How is Citigroup addressing CFTC Rewrite?
4. Is vendor path more likely given universal bank model?
5. How does ongoing strategic restructuring affect technology priorities?

---

## Prior Probability Assessment

### Baseline Prior
- Citigroup is universal bank with significant derivatives
- Base P(ARCHITECT) = 25%

### Contextual Adjustments

**Adjustment 1:** Significant Derivatives Business
- Citigroup has major trading and markets operation
- Adjustment: +10% to P(Architect)
- Rationale: Derivatives exposure creates CDM relevance

**Adjustment 2:** US Peer in Production (JPMorgan)
- JPMorgan CDM production creates peer pressure
- Adjustment: +5% to P(Architect)
- Rationale: Peer pressure but different business model

**Adjustment 3:** Strategic Restructuring
- Citigroup has been simplifying/restructuring operations
- Adjustment: -5% to P(Architect)
- Rationale: Technology investment may be constrained

**Adjustment 4:** Universal Bank Complexity
- Broader business model may favor vendor solutions
- Adjustment: -5% to P(Architect)
- Rationale: Less derivatives-focused than pure investment banks

### Adjusted Priors
- **P(ARCHITECT) = 25%**
- P(PRAGMATIST) = 75%
- Prior Odds (Architect : Pragmatist) = 0.33

---

## Known Evidence

| Evidence | Source | Implication |
|----------|--------|-------------|
| JPMorgan (peer) in CDM production | Official announcement | Potential peer pressure |
| Major markets business | Industry position | Derivatives relevance |
| Ongoing restructuring | Public announcements | Competing priorities |

---

## Pre-Mortem Analysis

### Failure Mode 1: Restructuring Priority
**Hypothesis:** Ongoing strategic simplification may be consuming technology capacity.
- Probability this applies: 30%
- Mitigation: Search for derivatives-specific technology initiatives
- Implication: May defer CDM to vendor

### Failure Mode 2: Following Larger Peers
**Hypothesis:** Citigroup may wait to see Goldman/Morgan Stanley approach before committing.
- Probability this applies: 25%
- Mitigation: Search for Citi-specific timeline
- Implication: May be later adopter

### Anticipated Difficulty: MODERATE
- Universal bank model provides multiple technology priorities
- Restructuring adds complexity to analysis

---

## Search Strategy

### Tier 1 Searches: Official Sources

**SEARCH 1.1:** Citigroup "Common Domain Model" OR CDM production pilot
**SEARCH 1.2:** site:citigroup.com CDM OR "derivatives reporting" OR "regulatory technology"
**SEARCH 1.3:** site:isda.org Citigroup CDM
**SEARCH 1.4:** site:finos.org Citigroup
**SEARCH 1.5:** Citigroup annual report 2024 "regulatory reporting" derivatives

### Reasoning Gate 1
[Complete standard Gate 1 assessment]

---

### Tier 2 Searches: Industry Sources

**SEARCH 2.1:** Citigroup CDM 2024 2025 derivatives technology
**SEARCH 2.2:** Citigroup CFTC reporting technology
**SEARCH 2.3:** site:risk.net Citigroup CDM OR derivatives reporting
**SEARCH 2.4:** Citigroup markets technology transformation
**SEARCH 2.5:** Citigroup ISDA working group

### Reasoning Gate 2
[Complete standard Gate 2 assessment]

---

### Tier 3 Searches: Indirect Signals

**SEARCH 3.1:** Citigroup CDM job posting
**SEARCH 3.2:** Citigroup regulatory reporting vendor partner
**SEARCH 3.3:** Citigroup derivatives operations technology

### Reasoning Gate 3
[Complete standard Gate 3 assessment]

---

## Observable Implications

### If ARCHITECT:
- [ ] ISDA/FINOS participation evidence
- [ ] CDM job postings
- [ ] Pilot or production announcements

### If PRAGMATIST:
- [ ] Vendor partnership announcements
- [ ] Outsourced regulatory reporting evidence
- [ ] Focus on other technology priorities

---

## Classification Decision Tree

```
Is there evidence of CDM production or pilot?
├── YES → ARCHITECT
└── NO → Is there evidence of CDM capability building?
    ├── YES → ARCHITECT-Follower
    └── NO → PRAGMATIST (Vendor-dependent)
```

---

## Peer Comparison

| Peer | Classification | Citigroup Comparison Point |
|------|----------------|---------------------------|
| JPMorgan | ARCHITECT-Native | US peer, more derivatives-focused |
| Bank of America | TBD | Similar universal bank model |
| HSBC | PRAGMATIST | Similar global universal bank |
| Deutsche Bank | PRAGMATIST | Similar restructuring context |

---

## Output Requirements

Save outputs to:
- `outputs/phase-8-us-investment-banks/citigroup/1-evidence/`
- `outputs/phase-8-us-investment-banks/citigroup/2-bayesian/`
- `outputs/phase-8-us-investment-banks/citigroup/3-gates/`
- `outputs/phase-8-us-investment-banks/citigroup/4-adversarial/`
- `outputs/phase-8-us-investment-banks/citigroup/5-synthesis/`

---

## Time Budget

| Activity | Est. Time |
|----------|-----------|
| Tier 1 searches + Gate 1 | 45 min |
| Tier 2 searches + Gate 2 | 45 min |
| Tier 3 searches (if needed) | 30 min |
| Adversarial (Abbreviated) | 30 min |
| Synthesis | 30 min |
| **Total** | **~3 hours** |

---

## Success Criteria

1. [ ] Classification determined (ARCHITECT vs PRAGMATIST)
2. [ ] Restructuring impact on CDM assessed
3. [ ] Universal bank vs investment bank comparison documented
4. [ ] CFTC Rewrite response assessed
