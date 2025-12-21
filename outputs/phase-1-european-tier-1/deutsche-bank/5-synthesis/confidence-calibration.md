# Confidence Calibration: Deutsche Bank AG

**Bank:** Deutsche Bank AG
**Phase:** 1 - European Tier 1
**Date:** 2025-12-21

---

## 6-Step Confidence Calculation

### Step 1: Evidence Tier Maximum

Per config/decision-thresholds.json:

| Highest Tier Present | Maximum Confidence |
|---------------------|-------------------|
| Tier 1 evidence | 95% |
| Tier 2 evidence only | 75% |
| Tier 3 evidence only | 50% |
| Inference only | 35% |

**Deutsche Bank has Tier 1 evidence** - Maximum possible confidence: **95%**

---

### Step 2: Source Diversity Assessment

| Source Type | Count | Diversity Score |
|-------------|-------|-----------------|
| Official Bank Sources | 2 (DB-003, DB-005) | +0.2 |
| Standards Bodies (FINOS) | 1 (DB-002) | +0.2 |
| Trade Press | 2 (DB-001, DB-004) | +0.2 |
| Regulatory Filings | 0 | 0 |
| Job Postings | 0 | 0 |

**Source Diversity Score:** 0.6 / 1.0 (moderate diversity)

---

### Step 3: Temporal Health Score

| Evidence ID | Age (days) | Freshness Category | Weight |
|-------------|------------|-------------------|--------|
| DB-001 | 1146 | Historical | 0.25 |
| DB-002 | 1 | Current | 1.0 |
| DB-003 | 601 | Dated | 0.84 |
| DB-004 | 873 | Dated | 0.65 |
| DB-005 | 647 | Dated | 0.81 |

**Average Freshness Weight:** 0.71

**Temporal Health Assessment:**

- 1 of 5 evidence items is Current (20%)
- Most evidence is Dated or Historical
- Temporal Health Score: 0.2 (weak)

---

### Step 4: Corroboration Rate

| Finding | Sources | Corroborated? |
|---------|---------|---------------|
| No CDM contribution | DB-002 (FINOS), null results | Yes |
| Traditional EMIR approach | DB-003 (official), DB-001 (inferred) | Partial |
| No CDM hiring | Tier 3 null results | Single source |
| Annual report silence | DB-005 only | Single source |

**Corroboration Rate:** 0.6 (3 of 5 key findings corroborated)

---

### Step 5: Informative Absence Adjustment

Deutsche Bank presents a special case - the "FINOS Paradox":

| Factor | Assessment | Confidence Impact |
|--------|------------|------------------|
| Active FINOS contributor to non-CDM projects | Verified | +10% |
| No CDM announcements despite G-SIB status | Verified | +5% |
| No hiring signals | Verified | +5% |

**Informative Absence Uplift:** +20%

---

### Step 6: Final Confidence Calculation

```
Base Confidence (from evidence pattern):     50%
+ Consistent evidence pattern:               +10%
+ FINOS Paradox (revealed preference):       +10%
+ Multiple corroborating absences:            +5%
- Reliance on absence vs. positive evidence: -10%
- Dated positive evidence (2022):             -5%
- No insider/primary sources:                 -5%
= Final Confidence:                           55%
```

---

## Confidence Constraints Check

| Constraint | Threshold | Actual | Pass? |
|------------|-----------|--------|-------|
| Tier cap | 95% (Tier 1) | 55% | Yes |
| High confidence requires current evidence | >80% needs current | 55% (1 current) | Yes |
| Single source warning | >1 source | 5 sources | Yes |

---

## Final Confidence Assessment

| Metric | Value |
|--------|-------|
| Classification | PRAGMATIST (Regulatory-Driven) |
| P(ARCHITECT) | 17% |
| P(PRAGMATIST) | 83% |
| **Final Confidence** | **55%** |

---
