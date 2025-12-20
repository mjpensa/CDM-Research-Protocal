# Bayesian Update Post-Tier 1: HSBC Holdings PLC

## Research Date
2025-12-19

---

## Prior Probability

**P(ARCHITECT) Prior = 40%**

Components:
- Base rate for global systemically important banks: 25%
- Derivatives-dominant adjustment: +10% (HSBC is major derivatives dealer)
- Vendor relationship ambiguous signal: +5%

**P(PRAGMATIST) Prior = 60%**

---

## Evidence Assessment

### Evidence Category 1: Delta Capita Global Outsourcing Agreement

**Evidence**: HSBC signed multi-year agreement with Delta Capita for global OTC derivatives confirmation and settlement services (January 2025)

**Likelihood Ratios**:
- P(This agreement | ARCHITECT) = 0.2
  - ARCHITECT banks may use vendors, but typically as components, not comprehensive global outsourcing
  - Comprehensive scope (confirmation + settlement + global) is unusual for ARCHITECT

- P(This agreement | PRAGMATIST) = 0.9
  - This is exactly what PRAGMATIST banks do - outsource CDM capability
  - Comprehensive scope aligns with vendor-dependent approach

**Likelihood Ratio (LR)**: 0.9 / 0.2 = 4.5 favoring PRAGMATIST

**Bayesian Update**:
```
Prior Odds (ARCHITECT) = 40/60 = 0.667
Posterior Odds = 0.667 / 4.5 = 0.148
Posterior P(ARCHITECT) = 0.148 / (1 + 0.148) = 12.9%
```

**Updated P(ARCHITECT) after Evidence 1: ~13%**

---

### Evidence Category 2: No Internal CDM Development Evidence

**Evidence**: Comprehensive search found no evidence of internal CDM teams, projects, or capability development at HSBC

**Likelihood Ratios**:
- P(No internal CDM evidence | ARCHITECT) = 0.15
  - ARCHITECT banks typically have visible CDM initiatives
  - Some internal projects may be unpublicized, but pattern shows disclosure

- P(No internal CDM evidence | PRAGMATIST) = 0.85
  - PRAGMATIST banks don't build internal CDM capability
  - Absence of evidence is expected

**Likelihood Ratio (LR)**: 0.85 / 0.15 = 5.67 favoring PRAGMATIST

**Bayesian Update**:
```
Prior Odds (from Evidence 1) = 0.148
Posterior Odds = 0.148 / 5.67 = 0.026
Posterior P(ARCHITECT) = 0.026 / (1 + 0.026) = 2.5%
```

**Updated P(ARCHITECT) after Evidence 2: ~2.5%**

---

### Evidence Category 3: Broader Outsourcing Strategy

**Evidence**: HSBC is considering outsourcing fixed-income trading operations to external market makers (Citadel Securities, Jane Street) to reduce IT costs

**Likelihood Ratios**:
- P(Outsourcing trading operations | ARCHITECT) = 0.3
  - ARCHITECT banks may outsource operations while retaining technology strategy
  - But pattern suggests cost-cutting priority over technology investment

- P(Outsourcing trading operations | PRAGMATIST) = 0.75
  - Consistent with vendor-dependent, cost-reduction approach
  - Aligns with not investing in internal capabilities

**Likelihood Ratio (LR)**: 0.75 / 0.3 = 2.5 favoring PRAGMATIST

**Bayesian Update**:
```
Prior Odds (from Evidence 2) = 0.026
Posterior Odds = 0.026 / 2.5 = 0.010
Posterior P(ARCHITECT) = 0.010 / (1 + 0.010) = 1.0%
```

**Updated P(ARCHITECT) after Evidence 3: ~1%**

---

### Evidence Category 4: 2018 DRR Pilot Participation (Counterbalancing)

**Evidence**: HSBC participated in 2018-2019 UK FCA/BoE Digital Regulatory Reporting pilot using ISDA CDM

**Likelihood Ratios**:
- P(Pilot participation | ARCHITECT) = 0.8
  - ARCHITECT banks would participate in such pilots
  - But many PRAGMATIST banks also participated

- P(Pilot participation | PRAGMATIST) = 0.5
  - Pilot was collaborative, low-commitment
  - Does not indicate internal capability building

**Likelihood Ratio (LR)**: 0.8 / 0.5 = 1.6 favoring ARCHITECT (mild)

**Bayesian Update**:
```
Prior Odds (from Evidence 3) = 0.010
Posterior Odds = 0.010 * 1.6 = 0.016
Posterior P(ARCHITECT) = 0.016 / (1 + 0.016) = 1.6%
```

**Updated P(ARCHITECT) after Evidence 4: ~1.6%**

---

### Evidence Category 5: ISDA Board Presence (Counterbalancing)

**Evidence**: HSBC executive (Jeroen Krens) served as ISDA Board Chair from January 2025

**Likelihood Ratios**:
- P(ISDA Board Chair | ARCHITECT) = 0.7
  - ARCHITECT banks engage at industry governance level
  - But board role is governance, not technical CDM contribution

- P(ISDA Board Chair | PRAGMATIST) = 0.4
  - PRAGMATIST banks can also have ISDA board presence
  - Governance role doesn't require CDM capability

**Likelihood Ratio (LR)**: 0.7 / 0.4 = 1.75 favoring ARCHITECT (mild)

**Bayesian Update**:
```
Prior Odds (from Evidence 4) = 0.016
Posterior Odds = 0.016 * 1.75 = 0.028
Posterior P(ARCHITECT) = 0.028 / (1 + 0.028) = 2.7%
```

**Updated P(ARCHITECT) after Evidence 5: ~2.7%**

---

### Evidence Category 6: FINOS Membership Without CDM Engagement

**Evidence**: HSBC is FINOS member but no CDM-specific participation found

**Likelihood Ratios**:
- P(FINOS member, no CDM | ARCHITECT) = 0.3
  - ARCHITECT banks in FINOS typically engage with CDM project
  - Non-engagement is unusual for ARCHITECT

- P(FINOS member, no CDM | PRAGMATIST) = 0.6
  - PRAGMATIST banks join FINOS for other reasons (Symphony, etc.)
  - No CDM engagement is expected

**Likelihood Ratio (LR)**: 0.6 / 0.3 = 2.0 favoring PRAGMATIST

**Bayesian Update**:
```
Prior Odds (from Evidence 5) = 0.028
Posterior Odds = 0.028 / 2.0 = 0.014
Posterior P(ARCHITECT) = 0.014 / (1 + 0.014) = 1.4%
```

**Updated P(ARCHITECT) after Evidence 6: ~1.4%**

---

### Evidence Category 7: No Post-Pilot CDM Implementation (6-Year Gap)

**Evidence**: No visible CDM implementation between 2018-2019 pilot and 2025 Delta Capita outsourcing

**Likelihood Ratios**:
- P(6-year gap with no action | ARCHITECT) = 0.05
  - ARCHITECT banks would have implemented learnings from pilot
  - 6-year gap with no action is highly unlikely for ARCHITECT

- P(6-year gap with no action | PRAGMATIST) = 0.8
  - PRAGMATIST banks participate in pilots without follow-through
  - Gap followed by outsourcing is characteristic pattern

**Likelihood Ratio (LR)**: 0.8 / 0.05 = 16.0 strongly favoring PRAGMATIST

**Bayesian Update**:
```
Prior Odds (from Evidence 6) = 0.014
Posterior Odds = 0.014 / 16.0 = 0.0009
Posterior P(ARCHITECT) = 0.0009 / (1 + 0.0009) = 0.09%
```

**Updated P(ARCHITECT) after Evidence 7: ~0.1%**

---

## Final Posterior Probability

**P(ARCHITECT) = 0.1%**
**P(PRAGMATIST) = 99.9%**

---

## Probability Trajectory

| Stage | Evidence | P(ARCHITECT) | P(PRAGMATIST) |
|-------|----------|--------------|---------------|
| Prior | Starting assessment | 40% | 60% |
| +E1 | Delta Capita global outsourcing | 13% | 87% |
| +E2 | No internal CDM evidence | 2.5% | 97.5% |
| +E3 | Broader outsourcing strategy | 1% | 99% |
| +E4 | DRR pilot participation (+) | 1.6% | 98.4% |
| +E5 | ISDA board presence (+) | 2.7% | 97.3% |
| +E6 | FINOS no CDM engagement | 1.4% | 98.6% |
| +E7 | 6-year gap no implementation | 0.1% | 99.9% |

---

## Classification Decision

**Classification**: PRAGMATIST (Vendor-dependent)
**Confidence**: Very High (99.9%)

**Reasoning**:
The evidence pattern is highly consistent with PRAGMATIST classification:
1. Comprehensive outsourcing to CDM-native vendor (Delta Capita/Fragmos Chain)
2. No internal CDM capability development
3. Broader strategy of outsourcing operations to reduce costs
4. Pilot participation without follow-through (6-year gap)
5. Industry governance engagement but no technical CDM contribution

---

## Gate 1 Decision

**Recommendation**: Proceed with PRAGMATIST classification

**Tier 2 searches**: Consider targeted searches to confirm no hidden internal capability, but Tier 1 evidence is sufficiently conclusive.

**Key risk to monitor**: Any evidence of internal CDM development that was missed would require reassessment. However, the pattern is strong enough that additional searches are unlikely to change classification.
