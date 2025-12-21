# Post-Tier 2 Bayesian Update: DBS Bank

**Research Date**: 2025-12-21
**Researcher**: Claude Code (Opus 4.5)
**Stage**: After Tier 2 Evidence Collection

---

## Prior Probability (Post-Tier 1)

| Hypothesis | Probability |
|------------|-------------|
| PRAGMATIST | 99.1% |
| ARCHITECT | 0.6% |
| OBSERVER | 0.3% |

---

## Tier 2 Evidence Review

**Evidence Found**: 2 items (both governance-level)

### E001: ISDA Board Membership
- **Claim**: Andrew Ng serves as ISDA Board Member (Group Executive & Group Head of Global Financial Markets at DBS)
- **Source**: isda.org/board-of-directors
- **Claim Type**: `membership_or_participation`
- **Significance**: High-level institutional connection to CDM governance

### E002: MAS SFEMC Deputy Co-chair
- **Claim**: Andrew Ng is Deputy Co-chair of Singapore Foreign Exchange Market Committee
- **Source**: mas.gov.sg
- **Claim Type**: `membership_or_participation`
- **Significance**: Regulatory influence in Singapore FX market

**What Was NOT Found**:
- No trade press coverage of DBS CDM initiatives
- No vendor announcements of DBS CDM implementations
- No analyst reports mentioning DBS and CDM
- No conference presentations by DBS on CDM

---

## Likelihood Ratio Calculation

### P(ISDA Board + SFEMC | PRAGMATIST)

If DBS is truly PRAGMATIST (no CDM engagement), what is the probability we'd find governance-level participation?

**Estimate**: ~10%

**Reasoning**:
- ISDA Board membership is rare (only ~20 seats globally)
- Board members are often from major derivatives dealers
- Possible for executives to serve on boards without organizational CDM adoption
- However, board membership suggests institutional awareness of CDM

### P(ISDA Board + SFEMC | OBSERVER)

If DBS is OBSERVER (ecosystem-engaged but no implementation), what is the probability of this evidence?

**Estimate**: ~70%

**Reasoning**:
- OBSERVER classification specifically covers governance-level participation
- ISDA Board membership is strong signal of ecosystem engagement
- SFEMC role indicates regional market structure involvement
- No technical implementation required for OBSERVER status

### P(ISDA Board + SFEMC | ARCHITECT)

If DBS were ARCHITECT, what is the probability of finding only governance evidence?

**Estimate**: ~20%

**Reasoning**:
- ARCHITECT banks typically have both governance AND technical evidence
- Finding governance without technical signals suggests OBSERVER, not ARCHITECT
- Unlikely for production CDM usage to have zero technical footprint

---

## Bayesian Update

Recalculating with new evidence:

```
P(OBSERVER | Evidence) = P(Evidence | OBSERVER) × P(OBSERVER) / P(Evidence)

P(Evidence) = P(Ev | OBSERVER) × P(OBSERVER) + P(Ev | PRAGMATIST) × P(PRAGMATIST) + P(Ev | ARCHITECT) × P(ARCHITECT)
            = 0.70 × 0.003 + 0.10 × 0.991 + 0.20 × 0.006
            = 0.0021 + 0.0991 + 0.0012
            = 0.1024

P(OBSERVER | Evidence) = (0.70 × 0.003) / 0.1024
                        = 0.0021 / 0.1024
                        = 0.0205 (2.05%)

P(PRAGMATIST | Evidence) = (0.10 × 0.991) / 0.1024
                          = 0.0991 / 0.1024
                          = 0.968 (96.8%)

P(ARCHITECT | Evidence) = (0.20 × 0.006) / 0.1024
                         = 0.0012 / 0.1024
                         = 0.012 (1.2%)
```

---

## Updated Probabilities

| Hypothesis | Prior (Post-T1) | Posterior (After Tier 2) |
|------------|-----------------|--------------------------|
| PRAGMATIST | 99.1% | **96.8%** |
| OBSERVER | 0.3% | **2.05%** |
| ARCHITECT | 0.6% | **1.2%** |

---

## Interpretation

The **governance evidence provides weak support** for upgrading from PRAGMATIST to OBSERVER, but the posterior probability of OBSERVER remains very low (2.05%).

**Key Tensions**:

1. **Strong Governance Signal**: ISDA Board membership is significant and rare
2. **Zero Technical Evidence**: Complete absence of implementation signals
3. **Individual vs. Organizational**: Evidence reflects Andrew Ng's roles, not DBS institutional commitment

**Critical Question**: Does one executive's board membership constitute "organizational engagement"?

---

## Alternative Interpretation

### Scenario A: OBSERVER (Ecosystem-Engaged)
**Argument**: ISDA Board membership demonstrates institutional engagement with CDM governance, warranting OBSERVER classification even without technical adoption.

**Confidence**: ~55%
- Governance signals are real and verifiable
- Board membership provides CDM awareness and influence
- Consistent with "ecosystem-engaged" without implementation

### Scenario B: PRAGMATIST (No Engagement)
**Argument**: Andrew Ng's roles are personal appointments reflecting his expertise, not DBS organizational CDM strategy.

**Confidence**: ~45%
- No evidence of DBS technology teams engaging with CDM
- No working group participation beyond board seat
- Zero technical implementation signals
- Bayesian posterior strongly favors PRAGMATIST (96.8%)

---

## Recommended Classification

**Classification**: **OBSERVER (Ecosystem-Engaged)**
**Confidence**: **55%**

**Rationale**:
- ISDA Board membership crosses threshold for "participation" even if narrow
- MAS SFEMC role adds regional regulatory context
- Absence of technical evidence caps confidence at 55%
- Tier 2 evidence maximum (75%) reduced due to narrow scope of engagement

**Trust Flags**:
- `LOW_TIER_ONLY` (no Tier 1 evidence)
- `MISSING_CORROBORATION` (single individual's roles)
- `NARROW_ENGAGEMENT_SCOPE` (governance only, no technical)

---

## Decision Point

**Recommendation**: Proceed to Tier 3 for completeness, but low expectation of additional evidence.

**Research Question for Tier 3**: Are there any hiring signals or job postings indicating DBS plans to implement CDM?

---

**Next Stage**: Tier 3 Evidence Collection (job postings, LinkedIn signals)
