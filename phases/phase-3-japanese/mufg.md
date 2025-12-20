# MUFG — CDM/DRR Research

## Bank Profile

| Attribute | Value |
|-----------|-------|
| **Full Name** | Mitsubishi UFJ Financial Group |
| **Bank ID** | mufg |
| **Headquarters** | Tokyo, Japan |
| **Region** | Asia (Japan) |
| **Business Model** | Megabank with global presence |
| **Derivatives Relevance** | High |
| **Primary Regulator** | FSA (Japan) |
| **Execution Tier** | B (Abbreviated Protocol) |

---

## Research Objective

**Primary Goal:** Assess response to JSCC CDM production (June 2025)

**Hypothesis to Test:** Japanese megabanks show cohort behavior in CDM response

**Key Questions:**
1. Is MUFG building CDM capability for JSCC connectivity?
2. What type of response: CDM-native build vs minimum connectivity vs vendor?
3. Are there ISDA/FINOS contributions from MUFG?
4. What is FSA position on CDM/DRR?

---

## Prior Probability Assessment

### Base Priors
- P(ARCHITECT-Native) = 5%
- P(ARCHITECT-Leader) = 10%
- P(ARCHITECT-Follower) = 15%
- P(PRAGMATIST) = 70%

### Contextual Adjustments

**Adjustment 1:** Derivatives-dominant business
- MUFG is a major derivatives dealer globally
- Adjustment: +10% to P(Architect)

**Adjustment 2:** JSCC Forcing Function
- JSCC CDM production June 2025 creates structural requirement
- Adjustment: +15% to P(Architect)
- Rationale: Connectivity requirement forces some CDM engagement

### Adjusted Priors (Starting Point)
- P(ARCHITECT total) = 55%
- P(PRAGMATIST) = 45%
- **Prior Odds (Architect : Pragmatist) = 0.55 : 0.45 = 1.22**

---

## Known Evidence

| Evidence | Source | Implication |
|----------|--------|-------------|
| JSCC CDM production June 2025 | JSCC announcement | Structural connectivity requirement for Japanese banks |

---

## Search Strategy

### Tier 1 Searches: Official Sources

**SEARCH 1.1:** "MUFG" OR "Mitsubishi UFJ" "annual report" 2024 "regulatory reporting" OR "derivatives technology"
- Target: Official disclosure of technology initiatives

**SEARCH 1.2:** site:isda.org "MUFG" OR "Mitsubishi UFJ"
- Target: Official ISDA communications

**SEARCH 1.3:** site:finos.org "MUFG" OR "Mitsubishi UFJ"
- Target: FINOS contributor/member documentation

**SEARCH 1.4:** "MUFG" JSCC CDM preparation connectivity
- Target: Official statements on JSCC CDM connectivity

### Tier 2 Searches: Industry Sources

**SEARCH 2.1:** "MUFG" "Common Domain Model" OR CDM 2024 2025
- Target: Trade press coverage

**SEARCH 2.2:** "MUFG" derivatives technology Japan regulatory
- Target: Japanese regulatory reporting approach

**SEARCH 2.3:** site:risk.net "MUFG" CDM OR derivatives
- Target: Specialist trade press

### Tier 3 Searches: Indirect Signals

**SEARCH 3.1:** "MUFG" OR "Mitsubishi UFJ" job posting CDM OR "regulatory reporting"
- Target: Hiring signals

---

## Observable Implications Checklist

### If ARCHITECT Hypothesis:
- [ ] Evidence of CDM-native build for JSCC connectivity
- [ ] Named individuals in ISDA/CDM working groups
- [ ] Job postings for CDM-related roles
- [ ] Public statements on CDM strategy

### If PRAGMATIST Hypothesis:
- [ ] Minimum connectivity approach to JSCC
- [ ] Vendor solution for CDM connectivity
- [ ] Absence from CDM governance discussions
- [ ] Regulatory compliance framing without strategic CDM intent

---

## Japanese Cohort Consistency

| Peer | Expected Relationship |
|------|----------------------|
| Nomura | MUFG should show similar JSCC response pattern |
| Mizuho | MUFG should be consistent with Mizuho |
| SMBC | MUFG should be consistent with SMBC |

**Note:** Japanese megabanks historically show cohort behavior on regulatory technology. Significant deviation from peers requires explanation.

---

## Output Requirements

Save outputs to:
- `outputs/phase-3-japanese/mufg/1-evidence/`
- `outputs/phase-3-japanese/mufg/2-bayesian/`
- `outputs/phase-3-japanese/mufg/3-gates/`
- `outputs/phase-3-japanese/mufg/4-adversarial/`
- `outputs/phase-3-japanese/mufg/5-synthesis/`

---

## Time Budget

| Activity | Est. Time |
|----------|-----------|
| Tier 1 searches + Gate 1 | 40 min |
| Tier 2 searches + Gate 2 | 40 min |
| Tier 3 searches (if needed) | 20 min |
| Adversarial (Abbreviated) | 20 min |
| Synthesis | 40 min |
| **Total** | **2.5-3 hours** |
