# Reasoning Gate 3: Post-Tier 3 (Final)

**Bank**: Banco Bilbao Vizcaya Argentaria S.A.
**Phase**: 5 (Spanish)
**Date**: 2025-12-21

---

## Gate Purpose

Final reasoning gate before classification decision.

---

## Complete Evidence Inventory

| ID | Claim | Type | Tier | Freshness |
|----|-------|------|------|-----------|
| BBVA-E001 | CFTC/SEC swap dealer | membership | 1 | Current |
| BBVA-E002 | ISDA FATCA Protocol | membership | 2 | Historical |
| BBVA-E003 | ISDA Resolution Stay | membership | 2 | Historical |
| BBVA-E004 | Accenture/Murex/Calypso | vendor_proxy | 2 | Current |
| Null | NOT in UK DRR pilot | - | 2 | - |
| Null | No CDM jobs | - | 3 | - |
| Null | No LinkedIn CDM | - | 3 | - |

---

## Classification Matrix

| Classification | Evidence For | Evidence Against | Probability |
|---------------|--------------|------------------|-------------|
| ARCHITECT | None | No FINOS, no pilot, no CDM | 0% |
| PRAGMATIST | Swap dealer, Murex/Calypso | No CDM evidence | 48% |
| OBSERVER | No CDM evidence | Active derivatives | 47% |
| UNKNOWN | - | Some evidence exists | 5% |

---

## PRAGMATIST vs OBSERVER Decision

This is a marginal call. Key considerations:

### PRAGMATIST Arguments
1. **Active swap dealer** - CFTC/SEC registration demonstrates derivatives business
2. **Vendor investment** - Murex/Calypso ecosystem via Accenture
3. **ISDA protocols** - Engaged with derivatives standards
4. **Business model** - CIB division exists for derivatives

### OBSERVER Arguments
1. **No CDM evidence** - Zero CDM-specific signals
2. **No DRR pilot** - Did not engage with UK pilot (unlike Santander)
3. **No hiring signals** - Not building CDM capability
4. **Retail focus** - Primary business is retail banking

### Decision
**PRAGMATIST (Traditional)** selected because:
- Active derivatives operations exist (swap dealer status is current)
- "Traditional" subtype captures derivatives-active but non-CDM approach
- OBSERVER would understate derivatives market participation

---

## Final Classification

| Field | Value |
|-------|-------|
| **Classification** | PRAGMATIST |
| **Subtype** | Traditional |
| **Confidence** | 45% |
| **Maturity Score** | 1 |

---

## Gate 3 Verdict

| Criterion | Status |
|-----------|--------|
| Sufficient for classification | ✅ Yes (marginal) |
| Classification confidence | ⚠️ Low (45%) |
| Alternative credible | ✅ OBSERVER (47%) |

**Decision**: **CLASSIFICATION COMPLETE - PROCEED TO ADVERSARIAL REVIEW**
