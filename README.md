# fe-deviner

Design-literate AI system for strict Tailwind config adherence and broad web design literacy.

**Phase 1:** Agent context files (Cursor rules + per-prompt style/pattern skills)  
**Phase 2:** Local fine-tuned model (QLoRA on Gemma 4 31B)

See [plan.md](./plan.md) for the full project plan.

## Eval Stack (Layers 1-3)

Deterministic validators for generated React/HTML output. Run all layers by default.

```bash
# Full eval (Tailwind + structural + render)
python -m eval path/to/component.tsx

# Single layer
python -m eval path/to/component.tsx --layer tailwind
python -m eval path/to/component.tsx --layer structural
python -m eval path/to/component.tsx --layer render

# Verbose output with per-violation details
python -m eval path/to/component.tsx -v

# JSON output for pipelines
python -m eval path/to/component.tsx --json

# Batch validate a training JSONL dataset
python -m eval --jsonl data/training.jsonl --field output

# Exit non-zero on violations (CI-friendly)
python -m eval path/to/component.tsx --fail-on-violations
```

Run tests:

```bash
pip install pytest
python -m pytest tests/ -v
```

### Layer 1 — Tailwind Classes
Checks CONFIG.md token rules: arbitrary values, primitive/forbidden colors, spacing/typography/radius/shadow/transition tokens, `!important`, unknown utilities.

### Layer 2 — Structural (METHOD.md)
Inline styles, default exports, non-semantic interactives (div onClick), missing alt/labels, focus-visible on interactives, icon-only buttons without aria-label, multiple h1.

### Layer 3 — Render Validity
Unclosed strings, unbalanced braces, unclosed/mismatched tags, fragment balance, malformed imports.

**Primary metric:** `violation_rate` per layer plus `overall_violation_rate` across all layers. Track across training runs as the automated quality signal.

## Agent polish (Phase 1 workflow)

After the agent generates a component, validate before committing or adding to a dataset:

```bash
python -m eval path/to/component.tsx -v --fail-on-violations
```

Reference implementations that must pass eval live in `samples/`. See [agent/EVAL.md](agent/EVAL.md) for the full checklist and common fixes.

```bash
# Gate reference samples + validators
python -m pytest tests/test_agent_samples.py tests/ -q

# Audit tsx fences inside agent/*.md (informational)
python scripts/audit_agent_snippets.py
```
