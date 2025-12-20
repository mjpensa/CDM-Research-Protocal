# Observable Implications Template

## Purpose

This template defines the 6 standard observable implications to test at Reasoning Gate 2 for each hypothesis. Testing ≥3 of 6 implications for the leading hypothesis is required.

---

## ARCHITECT Hypothesis Implications

If [Bank] is truly an ARCHITECT (actively building/contributing to CDM), we would expect to observe:

### Implication A1: Official Participation
- **Observable:** Bank name appears in ISDA CDM working group membership lists OR FINOS CDM contributor lists
- **Search:** ISDA website, FINOS GitHub contributors, working group announcements
- **Found:** [ ] Yes / [ ] No
- **Evidence ID:** ___________

### Implication A2: Named Individual Contributors
- **Observable:** Named employees of bank appear as CDM contributors, speakers, or authors
- **Search:** Conference speaker lists, ISDA publications, LinkedIn profiles
- **Found:** [ ] Yes / [ ] No
- **Evidence ID:** ___________

### Implication A3: Public Announcements
- **Observable:** Bank has made public statements about CDM adoption, pilots, or production
- **Search:** Press releases, investor presentations, annual reports
- **Found:** [ ] Yes / [ ] No
- **Evidence ID:** ___________

### Implication A4: Technical Investment Signals
- **Observable:** Job postings mention CDM, DRR, or common domain model
- **Search:** Bank careers page, LinkedIn jobs, Indeed
- **Found:** [ ] Yes / [ ] No
- **Evidence ID:** ___________

### Implication A5: Industry Recognition
- **Observable:** Trade press identifies bank as CDM adopter or contributor
- **Search:** Risk.net, Waters Technology, Financial Times derivatives coverage
- **Found:** [ ] Yes / [ ] No
- **Evidence ID:** ___________

### Implication A6: Ecosystem Relationships
- **Observable:** Bank mentioned by CDM vendors/utilities as client or partner
- **Search:** Vendor press releases, case studies, conference presentations
- **Found:** [ ] Yes / [ ] No
- **Evidence ID:** ___________

---

## PRAGMATIST Hypothesis Implications

If [Bank] is truly a PRAGMATIST (waiting for external pressure/utility), we would expect to observe:

### Implication P1: Vendor Dependency
- **Observable:** Bank uses third-party regulatory reporting vendors (not building in-house)
- **Search:** Vendor client lists, RFP announcements, technology partnerships
- **Found:** [ ] Yes / [ ] No
- **Evidence ID:** ___________

### Implication P2: Absence from CDM Forums
- **Observable:** Bank NOT mentioned in ISDA/FINOS CDM materials despite peer participation
- **Search:** Same sources as A1, looking for absence
- **Found:** [ ] Yes / [ ] No
- **Evidence ID:** ___________

### Implication P3: Traditional Technology Focus
- **Observable:** Job postings focus on traditional regulatory reporting, not CDM
- **Search:** Same sources as A4, different keywords
- **Found:** [ ] Yes / [ ] No
- **Evidence ID:** ___________

### Implication P4: Regulatory Compliance Focus
- **Observable:** Public statements emphasize compliance deadlines, not technology innovation
- **Search:** Regulatory filings, compliance announcements
- **Found:** [ ] Yes / [ ] No
- **Evidence ID:** ___________

### Implication P5: Utility/Infrastructure Reliance
- **Observable:** Bank relies on market utilities (DTCC, Regis-TR) rather than internal capability
- **Search:** Utility client lists, trade repository relationships
- **Found:** [ ] Yes / [ ] No
- **Evidence ID:** ___________

### Implication P6: Peer Differentiation
- **Observable:** Regional peers are ARCHITECTS while this bank is not participating
- **Search:** Compare to known ARCHITECT banks in same region
- **Found:** [ ] Yes / [ ] No
- **Evidence ID:** ___________

---

## Gate 2 Assessment Summary

**IMPORTANT: Test ALL 6 implications for BOTH hypotheses, not just the leading one.**

| Hypothesis | Implications Tested | Implications Found | Pass (≥3/6)? |
|------------|--------------------|--------------------|--------------|
| ARCHITECT | 6/6 | ___/6 | [ ] |
| PRAGMATIST | 6/6 | ___/6 | [ ] |

**Consistency Check:**

- [ ] Leading hypothesis passed (≥3/6 implications confirmed)
- [ ] Alternative hypothesis failed (<3/6 implications confirmed)
- [ ] If BOTH pass: Evidence is ambiguous — require Tier 3 or escalate
- [ ] If BOTH fail: Evidence pattern unclear — require additional targeted search

**Leading Hypothesis:** ___________
**Alternative Hypothesis:** ___________

**Results Interpretation:**

| Leading Pass? | Alternative Fail? | Interpretation | Action |
|---------------|-------------------|----------------|--------|
| Yes | Yes | Strong support for leading | Proceed to Tier 3 or Adversarial |
| Yes | No | Ambiguous evidence | Require Tier 3 / escalate to human |
| No | Yes | May need to reconsider hypothesis | Review evidence, consider switching |
| No | No | Insufficient discriminating evidence | Additional targeted searches required |

**Implication Test Result:** [ ] STRONG / [ ] AMBIGUOUS / [ ] WEAK / [ ] FAILED
**Action:** [ ] Proceed to Tier 3 / [ ] Proceed to Adversarial / [ ] Reconsider classification / [ ] Escalate to human review

---

## Usage Instructions

1. At Reasoning Gate 2, copy this template
2. Fill in [Bank] with the bank name
3. For the LEADING hypothesis (based on current probability), test at least 3 of 6 implications
4. Document evidence IDs from tier1-evidence.md and tier2-evidence.md
5. If <3 implications confirmed, flag for review before proceeding
6. Record summary in gate-2.md file

---

## Integration with Reasoning Gate

Reference this template in `config/agent-prompts/reasoning-gate.md` Gate 2 section:

```markdown
**Observable Implications Template:** Use `templates/observable-implications.md` for standard implications.
- Test ≥3 of 6 implications for LEADING hypothesis
- Document each implication test with evidence ID reference
- If <3 implications confirmed, flag for review before proceeding
```
