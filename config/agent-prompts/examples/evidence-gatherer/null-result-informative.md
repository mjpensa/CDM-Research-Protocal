# Example: Null Result Documentation (Informative Absence)

## Context

Tier 1 evidence gathering for Standard Chartered. This example shows how to document null results that are informationally meaningful.

## Bank Configuration

- **Bank**: Standard Chartered
- **Headquarters**: London, UK
- **Domain**: sc.com
- **Regulator**: FCA, PRA

---

## Null Result Block 1: Official Bank Announcements

```markdown
NULL RESULT BLOCK

Search Category: Tier 1 Official Bank Announcements
Queries Executed:
1. "Standard Chartered" "Common Domain Model" site:sc.com
2. "Standard Chartered" CDM derivatives announcement
3. "Standard Chartered" CDM production regulatory
4. site:sc.com CDM "regulatory reporting"
5. "Standard Chartered" ISDA CDM implementation

Results Reviewed: 45
Relevant Findings: 0

Null Classification:
[X] NO_RESULTS - Search returned no results for CDM
[ ] IRRELEVANT - Results exist but none relevant to CDM/DRR
[ ] PAYWALLED - Results exist but behind paywall
[ ] OUTDATED_ONLY - Only found results >3 years old

Null Explanation: No results found on sc.com or in press for Standard Chartered CDM adoption. General technology and digital banking announcements exist but no CDM-specific content.

Informative Absence Assessment:
Would we EXPECT to find evidence in this category if bank were ARCHITECT?
[YES]

If YES: This absence SUPPORTS PRAGMATIST
Because: ARCHITECT-level banks typically issue press releases about CDM initiatives. Tier 1 European banks (HSBC, Barclays, Deutsche) with CDM programs have official announcements. Absence suggests no CDM program to announce.
---
```

## Null Result Block 2: Annual Reports

```markdown
NULL RESULT BLOCK

Search Category: Tier 1 Annual Report / Investor Materials
Queries Executed:
1. "Standard Chartered" annual report 2024 CDM
2. "Standard Chartered" annual report 2024 "Common Domain Model"
3. "Standard Chartered" investor presentation 2024 derivatives technology
4. site:sc.com annual-report CDM
5. "Standard Chartered" strategic report technology derivatives

Results Reviewed: 12
Relevant Findings: 0

Null Classification:
[X] IRRELEVANT - Results exist but none relevant to CDM/DRR
[ ] NO_RESULTS - Search returned no results
[ ] PAYWALLED - Results exist but behind paywall
[ ] OUTDATED_ONLY - Only found results >3 years old

Null Explanation: Annual reports and investor materials found but contain no CDM references. Technology sections mention "digital transformation" and "platform modernization" but no CDM or ISDA standards specifically.

Informative Absence Assessment:
Would we EXPECT to find evidence in this category if bank were ARCHITECT?
[YES / UNCLEAR]

If UNCLEAR: This absence is WEAKLY SUPPORTS PRAGMATIST
Because: Not all banks mention CDM in investor materials. However, strategic technology initiatives typically appear in annual reports. Absence is mildly informative but not conclusive.
---
```

## Null Result Block 3: ISDA/FINOS Official

```markdown
NULL RESULT BLOCK

Search Category: Tier 1 ISDA/FINOS Official Participation
Queries Executed:
1. site:isda.org "Standard Chartered" CDM
2. site:finos.org "Standard Chartered"
3. site:github.com/finos "Standard Chartered" CDM
4. "Standard Chartered" ISDA working group CDM
5. "Standard Chartered" FINOS member CDM

Results Reviewed: 25
Relevant Findings: 0

Null Classification:
[X] NO_RESULTS - Search returned no results
[ ] IRRELEVANT - Results exist but none relevant to CDM/DRR
[ ] PAYWALLED - Results exist but behind paywall
[ ] OUTDATED_ONLY - Only found results >3 years old

Null Explanation: No ISDA or FINOS official mentions of Standard Chartered in CDM context. Bank is ISDA member but no CDM working group participation found.

Informative Absence Assessment:
Would we EXPECT to find evidence in this category if bank were ARCHITECT?
[YES]

If YES: This absence SUPPORTS PRAGMATIST
Because: ARCHITECT banks typically have ISDA/FINOS participation documented. BNP Paribas, Goldman Sachs, and other ARCHITECT banks appear in CDM working group announcements. Absence is informative.
---
```

---

## Null Results JSON Output

```json
{
  "null_results": [
    {
      "category": "Tier 1 Official Bank Announcements",
      "queries": [
        "\"Standard Chartered\" \"Common Domain Model\" site:sc.com",
        "\"Standard Chartered\" CDM derivatives announcement",
        "\"Standard Chartered\" CDM production regulatory",
        "site:sc.com CDM \"regulatory reporting\"",
        "\"Standard Chartered\" ISDA CDM implementation"
      ],
      "results_reviewed": 45,
      "null_type": "NO_RESULTS",
      "informative_absence": true,
      "expected_if_architect": true,
      "implication": "SUPPORTS_PRAGMATIST",
      "rationale": "ARCHITECT banks typically issue CDM announcements. Absence suggests no program."
    },
    {
      "category": "Tier 1 Annual Report / Investor Materials",
      "queries": [
        "\"Standard Chartered\" annual report 2024 CDM",
        "\"Standard Chartered\" annual report 2024 \"Common Domain Model\"",
        "\"Standard Chartered\" investor presentation 2024 derivatives technology"
      ],
      "results_reviewed": 12,
      "null_type": "IRRELEVANT",
      "informative_absence": true,
      "expected_if_architect": false,
      "implication": "WEAKLY_SUPPORTS_PRAGMATIST",
      "rationale": "Not all banks mention CDM in investor materials. Weakly informative."
    },
    {
      "category": "Tier 1 ISDA/FINOS Official Participation",
      "queries": [
        "site:isda.org \"Standard Chartered\" CDM",
        "site:finos.org \"Standard Chartered\"",
        "site:github.com/finos \"Standard Chartered\" CDM"
      ],
      "results_reviewed": 25,
      "null_type": "NO_RESULTS",
      "informative_absence": true,
      "expected_if_architect": true,
      "implication": "SUPPORTS_PRAGMATIST",
      "rationale": "ARCHITECT banks have documented ISDA/FINOS participation. Absence informative."
    }
  ]
}
```

---

## Tier 1 Null Summary

| Category | Null Type | Informative? | Implication |
|----------|-----------|--------------|-------------|
| Official Announcements | NO_RESULTS | Yes | SUPPORTS_PRAGMATIST |
| Annual Reports | IRRELEVANT | Weak | WEAKLY_SUPPORTS_PRAGMATIST |
| ISDA/FINOS | NO_RESULTS | Yes | SUPPORTS_PRAGMATIST |

**Combined Null Evidence LR**: 0.21 (strong informative absence)

**Interpretation**: The absence of CDM evidence across all Tier 1 categories is informationally significant. Standard Chartered shows pattern consistent with PRAGMATIST hypothesis.

**Next Steps**: Proceed to Tier 2 to search for indirect signals before classifying.
