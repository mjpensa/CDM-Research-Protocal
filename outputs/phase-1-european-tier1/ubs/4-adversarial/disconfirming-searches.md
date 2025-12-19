# Disconfirming Searches: UBS Group AG

**Date**: 2024-12-19
**Analyst**: CDM Research Protocol (Adversarial Mode)
**Bank**: UBS Group AG
**Objective**: Search for evidence that would DISCONFIRM ADOPTER classification

---

## Purpose

This document records searches specifically designed to find evidence AGAINST the current ADOPTER classification. Disconfirming searches test the robustness of the classification by actively seeking counter-evidence.

---

## Disconfirming Search 1: CDM Pilot Discontinuation

**Search Query**: `UBS CDM pilot discontinued ended stopped`

**Hypothesis**: If UBS discontinued CDM pilot, it would indicate MONITOR not ADOPTER

**Expected Disconfirming Evidence**: Announcements of pilot termination, personnel changes, strategy pivots away from CDM

**Actual Results**: No results found indicating pilot discontinuation

**Interpretation**: Absence of discontinuation evidence is weakly supportive of continued engagement. However, absence of evidence is not strong confirmation - many discontinued projects are never announced.

**Impact on Classification**: NEUTRAL (no disconfirming evidence found)

---

## Disconfirming Search 2: UBS Technology Strategy Without CDM

**Search Query**: `UBS derivatives technology strategy 2024 2025 -CDM`

**Hypothesis**: If UBS's technology strategy explicitly excludes CDM or focuses elsewhere, it would indicate lower CDM priority

**Expected Disconfirming Evidence**: Technology roadmaps, strategy announcements that don't mention CDM

**Actual Results**: UBS technology strategy focuses on:
- AI and machine learning
- Digital investment bank transformation
- Credit Suisse integration
- Client experience improvements

**Interpretation**: CDM is NOT mentioned in UBS's public technology strategy narrative. However, this is consistent with both:
- CDM work happening quietly (Swiss discretion)
- CDM not being a priority

**Impact on Classification**: WEAKLY DISCONFIRMING (CDM not in public tech narrative)

---

## Disconfirming Search 3: UBS Alternative Standards Adoption

**Search Query**: `UBS FpML FIX protocol derivatives messaging`

**Hypothesis**: If UBS is investing in alternative standards (FpML, FIX), it might indicate lower CDM priority

**Expected Disconfirming Evidence**: Announcements of FpML or FIX protocol implementations instead of CDM

**Actual Results**:
- UBS uses FpML for electronic derivatives trading
- UBS is active in FIX protocol community
- These are complementary to CDM, not alternatives

**Interpretation**: Use of FpML and FIX is expected for any derivatives dealer. These are message protocols while CDM is a data model - they serve different purposes and can coexist.

**Impact on Classification**: NEUTRAL (not disconfirming - complementary technologies)

---

## Disconfirming Search 4: UBS FINOS Non-CDM Focus

**Search Query**: `UBS FINOS Vuu Perspective Legend -CDM`

**Hypothesis**: If UBS's FINOS engagement is entirely non-CDM projects, it would undermine CDM inference

**Expected Disconfirming Evidence**: UBS highlighted for other FINOS projects with no CDM mention

**Actual Results**:
- UBS is mentioned for contributions to Vuu
- UBS contributed to Open Source Readiness SIG
- UBS contributed to FSOSD exam development
- CDM contributions also mentioned but less prominently

**Interpretation**: UBS's FINOS engagement is BROADER than just CDM. CDM is one of multiple projects. However, CDM contributions are explicitly mentioned, so this doesn't fully disconfirm.

**Impact on Classification**: WEAKLY DISCONFIRMING (CDM is not UBS's primary FINOS focus)

---

## Disconfirming Search 5: Credit Suisse CDM Investment Prior to Acquisition

**Search Query**: `"Credit Suisse" CDM implementation technology before UBS`

**Hypothesis**: If Credit Suisse had significant CDM investment, its abandonment by UBS would be disconfirming

**Expected Disconfirming Evidence**: CS CDM initiatives that were discontinued post-acquisition

**Actual Results**: No evidence of Credit Suisse CDM initiatives found

**Interpretation**: Credit Suisse appears to NOT have been a CDM participant. This is:
- Confirming of UBS-native CDM engagement
- Not disconfirming of current classification

**Impact on Classification**: NEUTRAL (no CS CDM legacy to abandon)

---

## Disconfirming Search 6: UBS Technology Headcount Cuts

**Search Query**: `UBS technology layoffs cuts 2024 2025 Credit Suisse integration`

**Hypothesis**: Significant technology headcount cuts would indicate reduced capacity for CDM initiatives

**Expected Disconfirming Evidence**: Announcements of technology team reductions affecting CDM-relevant areas

**Actual Results**:
- UBS cut 13,000 roles post-Credit Suisse (total company)
- Technology roles were affected but specific numbers not disclosed
- UBS also hired CS programmers for algorithmic trading
- Net technology impact is mixed

**Interpretation**: There were headcount reductions, but also selective hiring in strategic areas. Cannot determine CDM-specific impact from public sources.

**Impact on Classification**: WEAKLY DISCONFIRMING (capacity constraints are real but unquantified)

---

## Disconfirming Search 7: No UBS in ISDA CDM Showcase

**Search Query**: `site:isda.org CDM showcase case study UBS`

**Hypothesis**: If UBS is not featured in ISDA CDM success stories, it would indicate lower implementation maturity

**Expected Disconfirming Evidence**: ISDA CDM showcases that don't include UBS

**Actual Results**: UBS is not prominently featured in recent ISDA CDM case studies or showcase materials. Most CDM showcase content features:
- Barclays (DRR)
- REGnosys (technology provider)
- Bloomberg (data services)
- Various RegTech vendors

**Interpretation**: UBS's absence from CDM showcase materials suggests they haven't achieved notable CDM milestones worth publicizing. This is consistent with MONITOR status more than ADOPTER.

**Impact on Classification**: MODERATELY DISCONFIRMING (not showcased despite pilot participation)

---

## Disconfirming Search 8: UBS Regulatory Reporting Without CDM

**Search Query**: `UBS EMIR reporting technology 2024 -CDM`

**Hypothesis**: If UBS's regulatory reporting doesn't use CDM, it indicates CDM is not operationalized

**Expected Disconfirming Evidence**: UBS using non-CDM technology for derivatives reporting

**Actual Results**:
- UBS complies with EMIR, SFTR, FINFRAG
- No mention of CDM in regulatory reporting context
- Reporting appears to use traditional infrastructure

**Interpretation**: UBS's regulatory reporting does not appear to leverage CDM. Given that DRR (Digital Regulatory Reporting built on CDM) is ISDA's flagship CDM use case, absence of CDM in UBS reporting is meaningful.

**Impact on Classification**: MODERATELY DISCONFIRMING (key CDM use case not adopted)

---

## Disconfirming Evidence Summary

| Search | Result | Impact |
|--------|--------|--------|
| Pilot discontinuation | Not found | NEUTRAL |
| Tech strategy without CDM | CDM not mentioned | WEAKLY DISCONFIRMING |
| Alternative standards | Complementary | NEUTRAL |
| FINOS non-CDM focus | Broader engagement | WEAKLY DISCONFIRMING |
| CS CDM prior | No CS CDM | NEUTRAL |
| Tech headcount cuts | Mixed | WEAKLY DISCONFIRMING |
| ISDA showcase absence | Not featured | MODERATELY DISCONFIRMING |
| Regulatory reporting | Non-CDM | MODERATELY DISCONFIRMING |

---

## Aggregate Disconfirming Impact

**Total Disconfirming Signals**: 5 (2 moderate, 3 weak)
**Total Neutral**: 3

### Disconfirming LR Adjustment

| Factor | LR Adjustment |
|--------|---------------|
| No ISDA showcase | 0.8 |
| Non-CDM regulatory reporting | 0.85 |
| CDM not in tech strategy | 0.9 |
| FINOS broader than CDM | 0.95 |
| Headcount concerns | 0.95 |

**Aggregate Disconfirming LR**: 0.8 * 0.85 * 0.9 * 0.95 * 0.95 = 0.55

### Impact on Posterior

```
Original Posterior Odds = 1.883
Disconfirming Adjustment = 0.55
Adjusted Posterior Odds = 1.883 * 0.55 = 1.036
Adjusted P(Architect) = 1.036 / 2.036 = 50.9%
```

**Post-Disconfirming Classification**: MONITOR (borderline ADOPTER)

---

## Conclusion

Disconfirming searches reveal meaningful evidence against ADOPTER classification:

1. **UBS is not featured in CDM showcase materials** despite 2020 pilot participation
2. **UBS regulatory reporting does not use CDM** (key use case not adopted)
3. **CDM is not part of UBS public technology narrative**
4. **UBS's FINOS engagement is broader than CDM**

These findings suggest the original 65% ADOPTER classification may be **5-15% too high**.

**Revised Range**: 50-60% (borderline ADOPTER/MONITOR)

---

*Document Version: 1.0*
*Searches Conducted: 8*
*Disconfirming Impact: Moderate*
