# Tier 2 Evidence: Nomura Holdings, Inc.

## Search Execution Summary
- Execution Date: 2025-12-21
- Bank: Nomura Holdings, Inc.
- Phase: 3 (Japanese Banks)
- Searches Executed: 12
- Evidence Blocks Found: 2
- Null Results: 3

## Evidence Inventory

### [NOMURA-001] TIER 2 — SUPPORTS PRAGMATIST
**Claim:** Nomura is a clearing member of JSCC (Japan Securities Clearing Corporation), which launched CDM-based reporting in production in June 2025

**Source:** JSCC Official Website
**URL:** https://www.jpx.co.jp/jscc/en/index.html
**Date:** 2025-06-01

**Finding:**
JSCC is the first CCP globally to deploy CDM in production for derivatives clearing reporting (June 2025). Nomura as a clearing member is connected to this CDM infrastructure.

**Quality Assessment:**
- Authority: MEDIUM (Industry infrastructure, not official bank statement)
- Recency: CURRENT (June 2025)
- Specificity: MODERATE (Relationship confirmed but implementation details unclear)
- Corroborated: Pending

**Confidence:** MEDIUM

**Reasoning:**
This is indirect evidence through infrastructure connectivity. JSCC's CDM deployment creates exposure for clearing members, but does not prove Nomura has native CDM capabilities. Clearing members can interface with JSCC through vendor solutions.

**Caveats:**
- JSCC's CDM adoption does not necessarily indicate Nomura's internal CDM strategy
- Clearing members can interface with JSCC's CDM through vendor solutions without native CDM implementation
- This is an indirect signal based on infrastructure connection, not direct adoption evidence
- Product scope limited to cleared derivatives (IRS, CDS, Equity Swaps in Japan)

**Direction:** SUPPORTS_PRAGMATIST (vendor/infrastructure dependent approach)

---

### [NOMURA-002] TIER 2 — NEUTRAL
**Claim:** Nomura is listed as a sponsor of ISDA Annual General Meeting events

**Source:** ISDA
**URL:** https://www.isda.org
**Date:** 2024-04-01

**Finding:**
Nomura appears as sponsor/participant in ISDA events, demonstrating engagement with derivatives industry standards bodies.

**Quality Assessment:**
- Authority: MEDIUM (Industry association, confirms relationship)
- Recency: CURRENT (2024)
- Specificity: VAGUE (Event sponsorship, not technical participation)
- Corroborated: Yes (multiple ISDA events)

**Confidence:** LOW

**Reasoning:**
Event sponsorship is a weak signal. Many banks sponsor ISDA events for general industry engagement without specific CDM involvement. This confirms Nomura is engaged with ISDA but does not indicate CDM technical work.

**Caveats:**
- Event sponsorship does not indicate technical CDM implementation
- Many banks sponsor ISDA events for general industry engagement without specific CDM involvement
- No CDM-specific evidence from this participation
- Does not distinguish between strategic CDM commitment vs general ISDA membership

**Direction:** NEUTRAL (maintains industry presence but not CDM-specific)

---

## Tier 2 Assessment

**Total Evidence Items:** 2
**Supporting ARCHITECT:** 0
**Supporting PRAGMATIST:** 1
**NEUTRAL:** 1

**Key Findings:**
1. Indirect CDM exposure through JSCC clearing membership
2. General ISDA engagement but no CDM-specific participation
3. No trade press coverage of CDM initiatives
4. No conference presentations on CDM topics
5. No vendor announcements of Nomura CDM partnerships

**Implication:**
Tier 2 evidence is limited and indirect. The strongest signal is JSCC connectivity, which suggests Nomura is adapting to CDM infrastructure requirements but not leading adoption. Classification as OBSERVER (CCP-Connected) is appropriate given the indirect nature of evidence.
