# Assessment: Goldman Sachs Group, Inc.

**Bank**: Goldman Sachs Group, Inc.
**Date**: 2025-12-19
**Protocol**: Tier A (Full Protocol)
**Phase**: 8 - US Investment Banks

---

## Bank Profile

| Attribute | Value |
|-----------|-------|
| Headquarters | New York, USA |
| Business Model | Global investment bank |
| Derivatives Relevance | Very High |
| Primary Regulator | Federal Reserve/SEC/CFTC |
| G-SIB Status | Yes |
| Technology Culture | Strong proprietary systems |

---

## Prior Probability

**P(ARCHITECT) = 40%**

Adjustments:
- +15% for derivatives dominant business model
- +10% for JPMorgan peer pressure
- +5% for strong technology culture
- Base 25% for high-derivatives bank

**P(PRAGMATIST) = 60%**

---

## Evidence Summary

### Search Results Analysis

Goldman Sachs maintains characteristic secrecy about technology strategy. Key observations:

1. **No public CDM production announcement** - Unlike JPMorgan, Goldman has not announced CDM production or pilot
2. **ISDA membership confirmed** - Major ISDA member with working group participation
3. **Strong proprietary technology culture** - Goldman known for building internally rather than adopting standards
4. **CFTC compliance focus** - Addressing regulatory requirements through existing systems

---

## Evidence Blocks

### [GS-001] TIER 4 - SUPPORTS PRAGMATIST (No Production Announcement)
**Finding**: Goldman Sachs has not announced CDM production or pilot program. Unlike JPMorgan's October 2024 announcement, Goldman remains silent on CDM adoption.
**Source**: Absence of official announcement
**Confidence**: MEDIUM
**Implication**: If building CDM, not yet public; may be following vendor path

### [GS-002] TIER 2 - NEUTRAL (ISDA Membership)
**Finding**: Goldman Sachs is a major ISDA member participating in derivatives standards development. However, ISDA membership alone doesn't indicate CDM adoption - it's baseline for major dealers.
**Source**: ISDA membership records
**Confidence**: HIGH
**Implication**: Standards participation doesn't distinguish ARCHITECT from PRAGMATIST

### [GS-003] TIER 3 - WEAKLY SUPPORTS ARCHITECT (Technology Culture)
**Finding**: Goldman Sachs has strong reputation for proprietary technology development (e.g., Marquee platform). This culture could support internal CDM build rather than vendor adoption.
**Source**: Industry reputation, technology press
**Confidence**: MEDIUM
**Implication**: If CDM needed, Goldman would likely build internally

### [GS-004] TIER 4 - SUPPORTS PRAGMATIST (Competitor First Mover)
**Finding**: JPMorgan moved to CDM production first among US banks. Goldman typically prefers to lead, not follow. This may indicate Goldman pursuing alternative approach or delayed timeline.
**Source**: Industry analysis
**Confidence**: LOW-MEDIUM
**Implication**: Goldman may differentiate from JPMorgan approach

---

## Bayesian Update

### Prior
- P(Architect) = 40%
- P(Pragmatist) = 60%
- Prior Odds = 0.67

### Evidence Assessment
| Evidence | Likelihood Ratio | Direction |
|----------|-----------------|-----------|
| No production announcement | 0.3:1 | Supports PRAGMATIST |
| ISDA membership | 1:1 | Neutral |
| Technology culture | 1.5:1 | Weakly supports ARCHITECT |
| JPMorgan first mover | 0.7:1 | Weakly supports PRAGMATIST |

### Combined Likelihood Ratio
LR = 0.3 × 1 × 1.5 × 0.7 = 0.315

### Posterior Calculation
Posterior Odds = 0.67 × 0.315 = 0.21
**P(Architect | Evidence) = 17%**
**P(Pragmatist | Evidence) = 83%**

---

## Adversarial Analysis

### Testing for ARCHITECT
**Search**: Goldman Sachs CDM production pilot announcement 2024 2025
**Result**: No confirming evidence found

**Search**: Goldman Sachs FINOS contribution
**Result**: No confirming evidence found

### Testing for PRAGMATIST
**Search**: Goldman Sachs derivatives reporting vendor partner
**Result**: No specific vendor partnership announced, but also no internal CDM evidence

### Verdict
No strong evidence either direction. Classification based on absence of ARCHITECT signals and JPMorgan contrast.

---

## Single Adversarial Question

**Question**: Is Goldman Sachs building CDM capability internally without public announcement, consistent with their secretive technology culture?

**Answer**: Possible but unconfirmed. Goldman's technology culture could support stealth CDM development. However, JPMorgan's public announcement creates pressure for Goldman to respond. The absence of any CDM signals (hiring, FINOS, conferences) after JPMorgan's announcement suggests Goldman is likely pursuing vendor or alternative path rather than internal CDM build.

**Verdict**: **PRAGMATIST** - No evidence to support ARCHITECT classification

---

## Final Classification

| Classification | Probability | Confidence |
|---------------|-------------|------------|
| **PRAGMATIST** | 83% | 65% |
| Architect | 17% | - |

**Sub-classification**: Vendor-Dependent (likely) or Alternative Approach

**Confidence Note**: Lower confidence (65%) reflects Goldman's secretive culture. Classification could change if CDM announcement emerges.

---

## Key Findings

1. **No CDM production announcement** despite JPMorgan moving first
2. **Strong technology culture** suggests internal build IF CDM pursued
3. **ISDA membership** doesn't distinguish adoption posture
4. **JPMorgan competitive dynamic** may drive alternative approach
5. **Classification provisional** pending Goldman response to JPMorgan

---

## Comparison to JPMorgan

| Factor | JPMorgan | Goldman Sachs |
|--------|----------|---------------|
| CDM Production | Confirmed Oct 2024 | Not announced |
| Public Posture | Transparent | Secretive |
| Technology Culture | Strong | Very Strong |
| Regulatory Driver | CFTC Rewrite | Same |
| Classification | ARCHITECT | PRAGMATIST (provisional) |

Goldman's silence after JPMorgan's announcement is notable. Two interpretations:
1. **Building quietly** - Goldman developing CDM but not announcing
2. **Alternative path** - Goldman pursuing different approach (vendor or proprietary)

Current evidence supports interpretation #2.

---

*Assessment Complete*
*Protocol: Tier A*
*Classification: PRAGMATIST (83%, 65% confidence)*
