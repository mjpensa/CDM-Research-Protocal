# Pre-Mortem Analysis: HSBC Holdings PLC
**Date**: 2025-12-21
**Researcher**: Claude Opus 4.5
**Prior P(Architect)**: 40%

---

## Executive Summary

HSBC presents a CRITICAL classification boundary case. The January 2025 Delta Capita contract for "CDM connectivity" could indicate either:
- **ARCHITECT scenario**: HSBC building internal CDM capability, using Delta Capita for connectivity layer
- **PRAGMATIST scenario**: HSBC outsourcing CDM entirely to vendor without internal development

This pre-mortem identifies failure modes that could lead to incorrect classification.

---

## Known Evidence Baseline

### Confirmed Facts (from manifest)
1. **Delta Capita Contract (January 2025)**: Vendor relationship for CDM connectivity
2. **2018 UK DRR Pilot**: Participant in FCA/BoE Digital Regulatory Reporting pilot
3. **Headquarters**: London, UK (subject to FCA, PRA, EMIR Refit)
4. **Global Operations**: Major presence in Hong Kong (HKMA) and Singapore (MAS)

### Critical Ambiguities
- **Scope of Delta Capita engagement**: Build-only? Operate? Both?
- **Internal capability**: Does HSBC have internal CDM team alongside vendor?
- **Pilot legacy**: Did 2018 participation create sustained internal capability?
- **Asian regulators**: Do HKMA/MAS requirements drive additional CDM adoption?

---

## Failure Mode Analysis

### Failure Mode 1: Vendor Relationship Misclassification
**Risk**: Classifying as ARCHITECT based solely on vendor engagement without evidence of internal capability.

**Why It Could Happen**:
- Delta Capita announcement uses aspirational language ("CDM transformation", "modernization")
- Vendor marketing materials emphasize partnership rather than outsourcing
- Press releases omit operational details

**Mitigation Strategy**:
- Search for HSBC job postings for CDM developers, ISDA modelers, or internal CDM roles
- Look for HSBC-authored conference presentations or technical papers on CDM
- Search for HSBC contributions to FINOS/ISDA CDM repositories
- Distinguish between "HSBC is implementing CDM" (ambiguous) vs "HSBC has internal CDM development team" (specific)

**Disconfirming Evidence to Seek**:
- Statements indicating "full outsourcing" or "managed service"
- Absence of HSBC technical staff in CDM working groups
- Delta Capita positioning as primary CDM operator, not just integrator

---

### Failure Mode 2: Pilot Participation Overweighting
**Risk**: Treating 2018 UK DRR pilot as evidence of current production capability.

**Why It Could Happen**:
- Pilot was high-profile FCA initiative with strong public documentation
- HSBC participation demonstrates early interest
- Lack of follow-up reporting leaves status ambiguous

**Mitigation Strategy**:
- Apply temporal threshold: 2018 evidence is >7 years old (Historical category, 0.3 weight)
- Search explicitly for "HSBC DRR production", "HSBC pilot to production", "HSBC regulatory reporting modernization 2024-2025"
- Check FCA/BoE publications for post-pilot outcomes
- Look for evidence pilot was discontinued, scaled back, or transitioned to vendor solution

**Disconfirming Evidence to Seek**:
- Statements that pilot ended without production deployment
- Shift from internal development to vendor procurement post-2018
- Absence of any 2019-2025 references to continued DRR work

---

### Failure Mode 3: Regulatory Mandate Inference Without Evidence
**Risk**: Assuming EMIR Refit/CFTC Rewrite mandates mean HSBC must be adopting CDM.

**Why It Could Happen**:
- HSBC is major derivatives player subject to these regulations
- Industry commentary suggests CDM is optimal path to compliance
- Absence of evidence interpreted as "they must be doing it privately"

**Mitigation Strategy**:
- Do NOT classify as ARCHITECT based on regulatory exposure alone (would be Tier 4 inference, max 35% confidence)
- Search for specific HSBC statements on EMIR Refit/CFTC compliance strategy
- Look for evidence of alternative compliance approaches (traditional vendor upgrades, manual reporting)
- Require Tier 1/2 evidence of CDM-specific implementation

**Disconfirming Evidence to Seek**:
- HSBC using traditional reporting solutions (TradeSphere, etc.) without CDM layer
- Statements deferring to industry solutions or vendor roadmaps
- Compliance disclosures that don't mention CDM or standardized data models

---

### Failure Mode 4: Asian Subsidiary Confusion
**Risk**: Conflating HSBC Asia operations with London headquarters strategy.

**Why It Could Happen**:
- HSBC has major operations in Hong Kong, Singapore
- MAS (Singapore) has been proactive on RegTech/DRR
- Search results may surface regional initiatives disconnected from global CDM strategy

**Mitigation Strategy**:
- Track whether evidence pertains to HSBC Holdings (global) vs regional entities
- Note that HKMA/MAS requirements differ from UK/EU EMIR Refit
- Check if Asian initiatives use different technology stack or vendors
- Clarify whether Delta Capita contract is global or UK/EU-specific

**Disconfirming Evidence to Seek**:
- Evidence of different CDM approaches in different regions
- Regional vendors (e.g., Asian RegTech firms) separate from Delta Capita
- Statements indicating fragmented technology strategy across jurisdictions

---

### Failure Mode 5: FINOS/ISDA Membership Misinterpretation
**Risk**: Treating passive membership as evidence of active contribution.

**Why It Could Happen**:
- ISDA member lists include most major banks
- FINOS working group rosters may list banks with minimal engagement
- Membership announced publicly while actual contribution level is opaque

**Mitigation Strategy**:
- Search for HSBC-authored commits to finos/common-domain-model or isda/cdm repositories
- Look for named HSBC individuals in CDM working group leadership roles
- Distinguish between "member" (OBSERVER) and "contributor" (PRAGMATIST/ARCHITECT)
- Check GitHub contribution graphs for HSBC email domains

**Disconfirming Evidence to Seek**:
- Membership lists without evidence of technical contribution
- Zero code commits from HSBC employees
- Working group minutes showing HSBC as "absent" or "non-participating"

---

### Failure Mode 6: Vendor Lock-in Mischaracterization
**Risk**: Treating strategic vendor partnership as evidence of internal capability.

**Why It Could Happen**:
- Delta Capita may position engagement as "co-development"
- HSBC may use collaborative language in press materials
- Outsourcing relationships increasingly branded as "partnerships"

**Mitigation Strategy**:
- Search for Delta Capita's specific service model (build vs build+operate vs managed service)
- Look for HSBC job postings indicating skills transfer or internal capability development
- Check if Delta Capita contract is fixed-term (project-based) or ongoing (operational dependency)
- Distinguish between "vendor partner" (collaborative) and "vendor operator" (dependency)

**Disconfirming Evidence to Seek**:
- Delta Capita described as "managed service provider" or "outsourcing partner"
- Long-term operational contracts suggesting ongoing dependency
- Absence of HSBC-led CDM initiatives independent of Delta Capita

---

## Search Strategy

### Tier 1 Priority Searches
1. **FINOS GitHub**: Check for HSBC commits to common-domain-model
2. **ISDA Publications**: Search for HSBC in CDM case studies, working group outputs
3. **FCA Regulatory Filings**: Search for HSBC EMIR Refit compliance disclosures
4. **HSBC Investor Relations**: Annual reports, technology briefings for CDM mentions
5. **HKMA/MAS**: Check for HSBC participation in Asian DRR initiatives

### Tier 2 Priority Searches
1. **Risk.net**: "HSBC CDM", "HSBC ISDA Common Domain Model", "HSBC derivatives reporting"
2. **Waters Technology**: "HSBC regulatory reporting", "HSBC Delta Capita", "HSBC DRR"
3. **Delta Capita**: Search vendor site for HSBC case studies, press releases, service descriptions
4. **Conference Proceedings**: ISDA AGM, Sibos, A-Team summits for HSBC speakers
5. **Trade Press**: Search for HSBC technology leadership interviews on regulatory reporting

### Tier 3 Conditional Searches
1. **LinkedIn**: HSBC employees with "CDM", "ISDA", "Common Domain Model" in profiles
2. **Job Boards**: HSBC postings for CDM developers, ISDA modelers, regulatory reporting technologists
3. **GitHub Individual Profiles**: Search for HSBC employees contributing to CDM repos

### Negative Fact Checks
Before executing searches, verify against `knowledge_base/negative_facts.md`:
- Any prior failed searches for HSBC
- Any documented dead ends or false leads
- Any contradictory evidence already catalogued

---

## Classification Decision Tree

### Path to ARCHITECT (Native)
**Required Evidence**:
- Tier 1/2 evidence of production CDM usage in live derivatives reporting
- Evidence of internal CDM development capability (job postings, code contributions, or technical publications)
- Delta Capita contract scoped as integration/connectivity, NOT full operations

**Confidence Threshold**: >70% (requires current Tier 1 or multiple corroborating Tier 2 sources)

### Path to ARCHITECT (Active)
**Required Evidence**:
- Tier 1/2 evidence of CDM pilot or proof-of-concept
- Evidence of internal technical team (even if vendor-assisted)
- Clear intent to move to production

**Confidence Threshold**: >60%

### Path to PRAGMATIST (Vendor-Dependent)
**Required Evidence**:
- Delta Capita contract is managed service or build+operate model
- Absence of evidence for internal CDM capability
- No HSBC technical contributions to CDM ecosystem

**Confidence Threshold**: >60%

### Path to OBSERVER
**Required Evidence**:
- Only membership or pilot participation evidence
- No production usage or active development
- 2018 pilot did not transition to production

**Confidence Threshold**: >60%

### Path to UNKNOWN
**Conditions**:
- Delta Capita contract exists but scope is entirely unclear
- No other evidence found across all tiers
- Cannot determine vendor dependency vs internal capability

**Confidence Threshold**: N/A (insufficient evidence)

---

## Red Flags for Bias

### Confirmation Bias Risks
- [ ] Over-weighting vendor relationship as evidence of sophistication
- [ ] Assuming derivatives volume necessitates CDM adoption
- [ ] Interpreting silence as stealth capability rather than non-adoption

### Anchoring Risks
- [ ] Prior 40% probability influencing evidence interpretation
- [ ] Delta Capita contract creating halo effect
- [ ] 2018 pilot participation creating legacy assumption

### Availability Bias Risks
- [ ] Recent (January 2025) Delta Capita news dominating assessment
- [ ] Vivid pilot stories overriding lack of production evidence
- [ ] Prominent HSBC brand suggesting advanced capability

---

## Success Criteria

This pre-mortem will be considered successful if:

1. **Evidence Quality**: ≥70% of evidence is Tier 1 or Tier 2
2. **Recency**: ≥50% of evidence is Current (<12 months old)
3. **Corroboration**: Key claims supported by ≥2 independent sources
4. **Vendor Clarity**: Delta Capita relationship scope definitively characterized
5. **Internal Capability**: Clear determination of whether HSBC has internal CDM team
6. **Pilot Legacy**: Clear determination of 2018 pilot outcome
7. **No Single Source Dependency**: No critical claim relies on single source
8. **Contradiction Resolution**: Any conflicting evidence explicitly resolved

---

## Expected Challenges

### Challenge 1: Vendor Contract Opacity
**Expectation**: Delta Capita contract details likely proprietary, requiring inference from indirect signals.

**Contingency**:
- Search for Delta Capita's standard service models
- Look for analogous vendor relationships at peer banks
- Check job postings for clues about internal vs vendor-operated model

### Challenge 2: Post-Pilot Information Vacuum
**Expectation**: FCA/BoE may not have published detailed post-pilot outcomes.

**Contingency**:
- Search HSBC annual reports 2019-2025 for DRR mentions
- Look for conference presentations by HSBC technology leaders
- Check trade press for post-mortem coverage of UK DRR pilot

### Challenge 3: Asian Regulator Complexity
**Expectation**: HKMA/MAS initiatives may be distinct from UK/EU CDM adoption, creating confusion.

**Contingency**:
- Separate evidence by jurisdiction
- Note when evidence is region-specific vs global
- Assess whether Asian operations would drive separate CDM implementation

---

## Null Hypothesis

**H0**: HSBC is **PRAGMATIST (Vendor-Dependent)** — using Delta Capita for CDM connectivity without internal development capability.

**Rationale**:
- Default classification per CLAUDE.md is PRAGMATIST
- Vendor relationship is confirmed; internal capability is not
- 2018 pilot participation alone insufficient (Historical evidence, low weight)

**What evidence would falsify H0**:
- Tier 1/2 evidence of HSBC-led CDM development
- Code contributions to FINOS/ISDA repositories
- Job postings for internal CDM team
- Conference presentations by HSBC technologists on CDM implementation
- Annual report disclosures of internal CDM capability

---

## Research Execution Checklist

- [ ] Check `knowledge_base/negative_facts.md` for HSBC-specific dead ends
- [ ] Review `config/vendor-matrix.json` for Delta Capita relationship details
- [ ] Execute all Tier 1 searches before Tier 2
- [ ] Execute all Tier 2 searches before Tier 3
- [ ] Document null results in separate section
- [ ] Verify all URLs before adding to evidence.json
- [ ] Apply temporal thresholds rigorously
- [ ] Flag any contradictions for resolution
- [ ] Require corroboration for high-confidence claims
- [ ] Update Bayesian priors after each tier
- [ ] Execute adversarial challenge before final classification

---

_Pre-Mortem Complete. Proceeding to Tier 1 Research._
