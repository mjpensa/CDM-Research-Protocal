# Implementation Strategy: Fixes 1-8

**Created**: 2025-12-19
**Purpose**: Phased implementation plan to address inefficiencies, redundancies, and trustworthiness gaps in the CDM Research Protocol.

---

## Executive Summary

You already have **significant infrastructure** in place. The strategy is to **extend existing tools** rather than rebuild, and use a **phased approach** that delivers value at each stage.

---

## The 8 Fixes Being Addressed

| # | Fix | Priority | Effort |
|---|-----|----------|--------|
| 1 | Create integration layer connecting agents to tools | High | High |
| 2 | Implement automated Bayesian validation in Python | High | Medium |
| 3 | Add schema validation for markdown outputs | High | Medium |
| 4 | Centralize all thresholds in decision-thresholds.json | High | Low |
| 5 | Add LR independence checker | Medium | Medium |
| 6 | Implement real-time URL validation for Evidence Gatherer | Medium | Medium |
| 7 | Build automated QA validator in Python | Medium | Medium |
| 8 | Fix deprecated terminology in existing outputs | High | Low |

---

## What Already Exists (Good News!)

| Fix # | Requirement | Existing Tool | Gap |
|-------|-------------|---------------|-----|
| **4** | Centralize thresholds | `tools/config_loader.py` | Agent prompts still hardcode values |
| **7** | QA validator in Python | `tools/cross_bank_validator.py` | Missing 5 consistency tests from qa-validator.md |
| **8** | Fix deprecated terminology | `tools/migrate_terminology.py` | Just needs to be run |
| **3** | Parse markdown | `tools/markdown_to_json.py` | Only handles evidence, not gates/bayesian |
| **6** | URL validation | `tools/process_evidence.py` | Only post-hoc, not real-time |

---

## Dependency Graph

```
                    ┌────────────────────────────┐
                    │  FIX 4: Centralize Config  │ ◄── Do First (Foundation)
                    └─────────────┬──────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ FIX 8: Migrate  │    │ FIX 3: MD Schema│    │ FIX 6: RT URL   │
│ Terminology     │    │ Validation      │    │ Validation      │
└─────────────────┘    └────────┬────────┘    └─────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
          ┌─────────────────┐    ┌─────────────────┐
          │ FIX 2: Bayesian │    │ FIX 5: LR       │
          │ Validation      │◄───│ Independence    │
          └────────┬────────┘    └─────────────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ FIX 7: Enhanced │
          │ QA Validator    │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ FIX 1: Full     │ ◄── Do Last (Depends on all others)
          │ Integration     │
          └─────────────────┘
```

---

## Phased Implementation Plan

### **Phase 0: Quick Wins** (1-2 hours)
*Immediate value, no code changes needed*

| Task | Command | Result |
|------|---------|--------|
| Run terminology migration | `python tools/migrate_terminology.py outputs/ --apply` | Fix #8 complete |
| Run cross-bank validation | `python tools/cross_bank_validator.py outputs/` | See current issues |
| Test config_loader | `python tools/config_loader.py` | Verify config works |

**Deliverable**: Clean data, baseline validation report

---

### **Phase 1: Centralize Configuration** (2-3 hours)
*Complete Fix #4*

#### 1.1 Create threshold reference file for agents

Create `config/agent-config-reference.md` that agents can read:

```markdown
# Agent Configuration Reference
Generated from config/decision-thresholds.json

## Thresholds (DO NOT HARDCODE - reference this file)
- Skip to adversarial: 80%
- Low confidence block: 50%
- Uncertainty range: 40-60%
- Confidence caps: T1=95%, T2=75%, T3=50%, T4=35%
```

#### 1.2 Update agent prompts

Replace hardcoded values with references:

```markdown
# Before (in orchestrator.md)
"P(Architect) > 80%"

# After
"P(Architect) > skip_threshold (see config/decision-thresholds.json)"
```

#### 1.3 Create agent config injector

New tool: `tools/inject_agent_config.py`
- Reads agent prompt templates
- Injects current threshold values
- Outputs ready-to-use prompts

**Deliverable**: Single source of truth for all thresholds

---

### **Phase 2: Markdown Schema Validation** (4-6 hours)
*Complete Fix #3*

#### 2.1 Create markdown parsers

New file: `tools/markdown_parser.py`

```python
# Parsers for each output type:
def parse_evidence_block(text: str) -> dict
def parse_bayesian_update(text: str) -> dict
def parse_gate_output(text: str) -> dict
def parse_adversarial_verdict(text: str) -> dict
```

#### 2.2 Create validation schemas

New file: `templates/markdown-schemas.json`

```json
{
  "evidence_block": {
    "required_fields": ["id", "tier", "source", "date", "finding", "quality_assessment"],
    "patterns": {...}
  },
  "bayesian_update": {
    "required_sections": ["Prior", "Evidence This Tier", "Combined LR", "Posterior"],
    "must_contain_math": true
  }
}
```

#### 2.3 Integrate into run_pipeline.py

Add validation step after markdown is written, before JSON conversion.

**Deliverable**: Automated validation that catches malformed agent outputs

---

### **Phase 3: Bayesian Validation Engine** (6-8 hours)
*Complete Fixes #2 and #5*

#### 3.1 Build Python Bayesian calculator

New file: `tools/bayesian_calculator.py`

```python
class BayesianCalculator:
    def __init__(self, lr_tables_path: str):
        self.lr_tables = load_json(lr_tables_path)

    def calculate_posterior(
        self,
        prior: float,
        evidence_items: list[dict]
    ) -> BayesianResult:
        """
        Returns:
        - posterior_probability
        - combined_lr
        - per_evidence_lr
        - warnings (extreme LR, independence issues)
        """

    def check_independence(self, items: list[dict]) -> list[str]:
        """Flag evidence from same source"""

    def validate_agent_calculation(
        self,
        agent_output: dict,
        evidence: list[dict]
    ) -> ValidationResult:
        """Compare agent's math to Python calculation"""
```

#### 3.2 Add LR independence checker (Fix #5)

Within `bayesian_calculator.py`:

```python
def check_independence(self, items: list[dict]) -> list[str]:
    warnings = []

    # Check 1: Same URL
    urls = [i.get('source_url') for i in items]
    if len(urls) != len(set(urls)):
        warnings.append("DUPLICATE_URL: Same URL counted multiple times")

    # Check 2: Same domain for high-weight evidence
    domains = [extract_domain(i.get('source_url')) for i in items]
    domain_counts = Counter(domains)
    for domain, count in domain_counts.items():
        if count > 2:
            warnings.append(f"DOMAIN_CONCENTRATION: {count} items from {domain}")

    # Check 3: Causal linkage (vendor + vendor confirmation)
    # ...

    return warnings
```

#### 3.3 Integrate validation into pipeline

Add to `run_pipeline.py`:

```python
# After markdown_to_json conversion
from bayesian_calculator import BayesianCalculator

calc = BayesianCalculator(lr_tables_path)
result = calc.validate_agent_calculation(
    agent_output=parsed_bayesian_md,
    evidence=evidence_items
)

if result.discrepancy > 0.05:  # >5% difference
    logger.warning(f"Bayesian validation failed: agent={result.agent_value}, calculated={result.calculated_value}")
```

**Deliverable**: Python-verified Bayesian calculations, independence checking

---

### **Phase 4: Real-Time URL Validation** (3-4 hours)
*Complete Fix #6*

#### 4.1 Create lightweight URL checker

New file: `tools/url_validator.py`

```python
class URLValidator:
    def __init__(self, cache_path: str = None):
        self.cache = load_cache(cache_path)  # Cache results for session

    def check_url(self, url: str, quick: bool = True) -> URLStatus:
        """
        quick=True: HEAD request only (fast)
        quick=False: Full GET with content hash
        """

    def check_batch(self, urls: list[str]) -> dict[str, URLStatus]:
        """Parallel checking with rate limiting"""
```

#### 4.2 Integrate with evidence gathering

Create `tools/evidence_helper.py` that agents can conceptually use:

```python
# This provides real-time feedback during evidence gathering
def validate_evidence_block(block: dict) -> ValidationResult:
    """
    Called after each evidence block is written.
    Returns immediate feedback on URL status.
    """
    url_status = url_validator.check_url(block['source_url'], quick=True)

    if url_status == 'dead':
        return ValidationResult(
            valid=False,
            message=f"URL appears dead. Check Wayback: {wayback_url}"
        )
```

#### 4.3 Add to pipeline as optional step

```bash
python run_pipeline.py outputs/bank/ --validate-urls-first
```

**Deliverable**: Early detection of dead links, reduced wasted effort

---

### **Phase 5: Enhanced QA Validator** (4-6 hours)
*Complete Fix #7*

#### 5.1 Extend cross_bank_validator.py

Add the 5 consistency tests from `config/agent-prompts/qa-validator.md`:

```python
def check_ordinal_ranking(statuses: dict) -> list:
    """If Bank A has stronger evidence on every dimension, A must rank >= B"""

def check_similar_profiles(statuses: dict, manifest: dict) -> list:
    """Banks with similar business models should have similar classifications"""

def check_evidence_confidence_correlation(statuses: dict) -> list:
    """More/higher-tier evidence should correlate with higher confidence"""

def check_classification_distribution(statuses: dict) -> list:
    """Distribution should match priors (~30% Architect, ~70% Pragmatist)"""

def check_anchor_points(statuses: dict, anchors: dict) -> list:
    """No classification can violate immutable facts"""
```

#### 5.2 Add anchor point validation

Create `config/anchor-points.json`:

```json
{
  "production_banks": ["bnp-paribas", "jpmorgan", "jscc", "pictet"],
  "first_major_bank": {"id": "bnp-paribas", "date": "2022-Q3"},
  "confirmed_contributors": ["barclays", "standard-chartered"],
  "emir_refit_dates": {
    "eu": "2024-04",
    "uk": "2024-09"
  }
}
```

#### 5.3 Create QA report generator

```python
def generate_qa_report(phase: int) -> str:
    """Generate qa/phase-N-consistency.md"""
```

**Deliverable**: Automated cross-bank consistency checking matching qa-validator.md

---

### **Phase 6: Full Integration Layer** (8-12 hours)
*Complete Fix #1*

#### 6.1 Create master orchestration script

New file: `tools/research_runner.py`

```python
class ResearchRunner:
    """
    End-to-end research execution for a single bank.

    Stages:
    1. Load bank config from manifest
    2. Execute evidence gathering (via agent prompt + web search)
    3. Convert markdown to JSON
    4. Validate markdown structure
    5. Run Bayesian calculator
    6. Validate against agent's Bayesian output
    7. Execute gates (via agent prompt)
    8. Execute adversarial (via agent prompt)
    9. Run trust audit
    10. Generate synthesis
    11. Run QA validation
    12. Render final report
    """

    def run_bank(self, bank_id: str, phase: int) -> ResearchResult:
        """Execute full pipeline for one bank"""

    def run_phase(self, phase: int) -> PhaseResult:
        """Execute all banks in a phase with QA"""
```

#### 6.2 Create agent execution wrapper

```python
class AgentExecutor:
    """
    Wrapper that:
    1. Loads agent prompt from config/agent-prompts/
    2. Injects current config values
    3. Executes agent (this is where Claude API would be called)
    4. Captures output
    5. Validates output structure
    6. Writes to correct location
    """

    def execute_evidence_gatherer(self, bank_id: str, tier: int) -> Path:
        """Returns path to generated tier{N}-evidence.md"""

    def execute_bayesian_analyst(self, bank_id: str, tier: int) -> Path:
        """Returns path to generated post-tier{N}-update.md"""
```

#### 6.3 Connect everything

```
research_runner.py
    │
    ├── AgentExecutor
    │   ├── Reads agent prompts
    │   ├── Injects config
    │   └── Validates outputs
    │
    ├── markdown_parser.py
    │   └── Converts agent markdown to structured data
    │
    ├── bayesian_calculator.py
    │   ├── Validates agent math
    │   └── Checks independence
    │
    ├── url_validator.py
    │   └── Validates URLs in evidence
    │
    ├── trust_audit.py
    │   └── Calculates trust metrics
    │
    ├── cross_bank_validator.py
    │   └── Runs consistency checks
    │
    └── render_report.py
        └── Generates final output
```

**Deliverable**: Single command to run complete research pipeline

---

## Implementation Timeline

| Phase | Effort | Dependencies | Can Parallelize? |
|-------|--------|--------------|------------------|
| Phase 0 | 1-2 hours | None | N/A (do first) |
| Phase 1 | 2-3 hours | Phase 0 | No |
| Phase 2 | 4-6 hours | Phase 1 | Yes with Phase 4 |
| Phase 3 | 6-8 hours | Phase 2 | No |
| Phase 4 | 3-4 hours | Phase 1 | Yes with Phase 2 |
| Phase 5 | 4-6 hours | Phase 3 | No |
| Phase 6 | 8-12 hours | All others | No |

**Total estimated effort**: 28-41 hours

### Parallel Execution Path

```
Phase 0 → Phase 1 → ┬→ Phase 2 → Phase 3 → Phase 5 → Phase 6
                    └→ Phase 4 ────────────────────────┘
```

### Minimum Viable Path (if time-constrained)

```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 6 (minimal)
```

---

## Recommended Execution Order

1. **Start today**: Phase 0 (quick wins)
2. **Next session**: Phase 1 + start Phase 2
3. **Following session**: Complete Phase 2 + Phase 4 in parallel
4. **Next**: Phase 3 (depends on Phase 2)
5. **Then**: Phase 5 (depends on Phase 3)
6. **Finally**: Phase 6 (integration)

---

## Testing Strategy

Each phase should include:

1. **Unit tests** for new functions
2. **Integration test** using one bank (e.g., Deutsche Bank)
3. **Regression test** ensuring existing outputs still validate

```bash
# After each phase
python tools/run_pipeline.py outputs/phase-1-european-tier1/deutsche-bank/ --validate-only
python tools/cross_bank_validator.py outputs/
```

---

## Files to Create

| Phase | New File | Purpose |
|-------|----------|---------|
| 1 | `config/agent-config-reference.md` | Threshold reference for agents |
| 1 | `tools/inject_agent_config.py` | Inject config into agent prompts |
| 2 | `tools/markdown_parser.py` | Parse agent markdown outputs |
| 2 | `templates/markdown-schemas.json` | Validation schemas |
| 3 | `tools/bayesian_calculator.py` | Python Bayesian engine |
| 4 | `tools/url_validator.py` | Real-time URL checking |
| 4 | `tools/evidence_helper.py` | Evidence validation helpers |
| 5 | `config/anchor-points.json` | Immutable anchor facts |
| 6 | `tools/research_runner.py` | Master orchestration |

---

## Files to Modify

| Phase | Existing File | Changes |
|-------|---------------|---------|
| 1 | `config/agent-prompts/*.md` | Replace hardcoded thresholds |
| 2 | `tools/run_pipeline.py` | Add markdown validation step |
| 3 | `tools/run_pipeline.py` | Add Bayesian validation step |
| 4 | `tools/run_pipeline.py` | Add URL pre-validation option |
| 5 | `tools/cross_bank_validator.py` | Add 5 consistency tests |
| 6 | `tools/orchestrate.py` | Connect to research_runner |

---

## Success Criteria

### Phase 0
- [ ] No deprecated terminology in outputs
- [ ] cross_bank_validator.py runs without errors

### Phase 1
- [ ] All agent prompts reference config files, not hardcoded values
- [ ] Changing decision-thresholds.json propagates to agents

### Phase 2
- [ ] Malformed markdown is detected before pipeline continues
- [ ] All evidence blocks have required fields

### Phase 3
- [ ] Python Bayesian calculation matches agent within 5%
- [ ] Independence violations are flagged

### Phase 4
- [ ] Dead URLs detected before evidence is processed
- [ ] Wayback fallback suggested automatically

### Phase 5
- [ ] All 5 QA consistency tests implemented
- [ ] Anchor point violations block pipeline

### Phase 6
- [ ] Single command runs full bank research
- [ ] End-to-end pipeline validates at each stage

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking existing outputs | Run validation after each phase |
| Agents produce unexpected markdown | Build flexible parsers with fallbacks |
| Bayesian math disagreements | Allow tolerance threshold, flag for review |
| Integration complexity | Build incrementally, test each component |

---

*Last Updated: 2025-12-19*
