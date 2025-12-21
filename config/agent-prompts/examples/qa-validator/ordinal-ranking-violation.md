# Example: Ordinal Ranking Violation Detection

## Context

Phase 1 (European Tier 1) cross-bank consistency validation.
Testing whether bank classifications maintain ordinal ranking based on evidence strength.

## Input: Phase 1 Bank Classifications

| Bank | Classification | Variant | Confidence | Key Evidence |
|------|---------------|---------|------------|--------------|
| Barclays | ARCHITECT | Follower | 72% | FINOS commits, conference speaker |
| Deutsche Bank | ARCHITECT | Leader | 75% | ISDA working group, Delta Capita partnership |
| HSBC | PRAGMATIST | Vendor-Dependent | 65% | Murex platform, no CDM signals |
| Société Générale | ARCHITECT | Follower | 68% | Working group mention, job postings |
| UBS | PRAGMATIST | Integration-Constrained | 55% | Post-CS merger focus, no CDM evidence |

---

## Test 1: Ordinal Ranking Check

### Hierarchy for Reference

```
ARCHITECT-Native > ARCHITECT-Leader > ARCHITECT-Follower > PRAGMATIST
```

### Pairwise Comparison Matrix

| Bank A | Bank B | A Evidence | B Evidence | A Class | B Class | Consistent? |
|--------|--------|------------|------------|---------|---------|-------------|
| Barclays | Deutsche Bank | FINOS commits | Working group, vendor | Follower | Leader | ✓ Yes |
| Barclays | Société Générale | FINOS commits | Working group | Follower | Follower | ✓ Yes |
| Deutsche Bank | Société Générale | WG + vendor | WG only | Leader | Follower | ✓ Yes |
| HSBC | UBS | Murex platform | No evidence | Pragmatist | Pragmatist | ✓ Yes |
| **Barclays** | **HSBC** | **FINOS commits** | **No CDM signals** | **Follower** | **Pragmatist** | ✓ Yes |

### Problematic Comparison Detected

**⚠ VIOLATION CANDIDATE: Société Générale vs HSBC**

| Factor | Société Générale | HSBC |
|--------|-----------------|------|
| Classification | ARCHITECT-Follower | PRAGMATIST-Vendor |
| Confidence | 68% | 65% |
| Highest Tier Evidence | Tier 2 | Tier 2 |
| Evidence Count | 3 items | 2 items |
| Official Announcements | None | None |
| Production Status | No evidence | No evidence |

**Initial Assessment**: SocGen classified as Architect with similar evidence profile to HSBC (Pragmatist).

---

## Violation Analysis

### Evidence Comparison Detail

**Société Générale (ARCHITECT-Follower, 68%)**
- E001: Mentioned in ISDA working group roster (Tier 2)
- E005: Job posting for "derivatives data specialist" (Tier 3)
- E008: LinkedIn profile mentioning CDM project (Tier 3)

**HSBC (PRAGMATIST-Vendor, 65%)**
- E002: Murex implementation mentioned in trade press (Tier 2)
- E006: No CDM-specific job postings found (NULL)

### Ordinal Ranking Rule Application

**Rule**: If Bank A has stronger evidence on EVERY dimension than Bank B, A must rank ≥ B.

| Dimension | SocGen | HSBC | Stronger? |
|-----------|--------|------|-----------|
| Working Group Membership | Yes | No | SocGen |
| Open Source Contribution | No | No | Tie |
| Job Postings | CDM-adjacent | None | SocGen |
| Vendor Relationship | None specific | Murex (traditional) | HSBC (but not CDM) |
| Official Announcements | None | None | Tie |

**Assessment**: SocGen has slightly stronger CDM-specific signals (working group, job posting) while HSBC has traditional vendor relationship (Murex) but no CDM indicators.

### Verdict: NO VIOLATION

The ranking is **CONSISTENT** because:

1. SocGen has CDM-specific signals (working group participation, CDM job posting)
2. HSBC has traditional platform signals (Murex) but NO CDM-specific indicators
3. Working group membership (SocGen) is a positive CDM signal
4. Absence of CDM signals (HSBC) justifies Pragmatist classification

**The key differentiator is CDM-specificity, not overall evidence volume.**

---

## Actual Violation Example

### Hypothetical Violation Scenario

If the data showed:

| Bank | Evidence | Classification |
|------|----------|---------------|
| Bank A | Production announcement + FINOS commits | ARCHITECT-Follower |
| Bank B | Working group mention only | ARCHITECT-Leader |

This would be a **CLEAR VIOLATION** because:
- Bank A has stronger evidence (production + commits) but lower classification
- Bank B has weaker evidence (mention only) but higher classification

### Resolution Steps for True Violations

1. **Identify the conflict**: Which evidence supports which classification?
2. **Check for context**: Is there a documented exception?
3. **Propose adjustment**: Either upgrade Bank A or downgrade Bank B
4. **Document rationale**: Explain why the change maintains consistency
5. **Flag for human review**: BLOCK checkpoint triggered

---

## Violation Documentation Template

When a TRUE violation is found:

```markdown
## ORDINAL RANKING VIOLATION

**Banks Involved**: [Bank A] vs [Bank B]

**Current State**:
- Bank A: [Classification] at [Confidence]%
- Bank B: [Classification] at [Confidence]%

**Evidence Comparison**:
| Dimension | Bank A | Bank B | Stronger |
|-----------|--------|--------|----------|
| [dim1] | [value] | [value] | [winner] |
| ... | ... | ... | ... |

**Violation Description**:
Bank A has stronger evidence on [N] dimensions but is classified lower than Bank B.

**Recommended Resolution**:
- Option 1: Upgrade Bank A to [new classification]
- Option 2: Downgrade Bank B to [new classification]
- Option 3: [Other resolution with rationale]

**Action Required**: BLOCK for human review
```

---

## Test 1 Summary for Phase 1

| Comparison | Consistent? | Notes |
|------------|-------------|-------|
| Barclays vs Deutsche Bank | ✓ Yes | DB has vendor partnership advantage |
| Barclays vs SocGen | ✓ Yes | Similar evidence, same classification |
| Deutsche Bank vs SocGen | ✓ Yes | DB has more evidence, higher variant |
| SocGen vs HSBC | ✓ Yes | CDM-specific vs traditional platform |
| HSBC vs UBS | ✓ Yes | Both Pragmatist, HSBC has more context |
| All Architect vs All Pragmatist | ✓ Yes | Clear CDM signal differentiation |

**Test 1 Result: PASS**

No ordinal ranking violations detected in Phase 1.
All classifications are consistent with evidence hierarchy.
