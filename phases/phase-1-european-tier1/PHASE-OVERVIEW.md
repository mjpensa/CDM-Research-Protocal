# Phase 1: European Tier 1 Banks

## Overview

| Attribute | Value |
|-----------|-------|
| **Phase Number** | 1 |
| **Execution Tier** | A (Full Protocol) |
| **Time Budget** | 20-25 hours total |
| **Banks** | 5 |

---

## Banks in This Phase

| Bank | Prompt File | Time Budget | Key Research Question |
|------|-------------|-------------|----------------------|
| Deutsche Bank | `deutsche-bank.md` | 4-5 hours | Validate "Pilot; production 2025" claim |
| Société Générale | `societe-generale.md` | 4-5 hours | Following BNP with 12-24 month lag? |
| UBS | `ubs.md` | 4-5 hours | Integration consuming CDM capacity? |
| Barclays | `barclays.md` | 4-5 hours | Progressing from Follower to Leader? |
| HSBC | `hsbc.md` | 4-5 hours | Internal capability or vendor-only? |

---

## Phase Context

### Why These Banks First

1. **Highest derivatives exposure** among international banks
2. **Diverse regulatory contexts** (EU, UK, Switzerland)
3. **Varied known positions** (from confirmed contributor to unknown)
4. **Framework validation priority** — these banks carry most strategic weight

### Shared Context

All Phase 1 banks are affected by:
- **EMIR Refit** (April 2024) — EU banks directly, UK indirectly
- **UK EMIR** (September 2024) — UK banks directly
- **BNP Paribas precedent** — First major European bank in production

### Regional Distribution

| Region | Banks | Primary Forcing Function |
|--------|-------|-------------------------|
| Germany | Deutsche Bank | EMIR Refit |
| France | Société Générale | EMIR Refit, BNP peer pressure |
| Switzerland | UBS | FINMA, but integration constraints |
| UK | Barclays, HSBC | UK EMIR |

---

## Execution Order

Recommended order based on dependencies:

1. **Barclays** — Known contributor, establishes Follower benchmark
2. **HSBC** — Known vendor relationship, classification nuance
3. **Société Générale** — BNP comparison framework
4. **Deutsche Bank** — Framework claim validation
5. **UBS** — Integration constraint hypothesis

*Rationale:* Start with banks where baseline is established (Barclays, HSBC), then move to hypothesis testing (SocGen, DB), finish with constraint case (UBS).

---

## Cross-Bank Hypotheses

Test these across Phase 1:

### H1: European Tier 1 Bifurcation
"European Tier 1 banks are bifurcating into Architects (building capability) vs. Pragmatists (waiting for utilities)"

**Test by:** Comparing final classifications — is there clear bifurcation or a spectrum?

### H2: UK Leadership
"UK banks (Barclays, HSBC) are further along than continental European banks due to earlier BOE/FCA pilot program"

**Test by:** Comparing UK bank classifications to DB, SocGen

### H3: Capacity Constraints Override Business Case
"Even banks with strong derivatives business cases may be Pragmatist if capacity is constrained (UBS)"

**Test by:** UBS classification despite high derivatives exposure

---

## Success Criteria for Phase 1

1. [ ] All 5 banks have finalized assessments
2. [ ] Framework claims validated or refuted with evidence
3. [ ] Regional patterns documented
4. [ ] Phase synthesis completed
5. [ ] Average confidence ≥65%
6. [ ] All cross-bank consistency tests pass

---

## Phase Completion Deliverables

After Phase 1, produce:

1. **Per-bank assessments** (5 files in `/outputs/phase-1/`)
2. **Framework integration extracts** (5 files)
3. **Phase 1 synthesis** (using `/templates/phase-synthesis.md`)
4. **Protocol adjustments** for Phase 2 (if any)

---

## Dependencies on Phase 1

Other phases depend on Phase 1 findings:

| Phase | Dependency |
|-------|------------|
| Phase 2 (UK Regional) | Barclays/HSBC establish UK baseline |
| Phase 3 (Japanese) | No direct dependency, but Tier 1 precedent |
| Phase 4 (Other European) | DB/SocGen establish European patterns |
| Phase 6 (Deep Dives) | Phase 1 may identify candidates |
