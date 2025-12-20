# Protocol Execution Checklist

## Quick Reference for Research Execution

This checklist provides a step-by-step guide for executing the research protocol.

---

## Before Starting Any Research

### One-Time Setup

- [ ] Read `/methodology/core-principles.md` — understand foundational approach
- [ ] Review `/methodology/bayesian-updating.md` — understand probability framework
- [ ] Review `/methodology/confidence-calibration.md` — understand confidence criteria
- [ ] Familiarize with templates in `/templates/`
- [ ] Create output directories if not present

### Per-Phase Setup

- [ ] Read phase overview file (e.g., `/phases/phase-1-european-tier1/PHASE-OVERVIEW.md`)
- [ ] Understand phase context and dependencies
- [ ] Note cross-bank hypotheses to test
- [ ] Plan execution order

---

## Per-Bank Research Workflow

### Step 1: Load and Prepare (10-15 min)

- [ ] Open bank-specific prompt file (e.g., `/phases/phase-1-european-tier1/deutsche-bank.md`)
- [ ] Read completely before starting any searches
- [ ] Note the execution tier (A/B/C) and time budget
- [ ] Set up evidence tracking (text file or notes)
- [ ] Review anchor points that constrain findings

### Step 2: Pre-Research Analysis (15-20 min for Tier A, less for B/C)

- [ ] Complete Pre-Mortem Analysis
  - Document anticipated failure modes
  - Set mitigation strategies
  - Assess anticipated difficulty
- [ ] Document Prior Probability Assessment
  - Start with base priors
  - Apply contextual adjustments
  - Calculate starting odds
- [ ] Define success criteria for this bank

### Step 3: Evidence Gathering (60-120 min depending on tier)

#### Tier 1 Searches
- [ ] Execute all specified Tier 1 searches
- [ ] Document each result using evidence block format
- [ ] Document null results explicitly
- [ ] Complete Reasoning Gate 1
  - Evidence delta analysis
  - Probability update
  - Sufficiency check
  - Counterfactual test
  - Mini-adversarial
- [ ] Decide: proceed to Tier 2 or sufficient evidence?

#### Tier 2 Searches (if needed)
- [ ] Execute all specified Tier 2 searches
- [ ] Document results and nulls
- [ ] Complete Reasoning Gate 2
  - Corroboration assessment
  - Observable implications test
  - Probability update
- [ ] Decide: proceed to Tier 3 or sufficient evidence?

#### Tier 3 Searches (if needed)
- [ ] Execute specified Tier 3 searches
- [ ] Document results
- [ ] Complete Reasoning Gate 3
  - Final probability update
  - Evidence pattern assessment
  - Trajectory assessment

### Step 4: Synthesis (30-45 min for Tier A, less for B/C)

- [ ] Compile evidence inventory
- [ ] Build reasoning chain
- [ ] Determine preliminary classification
- [ ] Assess confidence using calibration criteria
- [ ] Complete stakeholder motivation analysis

### Step 5: Adversarial Challenge (15-45 min depending on tier)

**Tier A:** Full Adversarial
- [ ] Construct counter-case
- [ ] Execute targeted disconfirming searches
- [ ] Steelman the alternative
- [ ] Evaluate robustness
- [ ] Determine adversarial verdict

**Tier B:** Abbreviated Adversarial
- [ ] Document strongest counter-argument
- [ ] Execute single disconfirming search
- [ ] Adjust confidence if needed

**Tier C:** Single Adversarial Question
- [ ] Identify one thing that would make classification wrong
- [ ] Note if checked or flag as uncertainty

### Step 6: Cross-Validation (15-20 min for Tier A)

- [ ] Check against anchor points
- [ ] Verify consistency with known peers
- [ ] Address any coherence issues

### Step 7: Final Output (20-30 min)

- [ ] Complete per-bank output template
- [ ] Complete framework integration extract
- [ ] Run self-review checklist
- [ ] Address any red flags
- [ ] Save to appropriate output directory

---

## Per-Phase Completion Workflow

After completing all banks in a phase:

### Cross-Bank Validation (1-2 hours)

- [ ] Run ordinal ranking test
- [ ] Run similar profile test
- [ ] Check evidence-confidence correlation
- [ ] Verify classification distribution is reasonable
- [ ] Run anchor coherence test

### Phase Synthesis (1-2 hours)

- [ ] Complete phase synthesis template
- [ ] Extract regional patterns
- [ ] Analyze confidence distribution
- [ ] Document uncertainties
- [ ] Note protocol adjustments for next phase

### Quality Gate

- [ ] All banks have finalized assessments
- [ ] All self-review checklists pass
- [ ] Cross-bank tests pass
- [ ] Phase synthesis complete
- [ ] Ready for framework integration

---

## Final Synthesis Workflow

After completing all phases:

### Cross-Bank Pattern Recognition (2-3 hours)

- [ ] Complete cross-bank patterns template
- [ ] Analyze classification distribution
- [ ] Test regional clustering hypothesis
- [ ] Test business model correlation
- [ ] Analyze regulatory pressure response
- [ ] Assess first-mover dynamics
- [ ] Document confidence gaps

### Framework Integration (2-3 hours)

- [ ] Compile all framework integration extracts
- [ ] Update framework tables
- [ ] Draft narrative updates
- [ ] Identify validation priorities

---

## Quick Reference: Time Budgets

| Activity | Tier A | Tier B | Tier C |
|----------|--------|--------|--------|
| Pre-research | 15-20 min | 10-15 min | 5 min |
| Evidence gathering | 90-120 min | 60-90 min | 30-45 min |
| Synthesis | 30-45 min | 20-30 min | 10-15 min |
| Adversarial | 30-45 min | 15-20 min | 5 min |
| Cross-validation | 15-20 min | 10-15 min | 5 min |
| Output | 20-30 min | 15-20 min | 15-20 min |
| **Total** | **4-6 hours** | **2-3 hours** | **1-1.5 hours** |

---

## Common Mistakes to Avoid

| Mistake | Prevention |
|---------|------------|
| Skipping pre-mortem | Always complete before searching |
| Rushing through reasoning gates | Gates are mandatory checkpoints |
| Not documenting null results | Nulls are often informative |
| Ignoring adversarial | Adversarial is required, not optional |
| Overconfidence | Apply calibration criteria strictly |
| Inconsistent across banks | Run cross-bank validation |
| Forgetting anchor points | Check every classification against anchors |

---

## File Naming Conventions

### Per-Bank Outputs
```
/outputs/phase-[N]/[bank-name]-assessment.md
/outputs/phase-[N]/[bank-name]-integration.md
```

### Phase Outputs
```
/outputs/phase-[N]/phase-[N]-synthesis.md
```

### Final Outputs
```
/outputs/cross-bank-analysis.md
/outputs/framework-updates.md
```
