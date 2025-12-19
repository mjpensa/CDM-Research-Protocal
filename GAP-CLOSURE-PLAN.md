# Gap Closure Plan: CDM/DRR International Bank Research Protocol

## Executive Summary

This plan addresses 10 identified gaps in the research protocol, organized into 4 workstreams executed over 2-3 days before research begins.

| Workstream | Gaps Addressed | Time | Dependencies |
|------------|----------------|------|--------------|
| **A: Validation & Alignment** | #1, #2 | 2-3 hours | None — do first |
| **B: Strategic Translation** | #3, #4, #5 | 4-5 hours | Workstream A |
| **C: Analytical Enrichment** | #6, #7, #8 | 3-4 hours | Workstream A |
| **D: Ecosystem Mapping** | #9, #10 | 3-4 hours | Can parallel with B/C |

**Total Estimated Time:** 12-16 hours

---

# WORKSTREAM A: Validation & Alignment
## Gaps #1 and #2 (Critical — Execute First)

---

## Gap #1: Test Deep Research Source Access

### Objective
Verify Deep Research can access the source types our protocol depends on before investing 20+ hours in research.

### Test Protocol

**Test Bank:** Barclays (chosen because we have known evidence to verify against)

**Known Evidence to Find:**
- FINOS contributor status
- 2018 BOE/FCA DRR pilot participation
- Any ISDA working group participation

**Test Prompt:**
```
Research Barclays' participation in CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) initiatives.

Specifically search for and report on:

1. FINOS CONTRIBUTION
- Search FINOS.org for Barclays mentions
- Search GitHub FINOS repositories for Barclays contributors
- Report: Is Barclays listed as contributor? Any specific commits or contributions found?

2. REGULATORY PILOT PARTICIPATION  
- Search for Barclays participation in 2018 BOE/FCA DRR pilot
- Search FCA.org.uk and BankofEngland.co.uk for pilot documentation
- Report: Evidence of participation found?

3. ISDA ENGAGEMENT
- Search ISDA.org for Barclays mentions in CDM context
- Search for Barclays speakers at ISDA events
- Report: Any ISDA CDM working group participation?

4. TRADE PRESS COVERAGE
- Search Risk.net for "Barclays CDM" or "Barclays DRR"
- Search Waters Technology for same
- Report: Can you access these publications? What did you find?

5. OFFICIAL SOURCES
- Search for Barclays annual report 2023 or 2024 technology sections
- Report: Can you access/summarize relevant sections?

For each source type, explicitly report:
- Could you access it? (Yes/No/Partial)
- What did you find? (Summary)
- Any access limitations? (Paywall, blocked, etc.)
```

### Success Criteria

| Source Type | Minimum Acceptable | Ideal |
|-------------|-------------------|-------|
| FINOS.org | Can access, finds contributor status | Finds specific contribution details |
| GitHub/FINOS | Can search | Finds commit history |
| FCA/BOE | Can access regulatory sites | Finds pilot documentation |
| ISDA.org | Can access | Finds working group/speaker info |
| Risk.net | At least headlines/summaries | Full article access |
| Waters Technology | At least headlines/summaries | Full article access |
| Bank annual reports | Can find/summarize | Specific technology sections |

### Decision Matrix

| Result | Action |
|--------|--------|
| All sources accessible | Proceed with full plan |
| Trade press paywalled but others work | Proceed, note Tier 2 limitation |
| FINOS/ISDA inaccessible | Major issue — consider manual research for key sources |
| Multiple failures | Reassess approach — may need Claude Code for targeted searches |

### Output
- Source access assessment document
- Adjusted confidence expectations by source type
- Protocol modifications if needed

### Time Estimate: 45-60 minutes

---

## Gap #2: Confirm Framework Document Format

### Objective
Ensure research outputs align precisely with the framework document structure.

### Information Needed

**From You (Matthew):**

1. **International Bank Table Structure**
   - What are the exact column headers?
   - What format for each field? (e.g., is "Status" a dropdown or free text?)
   - Any character limits?
   - Example row from existing content?

2. **Regional Narrative Sections**
   - What regions have dedicated sections?
   - What's the typical length/format?
   - Are there existing examples I should match?

3. **Confidence Communication**
   - How is confidence currently expressed? (%, qualitative, color-coding?)
   - Is there a legend or key for confidence levels?
   - How are uncertainties flagged?

4. **Validation/Update Tracking**
   - Is there an existing validation log format?
   - How are changes tracked? (version history, changelog?)
   - What metadata is captured?

5. **Overall Document Structure**
   - What sections exist beyond bank tables?
   - Where do international banks fit in the overall narrative?
   - Any cross-references to maintain?

### Template Alignment Checklist

Once I have the framework format, I'll update:

| Template | Alignment Check |
|----------|----------------|
| `per-bank-output.md` | Add exact field mapping |
| `framework-integration.md` | Match table structure precisely |
| `phase-synthesis.md` | Match regional section format |
| `cross-bank-patterns.md` | Match executive summary style |

### Action Required
**Please provide:**
1. Screenshot or copy of the international bank table structure
2. Example of a regional narrative section
3. Confirmation of confidence expression format

### Time Estimate: 30-45 minutes (depending on information availability)

---

# WORKSTREAM B: Strategic Translation
## Gaps #3, #4, #5 (High Priority)

---

## Gap #3: Add "Client Implications" to Output Template

### Objective
Translate every classification into actionable strategic implications for US bank clients.

### Client Implication Framework

**Primary US Bank Clients (Assumed):**
- JPMorgan Chase
- Goldman Sachs
- Morgan Stanley
- Citigroup
- Bank of America

**Implication Categories:**

| Category | Question Answered |
|----------|-------------------|
| **Counterparty Connectivity** | How does this bank's CDM status affect transaction processing with US counterparts? |
| **Competitive Intelligence** | What does this positioning reveal about their strategic priorities? |
| **Network Effects** | Does this bank accelerate or slow CDM network adoption? |
| **Partnership/Utility** | Is this bank a potential partner, utility investor, or neither? |
| **Risk Consideration** | Does this positioning create any operational or regulatory risk? |

### Client Implications Template

Add to `per-bank-output.md`:

```markdown
## Client Strategic Implications

### For CDM-Native US Banks (JPMorgan, future others)

**Counterparty Connectivity Assessment:**
- Current friction level: [High/Medium/Low/None]
- Expected evolution: [Improving/Stable/Unknown]
- Timeline to CDM compatibility: [Estimate or "Unknown"]

**Implication:** [1-2 sentences on what this means for transaction processing]

---

### For CDM-Building US Banks (Most Tier 1)

**Competitive Intelligence:**
- Is [Bank] ahead, behind, or parallel to typical US Tier 1? [Assessment]
- Strategic signal: [What does their positioning reveal?]
- Watch for: [What would indicate strategic shift?]

**Implication:** [1-2 sentences on competitive positioning insight]

---

### For Utility/Infrastructure Decisions

**Network Value Assessment:**
- Does [Bank]'s positioning accelerate CDM adoption? [Yes/No/Neutral]
- Are they a potential utility investor/partner? [Yes/No/Unlikely]
- Critical mass contribution: [Significant/Marginal/None]

**Implication:** [1-2 sentences on network/utility strategy relevance]

---

### For Regulatory Strategy

**Jurisdictional Insight:**
- What does [Bank]'s approach reveal about [jurisdiction] regulatory expectations?
- Transferable learning: [Any approach worth emulating or avoiding?]

**Implication:** [1-2 sentences on regulatory strategy insight]

---

### Summary Client Action Items

| If Your Client Is... | Then This Bank's Positioning Suggests... |
|---------------------|------------------------------------------|
| Trading heavily with [Bank] | [Action/consideration] |
| Competing with [Bank] in [region] | [Action/consideration] |
| Evaluating utility investments | [Action/consideration] |
| Benchmarking their own timeline | [Action/consideration] |
```

### Classification-Specific Implication Patterns

**ARCHITECT-Native:**
```
- Counterparty: Seamless CDM connectivity available now
- Competitive: Industry leader, potential partner for others
- Network: High value node, accelerates adoption
- Utility: May be building/backing utilities
```

**ARCHITECT-Leader:**
```
- Counterparty: CDM connectivity coming [timeline]
- Competitive: Committed, will be early production
- Network: Valuable future node, worth monitoring timeline
- Utility: Potential utility investor/partner
```

**ARCHITECT-Follower:**
```
- Counterparty: CDM capability building, timeline uncertain
- Competitive: Engaged but not leading
- Network: Will contribute to critical mass eventually
- Utility: More likely consumer than investor
```

**PRAGMATIST-Vendor:**
```
- Counterparty: CDM connectivity via vendor, may be adequate
- Competitive: Not building capability, outsourcing
- Network: Passive participant, not driving adoption
- Utility: Consumer of utility services
```

**PRAGMATIST-Regulatory:**
```
- Counterparty: Will have CDM when required, not before
- Competitive: Reactive, not strategic on CDM
- Network: Will join when mandated
- Utility: Late adopter of utility services
```

**PRAGMATIST-Integration:**
```
- Counterparty: CDM deprioritized, expect delays
- Competitive: Capacity constrained, not indicative of strategy
- Network: Delayed participant
- Utility: Post-integration opportunity
```

### Time Estimate: 1.5-2 hours

---

## Gap #4: Add Executive Summary Layer

### Objective
Create C-suite-ready summaries that translate analytical outputs into business language.

### Executive Summary Template

Add to `per-bank-output.md`:

```markdown
## Executive Summary

### [BANK NAME] — CDM Positioning at a Glance

**Bottom Line:** [One sentence classification in plain language]

Examples:
- "Building CDM capability internally, production expected 2025-2026"
- "Waiting for industry utilities, no internal investment planned"
- "Outsourcing to Delta Capita, minimal internal capability"
- "Integration consuming all capacity, revisit post-2026"

**Confidence:** [High/Medium/Low] — [One sentence on evidence basis]

Examples:
- "High — Multiple official announcements and confirmed contributions"
- "Medium — Industry coverage consistent but no official confirmation"
- "Low — Limited public disclosure, inference from peer behavior"

**Key Evidence:**
1. [Most important finding in plain language]
2. [Second most important]
3. [Third if relevant]

**Strategic Relevance:**
- For counterparty strategy: [One sentence]
- For competitive benchmarking: [One sentence]
- For network/utility planning: [One sentence]

**Watch For:** [What development would change this assessment?]
```

### Executive Language Translation Guide

| Analytical Term | Executive Translation |
|-----------------|----------------------|
| ARCHITECT-Native | "In production, industry leader" |
| ARCHITECT-Leader | "Building capability, committed to production" |
| ARCHITECT-Follower | "Contributing to standard, production timeline unclear" |
| PRAGMATIST-Vendor | "Outsourcing to third-party solution" |
| PRAGMATIST-Regulatory | "Will adopt when mandated, not before" |
| PRAGMATIST-Integration | "Other priorities consuming capacity" |
| 90%+ confidence | "High confidence — strong evidence" |
| 70-89% confidence | "Moderate-high confidence — consistent signals" |
| 50-69% confidence | "Moderate confidence — limited direct evidence" |
| <50% confidence | "Low confidence — significant uncertainty" |
| Bayesian posterior | [Don't use — translate to confidence level] |
| Likelihood ratio | [Don't use — reference evidence strength] |
| Informative absence | "No evidence found despite thorough search" |

### Regional Executive Summaries

For phase syntheses, create regional executive summaries:

```markdown
## [Region] Executive Summary

**Regional Pattern:** [One sentence summary]

Example: "European Tier 1 banks are bifurcating — French banks following BNP 
toward internal capability, others waiting for utilities."

**Leaders:** [Bank(s)] — [Brief status]
**Mainstream:** [Bank(s)] — [Brief status]  
**Laggards:** [Bank(s)] — [Brief status]

**Client Relevance:**
- If trading heavily in [region]: [Implication]
- If competing in [region]: [Implication]

**Key Uncertainty:** [Biggest gap in regional picture]
```

### Time Estimate: 1-1.5 hours

---

## Gap #5: Add Diagnostic Engagement Briefs

### Objective
Convert low-confidence classifications into actionable business development opportunities.

### When to Create Diagnostic Brief

Create brief when:
- Confidence < 60%
- Classification is strategically important (Tier 1 bank, key counterparty)
- Validation would materially affect client recommendations

### Diagnostic Engagement Brief Template

Add to `per-bank-output.md` (conditional section):

```markdown
## Diagnostic Engagement Brief

> **Trigger:** Classification confidence is [X]%, below threshold for strategic recommendations.
> This represents a potential diagnostic engagement opportunity.

### Positioning Statement

**For Initial Outreach:**
"We're conducting research on CDM adoption patterns across major global banks 
to support strategic planning for [context — e.g., 'our financial services 
technology practice' / 'clients evaluating derivatives infrastructure investments']. 

We've mapped [X] institutions so far and are finding interesting regional patterns. 
Your institution's approach would be valuable to understand — particularly given 
[specific hook relevant to this bank]."

**Specific Hook for [BANK]:**
[Tailored hook based on what we know]

Examples:
- "...given your significant derivatives exposure and the EMIR Refit timeline"
- "...given the JSCC CDM production and its implications for clearing members"
- "...given BNP's early production and the French regulatory environment"
- "...given the Credit Suisse integration and post-integration technology priorities"

---

### Discovery Questions

**Tier 1 — Open-Ended (Start Here):**
1. "How is [Bank] thinking about derivatives data standards and regulatory reporting technology?"
2. "What's your perspective on CDM/DRR adoption timelines in [region/globally]?"
3. "How did [Bank] approach [recent regulatory milestone, e.g., EMIR Refit]?"

**Tier 2 — Probing (If Engagement Continues):**
4. "Is [Bank] building internal CDM capability, working with vendors, or evaluating options?"
5. "Are you participating in any ISDA or FINOS working groups on this?"
6. "What would accelerate or delay your CDM timeline?"

**Tier 3 — Specific (If Relationship Established):**
7. "What's your target production timeline, if any?"
8. "Who internally is driving your derivatives technology strategy?"
9. "Would you be interested in benchmarking against peer approaches?"

---

### Value Exchange

**What We Can Offer:**
- Aggregated (anonymized) view of peer positioning
- Regional pattern insights
- Regulatory timeline analysis
- Perspective on utility/infrastructure landscape

**What We're Seeking:**
- Validation of our classification hypothesis
- Understanding of internal priorities and timeline
- Insight into decision drivers
- Potential relationship for future engagement

---

### Target Contacts

**Ideal Contact Profiles:**
1. Head of Derivatives Technology / Post-Trade Technology
2. Head of Regulatory Reporting / Regulatory Change
3. Chief Data Officer (if derivatives data in scope)
4. CTO/CIO (for strategic-level conversation)

**Research Contact Paths:**
- LinkedIn search: "[Bank] + derivatives + technology + director/head"
- ISDA event speaker lists
- Industry conference attendee lists
- Client relationship leverage (if any)

---

### Engagement Logistics

**Preferred Format:** 30-minute video call or in-person if at same conference

**Timing Considerations:**
- Avoid quarter-end periods
- Post-regulatory-deadline is often good (people are reflecting)
- Conference sidebars are efficient

**Follow-Up Commitment:**
- Share relevant (non-confidential) insights from research
- Offer to reconnect when research is complete
- Provide framework document excerpt (sanitized) if appropriate

---

### Success Metrics

**Minimum Success:** Classification validated or refined with direct input
**Target Success:** Above + relationship established for future engagement  
**Stretch Success:** Above + potential project opportunity identified

---

### Uncertainty Reduction Target

**Current State:**
- Classification: [Current]
- Confidence: [X]%
- Key uncertainty: [What we don't know]

**Post-Engagement Target:**
- Classification: [Validated or revised]
- Confidence: [Target X+20%]
- Uncertainty resolved: [What we learned]
```

### Diagnostic Brief Priority Matrix

| Bank | Confidence | Strategic Importance | Priority |
|------|------------|---------------------|----------|
| [Bank with <60% confidence + high importance] | X% | High | **Create brief** |
| [Bank with <60% confidence + medium importance] | X% | Medium | Create if capacity |
| [Bank with <60% confidence + low importance] | X% | Low | Skip |
| [Bank with >60% confidence] | X% | Any | Not needed |

### Time Estimate: 2-2.5 hours (including template + priority framework)

---

# WORKSTREAM C: Analytical Enrichment
## Gaps #6, #7, #8 (Medium Priority)

---

## Gap #6: Add Counterparty Relevance Frame

### Objective
Map international banks to US client counterparty relationships to prioritize research and contextualize findings.

### Counterparty Relevance Matrix

**Step 1: Build Counterparty Map**

| International Bank | JPM | GS | MS | Citi | BofA | Overall Relevance |
|-------------------|-----|----|----|------|------|-------------------|
| Deutsche Bank | H | H | H | H | H | Critical |
| Barclays | H | H | H | H | H | Critical |
| HSBC | H | H | H | H | H | Critical |
| UBS | H | H | H | M | M | Critical |
| SocGen | M | H | M | M | M | High |
| BNP Paribas | M | H | M | H | M | High |
| Nomura | M | H | H | M | L | High |
| MUFG | M | M | H | M | M | High |
| Credit Agricole | L | M | L | M | L | Medium |
| Standard Chartered | L | L | L | M | L | Medium |
| [Others] | ... | ... | ... | ... | ... | ... |

**Legend:** H = High (significant trading relationship), M = Medium, L = Low

**Step 2: Source Counterparty Data**

Options for building this map:
1. **Client input** — Ask clients directly about key counterparties
2. **Public filings** — Check derivatives counterparty disclosures in 10-Ks
3. **Industry knowledge** — Use known market relationships
4. **Inference** — Base on geographic/product overlap

**Step 3: Add to Research Protocol**

Add to each bank prompt:

```markdown
### Counterparty Context

**Estimated US Bank Relevance:**
| US Bank | Relationship Intensity | Primary Product Areas |
|---------|----------------------|----------------------|
| JPMorgan | [H/M/L] | [Products] |
| Goldman Sachs | [H/M/L] | [Products] |
| Morgan Stanley | [H/M/L] | [Products] |
| Citigroup | [H/M/L] | [Products] |
| Bank of America | [H/M/L] | [Products] |

**Implication for Research Priority:**
[How does counterparty relevance affect research depth?]
```

**Step 4: Add to Output Template**

Add to `per-bank-output.md`:

```markdown
## Counterparty Relevance Assessment

### US Bank Counterparty Exposure

| US Bank | Relevance | CDM Connectivity Implication |
|---------|-----------|------------------------------|
| JPMorgan | [H/M/L] | [Implication given JPM's CDM status] |
| Goldman Sachs | [H/M/L] | [Implication] |
| Morgan Stanley | [H/M/L] | [Implication] |
| Citigroup | [H/M/L] | [Implication] |
| Bank of America | [H/M/L] | [Implication] |

### Connectivity Friction Assessment

**Current State:**
Given [Bank]'s [Classification] and US banks' CDM positioning:
- Transaction processing friction: [High/Medium/Low/None]
- Data reconciliation burden: [High/Medium/Low/None]
- Regulatory reporting alignment: [Aligned/Partial/Misaligned]

**Future State (12-24 months):**
Expected evolution of connectivity friction: [Improving/Stable/Worsening/Unknown]

### Priority Ranking

Based on counterparty relevance + strategic importance:
**Research Priority:** [Critical/High/Medium/Low]
**Validation Priority:** [Critical/High/Medium/Low]
```

### Time Estimate: 1.5-2 hours

---

## Gap #7: Define Visualization Requirements

### Objective
Specify visualizations needed for executive presentations and how classifications map to them.

### Required Visualizations

**Visualization 1: CDM Positioning Matrix (2x2)**

```
                    HIGH Business Case for CDM
                              │
         PRAGMATIST           │         ARCHITECT
         (Strategic Gap)      │         (Leaders)
                              │
    ──────────────────────────┼──────────────────────────
                              │
         PRAGMATIST           │         ARCHITECT
         (Rational)           │         (Over-invested?)
                              │
                    LOW Business Case for CDM
    
    LOW ←──── Current CDM Investment ────→ HIGH
```

**Mapping Rules:**
| Classification | X-Axis (Investment) | Y-Axis (Business Case) |
|----------------|---------------------|------------------------|
| ARCHITECT-Native | Far Right | Based on derivatives exposure |
| ARCHITECT-Leader | Right | Based on derivatives exposure |
| ARCHITECT-Follower | Center-Right | Based on derivatives exposure |
| PRAGMATIST-Vendor | Center | Based on derivatives exposure |
| PRAGMATIST-Regulatory | Left | Based on derivatives exposure |
| PRAGMATIST-Integration | Left (temporary) | Based on derivatives exposure |

**Data Required per Bank:**
- Classification (determines X position)
- Derivatives exposure metric (determines Y position)
- Label for plot point

---

**Visualization 2: Regional Heat Map**

```
┌─────────────────────────────────────────────────────────┐
│                    CDM ENGAGEMENT BY REGION             │
├─────────────┬─────────────┬─────────────┬──────────────┤
│   EUROPE    │     UK      │    JAPAN    │  OTHER ASIA  │
├─────────────┼─────────────┼─────────────┼──────────────┤
│ ████████░░  │ ██████████  │ ████████░░  │ ████░░░░░░   │
│ 65% engaged │ 80% engaged │ 70% engaged │ 40% engaged  │
├─────────────┴─────────────┴─────────────┴──────────────┤
│ Legend: ██ = Architect  ░░ = Pragmatist               │
└─────────────────────────────────────────────────────────┘
```

**Data Required:**
- Region assignment per bank
- Classification per bank
- Aggregation formula (% Architect by region)

---

**Visualization 3: Confidence Distribution**

```
CLASSIFICATION CONFIDENCE DISTRIBUTION

High (>80%)    ████████████░░░░░░░░  40% (8 banks)
Medium (50-80%) ██████████████░░░░░░  45% (9 banks)  
Low (<50%)     ███░░░░░░░░░░░░░░░░░  15% (3 banks)

Banks requiring validation: Deutsche Bank, UBS, [others]
```

**Data Required:**
- Confidence % per bank
- Threshold definitions

---

**Visualization 4: Timeline/Trajectory View**

```
CDM PRODUCTION TIMELINE

2022 ──●─────────────────────────────────────────────
       BNP Paribas (LIVE)

2024 ────────●───●───────────────────────────────────
             │   JPMorgan (LIVE)
             Pictet (LIVE)

2025 ────────────────●───○───○───○───────────────────
                     │   │   │   Expected production
                   JSCC  │   │   (various banks)
                     (LIVE)  │
                             Barclays? Deutsche Bank?

2026 ────────────────────────────○───○───○───────────
                                 Expected production
                                 (later movers)

Legend: ● = Confirmed  ○ = Expected/Projected
```

**Data Required:**
- Production status per bank
- Timeline (actual or projected)
- Confidence in timeline

---

**Visualization 5: Counterparty Network Graph**

```
        ┌─────────┐
        │   JPM   │ (CDM Production)
        └────┬────┘
             │ High volume
    ┌────────┼────────┐
    │        │        │
┌───▼──┐ ┌───▼──┐ ┌───▼──┐
│  DB  │ │ BARC │ │  UBS │
│(Prag)│ │(Arch)│ │(Prag)│
└──────┘ └──────┘ └──────┘

Friction: HIGH   LOW    HIGH
```

**Data Required:**
- Counterparty relationships
- Classification per bank
- Implied friction level

---

### Visualization Data Export Template

Add to `framework-integration.md`:

```markdown
## Visualization Data Export

### For Positioning Matrix
| Bank | Classification | X-Score (1-5) | Y-Score (Derivatives %) | Label |
|------|---------------|---------------|-------------------------|-------|
| [Bank] | [Class] | [Score] | [%] | [Short name] |

### For Regional Heat Map
| Region | Total Banks | Architects | Pragmatists | % Engaged |
|--------|-------------|------------|-------------|-----------|
| [Region] | [N] | [N] | [N] | [%] |

### For Confidence Distribution
| Confidence Band | Count | Banks |
|-----------------|-------|-------|
| High (>80%) | [N] | [List] |
| Medium (50-80%) | [N] | [List] |
| Low (<50%) | [N] | [List] |

### For Timeline View
| Bank | Status | Date | Confidence |
|------|--------|------|------------|
| [Bank] | [Live/Expected/Unknown] | [Date] | [%] |
```

### Time Estimate: 1-1.5 hours

---

## Gap #8: Document Temporal Decay/Refresh Plan

### Objective
Establish when research becomes stale and what triggers updates.

### Research Validity Framework

Add new document `RESEARCH-VALIDITY.md`:

```markdown
# Research Validity and Refresh Protocol

## Validity Period

### Standard Validity
- **Full validity:** 6 months from research date
- **Reduced validity:** 6-12 months (apply -10% confidence)
- **Stale:** >12 months (flag for refresh, do not cite without caveat)

### Accelerated Staleness Triggers

These events make research stale IMMEDIATELY regardless of age:

| Trigger Event | Banks Affected | Required Action |
|---------------|----------------|-----------------|
| New CDM production announcement | Announcing bank + regional peers | Refresh affected banks |
| Major M&A announcement | Both parties | Refresh both banks |
| Regulatory mandate announced | All banks in jurisdiction | Refresh jurisdiction |
| CCP CDM production | All clearing members | Refresh affected banks |
| Major vendor partnership | Bank involved | Refresh bank |

### Confidence Decay Schedule

| Age | Confidence Adjustment | Recommended Action |
|-----|----------------------|-------------------|
| 0-3 months | None | Current |
| 3-6 months | -5% | Monitor for triggers |
| 6-9 months | -10% | Plan refresh |
| 9-12 months | -15% | Execute refresh |
| >12 months | -25% | Required refresh |

---

## Refresh Protocol

### Quarterly Review (Recommended)

Every 3 months, execute:

1. **Trigger Scan**
   - Check ISDA news for production announcements
   - Check FINOS for new contributors
   - Check regulatory calendars for upcoming deadlines
   - Check trade press for major partnerships/initiatives

2. **Selective Refresh**
   - Re-research any bank with trigger event
   - Re-research lowest-confidence banks
   - Re-research strategically critical banks

3. **Confidence Adjustment**
   - Apply decay schedule to all non-refreshed banks
   - Update "as of" dates in framework

### Annual Full Refresh (Required)

Every 12 months, execute full research protocol on all banks.

---

## Research Metadata

Every bank assessment must include:

```markdown
### Research Metadata

- **Research Date:** [YYYY-MM-DD]
- **Valid Until:** [Research Date + 6 months]
- **Confidence Decay Applied:** [None / -X%]
- **Last Trigger Check:** [Date]
- **Next Scheduled Refresh:** [Date]
- **Staleness Triggers Active:** [List any applicable]
```

---

## Staleness Alert System

### For Framework Document

Include staleness header:

```markdown
> **Research Currency Notice**
> 
> International bank assessments last updated: [Date]
> Validity status: [Current / Aging / Stale]
> Next scheduled refresh: [Date]
> 
> Recent trigger events incorporated: [List or "None"]
> Pending trigger events to incorporate: [List or "None"]
```

### For Individual Bank Citations

When citing a bank's classification:

| Validity Status | Citation Format |
|-----------------|-----------------|
| Current | "[Bank] is classified as [Classification] (as of [Date])" |
| Aging | "[Bank] was classified as [Classification] (as of [Date], refresh pending)" |
| Stale | "Historical assessment: [Bank] was [Classification] (as of [Date], REQUIRES REFRESH)" |
```

### Time Estimate: 45 minutes - 1 hour

---

# WORKSTREAM D: Ecosystem Mapping
## Gaps #9 and #10 (Lower Priority, Can Parallel)

---

## Gap #9: Expand Utility/Infrastructure Mapping

### Objective
Create comprehensive inventory of CDM utilities/infrastructure that affects bank decisions.

### Utility/Infrastructure Inventory

Create new document `ECOSYSTEM-UTILITIES.md`:

```markdown
# CDM Ecosystem: Utilities and Infrastructure

## Production Infrastructure

### Central Counterparties (CCPs)

| CCP | CDM Status | Go-Live | Geography | Clearing Members Affected |
|-----|------------|---------|-----------|---------------------------|
| JSCC | **PRODUCTION** | June 2025 | Japan | Nomura, MUFG, Mizuho, SMBC, global banks with Japan exposure |
| LCH | Evaluating | TBD | Global | Most major dealers |
| CME | Evaluating | TBD | US/Global | Most major dealers |
| Eurex | Evaluating | TBD | Europe | European dealers |
| ICE | Unknown | TBD | US/Europe | Major dealers |

**Implication:** CCP CDM production creates structural requirement for clearing members.

---

### Trade Repositories

| Repository | CDM Status | Geography | Reporting Parties Affected |
|------------|------------|-----------|----------------------------|
| DTCC GTR | Evaluating CDM | Global | Global dealers |
| Regis-TR | Unknown | Europe | European reporters |
| KDPW | Unknown | Europe | Regional reporters |

**Implication:** Trade repository CDM adoption affects reporting technology choices.

---

### CDM-Native Utilities

| Utility | Status | Services | Known Clients |
|---------|--------|----------|---------------|
| **Delta Capita / Fragmos Chain** | Production | Regulatory reporting, CDM transformation | HSBC (confirmed Jan 2025) |
| **REGnosys** | Production | CDM tooling, Rosetta DSL | Technology provider |
| **ISDA Digital** | Production | Reference data, CDM tools | Industry utility |

**Implication:** Utility availability enables Pragmatist-Vendor path.

---

## Standards Bodies and Governance

### ISDA

| Body | CDM Role | Key Members |
|------|----------|-------------|
| CDM Steering Committee | Governance | Major dealers |
| CDM Working Groups | Technical development | Contributors |
| ISDA Board | Strategic direction | Industry leaders |

### FINOS

| Body | CDM Role | Key Contributors |
|------|----------|------------------|
| CDM Project | Open source development | Standard Chartered, Barclays, others |
| Technical Oversight Committee | Technical governance | Elected contributors |

---

## Bank-Utility Relationships

| Bank | Known Utility Relationships | Implication |
|------|----------------------------|-------------|
| HSBC | Delta Capita (Jan 2025) | Pragmatist-Vendor likely |
| BNP Paribas | Internal + ? | Built internally |
| JPMorgan | Internal + ? | Built internally |
| [Others] | Research finding | [Implication] |

---

## Geographic Coverage

| Region | Available Utilities | CCP CDM Status | Regulatory Driver |
|--------|--------------------|--------------------|-------------------|
| Japan | JSCC | Production | JFSA |
| EU | Delta Capita, others | CCPs evaluating | EMIR Refit |
| UK | Delta Capita, others | CCPs evaluating | UK EMIR |
| US | Limited | CCPs evaluating | CFTC |
| APAC ex-Japan | Limited | N/A | MAS, HKMA |

**Implication:** Utility availability varies by region, affecting build vs. buy decisions.
```

### Integration with Bank Research

Add to each bank prompt:

```markdown
### Utility/Infrastructure Context

**Relevant CCPs:** [List CCPs this bank clears through]
**CCP CDM Status:** [Production/Evaluating/Unknown]
**Available Utilities in Region:** [List]
**Known Utility Relationships:** [If any from prior knowledge]

**Research Focus:** Identify any utility/vendor relationships as part of classification.
```

### Time Estimate: 1.5-2 hours

---

## Gap #10: Add Vendor Landscape Layer

### Objective
Map CDM vendor ecosystem and vendor-bank relationships to support Pragmatist-Vendor classifications.

### Vendor Landscape Document

Create new document `ECOSYSTEM-VENDORS.md`:

```markdown
# CDM Vendor Landscape

## CDM-Native/Specialized Vendors

### Tier 1: Full CDM Solutions

| Vendor | Solution | CDM Capability | Known Clients | Geographic Focus |
|--------|----------|----------------|---------------|------------------|
| **Delta Capita** | Regulatory reporting utility | Native CDM, full transformation | HSBC | Global |
| **Fragmos Chain** | Post-trade utility | Native CDM, DLT-based | [Research] | Europe |
| **REGnosys** | Rosetta DSL, CDM tooling | CDM development platform | Technology clients | Global |

### Tier 2: CDM-Integrated Solutions

| Vendor | Solution | CDM Capability | Known Clients |
|--------|----------|----------------|---------------|
| **[Vendor]** | [Solution] | [Capability] | [Clients] |

### Tier 3: Traditional + CDM Roadmap

| Vendor | Solution | CDM Roadmap | Known Clients |
|--------|----------|-------------|---------------|
| **[Traditional vendor]** | [Solution] | [Planned/Evaluating] | [Clients] |

---

## Vendor Evaluation Criteria

For Pragmatist-Vendor classifications, assess vendor on:

| Criterion | Question | Rating |
|-----------|----------|--------|
| CDM Maturity | Is solution CDM-native or wrapper? | [Native/Integrated/Wrapper] |
| Production Readiness | In production at other clients? | [Yes/Pilot/No] |
| Geographic Coverage | Does it cover bank's jurisdictions? | [Full/Partial/Limited] |
| Regulatory Alignment | Validated against regulatory requirements? | [Yes/Partial/No] |
| Scalability | Can it handle bank's volumes? | [Yes/Unknown/No] |

---

## Vendor-Bank Relationship Mapping

| Bank | Vendor | Relationship Type | Evidence | Date |
|------|--------|-------------------|----------|------|
| HSBC | Delta Capita | Contract signed | Press release | Jan 2025 |
| [Bank] | [Vendor] | [Type] | [Source] | [Date] |

---

## Market Dynamics

### Vendor Consolidation
[Track any M&A in vendor space]

### New Entrants
[Track new vendors entering CDM space]

### Technology Partnerships
[Track vendor-vendor partnerships, e.g., data providers + CDM platforms]

---

## Implications for Bank Classification

| Vendor Relationship Pattern | Classification Implication |
|----------------------------|---------------------------|
| Contract with CDM-native vendor | PRAGMATIST-Vendor confirmed |
| Evaluating multiple vendors | PRAGMATIST-Vendor likely |
| Partnership with traditional vendor adding CDM | PRAGMATIST-Vendor (weaker) |
| No vendor signals, building internally | ARCHITECT likely |
| Both vendor + internal development | ARCHITECT with vendor acceleration |
```

### Integration with Bank Research

Add to each bank prompt:

```markdown
### Vendor Relationship Research

**Search for:**
- Vendor announcements naming this bank as client
- Bank announcements of vendor partnerships
- RFP or vendor selection news
- Trade press coverage of build vs. buy decision

**Classification Implication:**
- Vendor contract found → Supports PRAGMATIST-Vendor
- No vendor relationship + internal signals → Supports ARCHITECT
- Both vendor + internal → ARCHITECT with vendor layer
```

### Time Estimate: 1.5-2 hours

---

# Implementation Schedule

## Recommended Execution Order

### Day 1 (4-6 hours)

| Time | Activity | Deliverable |
|------|----------|-------------|
| Hour 1 | Gap #1: Test Deep Research | Source access assessment |
| Hour 1.5 | Gap #2: Confirm framework format | Alignment requirements |
| Hour 2-3.5 | Gap #3: Client Implications template | Updated output template |
| Hour 4-5.5 | Gap #4: Executive summary layer | Executive translation guide |

### Day 2 (4-6 hours)

| Time | Activity | Deliverable |
|------|----------|-------------|
| Hour 1-3 | Gap #5: Diagnostic engagement briefs | Brief template + priority framework |
| Hour 3.5-5 | Gap #6: Counterparty relevance frame | Counterparty matrix + template updates |
| Hour 5-6 | Gap #8: Temporal decay plan | RESEARCH-VALIDITY.md |

### Day 3 (4 hours)

| Time | Activity | Deliverable |
|------|----------|-------------|
| Hour 1-2.5 | Gap #7: Visualization requirements | Visualization specs + data export template |
| Hour 2.5-4 | Gaps #9-10: Ecosystem mapping | ECOSYSTEM-UTILITIES.md, ECOSYSTEM-VENDORS.md |

### Day 4+

Begin research execution with enhanced protocol.

---

## Dependencies

```
Gap #1 (Test DR) ──┬──► Gap #3 (Client Implications)
                   │
Gap #2 (Format)  ──┼──► Gap #4 (Executive Summary)
                   │
                   ├──► Gap #5 (Diagnostic Briefs)
                   │
                   ├──► Gap #6 (Counterparty)
                   │
                   └──► Gap #7 (Visualization)

Gap #9 (Utilities) ──► Integrated into bank prompts
Gap #10 (Vendors) ──► Integrated into bank prompts

Gap #8 (Temporal) ──► Standalone, no dependencies
```

---

## Success Criteria

| Gap | Success Metric |
|-----|----------------|
| #1 | Deep Research can access ≥5/7 source types |
| #2 | Output templates match framework exactly |
| #3 | Every classification has client implications |
| #4 | Every output has executive-ready summary |
| #5 | All <60% confidence banks have diagnostic briefs |
| #6 | Counterparty relevance rated for all banks |
| #7 | All visualizations have data export ready |
| #8 | Validity metadata on every assessment |
| #9 | Utility inventory complete with bank relationships |
| #10 | Vendor landscape documented with bank mapping |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Gap #1 fails (Deep Research can't access sources) | Pivot to Claude Code for targeted searches; accept lower source depth |
| Gap #2 reveals major format mismatch | Redesign output templates before proceeding |
| Gaps #9-10 reveal unknown utilities/vendors | Add to ecosystem docs as discovered during research |
| Time overrun | Prioritize Gaps #1-5 (critical/high); defer #9-10 if needed |
