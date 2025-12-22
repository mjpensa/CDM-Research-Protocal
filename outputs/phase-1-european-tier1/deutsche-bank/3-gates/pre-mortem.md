# Pre-Mortem Analysis: Deutsche Bank AG

**Date**: 2025-12-21
**Stage**: Pre-Search Failure Mode Identification

---

## Potential Failure Modes

### 1. Historical Pilot Conflation
- **Risk**: Over-weighting 2020-2021 FINOS Legend pilot without production follow-through
- **Mitigation**: Apply temporal weighting; require 2023-2024 evidence for high confidence
- **Classification Impact**: Historical pilot without continuation = PRAGMATIST

### 2. Regulatory Noise
- **Risk**: Deutsche Bank's extensive regulatory remediation may dominate search results
- **Mitigation**: Use CDM-specific search terms; filter out general compliance news
- **Classification Impact**: Regulatory burden may explain CDM capacity constraints

### 3. German Discretion Culture
- **Risk**: German banks may be less public about technology initiatives
- **Mitigation**: Search for conference presentations, named individuals, ISDA participation
- **Classification Impact**: Low public evidence may not equal low activity

### 4. FX Options Contribution Misinterpretation
- **Risk**: Code contribution may be one-time rather than strategic commitment
- **Mitigation**: Look for sustained contribution patterns, production deployment
- **Classification Impact**: Single contribution = PRAGMATIST; sustained = ARCHITECT

### 5. EMIR Refit Response Ambiguity
- **Risk**: EMIR Refit compliance may use traditional methods, not CDM
- **Mitigation**: Specifically search for CDM-based EMIR response
- **Classification Impact**: Non-CDM EMIR response indicates PRAGMATIST

---

## Key Questions to Answer

1. Did the FINOS Legend pilot lead to any production deployment?
2. Is there evidence of CDM activity after 2021?
3. How did Deutsche Bank address EMIR Refit (April 2024)?
4. Are there named individuals driving CDM work?
5. What is the scope of any FX Options CDM contribution?

---

## Search Strategy

### Tier 1 (Official Sources)
- Deutsche Bank official announcements
- ISDA official publications mentioning Deutsche Bank
- FINOS/GitHub contribution records
- BaFin regulatory filings

### Tier 2 (Industry Sources)
- Risk.net, Waters Technology coverage
- Conference presentations (Sibos, ISDA AGM)
- Vendor partnerships (REGnosys, etc.)

### Tier 3 (Signal Sources)
- LinkedIn posts from Deutsche Bank technology staff
- Job postings for CDM/ISDA roles

---

## Success Criteria

- [ ] Determine if Legend pilot led to production
- [ ] Find evidence of post-2021 CDM activity (or confirm absence)
- [ ] Identify EMIR Refit approach
- [ ] Locate named individuals if possible
- [ ] Assess contribution scope and sustainability
