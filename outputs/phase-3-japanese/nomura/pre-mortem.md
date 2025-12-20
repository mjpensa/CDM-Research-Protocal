# Pre-Mortem Analysis: Nomura Holdings, Inc.
**Date**: 2025-12-19
**Institution**: Nomura Holdings, Inc.
**Prior Probability**: P(Architect) = 35%

## Failure Mode 1: False Positive (Claiming ARCHITECT when NOT)

### Scenario
We might conclude Nomura is an ARCHITECT contributor to CDM when they are merely:
- Using vendor solutions that implement CDM
- Participating in ISDA working groups without substantial CDM contribution
- Having their subsidiaries (Nomura Securities International, Instinet) use CDM passively

### Warning Signs
- Press releases about "digital transformation" or "derivatives modernization" without CDM specifics
- Generic ISDA membership without CDM-specific contributions
- Vendor partnerships (FIS, Bloomberg, MarkitWire) that handle CDM implementation
- Regulatory compliance mentions without active standards development

### Mitigation
- Require evidence of direct ISDA CDM working group participation
- Distinguish between CDM usage vs. CDM development/contribution
- Verify technical contributions (code, use cases, documentation) to CDM GitHub
- Separate Nomura's global operations from Japan-based CDM strategy

## Failure Mode 2: False Negative (Missing ARCHITECT Evidence)

### Scenario
We might miss Nomura's ARCHITECT status because:
- Japanese financial institutions publish primarily in Japanese
- CDM contributions under subsidiary names (Nomura Securities, Instinet)
- Contributions through Japanese industry consortiums (JSDA, JFSA initiatives)
- Technical work published in industry forums not indexed by standard search

### Warning Signs
- Limited English-language results despite HIGH derivatives relevance
- Strong JFSA engagement on derivatives regulation
- Known global derivatives trading volume but no CDM mentions
- Presence in major derivatives markets (US, Europe, Asia) suggesting operational need

### Mitigation
- Search for Japanese-language CDM initiatives
- Check subsidiary contributions separately
- Investigate Japanese Financial Services Agency (JFSA) CDM positions
- Review participation in regional standards bodies (ASIFMA, JSDA)
- Consider Nomura's acquisition of Lehman Brothers' Asian/European operations (2008) and legacy system modernization needs

## Decision Point
**Proceed to Evidence Gathering**: YES

Both failure modes are plausible given:
1. Nomura's HIGH derivatives relevance and global footprint
2. Japan's unique regulatory environment and language barrier
3. Limited public information on Japanese institutions' CDM strategies
4. Need to distinguish between vendor usage and active contribution

The 35% prior probability acknowledges significant uncertainty. Evidence gathering will be critical to reach an informed classification.
