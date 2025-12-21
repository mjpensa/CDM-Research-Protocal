# Example: Pre-Mortem Analysis

## Context

Before beginning research on Nomura. Pre-mortem establishes expected failure modes and mitigation strategies.

## Input State

- **Bank**: Nomura Holdings
- **Headquarters**: Tokyo, Japan
- **Prior P(Architect)**: 40% (default)
- **Phase**: Phase 3 (Japanese Banks)

---

## Pre-Mortem Analysis

### 1. Failure Mode: Insufficient Public Information

**Description**: Nomura may not publicly disclose CDM activities due to Japanese corporate culture of limited external disclosure.

**Probability**: 45%

**Mitigation Strategy**:
- Prioritize English-language regulatory filings (JSCC requirements)
- Search Japanese financial press (Nikkei) with translation
- Look for ISDA Asia-Pacific event participation
- Check for JSCC connectivity announcements

**Fallback Plan**:
- If limited English sources, focus on JSCC deadline signals
- Infer from peer behavior (MUFG, Mizuho, SMBC)
- Document as knowledge gap for insider resolution

### 2. Failure Mode: Misleading Evidence

**Description**: Sources might overstate Nomura's engagement (vendor marketing) or understate it (confidentiality).

**Probability**: 30%

**Mitigation Strategy**:
- Require bank confirmation for vendor claims
- Cross-reference vendor announcements with trade press
- Distinguish "client" from "partner" relationships
- Check if evidence is aspirational vs. actual

**Fallback Plan**:
- Downweight unconfirmed vendor claims (LR = 1.5 max)
- Flag as "vendor claim only" in evidence record
- Seek corroboration before assigning high confidence

### 3. Failure Mode: Outdated Information

**Description**: Historical evidence from 2022-2023 may not reflect current 2025 status, especially with June 2025 JSCC deadline.

**Probability**: 35%

**Mitigation Strategy**:
- Filter for evidence from 2024-2025
- Apply recency weights per methodology
- Explicitly search for "Nomura CDM 2024" and "Nomura JSCC 2025"
- Look for trajectory signals (accelerating/decelerating)

**Fallback Plan**:
- If only dated evidence: document as Trajectory=Unknown
- Do not allow evidence >3 years old to drive classification
- Recommend targeted re-research if deadline approaches

### 4. Failure Mode: Confirmation Bias

**Description**: As a major Japanese bank with JSCC deadline, I might assume Nomura MUST be adopting CDM.

**Probability**: 25%

**Mitigation Strategy**:
- Apply null hypothesis rigorously: assume PRAGMATIST
- Explicitly search for disconfirming evidence
- Document null results for each tier
- Challenge any assumption that "must be building"

**Fallback Plan**:
- If I notice confirmatory pattern, pause and re-check
- Consult peer bank evidence (is pattern consistent?)
- Apply extra adversarial scrutiny if initial lean is ARCHITECT

---

## Difficulty Assessment

**Overall Difficulty**: MODERATE

**Rationale**:
- Japanese corporate disclosure is typically limited
- However, JSCC requirements create public signals
- English-language press coverage exists (Risk.net Asia coverage)
- ISDA Asia events provide evidence opportunities

---

## Success Criteria

**Criterion 1**: At least 5 evidence items documented across Tier 1-3
- Measurable: Count of evidence items in evidence.json
- Achievable: Japanese banks have ISDA/JSCC touchpoints

**Criterion 2**: Clear determination of JSCC CDM connectivity status
- Measurable: Binary - connected/not connected/unknown
- Achievable: JSCC connectivity is documented

**Criterion 3**: Trajectory assessment with temporal evidence
- Measurable: Evidence from multiple time periods
- Achievable: June 2025 deadline creates recent activity

---

## Search Priorities

Based on pre-mortem analysis, prioritize in this order:

1. **JSCC connectivity** (Tier 1) - Official deadline-driven evidence
2. **ISDA Asia participation** (Tier 2) - Conference/working group signals
3. **Risk.net Asia coverage** (Tier 2) - Trade press with Japan focus
4. **Japanese financial press** (Tier 2) - Nikkei, Japanese sources
5. **Job postings Japan** (Tier 3) - LinkedIn Japan, Nomura careers

---

## Pre-Mortem Complete

**Date**: 2025-12-21
**Gate Status**: CLEARED
**Proceed to**: Tier 1 Evidence Gathering
