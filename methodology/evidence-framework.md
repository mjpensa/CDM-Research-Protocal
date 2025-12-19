# Evidence Framework

## Evidence Tier Hierarchy

### Tier 1: Official Sources (Definitive Weight)

**Definition:** Primary sources with institutional authority

**Examples:**
- Bank press releases and official announcements
- Annual reports and investor presentations
- Regulatory filings (10-K, 20-F equivalents)
- ISDA official announcements naming the bank
- FINOS official communications
- Central bank/regulator announcements

**Characteristics:**
- Authored or approved by the institution
- Subject to legal/regulatory accuracy requirements
- Dated and verifiable
- Directly states facts (not inference)

**Usage:** Can drive classification alone if specific and current

---

### Tier 2: Industry Sources (Strong Weight)

**Definition:** Authoritative third-party coverage

**Examples:**
- Risk.net, Waters Technology, Financial News articles
- ISDA AGM speaker lists and presentation content
- FINOS event participation and GitHub contributions
- Specialist analyst reports (Oliver Wyman, McKinsey, etc.)
- Trade association publications
- Conference proceedings with named speakers

**Characteristics:**
- Professional editorial standards
- Subject matter expertise
- May include interpretation/analysis
- Generally reliable but verify key claims

**Usage:** Strong support for classification; 3+ Tier 2 sources can substitute for Tier 1

---

### Tier 3: Indirect Signals (Moderate Weight)

**Definition:** Evidence requiring inference

**Examples:**
- Job postings mentioning CDM/DRR
- LinkedIn profiles of bank employees
- Vendor announcements claiming bank as client
- Patent filings
- Academic papers authored by bank employees
- Industry conference attendance (without speaking)

**Characteristics:**
- May reflect aspirations rather than commitments
- May be outdated or inaccurate
- Requires corroboration
- Useful for pattern detection

**Usage:** Cannot drive classification alone; useful for corroboration or trajectory signals

---

### Tier 4: Contextual Inference (Weak Weight)

**Definition:** Conclusions drawn from context rather than direct evidence

**Examples:**
- Business model analysis (derivatives exposure suggests need)
- Regulatory pressure analysis (EMIR Refit requires response)
- Peer behavior inference (if BNP did it, SocGen might)
- Absence of evidence after thorough search
- Geographic/jurisdictional requirements

**Characteristics:**
- No direct evidence of CDM engagement
- Logical reasoning from context
- High uncertainty
- May reflect our assumptions more than reality

**Usage:** Supports Pragmatist classification when combined with evidence absence; cannot support Architect classification

---

## Evidence Block Format

Every piece of evidence must be documented using this format:

```markdown
[BANK-###] TIER [1/2/3/4] — [SUPPORTS/UNDERMINES/NEUTRAL] [Classification]

Source: [Full source name]
Date: [Publication date]
URL: [If available]

Finding: "[Exact quote or precise summary]"

Quality Assessment:
- Authority: [High/Medium/Low]
- Recency: [Current (<18mo) / Dated (18mo-3yr) / Historical (>3yr)]
- Specificity: [Specific/Moderate/Vague]
- Corroborated: [Yes/No/Pending]

Confidence: [HIGH/MEDIUM/LOW]
Reasoning: [Why this confidence level]

Caveats: [Limitations, alternative interpretations]

Bayesian Impact:
- Prior P(Architect): [X]%
- Likelihood Ratio: [From bayesian-updating.md table]
- Posterior P(Architect): [Updated %]
---
```

---

## Source Quality Filtering

### Filter 1: Recency

| Age | Classification | Usage |
|-----|----------------|-------|
| <18 months | Current | Full weight |
| 18 months - 3 years | Dated | Reduced weight; verify still accurate |
| >3 years | Historical | Context only; do not use for current classification |

**Exception:** Foundational events (e.g., 2018 DRR pilot participation) remain relevant as CONTEXT for trajectory analysis.

---

### Filter 2: Source Authority

| Source Type | Authority Level | Treatment |
|-------------|-----------------|-----------|
| Official bank/regulatory/ISDA/FINOS | HIGH | Accept; verify date |
| Established trade press (Risk.net, Waters, FN) | HIGH | Accept; note any caveats |
| Major business press (FT, WSJ, Bloomberg) | MEDIUM-HIGH | Accept; may lack technical depth |
| Consultant/analyst reports | MEDIUM | Accept with positioning bias caveat |
| Vendor marketing material | LOW | SKEPTICAL; verify independently |
| Press releases from vendors about clients | LOW | Verify with client source |
| Blog posts, opinion pieces | LOW | Weak corroboration only |
| Forums, social media, unverified LinkedIn | VERY LOW | Ignore unless corroborated |
| AI-generated summaries, content farms | REJECT | Do not use |

---

### Filter 3: Specificity

| Specificity Level | Example | Treatment |
|-------------------|---------|-----------|
| **Specific** | "Bank X announced CDM pilot in Q3 2024 with go-live expected Q2 2025" | High value; can drive classification |
| **Moderate** | "Bank X is participating in industry CDM initiatives" | Medium value; seek specifics |
| **Vague** | "Bank X is exploring derivatives technology modernization" | Low value; cannot drive classification |

---

### Filter 4: Conflict of Interest

**Check:** Does the source benefit from the claim being true?

| Scenario | Risk | Mitigation |
|----------|------|------------|
| Vendor claims bank uses their product | High — marketing incentive | Require bank confirmation |
| Bank claims industry leadership | Medium — reputational incentive | Require third-party verification |
| ISDA/FINOS claims contribution | Low — consortium accuracy incentive | Generally reliable |
| Trade press reports fact | Low — editorial reputation | Accept with standard verification |
| Competitor claims rival is behind | High — competitive positioning | Verify independently |

---

### Filter 5: Consistency

**Check:** Does this source contradict other sources of equal or higher authority?

If YES:
1. Do not selectively accept confirming evidence
2. Trigger Contradiction Resolution Protocol (see `/appendices/contradiction-resolution.md`)
3. Document the contradiction explicitly
4. Reduce confidence until resolved

If NO:
1. Note consistency with other sources
2. Consistency across independent sources increases confidence

---

## Evidence Sufficiency Thresholds

### Minimum Evidence for Classification

| Classification | Minimum Evidence Required |
|----------------|---------------------------|
| ARCHITECT-Native | Tier 1 production announcement + corroboration |
| ARCHITECT-Leader | Tier 1 production commitment OR Tier 1 + 2 Tier 2 contribution evidence |
| ARCHITECT-Follower | Tier 2 contribution evidence (2+ sources) |
| PRAGMATIST (confirmed) | Tier 1/2 evidence of non-CDM approach |
| PRAGMATIST (inferred) | Exhaustive search with no positive evidence + business model context |
| UNKNOWN | Insufficient evidence to classify either way |

### Evidence Insufficiency Indicators

Flag research as insufficient if:
- Fewer than 5 evidence blocks documented
- No Tier 1 or Tier 2 evidence found
- All evidence is >18 months old
- No null results documented (suggests incomplete search)
- Evidence only supports one hypothesis (no disconfirming search)

---

## Null Result Documentation

When searches return no relevant results, document:

```markdown
NULL RESULT BLOCK

Search Query: [Exact query executed]
Results Reviewed: [Number of results examined]
Relevant Findings: 0

Null Classification:
□ NO RESULTS — Query returned nothing
□ IRRELEVANT RESULTS — Results exist but don't address topic
□ PAYWALLED — Potentially relevant but inaccessible
□ OUTDATED ONLY — Only historical references found

Null Explanation: [Why no results — specific reason]

Informative Absence Assessment:
- Would we EXPECT to find evidence if hypothesis X were true? [Yes/No]
- If yes, absence [SUPPORTS/UNDERMINES] hypothesis X because [reason]
- If no, absence is [UNINFORMATIVE]

Next Action:
□ BROADEN — Try less specific query
□ PIVOT — Try different source type
□ ACCEPT — Document as informative absence
□ ESCALATE — Flag for alternative research method
---
```

---

## Evidence Inventory Template

At end of evidence gathering, compile inventory:

```markdown
## Evidence Inventory: [BANK NAME]

### Summary Statistics
- Total evidence blocks: [N]
- Tier 1: [N] | Tier 2: [N] | Tier 3: [N] | Tier 4: [N]
- Supports Architect: [N] | Supports Pragmatist: [N] | Neutral: [N]
- Null results documented: [N]

### Evidence by Hypothesis Support

**Supports ARCHITECT:**
- [BANK-001]: [Brief summary]
- [BANK-003]: [Brief summary]

**Supports PRAGMATIST:**
- [BANK-002]: [Brief summary]

**Neutral/Ambiguous:**
- [BANK-004]: [Brief summary]

### Strongest Evidence
Most compelling finding: [BANK-###]
Rationale: [Why this is most compelling]

### Weakest Evidence
Least reliable finding: [BANK-###]
Rationale: [Why this is least reliable]

### Contradictions Identified
[List any contradictions requiring resolution, or "None identified"]

### Evidence Gaps
What evidence would we expect but didn't find:
1. [Gap 1]
2. [Gap 2]
```
