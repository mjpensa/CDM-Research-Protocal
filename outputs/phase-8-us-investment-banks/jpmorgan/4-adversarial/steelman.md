# Steelman Analysis: JPMorgan

**Bank**: JPMorgan Chase & Co.
**Phase**: 8 (US Investment Banks)
**Date**: 2025-12-21

---

## Steelman Exercise

Constructing the **strongest possible argument** against the ARCHITECT (Native) classification.

---

## Steelman Case: JPMorgan Is ARCHITECT (Active), Not Native

### Core Argument

JPMorgan's CDM implementation, while impressive, may not yet qualify as fully "Native" because:

1. **Rolling implementation**: "In the middle of our ASIC implementation" suggests ongoing work
2. **Equity focus**: Nick Moger leads "Equity Derivatives Business" - may not cover all asset classes
3. **First ≠ Best**: Being first US bank doesn't mean mature production across all derivatives
4. **Maintainer ≠ Contributor**: Maintainer role could be governance participation without significant code contribution

### Supporting Logic

```
Production for some jurisdictions + Ongoing implementation for others
= Not yet fully "Native" across enterprise
= ARCHITECT (Active) more accurate than (Native)
```

### Evidence Marshaling

| Evidence | Steelman Interpretation |
|----------|------------------------|
| "In the middle of ASIC" | Implementation ongoing, not complete |
| "Equity Derivatives" | May be limited to one business line |
| "First major US bank" | First doesn't mean most mature |
| Maintainer appointment | Recent - implies earlier stage of contribution |

---

## Steelman Strength Assessment

| Factor | Strength |
|--------|----------|
| Evidence quality | Low - relies on interpretation |
| Logical coherence | Medium - argument is internally consistent |
| Falsifiability | Medium - scope could be clarified |
| Parsimony | Low - requires ignoring explicit claims |

**Overall Steelman Strength**: **WEAK**

The argument relies on interpretive stretches rather than contradictory evidence.

---

## Why Steelman Fails

### 1. "Primary Reporting Mechanism" Settles It

JPMorgan explicitly claims CDM/DRR is its "primary reporting mechanism." This is incompatible with ARCHITECT (Active):

- "Primary" means main, not experimental
- "Mechanism" implies operational infrastructure
- This terminology specifically distinguishes from pilot

### 2. FINOS Award Confirms Production

The 'Adoption Achiever' award is specifically for production adoption, not pilots:

- FINOS would not award "Adoption Achiever" for pilot
- Award recognizes actual usage, not intent
- This is third-party validation of production status

### 3. Maintainer Status Indicates Maturity

FINOS maintainer appointment indicates:

- Sufficient internal expertise to contribute to governance
- Production experience informing CDM evolution
- Long-term commitment to the standard

A firm at pilot stage would not receive maintainer status.

### 4. Multiple Jurisdictions Proves Scale

Production coverage of ASIC, MAS, EMIR, CFTC indicates:

- Enterprise-scale implementation
- Not limited to single business line
- Regulatory compliance across major jurisdictions

---

## Verdict

The steelman case is **weak and unconvincing**.

The strongest counter-argument (ongoing implementation → Active not Native) fails because:
1. "Primary mechanism" explicitly indicates production
2. FINOS award validates production adoption
3. Maintainer status requires demonstrated expertise
4. Multi-jurisdictional scope exceeds any reasonable pilot

**Recommendation**: Maintain ARCHITECT (Native) classification

---

*Steelman analysis under CDM Research Protocol v2.3*
