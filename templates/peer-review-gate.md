# Peer Review Gate (Optional)

## Purpose

This optional gate implements Denzin's investigator triangulation principle by introducing a second reviewer for high-stakes or ambiguous classifications. Peer review reduces individual analyst bias and improves overall calibration.

---

## When Peer Review is Required

Peer review should be triggered when any of the following conditions apply:

| Condition | Rationale |
|-----------|-----------|
| Classification confidence ≥ 85% | High-stakes claims need validation |
| Classification differs from prior framework claim | Contradicting existing assessments requires scrutiny |
| Adversarial challenge resulted in classification revision | Significant evidence reinterpretation occurred |
| Evidence contains unresolved contradictions | Multiple interpretations possible |
| Observable implications test was ambiguous (both passed or both failed) | Hypothesis discrimination was weak |
| Bank is strategically important to framework | Higher consequence of error |

---

## Peer Review Template

### Review Header

| Field | Value |
|-------|-------|
| **Bank Name** | [BANK NAME] |
| **Original Analyst** | [Name/ID] |
| **Peer Reviewer** | [Name/ID] |
| **Review Date** | [YYYY-MM-DD] |
| **Original Assessment Date** | [YYYY-MM-DD] |
| **Trigger Condition** | [Which condition above triggered review] |

---

### Section 1: Evidence Review

**Question**: Are all evidence items properly sourced, tiered, and weighted?

| Check | Status | Notes |
|-------|--------|-------|
| All Tier 1 sources verified and accessible | [ ] Pass [ ] Fail | |
| Tier assignments match source authority per CLAUDE.md | [ ] Pass [ ] Fail | |
| LR values match tables in bayesian-updating.md | [ ] Pass [ ] Fail | |
| Independence adjustments applied where needed | [ ] Pass [ ] Fail | |
| Temporal weights applied correctly | [ ] Pass [ ] Fail | |
| Null results documented appropriately | [ ] Pass [ ] Fail | |

**Evidence Review Verdict**: [ ] PASS / [ ] ISSUES FOUND

**Issues Found (if any)**:
- [ ] E___: [Description of issue]
- [ ] E___: [Description of issue]

---

### Section 2: Logic Review

**Question**: Is the reasoning chain from evidence to classification sound?

| Check | Status | Notes |
|-------|--------|-------|
| Prior probability justified with documented rationale | [ ] Pass [ ] Fail | |
| Bayesian calculation is mathematically correct | [ ] Pass [ ] Fail | |
| Counterfactual test properly conducted | [ ] Pass [ ] Fail | |
| Disconfirmation searches were attempted | [ ] Pass [ ] Fail | |
| Observable implications test covered BOTH hypotheses | [ ] Pass [ ] Fail | |
| Adversarial challenge was genuinely rigorous | [ ] Pass [ ] Fail | |

**Logic Review Verdict**: [ ] PASS / [ ] ISSUES FOUND

**Logical Issues (if any)**:
[Describe any flaws in the reasoning chain]

---

### Section 3: Calibration Review

**Question**: Is the confidence level appropriate for the evidence quality?

| Check | Status | Notes |
|-------|--------|-------|
| Confidence does not exceed tier-based caps | [ ] Pass [ ] Fail | |
| Betting test would pass at stated odds | [ ] Pass [ ] Fail | |
| Classification is consistent with similar banks | [ ] Pass [ ] Fail | |
| Language matches confidence level per calibration guide | [ ] Pass [ ] Fail | |

**Calibration Review Verdict**: [ ] PASS / [ ] ISSUES FOUND

**Calibration Issues (if any)**:
[Describe over/under-confidence concerns]

---

### Section 4: Alternative Interpretation

**Question**: Is there a reasonable alternative interpretation the original analyst missed?

**Reviewer's Alternative Interpretation**:
[Write 2-3 sentences describing a plausible alternative reading of the evidence]

**Is this alternative more compelling than the original?**
[ ] No — Original interpretation is stronger
[ ] Possibly — Alternative deserves consideration
[ ] Yes — Alternative is more compelling

**If "Possibly" or "Yes"**: Recommend specific follow-up searches:
1. [Search 1]
2. [Search 2]

---

### Section 5: Final Verdict

| Outcome | Description |
|---------|-------------|
| [ ] **CONCUR** | Classification confirmed as stated |
| [ ] **CONCUR WITH CAVEATS** | Classification confirmed with documented caveats |
| [ ] **REVISE CONFIDENCE** | Classification correct but confidence should change |
| [ ] **REVISE CLASSIFICATION** | Classification should change |
| [ ] **ADDITIONAL REVIEW** | Cannot determine; requires third reviewer or additional evidence |

**Recommended Changes (if any)**:

| Field | Original | Recommended | Rationale |
|-------|----------|-------------|-----------|
| Classification | [Original] | [Recommended] | [Why] |
| Confidence | [Original]% | [Recommended]% | [Why] |
| Variant | [Original] | [Recommended] | [Why] |

---

### Section 6: Sign-Off

**Peer Reviewer Statement**:

> I have independently reviewed the evidence, calculations, and reasoning for this classification. My verdict above represents my honest assessment of the analysis quality and conclusions.

| Field | Value |
|-------|-------|
| **Reviewer Signature** | [Name/ID] |
| **Date** | [YYYY-MM-DD] |
| **Time Spent on Review** | [X hours] |

---

## Post-Review Actions

### If CONCUR or CONCUR WITH CAVEATS:
- [ ] Add peer review note to final report
- [ ] Archive this review in `outputs/{bank}/peer-review/`
- [ ] Proceed to publication

### If REVISE CONFIDENCE or REVISE CLASSIFICATION:
- [ ] Original analyst reviews feedback
- [ ] Analyst either accepts changes or documents disagreement
- [ ] If disagreement persists, escalate to third reviewer
- [ ] Updated assessment replaces original

### If ADDITIONAL REVIEW:
- [ ] Document specific uncertainty
- [ ] Assign third reviewer
- [ ] Conduct additional evidence gathering if recommended

---

## Integration Notes

This template should be referenced in:
- `config/agent-prompts/orchestrator.md` — trigger conditions
- `docs/workflow.md` — as optional step after adversarial

---

_Template Version: 1.0_
_Last Updated: 2025-12-20_
