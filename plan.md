# Design-Specialized LLM & Agent System — Project Plan

## Overview

A two-phase project to build a design-literate AI system that:
1. Adheres strictly to a custom Tailwind config (primitives/themes naming structure)
2. Supports a wide range of web design styles, interaction patterns, and layout fundamentals
3. Runs locally on existing hardware
4. Starts as an agent/prompt system, evolves toward a fine-tuned model

---

## Phase 1 — Agent System (Now)

### Goal
Produce a working design agent using structured `.md` files injected as context. Immediately useful for personal vibe-coding workflow. Doubles as fine-tuning data generation pipeline.

### File Architecture

```
/agent
  CONFIG.md          # Always on — Tailwind token reference, what is allowed/forbidden
  METHOD.md          # Always on — component structure, React/HTML patterns, accessibility
  DESIGN.md          # Always on — design literacy, cross-style fundamentals
  STYLES/
    minimalist.md
    maximalist.md
    modernist.md
    retro.md
    editorial.md
    [others as needed]
  PATTERNS/
    scroll-driven.md
    3d.md
    typography-led.md
    grid-breaking.md
    asymmetrical.md
    [others as needed]
  SKILLS/
    card.md
    form.md
    navigation.md
    hero.md
    [others as needed]
```

### File Responsibilities

| File | Always On | Purpose |
|---|---|---|
| CONFIG.md | Yes | Authoritative Tailwind token reference. All allowed classes listed. Arbitrary values explicitly forbidden. |
| METHOD.md | Yes | Component structure, React/HTML patterns, accessibility requirements, naming conventions. |
| DESIGN.md | Yes | Design literacy layer — hierarchy, grid, typography, color, space as cross-style principles. Includes default style posture for unprompted generation. |
| STYLES/*.md | Activated per prompt | Style-specific aesthetic directives. Extend DESIGN.md, never override CONFIG.md or METHOD.md. |
| PATTERNS/*.md | Activated per prompt | Interaction and layout pattern implementations. Include performance constraints and fallback requirements. |
| SKILLS/*.md | Activated per prompt | Component-specific structural patterns. |

**Multi-file conflict resolution:** When multiple STYLES/ files are activated simultaneously, the prompt's explicit intent takes priority. If directives conflict (e.g., brutalist flatness vs. glassmorphism depth), the last-mentioned style in the prompt wins for that property. Where no explicit preference exists, defer to DESIGN.md's default posture. Irreconcilable combinations (structural opposites) should be flagged in comments in the output rather than silently blended.

### Context Stack at Inference

```
CONFIG.md         (non-negotiable constraints)
METHOD.md         (non-negotiable structure)
DESIGN.md         (always-on literacy)
STYLES/{n}.md     (activated — one or more)
PATTERNS/{n}.md   (activated — one or more)
SKILLS/{n}.md     (activated — optional)
[user prompt]
```

This order is fixed. It must match the system prompt structure used in training examples — the model trains on a context shape, so inference must produce the same shape.

### Injection Method

**Always-on files (CONFIG.md, METHOD.md, DESIGN.md) → Cursor Rules**
Place in `.cursor/rules/` with `alwaysApply: true`. Injected automatically into every inference with no manual steps.

**Per-prompt files (STYLES/, PATTERNS/, SKILLS/) → `@`-file mention**
Manually `@`-mention the relevant file(s) at the start of each prompt. Activation is explicit and intentional — aesthetic choices should be deliberate. Example: `@styles/brutalist.md @patterns/scroll-driven.md`.

**Training data generation → Python assembler script**
A separate script assembles the same context stack programmatically, calls the model, and logs prompt/output pairs to JSONL. This runs alongside the Cursor workflow — not a replacement for it. The `.md` files are shared between both paths.

**Format parity constraint:** Keep all `.md` file bodies in plain markdown. No Cursor-specific MDC frontmatter or syntax inside the file content. The files must be portable to the training pipeline without modification.

**Context window budget:** The always-on stack (CONFIG + METHOD + DESIGN) should stay under ~4k tokens combined. If any file grows beyond that, split it — CONFIG.md for tokens/constraints, a separate TOKENS.md for the full class reference if needed. Per-prompt files add on top of this; activating more than 2–3 simultaneously will compress the available space for output.

### CONFIG.md Must Include
- All primitive color tokens with scale steps
- All semantic theme tokens with usage descriptions
- Spacing scale and base unit
- Typography tokens (size, weight, leading)
- Border radius tokens
- Shadow tokens
- Transition duration tokens
- Explicit prohibition on arbitrary values (`w-[247px]`, `text-[13px]`, etc.)
- Explicit prohibition on inline styles and `!important`

**Sync mechanism:** CONFIG.md must be treated as generated output, not a hand-maintained document. Write a script that reads `tailwind.config.js` and regenerates the token sections of CONFIG.md. Run it whenever the Tailwind config changes. The prose sections (prohibitions, anti-patterns) are manually maintained but token tables are always code-derived. Stale CONFIG.md is a silent failure mode — the model follows it confidently while using tokens that no longer exist.

### DESIGN.md Must Cover
- Visual hierarchy (dominant element, contrast methods)
- Grid — making and breaking (define before breaking)
- Asymmetry as intentional imbalance, not absence of structure
- Negative space as design element
- Typography dual role (to be read AND to be seen)
- Color relationships over individual colors
- Minimalism vs maximalism as compositional approaches, not value judgments
- Rule-breaking with intent — document the why in comments
- Default style posture: clean, typographically-led, generous space when no style is specified

### Anti-Patterns Section (Required in CONFIG.md)
```markdown
## Never Do This
- No arbitrary Tailwind values
- No inline styles
- No !important
- No mixing spacing scales within a single component
- No color tokens outside semantic purpose
- No omitting focus states
- No unapproved component patterns
```

---

## Phase 2 — Fine-Tuned Model (Later)

### Goal
A LoRA-fine-tuned model that has internalized config adherence and design principles into weights. More reliable than agent files for complex/long outputs. Consistent across sessions without context window pressure.

### Hardware
- **GPU:** RTX 5090 (32GB VRAM) — sufficient, no new hardware needed
- **RAM:** 64GB DDR5 — sufficient
- **Storage:** Ensure 2TB+ NVMe available for models, datasets, checkpoints

### Hardware Compatibility

**RTX 5090 (32GB VRAM) with Gemma 4 31B:**
- Training (QLoRA + FlashAttention-2): ~24-28 GB VRAM
- Inference (Q4 quantization): ~18-20 GB VRAM
- Inference (vLLM + AWQ): ~20-22 GB VRAM with 8K context

**Requirements:**
- CUDA 12.1+
- Linux (vLLM requires Linux; WSL2 works for development)
- Python 3.10-3.11

### Model Target
- **Model:** Gemma 4 31B (Google DeepMind, April 2026)
- **Parameters:** 31 billion, dense transformer architecture
- **Context window:** 256K tokens
- **Capabilities:** Text + image multimodal input
- **VRAM at Q4:** ~18-20 GB (fits RTX 5090 with headroom)
- **VRAM at BF16:** 48-64 GB (requires multi-GPU or cloud)

### Training Method
- **Framework:** Axolotl (YAML-driven, production-grade fine-tuning)
- **Adapter:** QLoRA (4-bit quantized base + LoRA adapters)
- **Memory optimizations:**
  - BitsAndBytes NF4 quantization (`load_in_4bit: true`)
  - FlashAttention-2 (`flash_attention: true`)
  - Sample packing (`sample_packing: true`)
  - Gradient checkpointing
- **Training phases:** SFT first, then DPO

### Axolotl Configuration

**Installation:**
```bash
pip install axolotl
pip install flash-attn --no-build-isolation
```

**Base training config (`config.yml`):**
```yaml
base_model: google/gemma-4-31B
model_type: GemmaForCausalLM

# QLoRA settings
adapter: qlora
load_in_4bit: true
lora_r: 64
lora_alpha: 128
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj
  - gate_proj
  - up_proj
  - down_proj

# Memory optimizations
flash_attention: true
sample_packing: true
gradient_checkpointing: true
bf16: true

# Training parameters
micro_batch_size: 1
gradient_accumulation_steps: 8
num_epochs: 3
learning_rate: 2e-4
lr_scheduler: cosine
warmup_ratio: 0.03
optimizer: adamw_bnb_8bit

# Dataset
datasets:
  - path: ./data/training.jsonl
    type: sharegpt

output_dir: ./outputs/gemma-4-31b-qlora
```

**Run training:**
```bash
axolotl train config.yml
```

**Expected VRAM usage:** ~24-28 GB with QLoRA + FlashAttention-2 + gradient checkpointing

### Training Phases

| Phase | Method | Data Required | Goal |
|---|---|---|---|
| 1 | QLoRA SFT | 500–2k structured examples | Learn token vocabulary and component patterns |
| 2 | DPO | 500+ chosen/rejected pairs | Suppress base model fallback behavior |
| 3 | Eval loop | Automated validator output | Find and fix config drift |

### Serving and Inference (Phase 2)

The fine-tuned model runs locally via **vLLM** (primary) for high-throughput serving with PagedAttention.

**vLLM Installation:**
```bash
pip install vllm
```

**Key vLLM Features:**
- **PagedAttention:** Divides KV cache into 16-token blocks, reduces VRAM usage by 50%+ in long-context scenarios
- **Continuous Batching:** Iteration-level scheduling, 2-5x throughput vs static batching
- **Prefix caching:** Share context across requests with identical prefixes

**Serving the merged model:**
```bash
vllm serve ./outputs/gemma-4-31b-merged \
  --tensor-parallel-size 1 \
  --max-model-len 8192 \
  --quantization awq \
  --enable-prefix-caching
```

**Workflow:**
1. Merge LoRA adapters into base model after training
2. Optionally quantize merged model (AWQ or GPTQ) for lower VRAM
3. Serve via vLLM OpenAI-compatible API
4. Register in Cursor as custom model endpoint (`http://localhost:8000/v1`)
5. Per-prompt STYLES/PATTERNS files continue to be `@`-mentioned

**Fallback:** Ollama with GGUF conversion for simpler local deployment if vLLM overhead is unnecessary.

The Cursor rules injection method from Phase 1 remains unchanged in Phase 2. The only difference is the model behind the endpoint.

### System Prompt Structure for Training
```
[SYSTEM]
You are a UI developer. Only use tokens defined in the provided config.
{DESIGN.md principles}
{STYLE.md directives — if applicable}
{PATTERN.md directives — if applicable}

[CONFIG]
{ ...tailwind.config.js... }

[USER]
{prompt}

[ASSISTANT]
{curated output}
```

---

## Dataset Plan

### Source
Obsidian vault + LightRAG database

### Note Categories (Tag in Obsidian First)
- `#training/component` — has code, ready for extraction
- `#training/aesthetic` — style/mood reference → feeds STYLES/*.md files
- `#training/interaction` — interaction pattern → feeds PATTERNS/*.md files
- `#training/skip` — inspiration, process notes, not useful for training

### Freestanding Principles
Do NOT use as training pairs. Extract into DESIGN.md and STYLES/*.md files. These are the always-on system prompt layer, not per-example context.

### Data Schema

```json
{
  "id": "component-style-###",
  "component_type": "card | hero | form | navigation | ...",
  "aesthetic_style": ["minimalist", "maximalist", "retro", "..."],
  "interaction_patterns": ["scroll-driven", "3d", "hover-lift", "..."],
  "layout_patterns": ["grid-breaking", "asymmetrical", "typography-led", "..."],
  "complexity": "simple | moderate | complex",
  "source_project": "project-slug",
  "prompt": "Natural language prompt that would produce this output",
  "aesthetic_prompt": "Aesthetic intent description",
  "config_snapshot": "{ ...relevant tailwind config... }",
  "output": "// React or HTML/CSS code",
  "output_type": "react | html",
  "tokens_used": ["color-primary", "spacing-4", "radius-md"],
  "tier": 2
}
```

### Fidelity Tiers

| Tier | Description | Sufficient For |
|---|---|---|
| 1 | Prompt + output, loosely described | Pipeline validation only |
| 2 | Consistent format, clean renderable code, config always present | First real training target |
| 3 | Tier 2 + metadata tags (type, complexity, tokens used) | Dataset balancing and gap analysis |
| 4 | Tier 3 + chosen/rejected pairs | DPO training |

**Target:** Get all examples to Tier 2 before scaling dataset size. 300 consistent Tier 2 examples outperform 1000 inconsistent ones.

### Extraction Pipeline (Obsidian → JSONL)

```python
# 1. Walk vault, find notes tagged #training/component
# 2. Filter by presence of config token patterns in code blocks
# 3. For each qualifying note, call Claude API:
#    - Extract natural language prompt
#    - Extract clean output code
#    - List tokens used
#    - Tag aesthetic/interaction/layout context
# 4. Write to JSONL (HuggingFace standard format)
# 5. Manual review pass — approve or reject each entry
```

Manual review is non-negotiable. Dataset quality is the primary value differentiator.

### Rejection Pairs for DPO
- Run base model (pre-fine-tune) on your prompts
- Collect generic outputs as automatic rejection set
- Also create deliberate violations: correct prompt, wrong output using arbitrary Tailwind values

**Rejection set must be rebuilt before each DPO round.** Pre-SFT base model outputs as rejections work for the first DPO pass, but after SFT the model's failure modes shift. Collect rejection examples from the SFT-fine-tuned model's actual outputs on your eval set — these represent the real post-SFT failure modes and will produce a more targeted DPO signal. Reusing stale pre-SFT rejections in later rounds is less effective.

### Dataset Coverage Audit
Track distribution across:
- Component types
- Aesthetic styles
- Interaction patterns
- Layout patterns
- Output type (React vs HTML)
- Complexity levels

Identify and fill gaps before training. Imbalanced datasets produce imbalanced models.

### Synthetic Data Generation (Gap Filling)

The coverage audit will reveal holes — styles or component types with few or no Obsidian examples. Do not scale up weak real data; synthesize targeted examples instead.

**Process:**
1. Identify under-represented categories from the coverage audit
2. Use the Phase 1 agent system (CONFIG + METHOD + DESIGN + relevant STYLE/PATTERN files) to generate candidate components for the missing categories
3. Apply the same manual review standard as real examples — reject anything with token violations or structural issues
4. Tag with `"source_project": "synthetic"` in the schema for tracking
5. Limit synthetic examples to gap-filling only; they should not dominate any category

Synthetic data is a valid supplement, not a replacement. Real examples with provenance are always preferred.

---

## Eval System

### Layer 1 — Tailwind Class Validator (Build Before First Training Run)

```python
# Parse generated output
# Extract all Tailwind classes
# Check every class against config allowed tokens
# Flag: arbitrary values, unapproved color names, wrong scale usage
# Output: violation rate per class category
# Track violation rate across training runs as primary quality metric
```

Deterministic. This is the primary quality metric — a real number, not a loss curve.

### Layer 2 — Structural Validator

```python
# Parse output as JSX/HTML
# Check component structure against METHOD.md rules:
#   - Required accessibility attributes present (aria-*, role, focus states)
#   - No banned patterns (inline styles, !important)
#   - Named correctly per conventions
# Output: structural violation rate per rule category
```

Implemented in `eval/structural_validator/`. Checks inline styles, default exports, div/span onClick, missing alt/labels, focus-visible on interactives, icon-only buttons, multiple h1.

### Layer 3 — Render Validity Check

```python
# Attempt to parse/compile the generated code
# Flag: syntax errors, unclosed tags, invalid JSX, broken imports
# Output: pass/fail + error type
```

Implemented in `eval/render_validator/`. Checks unclosed strings, unbalanced braces, tag matching, JSX fragments, malformed imports.

### Layer 4 — LLM-as-Judge (Design Quality, Small Held-Out Set)

Run on a fixed set of 20–30 held-out prompts after each training experiment. Use a capable model (Claude, GPT-4) as evaluator with a structured rubric:
- Does the output reflect the requested aesthetic style?
- Is the visual hierarchy intentional and legible?
- Does the use of space, type, and color reflect DESIGN.md principles?

Score 1–5 per dimension. Track deltas across training runs. This is expensive — run selectively, not on every eval.

### Eval Cadence
- Layers 1–3: Run after every training experiment, automated
- Layer 4: Run before/after major training milestones
- Use Layer 1–3 failure cases to expand rejection set
- Re-train on augmented dataset

---

## Style and Pattern Coverage Targets

### Design Styles
- Minimalist
- Maximalist
- Modernist
- Retro (with era distinctions: 70s, 80s, 90s, Y2K)
- Editorial
- Brutalist
- Glassmorphism
- [Expand as curated examples exist]

### Interaction Patterns
- Scroll-driven animation (CSS scroll-driven + Intersection Observer fallback)
- 3D (CSS transforms + Three.js/R3F)
- Hover and focus micro-interactions
- Page transitions
- Gesture-driven (touch/swipe)
- [Expand as curated examples exist]

### Layout Fundamentals
- Grid systems (making and breaking)
- Typographic-led layouts
- Asymmetrical composition
- White space as design element
- Color-field layouts
- Full-bleed and contained content mixing
- [Expand as curated examples exist]

---

## Recommended Execution Order

### Week 1 — Audit and Structure
- [ ] Tag all Obsidian notes (`#training/component`, `#training/aesthetic`, `#training/interaction`, `#training/skip`)
- [ ] Extract freestanding principles into a single principles document
- [ ] Get clear count per category
- [ ] Draft DESIGN.md from freestanding principles
- [ ] Draft CONFIG.md from Tailwind config

### Week 2 — Agent System + Pipeline
- [ ] Complete CONFIG.md, METHOD.md, DESIGN.md
- [ ] Draft initial STYLES/ files for your most-used aesthetics
- [ ] Draft initial PATTERNS/ files for your most-used patterns
- [ ] Write Obsidian → JSONL extraction script
- [ ] Install Axolotl and verify FlashAttention-2 works on RTX 5090
- [ ] Install vLLM and test serving a small model
- [x] Build Tailwind class validator eval script (Layer 1)
- [x] Build structural validator (Layer 2) and render validity check (Layer 3)

### Week 3 — First Training Experiment
- [ ] Format strongest 50–100 component examples to Tier 2
- [ ] Run QLoRA SFT on Gemma 4 31B
- [ ] Run eval validator on outputs
- [ ] Identify primary drift failure modes

### Week 4+ — Iterate
- [ ] Scale dataset based on drift failure modes
- [ ] Add rejected pairs for DPO on weakest areas
- [ ] Expand STYLES/ and PATTERNS/ coverage
- [ ] Experiment with longer context lengths if quality is sufficient

---

## Key Decisions Already Made

| Decision | Choice | Reason |
|---|---|---|
| Build vs fine-tune | Fine-tune existing model | Cost, time, sufficient for goal |
| Base model | Gemma 4 31B | 256K context, strong code benchmarks, fits 32GB at Q4 |
| Training method | QLoRA + DPO | Single GPU viable, suppresses base model fallback |
| Framework | Axolotl + BitsAndBytes + FlashAttention-2 | Production-grade, memory-optimized, YAML-driven |
| Output targets | React and HTML/CSS | Both supported, tagged per example |
| Config injection | Full config every inference | Simpler, more reliable than partial slices |
| Injection method | Cursor Rules (always-on) + @-file (per-prompt) | IDE-native, zero friction, format-portable to training pipeline |
| Phase 2 serving | vLLM (PagedAttention + Continuous Batching) | 2-5x throughput, 50% VRAM reduction, OpenAI-compatible API |
| Aesthetic context | Preserved as prompt dimension | Core differentiator, not flattened away |
| Principles | System prompt layer, not training pairs | Editable without retraining |
| Start point | Agent .md files first | Immediate utility, feeds fine-tuning later |

---

## Open Questions for Next Session

- Finalize Tailwind config token naming structure for CONFIG.md
- Define default style posture for unprompted generation in DESIGN.md
- Determine if project-type context (editorial vs SaaS) needs explicit handling in schema
- Map which existing Obsidian notes qualify as Tier 2 without modification
