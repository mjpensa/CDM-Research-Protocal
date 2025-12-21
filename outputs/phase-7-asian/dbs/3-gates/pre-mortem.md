# Pre-Mortem Analysis: DBS Bank

**Research Date**: 2025-12-21
**Researcher**: Claude Code (Opus 4.5)
**Stage**: Before Evidence Collection

---

## Exercise Purpose

Conduct pre-mortem analysis to identify potential failure modes in DBS Bank CDM research before beginning evidence collection.

**Prompt**: "Imagine it is 6 months from now. Our DBS Bank CDM assessment was completely wrong. What went wrong?"

---

## Failure Scenario 1: False Negative (Missed Real Adoption)

### How We Failed
We classified DBS as PRAGMATIST/OBSERVER, but 6 months later DBS announced production CDM usage that had been underway for 18 months.

### Why It Happened
1. **Singapore Disclosure Norms**: Asian banks disclose less publicly than Western counterparts
2. **Regulatory Context**: No MAS mandate created no filing requirements
3. **Vendor Confidentiality**: DBS using vendor CDM solutions under NDA
4. **Internal Codenames**: DBS calls CDM implementation by different internal name
5. **FINOS Non-membership**: DBS implemented CDM without joining FINOS (not required)

### Mitigation Strategies
- ✅ Search for generic "derivatives data standardization" not just "CDM"
- ✅ Check MAS regulatory technology consultations for DBS participation
- ✅ Review DBS annual reports for "data harmonization" or "ISDA" mentions
- ✅ Search for DBS speakers at Sibos, ISDA conferences
- ✅ Check if Andrew Ng's ISDA Board role provides signals we're missing

---

## Failure Scenario 2: False Positive (Overstated Engagement)

### How We Failed
We classified DBS as OBSERVER based on Andrew Ng's board roles, but these were purely personal appointments with no organizational CDM engagement.

### Why It Happened
1. **Individual vs. Institutional**: Conflated executive's personal roles with bank's strategy
2. **Board Membership Misinterpretation**: Assumed ISDA Board seat implies CDM awareness
3. **Confirmation Bias**: After finding governance signals, stopped searching for disconfirming evidence
4. **Peer Comparison Failure**: Didn't compare DBS to similar-sized Asian banks

### Mitigation Strategies
- ✅ Explicitly search for "DBS not using CDM" or "DBS traditional systems"
- ✅ Check if other ISDA Board members' banks have CDM evidence (control test)
- ✅ Look for vendor announcements of traditional (non-CDM) systems at DBS
- ✅ Search for DBS technology architecture articles mentioning legacy systems

---

## Failure Scenario 3: Search Technique Failure

### How We Failed
DBS has CDM initiatives but we used wrong search terms or sources.

### Why It Happened
1. **Language Barrier**: Some Singapore sources in Mandarin or Malay not searched
2. **LinkedIn Blind Spot**: DBS employees' profiles set to private
3. **Conference Proceedings**: Missed DBS presentations at regional conferences
4. **Vendor Whitepapers**: Didn't check Bloomberg, Refinitiv, MarkitWire case studies
5. **GitHub Handle Mismatch**: DBS developers use non-@dbs.com email on GitHub

### Mitigation Strategies
- ✅ Search "DBS" + "数据标准化" (Chinese for data standardization)
- ✅ Check MarkitWire, Bloomberg, Refinitiv for DBS case studies
- ✅ Search GitHub with location:Singapore + CDM
- ✅ Review ISDA APAC conference agendas for DBS speakers
- ✅ Check Singapore FinTech Festival presentations

---

## Failure Scenario 4: Temporal Mismatch

### How We Failed
DBS had CDM evidence in 2021-2022 that is now stale, or has very recent (post-Nov 2024) announcements we can't access.

### Why It Happened
1. **Evidence Decay**: Old announcements removed from DBS website
2. **Pilot Termination**: DBS tried CDM in 2022, abandoned it, evidence remains but misleading
3. **Recency Bias**: Focused on current evidence, missed historical context
4. **Search Engine Lag**: Recent announcements not yet indexed

### Mitigation Strategies
- ✅ Use Wayback Machine for historical DBS website snapshots
- ✅ Search for date-restricted queries (2020-2024) not just recent
- ✅ Check ISDA historical working group membership lists
- ✅ Look for "DBS pilot CDM" or "DBS proof of concept" for terminated projects

---

## Failure Scenario 5: Misclassification of Maturity Level

### How We Failed
We found evidence correctly but assigned wrong classification level.

### Why It Happened
1. **OBSERVER vs. PRAGMATIST**: Borderline case where governance signals are ambiguous
2. **Vendor Dependency Misread**: Missed that DBS outsources all derivatives ops to vendor (making them PRAGMATIST-Vendor not OBSERVER)
3. **Confidence Miscalibration**: Set confidence too high or too low for evidence strength

### Mitigation Strategies
- ✅ Apply strict interpretation: governance-only = OBSERVER max
- ✅ Check if DBS uses BNY Mellon, State Street, or other outsourced ops
- ✅ Compare evidence strength to reference banks (UBS, Barclays) for calibration
- ✅ Use decision tree from CLAUDE.md Section 9 mechanically

---

## Pre-Search Hypotheses to Test

### H1: Singapore Regulatory Context
**Hypothesis**: Absence of MAS CDM mandate reduces DBS adoption likelihood vs. European banks.
**Test**: Compare DBS to European banks under EMIR Refit. If DBS = PRAGMATIST and Europeans = ARCHITECT, supports hypothesis.

### H2: ISDA Board Signal Strength
**Hypothesis**: Andrew Ng's ISDA Board membership is weak signal of organizational CDM engagement.
**Test**: Check other ISDA Board members' banks. If most lack CDM evidence, board seat is uninformative.

### H3: Asian Bank Disclosure Gap
**Hypothesis**: DBS may have CDM usage but doesn't disclose publicly like Western banks.
**Test**: Search Chinese/regional sources. If evidence found there but not Western press, supports hypothesis.

---

## Success Criteria

Research will be considered successful if:

1. ✅ We find EITHER positive CDM evidence OR high-confidence null result
2. ✅ We can explain Andrew Ng's ISDA Board role in context
3. ✅ We understand DBS's position relative to Asian/Singapore peers
4. ✅ Classification confidence matches evidence strength (no over/under-confidence)
5. ✅ All plausible search strategies exhausted before concluding

---

## Red Flags to Watch For

🚩 **Confirmation Bias**: If we find one piece of evidence and stop searching
🚩 **Western-Centric Sources**: If we only check US/UK media
🚩 **Recency Bias**: If we ignore pre-2023 evidence as "too old"
🚩 **Authority Bias**: If we over-weight Andrew Ng's role without organizational corroboration
🚩 **Null Result Acceptance**: If we accept "no evidence" without trying alternative search terms

---

**Commitment**: Before finalizing DBS classification, explicitly review this pre-mortem and confirm all mitigation strategies were applied.
