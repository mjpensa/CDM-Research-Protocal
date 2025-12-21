# Pre-Mortem Analysis: ING Group

**Bank:** ING Group
**Phase:** 4 - European Tier 2
**Analysis Date:** 2025-12-20

---

## Purpose

Identify potential failure modes before beginning research. Per Tetlock superforecasting methodology, pre-mortems improve accuracy by surfacing blind spots.

## Hypothetical Failure Scenario

*"It is 30 days from now. The ING classification has been proven wrong. What happened?"*

## Potential Failure Modes

### 1. Hidden CDM Adoption
**Risk Level:** Medium
**Description:** ING may be using CDM internally without public announcement
**Mitigation:** Search for vendor partnerships, regulatory filings mentioning CDM
**Residual Risk:** Internal-only adoption would not be discoverable

### 2. Recent Announcement Missed
**Risk Level:** Low
**Description:** ING announced CDM initiative in last 30 days, not yet indexed
**Mitigation:** Check ING newsroom directly, recent ISDA announcements
**Residual Risk:** Very recent news may not appear in searches

### 3. Subsidiary or Regional Adoption
**Risk Level:** Medium
**Description:** ING subsidiary (e.g., ING Belgium, ING Germany) pursuing CDM separately
**Mitigation:** Search with subsidiary names explicitly
**Residual Risk:** Regional initiatives may have limited English coverage

### 4. Vendor Proxy Signal Missed
**Risk Level:** Medium
**Description:** ING using CDM via vendor relationship not publicly disclosed
**Mitigation:** Check major CDM vendors (Murex, Calypso) for ING partnerships
**Residual Risk:** White-label arrangements may not be disclosed

### 5. Confidential Pilot
**Risk Level:** Low-Medium
**Description:** ING participating in confidential CDM pilot
**Mitigation:** None available - confidential by definition
**Residual Risk:** Cannot mitigate

## Pre-Mortem Checklist

| Check | Completed | Finding |
|-------|-----------|---------|
| ING official newsroom search | ✓ | No CDM announcements |
| ING annual report CDM search | ✓ | No CDM mentions |
| FINOS member list check | ✓ | ING not listed |
| GitHub contributor search | ✓ | No ING contributors |
| ISDA working group check | ✓ | No ING representatives |
| Vendor partnership search | ✓ | No CDM vendor announcements |

## Risk Assessment

| Failure Mode | Probability | Impact | Priority |
|--------------|-------------|--------|----------|
| Hidden adoption | 15% | High | Monitor |
| Recent announcement | 5% | Medium | Low |
| Subsidiary adoption | 20% | Medium | Search completed |
| Vendor proxy | 15% | Medium | Search completed |
| Confidential pilot | 10% | Low | Accept risk |

## Conclusion

The most likely failure mode is **hidden internal adoption** or **subsidiary-level adoption** that has not been publicly disclosed. These risks are acknowledged but cannot be fully mitigated with public sources.

Research may proceed with awareness of these limitations.
