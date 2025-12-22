# Pre-Mortem Analysis: BNY Mellon

**Bank**: Bank of New York Mellon
**Phase**: 9 (US Custody Banks)
**Date**: 2025-12-21

---

## Pre-Mortem Question

"If we fail to correctly classify BNY Mellon's CDM engagement, what could explain this?"

---

## Predicted Failure Modes

### 1. Mistaking FINOS Membership for CDM Work (MEDIUM Risk)
BNY Mellon's FINOS Platinum membership could be misinterpreted as CDM engagement when it's actually general open source participation.

**Mitigation**: Distinguish between general FINOS membership and CDM-specific contributions.

### 2. Missing Internal CDM Initiatives (LOW Risk)
BNY Mellon could have internal CDM exploration not publicly announced.

**Mitigation**: Search for job postings, vendor relationships, conference mentions.

### 3. Over-weighting CFTC Enforcement (LOW Risk)
CFTC penalties might incorrectly suggest no derivatives capability when BNY Mellon is a registered swap dealer.

**Mitigation**: Separate reporting failures from CDM adoption status.

---

## Outcome

OBSERVER classification is appropriate. FINOS membership is general, not CDM-specific. CFTC enforcement confirms traditional reporting approach.

---

*Pre-mortem analysis under CDM Research Protocol v2.3*
