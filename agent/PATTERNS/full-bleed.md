# PATTERN — Full-Bleed and Contained Mixing

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Alternating between elements that fill the full viewport width and elements contained within a max-width column. The contrast between edge-to-edge and contained creates rhythm, visual punctuation, and a sense of spatial depth across a scrolling page.

---

## When to Use

- Long scrolling pages (landing pages, case studies, product pages)
- Anywhere sections need to feel distinctly different in weight and importance
- When imagery or color should dominate a moment in the scroll journey
- To create visual breathing room between dense content sections

---

## Foundation: Container System

Establish both containment types up front:

```tsx
// Contained — standard content width
const Contained = ({ children, className }: { children: React.ReactNode; className?: string }) => (
  <div className={cn("mx-auto max-w-screen-xl px-4 sm:px-6 lg:px-8", className)}>
    {children}
  </div>
)

// Full-bleed section wrapper
const FullBleed = ({ children, className }: { children: React.ReactNode; className?: string }) => (
  <section className={cn("w-full", className)}>
    {children}
  </section>
)
```

A page alternates between `<Contained>` and `<FullBleed>` sections.

---

## Pattern 1: Full-Bleed Image Break

A full-viewport-width image between contained text sections. The image is visual punctuation — it creates a moment of pause in the reading flow.

```tsx
<section className="py-24">
  <Contained>
    <h2 className="text-4xl font-bold">Section Heading</h2>
    <p className="mt-4 max-w-prose text-lg text-muted-foreground leading-relaxed">
      Contained body text...
    </p>
  </Contained>
</section>

{/* Full-bleed image — no container */}
<div className="w-full aspect-[16/7] overflow-hidden">
  <img
    src="/image.jpg"
    alt="Descriptive alt text"
    className="w-full h-full object-cover"
  />
</div>

<section className="py-24">
  <Contained>
    <p className="max-w-prose text-lg text-muted-foreground leading-relaxed">
      Content continues after the image break...
    </p>
  </Contained>
</section>
```

---

## Pattern 2: Full-Bleed Color Block

A section with a full-width background color change — creates a spatial environment shift:

```tsx
<section className="w-full bg-primary py-24 text-primary-foreground">
  <Contained>
    <h2 className="text-5xl font-bold tracking-tight">
      Statement that owns its space
    </h2>
    <p className="mt-6 max-w-prose text-lg text-primary-foreground/80">
      Supporting content within the color field.
    </p>
    <a href="#" className="mt-8 inline-flex items-center gap-2 text-sm font-medium underline underline-offset-4">
      Call to action →
    </a>
  </Contained>
</section>
```

Color block sections should contain minimal content — they are atmospheric, not information-dense.

---

## Pattern 3: Alternating Rhythm

A structured alternation between contained and full-bleed sections:

```tsx
function Page() {
  return (
    <>
      {/* 1. Full-bleed hero */}
      <section className="relative w-full min-h-screen flex items-center bg-foreground text-background">
        <Contained>
          <h1 className="text-7xl font-black">Hero</h1>
        </Contained>
      </section>

      {/* 2. Contained intro */}
      <section className="py-24">
        <Contained>
          <p className="max-w-prose text-lg">Intro text...</p>
        </Contained>
      </section>

      {/* 3. Full-bleed image */}
      <div className="aspect-[21/9] w-full overflow-hidden">
        <img src="/feature.jpg" alt="" className="w-full h-full object-cover" />
      </div>

      {/* 4. Contained features */}
      <section className="py-24">
        <Contained>
          <div className="grid grid-cols-3 gap-8">
            {/* feature cards */}
          </div>
        </Contained>
      </section>

      {/* 5. Full-bleed CTA */}
      <section className="w-full bg-muted py-24">
        <Contained className="text-center">
          <h2 className="text-4xl font-bold">Ready?</h2>
        </Contained>
      </section>
    </>
  )
}
```

---

## Pattern 4: Partial Bleed (Bleeds One Side)

Content contained on one side, bleeds to the edge on the other:

```tsx
<section className="py-24">
  <div className="mx-auto max-w-screen-xl px-4 sm:px-6 lg:px-8">
    <div className="grid grid-cols-12 gap-8">
      {/* Text — contained */}
      <div className="col-span-12 lg:col-span-5 flex flex-col justify-center">
        <h2 className="text-4xl font-bold">Feature heading</h2>
        <p className="mt-4 text-muted-foreground leading-relaxed">Description...</p>
      </div>

      {/* Image — bleeds to the right edge */}
      <div className="col-span-12 lg:col-span-7 overflow-hidden rounded-l-xl lg:rounded-r-none">
        {/* -mr removes the right padding of the container, extending to viewport edge */}
        <div className="-mr-4 sm:-mr-6 lg:-mr-8">
          <img src="/image.jpg" alt="" className="w-full aspect-[4/3] object-cover" />
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## Pattern 5: Full-Bleed Video Background

```tsx
<section className="relative min-h-screen w-full overflow-hidden flex items-center">
  <video
    autoPlay
    muted
    loop
    playsInline
    className="absolute inset-0 w-full h-full object-cover"
    aria-hidden="true"
  >
    <source src="/hero.mp4" type="video/mp4" />
  </video>
  {/* Scrim for text legibility */}
  <div className="absolute inset-0 bg-foreground/50" />
  {/* Content */}
  <div className="relative z-10 w-full">
    <Contained>
      <h1 className="text-7xl font-black text-background">Heading</h1>
    </Contained>
  </div>
</section>
```

Auto-playing video must be muted and respect `prefers-reduced-motion` — pause or replace with static image.

---

## Aspect Ratio Reference for Full-Bleed Media

| Ratio | Tokens | Common use |
|---|---|---|
| `aspect-video` (16/9) | Built-in | Standard video, hero images |
| `aspect-[21/9]` | Exception | Ultra-wide cinematic |
| `aspect-[16/7]` | Exception | Between video and cinematic |
| `aspect-[4/3]` | Exception | Classic editorial |
| `aspect-square` | Built-in | Instagram-style, product |

---

## Performance Constraints

- Full-bleed images: always specify `width` and `height` attributes or CSS aspect ratio to prevent layout shift
- Use `loading="lazy"` on below-fold full-bleed images, `loading="eager"` on hero
- Video: keep full-bleed hero videos under 5MB — use modern codecs (HEVC, VP9, AV1) with MP4 fallback
- Large images: use `srcset` for responsive delivery

---

## Accessibility

- Full-bleed decorative images: `alt=""` and treat as background
- Full-bleed video backgrounds: `aria-hidden="true"`, `autoPlay muted` — never autoplaying audio
- Ensure text over full-bleed media has sufficient contrast — always add a scrim or gradient overlay when text appears on images
- `prefers-reduced-motion`: pause or freeze auto-playing video

---

## Common Pitfalls

- **No contrast on text:** text directly on a full-bleed image without a scrim. Add `bg-gradient-to-t from-foreground/60` minimum.
- **Unaspected full-bleed:** image without defined aspect ratio causes layout shift as it loads
- **Too many full-bleeds:** alternating every single section removes the impact. Full-bleed should feel like an event, not the default.
- **Broken on mobile:** full-bleed images with fixed heights break on mobile. Use aspect ratios or `min-h-*` on the container.
