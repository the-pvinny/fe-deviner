# PATTERN — Asymmetrical Composition

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Asymmetry is intentional imbalance — not the absence of structure, but a deliberate decision to weight the composition to one side, creating visual tension, movement, and dynamism. Asymmetry implies a force: something is heavier, more important, pulling the eye. Symmetry resolves; asymmetry propels.

---

## When to Use

- Hero sections where direction and movement are desired
- Feature sections with a dominant element and supporting content
- Editorial layouts where tension is part of the aesthetic
- When symmetric layouts feel static or corporate

Asymmetry is compositional — it applies at the section level and the page level, not just individual components.

---

## Foundation: Unequal Column Splits

The foundation of asymmetric layout is unequal grid allocation:

```tsx
{/* 60/40 split */}
<section className="grid grid-cols-12 gap-8 py-24 px-6">
  <div className="col-span-12 lg:col-span-7">
    {/* Dominant — the heavier side */}
  </div>
  <div className="col-span-12 lg:col-span-5">
    {/* Supporting — the lighter side */}
  </div>
</section>

{/* 70/30 split — more dramatic */}
<section className="grid grid-cols-12 gap-8 py-24 px-6">
  <div className="col-span-12 lg:col-span-8">
    {/* Strong dominance */}
  </div>
  <div className="col-span-12 lg:col-span-4">
    {/* Tight supporting column */}
  </div>
</section>

{/* 75/25 — extreme, for editorial use */}
<section className="grid grid-cols-12 gap-8 py-24 px-6">
  <div className="col-span-12 lg:col-span-9"></div>
  <div className="col-span-12 lg:col-span-3"></div>
</section>
```

---

## Pattern 1: Offset Heading Composition

Heading on one side, supporting content on the other, with vertical misalignment between them:

```tsx
<section className="grid grid-cols-12 items-start gap-8 py-32 px-6">
  {/* Heading — large, left, starts at top */}
  <div className="col-span-12 lg:col-span-6">
    <h2 className="text-6xl font-bold tracking-tight leading-none lg:text-7xl">
      Something
      <br />
      Worth
      <br />
      Saying
    </h2>
  </div>

  {/* Supporting content — right, pushed down */}
  <div className="col-span-12 lg:col-span-5 lg:col-start-8 lg:pt-24">
    <p className="text-lg text-muted-foreground leading-relaxed max-w-sm">
      Supporting text that begins partway down — the vertical offset creates visual tension with the heading.
    </p>
    <a href="#" className="mt-6 inline-block text-sm underline underline-offset-4">Learn more</a>
  </div>
</section>
```

The `lg:pt-24` offset is what creates the asymmetry. The elements share the viewport but don't sit at the same height.

---

## Pattern 2: Large/Small Element Contrast

One dominant element, one much smaller — proportion as the asymmetric device:

```tsx
<section className="grid grid-cols-12 gap-6 py-24 px-6">
  {/* Dominant: large image, 8 columns */}
  <div className="col-span-12 lg:col-span-8">
    <img
      src="/feature.jpg"
      alt="Feature image"
      className="w-full aspect-[4/3] object-cover rounded-xl"
    />
  </div>

  {/* Supporting: small text stack, 4 columns, vertically centered */}
  <div className="col-span-12 lg:col-span-4 flex flex-col justify-center gap-4">
    <span className="text-xs uppercase tracking-widest text-muted-foreground">Feature</span>
    <h3 className="text-2xl font-semibold">Compact heading</h3>
    <p className="text-sm text-muted-foreground leading-relaxed">Brief description that doesn't compete with the image.</p>
  </div>
</section>
```

---

## Pattern 3: Staggered Grid

Grid items at different vertical positions — some items start higher, some lower:

```tsx
<section className="grid grid-cols-12 gap-6 py-24 px-6">
  {/* Row 1 — starts at the top */}
  <div className="col-span-6 lg:col-span-4">
    <FeatureCard />
  </div>
  {/* Row 1 — starts lower (pushed down) */}
  <div className="col-span-6 lg:col-span-4 lg:mt-16">
    <FeatureCard />
  </div>
  {/* Row 1 — starts even lower */}
  <div className="col-span-12 lg:col-span-4 lg:mt-32">
    <FeatureCard />
  </div>
</section>
```

The `mt-16`, `mt-32` offsets create a cascading diagonal through the grid — implies momentum and movement.

---

## Pattern 4: Weighted Text Layout

Type-only composition where hierarchy is created through size asymmetry:

```tsx
<section className="py-24 px-6">
  {/* Massive heading — dominant weight */}
  <h1 className="text-[clamp(4rem,12vw,10rem)] font-black leading-none tracking-tighter">
    Heavy
  </h1>

  {/* Small label — offset right */}
  <div className="flex justify-end mt-2">
    <span className="text-xs text-muted-foreground uppercase tracking-widest">
      Since 2019
    </span>
  </div>

  {/* Body — pulled left, smaller */}
  <div className="mt-16 max-w-sm">
    <p className="text-base text-muted-foreground leading-relaxed">
      Supporting body text in a narrow column. The contrast between the massive heading and the tight body column is the composition.
    </p>
  </div>
</section>
```

---

## Pattern 5: Diagonal Visual Flow

Elements positioned to create an implied diagonal from one corner to another — the eye travels through the composition:

```tsx
<section className="relative min-h-[80vh] overflow-hidden py-24 px-6">
  {/* Top-left anchor */}
  <div className="max-w-md">
    <span className="text-xs uppercase tracking-widest text-muted-foreground">Top left</span>
    <h2 className="mt-2 text-4xl font-bold">Starting point</h2>
  </div>

  {/* Bottom-right landing point */}
  <div className="absolute bottom-16 right-6 max-w-xs text-right lg:right-16">
    <p className="text-sm text-muted-foreground">Ending point — eye travels across the space between these two anchors.</p>
    <a href="#" className="mt-2 inline-block text-sm underline underline-offset-4">Continue →</a>
  </div>

  {/* Decorative mid-point — draws the diagonal */}
  <div
    className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-px w-2/3 bg-border rotate-[15deg]"
    aria-hidden="true"
  />
</section>
```

---

## Balancing Asymmetry

True asymmetry achieves visual balance through contrast, not through equal weight on both sides:

| Heavy side has | Light side compensates with |
|---|---|
| Large element | Open space |
| Image | Typography |
| Dark color | Light color |
| Complex detail | Simplicity |
| Bottom position | Top position (visual weight reads differently by vertical position) |

The design is balanced when the visual tension feels resolved, even though the elements aren't equal in size.

---

## Responsive Behavior

Asymmetric layouts almost always collapse to symmetric or single-column on mobile:

```tsx
{/* Desktop: asymmetric 7/5 split */}
{/* Mobile: single column — clean stacking */}
<div className="grid grid-cols-12 gap-8">
  <div className="col-span-12 lg:col-span-7">{main}</div>
  <div className="col-span-12 lg:col-span-5">{supporting}</div>
</div>
```

The asymmetry is a desktop composition choice. Mobile gets its own intentional layout.

---

## Common Pitfalls

- **Accidental asymmetry:** misaligned elements that aren't intentional. Asymmetry must be decisive — if the offset is small, it looks like a mistake, not a choice.
- **No visual balance:** asymmetric weight on both sides creates chaos, not tension. The heavy side must be counterbalanced by space, simplicity, or contrast on the other.
- **Forgetting mobile:** staggered offsets and unequal columns often break badly at mobile. Always design the mobile state explicitly.
- **Everything asymmetric:** if every section is asymmetric, there's nothing for the asymmetry to push against. Alternate with more balanced compositions.
