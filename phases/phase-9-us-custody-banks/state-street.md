# State Street Corporation — CDM/DRR Research

## Bank Profile

| Attribute | Value |
|-----------|-------|
| **Full Name** | State Street Corporation |
| **Bank ID** | state-street |
| **Headquarters** | Boston, USA |
| **Region** | North America (USA) |
| **Business Model** | Custody bank and asset servicing |
| **Derivatives Relevance** | Medium |
| **Primary Regulator** | Federal Reserve/SEC |
| **Execution Tier** | C (Rapid Assessment) |

---

## Research Objective

**Primary Goal:** Assess custody bank CDM positioning

**Framework Claim:** None established — discovery research

**Critical Context:** State Street is one of the world's largest custody banks. Unlike investment banks, State Street's primary business is holding and administering assets for institutional clients, not derivatives trading. CDM relevance may come from:
1. Client service offerings
2. Processing client derivatives activity
3. Market infrastructure role

**Hypothesis to Test:** Custody banks may have different CDM drivers than investment banks — client service rather than trading

**Key Questions:**
1. Does custody/asset servicing drive different CDM motivation?
2. Is State Street building CDM capability for client servicing?
3. How does CFTC Rewrite affect custody bank derivatives operations?
4. Is there a market infrastructure angle to State Street's CDM approach?

---

## Prior Probability Assessment

### Baseline Prior
- State Street is custody bank, not derivatives dealer
- Base P(ARCHITECT) = 25%

### Contextual Adjustments

**Adjustment 1:** Non-Derivatives Core Business
- Custody/asset servicing is core, not derivatives
- Adjustment: -10% to P(Architect)
- Rationale: Lower CDM relevance than dealers

**Adjustment 2:** Client Service Potential
- May offer CDM services to institutional clients
- Adjustment: +5% to P(Architect)
- Rationale: Client service could drive CDM investment

**Adjustment 3:** US G-SIB Status
- G-SIB status creates regulatory attention
- Adjustment: neutral (0%)
- Rationale: G-SIB status less relevant for custody

### Adjusted Priors
- **P(ARCHITECT) = 15%**
- P(PRAGMATIST) = 85%
- Prior Odds (Architect : Pragmatist) = 0.18

---

## Search Strategy (Rapid Assessment)

### Tier 1-2 Combined Searches

**SEARCH 1:** "State Street" "Common Domain Model" OR CDM production pilot
**SEARCH 2:** site:statestreet.com CDM OR "derivatives reporting" OR "regulatory technology"
**SEARCH 3:** site:isda.org "State Street" CDM
**SEARCH 4:** "State Street" CDM 2024 2025 derivatives custody
**SEARCH 5:** "State Street" CFTC derivatives reporting custody
**SEARCH 6:** "State Street" regulatory reporting client services

---

## Observable Implications

### If ARCHITECT (Client Service Focus):
- [ ] CDM client service offerings
- [ ] Regulatory reporting support for clients
- [ ] ISDA/FINOS participation
- [ ] CDM-related hiring

### If PRAGMATIST:
- [ ] No CDM-specific evidence
- [ ] Focus on traditional custody services
- [ ] Vendor partnerships for reporting

---

## Single Adversarial Question (Tier C Protocol)

**Question:** Does State Street offer any CDM-based services to custody clients, or is CDM irrelevant to custody business model?

**Assessment Criteria:**
- If evidence of client CDM services → Consider ARCHITECT
- If no CDM evidence → PRAGMATIST confirmed
- If vendor-based client services → PRAGMATIST (Vendor-dependent)

---

## Classification Decision Tree

```
Is there evidence of CDM client services?
├── YES → ARCHITECT (Client-Service)
│   └── Check for: Client offerings, ISDA participation
└── NO → Is there evidence of CDM internal usage?
    ├── YES → ARCHITECT-Follower
    └── NO → PRAGMATIST (Custody focus)
```

---

## Peer Comparison

| Peer | Classification | State Street Comparison |
|------|----------------|------------------------|
| BNY Mellon | TBD | Direct custody peer |
| JPMorgan | ARCHITECT-Native | Different business model |
| Northern Trust | Not in study | Custody peer comparison |

---

## Output Requirements

Save outputs to:
- `outputs/phase-9-us-custody-banks/state-street/rapid-assessment.md`
- `outputs/phase-9-us-custody-banks/state-street/status.json`

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
2. [ ] Client service angle assessed
3. [ ] Custody business model impact understood
4. [ ] BNY Mellon comparison prepared
