# ACH Matrix Template (Optional)

## Purpose

This template provides a formal Analysis of Competing Hypotheses (ACH) matrix as an alternative to the observable implications test. Use this approach for high-stakes or highly ambiguous classifications where a structured matrix-based evaluation adds value.

**Reference**: Richards Heuer's ACH methodology focuses on **disproving** hypotheses rather than confirming them. The correct hypothesis is the one with the least inconsistent evidence.

---

## When to Use ACH Matrix

Consider using the formal ACH matrix when:

| Condition | Rationale |
|-----------|-----------|
| High-stakes classification | Bank is strategically important; error has high consequence |
| Evidence is highly ambiguous | Observable implications test returned ambiguous results |
| Multiple hypotheses remain viable after Gate 2 | Cannot clearly discriminate between ARCHITECT and PRAGMATIST |
| Contradictory evidence present | Need structured way to weigh conflicting signals |
| Peer review requested formal analysis | Additional rigor required |

---

## ACH Matrix: [BANK NAME]

### Header Information

| Field | Value |
|-------|-------|
| **Bank Name** | [BANK NAME] |
| **Date** | [YYYY-MM-DD] |
| **Analyst** | [Name/ID] |
| **Gate Triggering ACH** | [Gate 1 / Gate 2 / Gate 3 / Adversarial] |
| **Reason for ACH** | [Why standard approach insufficient] |

---

### Step 1: Define Hypotheses

List all reasonable hypotheses being considered:

| ID | Hypothesis | Description | Prior Probability |
|----|------------|-------------|-------------------|
| H1 | ARCHITECT-Active | Currently building/deploying CDM | [X]% |
| H2 | ARCHITECT-Dormant | Past engagement, current status unclear | [X]% |
| H3 | PRAGMATIST-Interested | Watching CDM, not investing | [X]% |
| H4 | PRAGMATIST-Opposed | Explicitly rejected CDM | [X]% |

**Note**: For binary analysis, use only H1 (ARCHITECT) and H2 (PRAGMATIST).

---

### Step 2: List All Evidence

Enumerate all evidence items, including null results:

| ID | Evidence Summary | Source | Tier | Credibility | Relevance |
|----|------------------|--------|------|-------------|-----------|
| E01 | [Brief description] | [URL] | [1/2/3] | [H/M/L] | [H/M/L] |
| E02 | [Brief description] | [URL] | [1/2/3] | [H/M/L] | [H/M/L] |
| E03 | [Brief description] | [URL] | [1/2/3] | [H/M/L] | [H/M/L] |
| E04 | [Null: No X found after Y searches] | N/A | [1/2/3] | [H/M/L] | [H/M/L] |

---

### Step 3: Construct ACH Matrix

Rate each piece of evidence against each hypothesis:

**Rating Scale:**
- `++` : Strongly consistent (would definitely expect to see this if hypothesis true)
- `+` : Consistent (would likely see this if hypothesis true)
- `--` : Strongly inconsistent (would NOT expect to see this if hypothesis true)
- `-` : Inconsistent (would likely NOT see this if hypothesis true)
- `N/A` : Not applicable or uninformative

| Evidence | H1: ARCHITECT | H2: PRAGMATIST | Diagnosticity | Notes |
|----------|---------------|----------------|---------------|-------|
| E01 | [++ / + / - / -- / N/A] | [++ / + / - / -- / N/A] | [High/Med/Low] | |
| E02 | [++ / + / - / -- / N/A] | [++ / + / - / -- / N/A] | [High/Med/Low] | |
| E03 | [++ / + / - / -- / N/A] | [++ / + / - / -- / N/A] | [High/Med/Low] | |
| E04 | [++ / + / - / -- / N/A] | [++ / + / - / -- / N/A] | [High/Med/Low] | |
| E05 | [++ / + / - / -- / N/A] | [++ / + / - / -- / N/A] | [High/Med/Low] | |

---

### Step 4: Count Inconsistencies

The ACH principle: **The hypothesis with the FEWEST inconsistencies is favored.**

| Hypothesis | Strong Inconsistencies (--) | Weak Inconsistencies (-) | Weighted Score |
|------------|----------------------------|--------------------------|----------------|
| H1: ARCHITECT | [count] | [count] | [2×strong + 1×weak] |
| H2: PRAGMATIST | [count] | [count] | [2×strong + 1×weak] |

**Focus on HIGH diagnosticity evidence** — inconsistencies from high-diagnostic evidence matter more.

---

### Step 5: Identify Most Diagnostic Evidence

List the 3-5 most diagnostic pieces of evidence (those that best discriminate between hypotheses):

| Rank | Evidence ID | Why Diagnostic |
|------|-------------|----------------|
| 1 | [E##] | [Explain why this evidence strongly favors one hypothesis] |
| 2 | [E##] | [Explain why this evidence strongly favors one hypothesis] |
| 3 | [E##] | [Explain why this evidence strongly favors one hypothesis] |

---

### Step 6: Sensitivity Analysis

Test robustness of conclusion:

**Question 1**: If [most diagnostic evidence] were wrong or misinterpreted, would conclusion change?
- [ ] Yes → Conclusion is fragile
- [ ] No → Conclusion is robust

**Question 2**: What new evidence would cause you to change your conclusion?
[Describe specific evidence that would flip the assessment]

**Question 3**: Are there alternative interpretations of key evidence?
[Describe plausible alternative readings]

---

### Step 7: ACH Conclusion

**Hypothesis Ranking** (by fewest inconsistencies):

| Rank | Hypothesis | Inconsistency Score | Assessment |
|------|------------|---------------------|------------|
| 1 | [Hx] | [Score] | Most likely |
| 2 | [Hy] | [Score] | Less likely |

**Final Classification**: [ARCHITECT / PRAGMATIST]
**Variant**: [Native / Leader / Follower / Vendor-Dependent / etc.]
**Confidence**: [X]%

**Key Reasoning**:
[2-3 sentences explaining why the winning hypothesis has the fewest inconsistencies and how diagnostic evidence supports this]

---

## Integration with Standard Workflow

### When ACH Complements Observable Implications

| Scenario | Recommendation |
|----------|----------------|
| Observable implications clear (≥4/6 one side) | Skip ACH, proceed normally |
| Observable implications ambiguous (3/6 both sides) | Use ACH to break tie |
| High-stakes bank | Use both approaches, compare results |
| Adversarial challenge raised concerns | Use ACH to re-evaluate |

### Recording ACH Results

After completing ACH analysis:

1. Save this completed template to `outputs/{bank}/ach-matrix.md`
2. Reference ACH conclusion in gate clearance
3. Note any differences from observable implications results
4. Include ACH summary in final report

---

## Common ACH Pitfalls

| Pitfall | Description | Mitigation |
|---------|-------------|------------|
| **Confirmation focus** | Rating evidence as consistent rather than testing for inconsistency | Start by asking "What would DISPROVE this?" |
| **Missing evidence** | Not including null results in matrix | Always include "No X found" as evidence |
| **Equal weighting** | Treating all evidence equally | Focus on HIGH diagnosticity evidence |
| **Single source** | Anchoring on one compelling piece | Require multiple inconsistencies before rejecting |
| **Ignoring alternatives** | Not seriously considering less likely hypotheses | Rate ALL hypotheses fairly |

---

## References

- Heuer, R. J. (1999). *Psychology of Intelligence Analysis*. CIA Center for the Study of Intelligence.
- Heuer, R. J., & Pherson, R. H. (2014). *Structured Analytic Techniques for Intelligence Analysis* (3rd ed.). CQ Press.
- ACH 2.0 Software: Developed by Palo Alto Research Center (PARC)

---

_Template Version: 1.0_
_Last Updated: 2025-12-20_
