# Phase 9: US Custody Banks

## Overview

Phase 9 assesses the two major US custody banks for CDM adoption posture. These banks have fundamentally different business models from investment banks — their primary business is asset servicing, custody, and securities processing rather than derivatives trading.

---

## Banks in Phase

| Bank | Execution Tier | Time Budget | Business Focus |
|------|---------------|-------------|----------------|
| State Street | C (Rapid) | 1.5 hours | Custody, asset servicing |
| BNY Mellon | C (Rapid) | 1.5 hours | Custody, asset servicing |

**Total Time Budget**: 3.0 hours

---

## Custody Bank Context

### Business Model Differences

Unlike investment banks, custody banks:
- **Primary function**: Hold and administer assets for institutional clients
- **Derivatives role**: Support client activity, not proprietary trading
- **CDM relevance**: May be different — client servicing vs trading
- **Technology focus**: Operations, processing, reporting for clients

### Potential CDM Motivations

Custody banks may engage with CDM for different reasons:
1. **Client service**: Helping clients with CDM-based reporting
2. **Operational efficiency**: Processing client derivatives activity
3. **Market infrastructure**: Playing infrastructure role in derivatives ecosystem
4. **Regulatory support**: Assisting clients with regulatory reporting

### Hypothesis

**Primary Hypothesis**: Custody banks have different CDM drivers than investment banks — client service rather than trading.

**Alternative Hypothesis**: Custody banks may be less engaged with CDM given limited proprietary derivatives activity.

---

## Prior Probability Framework

### State Street
- **P(ARCHITECT) = 15%**
- Custody/asset servicing focus reduces CDM relevance
- May have client-service driven engagement
- Research focus: Client service vs proprietary CDM motivation

### BNY Mellon
- **P(ARCHITECT) = 15%**
- Similar custody focus as State Street
- May have market infrastructure angle
- Research focus: Infrastructure role in CDM ecosystem

---

## Key Research Questions

1. **Client Service Angle**
   - Are custody banks offering CDM services to clients?
   - Is CDM part of regulatory reporting support for clients?

2. **Infrastructure Role**
   - Are custody banks playing market infrastructure role in CDM ecosystem?
   - Partnership with CCPs or trade repositories?

3. **Proprietary Usage**
   - Do custody banks use CDM for their own derivatives activity?
   - Or purely client-facing capability?

4. **Comparison to Investment Banks**
   - How does custody bank CDM approach differ from dealers?
   - Different timeline or motivation?

---

## Regulatory Context

### Custody Bank Regulatory Profile
- **Federal Reserve**: Primary regulator as bank holding companies
- **SEC**: Securities-related activities
- **OCC**: National bank charter (some entities)
- **CFTC**: Less relevant than for derivatives dealers

### CFTC Rewrite Impact
- Less direct impact than on derivatives dealers
- May affect client service offerings
- Operational processing of client trades

---

## Execution Order

1. **State Street** (Rapid) - Larger custody bank
2. **BNY Mellon** (Rapid) - Comparison point

---

## Success Criteria

1. [ ] State Street CDM posture determined
2. [ ] BNY Mellon CDM posture determined
3. [ ] Custody bank vs investment bank CDM differences documented
4. [ ] Client service vs proprietary motivation assessed
5. [ ] Market infrastructure role evaluated

---

## Output Structure

Each bank assessment follows rapid assessment structure:
- `outputs/phase-9-us-custody-banks/{bank}/rapid-assessment.md`
- `outputs/phase-9-us-custody-banks/{bank}/status.json`

---

## Dependencies

- Phase 8 establishes US investment bank CDM patterns
- Custody banks provide contrasting business model perspective
- Informs understanding of CDM ecosystem beyond dealers

---

## Expected Outcome

**Most Likely**: Both custody banks classified as PRAGMATIST
- Derivatives not core to business model
- May offer client services via vendor
- Infrastructure role possible but limited evidence expected

**Possible Surprise**: ARCHITECT classification if custody banks have significant client-service CDM offering

---

*Phase 9: US Custody Banks*
*2 Banks | 3.0 Hours Total*
