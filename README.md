# CDM/DRR International Bank Research Protocol v2.0

## Executive Summary

This protocol provides a rigorous, evidence-based methodology for determining the CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning of international banks. It employs advanced analytical techniques including Bayesian updating, structured adversarial challenges, and calibrated confidence scoring.

**Purpose:** Validate and refine international bank classifications for the CDM Strategic Framework document.

**Output:** Per-bank assessments with explicit confidence levels, documented uncertainties, and framework integration extracts.

---

## Quick Reference

### Classification Framework

```
ARCHITECT — Active builders/contributors to CDM ecosystem
├── Native: In production, governance leadership
├── Leader: Production committed, significant contribution  
└── Follower: Active contribution, no production commitment

PRAGMATIST — Will adopt when necessary, not building
├── Vendor-dependent: CDM connectivity via third-party
├── Integration-constrained: Capacity consumed elsewhere
├── Regulatory-driven: Will move when mandated
└── Network-accelerant: Will move on counterparty pressure
```

### Execution Tiers

| Tier | Time Budget | Banks | Passes |
|------|-------------|-------|--------|
| **A** | 4-6 hours | DB, SocGen, UBS, Barclays, HSBC | Full 6-pass |
| **B** | 2-3 hours | Japanese megabanks, UK regionals | Standard 5-pass |
| **C** | 1-1.5 hours | Other European, Spanish, Emerging | Rapid 3-pass |

### Confidence Thresholds

| Confidence | Criteria | Action |
|------------|----------|--------|
| **90%+** | Tier 1 evidence, corroborated | State as finding |
| **70-89%** | Strong Tier 2 evidence | State with minor caveat |
| **50-69%** | Tier 2 only, inference required | State with significant caveat |
| **30-49%** | Tier 3 or absence-based | Flag for validation |
| **<30%** | No meaningful evidence | Classify as UNKNOWN |

---

## Directory Structure

```
/cdm-research-protocol/
├── README.md                    ← You are here
├── methodology/
│   ├── core-principles.md       ← Foundational approach
│   ├── evidence-framework.md    ← Evidence tiers and quality filters
│   ├── bayesian-updating.md     ← Probability calculations
│   └── confidence-calibration.md ← Confidence criteria
├── templates/
│   ├── per-bank-output.md       ← Final output format
│   ├── framework-integration.md ← Data for framework document
│   ├── reasoning-gates.md       ← Required checkpoints
│   └── adversarial-checks.md    ← Challenge protocols
├── phases/
│   ├── phase-1-european-tier1/      ← Deutsche Bank, SocGen, UBS, Barclays, HSBC
│   ├── phase-2-uk-regional/         ← NatWest, Lloyds
│   ├── phase-3-japanese/            ← Nomura, MUFG, Mizuho, SMBC
│   ├── phase-4-other-european/      ← ING, Crédit Agricole, UniCredit, Commerzbank
│   ├── phase-5-spanish/             ← Santander, BBVA
│   ├── phase-6-deep-dives/          ← Standard Chartered, Pictet
│   ├── phase-7-emerging-markets/    ← DBS, Chinese banks
│   ├── phase-8-us-investment-banks/ ← JPMorgan, Goldman Sachs, Morgan Stanley, Citi, BofA
│   └── phase-9-us-custody-banks/    ← State Street, BNY Mellon
├── appendices/
│   ├── search-strategies.md     ← Query templates and iteration
│   ├── contradiction-resolution.md
│   ├── null-result-handling.md
│   └── quality-assurance.md     ← Self-review checklists
└── outputs/                     ← Research results go here
```

---

## Workflow Summary

### For Each Bank:

1. **Load** the bank-specific prompt from `/phases/`
2. **Execute** passes sequentially, completing all reasoning gates
3. **Apply** templates from `/templates/` for outputs
4. **Reference** `/methodology/` for analytical frameworks
5. **Consult** `/appendices/` for edge cases
6. **Save** results to `/outputs/`

### After Each Phase:

1. Complete phase synthesis template
2. Run cross-bank consistency validation
3. Update running pattern observations
4. Adjust protocol for next phase if needed

---

## Anchor Points (Immutable Facts)

These facts constrain all research findings:

| Anchor | Fact | Implication |
|--------|------|-------------|
| **Production Timeline** | BNP Paribas (2022), JPMorgan (Oct 2024), JSCC (Jun 2025) | No bank claims earlier production |
| **Total in Production** | 4 firms globally (BNP, JPM, JSCC, Pictet) | Production claims require verification |
| **EMIR Refit** | EU April 2024, UK September 2024 | European banks must have addressed |
| **Confirmed Contributors** | Standard Chartered, Barclays (FINOS) | Follower threshold established |

---

## Getting Started

1. Read `/methodology/core-principles.md` for foundational approach
2. Review `/methodology/bayesian-updating.md` for probability framework
3. Load first bank prompt from `/phases/phase-1-european-tier1/deutsche-bank.md`
4. Execute research following all gates and checkpoints
5. Complete output using `/templates/per-bank-output.md`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | Current | Modular structure, Bayesian updating, enhanced adversarial, quality gates |
| 1.0 | Prior | Initial protocol (monolithic) |
