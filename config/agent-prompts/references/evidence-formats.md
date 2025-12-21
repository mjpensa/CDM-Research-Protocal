# Evidence Documentation Formats

Reference file for Evidence Gatherer Agent output formatting.
Version: 1.0-20251221

---

## Evidence Block Format (Markdown)

```markdown
[BANK-###] TIER [1/2/3] — [SUPPORTS/UNDERMINES/NEUTRAL] [ARCHITECT/PRAGMATIST]

Source: [Full source name]
URL: [https://...]
Date: [YYYY-MM-DD]

Finding: "[Exact quote or precise summary in quotes]"

Quality Assessment:
- Authority: [HIGH/MEDIUM/LOW]
- Recency: [current (<12mo) / recent (12-18mo) / dated (18-36mo) / historical (>36mo)]
- Specificity: [specific / moderate / vague]
- Corroborated: [Yes - by BANK-XXX / No - pending]

Confidence: [HIGH/MEDIUM/LOW]
Reasoning: [One sentence justification]

Caveats: [Limitations, alternative interpretations, uncertainty]

Product Scope: [IRS, CDS, FX_Options, Equity_Derivatives, Commodities] or [unknown]
Jurisdiction Scope: [EU, UK, US, Japan, Singapore, Hong_Kong] or [unknown]
Coverage Specificity: [explicit / inferred / unknown]
---
```

---

## Evidence Block Format (JSON)

For `evidence.json` - the PRIMARY output file:

```json
{
  "id": "BANK-001",
  "claim": "Description of what this evidence shows",
  "source_url": "https://example.com/source",
  "tier": 1,
  "claim_type": "production_usage",
  "date": "2024-06-15",
  "direction": "SUPPORTS_ARCHITECT",
  "quality_assessment": {
    "authority": "HIGH",
    "recency": "current",
    "specificity": "specific"
  },
  "excerpt": "Exact quote from source in quotes",
  "caveats": "Any limitations or alternative interpretations",
  "lr_mapping": {
    "evidence_type": "official_production_announcement",
    "likelihood_ratio": 200.0
  },
  "product_scope": ["IRS", "CDS"],
  "jurisdiction_scope": ["EU", "UK"],
  "coverage_specificity": "explicit",
  "corroborated_by": []
}
```

---

## Claim Types (Valid Enum Values)

| Claim Type | Definition | Required Tier |
|------------|------------|---------------|
| `production_usage` | Live usage in production environment | Tier 1 or 2 |
| `pilot_or_poc` | Experimental usage or proof of concept | Tier 1 or 2 |
| `membership_or_participation` | Working group member without technical artifacts | Tier 1 or 2 |
| `open_source_contribution` | Code commits to CDM/FINOS repositories | Tier 1 |
| `vendor_proxy_signal` | Implied usage via vendor relationship | Tier 2 |
| `hiring_signal` | Job postings indicating intent | Tier 3 only |

---

## Direction Values

| Direction | When to Use |
|-----------|-------------|
| `SUPPORTS_ARCHITECT` | Evidence suggests active building/contributing to CDM |
| `SUPPORTS_PRAGMATIST` | Evidence suggests waiting/vendor-only/no engagement |
| `NEUTRAL` | Evidence doesn't clearly favor either hypothesis |

---

## Quality Assessment Criteria

### Authority Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| HIGH | Official sources, regulators, standards bodies | Bank press release, ISDA announcement, SEC filing |
| MEDIUM | Established trade press, industry analysts | Risk.net article, Celent report |
| LOW | Unverified claims, vendor marketing, old sources | LinkedIn post, vendor press release |

### Recency Categories

| Category | Age | Weight | Notes |
|----------|-----|--------|-------|
| current | < 12 months | 1.0 | Full weight |
| recent | 12-18 months | 0.8 | Transitional |
| dated | 18-36 months | 0.5 | Reduced weight |
| historical | > 36 months | 0.3 | Context only, cannot drive classification |

### Specificity Levels

| Level | Criteria |
|-------|----------|
| specific | Names CDM explicitly, gives timeline/scope, names individuals |
| moderate | Mentions derivatives technology generically, could be CDM-related |
| vague | General statements about technology investment |

---

## Null Result Block Format (Markdown)

```markdown
NULL RESULT BLOCK

Search Category: [e.g., "Tier 1 Official Bank Announcements"]
Queries Executed:
1. "[Exact query 1]"
2. "[Exact query 2]"
3. "[Exact query 3]"

Results Reviewed: [Number]
Relevant Findings: 0

Null Classification:
[X] NO_RESULTS - Search returned no results
[ ] IRRELEVANT - Results exist but none relevant to CDM/DRR
[ ] PAYWALLED - Results exist but behind paywall
[ ] OUTDATED_ONLY - Only found results >3 years old

Null Explanation: [Why no results - be specific]

Informative Absence Assessment:
Would we EXPECT to find evidence in this category if bank were ARCHITECT?
[YES / NO / UNCLEAR]

If YES: This absence [SUPPORTS PRAGMATIST / WEAKLY SUPPORTS PRAGMATIST / NEUTRAL]
Because: [One sentence rationale]
---
```

---

## Null Result Format (JSON)

For `evidence.json` null_results array:

```json
{
  "category": "Tier 1 Official Bank Announcements",
  "queries": [
    "\"Bank Name\" CDM site:bank.com",
    "\"Bank Name\" \"Common Domain Model\" announcement"
  ],
  "results_reviewed": 20,
  "null_type": "NO_RESULTS",
  "informative_absence": true,
  "expected_if_architect": true,
  "implication": "SUPPORTS_PRAGMATIST",
  "rationale": "Would expect official announcement if in production"
}
```

---

## Product-Specific Evidence Documentation

When product-level evidence is found, add these fields:

```markdown
Product Scope: [IRS, CDS, FX_Options, Equity_Derivatives, Commodities]
Coverage Specificity: [explicit - product named / inferred - from context / unknown]
Regulatory Driver: [EMIR_Refit / UK_EMIR / CFTC_Rewrite / JSCC / MAS / HKMA]
```

---

## Jurisdiction-Specific Evidence Documentation

When jurisdiction-level evidence is found, add these fields:

```markdown
Jurisdiction Scope: [EU, UK, US, Japan, Singapore, Hong_Kong]
Coverage Specificity: [explicit / inferred / unknown]
Regulatory Driver: [EMIR_Refit, UK_EMIR, CFTC_Rewrite, JSCC, MAS, HKMA]
```

---

## Counterparty Evidence Documentation

```markdown
[BANK-###] TIER [2/3] — COUNTERPARTY SIGNAL

Source: [URL]
Date: [YYYY-MM-DD]

Counterparty Type: [CCP / G16_dealer / utility]
Counterparty Name: [e.g., JSCC, JPMorgan, Delta Capita]

Finding: "[Quote or summary]"

Relationship Details:
- Membership/Client Status: [clearing_member / client_clearing / utility_client / bilateral_counterparty]
- CDM Requirement from Counterparty: [mandatory / preferred / none / unknown]
- CDM Deadline (if any): [YYYY-MM-DD or N/A]
- Bank CDM Status with Counterparty: [connected / building / planned / not_started / unknown]

Network Pressure Assessment:
- Pressure Level: [HIGH / MEDIUM / LOW]

Confidence: [HIGH / MEDIUM / LOW]
```

---

## Vendor Relationship Documentation

```markdown
[BANK-###] TIER [2/3] — VENDOR RELATIONSHIP

Source: [URL]
Date: [YYYY-MM-DD]

Vendor Name: [e.g., Murex, Delta Capita, Accenture]
Vendor Type: [platform_vendor / cdm_specialist / systems_integrator / consulting / utility_provider]

Finding: "[Quote or summary]"

Relationship Scope:
- Capabilities: [cdm_core / cdm_translation / reporting / matching / regulatory_filing / ccp_connectivity]
- Products Covered: [IRS, CDS, etc. if specified]
- Jurisdictions Covered: [EU, UK, US, etc. if specified]

Relationship Stage: [production / implementation / pilot / evaluation / planned / unknown]
Dependency Level: [HIGH / MEDIUM / LOW]

Evidence Quality:
- Source Type: [vendor_announcement / bank_confirmation / trade_press / job_posting]
- Confirmation Status: [confirmed_by_bank / vendor_claim_only / inferred]

Confidence: [HIGH / MEDIUM / LOW]
```

---

## Knowledge Gap Documentation

```markdown
GAP-### [Category]

Category: [product_coverage / jurisdiction / vendor / driver / counterparty / strategic / technical]
Gap Type: [specific type from gap-taxonomy.json]

Description: [What specifically is unknown]

Business Impact: [HIGH / MEDIUM / LOW]
Impact Rationale: [Why this gap matters]

Public Research Exhausted: [YES / NO]
Searches Attempted:
1. "[query 1]" - [result]
2. "[query 2]" - [result]

Suggested Resolution:
- Source Type: [insider_interview / vendor_backdoor / conference_networking / analyst_report]
- Target Role: [e.g., "Head of Derivatives Technology"]
- Discovery Question: "[Specific question to ask]"

Resolution Value: [0-100]
Strategic Urgency: [0-100]
Priority Score: [Calculated]

Related Evidence: [BANK-### items]
```

---

## LR Mapping Quick Reference

| Evidence Type | Typical LR | Interpretation |
|---------------|------------|----------------|
| Official production announcement | 95-200 | Near-definitive Architect |
| Official pilot with timeline | 15-27 | Moderate Architect |
| Named ISDA contributor | 10-14 | Moderate Architect |
| Trade press reports pilot | 10-15 | Moderate Architect |
| Conference speaker CDM topic | 4-5 | Weak Architect |
| Named working group | 3-4 | Weak Architect |
| Job posting CDM | 2-3 | Weak Architect |
| Vendor claim (unconfirmed) | 1.5-2 | Very weak Architect |
| No evidence Tier 1 | 0.2-0.3 | Weak Pragmatist |
| No evidence Tier 1+2 | 0.1-0.15 | Moderate Pragmatist |
| Official vendor-only statement | 0.2-0.25 | Moderate Pragmatist |
| No evidence full protocol | 0.01-0.02 | Strong Pragmatist |

See `config/bayesian-lr-tables.json` for complete mappings.

---

## Evidence Numbering Convention

- Format: `BANK-###` (e.g., BANK-001, BANK-042)
- Start from 001, increment sequentially
- Maintain across all tiers (don't restart numbering per tier)
- Use consistent padding (3 digits)
