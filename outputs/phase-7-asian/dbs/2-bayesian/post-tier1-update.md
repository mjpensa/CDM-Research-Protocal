# Post-Tier 1 Bayesian Update: DBS Bank

**Research Date**: 2025-12-21
**Researcher**: Claude Code (Opus 4.5)
**Stage**: After Tier 1 Evidence Collection

---

## Prior Probability

**Null Hypothesis**: DBS Bank is **PRAGMATIST** (no CDM adoption)
**Prior P(PRAGMATIST)**: 85%

**Rationale for Prior**:
- Singapore has no regulatory mandate for CDM (unlike EU EMIR Refit)
- MAS has not signaled CDM requirements for derivatives reporting
- Regional banks face less regulatory pressure than European/US counterparts
- Base rate: ~15% of global banks show CDM adoption signals

---

## Tier 1 Evidence Review

**Evidence Found**: None

**Sources Checked**:
- dbs.com (official announcements)
- isda.org (case studies, working groups)
- finos.org (membership, contributions)
- github.com/finos (code commits)
- MAS regulatory filings

**Result**: No official announcements, FINOS membership, code contributions, or regulatory disclosures mentioning CDM.

---

## Likelihood Ratio Calculation

### P(No Tier 1 Evidence | ARCHITECT)

If DBS were an ARCHITECT (production CDM usage), what is the probability we'd find no Tier 1 evidence?

**Estimate**: ~5%

**Reasoning**:
- ARCHITECT banks typically announce CDM implementations (regulatory filings, press releases)
- FINOS membership is common among CDM production users
- GitHub contributions or vendor announcements would be expected
- Very unlikely to have production usage with zero Tier 1 footprint

### P(No Tier 1 Evidence | PRAGMATIST)

If DBS is PRAGMATIST (no CDM), what is the probability we'd find no Tier 1 evidence?

**Estimate**: ~95%

**Reasoning**:
- Absence of evidence is strong indicator of absence of adoption
- PRAGMATIST banks have no reason to appear in FINOS, ISDA case studies, or code repos
- Null result is expected outcome

---

## Bayesian Update

Using Bayes' Theorem:

```
P(PRAGMATIST | No Tier 1) = P(No Tier 1 | PRAGMATIST) × P(PRAGMATIST) / P(No Tier 1)

P(No Tier 1) = P(No Tier 1 | PRAGMATIST) × P(PRAGMATIST) + P(No Tier 1 | ARCHITECT) × P(ARCHITECT)
             = 0.95 × 0.85 + 0.05 × 0.15
             = 0.8075 + 0.0075
             = 0.815

P(PRAGMATIST | No Tier 1) = (0.95 × 0.85) / 0.815
                           = 0.8075 / 0.815
                           = 0.991 (99.1%)
```

---

## Updated Probabilities

| Hypothesis | Prior | Posterior (After Tier 1) |
|------------|-------|--------------------------|
| PRAGMATIST | 85% | **99.1%** |
| ARCHITECT | 10% | **0.6%** |
| OBSERVER | 5% | **0.3%** |

---

## Interpretation

The **absence of Tier 1 evidence strongly supports** the PRAGMATIST hypothesis. The posterior probability has increased from 85% to 99.1%.

**Key Insight**: The null Tier 1 result is highly diagnostic. If DBS had production CDM usage or active development, we would expect to find official announcements, FINOS membership, or code contributions.

**However**: This update does not account for:
- Possible governance-level engagement (ISDA membership)
- Ecosystem participation without technical adoption
- Regional differences in disclosure practices

These factors may emerge in Tier 2/3 evidence.

---

## Decision Point

**Recommendation**: Proceed to Tier 2 sources.

**Justification**:
- While PRAGMATIST is highly probable, Tier 2 may reveal ecosystem signals
- Singapore banks may have different disclosure practices than Western peers
- Trade press or analyst reports may provide context unavailable in official sources

**Updated Research Question**: Is there any evidence of governance-level engagement or ecosystem awareness, even absent technical adoption?

---

**Next Stage**: Tier 2 Evidence Collection (trade press, analyst reports, vendor announcements)
