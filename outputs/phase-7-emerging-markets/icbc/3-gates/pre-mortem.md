# Pre-Mortem Analysis: ICBC

**Bank**: Industrial and Commercial Bank of China
**Phase**: 7 (Emerging Markets)
**Date**: 2025-12-21

---

## Potential Failure Modes

### 1. Missing CDM Evidence in Chinese Sources
- **Risk**: CDM adoption discussed in Mandarin sources not indexed by English search
- **Assessment**: LOW - CDM is primarily English/ISDA ecosystem, Chinese would use NAFMII terminology
- **Mitigation**: Searched for ISDA-China collaboration specifically

### 2. US Operations Using CDM
- **Risk**: ICBC's US subsidiaries (NY branch, ICBC USA NA) could be using CDM for CFTC reporting
- **Finding**: Resolution plan documents mention derivatives hedging but no CDM
- **Mitigation**: Searched regulatory filings, no CDM evidence

### 3. ISDA-NAFMII Bridge
- **Risk**: ISDA-NAFMII IBOR fallbacks collaboration could indicate CDM adoption
- **Finding**: Collaboration is on documentation standards, not CDM technology
- **Impact**: Confirms separate but collaborating frameworks

---

## Research Quality Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Source Diversity | Medium | ISDA, FINOS, US regulatory filings, trade press |
| Tier 1 Coverage | Complete | All relevant sources searched |
| Negative Space | Well-defined | NAFMII framework explains absence |
| Temporal Currency | Good | 2024-2025 sources |

---

## Structural Conclusion

The research correctly identified that ICBC operates in a **fundamentally different regulatory ecosystem** (NAFMII) that is outside the scope of ISDA CDM. This is a structural finding, not a research failure.

---

*Pre-mortem completed under CDM Research Protocol v2.3*
