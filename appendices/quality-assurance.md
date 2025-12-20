# Quality Assurance Appendix

## Overview

Quality assurance ensures research outputs are reliable, consistent, and ready for framework integration. This appendix provides checklists and validation protocols for self-review and cross-bank consistency.

---

## Per-Bank Self-Review Checklist

Complete BEFORE finalizing any bank assessment:

### Evidence Completeness

```markdown
□ Executed ALL specified Tier 1 searches (not just convenient ones)
  - Count executed: [X] / [Y] required
  - If < 100%, justify skips: [Reason]

□ Executed ALL specified Tier 2 searches
  - Count executed: [X] / [Y] required
  - If < 100%, justify skips: [Reason]

□ Executed Tier 3 searches as specified
  - Count executed: [X]

□ Documented NULL results (not just positive findings)
  - Null results documented: [X]
  - If zero nulls documented → RED FLAG (suggests incomplete documentation)

□ Executed adversarial searches regardless of leaning
  - Adversarial searches executed: [X]

□ Named individuals searched if identified in earlier tiers
  - Individuals identified: [List]
  - Individual searches executed: [Y/N for each]
```

### Reasoning Integrity

```markdown
□ Completed ALL reasoning gates BEFORE proceeding
  - Gate 1 completed: [Y/N]
  - Gate 2 completed: [Y/N]
  - Gate 3 completed: [Y/N]

□ Probability estimates updated after EACH evidence tier
  - Prior documented: [Y/N]
  - Post-Tier 1 update: [Y/N]
  - Post-Tier 2 update: [Y/N]
  - Post-Tier 3 update: [Y/N]
  - Post-Adversarial update: [Y/N]

□ Reasoning chain is followable without gaps
  - Can a reader follow from evidence to conclusion? [Y/N]
  - Are all logical steps explicit? [Y/N]

□ Contradictions addressed explicitly (not ignored)
  - Contradictions identified: [X]
  - Contradictions resolved: [X]
  - Unresolved contradictions flagged: [X]

□ Observable implications tested
  - If ARCHITECT: [X]/6 implications found
  - If PRAGMATIST: [X]/6 implications found
```

### Confidence Calibration

```markdown
□ Stated confidence matches evidence criteria
  - Evidence tier supporting classification: [1/2/3/4]
  - Expected confidence range for this tier: [X-Y%]
  - Stated confidence: [Z%]
  - Within expected range? [Y/N]

□ Would bet at odds implied by confidence level
  - Confidence: [X]%
  - Implied odds: [Y]:1
  - Would take bet? [Y/N]
  - If N, confidence should be reduced

□ Confidence consistent with similar banks
  - Similar evidence profiles: [List banks]
  - Their confidence levels: [List %]
  - Consistency check: [Pass/Fail]

□ Confidence adjustments documented
  - Corroboration adjustment: [+/- X%]
  - Contradiction adjustment: [+/- X%]
  - Adversarial adjustment: [+/- X%]
  - Coherence adjustment: [+/- X%]
```

### Adversarial Survival

```markdown
□ Completed full adversarial challenge [Y/N]

□ Genuinely searched for disconfirming evidence
  - Disconfirming searches executed: [3 required]
  - Disconfirming evidence found: [List or "None"]

□ Considered alternative interpretation seriously
  - Counter-case documented: [Y/N]
  - Counter-case addressed: [Y/N]

□ If classification changed after adversarial, reasoning updated
  - Classification changed? [Y/N]
  - If Y, change documented with reasoning: [Y/N]
```

### Framework Integration

```markdown
□ Classification consistent with anchor points
  - Checked against BNP timeline: [Y/N]
  - Checked against production count: [Y/N]
  - Checked against regulatory milestones: [Y/N]
  - All checks pass: [Y/N]

□ Classification makes sense relative to peers
  - Peers compared: [List]
  - Consistency verified: [Y/N]
  - Inconsistencies explained: [If any]

□ Framework integration extract completed
  - Bank table entry: [Y/N]
  - Regional analysis data: [Y/N]
  - Validation tracker entry: [Y/N]
  - Uncertainty log entry: [Y/N]
```

---

## Red Flags Requiring Rework

If ANY of the following are true, REDO the research:

| Red Flag | Issue | Required Action |
|----------|-------|-----------------|
| Classification changed after adversarial but reasoning not updated | Logic gap | Update reasoning chain to reflect new evidence |
| Confidence > 70% with only Tier 3 evidence | Overconfidence | Recalibrate using criteria; search for Tier 1/2 |
| Evidence inventory has <5 documented items | Incomplete search | Execute remaining searches |
| No null results documented | Documentation gap | Document all null results from searches |
| Reasoning gates contain only 1-2 sentence responses | Superficial analysis | Complete gates fully |
| Temporal trajectory not assessed | Missing dimension | Add trajectory analysis |
| Probability estimates not updated at each tier | Missing rigor | Add Bayesian updates |
| Observable implications not tested | Missing validation | Complete implications checklist |

---

## Cross-Bank Consistency Validation

Execute AFTER completing all banks in a phase:

### Test 1: Ordinal Ranking

List all banks from phase in order of CDM engagement (most to least):

```markdown
1. [Bank A] — [Classification, Confidence]
2. [Bank B] — [Classification, Confidence]
3. [Bank C] — [Classification, Confidence]
...
```

**Validation Check:**
For each adjacent pair, verify the higher-ranked bank has STRONGER evidence:

| Pair | Higher Bank Evidence | Lower Bank Evidence | Ordering Justified? |
|------|---------------------|---------------------|---------------------|
| A vs B | [Summary] | [Summary] | [Y/N] |
| B vs C | [Summary] | [Summary] | [Y/N] |

If any ordering NOT justified, recheck both classifications.

---

### Test 2: Similar Profile

Identify banks with similar profiles:

```markdown
Similar Profile Group 1: [Banks with similar region, business model, derivatives exposure]
- Bank X: [Classification, Confidence]
- Bank Y: [Classification, Confidence]

Similar Profile Group 2: [Another similar group]
- Bank P: [Classification, Confidence]
- Bank Q: [Classification, Confidence]
```

**Validation Check:**
Do similar banks have similar classifications?

| Group | Banks | Classifications Same? | Difference Explained? |
|-------|-------|----------------------|----------------------|
| 1 | X, Y | [Y/N] | [If N, what explains difference?] |
| 2 | P, Q | [Y/N] | [If N, what explains difference?] |

If classifications differ without explanation, recheck both.

---

### Test 3: Evidence-Confidence Correlation

Compare confidence levels across banks:

| Bank | Highest Tier | # Tier 1/2 Sources | Confidence | Correlation OK? |
|------|--------------|-------------------|------------|-----------------|
| [A] | [X] | [Y] | [Z%] | [Y/N] |
| [B] | [X] | [Y] | [Z%] | [Y/N] |
| [C] | [X] | [Y] | [Z%] | [Y/N] |

**Expected Pattern:**
- Tier 1 evidence → Confidence 75-95%
- Tier 2 only → Confidence 55-75%
- Tier 3 only → Confidence 35-55%
- Inference only → Confidence <40%

Flag any inversions (high confidence with weak evidence, or low confidence with strong evidence) for review.

---

### Test 4: Classification Distribution

Check phase-level distribution:

```markdown
Phase [X] Distribution:
- ARCHITECT-Native: [N] banks
- ARCHITECT-Leader: [N] banks
- ARCHITECT-Follower: [N] banks
- PRAGMATIST (various): [N] banks
- UNKNOWN: [N] banks
```

**Sanity Checks:**
- [ ] Total Architects < Total Pragmatists (expected based on industry reality)
- [ ] Native count ≤ Leader count ≤ Follower count (pyramid expected)
- [ ] Unknown count is reasonable given search quality

If distribution seems off, review classifications.

---

### Test 5: Anchor Coherence

Verify all classifications remain consistent with anchor points:

| Anchor Point | All Banks Consistent? | Exceptions |
|--------------|----------------------|------------|
| No bank claims production before BNP (2022) | [Y/N] | [List if N] |
| No bank claims "first" in filled category | [Y/N] | [List if N] |
| Regional forcing functions affect all regional banks | [Y/N] | [List if N] |
| Confirmed contributors (Standard Chartered, Barclays) set Follower bar | [Y/N] | [List if N] |

---

## Phase Completion Quality Gate

Before marking a phase complete, verify:

```markdown
## PHASE [X] COMPLETION QUALITY GATE

### Individual Bank Quality
□ All banks have completed per-bank output
□ All banks have completed framework integration extract
□ All self-review checklists pass
□ No outstanding red flags

### Cross-Bank Quality
□ Ordinal ranking test passes
□ Similar profile test passes
□ Evidence-confidence correlation test passes
□ Classification distribution is reasonable
□ Anchor coherence test passes

### Synthesis Quality
□ Phase synthesis document completed
□ Regional patterns documented
□ Confidence gaps identified
□ Protocol adjustments for next phase noted

### Documentation Quality
□ All evidence inventories complete
□ All null results documented
□ All contradictions logged and resolved or flagged
□ All uncertainties logged with resolution paths

PHASE [X] CLEARED: [ ] YES / [ ] NO

If NO, list blocking issues:
1. [Issue]
2. [Issue]
```

---

## Common Quality Issues and Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| **Confirmation bias** | All evidence supports initial hypothesis | Execute adversarial searches; re-examine disconfirming evidence |
| **Anchoring** | Confidence unchanged despite evidence | Review Bayesian updates; verify LRs correctly applied |
| **Incomplete search** | Few evidence blocks, quick classification | Return to Pass 2; complete all specified searches |
| **Overconfidence** | High confidence, weak evidence | Recalibrate using confidence criteria; apply betting test |
| **Inconsistent application** | Similar banks, different confidence | Cross-bank validation; standardize evidence weighting |
| **Missing trajectory** | Static classification only | Add temporal analysis from Reasoning Gate 3 |
| **Unaddressed contradictions** | Contradictions noted but not resolved | Apply contradiction resolution protocol |
| **Poor documentation** | Hard to follow reasoning | Rewrite reasoning chain with explicit steps |

---

## Quality Metrics Summary

After completing all research, compile quality metrics:

```markdown
## RESEARCH QUALITY SUMMARY

### Coverage Metrics
- Total banks researched: [N]
- Total evidence blocks documented: [N]
- Total null results documented: [N]
- Average evidence blocks per bank: [N]

### Confidence Distribution
- High confidence (70%+): [N] banks ([X]%)
- Moderate confidence (50-69%): [N] banks ([X]%)
- Low confidence (30-49%): [N] banks ([X]%)
- Insufficient (<30%): [N] banks ([X]%)

### Quality Check Results
- Self-review checklists passing: [N] / [N] banks
- Red flags identified and addressed: [N]
- Cross-bank consistency tests passing: [N] / 5

### Uncertainty Profile
- Banks requiring validation: [N]
- Unresolved contradictions: [N]
- Key uncertainties logged: [N]

### Time Investment
- Total research hours: [N]
- Average hours per bank: [N]
- Protocol compliance: [X]%
```
