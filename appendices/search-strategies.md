# Search Strategies Appendix

## Effective Search Query Patterns

### Official Source Queries

```
# Annual reports and investor materials
"[Bank Name]" "annual report" [year] "regulatory reporting" OR "derivatives technology"
"[Bank Name]" investor presentation [year] derivatives technology
"[Bank Name]" investor day technology transformation

# ISDA official sources
site:isda.org "[Bank Name]"
site:isda.org "[Bank Name]" CDM OR DRR
"[Bank Name]" ISDA announcement OR "press release"

# FINOS official sources
site:finos.org "[Bank Name]"
site:github.com/finos "[Bank Name]" contributor
FINOS "[Bank Name]" member OR contributor

# Bank corporate sites (use sparingly - often low yield)
site:[bankdomain.com] CDM OR "regulatory reporting" derivatives
site:[bankdomain.com] technology transformation

# Regulatory filings
"[Bank Name]" 10-K OR 20-F "regulatory reporting" technology
"[Bank Name]" SEC filing derivatives technology
```

### Industry Coverage Queries

```
# Specialist trade press
"[Bank Name]" Risk.net derivatives technology [year]
"[Bank Name]" "Waters Technology" [year]
"[Bank Name]" "Financial News" derivatives
"[Bank Name]" CDM OR "Common Domain Model" [year]

# Conference and event participation
"[Bank Name]" ISDA AGM speaker [year]
"[Bank Name]" "CDM Showcase" [year]
"[Bank Name]" FINOS "Open Source in Finance Forum"
"[Bank Name]" Sibos derivatives

# Regulatory compliance
"[Bank Name]" "EMIR Refit" implementation
"[Bank Name]" [regulator] derivatives reporting
"[Bank Name]" regulatory compliance technology
```

### Indirect Signal Queries

```
# Job postings
"[Bank Name]" job OR careers CDM OR DRR
"[Bank Name]" "regulatory reporting" engineer OR developer
"[Bank Name]" derivatives technology hiring

# LinkedIn (often blocked, use as backup)
site:linkedin.com "[Bank Name]" "Common Domain Model"
site:linkedin.com "[Bank Name]" CDM derivatives

# Vendor relationships
"[Bank Name]" [vendor name] derivatives
"[Bank Name]" RegTech derivatives reporting
"[Bank Name]" derivatives technology partner

# Academic/research
"[Bank Name]" CDM research OR paper OR whitepaper
```

### Adversarial Queries (Disconfirming)

```
# Looking for non-engagement
"[Bank Name]" CDM "no plans" OR "not pursuing" OR declined
"[Bank Name]" derivatives reporting vendor OR outsource OR "third party"
"[Bank Name]" legacy OR traditional derivatives reporting

# Looking for engagement (if classified Pragmatist)
"[Bank Name]" CDM pilot OR "proof of concept" OR prototype
"[Bank Name]" CDM initiative OR program OR investment
"[Bank Name]" "Common Domain Model" announcement
```

---

## Search Query Iteration Protocol

### When Initial Query Returns Nothing

**Attempt 1:** Execute exact query as designed
- If relevant results → Document and proceed
- If no relevant results → Execute Attempt 2

**Attempt 2:** Query Reformulation
- Remove least essential terms (usually the most specific)
- Add synonyms or alternative phrasings

Examples:
```
Original: "Deutsche Bank" "Common Domain Model" production
Reformulation 1: "Deutsche Bank" CDM derivatives
Reformulation 2: "Deutsche Bank" derivatives data standard
Reformulation 3: Deutsche Bank regulatory reporting technology
```

**Attempt 3:** Lateral Search
- Search for adjacent/related concepts that often co-occur with CDM engagement:

```
# Related standards
"[Bank Name]" ISO 20022 derivatives
"[Bank Name]" FpML adoption
"[Bank Name]" ISDA taxonomy

# Related technology
"[Bank Name]" DLT derivatives post-trade
"[Bank Name]" smart contracts derivatives
"[Bank Name]" derivatives automation

# Related initiatives
"[Bank Name]" post-trade transformation
"[Bank Name]" derivatives middle office modernization
"[Bank Name]" T+1 settlement derivatives
```

**Attempt 4:** Direct Source Investigation
If general search fails, go directly to likely sources:

```
1. Check ISDA event agendas manually:
   - Go to isda.org → Events → Past events
   - Search speaker lists for bank name

2. Check FINOS GitHub directly:
   - Go to github.com/finos
   - Search repositories for bank name in contributor logs

3. Search specialist publications directly:
   - Go to risk.net → Search → "[Bank name]" CDM
   - Go to waterstechnology.com → Search

4. Check regulatory databases:
   - CFTC enforcement actions → [Bank name]
   - FCA Final Notices → [Bank name]
```

### Query Formatting Rules

**DO:**
- Use quotes around bank names to ensure exact match: `"Deutsche Bank"`
- Use OR for synonyms: `CDM OR "Common Domain Model"`
- Include year for recency: `2024 2025`
- Use site: operator only for official sources: `site:isda.org`

**DON'T:**
- Use overly complex boolean logic (degrades search quality)
- Use the `-` exclusion operator (often causes issues)
- Add unnecessary terms that narrow results too much
- Use quotes around single common words

### Regional/Language Considerations

For non-English markets, consider native language queries:

**German (Deutsche Bank, Commerzbank):**
```
"Deutsche Bank" Derivate Meldewesen Technologie
"Deutsche Bank" regulatorische Berichterstattung
```

**French (SocGen, BNP, Crédit Agricole):**
```
"Société Générale" déclaration réglementaire dérivés
"Société Générale" technologie post-marché
```

**Japanese (Nomura, MUFG, etc.):**
- Use English queries first (Japanese financial press often uses English terms for technical topics)
- Consider romanized Japanese terms if needed

---

## Query Yield Expectations

### High-Yield Query Types
- ISDA site searches for confirmed contributors
- Risk.net/Waters Technology for thought leadership
- Regulatory enforcement searches
- Named individual + topic searches

### Medium-Yield Query Types
- Annual report technology sections
- Conference speaker searches
- Job posting searches (high noise)

### Low-Yield Query Types (Use for Completeness)
- Bank corporate website searches (usually client-facing only)
- LinkedIn searches (often blocked)
- Patent/academic searches

---

## Documenting Search Results

### For Each Search, Record:

```markdown
SEARCH ID: [BANK-S##]
QUERY: [Exact query used]
ATTEMPT: [1/2/3/4]
TIMESTAMP: [When executed]

RESULTS:
- Total results: [N]
- Results reviewed: [N]
- Relevant results: [N]

FINDINGS:
- [Finding 1]: [Brief description] → [Evidence block ID if documented]
- [Finding 2]: [Brief description] → [Evidence block ID if documented]

QUALITY:
- Top results relevant? [Y/N]
- Results recent? [Y/N]
- Source authority? [High/Med/Low]

NOTES:
[Any observations about search quality or unexpected results]
```

### For Null Results, Record:

```markdown
SEARCH ID: [BANK-S##]
QUERY: [Exact query used]
ATTEMPT: [1/2/3/4 - specify which attempts tried]
TIMESTAMP: [When executed]

RESULT: NULL

REASON:
[ ] No results returned
[ ] Results returned but irrelevant
[ ] Results exist but paywalled
[ ] Only outdated results found

INTERPRETATION:
- Is absence informative? [Y/N]
- Does this support/undermine hypothesis? [Describe]

NEXT ACTION:
[ ] Query reformulated → [New query]
[ ] Lateral search attempted → [New query]
[ ] Direct source checked → [Source]
[ ] Accepted as informative absence
```

---

## Search Quality Checklist

Before concluding evidence gathering, verify:

- [ ] All Tier 1 queries executed (not just convenient ones)
- [ ] At least 2 reformulation attempts for null results
- [ ] Direct source check for high-priority banks
- [ ] Adversarial queries executed regardless of direction
- [ ] Regional/language variants considered if relevant
- [ ] All searches documented (including nulls)
- [ ] Pattern of nulls analyzed for informative absence
