# CDM Research Protocol - Quick Reference

## Run Full Pipeline on a Bank

```bash
# Validate and process existing outputs
python tools/run_pipeline.py outputs/phase-1-european-tier1/barclays/

# Full validation with all checks
python tools/run_pipeline.py outputs/phase-1-european-tier1/barclays/ --full-validation

# Validate URLs before processing
python tools/run_pipeline.py outputs/phase-1-european-tier1/barclays/ --validate-urls-first
```

## Validate Research Outputs

```bash
# Validate single bank
python tools/research_runner.py --validate-only outputs/phase-1-european-tier1/barclays/

# Validate entire phase
python tools/research_runner.py --phase 1 --all

# Export results to JSON
python tools/research_runner.py --phase 1 --all --output results.json

# Run cross-bank validation
python tools/cross_bank_validator.py outputs/
```

## Individual Tools

```bash
# Check for deprecated terminology
python tools/migrate_terminology.py outputs/

# Test config loader
python tools/config_loader.py

# Parse markdown outputs
python tools/markdown_parser.py outputs/phase-1-european-tier1/barclays/

# Test Bayesian calculations
python tools/bayesian_calculator.py

# Validate URLs
python tools/url_validator.py outputs/phase-1-european-tier1/barclays/1-evidence/tier1-evidence.md

# Run trust audit
python tools/trust_audit.py outputs/phase-1-european-tier1/barclays/evidence.json

# Render final report
python tools/render_report.py outputs/phase-1-european-tier1/barclays/evidence.json

# Check workflow orchestration
python tools/orchestrate.py outputs/phase-1-european-tier1/barclays/ --status
```

## Configuration Files

| File | Purpose |
|------|---------|
| `config/decision-thresholds.json` | All numeric thresholds (confidence caps, skip conditions) |
| `config/bayesian-lr-tables.json` | Likelihood ratios for evidence types |
| `config/anchor-points.json` | Immutable facts for QA validation |
| `config/bank-manifest.json` | Bank metadata and phase assignments |
| `config/vendor-matrix.json` | Known vendor relationships |
| `config/classification-taxonomy.json` | Valid classification values |
| `config/agent-config-reference.md` | Agent-readable threshold reference |

## Evidence Tiers

| Tier | Max Confidence | Sources |
|------|---------------|---------|
| 1 | 95% | Official bank/ISDA/FINOS announcements, regulatory filings |
| 2 | 75% | Trade press (Risk.net, Waters), vendor releases, conferences |
| 3 | 50% | Job postings, LinkedIn, blogs |
| 4 | 35% | Inference only (business model, peer behavior) |

## Classification Values

- **ARCHITECT**: Native, Leader, Follower
- **PRAGMATIST**: Vendor-dependent, Ecosystem-aware
- **OBSERVER**: Monitoring
- **UNKNOWN**: Insufficient evidence

## Bayesian Thresholds

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Skip to adversarial | P > 80% or P < 20% | Skip remaining tiers |
| Low confidence block | P in 40-60% | Require human review |
| Early termination | P > 95% (Tier 1 only) | Complete research early |
| Extreme LR flag | LR < 0.01 or LR > 100 | Review calculation |

## Anchor Points (Immutable Facts)

Banks in production (must be ARCHITECT-Native):
- BNP Paribas (2022-Q3)
- JPMorgan (2024-10)
- JSCC (2023)
- Pictet (2024)

Confirmed contributors (must be ARCHITECT):
- Barclays
- Standard Chartered
- Deutsche Bank
- Societe Generale

## Common Workflows

### New Bank Research
1. Create output directory: `outputs/phase-N/{bank-id}/`
2. Check negative facts: `knowledge_base/negative_facts.md`
3. Run pre-mortem analysis
4. Gather Tier 1 evidence
5. Run Bayesian update
6. Check gate conditions
7. Continue to Tier 2/3 if needed
8. Run adversarial challenge
9. Generate synthesis

### Quality Assurance
1. Run cross-bank validation: `python tools/cross_bank_validator.py outputs/`
2. Check anchor point violations (critical)
3. Review ordinal ranking issues
4. Verify confidence-classification alignment

### Troubleshooting

| Issue | Solution |
|-------|----------|
| UnicodeEncodeError | Run tools with `python -X utf8` |
| Missing config | Check `config/` directory exists |
| URL validation errors | Check internet connectivity |
| Cross-bank failures | Review anchor-points.json |

---

*Last Updated: 2025-12-19*
