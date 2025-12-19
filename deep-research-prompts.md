# Deep Research Prompts for CDM/DRR International Bank Research

## How to Use This Document

1. **Execute each prompt in Deep Research** — one bank at a time or batch by phase
2. **Save outputs** for each bank
3. **Feed outputs to Claude Standard** using the Post-Research Analysis Template (at end of document)
4. **Apply Bayesian classification** and cross-bank validation

---

## Critical Context for All Prompts

Include this context block at the start of your first prompt in a session:

```
RESEARCH CONTEXT:

I'm researching international banks' positioning on CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) — ISDA's open-source data standard for derivatives.

KEY FACTS (anchor points — all findings must be consistent with these):
- BNP Paribas: First major bank in CDM production (Q3 2022)
- JPMorgan: CDM production announced October 2024
- JSCC (Japan Securities Clearing Corporation): CDM production June 2025
- Pictet: Confirmed in CDM production
- EMIR Refit: EU effective April 2024, UK effective September 2024
- Confirmed contributors: Standard Chartered, Barclays (FINOS)
- Delta Capita/Fragmos Chain: CDM-native utilities available

CLASSIFICATION FRAMEWORK:
- ARCHITECT: Actively building/contributing to CDM (Native/Leader/Follower variants)
- PRAGMATIST: Will adopt when necessary, not currently building (Vendor-dependent/Regulatory-driven variants)

I need EVIDENCE-BASED classification, not assumptions. Document what you found AND what you searched for but didn't find.
```

---

# PHASE 1: European Tier 1 Banks

## 1.1 Deutsche Bank

```
Research Deutsche Bank's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

SPECIFIC QUESTIONS TO ANSWER:
1. Has Deutsche Bank announced any CDM/DRR pilot or production timeline?
2. Is Deutsche Bank contributing to CDM development at ISDA or FINOS?
3. How did Deutsche Bank address EMIR Refit (April 2024)?
4. Are there named individuals at DB speaking about CDM/derivatives technology?
5. What vendor relationships exist for derivatives reporting?

CLAIM TO VALIDATE:
An earlier framework claimed Deutsche Bank has a "Pilot; production expected 2025" — find evidence confirming or refuting this.

SOURCES TO SEARCH:
- Deutsche Bank annual reports (2023, 2024) — technology sections
- Deutsche Bank investor presentations
- ISDA.org for Deutsche Bank mentions
- FINOS.org for Deutsche Bank contributions
- Risk.net, Waters Technology coverage of Deutsche Bank derivatives technology
- ISDA AGM speaker lists (2023, 2024, 2025)
- Job postings mentioning CDM or regulatory reporting
- BaFin (German regulator) communications

IMPORTANT: Document both what you FOUND and what you SEARCHED FOR BUT DIDN'T FIND. Absence of evidence in official sources is informative.

OUTPUT FORMAT:
1. Evidence inventory (source, date, finding, relevance)
2. Null results (what you searched for but didn't find)
3. Preliminary assessment with confidence level
4. Key uncertainties
```

---

## 1.2 Société Générale

```
Research Société Générale's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CRITICAL CONTEXT:
BNP Paribas (direct French competitor) went into CDM production in Q3 2022. French banks historically move as a cohort on regulatory technology. The key question is whether SocGen is following BNP's path.

SPECIFIC QUESTIONS TO ANSWER:
1. Has Société Générale announced any CDM/DRR initiatives?
2. Is there evidence of BNP → SocGen knowledge transfer or pattern following?
3. How did SocGen address EMIR Refit (April 2024)?
4. Are there named individuals at SocGen involved in CDM/ISDA working groups?
5. What is SocGen's derivatives technology direction?

HYPOTHESIS TO TEST:
"Société Générale is following BNP Paribas's CDM path with 12-24 month lag"

SOURCES TO SEARCH:
- Société Générale annual reports and investor presentations
- ISDA.org and FINOS.org for SocGen mentions
- Trade press coverage comparing French banks' approaches
- AMF/ACPR (French regulators) communications
- ISDA AGM speakers from SocGen
- Risk.net, Waters Technology articles
- French-language financial press if relevant

OUTPUT FORMAT:
1. Evidence inventory with BNP comparison where relevant
2. Null results
3. Assessment of "following BNP" hypothesis
4. Preliminary classification with confidence
5. Key uncertainties
```

---

## 1.3 UBS Group

```
Research UBS Group's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CRITICAL CONTEXT:
UBS acquired Credit Suisse in June 2023. Integration projected through 2026, ~90% complete as of October 2024. This is the largest banking merger in decades and may be consuming all technology investment capacity.

SPECIFIC QUESTIONS TO ANSWER:
1. Is there ANY evidence of CDM work at UBS despite the integration?
2. Did Credit Suisse have CDM initiatives that UBS may have inherited?
3. What are FINMA (Swiss regulator) requirements for derivatives reporting?
4. What is UBS's post-integration technology strategy for derivatives?
5. When will integration capacity constraints free up?

HYPOTHESIS TO TEST:
"Credit Suisse integration is consuming all CDM investment capacity through 2026"

SOURCES TO SEARCH:
- UBS annual reports and investor presentations (2023, 2024)
- UBS integration updates and technology announcements
- Credit Suisse historical CDM coverage (pre-acquisition)
- FINMA communications on derivatives reporting
- ISDA.org and FINOS.org for UBS/Credit Suisse mentions
- Risk.net, Waters Technology on UBS integration
- Swiss financial press

IMPORTANT: Search for BOTH UBS and historical Credit Suisse CDM evidence separately.

OUTPUT FORMAT:
1. UBS evidence inventory
2. Credit Suisse historical evidence inventory
3. Integration impact assessment
4. Null results
5. Preliminary classification with confidence
6. Key uncertainties (especially around post-integration trajectory)
```

---

## 1.4 Barclays

```
Research Barclays' CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CRITICAL CONTEXT:
Barclays is a CONFIRMED CDM contributor (FINOS). The question is NOT whether they're engaged, but HOW DEEPLY and whether they're moving toward production.

KNOWN EVIDENCE:
- FINOS contributor (confirmed)
- 2018 BOE/FCA DRR pilot participant
- Prototype demonstrated at industry events

SPECIFIC QUESTIONS TO ANSWER:
1. Is Barclays moving toward production commitment?
2. What is the scope and depth of their FINOS contribution?
3. Have they demonstrated production-grade capabilities?
4. Are they taking governance/leadership roles in CDM ecosystem?
5. How did they respond to UK EMIR (September 2024)?

UPGRADE CRITERIA TO ASSESS:
Does Barclays meet criteria to upgrade from "Follower" to "Leader"?
- Production commitment announced?
- Expanded beyond basic contribution?
- Governance/leadership role?
- Production demonstration (not just prototype)?
- Executive-level CDM endorsement?

SOURCES TO SEARCH:
- Barclays official announcements on CDM/DRR
- FINOS.org — Barclays contribution details, commits, working group participation
- FINOS GitHub for Barclays contributor activity
- ISDA AGM speakers and working groups
- FCA/BOE communications on DRR
- Risk.net, Waters Technology coverage
- Barclays job postings for CDM roles

OUTPUT FORMAT:
1. Evidence inventory organized by upgrade criteria
2. FINOS contribution depth assessment
3. UK EMIR response
4. Null results
5. Upgrade recommendation (Follower → Leader justified?)
6. Key uncertainties
```

---

## 1.5 HSBC

```
Research HSBC's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CRITICAL CONTEXT:
HSBC signed a contract with Delta Capita (CDM-native utility) in January 2025. The key question is whether HSBC is building internal CDM capability alongside this vendor relationship, or purely outsourcing.

KNOWN EVIDENCE:
- Delta Capita contract (January 2025)
- 2018 UK DRR pilot participant
- Global derivatives presence across UK, Asia, Americas

SPECIFIC QUESTIONS TO ANSWER:
1. Is HSBC building internal CDM capability in addition to Delta Capita?
2. Or is HSBC purely relying on vendor for CDM connectivity?
3. What is the scope of the Delta Capita engagement?
4. Did HSBC's 2018 pilot participation lead to sustained internal capability?
5. How do Asian regulatory requirements (HKMA, MAS) affect HSBC's approach?

CLASSIFICATION NUANCE:
- Building + vendor = ARCHITECT (vendor accelerates internal capability)
- Relying on vendor only = PRAGMATIST (vendor substitutes for internal capability)

SOURCES TO SEARCH:
- HSBC official announcements on CDM/DRR
- Delta Capita announcements about HSBC engagement
- HSBC annual reports — technology sections
- ISDA.org and FINOS.org for HSBC mentions
- HKMA, MAS communications on derivatives reporting
- Risk.net, Waters Technology coverage
- HSBC job postings for CDM/DRR roles
- UK FCA/BOE DRR pilot documentation

OUTPUT FORMAT:
1. Evidence inventory
2. Delta Capita relationship analysis (scope, role)
3. Internal capability evidence (or lack thereof)
4. 2018-2025 continuity assessment
5. Regional dimension (UK vs. Asia approach)
6. Null results
7. Preliminary classification with confidence
8. Key uncertainties
```

---

# PHASE 2: UK Regional Banks

## 2.1 NatWest Group

```
Research NatWest Group's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CONTEXT:
NatWest is a major UK bank with significant derivatives exposure. UK EMIR Refit became effective September 2024. Compare against UK peers Barclays and HSBC.

SPECIFIC QUESTIONS TO ANSWER:
1. Has NatWest announced any CDM/DRR initiatives?
2. How did NatWest address UK EMIR (September 2024)?
3. Is NatWest participating in ISDA/FINOS CDM work?
4. What is NatWest's derivatives technology strategy?
5. Any evidence of vendor relationships for regulatory reporting?

SOURCES TO SEARCH:
- NatWest annual reports and investor presentations
- ISDA.org and FINOS.org for NatWest mentions
- FCA communications
- Risk.net, Waters Technology coverage
- UK banking press
- NatWest job postings

OUTPUT FORMAT:
1. Evidence inventory
2. UK EMIR response
3. Comparison context vs. Barclays/HSBC
4. Null results
5. Preliminary classification with confidence
6. Key uncertainties
```

---

## 2.2 Lloyds Banking Group

```
Research Lloyds Banking Group's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CONTEXT:
Lloyds is primarily retail/commercial focused with lower derivatives exposure than investment banks. UK EMIR Refit effective September 2024.

SPECIFIC QUESTIONS TO ANSWER:
1. Has Lloyds announced any CDM/DRR initiatives?
2. What is Lloyds' derivatives exposure level (context for expected engagement)?
3. How did Lloyds address UK EMIR (September 2024)?
4. Any ISDA/FINOS participation?

NOTE: Lower derivatives exposure may justify lower CDM engagement — this is not necessarily a negative finding.

SOURCES TO SEARCH:
- Lloyds annual reports
- ISDA.org and FINOS.org
- FCA communications
- UK financial press

OUTPUT FORMAT:
1. Evidence inventory
2. Derivatives exposure context
3. Null results
4. Preliminary classification with confidence
5. Key uncertainties
```

---

# PHASE 3: Japanese Banks

## 3.1 Nomura Holdings

```
Research Nomura Holdings' CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CRITICAL CONTEXT:
JSCC (Japan Securities Clearing Corporation) went live with CDM in June 2025. This is the first CCP globally to be in CDM production. Banks clearing through JSCC face structural connectivity requirements. Nomura is a major JSCC clearing member.

SPECIFIC QUESTIONS TO ANSWER:
1. How is Nomura responding to JSCC CDM production?
2. Is Nomura building internal CDM capability or relying on connectivity wrapper?
3. What is JFSA (Japanese regulator) requiring for derivatives reporting?
4. Are there named executives discussing CDM/derivatives technology?
5. Any evidence at ISDA AGM Tokyo 2024?

CLASSIFICATION NUANCE:
- Building CDM-native infrastructure → ARCHITECT
- Minimum JSCC connectivity only → PRAGMATIST (Infrastructure-driven)
- Vendor-mediated connectivity → PRAGMATIST (Vendor-dependent)

SOURCES TO SEARCH:
- Nomura annual reports and investor materials
- JSCC announcements mentioning member readiness
- JFSA communications on derivatives reporting
- ISDA AGM Tokyo 2024 coverage
- ISDA.org for Nomura mentions
- Risk.net, Waters Technology Asia coverage
- Japanese financial press (English coverage)

OUTPUT FORMAT:
1. Evidence inventory
2. JSCC response assessment
3. Internal capability vs. connectivity wrapper evidence
4. Null results
5. Preliminary classification with confidence
6. Key uncertainties
```

---

## 3.2 MUFG (Mitsubishi UFJ Financial Group)

```
Research MUFG's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CONTEXT:
- MUFG is Japan's largest bank by assets
- Has Morgan Stanley alliance (potential technology sharing)
- JSCC CDM production June 2025 creates connectivity requirement

SPECIFIC QUESTIONS TO ANSWER:
1. How is MUFG responding to JSCC CDM production?
2. Is there any Morgan Stanley influence on derivatives technology approach?
3. Is MUFG building internal CDM capability?
4. Any ISDA/FINOS participation?
5. What is JFSA requiring?

SOURCES TO SEARCH:
- MUFG annual reports and investor presentations
- Morgan Stanley alliance technology announcements
- JSCC communications
- ISDA.org for MUFG mentions
- Japanese and international financial press

OUTPUT FORMAT:
1. Evidence inventory
2. Morgan Stanley technology sharing evidence
3. JSCC response assessment
4. Null results
5. Preliminary classification with confidence
6. Key uncertainties
```

---

## 3.3 Mizuho Financial Group

```
Research Mizuho Financial Group's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CONTEXT:
- Mizuho CEO delivered keynote at ISDA AGM Tokyo 2024 — significant executive engagement signal
- JSCC CDM production June 2025 creates connectivity requirement

SPECIFIC QUESTIONS TO ANSWER:
1. What did the Mizuho CEO say at ISDA AGM Tokyo 2024?
2. Does executive engagement translate to CDM investment?
3. How is Mizuho responding to JSCC CDM production?
4. Is Mizuho building internal CDM capability?
5. Any working group participation?

SOURCES TO SEARCH:
- ISDA AGM Tokyo 2024 coverage and presentations
- Mizuho annual reports
- JSCC communications
- ISDA.org for Mizuho mentions
- Japanese financial press

OUTPUT FORMAT:
1. Evidence inventory (especially ISDA AGM content)
2. Executive engagement assessment
3. JSCC response assessment
4. Null results
5. Preliminary classification with confidence
6. Key uncertainties
```

---

## 3.4 SMBC (Sumitomo Mitsui)

```
Research SMBC's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CONTEXT:
- Third Japanese megabank
- SMBC Nikko handles securities/derivatives
- JSCC CDM production June 2025

SPECIFIC QUESTIONS TO ANSWER:
1. How is SMBC responding to JSCC CDM production?
2. Is SMBC building internal CDM capability?
3. Any ISDA/FINOS participation?
4. Differentiation from Nomura, MUFG, Mizuho?

SOURCES TO SEARCH:
- SMBC and SMBC Nikko annual reports
- JSCC communications
- ISDA.org for SMBC mentions
- Japanese financial press

OUTPUT FORMAT:
1. Evidence inventory
2. JSCC response assessment
3. Comparison to other Japanese megabanks
4. Null results
5. Preliminary classification with confidence
6. Key uncertainties
```

---

# PHASE 4: Other European Banks

## 4.1 ING Group

```
Research ING Group's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CONTEXT:
Dutch bank subject to EMIR Refit (April 2024). Significant wholesale banking but not top-tier derivatives dealer.

SPECIFIC QUESTIONS TO ANSWER:
1. Has ING announced any CDM/DRR initiatives?
2. How did ING address EMIR Refit?
3. Any ISDA/FINOS participation?
4. What is ING's derivatives technology direction?

SOURCES TO SEARCH:
- ING annual reports
- ISDA.org and FINOS.org
- DNB (Dutch central bank) communications
- Risk.net, Waters Technology
- Dutch financial press

OUTPUT FORMAT:
1. Evidence inventory
2. EMIR Refit response
3. Null results
4. Preliminary classification with confidence
5. Key uncertainties
```

---

## 4.2 Crédit Agricole

```
Research Crédit Agricole's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CONTEXT:
Third major French bank after BNP Paribas and Société Générale. BNP is in CDM production since 2022. French banks may move as cohort.

SPECIFIC QUESTIONS TO ANSWER:
1. Has Crédit Agricole announced any CDM/DRR initiatives?
2. Is Crédit Agricole following BNP/SocGen pattern?
3. How did they address EMIR Refit?
4. Any ISDA/FINOS participation?

SOURCES TO SEARCH:
- Crédit Agricole annual reports
- ISDA.org and FINOS.org
- French regulatory communications
- French financial press
- Comparison coverage of French banks

OUTPUT FORMAT:
1. Evidence inventory
2. French bank cohort analysis
3. Null results
4. Preliminary classification with confidence
5. Key uncertainties
```

---

## 4.3 UniCredit

```
Research UniCredit's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CONTEXT:
Major Italian bank subject to EMIR Refit. Significant derivatives exposure.

SPECIFIC QUESTIONS TO ANSWER:
1. Has UniCredit announced any CDM/DRR initiatives?
2. How did UniCredit address EMIR Refit?
3. Any ISDA/FINOS participation?
4. What is UniCredit's derivatives technology direction?

SOURCES TO SEARCH:
- UniCredit annual reports
- ISDA.org and FINOS.org
- Consob/Bank of Italy communications
- Italian and European financial press

OUTPUT FORMAT:
1. Evidence inventory
2. EMIR Refit response
3. Null results
4. Preliminary classification with confidence
5. Key uncertainties
```

---

## 4.4 Commerzbank

```
Research Commerzbank's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CONTEXT:
Second major German bank after Deutsche Bank. Subject to EMIR Refit. Compare approach to Deutsche Bank.

SPECIFIC QUESTIONS TO ANSWER:
1. Has Commerzbank announced any CDM/DRR initiatives?
2. How did Commerzbank address EMIR Refit?
3. Any ISDA/FINOS participation?
4. How does approach compare to Deutsche Bank?

SOURCES TO SEARCH:
- Commerzbank annual reports
- ISDA.org and FINOS.org
- BaFin communications
- German financial press
- Comparison coverage with Deutsche Bank

OUTPUT FORMAT:
1. Evidence inventory
2. Deutsche Bank comparison
3. Null results
4. Preliminary classification with confidence
5. Key uncertainties
```

---

# PHASE 5: Spanish Banks

## 5.1 Santander

```
Research Banco Santander's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CONTEXT:
Largest Spanish bank, significant international presence. Subject to EMIR Refit.

SPECIFIC QUESTIONS TO ANSWER:
1. Has Santander announced any CDM/DRR initiatives?
2. How did Santander address EMIR Refit?
3. Any ISDA/FINOS participation?
4. What is Santander's derivatives technology direction?

SOURCES TO SEARCH:
- Santander annual reports
- ISDA.org and FINOS.org
- CNMV/Bank of Spain communications
- Spanish and international financial press

OUTPUT FORMAT:
1. Evidence inventory
2. EMIR Refit response
3. Null results
4. Preliminary classification with confidence
5. Key uncertainties
```

---

## 5.2 BBVA

```
Research BBVA's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CONTEXT:
Second major Spanish bank. Known for technology innovation. Subject to EMIR Refit.

SPECIFIC QUESTIONS TO ANSWER:
1. Has BBVA announced any CDM/DRR initiatives?
2. Given BBVA's technology focus, any CDM engagement?
3. How did BBVA address EMIR Refit?
4. Any ISDA/FINOS participation?

SOURCES TO SEARCH:
- BBVA annual reports and technology announcements
- ISDA.org and FINOS.org
- Spanish regulatory communications
- Spanish financial press

OUTPUT FORMAT:
1. Evidence inventory
2. Technology innovation vs. CDM engagement assessment
3. Null results
4. Preliminary classification with confidence
5. Key uncertainties
```

---

# PHASE 6: Confirmed Institution Deep Dives

## 6.1 Standard Chartered

```
Research Standard Chartered's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning in depth.

CRITICAL CONTEXT:
Standard Chartered is a CONFIRMED DRR contributor. Their contribution is notable because their derivatives business is smaller than typical contributors, suggesting strategic motivation.

KNOWN EVIDENCE:
- Confirmed DRR contributor
- Asia-Pacific focused
- Strong in trade finance

SPECIFIC QUESTIONS TO ANSWER:
1. What specifically has Standard Chartered contributed to CDM/DRR?
2. WHY is Standard Chartered contributing (strategic motivation)?
3. Are Asian regulatory requirements (MAS, HKMA) driving engagement?
4. Is there trade finance CDM interest beyond derivatives?
5. Who from Standard Chartered is involved?
6. Are they moving toward production?

HYPOTHESES TO TEST:
- H1: Strategic bet on CDM beyond immediate business need
- H2: Asian regulatory requirements driving engagement
- H3: Trade finance CDM applications motivating engagement

SOURCES TO SEARCH:
- Standard Chartered official announcements
- ISDA.org and FINOS.org — detailed contribution records
- FINOS GitHub for Standard Chartered commits
- MAS, HKMA communications
- Trade finance CDM coverage
- Risk.net, Waters Technology
- Standard Chartered job postings

OUTPUT FORMAT:
1. Detailed evidence inventory
2. Contribution depth assessment
3. Strategic motivation analysis
4. Asia regulatory driver assessment
5. Trade finance dimension
6. Named individuals
7. Preliminary classification with confidence
8. Key uncertainties
```

---

## 6.2 Pictet

```
Research Pictet Group's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning in depth.

CRITICAL CONTEXT:
Pictet is CONFIRMED to be in CDM production — one of only 4 firms globally. This is notable because Pictet is a Swiss private bank, not a major derivatives dealer.

KNOWN EVIDENCE:
- Confirmed in CDM production
- Swiss private bank
- Wealth management focused

SPECIFIC QUESTIONS TO ANSWER:
1. When did Pictet go into CDM production?
2. What is the scope of their CDM implementation?
3. WHY did a private bank pursue CDM production?
4. What competitive advantage are they seeking?
5. Who drove this decision?
6. How does this relate to their technology strategy?

SOURCES TO SEARCH:
- Pictet official announcements
- ISDA.org and FINOS.org for Pictet mentions
- Swiss financial press
- Wealth management technology coverage
- Risk.net, Waters Technology
- FINMA communications

NOTE: As a private bank, public information may be limited. Document what searches were attempted.

OUTPUT FORMAT:
1. Evidence inventory
2. Production timeline and scope
3. Strategic motivation analysis
4. Competitive positioning assessment
5. Null results (especially important for private bank)
6. Classification confirmation with confidence
7. Key uncertainties
```

---

# PHASE 7: Emerging Market Banks

## 7.1 DBS Bank

```
Research DBS Bank's CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

CONTEXT:
- Largest Southeast Asian bank
- Known for digital innovation
- Subject to MAS (Singapore) requirements
- May be influenced by JSCC CDM production for Japan-facing business

SPECIFIC QUESTIONS TO ANSWER:
1. Has DBS announced any CDM/DRR initiatives?
2. What is MAS requiring for derivatives reporting?
3. Is DBS building internal CDM capability?
4. How does DBS's digital innovation focus translate to CDM?
5. Any JSCC connectivity requirements?

SOURCES TO SEARCH:
- DBS annual reports and technology announcements
- MAS communications on derivatives reporting
- ISDA.org and FINOS.org
- Singapore financial press
- Risk.net Asia coverage

OUTPUT FORMAT:
1. Evidence inventory
2. MAS regulatory context
3. Digital innovation vs. CDM engagement assessment
4. Null results
5. Preliminary classification with confidence
6. Key uncertainties
```

---

## 7.2 Chinese Banks (Batch Research)

```
Research major Chinese banks' CDM (Common Domain Model) and DRR (Digital Regulatory Reporting) positioning.

BANKS TO COVER:
- ICBC (Industrial and Commercial Bank of China)
- China Construction Bank
- Bank of China
- Agricultural Bank of China

CONTEXT:
- Chinese banks have limited international derivatives exposure
- Domestic market uses different standards
- International subsidiaries may have different approach
- Limited public disclosure expected

SPECIFIC QUESTIONS TO ANSWER:
1. Do any Chinese banks participate in ISDA/FINOS CDM work?
2. What is CBIRC/PBoC approach to derivatives reporting standards?
3. Are international subsidiaries of Chinese banks engaged differently?
4. Any CDM mentions in English-language coverage?

NOTE: Expect limited evidence. Document search attempts thoroughly. "No evidence found" is an acceptable and informative outcome.

SOURCES TO SEARCH:
- ISDA.org and FINOS.org for Chinese bank mentions
- International financial press coverage
- Hong Kong subsidiary coverage
- Risk.net Asia coverage

OUTPUT FORMAT:
1. Evidence inventory (likely minimal)
2. Search attempts documented
3. Regulatory context
4. Null results (key output for this research)
5. Preliminary classification (likely "Unknown" or "Pragmatist-inferred")
6. Key uncertainties
```

---

# POST-RESEARCH ANALYSIS TEMPLATE

Use this template in **Claude Standard** after receiving Deep Research outputs:

```
I have research outputs from Deep Research on [BANK NAME]. Please help me apply the Bayesian classification framework.

RESEARCH OUTPUT:
[Paste Deep Research output here]

APPLY THIS ANALYSIS:

1. PRIOR PROBABILITY
- Base prior P(Architect) = 30%, P(Pragmatist) = 70%
- Apply contextual adjustments based on:
  - Derivatives exposure level
  - Regional peer behavior
  - Known regulatory pressure
  - Capacity constraints (if any)
- State adjusted prior

2. EVIDENCE CLASSIFICATION
For each piece of evidence found, classify:
- Tier (1=Official, 2=Industry, 3=Indirect, 4=Inference)
- Direction (Supports Architect / Supports Pragmatist / Neutral)
- Likelihood ratio (from standard table or estimate)

3. BAYESIAN UPDATE
- Calculate combined likelihood ratio
- Calculate posterior probability
- State final P(Architect) and P(Pragmatist)

4. CLASSIFICATION
Based on posterior:
- >80% Architect → ARCHITECT (determine variant)
- 50-80% Architect → ARCHITECT with reduced confidence
- 20-50% → UNCERTAIN
- <20% Architect → PRAGMATIST (determine variant)

5. ADVERSARIAL CHECK
- What is the strongest argument AGAINST this classification?
- Was disconfirming evidence searched for?
- Does the counter-argument have merit?
- Confidence adjustment needed?

6. CONFIDENCE CALIBRATION
Apply checklist:
- Highest evidence tier supporting classification
- Number of corroborating sources
- Contradictions present?
- Adversarial survival?
- State final confidence %

7. FINAL OUTPUT
- Classification: [POSTURE]-[Variant]
- Confidence: [X]%
- Key evidence: [Top 3 findings]
- Key uncertainties: [Top 2 gaps]
- Trajectory: [Accelerating/Stable/Stalled/Unknown]

8. FRAMEWORK INTEGRATION
- Recommendation: [Confirm/Revise/Add/Flag]
- Table entry: [Bank] | [Region] | [Posture] | [Variant] | [Status] | [Confidence]
```

---

# PHASE SYNTHESIS PROMPT

After completing all banks in a phase, use this in Claude Standard:

```
I have completed research on all banks in Phase [X]. Here are the individual assessments:

[Paste all bank assessments for the phase]

Please synthesize:

1. CLASSIFICATION DISTRIBUTION
- How many Architects vs. Pragmatists?
- What variants are represented?
- Is distribution reasonable?

2. REGIONAL PATTERNS
- Do banks cluster by geography?
- Is there a regional leader?
- What forcing functions are driving behavior?

3. CROSS-BANK CONSISTENCY
- Are similar banks classified similarly?
- Are there inconsistencies to resolve?
- Does the ordinal ranking make sense?

4. CONFIDENCE ASSESSMENT
- Average confidence across phase
- Where are the biggest gaps?
- Which banks need validation?

5. PATTERNS DISCOVERED
- What unexpected findings emerged?
- What hypotheses were confirmed/rejected?
- What should framework emphasize?

6. PROTOCOL ADJUSTMENTS
- What should change for next phase?
- Any search strategies that worked/failed?
```

---

# EXECUTION ORDER RECOMMENDATION

**Optimal sequence for 15-20 banks:**

Week 1:
- Day 1-2: Phase 1 (5 banks) — Highest priority, establishes patterns
- Day 3: Phase 1 synthesis and cross-validation

Week 2:
- Day 1: Phase 2 (2 banks) — UK completion
- Day 2: Phase 3 (4 banks) — Japan, JSCC-driven
- Day 3: Phase 2-3 synthesis

Week 3:
- Day 1: Phase 4 (4 banks) — Other European
- Day 2: Phase 5 (2 banks) — Spanish
- Day 3: Phase 4-5 synthesis

Week 4:
- Day 1: Phase 6 (2 banks) — Confirmed deep dives
- Day 2: Phase 7 (2-5 banks) — Emerging
- Day 3: Cross-bank pattern analysis and framework integration

**Total estimated time:** 60-80 hours research + 10-15 hours synthesis
