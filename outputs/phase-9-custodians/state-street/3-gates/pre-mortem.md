# Pre-Mortem: State Street Corporation

**Bank**: State Street Corporation
**Date**: 2025-12-21
**Stage**: Pre-Search Analysis

---

## Scenario

*"Six months from now, our research classified State Street incorrectly. What went wrong?"*

---

## Failure Mode 1: False Negative (Missed ARCHITECT/PRAGMATIST Evidence)

### How This Could Happen:
1. **Private CDM Implementation**: State Street deployed CDM internally without public announcement
2. **Vendor White-Labeling**: Using CDM-based vendor solution under different branding
3. **Subsidiary Activity**: CDM adoption by State Street Digital or regional entity not captured
4. **Recent Developments**: CDM announcement made after research completion
5. **Paywalled Content**: Key evidence behind subscription walls (Risk.net Premium, etc.)

### Mitigation Strategies:
- Search State Street investor presentations and earnings calls for CDM mentions
- Check vendor case studies (Bloomberg, DTCC, SimCorp) for State Street references
- Review State Street Digital and innovation hub announcements separately
- Set research cutoff date clearly and monitor for subsequent announcements
- Attempt access to paywalled trade press archives

---

## Failure Mode 2: False Positive (Over-Interpreting Weak Signals)

### How This Could Happen:
1. **Generic Derivatives Technology**: Confusing general derivatives tech with CDM-specific work
2. **Vendor Marketing**: Treating vendor claims as bank confirmation without independent verification
3. **Conference Attendance**: Interpreting passive attendance as active engagement
4. **Employee LinkedIn Hype**: Over-weighting individual employee posts without institutional backing

### Mitigation Strategies:
- Require explicit "CDM" or "ISDA Common Domain Model" language in sources
- Demand bank confirmation for vendor-sourced claims
- Distinguish between speaker roles vs. attendee roles at conferences
- Verify employee claims against official State Street communications

---

## Failure Mode 3: Search Execution Errors

### How This Could Happen:
1. **Incorrect Search Terms**: Missing State Street branding variations ("SSC", "State Street Global Services")
2. **Domain Restrictions**: Not checking statestreet.com subdomains thoroughly
3. **Date Range Issues**: Missing recent announcements due to search engine indexing lag
4. **Geographic Bias**: Focusing on US sources while missing European/APAC announcements

### Mitigation Strategies:
- Use multiple search term variations: "State Street", "SSC", "State Street Corporation", "State Street Global Services"
- Manually check statestreet.com/newsroom and investors.statestreet.com
- Use Google date filters + manual verification of dates
- Search international trade press (European Fund Management, Asian Banking & Finance)

---

## Failure Mode 4: Classification Boundary Errors

### How This Could Happen:
1. **OBSERVER Misclassification**: Weak signals present but dismissed, should be OBSERVER not UNKNOWN
2. **Custodian Model Assumption**: Assuming custodians don't adopt CDM without evidence
3. **Confidence Miscalibration**: Setting confidence too high given uncertainty

### Mitigation Strategies:
- Apply strict evidence thresholds: OBSERVER requires at minimum membership/participation signal
- Avoid business model stereotyping - evaluate evidence objectively
- Cap confidence per protocol (35% max for inference-only)
- Document reasoning for classification boundary decisions

---

## Pre-Registered Hypotheses

### Hypothesis 1: UNKNOWN Classification Most Likely
**Prediction**: State Street will have no public CDM signals across Tier 1-3
**Basis**: Custodian business model may not prioritize CDM; no preliminary signals found
**Disconfirmation Criteria**: Any Tier 1 or Tier 2 evidence of CDM engagement

### Hypothesis 2: If Evidence Exists, Likely PRAGMATIST (Vendor-Led)
**Prediction**: If CDM adoption found, will be through vendor solution (SimCorp, Bloomberg)
**Basis**: Custodians typically consume technology rather than building in-house
**Disconfirmation Criteria**: Evidence of internal CDM development team or FINOS contributions

### Hypothesis 3: Confidence Will Not Exceed 35%
**Prediction**: Absence of evidence will limit confidence to inference-only tier
**Basis**: No disconfirming evidence available; cannot rule out private exploration
**Disconfirmation Criteria**: Finding explicit "we are not pursuing CDM" statement (would raise confidence in UNKNOWN)

---

## Search Quality Checklist

Before finalizing classification, verify:

- [ ] Checked FINOS membership list
- [ ] Searched GitHub finos/common-domain-model contributors
- [ ] Reviewed statestreet.com official newsroom (12-month lookback)
- [ ] Searched Risk.net for "State Street" + "CDM"
- [ ] Searched Waters Technology for "State Street" + "ISDA"
- [ ] Checked LinkedIn jobs for "State Street" + "CDM"
- [ ] Reviewed State Street investor presentations
- [ ] Searched vendor case studies (Bloomberg, DTCC, SimCorp, Broadridge)
- [ ] Checked conference speaker lists (ISDA, FINOS events)
- [ ] Searched international trade press (not just US sources)

---

## Red Flags to Watch For

1. **Confirmation Bias**: Finding UNKNOWN and stopping search prematurely
2. **Availability Bias**: Over-weighting easily findable generic derivatives content
3. **Recency Bias**: Focusing only on 2024-2025 news and missing older foundational evidence
4. **Authority Bias**: Trusting vendor marketing without independent verification

---

## Success Criteria

Research will be considered successful if:

1. **Comprehensive Coverage**: All Tier 1-3 source types searched
2. **Transparent Documentation**: Search strategy and null results clearly documented
3. **Calibrated Confidence**: Confidence level matches evidence strength per protocol
4. **Falsifiable Claims**: Classification can be updated if new evidence emerges

---

**Commitment**: This pre-mortem will be reviewed post-search to identify any materialized failure modes.
