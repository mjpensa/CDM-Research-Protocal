# Claude Code Workflow Guide v1.0

This guide explains how to execute CDM/DRR research using Claude Code extension in VS Code.

## Prerequisites

- VS Code with Claude Code extension installed
- Claude Max subscription (enables built-in WebSearch)
- This repository cloned locally

## Quick Start

### Option 1: Interactive Research (Recommended)

Simply tell Claude Code what to research:

```
"Research Deutsche Bank's CDM adoption following the protocol in CLAUDE.md"
```

Claude Code will:
1. Read CLAUDE.md for research rules
2. Use WebSearch for evidence gathering
3. Create output files in the appropriate directory
4. Follow the Bayesian update workflow

### Option 2: Structured Execution

Generate research instructions for a specific bank:

```bash
python tools/claude_code_executor.py --bank deutsche-bank --phase 1 --generate-instructions
```

This creates `outputs/state/research-instructions-{bank}.md` which Claude Code can execute.

## Architecture

```
User → Claude Code (Opus 4.5) → WebSearch/Read/Write → Research
             ↓
  Python helpers (validation, state, rendering)
```

**No external API key required** - Claude Code's Max subscription includes WebSearch.

## Key Commands

### Validation

After completing a research stage, validate the output:

```bash
# Validate specific stage
python tools/validate_stage.py --bank deutsche-bank --phase 1 --stage tier1_evidence

# Auto-detect and validate current stage
python tools/validate_stage.py --bank deutsche-bank --phase 1 --auto

# Validate and advance to next stage
python tools/validate_stage.py --bank deutsche-bank --phase 1 --auto --advance
```

### State Management

Check research status:

```bash
python tools/claude_code_bridge.py --bank deutsche-bank --phase 1 --status
```

Get full bank context:

```bash
python tools/claude_code_bridge.py --bank deutsche-bank --phase 1 --context
```

### Queue Management

Generate task queue for structured processing:

```bash
python tools/claude_code_executor.py --bank deutsche-bank --phase 1 --generate
python tools/claude_code_executor.py --status
```

## Research Stages

The workflow consists of these stages:

| # | Stage | Description | Output File |
|---|-------|-------------|-------------|
| 1 | initialize | Set up bank directory | status.json |
| 2 | pre_mortem | Failure mode analysis | 3-gates/pre-mortem.md |
| 3 | tier1_evidence | Official source search | evidence.json, 1-evidence/tier1-evidence.md |
| 4 | bayesian_1 | Probability update | 2-bayesian/post-tier1-update.md |
| 5 | gate_1 | Skip decision | 3-gates/gate-1.md |
| 6 | tier2_evidence | Industry source search | evidence.json, 1-evidence/tier2-evidence.md |
| 7 | bayesian_2 | Probability update | 2-bayesian/post-tier2-update.md |
| 8 | gate_2 | Skip decision | 3-gates/gate-2.md |
| 9 | tier3_evidence | Signal source search | evidence.json, 1-evidence/tier3-evidence.md |
| 10 | bayesian_3 | Probability update | 2-bayesian/post-tier3-update.md |
| 11 | gate_3 | Final gate | 3-gates/gate-3.md |
| 12 | adversarial | Classification challenge | 4-adversarial/*.md |
| 13 | synthesis | Final assessment | 5-synthesis/*.md |
| 14 | complete | Mark complete | status.json |

## Skip Logic

At Gates 1, 2, and 3, if probability is very high (>80%) or very low (<20%), remaining tiers can be skipped and research proceeds directly to adversarial challenge.

## Output Structure

Each bank's research produces:

```
outputs/phase-{N}/{bank-id}/
├── evidence.json                 # PRIMARY: All evidence (Ledger-First)
├── 1-evidence/
│   ├── tier1-evidence.md        # Rendered view
│   ├── tier2-evidence.md
│   └── tier3-evidence.md
├── 2-bayesian/
│   ├── post-tier1-update.md     # Probability updates
│   ├── post-tier2-update.md
│   └── post-tier3-update.md
├── 3-gates/
│   ├── gate-1.md                # Decision points
│   ├── gate-2.md
│   └── gate-3.md
├── 4-adversarial/
│   ├── counter-case.md          # Counter-arguments
│   ├── disconfirming-searches.md
│   ├── steelman.md
│   └── verdict.md
├── 5-synthesis/
│   ├── confidence-calibration.md # MUST be created FIRST
│   ├── assessment.md
│   └── framework-integration.md
└── status.json                   # Bank state
```

## Validation Helpers

Claude Code can call these Python tools for validation:

```bash
# Trust audit
python tools/trust_audit.py outputs/phase-1/deutsche-bank/evidence.json

# Output validation
python tools/validate_outputs.py outputs/phase-1/deutsche-bank/

# Evidence processing
python tools/process_evidence.py outputs/phase-1/deutsche-bank/evidence.json
```

## Troubleshooting

### "Bank not found in manifest"
Ensure the bank ID is in `config/bank-manifest.json`.

### Validation errors
Check the specific error message and fix the output file before proceeding.

### State inconsistency
Run `python tools/claude_code_bridge.py --bank {bank} --phase 1 --status` to see current state.

## See Also

- [CLAUDE.md](../CLAUDE.md) - Research rules and evidence tiers
- [workflow.md](workflow.md) - Full workflow documentation
- [templates/](../templates/) - Output templates
