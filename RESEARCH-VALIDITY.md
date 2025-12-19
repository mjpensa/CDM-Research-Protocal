# Research Validity and Refresh Protocol

## Purpose

This document establishes when CDM/DRR bank research becomes stale and defines the refresh protocol to maintain research currency.

---

## Validity Periods

### Standard Validity Schedule

| Age from Research Date | Validity Status | Confidence Adjustment | Recommended Action |
|------------------------|-----------------|----------------------|-------------------|
| 0-3 months | **Current** | None | Use as-is |
| 3-6 months | **Aging** | -5% | Monitor for triggers |
| 6-9 months | **Dated** | -10% | Plan refresh |
| 9-12 months | **Stale** | -15% | Execute refresh |
| >12 months | **Expired** | -25% minimum | Required refresh before use |

### Applying Confidence Decay

**Example:**
- Original research: Deutsche Bank, 70% confidence, dated March 2025
- Current date: September 2025 (6 months elapsed)
- Adjusted confidence: 70% - 10% = 60%
- Status: Dated — plan refresh

---

## Accelerated Staleness Triggers

These events make research **immediately stale** regardless of age:

### Tier 1 Triggers (Immediate Full Refresh Required)

| Trigger | Banks Affected | Action |
|---------|----------------|--------|
| CDM production announcement by any bank | Announcing bank | Full refresh |
| CCP CDM production announcement | All clearing members | Full refresh of affected banks |
| Major M&A announcement (>$1B deal) | Both parties | Full refresh of both |
| Regulatory CDM mandate announced | All banks in jurisdiction | Full refresh of jurisdiction |

### Tier 2 Triggers (Refresh Within 30 Days)

| Trigger | Banks Affected | Action |
|---------|----------------|--------|
| Vendor partnership announcement | Bank involved | Refresh bank |
| ISDA/FINOS governance role change | Bank involved | Refresh bank |
| New FINOS contributor announced | New contributor | Refresh contributor |
| Regulatory deadline passed | Banks in jurisdiction | Verify response, update if needed |

### Tier 3 Triggers (Note and Monitor)

| Trigger | Banks Affected | Action |
|---------|----------------|--------|
| Executive leadership change (CTO, CDO) | Bank involved | Note, consider refresh |
| Trade press speculation | Bank mentioned | Note, verify if significant |
| Job posting pattern change | Bank involved | Note as signal |

---

## Trigger Monitoring Protocol

### Weekly Scan (15 minutes)

Check the following sources:
- [ ] ISDA.org news section
- [ ] FINOS.org announcements
- [ ] Risk.net headlines (CDM/DRR keywords)
- [ ] Google News alert: "Common Domain Model" bank

### Monthly Review (1 hour)

- [ ] Review all Tier 2 triggers from past month
- [ ] Check regulatory calendars for upcoming deadlines
- [ ] Review trade press for pattern changes
- [ ] Update trigger log

### Quarterly Assessment (2-3 hours)

- [ ] Apply confidence decay to all banks not refreshed
- [ ] Prioritize refresh candidates (lowest confidence + highest importance)
- [ ] Execute selective refresh (3-5 banks minimum)
- [ ] Update framework document validity notice

---

## Research Metadata Requirements

Every bank assessment **must** include:

```markdown
### Research Metadata

| Field | Value |
|-------|-------|
| **Research Date** | [YYYY-MM-DD] |
| **Researcher** | [Name/System] |
| **Protocol Version** | [v2.x] |
| **Valid Until** | [Research Date + 6 months] |
| **Current Status** | [Current/Aging/Dated/Stale/Expired] |
| **Confidence Decay Applied** | [None / -X%] |
| **Adjusted Confidence** | [Original]% → [Adjusted]% |
| **Last Trigger Check** | [YYYY-MM-DD] |
| **Staleness Triggers Active** | [None / List] |
| **Next Scheduled Refresh** | [YYYY-MM-DD] |
```

---

## Framework Document Validity Notice

Include at top of framework document:

```markdown
> ## Research Currency Notice
> 
> **International bank assessments**
> - Last comprehensive update: [Date]
> - Validity status: [Current / Aging / Stale]
> - Next scheduled refresh: [Date]
> 
> **Recent updates incorporated:**
> - [Date]: [Bank] — [What changed]
> - [Date]: [Bank] — [What changed]
> 
> **Pending triggers to address:**
> - [Trigger] — Affects [Banks] — Refresh by [Date]
> 
> **Usage guidance:**
> - Classifications marked "Current" may be cited without caveat
> - Classifications marked "Aging" should note "as of [date]"
> - Classifications marked "Stale" require refresh before strategic use
```

---

## Citation Formats by Validity

### Current Research (0-6 months)

**Internal Use:**
> Deutsche Bank is classified as PRAGMATIST (Regulatory-driven) with 70% confidence.

**Client-Facing:**
> "Deutsche Bank's current positioning suggests they will adopt CDM when regulatory requirements demand it, rather than building proprietary capability."

### Aging Research (6-9 months)

**Internal Use:**
> Deutsche Bank was classified as PRAGMATIST (Regulatory-driven) with 70% confidence (as of [Date], -10% decay applied → 60% effective confidence).

**Client-Facing:**
> "As of [Date], Deutsche Bank's positioning suggested regulatory-driven adoption. We recommend validating this assessment given [time elapsed / relevant developments]."

### Stale Research (9-12 months)

**Internal Use:**
> ⚠️ STALE: Deutsche Bank classification requires refresh. Historical assessment: PRAGMATIST (Regulatory-driven), 70% original confidence, now 55% effective. Do not use for strategic decisions without refresh.

**Client-Facing:**
> "Our last assessment of Deutsche Bank is from [Date]. Given the time elapsed, we recommend a refresh before relying on this classification for strategic planning."

### Expired Research (>12 months)

**Internal Use:**
> 🚫 EXPIRED: Deutsche Bank classification is invalid. Refresh required before any use.

**Client-Facing:**
> [Do not cite. Execute refresh first.]

---

## Refresh Execution Protocol

### Selective Refresh (Single Bank)

1. Re-execute Deep Research prompt for bank
2. Apply Bayesian analysis in Claude Standard
3. Compare to previous classification
4. Document change rationale if classification changed
5. Update metadata
6. Update framework document

**Time estimate:** 45-60 minutes per bank

### Phase Refresh (Regional Group)

1. Re-execute all bank prompts in phase
2. Run phase synthesis
3. Check cross-bank consistency
4. Update all metadata
5. Update framework regional section

**Time estimate:** 4-6 hours per phase

### Full Refresh (All Banks)

1. Execute complete research protocol
2. Full cross-bank analysis
3. Complete framework update
4. Reset all validity dates

**Time estimate:** 20-25 hours

---

## Refresh Priority Matrix

When refresh capacity is limited, prioritize:

| Priority | Criteria | Banks |
|----------|----------|-------|
| **Critical** | Trigger event occurred | [Affected banks] |
| **High** | <50% confidence + High strategic importance | [List] |
| **High** | Expired + used in active client work | [List] |
| **Medium** | Stale + Medium strategic importance | [List] |
| **Medium** | Aging + Low confidence | [List] |
| **Lower** | Aging + High confidence | [List] |
| **Defer** | Current + Not in active use | [List] |

---

## Change Log Template

Maintain running log of research updates:

```markdown
## Research Change Log

### [YYYY-MM-DD] — [Bank Name]

**Trigger:** [What prompted refresh]
**Previous:** [Classification] @ [Confidence]%
**Updated:** [Classification] @ [Confidence]%
**Change:** [Upgraded / Downgraded / Confirmed / Refined]
**Rationale:** [Brief explanation]
**Key New Evidence:** [What was found]

---
```

---

## Annual Review Checklist

Every 12 months, execute:

- [ ] Full refresh of all banks
- [ ] Protocol effectiveness review
  - Did confidence levels prove accurate?
  - Were any classifications dramatically wrong?
  - What sources proved most/least valuable?
- [ ] Trigger monitoring effectiveness
  - Did we catch all significant events?
  - Any false positives/negatives?
- [ ] Update likelihood ratios if calibration needed
- [ ] Update ecosystem documents (utilities, vendors)
- [ ] Archive previous year's research
- [ ] Reset validity dates
