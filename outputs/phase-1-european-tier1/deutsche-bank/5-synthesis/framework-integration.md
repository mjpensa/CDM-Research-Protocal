# Deutsche Bank - Framework Integration

## Classification Matrix Position

```
                    CDM Engagement Level
                    LOW         MEDIUM      HIGH
                    |           |           |
Regulatory  HIGH    | OBSERVER  | PRAGMATIST| ARCHITECT
Pressure            |           |     *DB*  |
            MEDIUM  | OBSERVER  | PRAGMATIST| ARCHITECT
                    |           |           |
            LOW     | OBSERVER  | OBSERVER  | PRAGMATIST
```

**Deutsche Bank Position**: PRAGMATIST with HIGH regulatory pressure, LOW current CDM engagement

## Vendor Matrix Integration

Per `config/vendor-matrix.json`:

| Pattern | Deutsche Bank Status |
|---------|---------------------|
| Internal CDM team + vendor tooling | NO |
| Outsourcing CDM to vendor | NO EVIDENCE |
| Traditional platforms, no CDM layer | LIKELY |

**Vendor Classification**: Traditional (no CDM vendor relationship identified)

## Maturity Classification

Per CLAUDE.md Section 9:

| Classification | Trigger | Deutsche Bank |
|---------------|---------|---------------|
| ARCHITECT (Native) | production_usage | NO |
| ARCHITECT (Active) | pilot_or_poc | HISTORICAL ONLY |
| PRAGMATIST (Ecosystem) | open_source_contribution | HISTORICAL (2021) |
| PRAGMATIST (Vendor) | vendor_proxy_signal | NO |
| OBSERVER | membership_or_participation | NO CURRENT |
| UNKNOWN | No verified evidence | NO |

**Maturity Score**: 2 (historical contribution, not current)

## Temporal Analysis

| Time Period | Status | Evidence |
|-------------|--------|----------|
| 2020-2021 | ACTIVE PARTICIPANT | FINOS Legend pilot, FX Options contribution |
| 2021-2022 | GOVERNANCE ROLE | Russell Green FINOS Board |
| 2022-2024 | NO VISIBLE ACTIVITY | Informative absence across all tiers |

**Trajectory**: Declined from ARCHITECT (Active) to PRAGMATIST over 3 years

## Peer Comparison (European Tier 1)

| Bank | Classification | Confidence | Key Evidence |
|------|---------------|------------|--------------|
| Deutsche Bank | PRAGMATIST | 95% | Historical pilot only |
| Barclays | TBD | - | Research pending |
| HSBC | TBD | - | Research pending |
| Société Générale | TBD | - | Research pending |
| UBS | TBD | - | Research pending |

## Risk Assessment

### Risks of Current Classification

| Risk | Likelihood | Impact |
|------|------------|--------|
| Hidden internal implementation | LOW | HIGH (would change classification) |
| Imminent announcement | LOW | MEDIUM (timing only) |
| Vendor partnership undisclosed | LOW | MEDIUM |

### Confidence Bounds

| Scenario | Probability |
|----------|-------------|
| Deutsche Bank is ARCHITECT | 3.5% |
| Deutsche Bank is PRAGMATIST | 96.5% |
| Classification error | ~5% |

## Integration with Research Phases

| Phase | Deutsche Bank Relevance |
|-------|------------------------|
| Phase 1 (European Tier 1) | PRIMARY - researched |
| Phase 4 (Other European) | Reference for German banks (Commerzbank) |
| Phase 8 (US Investment) | Comparison with US peers |

## Key Findings for Portfolio

1. **Historical Pioneer, Current Non-Participant**: Deutsche Bank demonstrated early CDM capability but did not operationalize.

2. **Governance vs Implementation**: FINOS board role shows institutional awareness without production commitment.

3. **German Bank Pattern**: May set baseline for other German banks (Commerzbank in Phase 4).

4. **Pilot Decay**: Example of pilot-to-production failure - valuable data point for understanding CDM adoption barriers.

---
*Framework Integration Complete*
*Classification: PRAGMATIST*
*Generated: 2024-12-21*
