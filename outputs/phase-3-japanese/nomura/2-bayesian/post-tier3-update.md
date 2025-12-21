# Post-Tier 3 Bayesian Update: Nomura Holdings, Inc.

## Prior (Post-Tier 2)
**P(ARCHITECT) = 0.01**
**P(PRAGMATIST) = 0.30**
**P(OBSERVER) = 0.69**

---

## Tier 3 Evidence Summary
**Evidence Items Found:** 0
**Null Results:** 4 (highly informative)

**Key Null Results:**
1. No CDM-related job postings
2. No LinkedIn profiles indicating CDM expertise
3. No technical blog posts or patents on CDM
4. No GitHub activity related to CDM

---

## Likelihood Ratio Analysis

### Evidence: No CDM Job Postings (Informative Null)
**LR = 0.3** (strongly supports OBSERVER over PRAGMATIST)

**Reasoning:**
Banks building CDM capabilities (PRAGMATIST) typically hire developers, analysts, and project managers with CDM expertise. The complete absence of CDM job postings indicates Nomura is not building internal CDM capacity. This is highly informative evidence against PRAGMATIST and in favor of OBSERVER.

**Impact:**
Strong negative evidence against capability building. Distinguishes OBSERVER (no internal development) from PRAGMATIST (vendor-assisted development requiring internal teams).

---

### Evidence: No LinkedIn CDM Expertise (Informative Null)
**LR = 0.4** (supports OBSERVER)

**Reasoning:**
No Nomura employees have LinkedIn profiles indicating CDM project involvement or expertise. This corroborates the job posting null result: Nomura is not accumulating CDM human capital.

---

## Bayesian Update Calculation

**Starting Prior (Post-Tier 2):**
- P(ARCHITECT) = 0.01
- P(PRAGMATIST) = 0.30
- P(OBSERVER) = 0.69

**Combined Likelihood Ratio for Tier 3 Null Results:**
LR_jobs = 0.3 (strongly favors OBSERVER)
LR_expertise = 0.4 (favors OBSERVER)

**Combined LR = 0.3 × 0.4 = 0.12**

This LR applies to PRAGMATIST (capability building) vs OBSERVER (no capability building).

**Posterior Calculation:**
- P(OBSERVER | no hiring signals) ∝ P(OBSERVER) × (1/LR)
- P(OBSERVER) ∝ 0.69 × (1/0.12) = 0.69 × 8.33 = 5.75
- P(PRAGMATIST | no hiring signals) ∝ P(PRAGMATIST) × LR
- P(PRAGMATIST) ∝ 0.30 × 0.12 = 0.036

**Normalization:** 5.75 + 0.036 = 5.786

**Post-Tier 3 Posterior:**
- P(ARCHITECT) = **<0.01 (effectively 0%)**
- P(PRAGMATIST) = 0.036 / 5.786 = **0.006 (<1%)**
- P(OBSERVER) = 5.75 / 5.786 = **0.994 (~99%)**

---

## Final Classification

**Primary Classification:** OBSERVER
**Sub-Classification:** CCP-Connected
**Confidence:** 45%

**Rationale:**
Tier 3 null results decisively rule out PRAGMATIST. Nomura is not building CDM capabilities, not hiring CDM talent, and not developing internal expertise. The only CDM connection is through JSCC clearing membership, which is an infrastructure requirement rather than a strategic choice.

---

## Confidence Calibration

Why only 45% confidence despite 99% Bayesian posterior for OBSERVER?

1. **Limited Positive Evidence:** Classification rests primarily on null results and a single indirect infrastructure connection
2. **Tier Cap:** No Tier 1 evidence means maximum confidence is capped at 75% per CLAUDE.md Section 7
3. **Uncertainty About Internal Activity:** Absence of public evidence does not prove absence of private CDM work
4. **JSCC Ambiguity:** JSCC connection could be passive (OBSERVER) or could indicate future intent (pre-PRAGMATIST)

**Confidence Breakdown:**
- Certain about "not ARCHITECT": 95%
- Confident about "OBSERVER vs PRAGMATIST": 75%
- Overall classification confidence: 45% (appropriate given evidence quality)

---

## Summary

All three tiers of research converge on the same conclusion: Nomura is an OBSERVER with indirect CDM exposure through JSCC. No evidence of strategic commitment, internal capability building, or vendor partnerships. Classification is stable and well-supported by consistent null results across all evidence tiers.
