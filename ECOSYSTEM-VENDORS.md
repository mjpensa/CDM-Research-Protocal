# CDM Vendor Landscape

## Purpose

This document maps the CDM vendor ecosystem to support PRAGMATIST-Vendor classifications and understand bank build vs. buy decisions.

---

## Vendor Taxonomy

### Tier 1: CDM-Native Solution Providers

These vendors offer solutions built on CDM from the ground up.

| Vendor | Primary Solution | CDM Capability | Deployment Model | Geographic Focus |
|--------|------------------|----------------|------------------|------------------|
| **Delta Capita** | Regulatory reporting utility | Native CDM transformation and reporting | Managed service | Global |
| **Fragmos Chain** | Post-trade processing | Native CDM with DLT settlement | Platform | Europe initially |
| **REGnosys** | Rosetta DSL platform | CDM modeling and validation | Platform/tools | Global |

#### Delta Capita — Deep Dive

**Overview:** Leading CDM-native regulatory reporting utility

**Key Capabilities:**
- Trade capture and normalization
- CDM transformation
- Multi-jurisdictional regulatory reporting
- Managed service model

**Known Clients:**
- HSBC (announced January 2025)
- [Research for others]

**Business Model:** Utility/managed service — bank outsources reporting to Delta Capita

**Classification Implication:** Bank using Delta Capita = PRAGMATIST-Vendor (unless also building internal)

**Research Signals:**
- Press releases mentioning bank as client
- Bank job postings referencing Delta Capita
- Trade press coverage of implementation

---

#### Fragmos Chain — Deep Dive

**Overview:** DLT-based post-trade utility using CDM

**Key Capabilities:**
- Post-trade processing
- CDM-native data model
- DLT for settlement finality
- Cross-party reconciliation

**Known Clients:** [Research needed]

**Business Model:** Network utility — banks join network

**Classification Implication:** Fragmos participant = PRAGMATIST-Vendor or ARCHITECT (if also building)

---

#### REGnosys — Deep Dive

**Overview:** CDM tooling and Rosetta DSL maintainer

**Key Capabilities:**
- Rosetta DSL (domain-specific language for CDM)
- CDM validation and testing tools
- Model development environment
- Technical consulting

**Role:** Technology provider to banks building CDM capability

**Classification Implication:** REGnosys client could be either:
- ARCHITECT (using tools to build internally)
- Vendor building CDM solution

---

### Tier 2: CDM-Integrated Vendors

These vendors have integrated CDM into existing solutions.

| Vendor | Primary Solution | CDM Capability | Integration Status |
|--------|------------------|----------------|-------------------|
| **Acadia** | Margin/collateral | CDM integration planned | In development |
| **TriOptima** | Compression/optimization | CDM alignment | Evaluating |
| **Calypso** | Trading/risk platform | CDM connector | Available |
| **Murex** | Trading/risk platform | CDM mapping | Available |
| **Finastra** | Banking platform | CDM roadmap | Planned |

**Classification Implication:** 
- Using CDM-integrated vendor ≠ CDM commitment
- May enable CDM connectivity without bank initiative
- Bank may be unaware of CDM capability in their vendor stack

---

### Tier 3: Traditional Vendors + CDM Roadmap

These established vendors are developing CDM capabilities.

| Vendor | Primary Solution | CDM Roadmap | Timeline |
|--------|------------------|-------------|----------|
| **Broadridge** | Post-trade services | CDM integration planned | TBD |
| **IHS Markit (S&P)** | Data/processing | CDM mapping | TBD |
| **Bloomberg** | Data/trading | CDM alignment | TBD |
| **Refinitiv (LSEG)** | Data/trading | CDM roadmap | TBD |

**Classification Implication:**
- Bank waiting for traditional vendor to add CDM = PRAGMATIST-Regulatory
- Vendor CDM roadmap may affect bank timeline decisions

---

## Vendor Selection Criteria

When banks choose vendors, they evaluate:

| Criterion | Question | ARCHITECT Preference | PRAGMATIST Preference |
|-----------|----------|---------------------|----------------------|
| **Control** | How much control over implementation? | High (build internally) | Low (outsource) |
| **Time to Market** | How fast to production? | Willing to invest time | Want fast solution |
| **Cost Structure** | Capex vs. Opex? | Willing to invest capex | Prefer opex model |
| **Flexibility** | Ability to customize? | Essential | Nice to have |
| **Dependency** | Vendor lock-in concern? | High concern | Acceptable tradeoff |
| **Expertise** | Internal capability? | Have or building | Prefer to outsource |

---

## Vendor-Bank Relationship Mapping

### Confirmed Relationships

| Bank | Vendor | Relationship Type | Evidence Source | Date |
|------|--------|-------------------|-----------------|------|
| HSBC | Delta Capita | Client — regulatory reporting | Press release | Jan 2025 |
| | | | | |

### Suspected/Rumored Relationships

| Bank | Vendor | Relationship Type | Evidence Source | Confidence |
|------|--------|-------------------|-----------------|------------|
| | | | | |

### To Research

| Bank | Vendor Signals to Check | Research Query |
|------|------------------------|----------------|
| Deutsche Bank | Any vendor partnership | "[Bank]" vendor derivatives reporting CDM |
| UBS | Post-integration vendor strategy | UBS vendor post-trade technology |
| SocGen | Following BNP or different vendor? | "Société Générale" regulatory reporting vendor |
| [All banks] | Delta Capita, Fragmos relationships | "[Bank]" "Delta Capita" OR "Fragmos" |

---

## Vendor Evaluation Framework

For PRAGMATIST-Vendor classifications, assess vendor choice on:

```markdown
### Vendor Assessment: [Vendor Name]

| Criterion | Assessment | Notes |
|-----------|------------|-------|
| **CDM Maturity** | [Native/Integrated/Wrapper/Planned] | [Details] |
| **Production Status** | [Production/Pilot/Development] | [Client references?] |
| **Geographic Coverage** | [Global/Regional/Limited] | [Jurisdictions] |
| **Regulatory Validation** | [Validated/Testing/Unvalidated] | [Which regs?] |
| **Bank's Scale Fit** | [Appropriate/Uncertain/Mismatch] | [Volume considerations] |
| **Dependency Risk** | [Low/Medium/High] | [Lock-in concerns] |

**Overall Vendor Risk:** [Low/Medium/High]

**Implication for Bank Classification:**
- If vendor is production-ready CDM-native → Strong PRAGMATIST-Vendor
- If vendor is developing CDM → PRAGMATIST (trajectory depends on vendor)
- If vendor has limited CDM → Bank may need additional solution
```

---

## Market Dynamics

### Vendor Consolidation

| Date | Event | Impact |
|------|-------|--------|
| [Track M&A] | | |

### New Entrants

| Date | Vendor | Offering | Impact |
|------|--------|----------|--------|
| [Track new entrants] | | | |

### Partnerships

| Date | Partners | Nature | Impact |
|------|----------|--------|--------|
| [Track partnerships] | | | |

---

## Vendor Signals in Research

### What to Look For

When researching banks, search for vendor signals:

**Strong Vendor Relationship Signals:**
- Press release announcing client relationship
- Bank explicitly names vendor as solution
- Implementation project mentioned
- Vendor case study features bank

**Moderate Vendor Signals:**
- Job posting references specific vendor
- Conference presentation mentions evaluation
- RFP process mentioned in trade press

**Weak Vendor Signals:**
- General "vendor" or "third-party" language
- Industry analyst speculation
- Vendor claims bank as client (unconfirmed)

### Research Queries

```
# For any bank, search:
"[Bank]" "Delta Capita" OR "Fragmos" OR "CDM vendor"
"[Bank]" regulatory reporting "third-party" OR outsource OR vendor
"[Bank]" derivatives technology partner OR vendor OR solution
```

---

## Classification Decision Support

### Vendor Relationship → Classification

| Evidence Found | Classification |
|----------------|----------------|
| Delta Capita/Fragmos client (confirmed) | PRAGMATIST-Vendor |
| Tier 2 vendor with CDM integration | PRAGMATIST (may have CDM passively) |
| Traditional vendor, waiting for CDM | PRAGMATIST-Regulatory |
| No vendor signals + internal build signals | ARCHITECT |
| Vendor + internal signals | ARCHITECT with vendor acceleration |
| No signals either direction | PRAGMATIST (default) or UNKNOWN |

### Vendor Quality → Confidence

| Vendor CDM Maturity | Confidence Adjustment |
|---------------------|----------------------|
| CDM-native, production | High confidence in classification |
| CDM-integrated | Medium confidence |
| CDM-planned | Lower confidence (trajectory uncertain) |

---

## Integration with Bank Research

### Add to Deep Research Prompts

```markdown
### Vendor Relationship Research

**Search for vendor signals:**
- Official announcements: "[Bank]" "Delta Capita" OR "Fragmos"
- General vendor: "[Bank]" derivatives reporting vendor OR outsource
- Platforms: "[Bank]" Calypso OR Murex OR Finastra CDM

**Evaluate findings:**
- Is relationship confirmed (press release) or suspected?
- What is vendor's CDM maturity?
- Does vendor relationship explain bank's CDM posture?
```

### Add to Output Template

```markdown
## Vendor Relationship Assessment

### Known Vendor Relationships

| Vendor | Relationship | Evidence | Date |
|--------|--------------|----------|------|
| [Vendor] | [Client/Evaluating/None] | [Source] | [Date] |

### Vendor Assessment (if applicable)

| Criterion | [Vendor Name] |
|-----------|---------------|
| CDM Maturity | [Native/Integrated/Planned] |
| Production Status | [Production/Pilot/Development] |
| Geographic Fit | [Covers bank's jurisdictions?] |
| Scale Fit | [Appropriate for bank's volume?] |

### Vendor → Classification Implication

[How does vendor relationship inform classification?]
- If CDM-native vendor client: Supports PRAGMATIST-Vendor
- If building alongside vendor: Supports ARCHITECT
- If no vendor signals: Neither supports nor refutes
```

---

## Vendor Landscape Update Log

```markdown
## Vendor Update Log

### [YYYY-MM-DD] — [Event]

**Type:** [New Vendor / Client Announcement / M&A / Product Update]
**Vendor:** [Name]
**Details:** [What changed]
**Banks Affected:** [If any]
**Action:** [Update to ecosystem / Bank refresh needed]

---
```
