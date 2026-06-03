# PATTERN — Grid-Breaking

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Elements intentionally violate the established grid to create visual emphasis, depth, and dynamism. A break is only meaningful when a grid exists to break. Establish structure rigorously — then violate it with precision.

---

## When to Use

- Emphasizing a single hero element above all others
- Creating visual depth through layering and overlap
- Editorial layouts where images respond to text
- Breaking monotony in list-heavy or card-heavy layouts

Never use without first establishing the grid. Elements that don't align to anything are not "breaking the grid" — they are simply unaligned.

---

## Foundation: Grid Architecture

Every grid-breaking layout starts with a strict grid:

```tsx
<section className="grid grid-cols-12 gap-4 px-6">
  {/* Most elements respect the grid */}
  <div className="col-span-12 lg:col-span-8">...</div>
  <div className="col-span-12 lg:col-span-4">...</div>
</section>
```

Then specific elements intentionally violate it.

---

## Break Technique 1: Full-Bleed Out of Container

An element extends beyond its container to the viewport edge:

```tsx
<section className="max-w-5xl mx-auto px-6 py-24">
  <p className="max-w-prose text-lg leading-relaxed">Body text in container...</p>

  {/* Breaks containment — extends to viewport edge */}
  <div className="relative left-1/2 right-1/2 -ml-[50vw] -mr-[50vw] w-screen my-16">
    <img src="/hero.jpg" alt="..." className="w-full aspect-video object-cover" />
  </div>

  <p className="max-w-prose text-lg leading-relaxed">Body text continues in container...</p>
</section>
```

The `-ml-[50vw] -mr-[50vw] w-screen` technique breaks a centered container to full viewport width. Document as intentional.

---

## Break Technique 2: Column Overflow (Bleeds into Adjacent Column)

An element sized to overflow its column into a neighboring one:

```tsx
<section className="grid grid-cols-12 gap-4 px-6">
  {/* Text in left 5 columns */}
  <div className="col-span-12 lg:col-span-5 flex flex-col justify-center py-24">
    <h2 className="text-4xl font-bold">Heading that stays in its column</h2>
    <p className="mt-4 text-muted-foreground">Supporting text.</p>
  </div>

  {/* Image occupies 9 columns — bleeds past the 7-column right boundary */}
  {/* This works because col 6-12 = 7 cols, but the image spans into col 5 territory */}
  <div className="col-span-12 lg:col-start-5 lg:col-span-8">
    <img src="/image.jpg" alt="..." className="w-full aspect-[4/3] object-cover" />
  </div>
</section>
```

The overlap creates a layered effect when combined with `z-index`.

---

## Break Technique 3: Negative Margin Overlap

Elements pulled out of normal flow to overlap adjacent elements:

```tsx
<section className="relative">
  {/* Background full-bleed image */}
  <div className="aspect-[16/9] w-full overflow-hidden">
    <img src="/bg.jpg" alt="" className="w-full h-full object-cover" />
  </div>

  {/* Card pulled up with negative margin — overlaps the image */}
  <div className="relative mx-auto max-w-2xl -mt-24 px-6">
    <div className="rounded-xl bg-card p-8 shadow-2xl">
      <h2 className="text-2xl font-bold">Overlapping card</h2>
      <p className="mt-2 text-muted-foreground">Content that sits over the image.</p>
    </div>
  </div>
</section>
```

---

## Break Technique 4: Absolute Positioning Within Grid

Elements positioned outside the grid flow within a relative parent:

```tsx
<section className="relative min-h-screen">
  {/* Grid-contained content */}
  <div className="grid grid-cols-12 gap-4 px-6 py-24">
    <div className="col-span-12 lg:col-span-6">
      <h1 className="text-6xl font-bold">Main Heading</h1>
    </div>
  </div>

  {/* Decorative element — absolutely positioned, ignores grid */}
  <div
    className="absolute right-0 top-1/2 -translate-y-1/2 w-[40vw] aspect-square rounded-full bg-accent/20"
    aria-hidden="true"
  />

  {/* Floating label — anchored to viewport, not grid */}
  <span className="absolute right-8 bottom-8 text-xs text-muted-foreground rotate-90 origin-bottom-right">
    Scroll to explore
  </span>
</section>
```

---

## Break Technique 5: Rotated / Diagonal Elements

Text or elements rotated out of the horizontal axis:

```tsx
{/* Vertical label alongside content */}
<div className="flex gap-8 items-start">
  <span
    className="text-xs uppercase tracking-widest text-muted-foreground -rotate-90 origin-left translate-x-4 translate-y-12 whitespace-nowrap"
    aria-hidden="true"
  >
    Category — 2024
  </span>
  <div>
    <h2 className="text-4xl font-bold">Main Content</h2>
    <p className="mt-4 text-muted-foreground">Body text.</p>
  </div>
</div>
```

---

## Break Technique 6: Oversized Type Breaking Grid Bounds

A heading that extends beyond the column boundary — readable because it's legible, impactful because it breaks the expected edge:

```tsx
<section className="overflow-hidden px-6 py-24">
  {/* Grid-contained subheading */}
  <p className="max-w-5xl text-sm uppercase tracking-widest text-muted-foreground">Category</p>

  {/* Heading intentionally oversized — bleeds off-screen on the right */}
  <h2 className="mt-4 whitespace-nowrap text-[15vw] font-black leading-none tracking-tighter">
    Very Long Heading
  </h2>

  {/* Content back in grid */}
  <div className="mt-12 max-w-2xl">
    <p className="text-lg text-muted-foreground leading-relaxed">Body content anchored to the left column.</p>
  </div>
</section>
```

`overflow-hidden` on the section clips the overflow intentionally.

---

## Rules for Breaking Responsibly

1. **Document every break:** add a comment explaining what grid rule is being violated and why. `{/* breaks 12-col grid — full viewport width to create visual pause */}`
2. **One major break per section:** multiple breaks in one viewport fight each other and cancel out.
3. **The break serves hierarchy:** the breaking element should be the most important element in that section.
4. **Mobile must still work:** most grid breaks only apply at `lg:` — ensure the mobile layout is clean and intentional in its own right.
5. **Test with content reflow:** grid breaks with text overflow can cause horizontal scroll on unexpected screen sizes. Test all breakpoints.

---

## Accessibility

- Decorative elements that break the grid must be `aria-hidden="true"` — they carry no semantic meaning
- Reading order must not be damaged — `position: absolute` elements are still read in DOM order by screen readers
- Rotated text must also be in the DOM at normal orientation for screen readers — use `aria-hidden` on the rotated version if content is duplicated

---

## Common Pitfalls

- **Breaking without establishing:** a layout where nothing aligns is not grid-breaking — it's chaos. Build the grid first.
- **Multiple breaks competing:** two full-bleed images and an oversized heading in one section destroy hierarchy. One break per focal point.
- **Mobile neglect:** grid breaks designed for 12-column desktop often collapse badly on mobile. The mobile layout needs its own intentional composition.
- **Horizontal scroll:** full-bleed images or oversized text that aren't properly clipped cause horizontal scroll. `overflow-hidden` on the parent, `w-screen` with proper offset.
