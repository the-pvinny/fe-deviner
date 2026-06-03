# PATTERN — Typography-Led Layout

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Type does the compositional work that images do in other layouts. Headings, numbers, pull quotes, and body text are positioned as visual objects — not just containers for words. The layout only works if the typography is strong enough to hold it.

---

## When to Use

- Editorial and content-first pages where writing is the product
- Portfolios and studios that lead with voice, not visuals
- Landing pages where the headline IS the hero
- Sections that need impact without imagery

---

## Foundation: Type as Anchor

The dominant typographic element anchors the composition. Everything else positions relative to it.

```tsx
<section className="grid min-h-screen grid-cols-1 items-center py-32 lg:grid-cols-2 lg:gap-16">
  {/* Typography anchor — leads */}
  <div>
    <h1 className="text-7xl font-bold tracking-tight leading-none lg:text-9xl">
      We make things
      <br />
      <span className="text-muted-foreground">worth making.</span>
    </h1>
  </div>
  {/* Supporting content — follows */}
  <div className="flex flex-col gap-6 lg:pt-8">
    <p className="text-lg text-muted-foreground leading-relaxed max-w-prose">
      Body text that supports the heading...
    </p>
  </div>
</section>
```

---

## Pattern 1: Oversized Headline Hero

The heading fills most of the viewport. Other content is subordinate.

```tsx
<section className="flex min-h-[80vh] flex-col justify-between px-6 py-16 lg:px-12">
  {/* Kicker / label */}
  <span className="text-xs uppercase tracking-widest text-muted-foreground">
    Studio — Est. 2019
  </span>

  {/* The heading IS the hero */}
  <h1 className="max-w-6xl text-[clamp(3rem,10vw,8rem)] font-black leading-none tracking-tighter">
    Design that refuses to be ordinary
  </h1>

  {/* Bottom row */}
  <div className="flex items-end justify-between">
    <p className="max-w-xs text-sm text-muted-foreground leading-relaxed">
      Brief supporting description that doesn't compete with the heading.
    </p>
    <a href="/work" className="text-sm underline underline-offset-4">View work ↓</a>
  </div>
</section>
```

**`clamp()` for fluid type:** `text-[clamp(3rem,10vw,8rem)]` — type scales with viewport width, never below 3rem, never above 8rem. This is the correct approach for fluid display typography. Document as an exception to the no-arbitrary-values rule when no Tailwind token covers the full fluid range.

---

## Pattern 2: Type Grid

Text elements arranged in a grid — headings and labels as compositional blocks:

```tsx
<section className="grid grid-cols-12 gap-4 py-24">
  {/* Large heading across 8 columns */}
  <h2 className="col-span-12 text-6xl font-bold tracking-tight lg:col-span-8">
    Selected Work
  </h2>

  {/* Counter in remaining 4 columns, aligned to bottom */}
  <div className="col-span-12 flex items-end lg:col-span-4">
    <span className="text-sm text-muted-foreground">12 projects</span>
  </div>

  {/* Horizontal rule — full width */}
  <div className="col-span-12 border-t border-border" />

  {/* Project list items in grid */}
  {projects.map((project, i) => (
    <div key={project.id} className="col-span-12 grid grid-cols-12 gap-4 py-6 border-b border-border">
      <span className="col-span-1 text-xs text-muted-foreground tabular-nums">{String(i + 1).padStart(2, "0")}</span>
      <h3 className="col-span-7 text-2xl font-medium">{project.title}</h3>
      <span className="col-span-2 text-sm text-muted-foreground">{project.year}</span>
      <span className="col-span-2 text-sm text-muted-foreground text-right">{project.category}</span>
    </div>
  ))}
</section>
```

---

## Pattern 3: Pull Quote as Layout Element

Pull quote sized to break the reading flow and dominate a section:

```tsx
<section className="relative py-24">
  <div className="mx-auto max-w-4xl px-6">
    <p className="text-base text-muted-foreground leading-relaxed max-w-prose">
      Opening paragraph that sets context...
    </p>

    {/* Pull quote — breaks the column width */}
    <blockquote className="my-16 -mx-6 lg:-mx-24 border-l-4 border-primary pl-8">
      <p className="text-3xl font-light leading-snug lg:text-4xl">
        "The specific claim or idea worth highlighting, sized to be impossible to skip."
      </p>
    </blockquote>

    <p className="text-base text-muted-foreground leading-relaxed max-w-prose">
      Continuing paragraph...
    </p>
  </div>
</section>
```

---

## Pattern 4: Typographic Marquee / Ticker

Continuously scrolling text — for availability status, announcement, or ambient typography:

```tsx
function Marquee({ text, speed = 30 }: { text: string; speed?: number }) {
  return (
    <div className="flex overflow-hidden py-4 border-y border-border" aria-hidden="true">
      <div
        className="flex shrink-0 animate-[marquee_linear_infinite]"
        style={{ animationDuration: `${speed}s` }}
      >
        {/* Duplicate for seamless loop */}
        {[0, 1].map(i => (
          <span key={i} className="text-5xl font-black uppercase tracking-tighter whitespace-nowrap pr-16">
            {text} ★ {text} ★ {text} ★&nbsp;
          </span>
        ))}
      </div>
    </div>
  )
}
// @keyframes marquee { from { translate: 0 0 } to { translate: -50% 0 } }
```

Pause on hover: `animation-play-state: paused` on `.group:hover .marquee`.

---

## Pattern 5: Running Text / Watermark

Large background text as a compositional layer, behind foreground content:

```tsx
<section className="relative py-32 overflow-hidden">
  {/* Background text — decorative, large, low contrast */}
  <span
    className="absolute inset-0 flex items-center justify-center text-[20vw] font-black text-muted/20 select-none pointer-events-none whitespace-nowrap"
    aria-hidden="true"
  >
    STUDIO
  </span>

  {/* Foreground content */}
  <div className="relative z-10 max-w-2xl mx-auto text-center px-6">
    <h2 className="text-4xl font-bold">Section Heading</h2>
    <p className="mt-4 text-muted-foreground">Supporting content...</p>
  </div>
</section>
```

---

## Pattern 6: Stat / Number Feature

Large numerics as primary visual elements — for metrics, pricing, specifications:

```tsx
<section className="grid grid-cols-2 gap-px bg-border lg:grid-cols-4">
  {stats.map(stat => (
    <div key={stat.label} className="bg-background p-8">
      <p className="text-6xl font-black tabular-nums tracking-tight lg:text-7xl">
        {stat.value}
      </p>
      <p className="mt-2 text-sm text-muted-foreground">{stat.label}</p>
    </div>
  ))}
</section>
```

`tabular-nums` ensures numerals align on their baseline regardless of digit width — critical for number-heavy layouts.

---

## Fluid Type Scale

For typography-led layouts, fluid type (viewport-responsive) is often more appropriate than fixed breakpoint scaling:

```css
/* In globals.css */
:root {
  --text-display:    clamp(3rem, 8vw, 7rem);
  --text-headline:   clamp(2rem, 5vw, 4rem);
  --text-subheading: clamp(1.25rem, 2.5vw, 1.875rem);
}
```

Apply via: `font-size: var(--text-display)` in a utility class. Document as a deliberate exception to fixed token use.

---

## Spacing Principles for Type-Led Layouts

- The dominant heading has the most space around it — `py-16` to `py-32`
- Space between type elements is proportional to their relationship — heading to body is tighter than heading to next section
- Horizontal padding is generous at desktop: `px-12` to `px-24` — type needs breathing room at its edges
- Vertical rhythm uses a consistent base unit — if `py-16` is a section break, body paragraphs are `mt-6`, not `mt-7`

---

## Common Pitfalls

- **Weak headline:** if the heading isn't strong enough to anchor the layout, the whole pattern collapses. Size up or add weight.
- **Centered everything:** centering text in a typography-led layout often removes the compositional tension. Left-align more aggressively.
- **Too many type treatments:** pick 3–4 distinct type roles (display, heading, label, body) and stick to them. More creates hierarchy collapse.
- **No rhythm:** inconsistent spacing between typographic sections destroys the reading flow. Establish a vertical rhythm and maintain it.
- **Fluid type overused:** `clamp()` on body text makes measure (line length) unpredictable. Use fluid type for display and headings only.
