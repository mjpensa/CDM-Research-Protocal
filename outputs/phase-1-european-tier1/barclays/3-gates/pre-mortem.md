# Pre-Mortem Analysis: Barclays PLC

**Bank**: Barclays PLC
**Phase**: 1 (European Tier 1)
**Date**: 2025-12-21
**Prior P(Architect)**: 55%
**Framework Claim**: ARCHITECT-Follower (confirmed)
**Research Hypothesis**: Barclays meets upgrade criteria from Follower to Leader

---

## 1. Base Rate Context

### Prior Probability Justification
- **Base Rate (European Tier 1)**: 40%
- **Derivatives Dominant Adjustment**: +10% (major IRS, FX, equity derivatives franchises)
- **Confirmed FINOS Contributor**: +15% (active participation in open source)
- **UK Regulatory Environment**: +5% (home regulator for DRR pilot, EMIR Refit adoption)
- **Resulting Prior**: 55%

### Framework Position
Barclays is currently classified as ARCHITECT-Follower based on:
- Confirmed FINOS CDM contribution (open source)
- 2018 BOE/FCA DRR pilot participant
- Uncertain production deployment status
- Uncertain scope/depth of engagement

---

## 2. Known Evidence Summary

### Confirmed Facts
1. **FINOS Contribution**: Barclays is listed as a contributor to FINOS CDM repositories (source: github.com/finos)
2. **DRR Pilot**: Participated in 2018 Bank of England/FCA Digital Regulatory Reporting pilot
3. **Headquarters**: London, UK (subject to FCA/BOE regulation, EMIR Refit UK version)
4. **Derivatives Profile**: Major dealer in IRS, FX derivatives, equity derivatives

### Unknown Factors
1. **Depth of FINOS contribution**: Number of commits, scope, recency
2. **Production status**: Has pilot work progressed to production?
3. **Product coverage**: Which derivatives products use CDM?
4. **Jurisdiction rollout**: UK only, or expanded to EU/US?
5. **EMIR Refit response**: How did Barclays respond to September 2024 UK EMIR deadline?
6. **Vendor relationships**: Build internally or outsource to vendors?

---

## 3. Hypotheses to Test

### Primary Hypothesis: ARCHITECT-Leader Upgrade
**Hypothesis**: Barclays has progressed from experimental engagement (2018 DRR pilot) to production deployment, demonstrating leadership through sustained FINOS contribution and production-grade capabilities.

**Required Evidence**:
- Recent (2024-2025) FINOS commits or technical contributions
- Public announcements of production CDM deployment
- Evidence of EMIR Refit compliance using CDM
- Speaking engagements, thought leadership, or governance role in ISDA/FINOS
- Multi-jurisdiction or multi-product coverage

**Upgrade Criteria** (from Follower to Leader):
- Production deployment confirmed (not just pilot)
- Active technical contribution to FINOS/ISDA (recent commits)
- Thought leadership or governance participation
- Multi-product or multi-jurisdiction coverage

### Alternative Hypothesis 1: ARCHITECT-Follower Remains
**Hypothesis**: Barclays participated in early exploration (2018 DRR pilot, initial FINOS contribution) but has not progressed to production deployment or sustained technical leadership.

**Supporting Evidence Would Include**:
- Stale FINOS contributions (2018-2019 only, no recent activity)
- No announcements of production deployment
- Silence on EMIR Refit CDM usage
- Vendor outsourcing announcements (like HSBC-Delta Capita)

### Alternative Hypothesis 2: PRAGMATIST (Downgrade)
**Hypothesis**: Barclays' FINOS contribution was superficial or exploratory only; the bank has adopted a vendor-dependent or traditional compliance approach.

**Supporting Evidence Would Include**:
- Vendor outsourcing announcement (e.g., Delta Capita, Broadridge)
- Minimal FINOS commits (observer status only)
- No internal CDM team hiring signals
- Traditional derivatives platform announcements (Murex, Calypso without CDM modules)

---

## 4. Failure Modes (What Could Go Wrong)

### Research Failure Modes

#### Mode 1: UK Discretion Barrier
**Description**: UK banks, particularly Barclays, may follow Swiss-style discretion regarding technology positioning.
**Likelihood**: Medium
**Mitigation**: Focus on FINOS commits (verifiable), trade press (Risk.net, Waters), regulatory filings, job postings.
**Detection**: Exhaustive Tier 1/2 searches yield only 2018 DRR pilot reference.

#### Mode 2: Vendor Outsourcing (Post-Research Revelation)
**Description**: Barclays outsources CDM to vendor (e.g., Delta Capita), announced after research period or paywalled in vendor PR.
**Likelihood**: Medium
**Mitigation**: Check vendor press releases (Delta Capita, Broadridge, Regnosys), job postings for vendor product expertise.
**Detection**: Vendor press release without bank confirmation (Tier 2 max).

#### Mode 3: FINOS Contribution Misattribution
**Description**: FINOS commits attributed to "Barclays" are from individual contributors, not official bank engagement.
**Likelihood**: Low
**Mitigation**: Verify contributor email domains, check for organizational affiliation metadata in GitHub.
**Detection**: Email domains are personal (gmail.com) or commits are low-volume/isolated.

#### Mode 4: DRR Pilot Didn't Translate to Production
**Description**: 2018 DRR pilot was experimental only; Barclays did not continue to production deployment.
**Likelihood**: Medium-High
**Mitigation**: Search for post-2018 updates, EMIR Refit compliance announcements, recent BOE/FCA regulatory technology reports.
**Detection**: No evidence of activity between 2019-2025.

#### Mode 5: Conflicting Vendor Evidence
**Description**: Multiple vendor announcements conflict (e.g., Murex partnership AND Delta Capita outsourcing).
**Likelihood**: Low
**Mitigation**: Triangulate using job postings, official bank statements, regulatory filings.
**Detection**: Contradictory vendor claims require resolution in 3-gates/contradiction-resolution.md.

### Classification Failure Modes

#### Mode 6: Over-Weighting Historical Evidence
**Description**: 2018 DRR pilot drives classification despite lack of recent activity.
**Likelihood**: Medium
**Mitigation**: Apply temporal thresholds (CLAUDE.md Section 6); downweight evidence >3 years old unless corroborated.
**Detection**: Final confidence rests on single 2018 source.

#### Mode 7: Under-Weighting Negative Evidence
**Description**: Informative absence (no production announcements, no EMIR Refit CDM references) is dismissed.
**Likelihood**: Medium
**Mitigation**: Document null results; apply Bayesian updates for informative absences.
**Detection**: High confidence despite exhaustive null results in Tier 1/2.

---

## 5. Search Strategy Calibration

### Tier 1 Priority Targets
1. **FINOS GitHub Repositories**:
   - `github.com/finos/common-domain-model` (commits, issues, PRs)
   - Contributor metadata (email domains, organizational affiliation)
   - Temporal distribution of commits (recent vs. historical)

2. **ISDA Official Sources**:
   - ISDA.org member announcements, working groups
   - CDM Steering Committee membership
   - ISDA conference presentations (2023-2025)

3. **UK Regulatory Sources**:
   - FCA publications mentioning Barclays + DRR/CDM
   - Bank of England FinTech Hub updates
   - EMIR Refit compliance reports (September 2024 deadline)

4. **Barclays Official Domain**:
   - `site:home.barclays` CDM, ISDA, DRR, EMIR
   - Annual reports (2023, 2024) for technology/regulatory mentions

### Tier 2 Priority Targets
1. **Trade Press**:
   - Risk.net: Barclays ISDA CDM, Barclays DRR, Barclays derivatives reporting
   - Waters Technology: Barclays CDM, Barclays FINOS
   - Financial News London: Barclays regulatory technology

2. **Conference Sources**:
   - ISDA Annual Conference 2024, 2023
   - FINOS Open Source in Finance 2024, 2023
   - A-Team Innovation Awards, RegTech Summit

3. **Vendor Press Releases**:
   - Delta Capita (Elaris platform announcements)
   - Regnosys (CDM implementation partnerships)
   - Murex, Calypso (platform upgrade announcements)

### Tier 3 Priority Targets
1. **Job Postings**:
   - LinkedIn Jobs: Barclays + "ISDA CDM", "Common Domain Model", "Rosetta DSL"
   - Barclays careers page: Derivatives technology, regulatory reporting roles

2. **LinkedIn Signals**:
   - Barclays employee profiles mentioning CDM, ISDA, DRR
   - LinkedIn posts by Barclays executives about regulatory technology

---

## 6. Negative Facts Pre-Check

### Relevant Patterns from knowledge_base/negative_facts.md
1. **FINOS != CDM**: Verify FINOS contribution is specifically to CDM repositories, not Waltz, Legend, Fluxnova.
2. **2018 DRR Pilot**: Hackathon/pilot participation does not imply sustained production usage; check for post-event follow-through.
3. **UK Bank Discretion**: UK banks may not publicize technology choices on corporate sites; prioritize trade press and FINOS commits.
4. **Working Group Membership**: ISDA CDM working group membership is "observer" status, not production adoption.

### Searches to Avoid
- `"Barclays derivatives reporting"` (too vague, returns generic compliance articles)
- `"Barclays FINOS"` alone (may return non-CDM projects)
- `"Barclays regulatory technology"` (too broad, RegTech includes KYC/AML)
- `site:home.barclays CDM` (UK banks rarely publish tech stack details on corporate sites)

---

## 7. Reasoning Checkpoints

### Gate 1: Post-Tier 1 Assessment
**Key Question**: Is there direct evidence of production CDM usage or sustained FINOS contribution?

**Decision Criteria**:
- If **YES** (recent FINOS commits, production announcement, EMIR Refit CDM usage) → Proceed to Tier 2 to assess depth/leadership.
- If **PARTIAL** (FINOS contributions exist but unclear scope) → Proceed to Tier 2 for triangulation.
- If **NO** (only 2018 DRR pilot, stale FINOS contributions) → Proceed to Tier 2/3 to check vendor outsourcing or downgrade.

### Gate 2: Post-Tier 2 Assessment
**Key Question**: Can we triangulate Tier 1 findings with industry sources?

**Decision Criteria**:
- If Tier 1 shows production usage → Look for trade press corroboration, conference presentations.
- If Tier 1 shows minimal engagement → Look for vendor outsourcing announcements, traditional platform usage.
- If Tier 1 is null → Look for informative absences (what does silence mean?).

### Gate 3: Post-Tier 3 Assessment
**Key Question**: Do hiring signals or LinkedIn activity support or contradict higher-tier findings?

**Decision Criteria**:
- Hiring for "ISDA CDM" roles supports internal build hypothesis.
- Hiring for "Murex" or "Calypso" without CDM mentions suggests traditional approach.
- No CDM hiring signals after exhaustive search suggests vendor outsourcing or non-adoption.

---

## 8. Red Flags to Watch For

### Evidence Quality Red Flags
1. **Single Source Dependency**: All evidence comes from one source (e.g., only 2018 DRR pilot).
2. **Temporal Gap**: Evidence exists for 2018 but nothing for 2019-2025 (suggests abandoned effort).
3. **Vendor-Only Claims**: Vendor announces Barclays partnership without bank confirmation.
4. **Contradictory Signals**: Job postings for Murex experts while FINOS commits suggest internal CDM build.

### Trust Flags to Monitor
- `SINGLE_SOURCE_CLAIM`: If all evidence rests on 2018 DRR pilot.
- `STALE_EVIDENCE`: If FINOS contributions are all 2018-2019.
- `LOW_TIER_ONLY`: If no Tier 1/2 evidence exists (only LinkedIn/job postings).
- `MISSING_CORROBORATION`: If production usage claimed but no trade press coverage.

---

## 9. Success Criteria

### Minimum Viable Classification
To classify Barclays as **ARCHITECT-Leader**, require:
1. **Production Evidence**: Tier 1 or 2 evidence of production CDM usage (not just pilot).
2. **Technical Contribution**: Recent (2023-2025) FINOS commits or technical artifacts.
3. **Leadership Indicators**: Governance role, conference speaking, thought leadership, OR multi-jurisdiction/product coverage.
4. **Confidence**: ≥75% confidence based on triangulated Tier 1/2 evidence.

To classify Barclays as **ARCHITECT-Follower** (status quo), require:
1. **Confirmed FINOS Contribution**: Verifiable commits to FINOS CDM (any timeframe).
2. **No Production Evidence**: Absence of production deployment announcements.
3. **No Leadership Indicators**: No governance role or thought leadership.
4. **Confidence**: ≥60% confidence.

To classify Barclays as **PRAGMATIST**, require:
1. **Vendor Outsourcing Evidence**: Confirmed vendor relationship for CDM (Tier 1/2).
2. **Minimal Internal Capability**: No internal CDM team, no FINOS contributions, OR superficial contributions only.
3. **Confidence**: ≥60% confidence.

---

## 10. Estimated Timelines

### Research Execution
- **Tier 1 Searches**: 2-3 hours (FINOS GitHub, ISDA, FCA, Barclays official)
- **Tier 2 Searches**: 2-3 hours (Risk.net, Waters, vendors, conferences)
- **Tier 3 Searches**: 1-2 hours (LinkedIn, job postings)
- **Total Research Time**: 5-8 hours

### Processing & Analysis
- **evidence.json compilation**: 1 hour
- **Bayesian updates**: 30 minutes
- **Gate assessments**: 1 hour
- **Adversarial challenge**: 1 hour
- **Synthesis assessment**: 2-3 hours
- **Total Processing Time**: 5.5-6.5 hours

**Total Estimated Time**: 10.5-14.5 hours

---

## 11. Pre-Mortem Prediction

### Most Likely Outcome
**Classification**: ARCHITECT-Follower (status quo maintained)
**Confidence**: 65%
**Rationale**: Barclays likely participated in 2018 DRR pilot and contributed to FINOS in early stages but has not progressed to production deployment or sustained technical leadership. Evidence will show historical engagement without recent activity.

### Alternative Outcome 1
**Classification**: ARCHITECT-Leader (upgrade)
**Confidence**: 25%
**Rationale**: Barclays has sustained FINOS contribution and deployed CDM in production for EMIR Refit compliance. Evidence will show recent commits, production announcements, and thought leadership.

### Alternative Outcome 2
**Classification**: PRAGMATIST-Vendor-Dependent (downgrade)
**Confidence**: 10%
**Rationale**: Barclays outsourced CDM to vendor (e.g., Delta Capita, Broadridge). FINOS contribution was superficial or exploratory only. Evidence will show vendor partnership announcement without internal capability.

---

## 12. Commitments

### Epistemic Commitments
1. Evidence-First: No claim without citation.
2. Null Hypothesis: Assume PRAGMATIST until evidence proves otherwise.
3. Temporal Discounting: Apply weight multipliers per CLAUDE.md Section 6.
4. Triangulation: Require corroboration for high-confidence claims.

### Process Commitments
1. Execute all three tiers regardless of early findings.
2. Document null results with informative absence assessment.
3. Resolve contradictions explicitly in 3-gates/contradiction-resolution.md.
4. Apply Bayesian updates after each tier.
5. Execute adversarial challenge before final synthesis.

### Output Commitments
1. Ledger-First: evidence.json is PRIMARY output.
2. All Markdown files rendered from evidence.json.
3. Confidence calibration follows 6-step framework from config/decision-thresholds.json.
4. Final classification includes knowledge gaps and primary research recommendations.

---

**Pre-Mortem Complete. Proceeding to Tier 1 Research.**
