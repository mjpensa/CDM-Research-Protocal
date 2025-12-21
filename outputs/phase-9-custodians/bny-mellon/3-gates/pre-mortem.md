# Pre-Mortem: The Bank of New York Mellon Corporation

**Bank**: The Bank of New York Mellon Corporation
**Date**: 2025-12-21
**Stage**: Pre-Search Analysis

---

## Scenario

*"Six months from now, our research classified BNY Mellon incorrectly. What went wrong?"*

---

## Failure Mode 1: False Negative (Missed ARCHITECT/PRAGMATIST Evidence)

### How This Could Happen:
1. **Innovation Hub Activity**: CDM work conducted at Dublin Digital R&D Hub or Ascent Program not publicly disclosed
2. **Private FINOS Membership**: BNY Mellon member but not listed publicly
3. **Vendor Partnership**: Using Bloomberg/DTCC CDM solutions under NDA
4. **Recent Announcement**: CDM initiative announced after research cutoff date
5. **Regional Activity**: CDM work in European or APAC entities not captured by US-focused search

### Mitigation Strategies:
- Search BNY Mellon Innovation Centers and Ascent Program separately
- Check FINOS membership list thoroughly
- Review Bloomberg, DTCC, SimCorp case studies for BNY Mellon
- Set clear research cutoff date (2025-12-21)
- Include European fintech press (FinExtra, Finextra)

---

## Failure Mode 2: False Positive (Over-Interpreting Weak Signals)

### How This Could Happen:
1. **Generic Fintech**: Confusing Ascent Program fintech work with CDM-specific initiatives
2. **Vendor Hype**: Trusting vendor claims without BNY Mellon confirmation
3. **Innovation Theater**: Interpreting innovation marketing as actual CDM engagement
4. **Employee Speculation**: Over-weighting LinkedIn posts about potential CDM interest

### Mitigation Strategies:
- Require explicit "CDM" or "ISDA Common Domain Model" in evidence
- Demand bank confirmation for vendor claims
- Distinguish innovation programs from CDM-specific work
- Verify employee claims against official communications

---

## Failure Mode 3: Search Execution Errors

### How This Could Happen:
1. **Brand Variations**: Missing "The Bank of New York Mellon", "BNYM", "Mellon" variations
2. **Subsidiary Confusion**: Not checking Pershing, BNY Mellon Wealth Management separately
3. **Innovation Hub Oversight**: Not searching Dublin Digital Hub, Ascent Program thoroughly
4. **Date Range Issues**: Missing recent announcements due to search indexing lag

### Mitigation Strategies:
- Use multiple search terms: "BNY Mellon", "Bank of New York Mellon", "BNYM"
- Check Pershing and wealth management subsidiaries separately
- Dedicated search for innovation hub CDM activity
- Use date filters + manual verification

---

## Failure Mode 4: Classification Boundary Errors

### How This Could Happen:
1. **Innovation Inference**: Assuming Ascent Program implies CDM exploration without evidence
2. **Custodian Model Bias**: Expecting custodians not to adopt CDM
3. **Confidence Miscalibration**: Setting confidence too high or too low

### Mitigation Strategies:
- Evidence-First mandate: innovation programs ≠ CDM engagement
- Evaluate objectively regardless of business model
- Follow protocol confidence caps (35% max for inference-only)
- Document reasoning for confidence calibration

---

## Pre-Registered Hypotheses

### Hypothesis 1: UNKNOWN Classification Most Likely
**Prediction**: BNY Mellon will have no public CDM signals across Tier 1-3
**Basis**: No preliminary signals found; custodian business model may not prioritize CDM
**Disconfirmation Criteria**: Any Tier 1 or Tier 2 evidence of CDM engagement

### Hypothesis 2: Higher Confidence Than State Street
**Prediction**: If UNKNOWN, confidence will be 35% (vs State Street 30%)
**Basis**: Active fintech programs suggest higher likelihood of private exploration
**Disconfirmation Criteria**: Finding evidence that BNY Mellon is less innovative than assumed

### Hypothesis 3: If Evidence Exists, Likely Through Innovation Hubs
**Prediction**: If CDM adoption found, will be via Dublin Digital Hub or Ascent Program
**Basis**: Innovation centers most likely locus for new technology exploration
**Disconfirmation Criteria**: Finding CDM work in traditional custody operations

---

## Search Quality Checklist

Before finalizing classification, verify:

- [ ] Checked FINOS membership list
- [ ] Searched GitHub finos/common-domain-model contributors
- [ ] Reviewed bnymellon.com official newsroom (12-month lookback)
- [ ] Searched Risk.net for "BNY Mellon" + "CDM"
- [ ] Searched Waters Technology for "BNY Mellon" + "ISDA"
- [ ] Checked LinkedIn jobs for "BNY Mellon" + "CDM"
- [ ] Reviewed BNY Mellon investor presentations
- [ ] Searched vendor case studies (Bloomberg, DTCC, SimCorp, Broadridge)
- [ ] Checked ISDA, FINOS conference speaker lists
- [ ] Searched BNY Mellon Ascent Program announcements
- [ ] Searched Dublin Digital R&D Hub announcements
- [ ] Checked Pershing (subsidiary) separately

---

## Red Flags to Watch For

1. **Innovation Bias**: Assuming fintech programs imply CDM work
2. **Confirmation Bias**: Finding UNKNOWN and stopping search prematurely
3. **Availability Bias**: Over-weighting easily findable generic fintech content
4. **Peer Comparison Error**: Assuming BNY Mellon same as State Street without independent analysis

---

## Success Criteria

Research will be considered successful if:

1. **Comprehensive Coverage**: All Tier 1-3 source types searched, including innovation hubs
2. **Transparent Documentation**: Search strategy and null results clearly documented
3. **Calibrated Confidence**: Confidence appropriately set (expect 35% if UNKNOWN)
4. **State Street Comparison**: Explicitly compare findings to justify confidence differential

---

**Commitment**: This pre-mortem will be reviewed post-search to identify any materialized failure modes.
