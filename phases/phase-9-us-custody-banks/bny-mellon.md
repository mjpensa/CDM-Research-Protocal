# The Bank of New York Mellon Corporation — CDM/DRR Research

## Bank Profile

| Attribute | Value |
|-----------|-------|
| **Full Name** | The Bank of New York Mellon Corporation |
| **Bank ID** | bny-mellon |
| **Headquarters** | New York, USA |
| **Region** | North America (USA) |
| **Business Model** | Custody bank and asset servicing |
| **Derivatives Relevance** | Medium |
| **Primary Regulator** | Federal Reserve/SEC |
| **Execution Tier** | C (Rapid Assessment) |

---

## Research Objective

**Primary Goal:** Assess custody bank CDM positioning

**Framework Claim:** None established — discovery research

**Critical Context:** BNY Mellon is one of the world's largest custody banks and a major provider of financial market infrastructure services. Unlike investment banks, BNY Mellon's primary business is asset servicing, custody, and market infrastructure. CDM relevance may come from:
1. Client service offerings
2. Market infrastructure role (clearing, settlement)
3. Processing client derivatives activity

**Hypothesis to Test:** Custody banks may have different CDM drivers than investment banks

**Key Questions:**
1. Does custody/asset servicing drive different CDM motivation?
2. Is BNY Mellon building CDM capability for client servicing?
3. How does CFTC Rewrite affect custody bank derivatives operations?
4. Is there a market infrastructure angle given BNY Mellon's clearing/settlement role?

---

## Prior Probability Assessment

### Baseline Prior
- BNY Mellon is custody bank with market infrastructure role
- Base P(ARCHITECT) = 25%

### Contextual Adjustments

**Adjustment 1:** Non-Derivatives Core Business
- Custody/asset servicing is core, not derivatives trading
- Adjustment: -10% to P(Architect)
- Rationale: Lower CDM relevance than dealers

**Adjustment 2:** Market Infrastructure Role
- BNY Mellon has clearing and settlement operations
- Adjustment: +5% to P(Architect)
- Rationale: Infrastructure role may drive CDM interest

**Adjustment 3:** Client Service Potential
- May offer CDM services to institutional clients
- Adjustment: +5% to P(Architect)
- Rationale: Client service could drive investment

### Adjusted Priors
- **P(ARCHITECT) = 15%**
- P(PRAGMATIST) = 85%
- Prior Odds (Architect : Pragmatist) = 0.18

---

## Search Strategy (Rapid Assessment)

### Tier 1-2 Combined Searches

**SEARCH 1:** "BNY Mellon" "Common Domain Model" OR CDM production pilot
**SEARCH 2:** site:bnymellon.com CDM OR "derivatives reporting" OR "regulatory technology"
**SEARCH 3:** site:isda.org "BNY Mellon" CDM
**SEARCH 4:** "BNY Mellon" CDM 2024 2025 derivatives custody
**SEARCH 5:** "BNY Mellon" CFTC derivatives reporting clearing settlement
**SEARCH 6:** "BNY Mellon" market infrastructure CDM derivatives

---

## Observable Implications

### If ARCHITECT (Infrastructure/Client Service):
- [ ] CDM client service offerings
- [ ] Market infrastructure CDM role
- [ ] Clearing/settlement CDM integration
- [ ] ISDA/FINOS participation

### If PRAGMATIST:
- [ ] No CDM-specific evidence
- [ ] Focus on traditional custody services
- [ ] Vendor partnerships for reporting

---

## Single Adversarial Question (Full Protocol)

**Question:** Does BNY Mellon's market infrastructure role (clearing, settlement) create CDM engagement, or is CDM irrelevant to custody business model?

**Assessment Criteria:**
- If evidence of infrastructure CDM role → Consider ARCHITECT
- If evidence of client CDM services → Consider ARCHITECT
- If no CDM evidence → PRAGMATIST confirmed

---

## Classification Decision Tree

```
Is there evidence of CDM infrastructure role?
├── YES → ARCHITECT (Infrastructure)
│   └── Check for: Clearing/settlement CDM, ISDA participation
└── NO → Is there evidence of CDM client services?
    ├── YES → ARCHITECT (Client-Service)
    └── NO → PRAGMATIST (Custody focus)
```

---

## Peer Comparison

| Peer | Classification | BNY Mellon Comparison |
|------|----------------|----------------------|
| State Street | TBD | Direct custody peer |
| JPMorgan | ARCHITECT-Native | Different business model |
| DTCC | Not in study | Market infrastructure comparison |

---

## Output Requirements

Save outputs to:
- `outputs/phase-9-us-custody-banks/bny-mellon/rapid-assessment.md`
- `outputs/phase-9-us-custody-banks/bny-mellon/status.json`

---

## Time Budget

| Activity | Est. Time |
|----------|-----------|
| Searches (Tier 1-2 combined) | 40 min |
| Single adversarial question | 15 min |
| Synthesis | 25 min |
| **Total** | **~1.5 hours** |

---

## Success Criteria

1. [ ] Classification determined (ARCHITECT vs PRAGMATIST)
2. [ ] Market infrastructure angle assessed
3. [ ] Custody business model impact understood
4. [ ] State Street comparison documented
