# Hybrid Workflow Guide: Deep Research + Analytical Framework

## Overview

This guide explains how to combine Claude Deep Research (for evidence gathering) with Claude Standard (for Bayesian classification and quality assurance).

---

## Why a Hybrid Approach?

| Capability | Deep Research | Claude Standard | Hybrid |
|------------|---------------|-----------------|--------|
| Web search breadth | ★★★★★ | ★★☆☆☆ | ★★★★★ |
| Multi-source synthesis | ★★★★★ | ★★★☆☆ | ★★★★★ |
| Protocol adherence | ★★☆☆☆ | ★★★★★ | ★★★★★ |
| Bayesian reasoning | ★★☆☆☆ | ★★★★★ | ★★★★★ |
| Adversarial challenge | ★★☆☆☆ | ★★★★★ | ★★★★★ |
| Cross-bank consistency | ★☆☆☆☆ | ★★★★★ | ★★★★★ |
| Time efficiency | ★★★★★ | ★★☆☆☆ | ★★★★☆ |

**The hybrid approach captures the best of both:**
- Deep Research's extensive web search and synthesis capabilities
- Claude Standard's ability to follow structured analytical frameworks

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE WORKFLOW                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐                                        │
│  │  Deep Research  │  ← Execute prompts from                │
│  │  (Per Bank)     │    deep-research-prompts.md            │
│  └────────┬────────┘                                        │
│           │                                                 │
│           ▼ Output: Evidence + Null Results                 │
│                                                             │
│  ┌─────────────────┐                                        │
│  │ Claude Standard │  ← Apply Post-Research                 │
│  │ (Per Bank)      │    Analysis Template                   │
│  └────────┬────────┘                                        │
│           │                                                 │
│           ▼ Output: Classification + Confidence             │
│                                                             │
│  ┌─────────────────┐                                        │
│  │ Claude Standard │  ← Apply Phase Synthesis               │
│  │ (Per Phase)     │    Prompt                              │
│  └────────┬────────┘                                        │
│           │                                                 │
│           ▼ Output: Patterns + Consistency Check            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Instructions

### Step 1: Prepare Deep Research Session

Before starting Deep Research, have ready:
- The bank's prompt from `deep-research-prompts.md`
- A place to save the output (document, note, etc.)
- The context block (copy once at session start)

### Step 2: Execute Deep Research (Per Bank)

1. **Start Deep Research session**
2. **Paste context block** (first prompt only):
   ```
   RESEARCH CONTEXT:
   [Copy from deep-research-prompts.md]
   ```

3. **Paste bank-specific prompt**:
   ```
   Research [Bank Name]'s CDM positioning...
   [Full prompt from document]
   ```

4. **Wait for Deep Research to complete** (may take several minutes)

5. **Save the full output** — you'll need:
   - Evidence inventory
   - Null results
   - Preliminary assessment
   - Sources cited

### Step 3: Apply Bayesian Framework (Claude Standard)

1. **Open Claude Standard conversation**

2. **Paste the Post-Research Analysis Template** with Deep Research output:
   ```
   I have research outputs from Deep Research on [BANK NAME]. 
   Please help me apply the Bayesian classification framework.

   RESEARCH OUTPUT:
   [Paste full Deep Research output]

   APPLY THIS ANALYSIS:
   [Template continues...]
   ```

3. **Review Claude's analysis** for:
   - Prior probability adjustments
   - Evidence tier classifications
   - Likelihood ratio applications
   - Posterior calculations
   - Adversarial considerations

4. **Save the final classification** with:
   - Classification and variant
   - Confidence percentage
   - Key evidence
   - Key uncertainties
   - Framework table entry

### Step 4: Phase Synthesis (After All Phase Banks)

1. **Compile all bank assessments** for the phase

2. **Use Phase Synthesis prompt** in Claude Standard:
   ```
   I have completed research on all banks in Phase [X]. 
   Here are the individual assessments:
   [Paste all assessments]
   
   Please synthesize...
   ```

3. **Review for**:
   - Cross-bank consistency
   - Regional patterns
   - Classification distribution
   - Confidence gaps

4. **Adjust any inconsistent classifications** before moving to next phase

### Step 5: Final Cross-Bank Analysis (After All Phases)

1. **Compile all phase syntheses**

2. **Apply cross-bank pattern recognition**:
   - Regional clustering
   - Business model correlations
   - Regulatory pressure responses
   - First-mover dynamics

3. **Produce final framework integration**

---

## Time Estimates

### Per Bank

| Step | Deep Research | Claude Standard | Total |
|------|---------------|-----------------|-------|
| Tier 1 bank (DB, SocGen, etc.) | 15-20 min | 20-30 min | 35-50 min |
| Tier 2 bank (Nomura, etc.) | 10-15 min | 15-20 min | 25-35 min |
| Tier 3 bank (ING, etc.) | 8-12 min | 10-15 min | 18-27 min |

### Per Phase

| Phase | Banks | Deep Research | Analysis | Synthesis | Total |
|-------|-------|---------------|----------|-----------|-------|
| Phase 1 | 5 | 1.5 hrs | 2 hrs | 1 hr | 4.5 hrs |
| Phase 2 | 2 | 30 min | 45 min | 30 min | 1.75 hrs |
| Phase 3 | 4 | 1 hr | 1.5 hrs | 45 min | 3.25 hrs |
| Phase 4 | 4 | 45 min | 1 hr | 30 min | 2.25 hrs |
| Phase 5 | 2 | 20 min | 30 min | 20 min | 1.2 hrs |
| Phase 6 | 2 | 30 min | 45 min | 30 min | 1.75 hrs |
| Phase 7 | 2-5 | 30 min | 45 min | 30 min | 1.75 hrs |
| **Total** | **21-24** | **~5.5 hrs** | **~7.5 hrs** | **~4 hrs** | **~17 hrs** |

Plus final cross-bank analysis: ~3 hours

**Total estimated time: 20 hours** (vs. 60-80 hours for full manual protocol)

---

## Quality Checkpoints

### After Each Bank

- [ ] Deep Research output saved
- [ ] Evidence inventory captured
- [ ] Null results documented
- [ ] Bayesian analysis completed
- [ ] Classification determined with confidence
- [ ] Adversarial check completed
- [ ] Framework table entry ready

### After Each Phase

- [ ] All banks classified
- [ ] Cross-bank consistency checked
- [ ] Ordinal ranking makes sense
- [ ] Regional patterns documented
- [ ] Confidence gaps identified
- [ ] Inconsistencies resolved

### After All Phases

- [ ] Global distribution reasonable
- [ ] All anchor points respected
- [ ] Pattern analysis complete
- [ ] Framework integration ready
- [ ] Validation priorities identified

---

## Handling Edge Cases

### Deep Research Returns Minimal Evidence

If Deep Research finds little evidence:
1. This is informative — document the absence
2. In Claude Standard, apply "informative absence" likelihood ratios
3. Classify as PRAGMATIST (inferred) with appropriate confidence discount
4. Flag for potential validation

### Deep Research Returns Contradictory Evidence

If Deep Research finds conflicting information:
1. Note both pieces of evidence
2. In Claude Standard, apply contradiction resolution protocol
3. Assess source reliability and recency
4. Document unresolved contradictions as uncertainties

### Classification Doesn't Match Expected Pattern

If a bank's classification seems inconsistent with peers:
1. Review the evidence again
2. Check if there's a specific explanation (e.g., M&A, regulatory action)
3. Document the exception and explanation
4. Adjust if evidence doesn't support the outlier classification

---

## Document Management

### Recommended Folder Structure

```
/cdm-research/
├── deep-research-outputs/
│   ├── phase-1/
│   │   ├── deutsche-bank-raw.md
│   │   ├── societe-generale-raw.md
│   │   └── ...
│   ├── phase-2/
│   └── ...
├── bayesian-analyses/
│   ├── phase-1/
│   │   ├── deutsche-bank-analysis.md
│   │   ├── societe-generale-analysis.md
│   │   └── ...
│   └── ...
├── phase-syntheses/
│   ├── phase-1-synthesis.md
│   ├── phase-2-synthesis.md
│   └── ...
├── final-outputs/
│   ├── cross-bank-analysis.md
│   ├── framework-integration.md
│   └── classification-table.md
└── notes/
    ├── validation-priorities.md
    └── methodology-observations.md
```

---

## Quick Reference Card

### Deep Research Prompt Structure
```
Research [Bank]'s CDM positioning.

CONTEXT: [Known facts, regulatory pressure]
QUESTIONS: [5-6 specific questions]
HYPOTHESIS: [If testing specific hypothesis]
SOURCES: [Where to search]
OUTPUT: [What format to use]
```

### Claude Standard Analysis Structure
```
1. Prior probability (base + adjustments)
2. Evidence classification (tier, direction, LR)
3. Bayesian update (calculate posterior)
4. Classification (posture + variant)
5. Adversarial check
6. Confidence calibration
7. Final output
8. Framework integration
```

### Classification Quick Reference
```
P(Architect) > 80% → ARCHITECT
P(Architect) 50-80% → ARCHITECT (reduced confidence)
P(Architect) 20-50% → UNCERTAIN
P(Architect) < 20% → PRAGMATIST
```
