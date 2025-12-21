# CDM/DRR Research Protocol Execution Prompt v2.0

> **Schema Version**: 4.3 | **Banks**: 31 | **Phases**: 9
> **Last Updated**: 2025-12-21

---

Execute CDM/DRR research for all 31 banks following the protocol in CLAUDE.md.

For EACH bank in config/bank-manifest.json, process sequentially through all stages:

## Stage Sequence (Per Bank)

1. **Initialize** - Create `outputs/phase-{N}/{bank-id}/` directory and `status.json` with calculated prior from manifest
2. **Pre-mortem** - Identify potential failure modes in `3-gates/pre-mortem.md`
3. **Tier 1 Evidence** - Search official sources (isda.org, finos.org, bank websites, regulatory filings), write to `evidence.json`
4. **Bayesian Update 1** - Calculate posterior probability in `2-bayesian/post-tier1-update.md`
5. **Gate 1** - Assess evidence in `3-gates/gate-1.md` (always proceed to Tier 2)
6. **Tier 2 Evidence** - Search industry sources (Risk.net, Waters Technology, press), append to `evidence.json`
7. **Bayesian Update 2** - Update probability in `2-bayesian/post-tier2-update.md`
8. **Gate 2** - Assess evidence in `3-gates/gate-2.md` (always proceed to Tier 3)
9. **Tier 3 Evidence** - Search signal sources (job postings, LinkedIn, blogs), append to `evidence.json`
10. **Bayesian Update 3** - Final probability update in `2-bayesian/post-tier3-update.md`
11. **Gate 3** - Proceed to adversarial in `3-gates/gate-3.md`
12. **Contradiction Resolution** - If CONTRADICTIONS_DETECTED flag set, create `3-gates/contradiction-resolution.md`
13. **Adversarial Challenge** - Devil's advocate analysis in `4-adversarial/`
14. **Final Classification** - Assign ARCHITECT/PRAGMATIST with sub-classification and confidence
15. **Confidence Calibration** - Create `5-synthesis/confidence-calibration.md` FIRST (6-step process)
16. **Synthesis** - Create `5-synthesis/assessment.md` with all 19 sections
17. **Framework Integration** - Create `5-synthesis/framework-integration.md`

---

## CRITICAL RULES

### Ledger-First Principle
- `evidence.json` is the PRIMARY output. All evidence goes there FIRST.
- Markdown files in `1-evidence/` are RENDERED views (secondary outputs)
- Use `tools/render_evidence_md.py` to generate Markdown from JSON

### Evidence Tiers - Process ALL 3 for Every Bank
- Do NOT skip any evidence tiers
- Track all WebSearch queries in `evidence.json` → `search_tracking` section

### Claim Types (use EXACTLY)
```
production_usage
pilot_or_poc
membership_or_participation
open_source_contribution
vendor_proxy_signal
hiring_signal
```

### Confidence Caps by Tier
| Highest Tier Present | Maximum Confidence |
|---------------------|-------------------|
| Tier 1 evidence | 95% |
| Tier 2 only | 75% |
| Tier 3 only | 50% |
| Inference only | 35% |

### Classification Taxonomy
```
ARCHITECT: Native, Leader, Follower
PRAGMATIST: Vendor-Dependent, Integration-Constrained, Regulatory-Driven, Network-Accelerant
OBSERVER: Active-Watcher, Passive
UNKNOWN: Insufficient-Evidence, Conflicting-Evidence
```

---

## Schema v4.3 Sections (NEW in v2)

### search_tracking (Required)
Track WebSearch completion for batch validation:
```json
{
  "search_tracking": {
    "tier1_searches": {
      "expected": 8,
      "completed": 8,
      "failed": 0,
      "queries": [
        {
          "query": "Deutsche Bank CDM ISDA site:isda.org",
          "source_category": "isda",
          "status": "completed",
          "results_found": 3,
          "timestamp": "2025-12-21T10:00:00Z"
        }
      ]
    },
    "tier2_searches": { ... },
    "tier3_searches": { ... },
    "summary": {
      "total_expected": 24,
      "total_completed": 24,
      "total_failed": 0,
      "completion_rate": 1.0,
      "all_tiers_complete": true,
      "validation_status": "complete"
    }
  }
}
```

### product_coverage (Populate when evidence available)
Per-product CDM status assessment:
```json
{
  "product_coverage": {
    "assessment_date": "2025-12-21",
    "overall_confidence": 65,
    "products": {
      "IRS": {
        "cdm_status": "production|pilot|evaluation|planned|none|unknown",
        "cdm_reliance": "native|partial|minimal|none|unknown",
        "regulatory_driver": "EMIR_Refit|UK_EMIR|CFTC_Rewrite|JSCC|multiple|none",
        "confidence": 70,
        "evidence_ids": ["BANK-001", "BANK-003"],
        "knowledge_gap": false,
        "vendor_solution": "Delta Capita"
      },
      "CDS": { ... },
      "FX_Options": { ... }
    }
  }
}
```
**Product enum**: IRS, CDS, FX_Forwards, FX_Options, Equity_Swaps, Equity_Options, Commodities, Structured_Products, Repo, ETD

### jurisdiction_rollout (Populate when evidence available)
Per-jurisdiction CDM deployment priorities:
```json
{
  "jurisdiction_rollout": {
    "assessment_date": "2025-12-21",
    "jurisdictions": {
      "EU": {
        "regulatory_driver": "EMIR Refit",
        "deadline": "2024-04-29",
        "cdm_status": "production|pilot|compliant_traditional|non_compliant|unknown",
        "priority_level": "primary|secondary|tertiary|unknown",
        "confidence": 75,
        "evidence_ids": ["BANK-002"]
      },
      "UK": { ... },
      "US": { ... }
    },
    "rollout_sequence": {
      "first_jurisdiction": "EU",
      "subsequent_planned": ["UK", "US"],
      "confidence": 60
    }
  }
}
```
**Jurisdiction enum**: EU, UK, US, Japan, Singapore, Hong_Kong, Australia, Switzerland, Canada, Other

### adoption_drivers (Required for all banks)
Forces pushing toward or against CDM adoption:
```json
{
  "adoption_drivers": {
    "assessment_date": "2025-12-21",
    "pressures_to_adopt": [
      {
        "driver_type": "regulatory_mandate|infrastructure_mandate|counterparty_pressure|competitive_positioning|operational_efficiency",
        "description": "EMIR Refit deadline April 2024 requires enhanced reporting",
        "strength": "high|medium|low",
        "timeline_impact": "Immediate - deadline passed",
        "evidence_ids": ["BANK-001"],
        "confidence": 85
      }
    ],
    "hesitations_against": [
      {
        "hesitation_type": "capacity_constraint|insufficient_business_case|vendor_preference|technology_debt|wait_for_maturity|regulatory_remediation|ma_integration",
        "description": "Credit Suisse integration consuming technology capacity",
        "strength": "high|medium|low",
        "expected_duration": "temporary|medium_term|structural",
        "evidence_ids": ["BANK-004"],
        "confidence": 80
      }
    ],
    "net_assessment": {
      "outcome": "adoption_likely|adoption_possible|adoption_uncertain|adoption_unlikely",
      "rationale": "Strong regulatory pressure outweighs temporary capacity constraints",
      "timeline_estimate": "H2 2025",
      "confidence": 65,
      "knowledge_gaps_affect_assessment": true
    }
  }
}
```

### knowledge_gaps (Required - document research limits)
Where public research is exhausted:
```json
{
  "knowledge_gaps": [
    {
      "id": "GAP-001",
      "category": "product_coverage|jurisdiction|vendor|driver|counterparty|strategic|technical",
      "gap_type": "specific type from gap-taxonomy.json",
      "description": "Unknown which products are in CDM scope for EU reporting",
      "business_impact": "high|medium|low",
      "impact_rationale": "Cannot assess true CDM production scope",
      "public_research_exhausted": true,
      "searches_attempted": [
        "Deutsche Bank CDM product scope",
        "Deutsche Bank EMIR Refit products"
      ],
      "suggested_sources": [
        {
          "source_type": "insider_interview|vendor_backdoor|conference_networking",
          "target_role": "Head of Regulatory Reporting",
          "discovery_question": "Which product lines are using CDM for EMIR Refit reporting?"
        }
      ],
      "resolution_value": 80,
      "strategic_urgency": 70,
      "priority_score": 75
    }
  ],
  "gap_summary": {
    "total_gaps": 5,
    "critical_gaps": 1,
    "high_gaps": 2,
    "primary_research_recommended": true,
    "top_priority_gaps": ["GAP-001", "GAP-003"],
    "discovery_call_brief": {
      "recommended_targets": ["Head of Derivatives Technology", "CDM Program Lead"],
      "key_questions": ["Product scope?", "Timeline?", "Vendor vs build?"],
      "value_proposition": "CDM adoption benchmarking insights"
    }
  }
}
```

### counterparty_map (Populate when evidence available)
CCP and counterparty CDM connectivity:
```json
{
  "counterparty_map": {
    "assessment_date": "2025-12-21",
    "ccp_relationships": [
      {
        "ccp_name": "LCH|CME|Eurex|JSCC|ICE|DTCC|SGX|HKEX|ASX",
        "membership_status": "clearing_member|client_clearing|no_relationship|unknown",
        "cdm_requirement": "mandatory|preferred|optional|none|unknown",
        "cdm_deadline": "2025-06-01",
        "bank_cdm_status": "connected|building|planned|not_started|unknown",
        "products_cleared": ["IRS", "CDS"],
        "confidence": 70,
        "evidence_ids": ["BANK-005"]
      }
    ],
    "g16_exposure": [
      {
        "counterparty_bank": "JPMorgan",
        "relationship_type": "major_counterparty|moderate_counterparty|minor_counterparty",
        "counterparty_cdm_status": "cdm_native|cdm_enabled|traditional|unknown",
        "bilateral_cdm_connectivity": "operational|testing|planned|not_started|unknown",
        "interoperability_pressure": "high|medium|low|none"
      }
    ],
    "aggregated_assessment": {
      "bilateral_cdm_pressure_level": "high|medium|low|unknown",
      "network_effect_assessment": "strong_pull|moderate_pull|weak_pull|no_pull|unknown"
    }
  }
}
```

### vendor_analysis (Required for PRAGMATIST classification)
Build vs buy assessment:
```json
{
  "vendor_analysis": {
    "assessment_date": "2025-12-21",
    "overall_strategy": "internal_build|hybrid_internal_lead|hybrid_vendor_lead|full_outsource|unknown",
    "vendor_relationships": [
      {
        "vendor_name": "Delta Capita",
        "vendor_type": "platform_vendor|cdm_specialist|systems_integrator|consulting|utility_provider",
        "scope": ["cdm_core", "cdm_translation", "reporting", "ccp_connectivity"],
        "products_covered": ["IRS", "CDS"],
        "jurisdictions_covered": ["EU", "UK"],
        "relationship_stage": "production|implementation|pilot|evaluation|planned",
        "dependency_level": "high|medium|low",
        "confidence": 75,
        "evidence_ids": ["BANK-006"]
      }
    ],
    "internal_capabilities": {
      "has_internal_cdm_team": "yes_dedicated|yes_shared|no|unknown",
      "team_size_estimate": "large_10plus|medium_5to10|small_under5|unknown",
      "internal_scope": ["cdm_core_development", "integration", "testing"],
      "build_appetite": "high_prefers_build|balanced|low_prefers_buy|unknown"
    },
    "aggregated_assessment": {
      "vendor_dependency_score": "high|medium|low|none|unknown",
      "internal_capability_score": "strong|moderate|weak|none|unknown",
      "classification_implication": "supports_architect|supports_pragmatist_vendor|supports_pragmatist_hybrid|neutral|insufficient_data"
    }
  }
}
```

---

## Phase Execution Order

### Phase 1: European Tier 1 (5 banks)
```
deutsche-bank, societe-generale, ubs, barclays, hsbc
```

### Phase 2: UK Regional (2 banks)
```
natwest, lloyds
```

### Phase 3: Japanese (4 banks)
```
nomura, mufg, mizuho, smbc
```

### Phase 4: Other European (4 banks)
```
ing, credit-agricole, unicredit, commerzbank
```

### Phase 5: Spanish (2 banks)
```
santander, bbva
```

### Phase 6: Deep Dives (2 banks)
```
standard-chartered, pictet
```

### Phase 7: Emerging Markets (5 banks)
```
dbs, icbc, bank-of-china, ccb, abc
```

### Phase 8: US Investment Banks (5 banks)
```
jpmorgan, goldman-sachs, morgan-stanley, citigroup, bank-of-america
```

### Phase 9: US Custody Banks (2 banks)
```
state-street, bny-mellon
```

---

## Output Structure Per Bank

```
outputs/phase-{N}/{bank-id}/
├── evidence.json                         # PRIMARY (Ledger-First)
├── status.json                           # Bank processing status
├── 1-evidence/
│   ├── tier1-evidence.md                 # Rendered from evidence.json
│   ├── tier2-evidence.md
│   ├── tier3-evidence.md
│   └── null-results.md
├── 2-bayesian/
│   ├── post-tier1-update.md
│   ├── post-tier2-update.md
│   └── post-tier3-update.md
├── 3-gates/
│   ├── pre-mortem.md
│   ├── gate-1.md
│   ├── gate-2.md
│   ├── gate-3.md
│   └── contradiction-resolution.md       # If CONTRADICTIONS_DETECTED
├── 4-adversarial/
│   ├── counter-case.md
│   ├── disconfirming-searches.md
│   ├── steelman.md
│   └── verdict.md
├── 5-synthesis/
│   ├── confidence-calibration.md         # MUST be created FIRST
│   ├── assessment.md                     # Full 19-section assessment
│   └── framework-integration.md
└── snapshots/                            # Cached source content
```

---

## Validation Commands

```bash
# Validate evidence.json schema compliance
python tools/process_evidence.py --dry-run outputs/phase-1/deutsche-bank/evidence.json

# Run trust audit
python tools/trust_audit.py outputs/phase-1/deutsche-bank/evidence.json

# Validate stage completion
python tools/validate_stage.py --bank deutsche-bank --phase 1 --auto

# Render Markdown from evidence.json
python tools/render_evidence_md.py outputs/phase-1/deutsche-bank/evidence.json

# Full pipeline (verify + audit + render)
python tools/run_pipeline.py outputs/phase-1/deutsche-bank/evidence.json
```

---

## Anchor Points (Calibration Reference)

| Anchor | Fact | Validation Check |
|--------|------|------------------|
| BNP Paribas | First major bank CDM production Q3 2022 | No earlier major bank production claims |
| JPMorgan | CDM production October 2024 | Validates US bank adoption |
| JSCC | CDM production June 2025 | Japanese bank forcing function |
| Pictet | Confirmed CDM production | Validates wealth management use case |
| EMIR Refit | EU April 2024, UK September 2024 | European banks must have addressed |
| CFTC Rewrite | US reporting overhaul | US banks must address |

---

## Execution Start

Begin with Phase 1 banks in order:
1. deutsche-bank
2. societe-generale
3. ubs
4. barclays
5. hsbc

Then continue through all 9 phases in manifest order.

**Total Banks**: 31
**Total Phases**: 9
**Schema Version**: 4.3
