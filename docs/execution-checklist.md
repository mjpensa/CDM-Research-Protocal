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
- [ ] Set up evidence tracking (text file or notes)
- [ ] Review anchor points that constrain findings

### Step 2: Pre-Research Analysis (15-20 min)

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

**CRITICAL (Ledger-First)**: Evidence Gatherer produces `evidence.json` as PRIMARY output. Markdown files in `1-evidence/` are rendered from JSON.

#### Tier 1 Searches
- [ ] Execute all specified Tier 1 searches
- [ ] Document each result in `evidence.json` with `lr_mapping` field
- [ ] Document null results in `evidence.json` `null_results` array
- [ ] Run `tools/run_pipeline.py` to verify and render Markdown views
- [ ] Complete Reasoning Gate 1
  - Evidence delta analysis
  - Probability update
  - Sufficiency check
  - Counterfactual test
  - Mini-adversarial
- [ ] **If CONTRADICTIONS_DETECTED**: Complete Stage 5.5 Contradiction Resolution
  - Create `3-gates/contradiction-resolution.md`
  - Classify each contradiction (Temporal/Definitional/Factual)
  - Apply resolution methodology
  - Calculate confidence impact
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

### Step 4: Synthesis (30-45 min)

- [ ] Compile evidence inventory
- [ ] Build reasoning chain
- [ ] Determine preliminary classification
- [ ] Assess confidence using calibration criteria
- [ ] Complete stakeholder motivation analysis

### Step 5: Adversarial Challenge (30-45 min)

**Full Adversarial (required for all banks):**
- [ ] Construct counter-case
- [ ] Execute targeted disconfirming searches (3 required)
- [ ] Steelman the alternative
- [ ] Evaluate robustness (5 questions)
- [ ] Determine adversarial verdict

### Step 6: Cross-Validation (15-20 min)

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

All banks receive the same full protocol:

| Activity | Time |
|----------|------|
| Pre-research | 15-20 min |
| Evidence gathering (all 3 tiers) | 90-120 min |
| Reasoning gates (3 gates) | 30-45 min |
| Synthesis | 30-45 min |
| Adversarial (full) | 30-45 min |
| Cross-validation | 15-20 min |
| Output | 20-30 min |
| **Total per bank** | **4-6 hours** |

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
