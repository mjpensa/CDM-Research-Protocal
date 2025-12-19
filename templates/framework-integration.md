# Framework Integration Template

## Overview

This template extracts key data points from per-bank research for direct integration into the CDM Strategic Framework document. Complete this AFTER finalizing the per-bank output.

---

```markdown
# Framework Integration Extract: [BANK NAME]

## Date: [YYYY-MM-DD]

---

## 1. International Bank Table Entry

For direct insertion into framework document's international bank table:

| Bank | Region | Posture | Variant | Status | Evidence Date | Confidence | Notes |
|------|--------|---------|---------|--------|---------------|------------|-------|
| [Bank Name] | [Europe/UK/Japan/Asia/etc.] | [ARCHITECT/PRAGMATIST] | [Variant] | [Live/Pilot/POC/Eval/None] | [Most recent evidence date] | [X]% | [Brief note if needed] |

---

## 2. Regional Analysis Data

For the regional analysis section of the framework:

### Regional Classification
- **Region:** [Europe / UK / Japan / Other Asia / Americas]
- **Sub-region (if applicable):** [e.g., "French banks", "Japanese megabanks"]

### Regional Context
- **Primary Forcing Function:** [EMIR Refit / UK EMIR / JFSA / JSCC / Other]
- **Regulatory Deadline (if applicable):** [Date]
- **Regional Leader (if any):** [Bank name if a regional peer leads]

### Peer Comparison
| Peer | Their Classification | [Bank]'s Relative Position |
|------|---------------------|---------------------------|
| [Peer 1] | [Classification] | [Ahead / Same / Behind / Different path] |
| [Peer 2] | [Classification] | [Ahead / Same / Behind / Different path] |

### Regional Insight (1-2 sentences)
[What does this bank's position tell us about the regional pattern?]

---

## 3. Validation Tracker Entry

For the framework's validation and update tracking:

### Original vs. Research Comparison

| Dimension | Original Framework (v20) | Research Finding | Match? |
|-----------|--------------------------|------------------|--------|
| Included in framework? | [Yes/No] | [Yes - researched] | N/A |
| Classification | [Original or "Not included"] | [Finding] | [Yes/No] |
| Production Status | [Original or "Not included"] | [Finding] | [Yes/No] |
| Timeline | [Original or "Not included"] | [Finding] | [Yes/No] |

### Recommended Action

**Action Code:** [CONFIRM / REVISE / ADD / REMOVE / FLAG]

**Details:**
- If CONFIRM: "Research validates original classification of [X]"
- If REVISE: "Change from [original] to [new] based on [brief reason]"
- If ADD: "Add to framework as [classification] based on [brief reason]"
- If REMOVE: "Remove from framework because [brief reason]"
- If FLAG: "Insufficient evidence to classify; mark for direct validation"

### Change Log Entry (if REVISE or ADD)
```
[DATE] - [BANK NAME]
- Previous: [Classification or "Not in framework"]
- Updated: [New classification]
- Reason: [1 sentence]
- Evidence: [Key source]
- Confidence: [X]%
```

---

## 4. Uncertainty Log Entry

For the framework's uncertainty tracking:

### Bank-Specific Uncertainties

| ID | Uncertainty | Impact | Resolution Path | Priority |
|----|-------------|--------|-----------------|----------|
| [BANK]-U1 | [What we don't know] | [High/Med/Low] | [How to resolve] | [High/Med/Low] |
| [BANK]-U2 | [What we don't know] | [High/Med/Low] | [How to resolve] | [High/Med/Low] |

### Validation Opportunity

If confidence is <70%, this represents a potential client engagement opportunity:

**Diagnostic Questions:**
1. [Question that would resolve primary uncertainty]
2. [Question that would resolve secondary uncertainty]

**Engagement Hook:**
[1-2 sentences on how this uncertainty could be positioned as a diagnostic conversation starter]

---

## 5. Cross-Reference Updates

### Anchor Point Implications

Does this research affect any framework anchor points?

| Anchor | Impact | Update Needed? |
|--------|--------|----------------|
| Production count (currently 4) | [Does this add to count?] | [Yes/No] |
| First in region | [Does this change regional first?] | [Yes/No] |
| Confirmed contributors | [Does this add/remove from list?] | [Yes/No] |

### Peer Classification Implications

Does this research suggest any peer classifications should be revisited?

| Peer | Current Classification | Implication | Action |
|------|------------------------|-------------|--------|
| [Peer 1] | [Classification] | [What this research implies] | [None/Revisit] |

---

## 6. Narrative Elements

### For Executive Summary (if significant finding)

If this bank represents a notable finding (production confirmed, major reclassification, unexpected result), draft 1-2 sentences for potential inclusion in framework executive summary:

"[Draft sentence for executive summary if applicable]"

### For Regional Discussion

Draft 1-2 sentences for inclusion in the relevant regional analysis section:

"[Draft sentence for regional analysis]"

---

## 7. Data Quality Flag

### Confidence Assessment

| Confidence Level | Framework Treatment |
|------------------|---------------------|
| 90%+ | State as fact |
| 70-89% | State with "based on strong evidence" |
| 50-69% | State with "based on available evidence" |
| 30-49% | State with "preliminary assessment suggests" |
| <30% | Do not include; list in "requires validation" |

**This bank's treatment:** [Select appropriate language]

### Evidence Freshness

| Most Recent Evidence | Treatment |
|---------------------|-----------|
| <6 months | Current |
| 6-12 months | Note "as of [date]" |
| 12-18 months | Note "based on [date] evidence; may have changed" |
| >18 months | Flag for refresh |

**This bank's treatment:** [Select appropriate language]

---

## Integration Checklist

Before adding to framework document:

- [ ] Bank table entry is complete and accurate
- [ ] Regional analysis data is consistent with other regional banks
- [ ] Validation tracker reflects any changes from original
- [ ] Uncertainties are logged
- [ ] Cross-references checked
- [ ] Appropriate confidence language selected
- [ ] Evidence freshness noted if needed

**Ready for framework integration:** [ ] YES / [ ] NO

---

## Quick Copy Section

### For Spreadsheet/Table (tab-separated)
```
[Bank Name]	[Region]	[Posture]	[Variant]	[Status]	[Evidence Date]	[Confidence]%	[Notes]
```

### For Bullet Point List
```
- **[Bank Name]** ([Region]): [POSTURE]-[Variant], [Status], [Confidence]% confidence
```

### For Narrative Paragraph
```
[Bank Name] is classified as [POSTURE] ([Variant]) with [X]% confidence based on [brief evidence summary]. [One sentence on forcing functions or trajectory if relevant].
```
```
