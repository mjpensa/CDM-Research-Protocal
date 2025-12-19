# CDM Ecosystem: Utilities and Infrastructure

## Purpose

This document maps the CDM utility and infrastructure landscape that affects bank adoption decisions. Bank CDM positioning cannot be understood in isolation — it depends on available infrastructure.

---

## Production Infrastructure

### Central Counterparties (CCPs)

CCPs are critical infrastructure. CCP CDM adoption creates structural requirements for clearing members.

| CCP | Jurisdiction | CDM Status | Go-Live Date | Affected Banks | Notes |
|-----|--------------|------------|--------------|----------------|-------|
| **JSCC** | Japan | ✅ **PRODUCTION** | June 27, 2025 | Nomura, MUFG, Mizuho, SMBC, all Japan clearers | First CCP globally |
| **LCH** | UK/Global | 🔄 Evaluating | TBD | Most global dealers | SwapClear, key for rates |
| **CME** | US/Global | 🔄 Evaluating | TBD | US dealers, global banks | CME Clearing |
| **Eurex** | Germany/EU | 🔄 Evaluating | TBD | European dealers | Euro rates |
| **ICE** | US/UK | ❓ Unknown | TBD | CDS market participants | ICE Clear Credit/Europe |
| **HKEX** | Hong Kong | ❓ Unknown | TBD | Asia-Pacific dealers | OTC Clear |
| **SGX** | Singapore | ❓ Unknown | TBD | Singapore clearers | |

**Strategic Implication:**
- JSCC production = Japanese banks MUST have CDM connectivity (internal or wrapper)
- LCH/CME production would be transformative — affects virtually all global dealers
- CCP announcements are Tier 1 staleness triggers

---

### Trade Repositories

Trade repositories receive regulatory reports. CDM adoption affects reporting technology.

| Repository | Jurisdiction | CDM Status | Regulatory Regime | Affected Banks |
|------------|--------------|------------|-------------------|----------------|
| **DTCC GTR** | Global | 🔄 Evaluating | CFTC, EMIR, others | Global dealers |
| **DTCC DDR** | US | 🔄 Evaluating | CFTC | US reporters |
| **Regis-TR** | EU | ❓ Unknown | EMIR | European reporters |
| **UnaVista** | UK/EU | ❓ Unknown | UK EMIR, EMIR | UK/EU reporters |
| **KDPW** | Poland/EU | ❓ Unknown | EMIR | Regional reporters |
| **CME TR** | US | ❓ Unknown | CFTC | CME participants |

**Strategic Implication:**
- Trade repository CDM adoption would simplify regulatory reporting
- Less immediate pressure than CCPs (reporting can use transformation layers)
- DTCC direction particularly important given market share

---

### CDM-Native Utilities

These vendors provide CDM-native solutions banks can adopt instead of building.

| Utility | Solution Type | CDM Capability | Status | Known Clients | Geographic Focus |
|---------|---------------|----------------|--------|---------------|------------------|
| **Delta Capita** | Regulatory reporting | Native CDM transformation | Production | HSBC (Jan 2025) | Global |
| **Fragmos Chain** | Post-trade utility | Native CDM, DLT-based | Production | [Research] | Europe |
| **ISDA Digital** | Reference data, validation | CDM reference implementation | Production | Industry-wide | Global |
| **Acadia** | Margin/collateral | CDM integration planned | Development | Major dealers | Global |

**Strategic Implication:**
- Utility availability enables PRAGMATIST-Vendor path
- Banks can achieve CDM connectivity without internal build
- Vendor choice affects flexibility and control

---

## Technology Providers

These companies provide CDM tooling and platforms (not end-to-end solutions).

| Provider | Offering | Role in Ecosystem | Clients |
|----------|----------|-------------------|---------|
| **REGnosys** | Rosetta DSL, CDM tooling | Development platform, model maintenance | Technology teams |
| **ISDA** | CDM specification | Standard owner, governance | Industry |
| **FINOS** | Open source hosting | Collaboration platform | Contributors |
| **Axoni** | DLT infrastructure | Underlying technology | Various |

---

## Standards Bodies and Governance

### ISDA CDM Governance

| Body | Role | Composition | Relevance |
|------|------|-------------|-----------|
| **CDM Steering Committee** | Strategic direction | Senior bank representatives | Sets priorities |
| **CDM Architecture WG** | Technical design | Bank technologists | Shapes standard |
| **CDM Regulatory WG** | Regulatory alignment | Compliance + tech | Influences adoption |
| **ISDA Board** | Overall governance | Industry leaders | Ultimate authority |

**Bank Participation Signals:**
- Steering Committee membership = Strong commitment
- Working Group participation = Active engagement
- No ISDA participation = Limited engagement

### FINOS CDM Governance

| Body | Role | Composition | Relevance |
|------|------|-------------|-----------|
| **CDM Project** | Open source development | Contributors | Code development |
| **Technical Oversight** | Technical decisions | Elected members | Technical direction |
| **FINOS Board** | Foundation governance | Member firms | Strategic priorities |

**Bank Participation Signals:**
- Active code contribution = ARCHITECT-Follower minimum
- Governance role = ARCHITECT-Leader signal
- Member only = Awareness, not commitment

---

## Bank-Infrastructure Relationships

### Confirmed Relationships

| Bank | Infrastructure | Relationship | Evidence Date | Classification Impact |
|------|----------------|--------------|---------------|----------------------|
| HSBC | Delta Capita | Client contract | Jan 2025 | Supports PRAGMATIST-Vendor |
| BNP Paribas | Internal | Production system | 2022 | Confirms ARCHITECT-Native |
| JPMorgan | Internal | Production system | Oct 2024 | Confirms ARCHITECT-Native |
| Barclays | FINOS | Contributor | Ongoing | Confirms ARCHITECT-Follower+ |
| Standard Chartered | FINOS/DRR | Contributor | Ongoing | Confirms ARCHITECT-Follower |
| Japanese megabanks | JSCC | Clearing members | Jun 2025 | Must have connectivity |

### Relationships to Research

| Bank | Likely Infrastructure | Evidence Needed |
|------|----------------------|-----------------|
| Deutsche Bank | Unknown | Vendor relationship OR internal build |
| SocGen | Unknown (likely following BNP) | Internal build OR vendor |
| UBS | Unknown (constrained) | Post-integration direction |
| [Others] | Unknown | Research focus |

---

## Geographic Infrastructure Availability

| Region | Available Utilities | CCP CDM Status | Regulatory Driver | Bank Options |
|--------|--------------------|--------------------|-------------------|--------------|
| **Japan** | Limited | JSCC Production | JFSA | Must connect to JSCC |
| **EU** | Delta Capita, Fragmos | CCPs evaluating | EMIR Refit | Build, buy, or wait |
| **UK** | Delta Capita, others | CCPs evaluating | UK EMIR | Build, buy, or wait |
| **US** | Limited CDM-native | CCPs evaluating | CFTC | Build or wait |
| **Singapore** | Limited | Unknown | MAS | Build or wait |
| **Hong Kong** | Limited | Unknown | HKMA | Build or wait |

**Implication:**
- Japan: Most constrained, JSCC forces connectivity
- EU/UK: Options available, regulatory pressure present
- US/Asia ex-Japan: Less immediate pressure, fewer utilities

---

## Infrastructure Decision Tree

When researching a bank's CDM positioning, consider:

```
Is the bank a clearing member of a CDM-production CCP?
├── YES (e.g., JSCC member)
│   └── Bank MUST have CDM connectivity
│       ├── Evidence of internal build? → ARCHITECT
│       ├── Evidence of vendor/wrapper? → PRAGMATIST-Vendor
│       └── No evidence? → Research gap (concerning)
│
└── NO
    └── Bank has choice
        ├── Building internally? → ARCHITECT
        ├── Vendor contract? → PRAGMATIST-Vendor
        ├── Waiting for utilities/mandates? → PRAGMATIST-Regulatory
        └── No signals? → PRAGMATIST (default) or UNKNOWN
```

---

## Monitoring Infrastructure Changes

### High-Impact Events to Track

| Event Type | Impact | Action |
|------------|--------|--------|
| CCP production announcement | Affects all clearing members | Refresh all affected banks |
| DTCC CDM announcement | Affects all reporters | Refresh trade repository users |
| New utility launches | Creates new options | Update ecosystem doc |
| Utility acquisition/merger | Affects clients | Update ecosystem + refresh clients |
| Regulatory CDM mandate | Creates deadline | Refresh affected jurisdiction |

### Infrastructure Update Log

```markdown
## Infrastructure Change Log

### [YYYY-MM-DD] — [Event]

**Type:** [CCP/Utility/Regulatory]
**Description:** [What happened]
**Banks Affected:** [List]
**Action Taken:** [What updates made]

---
```

---

## Integration with Bank Research

### Add to Each Bank Prompt

```markdown
### Infrastructure Context

**Relevant CCPs:**
- [CCP]: [CDM Status] — [Bank's clearing relationship]

**Available Utilities in Region:**
- [Utility]: [Status] — [Known relationship?]

**Infrastructure-Driven Classification Considerations:**
- If [CCP] clearing member + no internal build evidence → Likely wrapper/vendor
- If [Utility] client → PRAGMATIST-Vendor
- If neither → Research internal capability
```

### Add to Output Template

```markdown
## Infrastructure Relationship Assessment

### CCP Connectivity Requirements

| CCP | Clearing Member? | CDM Requirement | Bank's Response |
|-----|------------------|-----------------|-----------------|
| JSCC | [Y/N] | Production (Jun 2025) | [Internal/Vendor/Unknown] |
| LCH | [Y/N] | Pending | [N/A yet] |
| CME | [Y/N] | Pending | [N/A yet] |

### Utility Relationships

| Utility | Relationship | Evidence | Classification Impact |
|---------|--------------|----------|----------------------|
| Delta Capita | [Client/None/Unknown] | [Source] | [Impact] |
| Fragmos | [Client/None/Unknown] | [Source] | [Impact] |
| Other | [If any] | [Source] | [Impact] |

### Infrastructure-Informed Classification

Based on infrastructure relationships:
- Required connectivity: [What must bank have?]
- Chosen approach: [Build/Buy/Unknown]
- Infrastructure supports classification: [How?]
```
