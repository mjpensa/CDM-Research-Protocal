# Pre-Mortem Analysis: NatWest Group PLC
## Tier B Protocol (Abbreviated - 2 Failure Modes)

**Bank**: NatWest Group PLC
**Date**: 2025-12-19
**Prior**: P(Architect) = 20%

---

## Failure Mode 1: False Positive Risk (Classify as Architect when actually Adopter)

### Scenario
NatWest gets classified as CDM Architect based on:
- General ISDA membership and participation in industry consultations
- UK regulatory compliance discussions that mention standardization
- Vendor partnership announcements that could be misread as direct CDM engagement

### Why This Could Happen
1. **ISDA Membership Confusion**: As a major UK bank, NatWest participates in ISDA activities. General ISDA involvement could be conflated with specific CDM contribution.
2. **UK EMIR Refit Compliance**: NatWest must comply with UK EMIR (Sept 2024). Compliance work may reference standardization without implying CDM architecture involvement.
3. **Vendor Solution Misattribution**: If NatWest partners with a CDM-capable vendor (e.g., DTCC, MarkitServ), statements about "standards adoption" could be misread as direct CDM development.

### Mitigation Strategy
- Require EXPLICIT mentions of CDM code contribution, working group leadership, or named CDM initiatives
- Distinguish between "regulatory compliance" and "standards development"
- Verify any ISDA participation is CDM-specific, not general derivatives operations

---

## Failure Mode 2: False Negative Risk (Classify as Adopter when actually Architect)

### Scenario
NatWest is incorrectly classified as Adopter/PRAGMATIST because:
- CDM work is conducted through subsidiaries or joint ventures
- Technical contributions are made quietly without public announcements
- UK-specific regulatory initiatives overlap with CDM but aren't labeled as such

### Why This Could Happen
1. **Low Public Profile**: Regional banks may contribute to CDM without extensive press releases
2. **Consortium Participation**: NatWest could be contributing through UK Finance or other industry bodies
3. **Technical Staff Involvement**: Individual engineers may participate in CDM working groups without corporate announcements
4. **FCA/BoE Mandates**: UK regulatory push for standardization may drive CDM work that isn't explicitly marketed

### Mitigation Strategy
- Search for individual contributor names from NatWest in CDM repositories
- Check UK Finance and UK regulatory body publications for NatWest-specific mentions
- Look for technical conference presentations or working group participation lists

---

## Pre-Mortem Gate Decision

**PASS**: Failure modes identified and mitigation strategies defined.

### Key Search Focus Areas (Informing Evidence Gathering)
1. **Explicit CDM mentions** - Direct NatWest + CDM references
2. **ISDA working group participation** - Specific CDM working group involvement
3. **UK EMIR compliance** - Distinguishing compliance from development
4. **Vendor relationships** - Understanding if vendor-mediated or direct
5. **Technical contributions** - GitHub, conferences, working groups
6. **Industry body participation** - UK Finance, BoE consultations

### Risk Assessment
- **False Positive Risk**: MODERATE - Need to distinguish compliance from architecture
- **False Negative Risk**: LOW-MODERATE - Limited public profile expected for regional bank
