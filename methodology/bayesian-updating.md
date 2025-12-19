# Bayesian Evidence Updating

## Overview

This framework provides a structured approach to updating beliefs based on evidence. It prevents both overconfidence (updating too much on weak evidence) and underconfidence (failing to update on strong evidence).

---

## Prior Probability Distribution

### Default Priors (No Prior Information)

For ANY bank with no prior evidence or framework claims:

| Classification | Prior Probability | Rationale |
|----------------|-------------------|-----------|
| ARCHITECT-Native | 5% | Only 4 firms globally confirmed in production |
| ARCHITECT-Leader | 10% | Requires significant commitment; rare |
| ARCHITECT-Follower | 15% | More common but still minority |
| PRAGMATIST | 70% | Default assumption; most banks |
| **Total** | **100%** | |

### Adjusted Priors (With Context)

Adjust priors based on known context BEFORE searching:

**If bank is derivatives-dominant (>40% IB&M revenue):**
- P(Architect) increases by 15 percentage points
- Rationale: Higher derivatives exposure = stronger business case

**If bank has known regulatory enforcement history:**
- P(Architect) increases by 10 percentage points OR decreases by 10 percentage points
- Direction depends on: Is enforcement driving investment or consuming capacity?

**If bank's regional peer is confirmed Architect:**
- P(Architect) increases by 10 percentage points
- Rationale: Regional peer pressure and follow-the-leader dynamics

**If bank is in active M&A integration:**
- P(Pragmatist) increases by 15 percentage points
- Rationale: Capacity constraints

### Prior Documentation Template

Before beginning research, document:

```markdown
## Prior Probability Assessment: [BANK NAME]

### Base Priors
- P(ARCHITECT-Native) = 5%
- P(ARCHITECT-Leader) = 10%
- P(ARCHITECT-Follower) = 15%
- P(PRAGMATIST) = 70%

### Contextual Adjustments
1. [Adjustment 1]: [+/- X%] because [reason]
2. [Adjustment 2]: [+/- X%] because [reason]

### Adjusted Priors (Starting Point)
- P(ARCHITECT-Native) = [X]%
- P(ARCHITECT-Leader) = [X]%
- P(ARCHITECT-Follower) = [X]%
- P(PRAGMATIST) = [X]%
- P(ARCHITECT total) = [sum]%

### Simplified Binary Prior
For calculation simplicity:
- P(ARCHITECT) = [sum of Native + Leader + Follower]%
- P(PRAGMATIST) = [X]%
- Prior Odds (Architect : Pragmatist) = [X] : [Y] = [ratio]
```

---

## Likelihood Ratios by Evidence Type

The likelihood ratio (LR) represents how much more likely you are to see this evidence if the Architect hypothesis is true vs. if the Pragmatist hypothesis is true.

- LR > 1: Evidence supports Architect
- LR < 1: Evidence supports Pragmatist  
- LR = 1: Evidence is uninformative

### Tier 1 Evidence Likelihood Ratios

| Evidence Type | P(E\|Architect) | P(E\|Pragmatist) | LR | Interpretation |
|---------------|-----------------|------------------|-----|----------------|
| Official production announcement | 0.95 | 0.01 | **95** | Near-definitive Architect |
| Official pilot announcement with timeline | 0.80 | 0.03 | **27** | Very strong Architect |
| Named in ISDA press release as contributor | 0.70 | 0.05 | **14** | Strong Architect |
| Named in FINOS announcement | 0.65 | 0.05 | **13** | Strong Architect |
| Annual report mentions CDM initiative | 0.60 | 0.08 | **7.5** | Moderate Architect |
| Official statement of no CDM plans | 0.02 | 0.70 | **0.03** | Strong Pragmatist |
| Announced vendor-only approach | 0.15 | 0.60 | **0.25** | Moderate Pragmatist |

### Tier 2 Evidence Likelihood Ratios

| Evidence Type | P(E\|Architect) | P(E\|Pragmatist) | LR | Interpretation |
|---------------|-----------------|------------------|-----|----------------|
| Trade press reports CDM pilot | 0.75 | 0.05 | **15** | Strong Architect |
| Conference speaker on CDM topic | 0.50 | 0.10 | **5** | Moderate Architect |
| Named in working group membership list | 0.55 | 0.15 | **3.7** | Moderate Architect |
| ISDA AGM speaker (general, not CDM) | 0.40 | 0.25 | **1.6** | Weak Architect |
| Trade press reports traditional approach | 0.10 | 0.50 | **0.2** | Moderate Pragmatist |
| No mention in CDM trade coverage | 0.20 | 0.60 | **0.33** | Weak Pragmatist |

### Tier 3 Evidence Likelihood Ratios

| Evidence Type | P(E\|Architect) | P(E\|Pragmatist) | LR | Interpretation |
|---------------|-----------------|------------------|-----|----------------|
| Job posting specifically mentions CDM | 0.45 | 0.15 | **3** | Weak Architect |
| LinkedIn profile mentions CDM work | 0.35 | 0.15 | **2.3** | Weak Architect |
| Vendor claims bank as CDM client | 0.40 | 0.20 | **2** | Very weak Architect |
| Job postings generic "regulatory reporting" | 0.30 | 0.30 | **1** | Uninformative |
| No CDM job postings found | 0.30 | 0.50 | **0.6** | Very weak Pragmatist |

### Absence Evidence Likelihood Ratios

| Evidence Type | P(E\|Architect) | P(E\|Pragmatist) | LR | Interpretation |
|---------------|-----------------|------------------|-----|----------------|
| No evidence after exhaustive Tier 1 search | 0.15 | 0.70 | **0.21** | Moderate Pragmatist |
| No evidence after exhaustive Tier 1+2 search | 0.08 | 0.75 | **0.11** | Strong Pragmatist |
| No evidence after full protocol search | 0.05 | 0.80 | **0.06** | Very strong Pragmatist |

---

## Posterior Calculation

### Step-by-Step Process

**Step 1: Establish Prior Odds**
```
Prior Odds = P(Architect) / P(Pragmatist)
Example: 0.30 / 0.70 = 0.43
```

**Step 2: Calculate Combined Likelihood Ratio**
```
Combined LR = LR₁ × LR₂ × LR₃ × ... × LRₙ

Example:
- Evidence 1 (Named in ISDA contributor): LR = 14
- Evidence 2 (Conference speaker): LR = 5
- Evidence 3 (No production announcement): LR = 0.21
Combined LR = 14 × 5 × 0.21 = 14.7
```

**Step 3: Calculate Posterior Odds**
```
Posterior Odds = Prior Odds × Combined LR
Example: 0.43 × 14.7 = 6.32
```

**Step 4: Convert to Probability**
```
P(Architect | Evidence) = Posterior Odds / (1 + Posterior Odds)
Example: 6.32 / (1 + 6.32) = 6.32 / 7.32 = 0.86 = 86%
```

**Step 5: Determine Variant**
If P(Architect) > 50%, determine variant based on evidence:
- Production confirmed → Native
- Production committed → Leader
- Contributing without production → Follower

---

## Calculation Template

Use this template after each evidence tier:

```markdown
## Bayesian Update: [BANK NAME] — After Tier [X]

### Prior (Before This Tier)
P(Architect) = [X]%
P(Pragmatist) = [Y]%
Prior Odds = [X/Y] = [ratio]

### Evidence This Tier
| Finding ID | Evidence Type | LR | Direction |
|------------|---------------|-----|-----------|
| [BANK-001] | [Type from table] | [X] | [Architect/Pragmatist] |
| [BANK-002] | [Type from table] | [X] | [Architect/Pragmatist] |
| [BANK-003] | [Type from table] | [X] | [Architect/Pragmatist] |

### Combined Likelihood Ratio
Combined LR = [LR1] × [LR2] × [LR3] = [result]

### Posterior Calculation
Posterior Odds = [Prior Odds] × [Combined LR] = [result]
P(Architect | Evidence) = [Posterior Odds] / (1 + [Posterior Odds]) = [X]%

### Updated Beliefs
P(Architect) = [X]%
P(Pragmatist) = [100-X]%

### Interpretation
[1-2 sentences on what this update means]

### Proceeding Decision
□ P(Architect) > 80% or P(Pragmatist) > 80% → Evidence sufficient, proceed to synthesis
□ 50% < P < 80% → Continue gathering evidence
□ P near 50% → Substantial uncertainty remains, prioritize disconfirming searches
```

---

## Worked Example: Deutsche Bank

### Prior Assessment
- Base P(Architect) = 30%
- Adjustment: Major derivatives business (+10%) → P(Architect) = 40%
- Adjustment: Historical regulatory issues (direction unclear, +0%) → P(Architect) = 40%
- Prior Odds = 0.40 / 0.60 = 0.67

### After Tier 1 Searches
Evidence found:
- [DB-001] No production announcement found (absence): LR = 0.21
- [DB-002] No ISDA press release naming DB: LR = 0.33 (Tier 2 absence applied to Tier 1)

Combined LR = 0.21 × 0.33 = 0.07

Posterior Odds = 0.67 × 0.07 = 0.047
P(Architect) = 0.047 / 1.047 = 4.5%

**Interpretation:** Tier 1 absence strongly suggests Pragmatist. But we should continue to Tier 2 to verify.

### After Tier 2 Searches
Evidence found:
- [DB-003] Trade press article mentions DB derivatives technology transformation: LR = 1.6 (weak, generic)
- [DB-004] DB speaker at ISDA AGM (general topic): LR = 1.6
- [DB-005] No specific CDM coverage found (absence): LR = 0.33

Combined LR (Tier 2 only) = 1.6 × 1.6 × 0.33 = 0.85

Posterior Odds = 0.047 × 0.85 = 0.04
P(Architect) = 0.04 / 1.04 = 3.8%

**Interpretation:** Tier 2 evidence is weak and doesn't overcome Tier 1 absence. Classification trending strongly toward Pragmatist.

### Final Assessment
P(Architect) ≈ 4%
P(Pragmatist) ≈ 96%
**Classification: PRAGMATIST** with high confidence

---

## Calibration Checks

### Sanity Check 1: Extreme LRs
If your combined LR is >100 or <0.01, verify:
- Are you double-counting the same evidence?
- Is a single piece of evidence carrying too much weight?
- Have you correctly identified the evidence type?

### Sanity Check 2: Belief Reversal
If your posterior is opposite your prior (e.g., 80% Pragmatist → 80% Architect), verify:
- Is the evidence really that strong?
- Could there be a simpler explanation?
- Does this pass the "would I bet at these odds" test?

### Sanity Check 3: Unchanged Beliefs
If your posterior ≈ your prior despite substantial searching, verify:
- Did you find genuinely uninformative evidence (all LR ≈ 1)?
- Or did positive and negative evidence cancel out (worth noting)?
- Is "unchanged with more confidence" the right interpretation?

---

## Limitations and Caveats

1. **LRs are estimates:** The likelihood ratios in the tables are informed estimates, not precise measurements. Use judgment when evidence doesn't fit neatly into categories.

2. **Independence assumption:** Multiplying LRs assumes evidence is independent. If two pieces of evidence come from the same source or are causally linked, don't count both fully.

3. **Missing evidence types:** If you encounter evidence not in the tables, estimate LR by asking: "How much more likely is this if Architect vs. Pragmatist?"

4. **Subjectivity in prior:** Prior adjustments are subjective. Document your reasoning so it can be reviewed.

5. **This is a tool, not a replacement for judgment:** The Bayesian framework structures thinking but doesn't eliminate the need for analytical judgment.
