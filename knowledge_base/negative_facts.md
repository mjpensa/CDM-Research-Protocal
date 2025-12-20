# Negative Facts Knowledge Base

**Last Updated**: 2025-12-19
**Purpose**: Prevent wasted research by documenting proven dead ends, false leads, and debunked claims.
**Usage**: Check this file during Pre-Flight (Step 1) before executing search strategies.

---

## A. Dead End Search Patterns

### Bank-Agnostic Searches (Skip Globally)

| Query Pattern | Why It Fails | Better Alternative |
|--------------|--------------|-------------------|
| `"[Bank] derivatives reporting"` | Too vague; returns compliance articles, not CDM evidence | `"[Bank] ISDA CDM"` or `"[Bank] EMIR Refit CDM"` |
| `"[Bank] technology modernization"` | Too broad; dilutes CDM signal in noise | `"[Bank] Common Domain Model"` |
| `"[Bank] FINOS"` alone | Returns non-CDM FINOS projects (Fluxnova, Waltz, Legend) | `"[Bank] FINOS CDM"` or check specific CDM repos |
| `"[Bank] regulatory technology"` | RegTech is too broad; includes KYC, AML, sanctions | `"[Bank] trade reporting CDM"` |
| `"CDM implementation case study"` | Returns only vendor marketing, not actual bank evidence | Search specific bank names directly |

### Jurisdiction-Specific Dead Ends

| Jurisdiction | Pattern to Avoid | Reason | Better Approach |
|-------------|-----------------|--------|-----------------|
| **Swiss banks** | `site:[bank.com] CDM` | Swiss discretion norms; no public CDM positioning | Check ISDA/FINOS repos and trade press first |
| **Japanese banks** | English press for CDM details | Language barrier; internal work not publicized in English | Check Japanese trade publications or ISDA Asia events |
| **UK regional** | Innovation press releases | Focus on retail banking, not derivatives | Target trade press (Risk.net) specifically |
| **German banks** | English-only searches | Technical documentation often in German | Include German terms: "Derivateberichterstattung" |

---

## B. False Leads Registry

### Fluxnova ≠ CDM

- **Misleading Signal**: `"[Bank] Fluxnova participation"` or `"[Bank] FINOS workflow"`
- **Reality**: Fluxnova is a FINOS project for **process orchestration**, NOT data modeling
- **Why It Confuses**: Both are FINOS projects; casual mentions conflate them
- **Lesson**: Always verify the specific FINOS project is CDM-related
- **Banks affected**: Any FINOS member (many participate in non-CDM projects)

### Waltz ≠ CDM

- **Misleading Signal**: `"[Bank] FINOS Waltz"`
- **Reality**: Waltz is a FINOS project for **enterprise architecture visualization**
- **Lesson**: FINOS membership doesn't imply CDM engagement

### Legend ≠ CDM

- **Misleading Signal**: `"[Bank] FINOS Legend"` or `"[Bank] Goldman Sachs Legend"`
- **Reality**: Legend is a data modeling platform that **could** use CDM but isn't CDM itself
- **Lesson**: Distinguish CDM-compatible tools from CDM adoption evidence

### Vendor Claims Without Bank Confirmation

- **Misleading Signal**: `"Vendor X announces Bank Y uses our CDM solution"`
- **Reality**: Vendor marketing incentive; bank may use non-CDM portion of vendor's product
- **Lesson**: Always require **bank-side** confirmation for Tier 1/2 classification
- **Example**: Delta Capita claiming "CDM-native" requires HSBC to confirm scope

### DerivHack Participation

- **Misleading Signal**: `"[Bank] won DerivHack 2018"` or `"[Bank] DerivHack finalist"`
- **Reality**: Hackathon participation demonstrates **awareness**, not production adoption
- **Lesson**: Check for sustained follow-through post-event (2+ years of continued activity)
- **Example**: Many 2018/2019 DerivHack participants show no subsequent CDM activity

### Working Group Membership

- **Misleading Signal**: `"[Bank] ISDA CDM working group member"`
- **Reality**: Membership indicates **observer** status; many members never implement
- **Lesson**: Classify as `membership_or_participation` (Tier 2), not `production_usage`

---

## C. Debunked Claims

| Claim | Source | Debunking Evidence | Lesson |
|-------|--------|-------------------|--------|
| _Template - add as discovered_ | | | |

### How to Add Entries

When a claim is debunked during research:
1. Document the original claim exactly
2. Note where it appeared (URL, date)
3. Record what evidence contradicted it
4. Extract the generalizable lesson

---

## D. Informative Absences

### Absence = Evidence (Informative)

These searches, when yielding nothing, tell us something meaningful:

| Search | What We'd Expect If True | Implication of Absence |
|--------|-------------------------|----------------------|
| `"[Bank]" site:github.com/finos/common-domain-model` | ARCHITECT banks contribute code | Absence suggests not actively contributing |
| `"[Bank]" ISDA CDM steering committee` | Governance-level banks are listed | Absence suggests not in leadership |
| `"[Bank]" CDM production` | Production users eventually announce | Continued absence suggests no production deployment |
| `"[Bank]" DRR pilot` | Pilot participants are documented | Absence suggests not participating |

### Absence ≠ Evidence (Uninformative)

These absences don't tell us anything reliable:

| Search | Why Uninformative |
|--------|------------------|
| `"[Swiss Bank] CDM announcement"` | Swiss banking culture avoids public technology positioning |
| `"[Japanese Bank] CDM" English press` | Language barrier; internal work won't appear in English |
| `"[Bank] CDM" site:[bank.com]` | Most banks don't publicize technology choices on corporate sites |
| `"[Private Bank] CDM strategy"` | Private banks have minimal public disclosure |

---

## E. Vendor Domain Cautions

When evidence comes from these domains, apply extra scrutiny:

| Vendor Domain | Caution | Required Corroboration |
|--------------|---------|----------------------|
| murex.com | Vendor marketing | Bank confirmation of Murex CDM module adoption |
| calypso.com | Vendor marketing | Bank confirmation of specific CDM features |
| finastra.com | Vendor marketing | Bank deployment confirmation |
| deltacapita.com | Vendor marketing | Bank confirmation of CDM-native services |
| regnosys.com | CDM tooling vendor | Bank project confirmation |

**Rule**: Vendor press releases alone = Tier 2 `vendor_proxy_signal` at best, never `production_usage`.

---

## F. Time Savings Estimates

| Pattern Avoided | Hours Saved per Bank |
|----------------|---------------------|
| Swiss site-restricted searches | 2-3 hours |
| Vendor claim verification rabbit holes | 1-2 hours |
| FINOS project disambiguation | 1 hour |
| Jurisdiction-calibrated search order | 2-4 hours |
| DerivHack/hackathon overweighting | 0.5 hours |
| Working group vs. implementation confusion | 0.5 hours |

**Phase 1 savings estimate**: ~15-20 hours across 5 banks
**Cumulative benefit**: Each phase learns from previous; Phase 3+ saves 30-40% more

---

## G. Pattern Recognition by Phase

### Phase 1: European Tier 1 (Completed)
- _Add learnings after Phase 1 completion_

### Phase 2: UK Regional
- _Add learnings after Phase 2 completion_

### Phase 3: Japanese
- _Add learnings after Phase 3 completion_

---

## H. How to Update This File

After completing each bank's research:

1. **Document any null searches** that consumed >30 minutes without results
2. **Record any false leads** that initially seemed promising but proved misleading
3. **Note any debunked claims** where initial evidence was later contradicted
4. **Update jurisdiction patterns** if a new regional pattern emerges
5. **Add time savings** estimate for patterns that would have wasted effort

### Entry Template

```markdown
### [Pattern Name]

- **Misleading Signal**: What the search/evidence appeared to show
- **Reality**: What was actually true
- **Why It Confuses**: Why this false positive occurs
- **Lesson**: How to avoid in future
- **Banks affected**: Which banks this applies to
- **Time wasted**: How much time this cost (for prioritization)
```

---

_This document is a living registry. Update after each bank completes research._
