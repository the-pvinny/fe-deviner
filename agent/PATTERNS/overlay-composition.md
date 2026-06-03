# PATTERN — Overlay Composition

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Elements stacked on the z-axis to create visual depth within a flat medium. Text over image, cards over backgrounds, elements overlapping across sections. Overlay composition simulates physical layering — the world has depth, and the design reflects it.

---

## When to Use

- Placing text or UI over photography or color fields
- Creating depth in sections that don't use shadows or 3D transforms
- Hero sections where content floats over a background environment
- Feature cards that overlap section boundaries

---

## Foundation: Positioning Layers

Three-layer model for most overlay compositions:

```tsx
<div className="relative"> {/* positioning context */}
  <div className="absolute inset-0"> {/* layer 1: background */}
    <img src="/bg.jpg" alt="" className="w-full h-full object-cover" />
  </div>
  <div className="absolute inset-0 bg-foreground/40" /> {/* layer 2: scrim */}
  <div className="relative z-10"> {/* layer 3: content — z-10 lifts above absolute layers */}
    {/* Content */}
  </div>
</div>
```

---

## Pattern 1: Text Over Image

The most fundamental overlay — readable text over a photographic background:

```tsx
<section className="relative min-h-[70vh] flex items-end overflow-hidden">
  {/* Background image */}
  <img
    src="/hero.jpg"
    alt=""
    aria-hidden="true"
    className="absolute inset-0 w-full h-full object-cover"
  />

  {/* Gradient scrim — more natural than solid overlay */}
  <div className="absolute inset-0 bg-gradient-to-t from-foreground/80 via-foreground/20 to-transparent" />

  {/* Text content — positioned at bottom, above scrim */}
  <div className="relative z-10 p-8 lg:p-16 max-w-3xl">
    <h1 className="text-5xl font-bold text-background leading-tight lg:text-6xl">
      Heading that reads over the image
    </h1>
    <p className="mt-4 text-lg text-background/80 leading-relaxed max-w-prose">
      Supporting text — the gradient below ensures this is always readable.
    </p>
  </div>
</section>
```

### Scrim options

| Type | Class | Character |
|---|---|---|
| Solid | `bg-foreground/50` | Flat, even coverage |
| Bottom gradient | `bg-gradient-to-t from-foreground/80 to-transparent` | Natural, atmospheric |
| Top gradient | `bg-gradient-to-b from-foreground/60 to-transparent` | Dark top, for nav |
| Full gradient | `bg-gradient-to-t from-foreground/80 via-foreground/20 to-transparent` | Middle clarity |
| Vignette | Radial gradient from edges | Cinematic focus |

---

## Pattern 2: Card Overlapping Section Boundary

A card that bleeds from one section into the next — creates continuity and depth across scroll:

```tsx
<>
  {/* Top section with extra bottom padding to accommodate the card */}
  <section className="relative bg-muted pb-32 pt-24">
    <div className="max-w-screen-xl mx-auto px-6">
      <h2 className="text-4xl font-bold">Section Heading</h2>
    </div>

    {/* Card — absolutely positioned, overlaps into next section */}
    <div className="absolute bottom-0 left-1/2 w-full max-w-4xl -translate-x-1/2 translate-y-1/2 px-6">
      <div className="rounded-2xl bg-card p-8 shadow-2xl border border-border">
        <h3 className="text-2xl font-semibold">Overlapping card</h3>
        <p className="mt-2 text-muted-foreground">Content that bridges two sections.</p>
      </div>
    </div>
  </section>

  {/* Bottom section with extra top padding to clear the card */}
  <section className="pt-32 pb-24 bg-background">
    <div className="max-w-screen-xl mx-auto px-6">
      {/* Content below the overlapping card */}
    </div>
  </section>
</>
```

---

## Pattern 3: Floating UI Elements Over Content

Interface elements that float above page content:

```tsx
<section className="relative py-24 px-6">
  {/* Main content */}
  <div className="max-w-2xl">
    <h2 className="text-4xl font-bold">Feature Section</h2>
    <p className="mt-4 text-muted-foreground leading-relaxed">Body content...</p>
  </div>

  {/* Floating badge — decorative, anchored to parent */}
  <div
    className="absolute right-6 top-8 rounded-full bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow-lg lg:right-16"
    aria-hidden="true"
  >
    New
  </div>

  {/* Floating image — offset from main content */}
  <div className="absolute right-0 top-1/2 -translate-y-1/2 w-[40%] rounded-l-2xl overflow-hidden shadow-2xl hidden lg:block">
    <img src="/feature.jpg" alt="Feature illustration" className="w-full aspect-[4/3] object-cover" />
  </div>
</section>
```

---

## Pattern 4: Label Over Color Field

Text on a solid color background — color field as the design foundation:

```tsx
<section className="relative bg-primary min-h-[60vh] flex items-center overflow-hidden">
  {/* Background typography watermark */}
  <span
    className="absolute right-0 top-1/2 -translate-y-1/2 text-[20vw] font-black text-primary-foreground/10 select-none pointer-events-none leading-none"
    aria-hidden="true"
  >
    WORKS
  </span>

  {/* Foreground content */}
  <div className="relative z-10 max-w-screen-xl mx-auto px-6 py-16">
    <h2 className="text-5xl font-bold text-primary-foreground">
      Statement on color field
    </h2>
    <p className="mt-4 max-w-prose text-primary-foreground/80 leading-relaxed">
      Supporting text on the primary color field.
    </p>
  </div>
</section>
```

---

## Pattern 5: Multi-Layer Depth Stack

Multiple layers creating genuine visual depth within a static layout:

```tsx
<section className="relative h-[80vh] overflow-hidden bg-neutral-950">
  {/* Layer 1: Background gradient (deepest) */}
  <div className="absolute inset-0 bg-gradient-to-br from-violet-900/30 via-transparent to-blue-900/30" />

  {/* Layer 2: Mid decorative element */}
  <div
    className="absolute left-1/4 top-1/4 h-96 w-96 rounded-full bg-violet-500/10 blur-3xl"
    aria-hidden="true"
  />

  {/* Layer 3: Card surface */}
  <div className="absolute inset-x-8 top-1/2 -translate-y-1/2 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 p-8 lg:inset-x-24">
    <h2 className="text-4xl font-bold text-white">Layered composition</h2>
    <p className="mt-3 text-white/60">Multiple z-levels create real depth.</p>
  </div>

  {/* Layer 4: Foreground decorative type (shallowest) */}
  <div
    className="absolute bottom-8 right-8 text-xs uppercase tracking-widest text-white/20"
    aria-hidden="true"
  >
    Scroll
  </div>
</section>
```

---

## Contrast Rules for Text Over Overlays

Text over imagery is an accessibility minefield. Non-negotiable rules:

1. **Never text directly on an image** without a scrim — contrast cannot be guaranteed as images change
2. **Minimum contrast:** 4.5:1 for body text, 3:1 for large text (≥18px normal, ≥14px bold) — test with actual images, not approximations
3. **Test with brightness extremes:** the image might load a light region in front of light text — verify with the brightest possible area of the image
4. **Prefer gradient scrims over solid** — they look more natural while still guaranteeing contrast at the text location

---

## Z-Index Management

Use the defined z-index scale from CONFIG.md. Don't create ad-hoc values.

```
z-0  — base content
z-10 — raised content, decorative overlays
z-20 — interactive overlays, dropdowns
z-30 — sticky navigation
z-40 — modal backdrops
z-50 — modals, toast notifications
```

Decorative overlay elements should live at `z-0` to `z-10`. Never use `z-[9999]` — it indicates an architectural problem.

---

## Accessibility

- Decorative overlay elements (`aria-hidden="true"`) — do not need accessible labels
- Background images (`aria-hidden` or `alt=""`) — the content is the foreground text, not the image
- Floating UI over content must not overlap interactive elements or make them unreachable
- Ensure scrim opacity creates sufficient contrast — don't approximate, measure

---

## Common Pitfalls

- **No scrim:** text directly on image with no overlay. Non-negotiable: always add a scrim.
- **Opaque scrim:** solid `bg-foreground/50` looks flat and heavy. Use gradients that cover only the area of text.
- **Overlapping interactive elements:** absolute-positioned decoratives that cover buttons or links. Use `pointer-events-none` on decoratives.
- **z-index wars:** ad-hoc `z-[100]`, `z-[999]` values piling up. Establish and follow the z-index scale.
- **Not testing with varied images:** a dark scrim over a CMS image that's already very dark becomes double-dark. Test with the actual image range.
