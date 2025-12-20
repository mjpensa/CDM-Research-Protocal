# Lloyds Banking Group — CDM/DRR Research

## Bank Profile

| Attribute | Value |
|-----------|-------|
| **Full Name** | Lloyds Banking Group PLC |
| **Bank ID** | lloyds |
| **Headquarters** | London, United Kingdom |
| **Region** | Europe (UK) |
| **Business Model** | UK-focused retail and commercial bank |
| **Derivatives Relevance** | Medium |
| **Primary Regulator** | FCA/PRA |
| **Execution Tier** | B (Abbreviated Protocol) |

---

## Research Objective

**Primary Goal:** Assess UK regional bank CDM positioning

**Key Questions:**
1. Is Lloyds following larger UK banks (Barclays/HSBC) in CDM adoption?
2. What is UK EMIR (September 2024) impact on Lloyds?
3. Is Lloyds relying on vendor solutions for regulatory reporting?

---

## Prior Probability Assessment

### Base Priors
- P(ARCHITECT-Native) = 5%
- P(ARCHITECT-Leader) = 10%
- P(ARCHITECT-Follower) = 15%
- P(PRAGMATIST) = 70%

### Contextual Adjustments

**Adjustment 1:** Non-derivatives-dominant business
- Lloyds is primarily retail/commercial focused
- Adjustment: +0% (no uplift for derivatives pressure)

**Adjustment 2:** UK Regional Bank
- Smaller derivatives footprint than Barclays/HSBC
- May follow larger peers rather than lead
- Adjustment: +0%

### Adjusted Priors (Starting Point)
- P(ARCHITECT total) = 30%
- P(PRAGMATIST) = 70%
- **Prior Odds (Architect : Pragmatist) = 0.30 : 0.70 = 0.43**

---

## Search Strategy

### Tier 1 Searches: Official Sources

**SEARCH 1.1:** "Lloyds Banking Group" "annual report" 2024 "regulatory reporting" OR "derivatives"
- Target: Official disclosure of technology initiatives

**SEARCH 1.2:** site:isda.org "Lloyds"
- Target: Official ISDA communications mentioning Lloyds

**SEARCH 1.3:** site:finos.org "Lloyds"
- Target: FINOS contributor/member documentation

### Tier 2 Searches: Industry Sources

**SEARCH 2.1:** "Lloyds" bank "Common Domain Model" OR CDM 2024 2025
- Target: Trade press coverage

**SEARCH 2.2:** "Lloyds" "UK EMIR" OR "EMIR Refit" implementation
- Target: Regulatory compliance approach

**SEARCH 2.3:** "Lloyds" derivatives technology vendor solution
- Target: Evidence of vendor dependency

### Tier 3 Searches: Indirect Signals

**SEARCH 3.1:** "Lloyds Banking Group" job posting CDM OR "regulatory reporting"
- Target: Hiring signals for CDM capability building

---

## Observable Implications Checklist

### If ARCHITECT Hypothesis:
- [ ] Bank mentioned in ISDA/FINOS contributor materials
- [ ] Named individuals speaking at CDM/DRR events
- [ ] Job postings for CDM-related roles
- [ ] Technology section of annual report mentions CDM/DRR

### If PRAGMATIST Hypothesis:
- [ ] Absence of CDM mentions in technology communications
- [ ] Traditional vendor partnerships for reporting
- [ ] Regulatory compliance described without CDM
- [ ] No CDM-related hiring activity

---

## Peer Comparison

| Peer | Expected Relationship |
|------|----------------------|
| Barclays | Lloyds likely behind (Barclays is ARCHITECT-Follower) |
| HSBC | Lloyds likely similar or behind |
| NatWest | Lloyds should be consistent with NatWest (same tier) |

---

## Output Requirements

Save outputs to:
- `outputs/phase-2-uk-regional/lloyds/1-evidence/`
- `outputs/phase-2-uk-regional/lloyds/2-bayesian/`
- `outputs/phase-2-uk-regional/lloyds/3-gates/`
- `outputs/phase-2-uk-regional/lloyds/4-adversarial/`
- `outputs/phase-2-uk-regional/lloyds/5-synthesis/`

---

## Time Budget

| Activity | Est. Time |
|----------|-----------|
| Tier 1 searches + Gate 1 | 30 min |
| Tier 2 searches + Gate 2 | 30 min |
| Tier 3 searches (if needed) | 20 min |
| Adversarial (Abbreviated) | 20 min |
| Synthesis | 30 min |
| **Total** | **2-2.5 hours** |
