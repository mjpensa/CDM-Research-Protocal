# Example: Gate 2 Observable Implications Test

## Context

After completing Tier 2 evidence gathering for Deutsche Bank.
Testing whether the ARCHITECT hypothesis (leading) is supported by observable implications.

## Input State

- **Bank**: Deutsche Bank
- **Current P(Architect)**: 68%
- **Current P(Pragmatist)**: 32%
- **Evidence collected**:
  - E001: ISDA working group membership (Tier 2)
  - E002: Conference speaker on CDM topic (Tier 2)
  - E003: Vendor partnership with Delta Capita (Tier 2)
  - E005: Job posting mentioning CDM (Tier 3)
  - NULL: No official production announcement found (Tier 1)

---

## Observable Implications Test

### Testing ARCHITECT Hypothesis (Leading - 68%)

If Deutsche Bank is truly an ARCHITECT, we would expect to observe these signals:

| Implication | Expected if ARCHITECT | Found? | Evidence | Assessment |
|-------------|----------------------|--------|----------|------------|
| A1: Official ISDA/FINOS participation | Yes | ✓ Yes | E001: Named in ISDA CDM working group list | **CONFIRMED** |
| A2: Named individual contributors | Likely | ✓ Yes | E002: Dr. Schmidt spoke at ISDA AGM on CDM | **CONFIRMED** |
| A3: Public production announcements | Yes | ✗ No | No Tier 1 official announcements found | **NOT FOUND** |
| A4: CDM-specific job postings | Likely | ✓ Yes | E005: "CDM Developer" role posted Q3 2024 | **CONFIRMED** |
| A5: Industry recognition as CDM adopter | Likely | ✗ No | No Risk.net/Waters articles naming DB as adopter | **NOT FOUND** |
| A6: CDM ecosystem relationships | Possible | ✓ Yes | E003: Delta Capita partnership for EMIR Refit | **CONFIRMED** |

**ARCHITECT Implication Score: 4/6 confirmed**

### Testing PRAGMATIST Hypothesis (Alternative - 32%)

If Deutsche Bank is truly a PRAGMATIST, we would expect to observe these signals:

| Implication | Expected if PRAGMATIST | Found? | Evidence | Assessment |
|-------------|------------------------|--------|----------|------------|
| P1: Heavy vendor dependency | Yes | ? Partial | E003 shows vendor partnership, but also internal work | **INCONCLUSIVE** |
| P2: Absence from CDM forums | Yes | ✗ No | E001 contradicts this - active in working groups | **CONTRADICTED** |
| P3: Traditional technology focus | Yes | ? Unclear | No specific evidence either way | **NO DATA** |
| P4: Compliance-only messaging | Yes | ✗ No | E002 shows strategic engagement beyond compliance | **CONTRADICTED** |
| P5: Utility/outsource reliance | Likely | ✗ No | E005 shows internal hiring | **CONTRADICTED** |
| P6: Differentiation from CDM peers | Possible | ✗ No | Similar profile to other European banks engaging | **CONTRADICTED** |

**PRAGMATIST Implication Score: 0-1/6 confirmed (1 inconclusive)**

---

## Observable Implications Analysis

### Summary Table

| Hypothesis | Confirmed | Not Found | Contradicted | Score |
|------------|-----------|-----------|--------------|-------|
| ARCHITECT | 4 | 2 | 0 | 4/6 (67%) |
| PRAGMATIST | 0 | 0 | 4 | 0/6 (0%) |

### Interpretation

**ARCHITECT hypothesis is SUPPORTED**:
- 4 of 6 expected implications are confirmed by evidence
- No implications are contradicted
- Missing implications (A3, A5) are absence of evidence, not contradictory evidence

**PRAGMATIST hypothesis is NOT SUPPORTED**:
- 0 of 6 expected implications are confirmed
- 4 of 6 implications are actively contradicted by evidence
- Contradictions are stronger signal than mere absence

### Counterfactual Test

**Q: If we're wrong about ARCHITECT, what would we expect to see?**
- We would expect A1, A2, A4, A6 to be false positives
- Most likely explanation for false positives: Vendor-driven CDM work (not internal)
- However, E002 (conference speaker) and E005 (hiring) suggest internal capability building

**Counterfactual probability**: Low (~20%) - evidence pattern strongly favors ARCHITECT

---

## Gate 2 Decision

### Skip Threshold Check

- Current P(Architect): 68%
- Skip threshold: 80% (from config/decision-thresholds.json)
- P(Architect) < 80% → **DO NOT SKIP**

### Recommendation

**Decision**: PROCEED to Tier 3 Evidence Gathering

**Rationale**:
1. ARCHITECT hypothesis leads but below skip threshold
2. Missing A3 (official announcement) and A5 (industry recognition) could be found in Tier 3
3. Additional evidence could push probability above 80% or reveal disconfirming signals
4. Tier 3 job posting and LinkedIn analysis may clarify internal vs vendor capability

### Key Questions for Tier 3

1. Are there LinkedIn profiles showing internal CDM team members?
2. Do job postings indicate internal build vs vendor implementation support?
3. Are there any vendor-only claims that would suggest outsourcing?

---

## Mini-Adversarial Check

**Devil's Advocate Position**: Deutsche Bank is a PRAGMATIST using vendor partnerships

**Counter-argument**:
- E003 (Delta Capita partnership) could indicate vendor dependency
- E002 speaker could be representing vendor work, not internal
- Job postings (E005) could be for vendor management, not CDM development

**Assessment**: Weak counter-argument
- E001 (working group) suggests active participation beyond vendor management
- Conference topic was "internal CDM implementation strategy" (from E002)
- Job posting explicitly mentions "CDM development" not "vendor liaison"

**Adversarial Verdict**: Classification trajectory remains ARCHITECT

---

## Output Summary

```
Gate 2 Complete: Deutsche Bank
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
P(Architect): 68% (no change from Bayesian update)
Observable Implications: ARCHITECT 4/6, PRAGMATIST 0/6
Skip Decision: NO - below 80% threshold
Next Stage: Tier 3 Evidence Gathering
Trajectory: Stable toward ARCHITECT
Confidence in trajectory: MEDIUM-HIGH
```
