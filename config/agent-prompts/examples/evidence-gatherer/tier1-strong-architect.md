# Example: Tier 1 Strong Architect Evidence

## Context

Tier 1 evidence gathering for Goldman Sachs. This example shows documentation of strong ARCHITECT evidence from official sources.

## Bank Configuration

- **Bank**: Goldman Sachs
- **Headquarters**: New York, USA
- **Domain**: goldmansachs.com
- **Regulator**: SEC, CFTC

---

## Evidence Found

### Evidence Block 1 (Strong Architect)

```markdown
[GS-001] TIER 1 -- SUPPORTS ARCHITECT

Source: Goldman Sachs Engineering Blog
URL: https://www.goldmansachs.com/developer/blog/cdm-implementation
Date: 2024-09-15

Finding: "Goldman Sachs has deployed CDM-based trade representation across our derivatives processing infrastructure. The Common Domain Model now serves as our canonical data format for regulatory reporting under CFTC Rewrite requirements."

Quality Assessment:
- Authority: HIGH (official bank domain)
- Recency: current (3 months old)
- Specificity: specific (names CDM, CFTC, production deployment)
- Corroborated: No - pending

Confidence: HIGH
Reasoning: Official bank technology blog with specific production claims.

Caveats: Engineering blog may overstate progress; verify with regulatory filings.

Product Scope: [IRS, CDS, FX_Options]
Jurisdiction Scope: [US]
Coverage Specificity: explicit
---
```

### Evidence Block 2 (Corroborating)

```markdown
[GS-002] TIER 1 -- SUPPORTS ARCHITECT

Source: FINOS CDM GitHub Contributors
URL: https://github.com/finos/common-domain-model/graphs/contributors
Date: 2024-12-01

Finding: Multiple Goldman Sachs employees listed as CDM repository contributors with commits in 2024. Named contributors: [J. Smith], [A. Kumar], [M. Chen].

Quality Assessment:
- Authority: HIGH (FINOS official repository)
- Recency: current (ongoing contributions)
- Specificity: specific (named individuals, verified commits)
- Corroborated: Yes - by GS-001

Confidence: HIGH
Reasoning: GitHub contribution history is verifiable and ongoing.

Caveats: Contributions may be exploratory rather than production-driven.

Product Scope: [unknown] - repository contributions don't specify product
Jurisdiction Scope: [unknown]
Coverage Specificity: unknown
---
```

### Evidence Block 3 (ISDA Confirmation)

```markdown
[GS-003] TIER 1 -- SUPPORTS ARCHITECT

Source: ISDA Official Announcement
URL: https://www.isda.org/2024/10/01/cdm-production-update
Date: 2024-10-01

Finding: "ISDA announces that Goldman Sachs, along with five other major dealers, has achieved CDM production status for regulatory trade reporting."

Quality Assessment:
- Authority: HIGH (ISDA official)
- Recency: current (2 months old)
- Specificity: specific (names bank, confirms production)
- Corroborated: Yes - by GS-001, GS-002

Confidence: HIGH
Reasoning: ISDA announcement is definitive evidence of production status.

Caveats: None identified.

Product Scope: [IRS, CDS] - mentioned in announcement
Jurisdiction Scope: [US, EU] - regulatory reporting mentioned
Coverage Specificity: explicit
---
```

---

## Evidence JSON Output

```json
{
  "evidence_items": [
    {
      "id": "GS-001",
      "claim": "Goldman Sachs has deployed CDM for derivatives processing and CFTC regulatory reporting",
      "source_url": "https://www.goldmansachs.com/developer/blog/cdm-implementation",
      "tier": 1,
      "claim_type": "production_usage",
      "date": "2024-09-15",
      "direction": "SUPPORTS_ARCHITECT",
      "quality_assessment": {
        "authority": "HIGH",
        "recency": "current",
        "specificity": "specific"
      },
      "excerpt": "Goldman Sachs has deployed CDM-based trade representation across our derivatives processing infrastructure.",
      "caveats": "Engineering blog may overstate progress",
      "lr_mapping": {
        "evidence_type": "official_production_announcement",
        "likelihood_ratio": 200.0
      },
      "product_scope": ["IRS", "CDS", "FX_Options"],
      "jurisdiction_scope": ["US"],
      "coverage_specificity": "explicit",
      "corroborated_by": ["GS-002", "GS-003"]
    },
    {
      "id": "GS-002",
      "claim": "Multiple Goldman Sachs employees are active CDM repository contributors",
      "source_url": "https://github.com/finos/common-domain-model/graphs/contributors",
      "tier": 1,
      "claim_type": "open_source_contribution",
      "date": "2024-12-01",
      "direction": "SUPPORTS_ARCHITECT",
      "quality_assessment": {
        "authority": "HIGH",
        "recency": "current",
        "specificity": "specific"
      },
      "excerpt": "Multiple Goldman Sachs employees listed as CDM repository contributors with commits in 2024",
      "caveats": "Contributions may be exploratory",
      "lr_mapping": {
        "evidence_type": "named_finos_contributor_active",
        "likelihood_ratio": 12.0
      },
      "product_scope": [],
      "jurisdiction_scope": [],
      "coverage_specificity": "unknown",
      "corroborated_by": ["GS-001"]
    },
    {
      "id": "GS-003",
      "claim": "ISDA confirms Goldman Sachs achieved CDM production status",
      "source_url": "https://www.isda.org/2024/10/01/cdm-production-update",
      "tier": 1,
      "claim_type": "production_usage",
      "date": "2024-10-01",
      "direction": "SUPPORTS_ARCHITECT",
      "quality_assessment": {
        "authority": "HIGH",
        "recency": "current",
        "specificity": "specific"
      },
      "excerpt": "ISDA announces that Goldman Sachs, along with five other major dealers, has achieved CDM production status",
      "caveats": null,
      "lr_mapping": {
        "evidence_type": "isda_official_confirmation",
        "likelihood_ratio": 95.0
      },
      "product_scope": ["IRS", "CDS"],
      "jurisdiction_scope": ["US", "EU"],
      "coverage_specificity": "explicit",
      "corroborated_by": ["GS-001", "GS-002"]
    }
  ]
}
```

---

## Tier 1 Summary

| Metric | Value |
|--------|-------|
| Evidence items found | 3 |
| Direction | All SUPPORTS_ARCHITECT |
| Combined LR | 200 x 12 x 95 = 228,000 (dampened) |
| Highest claim type | production_usage |
| Corroboration | Triangulated (3 sources) |
| Classification Signal | Strong ARCHITECT |

**Note**: This Tier 1 evidence is unusually strong. May qualify for skip-to-adversarial after Gate 1.
