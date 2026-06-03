# EVAL — Agent Output Quality Gate

Use the eval stack on every component you ship from the agent workflow. Passing eval is the minimum bar before a file enters your project or training dataset.

## Quick check

```bash
python -m eval path/to/component.tsx -v --fail-on-violations
```

Batch reference implementations (must always pass):

```bash
python -m pytest tests/test_agent_samples.py -v
```

Audit `tsx` examples embedded in agent docs (informational; many snippets are partial):

```bash
python scripts/audit_agent_snippets.py
```

## What each layer enforces

| Layer | Source of truth | Catches |
|---|---|---|
| 1 — Tailwind | `CONFIG.md` / allowlist | Arbitrary values (`w-[247px]`), primitive colors (`bg-neutral-100`), `text-white` / `text-black`, `!important`, unknown utilities |
| 2 — Structural | `METHOD.md` | Inline styles, `export default`, `div onClick`, missing `alt` / labels / `aria-label`, missing `focus-visible:ring` on `<button>`, `<a>`, `<input>`, `<textarea>` |
| 3 — Render | JSX/HTML sanity | Unclosed tags/strings, broken imports, fragment imbalance |

**Primary metric:** `overall_violation_rate` — track it down across iterations.

## Reference samples (`samples/`)

Complete, copy-ready components that demonstrate compliant output:

| File | Demonstrates |
|---|---|
| `centered-hero.tsx` | Single `<h1>`, semantic CTAs, responsive type scale |
| `full-bleed-hero.tsx` | Inverted text via `text-primary-foreground` (never `text-white`) |
| `interactive-card.tsx` | Full-card link, `data-slot`, hover lift |
| `main-navigation.tsx` | Sticky nav, `aria-current`, mobile menu button |
| `contact-form.tsx` | Labels, focus rings, textarea |

When agent output fails eval, diff against the closest sample.

## Common failure clusters

### Forbidden colors on dark overlays

Wrong: `text-white`, `border-white`, `bg-white`  
Right: `text-primary-foreground`, `border-primary-foreground`, `bg-primary-foreground` with opacity (`/80`, `/10`)

See `samples/full-bleed-hero.tsx` and `SKILLS/footer.md`.

### Arbitrary aspect ratios

Wrong: `aspect-[4/5]`, `aspect-[4/3]` in component classes  
Right: `aspect-video`, `aspect-square` — or restructure layout without arbitrary ratios

PATTERNS docs may document cinematic ratios as **exceptions** for marketing layouts; generated production components should stay on the allowlist unless you extend CONFIG.

### Apostrophes inside JSX string examples

Wrong: `they'll` inside single-quoted attribute strings in docs (breaks render validator)  
Right: `they will` or double-quoted strings

### `<Button>` in SKILLS snippets

SKILLS examples often use shadcn `<Button>`, which carries focus styles in the real component library. The structural validator only sees raw JSX — partial snippets may report false positives for focus. **Validate complete output files**, not isolated doc fences.

### Background stacking

`-z-10` on decorative layers behind content is allowed (negative z-index on the approved scale).

## Workflow after each generation

1. Save output to a `.tsx` file.
2. Run `python -m eval <file> -v --fail-on-violations`.
3. Fix violations by category (colors first, then a11y, then render).
4. Re-run until PASS.
5. Optionally compare structure to `samples/` and relevant `SKILLS/*.md`.

## CI suggestion

```bash
python -m pytest tests/test_agent_samples.py tests/test_eval_layers.py tests/test_tailwind_validator.py -q
```

Add your own outputs under `samples/` or a project components folder with the same test pattern when you want a stricter gate.
