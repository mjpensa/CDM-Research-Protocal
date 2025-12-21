# Pre-Mortem: UniCredit CDM Research

**Bank:** UniCredit
**Phase:** 4 - European Tier 2
**Pre-Mortem Date:** 2025-12-20

---

## Scenario: Research Yields Inconclusive Results

Imagine it is 2 hours from now. The UniCredit CDM research has concluded with inconclusive or contradictory results. What went wrong?

---

## Potential Failure Modes

### 1. Historical Evidence Misinterpretation

**Failure:** Treating 2011-2016 ISDA Board membership as current engagement.

**Symptoms:**
- Overweighting TJ Lim's board role
- Ignoring 9-year gap since last engagement
- Conflating pre-CDM era board work with CDM adoption

**Prevention:**
- Apply strict temporal thresholds per CLAUDE.md Section 6
- Weight historical evidence at 0.3 multiplier
- Clearly distinguish historical vs. current engagement
- Check for continuity of engagement

---

### 2. False Negative: Missing Current Evidence

**Failure:** UniCredit has CDM initiatives but we fail to find evidence.

**Symptoms:**
- Limited search queries
- Overlooking non-English sources (Italian press)
- Missing subsidiary or regional CDM work
- Vendor announcements not surfaced

**Prevention:**
- Search multiple Tier 2 sources (Risk.net, Waters, DerivSource)
- Check for UniCredit Bank AG (German subsidiary)
- Look for vendor case studies
- Search conference presentations

---

### 3. Null Result Overinterpretation

**Failure:** Assuming no evidence means no engagement.

**Symptoms:**
- Classifying as UNKNOWN when OBSERVER is more accurate
- Ignoring historical ISDA Board signal
- Treating absence of evidence as evidence of absence

**Prevention:**
- Historical board membership is real evidence, even if dated
- Classify based on best available evidence
- OBSERVER (Historical-Engagement) is valid classification
- Acknowledge uncertainty explicitly

---

### 4. Peer Comparison Bias

**Failure:** Expecting UniCredit to match Credit Agricole's engagement level.

**Symptoms:**
- Searching for current board members because CA has one
- Disappointed by lack of recent evidence
- Inappropriately comparing Tier 2 banks

**Prevention:**
- Each bank has unique profile
- Historical engagement is still engagement
- Not all Tier 2 banks have same CDM posture
- Evidence dictates classification, not peer expectations

---

### 5. Temporal Confusion: CDM Timeline

**Failure:** Not accounting for when CDM development began.

**Symptoms:**
- Expecting CDM evidence from 2011-2016 period
- Treating pre-CDM board membership as CDM-related
- Confusion about ISDA's CDM initiative timeline

**Prevention:**
- ISDA CDM development began ~2017
- TJ Lim's board tenure (2011-2016) predates CDM
- Historical board membership shows ISDA ecosystem engagement, not CDM engagement
- Clearly note temporal mismatch in analysis

---

## Success Criteria

Research will be considered successful if it:

1. Accurately classifies UniCredit based on available evidence
2. Clearly distinguishes historical from current engagement
3. Applies appropriate confidence levels to dated evidence
4. Exhaustively searches Tier 1-3 sources
5. Acknowledges limitations of historical evidence
6. Provides clear rationale for OBSERVER (Historical-Engagement) classification

---

## Key Questions to Answer

1. When did TJ Lim's ISDA Board tenure end? (2016)
2. When did ISDA CDM development begin? (~2017)
3. Are there any current UniCredit representatives in ISDA roles? (No)
4. Has UniCredit engaged with CDM since 2016? (No evidence found)
5. What is the appropriate confidence level for 9-year-old evidence? (40% per temporal thresholds)

---

## Risk Mitigation Checklist

- [ ] Verify TJ Lim's board tenure dates
- [ ] Confirm no current UniCredit ISDA Board representation
- [ ] Search multiple Tier 2 sources (Risk.net, Waters, DerivSource)
- [ ] Check FINOS member directory
- [ ] Apply 0.3 temporal weight multiplier for historical evidence
- [ ] Distinguish OBSERVER (Historical) from OBSERVER (Ecosystem-Engaged)
- [ ] Set confidence at 40% maximum for historical-only evidence
- [ ] Document all null results as informative absence

---

## Expected Outcome

**Most Likely:** OBSERVER (Historical-Engagement) at 40% confidence

**Rationale:**
- Single historical evidence item (TJ Lim board membership 2011-2016)
- Evidence predates CDM development
- No current engagement signals found
- Comprehensive null results across Tier 2-3
- Historical evidence warrants OBSERVER classification, not UNKNOWN
- Temporal decay limits confidence to 40%

---

## Red Flags

If research concludes with any of these, reassess:

1. Confidence >50% with only historical evidence
2. ARCHITECT classification without technical evidence
3. UNKNOWN classification despite ISDA Board evidence
4. Failure to distinguish historical vs. current engagement
5. Missing Tier 2 searches (Risk.net, Waters)
