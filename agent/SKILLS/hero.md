# SKILL — Hero

Applies within CONFIG.md and METHOD.md constraints. Works alongside any STYLES/ or PATTERNS/ file.

---

## Core Principle

The hero is the first impression. It carries a single message at maximum clarity. Its job is to communicate the value proposition and propel the visitor toward the next action — not to showcase every feature the product has. One dominant headline. One CTA. Everything else is support.

---

## Anatomy

Every hero has the same five parts regardless of layout variant. The visual arrangement changes; the content hierarchy does not.

| Slot | Content | Required |
|---|---|---|
| Eyebrow | Small label or category tag above the headline | Optional |
| Headline | The dominant message — one idea, stated plainly | Yes |
| Subheadline | Supporting context, 1–2 sentences max | Yes |
| CTA group | Primary action + optional secondary action | Yes |
| Visual | Image, illustration, video, or 3D element | Contextual |

---

## Centered Hero (default)

The most common variant. Works for SaaS, landing pages, and any context where the value prop is the whole story.

```tsx
<section
  aria-labelledby="hero-heading"
  className="relative flex flex-col items-center justify-center text-center px-4 pt-24 pb-20 sm:pt-32 sm:pb-28"
>
  {eyebrow && (
    <span className="inline-flex items-center gap-1.5 rounded-full border border-border bg-muted px-3 py-1 text-xs font-medium text-muted-foreground mb-6">
      {eyebrow}
    </span>
  )}

  <h1
    id="hero-heading"
    className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-foreground max-w-3xl"
  >
    {headline}
  </h1>

  <p className="mt-6 text-lg sm:text-xl text-muted-foreground max-w-xl leading-relaxed">
    {subheadline}
  </p>

  <div className="mt-10 flex flex-col sm:flex-row items-center gap-3">
    <Button size="lg" asChild>
      <a href={primaryHref}>{primaryLabel}</a>
    </Button>
    {secondaryLabel && (
      <Button size="lg" variant="outline" asChild>
        <a href={secondaryHref}>{secondaryLabel}</a>
      </Button>
    )}
  </div>

  {trustSignal && (
    <p className="mt-6 text-xs text-muted-foreground">{trustSignal}</p>
  )}
</section>
```

**`text-4xl sm:text-5xl lg:text-6xl`** — scale the headline with viewport. Never a fixed `text-7xl` on all screens. The headline must be readable at all breakpoints without horizontal scroll.

---

## Split Hero (text + visual)

For products where showing beats telling — a screenshot, dashboard, or product image alongside the copy.

```tsx
<section
  aria-labelledby="hero-heading"
  className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28 grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center"
>
  {/* Left: copy */}
  <div>
    {eyebrow && <span className={eyebrowClasses}>{eyebrow}</span>}
    <h1 id="hero-heading" className="text-4xl lg:text-5xl font-bold tracking-tight mt-4 mb-6">
      {headline}
    </h1>
    <p className="text-lg text-muted-foreground leading-relaxed mb-8 max-w-lg">
      {subheadline}
    </p>
    <div className="flex flex-col sm:flex-row gap-3">
      <Button size="lg">{primaryLabel}</Button>
      {secondaryLabel && <Button size="lg" variant="outline">{secondaryLabel}</Button>}
    </div>
  </div>

  {/* Right: visual */}
  <div className="relative lg:order-last">
    <div className="rounded-xl overflow-hidden border border-border shadow-2xl">
      <img
        src={visualSrc}
        alt={visualAlt}
        className="w-full"
        priority
      />
    </div>
  </div>
</section>
```

Order matters on mobile: copy first, visual second. The `lg:order-last` class ensures the visual moves right at large viewports while remaining below copy at mobile.

---

## Full-Bleed Hero (with background)

For marketing pages, event announcements, or editorial launches where the visual carries weight.

```tsx
<section
  aria-labelledby="hero-heading"
  className="relative min-h-svh flex items-center justify-center overflow-hidden"
>
  {/* Background — image or video */}
  <div className="absolute inset-0 -z-10">
    <img
      src={backgroundSrc}
      alt=""
      aria-hidden="true"
      className="w-full h-full object-cover"
    />
    {/* Overlay to ensure text contrast */}
    <div className="absolute inset-0 bg-foreground/50" />
  </div>

  {/* Content */}
  <div className="relative text-center px-4 py-24 max-w-4xl mx-auto">
    <h1
      id="hero-heading"
      className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-primary-foreground"
    >
      {headline}
    </h1>
    <p className="mt-6 text-xl text-primary-foreground/80 max-w-xl mx-auto leading-relaxed">
      {subheadline}
    </p>
    <div className="mt-10 flex flex-col sm:flex-row justify-center gap-3">
      <Button size="lg" className="bg-primary-foreground text-foreground hover:bg-primary-foreground/90">{primaryLabel}</Button>
      <Button size="lg" variant="outline" className="border-primary-foreground text-primary-foreground hover:bg-primary-foreground/10">{secondaryLabel}</Button>
    </div>
  </div>

  {/* Scroll indicator */}
  <div className="absolute bottom-8 left-1/2 -translate-x-1/2 motion-safe:animate-bounce" aria-hidden="true">
    <ChevronDown className="size-6 text-primary-foreground/60" />
  </div>
</section>
```

**Always use an overlay** on background images — never place text directly on a photograph without testing contrast. The `bg-foreground/50` overlay creates a reliable fallback for varied imagery.

---

## Minimal / Typographic Hero

For editorial, agencies, and personal sites where the copy _is_ the visual:

```tsx
<section
  aria-labelledby="hero-heading"
  className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-16"
>
  {eyebrow && (
    <p className="text-sm font-medium uppercase tracking-widest text-muted-foreground mb-6">
      {eyebrow}
    </p>
  )}
  <h1
    id="hero-heading"
    className="text-6xl sm:text-7xl lg:text-8xl font-black tracking-tighter leading-none text-foreground max-w-5xl"
  >
    {headline}
  </h1>
  <div className="mt-8 flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6">
    <p className="text-lg text-muted-foreground max-w-md leading-relaxed">{subheadline}</p>
    <Button size="lg" variant="outline" className="lg:shrink-0">{primaryLabel}</Button>
  </div>
</section>
```

This variant deliberately breaks the centered alignment. The CTA is placed in the lower-right, creating visual tension with the massive headline. Works in modernist and editorial styles.

---

## Video Background Hero

```tsx
<section aria-labelledby="hero-heading" className="relative min-h-svh flex items-center overflow-hidden">
  <div className="absolute inset-0 -z-10">
    <video
      autoPlay
      muted
      loop
      playsInline
      aria-hidden="true"
      className="w-full h-full object-cover"
    >
      <source src={videoSrc} type="video/mp4" />
    </video>
    <div className="absolute inset-0 bg-foreground/60" />
  </div>
  {/* ... content same as full-bleed hero ... */}
</section>
```

`muted` + `autoPlay` is required for autoplay to work in browsers. `playsInline` prevents fullscreen on iOS. Always provide the overlay — video content is unpredictable in contrast.

Under `prefers-reduced-motion: reduce`, pause the video:

```tsx
useEffect(() => {
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches
  if (prefersReduced && videoRef.current) videoRef.current.pause()
}, [])
```

---

## Trust Signals and Social Proof

Insert below the CTA — never between headline and CTA (breaks the line to action).

```tsx
{/* Logo bar */}
<div className="mt-16 text-center">
  <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground mb-6">
    Trusted by teams at
  </p>
  <div className="flex flex-wrap items-center justify-center gap-8 grayscale opacity-60">
    {logos.map((logo) => (
      <img key={logo.name} src={logo.src} alt={logo.name} className="h-6 w-auto" />
    ))}
  </div>
</div>
```

`grayscale opacity-60` is the standard treatment — muted enough to not compete with the hero, present enough to establish credibility.

---

## CTA Sizing and Hierarchy

| Situation | Primary | Secondary |
|---|---|---|
| Centered hero, single CTA | `size="lg"` | — |
| Two CTAs, equal weight | `size="lg"` | `size="lg" variant="outline"` |
| Primary + learn more | `size="lg"` | `size="lg" variant="ghost"` |
| High-density hero | `size="md"` | `size="md" variant="outline"` |

Never use `size="sm"` on a hero CTA — the touch target is too small and the visual weight is insufficient.

---

## Responsive Behavior

| Breakpoint | Headline | CTA stack | Layout |
|---|---|---|---|
| Mobile | `text-4xl` | Stacked, full-width | Always single-column |
| sm (640px) | `text-5xl` | Inline row | — |
| lg (1024px) | `text-6xl`–`text-7xl` | Inline row | Split hero goes two-column |

On mobile: CTA buttons stack vertically (`flex-col sm:flex-row`). Never show a two-button row on narrow mobile — both buttons lose meaningful tap area.

---

## Accessibility

- The hero `<section>` must be labeled via `aria-labelledby` pointing to the `<h1>` id
- `<h1>` appears exactly once per page — always the hero headline if a hero exists
- Background images: `alt=""` + `aria-hidden="true"` — they are decorative
- Background video: `aria-hidden="true"` — screen readers have no use for decorative video
- Trust signal logos: real `alt` text for each logo (the company name)
- CTA links vs buttons: if the primary CTA navigates to a new page or route, use `<a>` (wrapped with `asChild`). If it triggers an action (open modal, start trial flow inline), use `<button>`

---

## Common Pitfalls

- **Headline too long:** headlines over 10–12 words at display sizes become banners, not statements. Cut ruthlessly.
- **CTA label too generic:** "Get started" is fine. "Click here" is meaningless. "Start your free trial" is best — it tells the user what happens.
- **No contrast on background image:** text over photography without an overlay will fail contrast requirements on most images.
- **Missing `priority` on hero image:** in Next.js, hero images above the fold should have `priority` to avoid LCP regression.
- **Two h1 elements:** if both a page title and hero headline are on the same page, one must be `<h2>`. The hero usually wins the `<h1>`.
- **Trust signal logos with no alt text:** logo images need their company name as `alt` text — not `alt="logo"`, not `alt=""`.
