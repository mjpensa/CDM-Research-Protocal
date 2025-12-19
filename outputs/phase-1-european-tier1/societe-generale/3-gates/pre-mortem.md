# Pre-Mortem Gate: Societe Generale

**Bank**: Societe Generale
**Headquarters**: Paris, France
**Primary Regulator**: AMF/ACPR
**Phase**: 1 (European Tier 1)
**Execution Tier**: A (Full protocol)
**Date**: 2025-12-19

---

## Prior Probability Assessment

**P(Architect) = 45%**

Composition:
- Base prior: 25%
- Derivatives-dominant adjustment: +10% (Global equity derivatives leader)
- Regional peer architect (BNP Paribas CDM production Q3 2022): +10%

---

## Failure Mode Analysis

### 1. Insufficient Public Information

**Risk Level**: HIGH

**Why SocGen May Not Disclose CDM-Related Activities**:

- **Competitive Sensitivity**: SocGen's equity derivatives business is a key differentiator and profit center. Any technology investments that provide operational alpha may be deliberately undisclosed
- **French Corporate Culture**: French banks tend toward more conservative external communications about technology initiatives compared to US or UK peers
- **Internal vs External Focus**: Eric Litvack's ISDA chairmanship (2015-2024) provided significant industry influence without requiring SocGen to publicly announce CDM participation
- **Follow-Not-Lead Strategy**: If SocGen is intentionally following BNP Paribas at a lag, they may avoid announcements until implementation is mature
- **No Direct CDM Production Evidence**: Unlike BNP Paribas (November 2022 DRR announcement), SocGen has made no public CDM-related press releases

**Mitigation**: Seek indirect evidence through ISDA working group participation, technology vendor partnerships (Capitolis, REGnosys), and regulatory filing technology mentions.

---

### 2. Misleading Evidence

**Risk Level**: HIGH

**BNP Comparison Creating False Inference**:

- **Assumption Risk**: The hypothesis assumes SocGen follows BNP Paribas patterns. However:
  - BNP Paribas emphasized regulatory reporting efficiency (CFTC rewrite)
  - SocGen may prioritize different use cases (equity derivatives structuring, prime brokerage)
  - Different strategic priorities despite similar market positions

- **Eric Litvack ISDA Chairmanship Overinterpretation**:
  - 10-year ISDA chairmanship (2015-2024) shows derivatives industry engagement
  - Does NOT necessarily indicate SocGen internal CDM adoption
  - ISDA role is industry governance, not firm technology implementation

- **SG-FORGE Digital Assets Distraction**:
  - Strong evidence of blockchain/tokenization innovation (EURCV, USDCV stablecoins, digital bonds)
  - Digital asset innovation is NOT equivalent to CDM adoption
  - May indicate alternative technology investment priorities

- **Capitolis Partnership Misattribution**:
  - SocGen partnership with Capitolis for derivatives novations automation (2025)
  - Capitolis uses proprietary algorithms, NOT CDM
  - Operational automation does not equal standards adoption

**Mitigation**: Distinguish between general "derivatives technology innovation" and specific "CDM/DRR implementation" evidence. Require explicit CDM mentions, not inference.

---

### 3. Outdated Information

**Risk Level**: MODERATE

**Temporal Concerns**:

- **Eric Litvack Transition**: Stepped down as ISDA Chair December 2024. SocGen's influence on ISDA CDM direction may shift with Jeroen Krens (Citigroup) taking over
- **EMIR Refit Timeline**: EU EMIR Refit effective April 2024, UK EMIR Refit October 2024. Evidence pre-dating these deadlines may not reflect current state
- **BNP Paribas Reference Point**: BNP's CDM production was November 2022 - now 2+ years ago. The "12-24 month lag" hypothesis window has partially closed
- **Rapid Technology Evolution**: Generative AI strategy announced at AI for Finance 2024 (Paris) may indicate pivot to AI-first approach over standards-based approach
- **SG-FORGE Maturation**: 2023-2025 acceleration of digital asset activities may have absorbed innovation budget

**Mitigation**: Weight 2024-2025 evidence more heavily. Seek current-state indicators over historical announcements.

---

### 4. Confirmation Bias

**Risk Level**: HIGH

**How Regional Peer Assumption Might Skew Search**:

- **French Bank Homogeneity Assumption**: Treating French Tier 1 banks (BNP, SocGen, Credit Agricole) as technologically homogeneous ignores:
  - Different business mixes (SocGen: equity derivatives; BNP: global corporate banking)
  - Different technology heritage and architecture
  - Different strategic priorities and competitive positioning

- **"Lag Follower" Framing**:
  - Hypothesis pre-supposes SocGen is "following" BNP
  - May miss evidence that SocGen is pursuing alternative paths
  - Could overlook evidence of PRAGMATIST positioning

- **ISDA Leadership = CDM Champion Assumption**:
  - Eric Litvack's role may lead to assumption SocGen is CDM-forward
  - His responsibilities were industry-wide, not SocGen-specific
  - LIBOR transition and margin rules were priorities, not necessarily CDM

- **Search Term Selection Bias**:
  - Searches designed to find CDM evidence may miss PRAGMATIST indicators
  - "No CDM evidence" could be misinterpreted as "insufficient search" rather than "genuine absence"

**Mitigation**: Actively search for evidence of alternative approaches. Give equal weight to null results as disconfirming evidence.

---

## Difficulty Assessment

**Research Difficulty**: MODERATE-HIGH

**Factors**:
| Factor | Assessment | Impact |
|--------|------------|--------|
| Public disclosure culture | Conservative | High difficulty |
| English-language sources | Mixed (some French-only) | Moderate difficulty |
| ISDA leadership connection | Strong | May ease discovery |
| Recent press activity | High (SG-FORGE, Bernstein JV) | Low difficulty for digital |
| CDM-specific disclosure | Absent | High difficulty |
| Regulatory filing accessibility | Moderate (AMF filings) | Moderate difficulty |

**Overall Assessment**: Difficulty is elevated because SocGen has strong derivatives technology activity but no specific CDM mentions. The absence may be real (PRAGMATIST) or reflect disclosure preferences (undisclosed ARCHITECT).

---

## Success Criteria

### Criterion 1: Direct CDM Reference
**Description**: Find explicit mention of "Common Domain Model," "CDM," or "Digital Regulatory Reporting" in SocGen official communications, presentations, or job postings
**Threshold**: At least 1 verifiable source with explicit CDM/DRR terminology attributed to SocGen
**Outcome if Met**: Strong ARCHITECT signal; revise P(Architect) upward by +15-20%

### Criterion 2: Named Individual in ISDA CDM Working Groups
**Description**: Identify SocGen employee (beyond Eric Litvack) participating in ISDA CDM, Digital Assets, or DRR working groups
**Threshold**: Named individual with SocGen affiliation on ISDA CDM-related committee or contributor list
**Outcome if Met**: Moderate ARCHITECT signal; confirms institutional commitment beyond former chairman

### Criterion 3: Technology Vendor Partnership for CDM/DRR
**Description**: Find evidence of SocGen partnership with CDM ecosystem vendors (REGnosys, Rosetta, FINOS contributors) for regulatory reporting
**Threshold**: Press release, case study, or job posting referencing CDM-related vendor engagement
**Outcome if Met**: Strong ARCHITECT signal; indicates active implementation

---

## Null Hypothesis

**Statement**: Societe Generale is a PRAGMATIST institution that has NOT adopted CDM and is addressing regulatory requirements (EMIR Refit) through traditional vendor solutions or internal development.

**Supporting Indicators**:
- No direct CDM mentions found in Tier 1 searches
- No SocGen presence on FINOS CDM contributor list
- Alternative innovation focus on SG-FORGE (digital assets) rather than derivatives standardization
- Capitolis partnership focuses on proprietary novations algorithms, not open standards
- EMIR compliance page describes obligations but not implementation technology

**Evidence Required to Reject Null**: Meeting any of the 3 success criteria above would provide sufficient evidence to reject the null hypothesis.

---

## Gate Decision

**Status**: PROCEED TO TIER 2

**Rationale**:
- Tier 1 searches yielded significant contextual evidence but no direct CDM confirmation
- High prior probability (45%) and BNP Paribas regional peer pattern warrant deeper investigation
- Eric Litvack ISDA connection provides a reasonable path for Tier 2 LinkedIn/personnel searches
- Absence of FINOS participation is a notable negative signal requiring explanation
- Pre-mortem analysis identifies clear risks that Tier 2 can address

**Tier 2 Priority Searches**:
1. LinkedIn search for SocGen employees with CDM/DRR in profiles
2. ISDA working group participant lists for SocGen representation
3. REGnosys/Rosetta client references for French banks
4. French-language regulatory technology announcements
5. SocGen Annual Report technology investment sections

---

*Pre-Mortem Gate completed: 2025-12-19*
