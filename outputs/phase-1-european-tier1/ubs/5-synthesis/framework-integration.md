# Framework Integration: UBS Group AG

**Date**: 2024-12-19
**Analyst**: CDM Research Protocol
**Bank**: UBS Group AG
**Purpose**: Extract generalizable insights for CDM research framework

---

## Section 1: Framework Contribution Summary

This UBS assessment provides several generalizable insights for the CDM research framework, particularly regarding:
1. Post-M&A technology assessment methodology
2. Swiss/European disclosure norm adjustments
3. Evidence aging and temporal discounting
4. Borderline classification decision protocols
5. Adversarial process value demonstration

---

## Section 2: Methodological Learnings

### 2.1 Post-M&A Research Protocol

**Finding**: Major acquisitions create significant research complexity but do NOT necessarily eliminate CDM engagement.

**Framework Contribution**: When researching banks with recent major M&A activity:

| Scenario | Research Approach |
|----------|------------------|
| Acquirer rejected target tech | Assume acquirer CDM work preserved |
| Acquirer absorbed target tech | Research both entities' CDM history |
| Integration consuming capacity | Look for "maintenance mode" signals |
| Integration complete | Reassess as new entity |

**UBS-Specific Learning**: UBS's explicit rejection of Credit Suisse technology meant CDM research could focus on UBS history without CS complication.

### 2.2 Evidence Temporal Discounting

**Finding**: 5-year-old evidence (2020 pilot) requires significant discounting but is not invalidated if confirmed by recent activity (2025 contributions).

**Framework Contribution**: Evidence aging protocol:

| Evidence Age | Discount Factor | Exception |
|--------------|-----------------|-----------|
| 0-2 years | 1.0 (no discount) | None |
| 2-4 years | 0.8 | Continuation evidence present |
| 4-6 years | 0.6 | Strong continuation evidence |
| 6+ years | 0.4 | Only if confirmed by recent activity |

**Applied**: UBS 2020 pilot discounted by ~0.6, but presence of 2025 contributions provided continuation evidence.

### 2.3 Unquantified Evidence Handling

**Finding**: Evidence statements like "UBS contributed to CDM" without quantification require skeptical interpretation.

**Framework Contribution**: Quantification uncertainty protocol:

| Evidence Type | LR Adjustment |
|---------------|---------------|
| Specific quantified (X commits, Y lines) | Full LR |
| Named contributor, unquantified | 0.7 * LR |
| General "contributions" claim | 0.5 * LR |
| Implied from membership | 0.3 * LR |

**Applied**: FINOS contribution claim reduced from LR 5.0 to effective LR 3.0 due to lack of quantification.

---

## Section 3: Prior Probability Refinements

### 3.1 Derivatives-Dominant Bank Adjustment

**Framework Contribution**: The +10% adjustment for derivatives-dominant business is validated.

**Rationale**: Derivatives-heavy banks have:
- Higher CDM value proposition (complexity reduction)
- More ISDA engagement (CDM governance body)
- Greater standardization incentives (counterparty interoperability)

**Recommended Adjustment**: +8% to +12% depending on derivatives percentage of revenue

### 3.2 Integration Constraint Handling

**Finding**: Integration constraints should NOT be included in prior; they should be tested via evidence.

**Framework Contribution**: Separate capacity constraints from likelihood assessment:

| Factor | Prior Adjustment | Evidence Test |
|--------|------------------|---------------|
| Business profile | Include | Not needed |
| Historical engagement | Include | Confirmation search |
| Capacity constraints | Exclude | Test via activity search |
| Regulatory pressure | Include | Confirmation search |

**Applied**: UBS 35% prior did not discount for integration; evidence gathering tested whether integration blocked CDM.

---

## Section 4: Disconfirming Evidence Protocol

### 4.1 Expected Disconfirming Sources

**Framework Contribution**: Standardized disconfirming search battery for CDM research:

| Search | Purpose | Typical Impact |
|--------|---------|----------------|
| [Bank] CDM discontinued/ended | Find explicit withdrawal | High if found |
| [Bank] technology strategy -CDM | Check CDM absence from priorities | Moderate |
| [Bank] alternative standards (FpML, FIX) | Check competing investments | Low (usually complementary) |
| site:isda.org CDM showcase [Bank] | Check for showcase absence | Moderate |
| [Bank] regulatory reporting technology | Check for non-CDM reporting | Moderate |

### 4.2 Disconfirming LR Assignments

**Framework Contribution**: Standardized disconfirming evidence impact:

| Finding | Disconfirming LR |
|---------|-----------------|
| Not in ISDA showcase | 0.85 |
| CDM not in tech strategy | 0.90-0.95 |
| Non-CDM regulatory reporting | 0.85-0.90 |
| Alternative standards investment | 0.95 (usually neutral) |
| Technology headcount cuts | 0.90-0.95 |

**Applied**: UBS aggregate disconfirming LR = 0.73

---

## Section 5: Adversarial Process Refinements

### 5.1 Counter-Case Construction Guidelines

**Framework Contribution**: Counter-case should challenge:

1. **Evidence recency**: Apply maximum reasonable temporal discount
2. **Evidence quantification**: Assume minimum viable interpretation
3. **Evidence specificity**: Question CDM-specific vs. general relevance
4. **Capacity constraints**: Assume maximum constraint impact
5. **Production gap**: Require production evidence for high classifications

### 5.2 Steelman Defense Guidelines

**Framework Contribution**: Steelman should defend:

1. **Evidence existence**: Concrete evidence > inference
2. **Continuation signals**: Recent activity validates older evidence
3. **Direction consistency**: All evidence pointing same direction is significant
4. **Cultural factors**: Swiss discretion, European disclosure norms
5. **Classification definition**: ADOPTER ≠ production required

### 5.3 Adversarial Impact Calibration

**Finding**: UBS adversarial process reduced confidence by 11 percentage points (65% to 54%).

**Framework Contribution**: Expected adversarial impact ranges:

| Evidence Quality | Expected Reduction |
|------------------|-------------------|
| Strong, recent, quantified | 0-5% |
| Moderate, mixed recency | 5-10% |
| Older, unquantified | 10-15% |
| Weak, circumstantial | 15-25% |

**Applied**: UBS evidence (older, unquantified) correctly produced ~11% reduction.

---

## Section 6: Classification Boundary Protocols

### 6.1 Borderline Decision Framework

**Finding**: UBS at 54% required explicit boundary decision protocol.

**Framework Contribution**: When probability is within 5% of classification boundary:

| Tie-Breaker Criterion | Decision Rule |
|----------------------|---------------|
| Evidence direction | If all evidence points same direction, classify to higher tier |
| Evidence concreteness | Concrete evidence > absence/inference |
| Conservative bias | When uncertain, err toward lower classification |
| Business impact | Consider implications of misclassification |

**Applied**: UBS concrete positive evidence (pilot + contributions) justified ADOPTER despite 54% borderline.

### 6.2 Confidence Level Assignment

**Framework Contribution**: Standardized confidence level criteria:

| Confidence | Criteria |
|------------|----------|
| HIGH | 80% CI within classification tier, evidence <2 years, quantified |
| MODERATE | 80% CI mostly within tier, evidence <4 years |
| LOW | 80% CI spans boundary, evidence >4 years or unquantified |

**Applied**: UBS LOW confidence due to boundary-spanning CI and evidence age.

---

## Section 7: Swiss/European Bank Adjustments

### 7.1 Swiss Discretion Factor

**Finding**: Swiss banks consistently under-report technology initiatives publicly.

**Framework Contribution**: Swiss bank research protocol:

1. **Weight external sources**: ISDA, FINOS, consortium sources over corporate communications
2. **Accept null results on corporate sites**: Not disconfirming for Swiss banks
3. **Increase confidence in consortium evidence**: Swiss banks let consortiums communicate
4. **Widen confidence intervals**: +3-5% additional uncertainty

### 7.2 European Tier 1 Patterns

**Framework Contribution**: European Tier 1 bank CDM pattern observations:

| Pattern | Observation |
|---------|-------------|
| ISDA engagement | Typically through London offices |
| FINOS participation | Variable, not universal |
| Regulatory driver | EMIR/DRR more significant than US SEC |
| Disclosure norm | Less transparent than US banks |
| CDM leadership | Few European architects; mostly adopters/monitors |

---

## Section 8: Hypothesis Testing Protocol

### 8.1 Integration Capacity Hypothesis Template

**Framework Contribution**: Standard hypothesis template for M&A-affected banks:

```
Hypothesis: "[Integration event] is consuming all [initiative] capacity through [year]"

Test via:
1. Activity search for [initiative] post-[event]
2. Technology strategy analysis for [initiative] priority
3. Personnel/investment changes affecting [initiative]
4. Explicit statements about [initiative] during integration

Verdict criteria:
- REFUTED: Clear [initiative] activity post-event
- PARTIALLY REFUTED: Some activity but reduced
- CONFIRMED: No activity and explicit deprioritization
- INCONCLUSIVE: No activity but no explicit statements
```

**Applied**: UBS hypothesis "partially refuted" due to 2025 activity despite integration.

---

## Section 9: Output Quality Standards

### 9.1 Evidence Documentation Standards

**Framework Contribution**: Required evidence documentation:

| Field | Requirement |
|-------|-------------|
| Source URL | Direct link to evidence |
| Source type | Bank official, industry association, publication, etc. |
| Date | Publication/observation date |
| Quote | Direct quote where available |
| LR assignment | Explicit likelihood ratio with justification |
| Temporal flag | Age category and discount if applicable |

### 9.2 Bayesian Calculation Standards

**Framework Contribution**: Required calculation documentation:

1. Explicit prior justification with component breakdown
2. Individual evidence LRs with P(E|A) and P(E|~A)
3. Independence assessment and correlation adjustment
4. Pre- and post-adversarial calculations
5. Confidence interval with uncertainty source attribution

---

## Section 10: Cross-Bank Comparison Data

### 10.1 UBS Positioning Data

**Framework Contribution**: UBS metrics for cross-bank comparison:

| Metric | UBS Value |
|--------|-----------|
| Final Classification | ADOPTER (Low) |
| Final Probability | 54% |
| 80% CI Width | 24% (42%-66%) |
| Pre-Adversarial | 65% |
| Adversarial Impact | -11% |
| Prior | 35% |
| Primary LR (strongest) | 4.0 |
| Evidence Items | 7 |
| Null Results | 6 |
| Research Hours | N/A (automated) |

### 10.2 Comparable Bank Benchmarks

For future European Tier 1 assessments:

| Bank | Expected Profile |
|------|------------------|
| Deutsche Bank | Higher FINOS visibility, comparable complexity |
| Barclays | Higher CDM engagement (UK regulatory driver) |
| BNP Paribas | Similar discretion norms, French regulatory context |
| Credit Agricole | Less derivatives-focused, lower CDM incentive |
| Societe Generale | Comparable profile, French context |

---

## Section 11: Research Efficiency Observations

### 11.1 Search Efficiency

**Framework Contribution**: Search strategy efficiency observations:

| Search Type | Value | Notes |
|-------------|-------|-------|
| Bank + "Common Domain Model" | HIGH | Definitive when results found |
| site:isda.org Bank CDM | HIGH | Authoritative source |
| site:finos.org Bank | HIGH | Direct consortium evidence |
| Bank CDM + year | MODERATE | Provides temporal context |
| Bank derivatives technology | LOW | Too broad, requires filtering |
| Regulatory + CDM | LOW | Rarely yields bank-specific results |

### 11.2 Gate Decision Efficiency

**Finding**: Gate 1 "SKIP TO ADVERSARIAL" decision was correct for UBS.

**Framework Contribution**: Skip-to-adversarial criteria:

1. Two or more STRONG evidence items found
2. Evidence is specific (named participation, quotes)
3. Classification is above MONITOR threshold
4. Expected Tier 2 information value is LOW
5. Research objective can be tested with current evidence

---

## Section 12: Framework Update Recommendations

### 12.1 Recommended Framework Updates

Based on UBS research:

1. **Add M&A research protocol** to methodology documentation
2. **Formalize temporal discounting** with specific factors
3. **Standardize disconfirming search battery** across all assessments
4. **Add borderline decision protocol** for boundary cases
5. **Include Swiss/European disclosure adjustment** guidance

### 12.2 Template Updates

Recommended template additions:

1. Add "Major M&A Events" field to bank profile section
2. Add "Evidence Age" column to evidence tables
3. Add "Disconfirming LR" to adversarial documentation
4. Add "Confidence Level" (High/Moderate/Low) to final classification

---

## Section 13: Lessons Learned Summary

### 13.1 What Worked Well

1. **ISDA/FINOS primary source strategy** yielded strong evidence
2. **Hypothesis-driven approach** enabled clear testing
3. **Adversarial challenge** appropriately reduced overconfidence
4. **Tiered evidence gathering** with early stopping was efficient

### 13.2 What Could Improve

1. **FINOS contribution quantification** should be sought more aggressively
2. **GitHub commit analysis** could provide quantified evidence
3. **Personnel search** (LinkedIn) could identify CDM practitioners
4. **Conference presentation search** could yield recent activity

### 13.3 What Surprised

1. **UBS CDM contributions during integration** - demonstrated engagement persists despite constraints
2. **No Credit Suisse CDM legacy** - simplified research but surprising given CS's derivatives business
3. **Adversarial impact magnitude** - 11% reduction is significant and warranted

---

## Section 14: Future Research Priorities

### 14.1 UBS-Specific Follow-Up

- Q1 2027: Post-integration reassessment
- Monitor ISDA CDM showcases for UBS appearance
- Track FINOS contribution reports for quantification

### 14.2 Framework Research Priorities

- Develop automated GitHub contribution quantification
- Create European Tier 1 cross-comparison analysis
- Test M&A protocol on other recently-merged banks
- Validate temporal discounting factors empirically

---

*Document Version: 1.0*
*Framework Contributions: 12 methodological learnings*
*Template Updates Recommended: 4*
*Protocol Updates Recommended: 5*
