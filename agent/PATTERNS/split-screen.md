# PATTERN — Split-Screen

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

The viewport is divided into two distinct regions — typically vertical — each with its own content, background, or function. Split-screen creates visual tension, implies comparison or duality, and makes maximum use of wide screens.

---

## When to Use

- Hero sections that pair a headline with an image or product shot
- Before/after or A/B comparisons
- Login/signup pages (form on one side, marketing on the other)
- Feature sections where two ideas need equal visual weight
- Portfolios showing process on one side and result on the other

---

## Pattern 1: Static Split Hero

Two equal halves, each with distinct backgrounds:

```tsx
<section className="grid min-h-screen grid-cols-1 lg:grid-cols-2">
  {/* Left half */}
  <div className="flex flex-col justify-center bg-background px-8 py-16 lg:px-16">
    <span className="text-xs uppercase tracking-widest text-muted-foreground">Studio</span>
    <h1 className="mt-4 text-5xl font-bold leading-tight tracking-tight lg:text-6xl">
      We build things worth using.
    </h1>
    <p className="mt-6 max-w-sm text-muted-foreground leading-relaxed">
      Supporting description that doesn't compete with the heading.
    </p>
    <div className="mt-8 flex gap-4">
      <a href="/work" className="rounded-lg bg-primary px-6 py-3 text-sm font-medium text-primary-foreground">
        View Work
      </a>
      <a href="/about" className="rounded-lg border px-6 py-3 text-sm font-medium">
        About
      </a>
    </div>
  </div>

  {/* Right half — image or color */}
  <div className="relative min-h-64 overflow-hidden bg-muted lg:min-h-0">
    <img
      src="/hero.jpg"
      alt="Studio work"
      className="absolute inset-0 h-full w-full object-cover"
    />
  </div>
</section>
```

---

## Pattern 2: Unequal Split (Dominant/Supporting)

One side takes more visual weight:

```tsx
<section className="grid min-h-screen grid-cols-1 lg:grid-cols-[3fr_2fr]">
  {/* Dominant left — 60% */}
  <div className="relative overflow-hidden bg-foreground min-h-64">
    <img src="/feature.jpg" alt="" className="absolute inset-0 h-full w-full object-cover opacity-60" />
    <div className="relative z-10 flex h-full flex-col justify-end p-12">
      <h1 className="text-5xl font-black text-background leading-tight">Product Launch</h1>
    </div>
  </div>

  {/* Supporting right — 40% */}
  <div className="flex flex-col justify-center gap-8 bg-background p-12">
    <p className="text-muted-foreground leading-relaxed">
      Details and supporting content on the quieter side of the split.
    </p>
    <div className="space-y-3">
      {features.map(f => (
        <div key={f} className="flex items-center gap-3 text-sm">
          <div className="h-1.5 w-1.5 rounded-full bg-primary" />
          <span>{f}</span>
        </div>
      ))}
    </div>
  </div>
</section>
```

---

## Pattern 3: Auth Split (Form + Marketing)

Classic login/signup layout:

```tsx
<div className="grid min-h-screen grid-cols-1 lg:grid-cols-2">
  {/* Marketing — hidden on mobile */}
  <div className="hidden lg:flex flex-col justify-between bg-primary p-12 text-primary-foreground">
    <div>
      <span className="text-xl font-bold">Brand</span>
    </div>
    <div>
      <blockquote className="text-2xl font-light leading-snug">
        "This product changed how our team works."
      </blockquote>
      <cite className="mt-4 block text-sm text-primary-foreground/70">— Customer Name, Title</cite>
    </div>
    <p className="text-sm text-primary-foreground/50">© 2026 Brand Inc.</p>
  </div>

  {/* Form */}
  <div className="flex items-center justify-center px-6 py-16">
    <div className="w-full max-w-sm">
      <h1 className="text-2xl font-bold">Sign in</h1>
      <p className="mt-2 text-sm text-muted-foreground">Enter your email to continue.</p>
      {/* form fields */}
    </div>
  </div>
</div>
```

---

## Pattern 4: Interactive Split (Hover-Triggered)

Each side expands on hover — used for showcasing two options or states:

```tsx
function InteractiveSplit({ left, right }: { left: PanelProps; right: PanelProps }) {
  const [hovered, setHovered] = useState<"left" | "right" | null>(null)

  return (
    <section className="flex min-h-screen">
      {[
        { side: "left" as const, data: left },
        { side: "right" as const, data: right },
      ].map(({ side, data }) => (
        <div
          key={side}
          className={cn(
            "relative overflow-hidden transition-all duration-500 ease-in-out flex-shrink-0",
            hovered === side ? "flex-[0.65]" : hovered ? "flex-[0.35]" : "flex-[0.5]"
          )}
          onMouseEnter={() => setHovered(side)}
          onMouseLeave={() => setHovered(null)}
        >
          <div className="absolute inset-0">
            <img src={data.image} alt="" className="h-full w-full object-cover" />
            <div className="absolute inset-0 bg-foreground/40" />
          </div>
          <div className="relative z-10 flex h-full flex-col justify-end p-8 text-background">
            <h2 className="text-3xl font-bold">{data.title}</h2>
            <p
              className={cn(
                "mt-2 max-w-xs text-sm text-background/70 transition-all duration-300",
                hovered === side ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2"
              )}
            >
              {data.description}
            </p>
          </div>
        </div>
      ))}
    </section>
  )
}
```

---

## Pattern 5: Sticky Split (Scroll-Linked)

One side is fixed/sticky; the other scrolls. Used for step-by-step product showcases:

```tsx
<section className="grid grid-cols-1 lg:grid-cols-2 gap-0 lg:min-h-screen">
  {/* Sticky left — stays in view */}
  <div className="lg:sticky lg:top-0 lg:h-screen flex items-center bg-muted p-12">
    <div className="max-w-sm">
      <h2 className="text-4xl font-bold">How it works</h2>
      <p className="mt-4 text-muted-foreground">Step-by-step explanation locked to this side.</p>
    </div>
  </div>

  {/* Scrollable right — steps reveal as you scroll */}
  <div className="flex flex-col">
    {steps.map((step, i) => (
      <div key={i} className="flex min-h-[60vh] items-center p-12 border-t border-border">
        <div>
          <span className="text-xs uppercase tracking-widest text-muted-foreground">
            Step {i + 1}
          </span>
          <h3 className="mt-2 text-2xl font-semibold">{step.title}</h3>
          <p className="mt-3 text-muted-foreground leading-relaxed">{step.description}</p>
        </div>
      </div>
    ))}
  </div>
</section>
```

---

## Divider Options

The visual split between halves can be:

| Type | Implementation | Character |
|---|---|---|
| None | Adjacent backgrounds create implicit split | Seamless, modern |
| Rule | `border-l border-border` on right panel | Structured, editorial |
| Gap | `gap-px bg-border` on the grid | Grid-like, systematic |
| Gradient bleed | One side's color fades into the other | Soft, organic |
| Overlap | Right panel has negative left margin | Layered, dynamic |

---

## Responsive Behavior

On mobile, split-screens stack vertically. The visual order should match reading priority:

```tsx
<div className="grid grid-cols-1 lg:grid-cols-2">
  {/* On mobile: this appears first — ensure it's the primary content */}
  <div className="order-2 lg:order-1">{leftContent}</div>
  {/* On mobile: this appears second */}
  <div className="order-1 lg:order-2">{rightContent}</div>
</div>
```

Images-first on mobile (content below image) is usually preferable to text-first — the image sets context.

---

## Common Pitfalls

- **Equal priority:** both sides competing for attention with the same size, weight, and color. One side should lead.
- **Forgetting mobile stack:** the order in which panels stack on mobile matters — often the image should come first.
- **Image without defined height on mobile:** the image half collapses to zero height without `min-h-*` or an aspect ratio.
- **The boring auth split:** generic split login pages have become a visual cliché. Invest in the marketing panel — it's prime real estate.
