# Adversarial Checks Template

## Overview

Adversarial thinking is critical to producing reliable classifications. This template provides structured approaches for challenging conclusions at different depth levels.

---

## Full Adversarial Challenge (Tier A Banks)

Use for: Deutsche Bank, Société Générale, UBS, Barclays, HSBC

Estimated time: 30-45 minutes

```markdown
## FULL ADVERSARIAL CHALLENGE: [BANK NAME]

### Preliminary Conclusion
From synthesis, my classification is: [POSTURE-VARIANT]
My confidence is: [X]%
Key evidence supporting this: [List top 3 pieces]

---

### Section 1: Construct the Counter-Case

**Task:** You are now a skeptic who believes this classification is WRONG. Build the best possible case for the OPPOSITE classification.

**If classified as ARCHITECT, argue for PRAGMATIST:**

"The case that [Bank] is actually a PRAGMATIST, not an ARCHITECT:

1. **Evidence Reinterpretation:**
   The evidence I found can be explained without genuine CDM commitment because:
   [Write 2-3 sentences reinterpreting key evidence]

2. **Missing Evidence Problem:**
   If [Bank] were truly an ARCHITECT, we would expect to see [X, Y, Z] but we found none of these because:
   [Explain what's missing and why it matters]

3. **Alternative Explanation:**
   The most likely explanation for the evidence pattern is:
   [Provide non-ARCHITECT explanation]

4. **Motivation Analysis:**
   [Bank] lacks motivation to be an ARCHITECT because:
   [Explain why CDM investment doesn't make sense for them]

This counter-case is credible because: [Explain strength]
This counter-case is weak because: [Explain weakness]"

**If classified as PRAGMATIST, argue for ARCHITECT:**

"The case that [Bank] is actually an ARCHITECT, not a PRAGMATIST:

1. **Hidden Activity:**
   [Bank] may be engaged in CDM work that isn't publicly visible because:
   [Write 2-3 sentences on why evidence might be hidden]

2. **Evidence We Missed:**
   There may be evidence of engagement in [X, Y, Z] that our searches didn't capture because:
   [Explain potential search gaps]

3. **Strategic Silence:**
   [Bank] might be intentionally quiet about CDM plans because:
   [Provide strategic rationale]

4. **Forcing Functions:**
   [Bank] faces pressure that would drive CDM investment:
   [List regulatory, competitive, or operational pressures]

This counter-case is credible because: [Explain strength]
This counter-case is weak because: [Explain weakness]"

---

### Section 2: Targeted Disconfirming Searches

Execute searches specifically designed to find evidence AGAINST your conclusion.

**If classified as ARCHITECT, search for PRAGMATIST evidence:**

SEARCH A1: "[Bank]" derivatives reporting "vendor" OR "outsource" OR "third-party"
Result: [Document finding or null]
Impact: [Does this undermine ARCHITECT classification?]

SEARCH A2: "[Bank]" CDM "no plans" OR "not pursuing" OR "deferred"
Result: [Document finding or null]
Impact: [Does this undermine ARCHITECT classification?]

SEARCH A3: "[Bank]" derivatives technology "traditional" OR "legacy" OR "existing systems"
Result: [Document finding or null]
Impact: [Does this undermine ARCHITECT classification?]

**If classified as PRAGMATIST, search for ARCHITECT evidence:**

SEARCH P1: "[Bank]" CDM pilot OR "proof of concept" OR prototype
Result: [Document finding or null]
Impact: [Does this undermine PRAGMATIST classification?]

SEARCH P2: "[Bank]" FINOS contributor OR "working group" CDM
Result: [Document finding or null]
Impact: [Does this undermine PRAGMATIST classification?]

SEARCH P3: "[Bank]" "Common Domain Model" announcement OR initiative
Result: [Document finding or null]
Impact: [Does this undermine PRAGMATIST classification?]

---

### Section 3: Steelman the Alternative

**Task:** Write the strongest possible 2-3 paragraph argument for the opposite classification, as if you were presenting it to a skeptical executive.

"[Write steelman argument here - this should be genuinely persuasive, not a strawman]"

---

### Section 4: Evaluate Robustness

| Assessment Question | Answer | Evidence |
|---------------------|--------|----------|
| Did adversarial searches find meaningful counter-evidence? | [ ] Yes [ ] No | [Cite if yes] |
| Is the counter-case logically compelling? | [ ] Yes [ ] Somewhat [ ] No | [Explain] |
| Does the steelman reveal weaknesses in original reasoning? | [ ] Yes [ ] No | [Explain] |
| Are there gaps in my evidence that the counter-case exploits? | [ ] Yes [ ] No | [List gaps] |
| Would a reasonable person find the counter-case persuasive? | [ ] Yes [ ] Somewhat [ ] No | [Explain] |

---

### Section 5: Final Verdict

**Adversarial Outcome:**

[ ] **STRENGTHENED:** Counter-case is weak, adversarial searches found nothing, steelman is unpersuasive
    → Increase confidence by 5-10%
    → Classification confirmed: [STATE]

[ ] **UNCHANGED:** Counter-case has some merit but doesn't overcome evidence
    → Confidence unchanged
    → Classification confirmed: [STATE]

[ ] **WEAKENED:** Counter-case raises legitimate concerns, some counter-evidence found
    → Decrease confidence by 5-15%
    → Classification maintained with caveats: [STATE + CAVEATS]

[ ] **REVISED:** Counter-case is compelling, significant counter-evidence found
    → Classification changed to: [NEW CLASSIFICATION]
    → New confidence: [X]%
    → Reasoning: [Explain what changed your mind]

**Post-Adversarial Confidence:** [X]% (was [Y]% before adversarial)

**Key Uncertainty Surfaced by Adversarial:**
[What is the most important thing the adversarial process revealed?]
```

---

## Abbreviated Adversarial (Tier B Banks)

Use for: Japanese megabanks, UK regional banks, Phase 6 deep-dives

Estimated time: 15-20 minutes

```markdown
## ABBREVIATED ADVERSARIAL: [BANK NAME]

### Classification Under Challenge
Classification: [POSTURE-VARIANT]
Confidence: [X]%

---

### Counter-Argument Construction

"The single strongest argument against my classification is:

[Write 3-5 sentences presenting the best counter-argument. Be specific and cite what evidence would need to exist or what interpretation would need to change.]"

This argument is:
[ ] Compelling — I need to address this
[ ] Somewhat compelling — Worth noting as uncertainty
[ ] Not compelling — Considered and rejected because: [reason]

---

### Targeted Disconfirming Search

The ONE search most likely to disprove my classification:

Search query: [Write query]
Result: [Document finding or null]
Impact on classification: [None / Minor / Significant]

---

### Confidence Adjustment

| Factor | Adjustment |
|--------|------------|
| Counter-argument strength | [+/- X]% |
| Disconfirming search result | [+/- X]% |
| **Net adjustment** | [+/- X]% |

**Post-Adversarial Confidence:** [X]% (was [Y]%)

---

### Uncertainty Flag

Based on adversarial challenge, the key uncertainty for this bank is:
[Write 1-2 sentences]

This should be flagged in final output: [ ] Yes [ ] No
```

---

## Single Adversarial Question (Tier C Banks)

Use for: Other European banks, Spanish banks, Emerging market banks

Estimated time: 5 minutes

```markdown
## SINGLE ADVERSARIAL: [BANK NAME]

### Classification: [POSTURE-VARIANT] at [X]% confidence

### The Adversarial Question

"What is ONE thing that, if true, would make this classification WRONG?"

Answer: [Write 1-2 sentences identifying the key vulnerability]

---

### Verification

Did I check for this during research?

[ ] **YES** — Result: [What I found]
    → Impact: [None / Classification adjusted]

[ ] **NO** — Flag as: [Key uncertainty to document]
    → Should I search now? [ ] Yes (execute) / [ ] No (document gap)

---

### Confidence Impact

Adversarial question changes confidence: [ ] Yes: [X]% → [Y]% / [ ] No

### Output Note

Include in uncertainties section: [ ] Yes / [ ] No
```

---

## Adversarial Mindset Guidance

### Common Adversarial Failures

| Failure | Description | Correction |
|---------|-------------|------------|
| **Strawman** | Making counter-argument deliberately weak | Write as if you're being paid to argue the opposite |
| **Confirmation search** | Searching in ways unlikely to find counter-evidence | Use genuinely challenging search terms |
| **Dismissive evaluation** | Rejecting counter-argument without serious consideration | Imagine presenting to skeptical client |
| **Token compliance** | Going through motions without genuine challenge | Ask: "Would I bet against my conclusion?" |

### Effective Adversarial Thinking

1. **Adopt the opposite view genuinely** — For the duration of this exercise, BELIEVE the opposite
2. **Search where counter-evidence would be** — If they're a Pragmatist, where would that be documented?
3. **Consider what's missing** — Absence of expected evidence is itself evidence
4. **Evaluate fairly** — Apply same evidence standards to counter-case as original case
5. **Be willing to change** — The goal is truth, not defending your original view

### When to Revise Classification

Consider revision if adversarial challenge reveals:
- Tier 1 or Tier 2 counter-evidence you missed
- Systematic gap in your evidence gathering
- Logical flaw in your reasoning chain
- Counter-interpretation that better explains evidence pattern
- Observable implications that weren't met

Do NOT revise just because:
- Counter-argument exists (there's always a counter-argument)
- You feel uncertain (uncertainty is normal)
- Tier 3 or Tier 4 counter-evidence surfaces
- Counter-argument is theoretically possible but has no evidence
