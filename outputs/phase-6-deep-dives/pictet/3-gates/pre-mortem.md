# Pre-Mortem Analysis - Pictet Group

**Bank:** Pictet Group
**Phase:** 6 (Deep Dive)
**Date:** 2025-12-21

---

## Purpose

Before commencing evidence collection, this pre-mortem analysis identifies potential failure modes, search pitfalls, and classification errors. This prospective analysis helps prevent confirmation bias and ensures systematic evidence gathering.

---

## Hypothetical Failure Scenario

**Imagined Outcome (6 months from now):**

> "Pictet Group research was published with 90% confidence ARCHITECT classification, but subsequent investigation revealed the implementation was limited to a single European subsidiary for EMIR Refit compliance, using vendor-managed tooling. The bank should have been classified as PRAGMATIST (Vendor-Dependent) with 65% confidence."

**Question:** What went wrong? How did we arrive at this incorrect classification?

---

## Identified Failure Modes

### Failure Mode 1: Swiss Discretion Bias (Overcorrection)

**The Mistake:**
Researchers assumed Swiss banking discretion explained absence of evidence, when absence actually reflected limited implementation scope.

**How It Could Happen:**
1. ISDA announces Pictet as DRR consortium member
2. Researchers find no GitHub activity, no job postings, no technical blog posts
3. Researchers attribute absence to "Swiss discretion culture"
4. Actually, absence reflects vendor-managed implementation with limited internal technical team

**Prevention Strategy:**
- ✅ Distinguish between "expected discretion" (no marketing) and "suspicious absence" (no technical artifacts)
- ✅ Compare to other Swiss banks (UBS, Credit Suisse) - do they have GitHub activity?
- ✅ Seek specific implementation details (desk coverage, transaction volumes, technology stack)
- ✅ Verify "production usage" with scope indicators (region, business unit, trade types)

**Red Flags to Watch:**
- ⚠️ ALL evidence from governance/participation channels, ZERO from technical channels
- ⚠️ Vague "production usage" language without specifics
- ⚠️ No technical job postings or LinkedIn activity even from non-Swiss banks using same vendors

---

### Failure Mode 2: ISDA Marketing Echo Chamber

**The Mistake:**
ISDA has incentive to overstate member adoption. All evidence from ISDA sources creates circular validation.

**How It Could Happen:**
1. ISDA announces Pictet "in production with DRR"
2. Pictet presents at ISDA conference (supporting ISDA initiative)
3. ISDA working group lists Pictet as member
4. All three sources cite each other, creating appearance of corroboration
5. Actually, Pictet may be "production-ready" (pilot stage) rather than "in production" (live trading)

**Prevention Strategy:**
- ✅ Require at least ONE non-ISDA source for high-confidence classification
- ✅ Seek regulatory filings (FCA, BaFin, FINMA) that would mention material system changes
- ✅ Look for vendor press releases (vendors announce major implementations)
- ✅ Check trade press (Risk.net, Waters Technology) for independent coverage
- ✅ Distinguish "consortium membership" from "production deployment"

**Red Flags to Watch:**
- ⚠️ 100% of evidence from ISDA ecosystem (isda.org, ISDA events, ISDA working groups)
- ⚠️ No vendor claiming Pictet as client (suggests internal build OR no deployment)
- ⚠️ No regulatory mentions (unusual for major system change)
- ⚠️ Vague language: "developing," "implementing," "working toward production"

---

### Failure Mode 3: Temporal Optimism (Stale Evidence Misread)

**The Mistake:**
Evidence from 2023-2024 reflects active project, but project was discontinued in late 2024. Classification based on historical state, not current state.

**How It Could Happen:**
1. Nov 2023: ISDA announces Pictet production deployment (accurate at time)
2. Mar-Jun 2024: Continued evidence of ISDA participation
3. Jul 2024-present: Project deprioritized due to cost, technical challenges, or strategic shift
4. Dec 2025: Researchers find 2023-2024 evidence, classify as ARCHITECT
5. Actually, CDM implementation abandoned 6 months ago

**Prevention Strategy:**
- ✅ Require at least ONE piece of Current evidence (<12 months old) for 85%+ confidence
- ✅ Search for 2025 signals: job postings, LinkedIn posts, recent conference presentations
- ✅ Check for negative signals: layoffs, project cancellations, vendor partnerships ending
- ✅ Contact bank directly for current status (if possible within research constraints)
- ✅ Apply aggressive temporal weight decay per CLAUDE.md Section 6

**Red Flags to Watch:**
- ⚠️ All evidence >12 months old (Current category empty)
- ⚠️ Evidence clusters in 2023-2024 with sudden silence in 2025
- ⚠️ Key personnel departed (LinkedIn shows role changes)
- ⚠️ No recent working group participation or conference presentations

---

### Failure Mode 4: Geography Overgeneralization

**The Mistake:**
European subsidiary has CDM for EMIR Refit compliance, but researchers generalize to bank-wide implementation.

**How It Could Happen:**
1. EMIR Refit mandates CDM-based reporting for EU derivatives
2. Pictet's European subsidiary deploys vendor CDM solution for compliance
3. ISDA lists Pictet (corporate level) as DRR consortium member
4. Researchers assume bank-wide implementation
5. Actually, Asia-Pacific and Swiss operations use legacy systems (no CDM)

**Prevention Strategy:**
- ✅ Search for regulatory drivers (EMIR Refit in Europe, CFTC Rewrite in US)
- ✅ Check bank's geographic revenue distribution (where is derivatives business concentrated?)
- ✅ Look for region-specific evidence (FCA filings vs. FINMA filings vs. MAS filings)
- ✅ Verify "production usage" includes scope indicators (Europe only vs. global)
- ✅ Compare to peer banks' implementation scope (are others Europe-only?)

**Red Flags to Watch:**
- ⚠️ Only European regulatory references (EMIR Refit, FCA)
- ⚠️ No Asia-Pacific or Americas evidence
- ⚠️ Bank's revenue heavily concentrated outside Europe
- ⚠️ Implementation timeline aligns with EMIR Refit deadline (suggests compliance-driven, not strategic)

---

### Failure Mode 5: Vendor Proxy Misattribution

**The Mistake:**
Pictet is using vendor CDM implementation (Regnosys, Bloomberg, etc.) but researchers classify as "Native" due to production usage confirmation.

**How It Could Happen:**
1. Pictet purchases Regnosys CDM solution for EMIR Refit compliance
2. Regnosys deploys solution in Pictet's production environment
3. ISDA announces Pictet "in production with CDM" (technically true)
4. Researchers classify as ARCHITECT (Native) due to production usage
5. Actually, Pictet is PRAGMATIST (Vendor-Dependent) with zero internal CDM development

**Prevention Strategy:**
- ✅ Search for vendor press releases claiming Pictet as client
- ✅ Check GitHub for Pictet contributor emails (native build would have code commits)
- ✅ Look for technical blog posts describing architecture (native teams write about their work)
- ✅ Verify job postings mention CDM development vs. CDM integration/operations
- ✅ Distinguish "deployed" (could be vendor) from "developed" (native capability)

**Red Flags to Watch:**
- ⚠️ Zero GitHub/FINOS activity (native teams contribute to open source)
- ⚠️ Zero technical artifacts (blog posts, conference slide decks with architecture)
- ⚠️ Vague "deployed" language without "developed" or "built"
- ⚠️ Operational job postings ("CDM Operations Analyst") vs. development roles ("CDM Developer")

---

### Failure Mode 6: Private Bank Scale Misunderstanding

**The Mistake:**
Assuming Pictet's "production usage" is comparable to JPMorgan or BNP Paribas scale, when actually covers small derivatives desk.

**How It Could Happen:**
1. ISDA groups Pictet with BNP Paribas and JPMorgan as "early adopters"
2. Researchers assume comparable scale and scope
3. Actually, Pictet's derivatives operations 10x smaller than universal banks
4. CDM deployment covers smaller absolute volume despite being "production"
5. Maturity score should be lower due to limited scope

**Prevention Strategy:**
- ✅ Research bank's derivatives business size (balance sheet, trading volumes, desk count)
- ✅ Compare private bank (Pictet) to universal banks (BNP Paribas) - expect different scales
- ✅ Look for transaction volume or desk coverage metrics in evidence
- ✅ Adjust maturity assessment for business unit size
- ✅ "Production for private bank" ≠ "production for universal bank"

**Red Flags to Watch:**
- ⚠️ No scale metrics in any evidence (volume, desks, regions)
- ⚠️ Direct comparison to universal banks without acknowledging size difference
- ⚠️ Assumption that "production" means same thing across bank types

---

## Search Strategy Pitfalls

### Pitfall 1: Language Barrier (French/German)
**Risk:** Swiss banks may publish in French or German, missing evidence in English-only searches.

**Mitigation:**
- Search "Pictet CDM" in French: "Pictet modèle de domaine commun ISDA"
- Search in German: "Pictet gemeinsames Domänenmodell ISDA"
- Check Swiss financial press (Finanz und Wirtschaft, Le Temps)

### Pitfall 2: Spelling Variations
**Risk:** "Pictet" could be misspelled or have variations.

**Mitigation:**
- Search "Pictet Group" vs. "Pictet & Cie" vs. "Banque Pictet"
- Include "Pictet Group" AND "CDM" AND "ISDA"

### Pitfall 3: Privacy/Firewall
**Risk:** Pictet content behind client portal or member-only access.

**Mitigation:**
- Accept that some evidence will be inaccessible (unavoidable)
- Focus on public sources (ISDA, trade press, regulatory filings)
- Document inaccessible sources as null results

---

## Evidence Quality Checklist

Before accepting any evidence item, verify:

- [ ] **Source Authority:** Is source tier appropriate for claim type?
- [ ] **Claim Specificity:** Does evidence provide specific details or vague generalities?
- [ ] **Temporal Freshness:** Is evidence Current (<12 months) or Dated (>18 months)?
- [ ] **Production Verification:** Does "production" mean live trading or production-grade pilot?
- [ ] **Geographic Scope:** Does evidence specify region (Europe, Asia, global)?
- [ ] **Vendor Independence:** Does evidence distinguish native build from vendor solution?
- [ ] **Source Diversity:** Is this independent corroboration or ISDA echo chamber?

---

## Success Criteria

**Research will be considered successful if:**

1. ✅ At least ONE non-ISDA source confirms production usage (trade press, regulatory filing, vendor)
2. ✅ At least ONE piece of Current evidence (<12 months old) confirms continued implementation
3. ✅ Clear distinction between native development and vendor dependency
4. ✅ Geographic scope clearly identified (Europe only vs. global)
5. ✅ No contradictory evidence found across all tiers
6. ✅ Confidence calibration accounts for Swiss discretion bias and temporal staleness

**Red Flags That Would Trigger Reclassification:**

1. ⚠️ 100% ISDA sources with zero independent corroboration
2. ⚠️ All evidence >18 months old (Dated category) with no Current signals
3. ⚠️ Vendor press release claiming Pictet as client (vendor-dependent)
4. ⚠️ Contradictory evidence (e.g., "Pictet abandons CDM project")
5. ⚠️ Zero technical artifacts suggesting operational role only

---

## Classification Decision Tree

```
IF (Tier 1 production_usage confirmed)
  AND (Independent non-ISDA source corroborates)
  AND (At least 1 Current evidence <12 months)
  AND (No vendor press releases claiming Pictet)
  THEN: ARCHITECT (Native) at 90-95% confidence

ELSE IF (Tier 1 production_usage confirmed)
  AND (No independent corroboration)
  OR (All evidence >12 months old)
  THEN: ARCHITECT (Native) at 75-85% confidence (with caveats)

ELSE IF (Tier 1 production_usage confirmed)
  AND (Vendor press release found)
  THEN: PRAGMATIST (Vendor-Dependent) at 70-80% confidence

ELSE IF (Only Tier 2 signals OR only participation evidence)
  THEN: OBSERVER at 60-70% confidence

ELSE IF (No evidence found across all tiers)
  THEN: UNKNOWN
```

---

## Conclusion

**Pre-Mortem Status:** COMPLETE

**Key Risks Identified:**
1. Swiss discretion bias (overcorrecting for expected absence of evidence)
2. ISDA echo chamber (all sources from interested party)
3. Temporal optimism (stale evidence from discontinued project)
4. Geography overgeneralization (Europe-only misread as bank-wide)
5. Vendor proxy misattribution (vendor implementation classified as native)
6. Scale misunderstanding (private bank scope vs. universal bank scope)

**Mitigation Plan:**
- Require independent (non-ISDA) corroboration for 85%+ confidence
- Require Current (<12 months) evidence for 90%+ confidence
- Distinguish vendor deployment from native development
- Verify geographic and business unit scope
- Apply Swiss discretion lens carefully (expected vs. suspicious absence)

**Proceed to Tier 1 evidence collection with failure modes in mind.**
