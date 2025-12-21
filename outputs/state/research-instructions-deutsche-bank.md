# Research Task: Deutsche Bank AG

## Overview
Execute CDM/DRR research for Deutsche Bank AG following the protocol in docs/workflow.md.

## Output Directory
outputs/phase-1-european-tier-1/deutsche-bank/

## Steps to Execute

### 1. Pre-Flight
- Read CLAUDE.md for rules
- Check knowledge_base/negative_facts.md for known dead ends
- Create output directory structure

### 2. Tier 1 Evidence (Official Sources)
Use WebSearch to find evidence from:
- Deutsche Bank AG's official website (investor relations, press, technology)
- ISDA.org mentions of this bank
- FINOS.org / github.com/finos contribution history
- Regulatory filings (SEC, FCA, BaFin, ESMA)
- Annual reports mentioning CDM/DRR

Search queries to try:
- "Deutsche Bank AG" "Common Domain Model" OR CDM
- "Deutsche Bank AG" ISDA contribution OR member
- "Deutsche Bank AG" FINOS CDM
- site:isda.org "Deutsche Bank AG"
- site:finos.org "Deutsche Bank AG"

Save findings to: outputs/phase-1-european-tier-1/deutsche-bank/1-evidence/tier1-evidence.md

### 3. Bayesian Update T1
Calculate P(ARCHITECT) update based on Tier 1 evidence.
Save to: outputs/phase-1-european-tier-1/deutsche-bank/2-bayesian/post-tier1-update.md

### 4. Gate 1 Decision
If P(ARCHITECT) > 80% or P(PRAGMATIST) > 80%, skip to adversarial.
Otherwise continue to Tier 2.

### 5. Tier 2 Evidence (Industry Sources)
Search Risk.net, Waters Technology, Bloomberg, FT for:
- "Deutsche Bank AG" derivatives reporting modernization
- "Deutsche Bank AG" CDM pilot OR implementation
- Conference presentations by Deutsche Bank AG on CDM

Save to: outputs/phase-1-european-tier-1/deutsche-bank/1-evidence/tier2-evidence.md

### 6. Bayesian Update T2
Update probabilities.
Save to: outputs/phase-1-european-tier-1/deutsche-bank/2-bayesian/post-tier2-update.md

### 7. Gate 2 Decision
Check skip conditions again.

### 8. Tier 3 Evidence (Signals)
Search for:
- Job postings: site:deutschebankag.com CDM OR "ISDA" jobs
- LinkedIn: Deutsche Bank AG CDM team
- Patent filings

Save to: outputs/phase-1-european-tier-1/deutsche-bank/1-evidence/tier3-evidence.md

### 9. Bayesian Update T3
Final probability update.
Save to: outputs/phase-1-european-tier-1/deutsche-bank/2-bayesian/post-tier3-update.md

### 10. Adversarial Challenge
Try to DISPROVE the current classification:
- Search for counter-evidence
- Build strongest case for opposite classification
- Issue verdict: SUSTAINED, WEAKENED, or REVISED

Save to: outputs/phase-1-european-tier-1/deutsche-bank/4-adversarial/verdict.md

### 11. Synthesis
Generate final assessment following templates/per-bank-output.md.
Save to: outputs/phase-1-european-tier-1/deutsche-bank/5-synthesis/assessment.md

### 11a. Product Line CDM Intelligence (v4.0)
For each product type (IRS, CDS, FX, Equity, Commodities), gather:

**Search Patterns:**
- "Deutsche Bank AG" CDM "interest rate swaps" OR IRS
- "Deutsche Bank AG" CDM "credit derivatives" OR CDS
- "Deutsche Bank AG" CDM FX OR "foreign exchange"
- "Deutsche Bank AG" CDM equity derivatives
- "Deutsche Bank AG" CDM commodities

**For each product, document:**
- CDM Status: production / pilot / planned / none / unknown
- Regulatory Driver: EMIR_Refit / UK_EMIR / CFTC_Rewrite / JSCC / multiple / none
- Approach: Internal build / Vendor solution / Hybrid / Unknown
- Confidence: percentage
- Knowledge Gap: Yes/No (if insider knowledge would be required)

**Product Coverage Matrix:**
| Product | CDM Status | Regulatory Driver | Approach | Confidence | Knowledge Gap |
|---------|------------|-------------------|----------|------------|---------------|
| IRS     | [status]   | [driver]          | [approach] | [X]%     | [Yes/No]     |
| CDS     | [status]   | [driver]          | [approach] | [X]%     | [Yes/No]     |
| FX      | [status]   | [driver]          | [approach] | [X]%     | [Yes/No]     |
| Equity  | [status]   | [driver]          | [approach] | [X]%     | [Yes/No]     |
| Commodities | [status] | [driver]       | [approach] | [X]%     | [Yes/No]     |

### 11b. Jurisdiction CDM Intelligence (v4.0)
For each jurisdiction where Deutsche Bank AG has derivatives operations:

**Regulatory Calendar:**
| Jurisdiction | Regulation | Deadline | Status |
|--------------|------------|----------|--------|
| EU | EMIR Refit | April 2024 | LIVE |
| UK | UK EMIR | September 2024 | LIVE |
| US | CFTC Rewrite | December 2024 | LIVE |
| Japan | JSCC CDM | June 2025 | Pending |
| Singapore | MAS | TBD | Following G7 |
| Hong Kong | HKMA | TBD | Following G7 |

**Search Patterns:**
- "Deutsche Bank AG" "EMIR Refit" CDM OR technology
- "Deutsche Bank AG" "CFTC Rewrite" OR "CFTC swap reporting"
- "Deutsche Bank AG" JSCC CDM connectivity
- "Deutsche Bank AG" UK EMIR derivatives reporting

**For each jurisdiction, document:**
- CDM Status: production / pilot / compliant_traditional / unknown
- Priority Level: primary / secondary / tertiary / unknown
- Approach: Internal / Vendor / Hybrid
- Confidence: percentage
- Knowledge Gap: Yes/No

**Jurisdiction Rollout Matrix:**
| Jurisdiction | CDM Status | Priority | Approach | Confidence | Knowledge Gap |
|--------------|------------|----------|----------|------------|---------------|
| EU | [status] | [priority] | [approach] | [X]% | [Yes/No] |
| UK | [status] | [priority] | [approach] | [X]% | [Yes/No] |
| US | [status] | [priority] | [approach] | [X]% | [Yes/No] |
| Japan | [status] | [priority] | [approach] | [X]% | [Yes/No] |

### 11c. Knowledge Gap Summary
Document areas where public research is exhausted but insider knowledge would be valuable:

| Gap ID | Category | Description | Impact | Suggested Source |
|--------|----------|-------------|--------|------------------|
| GAP-001 | product_coverage | [what's unknown] | [high/medium/low] | [interview target] |
| GAP-002 | jurisdiction | [what's unknown] | [high/medium/low] | [interview target] |

Include in assessment.md and update evidence.json with product_coverage and jurisdiction_rollout objects.

### 12. Status Update
Create/update outputs/phase-1-european-tier-1/deutsche-bank/status.json with:
- classification
- sub_classification
- confidence
- probability_architect
- stages_completed

## Key Research Questions
- Has Deutsche Bank announced any CDM/DRR pilot or production timeline?
- Is Deutsche Bank contributing to CDM development at ISDA or FINOS?
- How did Deutsche Bank address EMIR Refit (April 2024)?
- Are regulatory enforcement priorities consuming technology capacity?
- What do named individuals say about derivatives technology direction?

## Known Starting Evidence
- No prior evidence. Start from scratch.

## Evidence Output Format
For each piece of evidence found:

### Evidence [ID]
- **Source URL**: [exact URL]
- **Source Date**: [YYYY-MM-DD]
- **Claim Type**: [production_usage/pilot_or_poc/membership_or_participation/open_source_contribution/vendor_proxy_signal/hiring_signal]
- **Finding**: [what you found]
- **Excerpt**: "[relevant quote]"
- **Supports**: [ARCHITECT/PRAGMATIST/NEUTRAL]
- **Confidence**: [1-10]

---

Ready to begin? Start with Step 1 (Pre-Flight) and proceed through all steps.
