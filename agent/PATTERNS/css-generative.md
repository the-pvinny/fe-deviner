# PATTERN — CSS Generative & Graphic Effects

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

CSS has crossed a threshold where non-trivial generative graphics — morphing shapes, particle systems, custom cursor effects, precision clipping — are achievable with zero JavaScript or with only CSS custom properties as the control surface. This pattern covers techniques that go beyond static styling into territory previously requiring canvas or SVG.

**Scope boundary with `ambient-background.md`:** that file covers blur blobs (`filter: blur()` circles), gradient meshes, and animated position/scale blobs as background atmosphere. This file covers *structural* graphic effects: shape morphing via border-radius animation, custom paint via Houdini, precision clipping via `clip-path: shape()`, and glitch decomposition via pseudo-element desync.

---

## When to Use

- Hero sections where a distinctive shape or graphic effect is the visual differentiator
- Creative / portfolio / product launch pages where the CSS effect *is* the content
- When the same effect would require a canvas element with a render loop (Houdini replaces this for certain use cases)
- Glitch: cyberpunk, tech, gaming aesthetics — never in professional or healthcare contexts
- Clip-path notches: card UI with distinctive corner treatments, tab interfaces, diagonal-cut designs

## When Not to Use

- Content-first pages (blog, docs, e-commerce listing) — generative effects add cognitive load
- When accessibility is compromised — decorative animations must not interfere with content or focus
- Blob morphing in the background (use `ambient-background.md` instead — this covers foreground structural shapes)
- When browser support is critical and progressive enhancement is not feasible for the specific effect

---

## Technique 1 — Blob Morphing via Animated 8-Value `border-radius`

CSS `border-radius` accepts 8 values in the form `X% X% X% X% / X% X% X% X%`. The first four control horizontal radii (top-left, top-right, bottom-right, bottom-left); the second four control vertical radii. Animating between two such states produces organic, amoeba-like shape shifts.

**Browser support:** All modern browsers. `border-radius` animation is in the CSS spec.

```tsx
function MorphBlob({ className }: { className?: string }) {
  return (
    <div
      aria-hidden="true"
      className={cn(
        "w-48 h-48 bg-primary/80",
        "motion-safe:animate-[morphBlob_8s_ease-in-out_infinite]",
        className
      )}
    />
  )
}
```

```css
@keyframes morphBlob {
  0%, 100% {
    border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
  }
  25% {
    border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%;
  }
  50% {
    border-radius: 50% 60% 30% 60% / 30% 70% 40% 50%;
  }
  75% {
    border-radius: 70% 30% 50% 40% / 60% 40% 60% 30%;
  }
}
```

### As a foreground shape element (not a background blob)

```tsx
function FeatureBlobCard({
  children,
  color = "bg-primary",
  className,
}: {
  children: React.ReactNode
  color?: string
  className?: string
}) {
  return (
    <div className={cn("relative inline-flex items-center justify-center", className)}>
      {/* Morphing blob behind content */}
      <div
        aria-hidden="true"
        className={cn(
          "absolute inset-0",
          color,
          "opacity-20 motion-safe:animate-[morphBlob_10s_ease-in-out_infinite]"
        )}
      />
      {/* Content sits in front */}
      <div className="relative z-10">{children}</div>
    </div>
  )
}
```

### Keyframe generation tips

- Keep corner values between 30% and 70% — values outside this range produce sharp pinched corners
- Ensure consecutive keyframes share no identical value pairs — interpolation needs contrast to look organic
- Longer durations (8–14s) read as alive; shorter (2–4s) feel mechanical or agitated
- Add a second, offset animation on an adjacent element for a multi-blob composition

---

## Technique 2 — CSS Houdini PaintWorklet (Custom Cursor-Driven Particle Effects)

Houdini's `CSS.paintWorklet` lets you describe custom graphics in CSS `background` declarations, updated cheaply via CSS custom properties. The browser rasterises using your worklet; JS only updates the property values — no canvas `requestAnimationFrame` loop needed.

**Browser support (2026):** Chrome 65+, Edge 79+. Firefox and Safari: not supported. Always gate behind `CSS.paintWorklet` detection.

```tsx
function HoudiniParticleBackground({ children }: { children: React.ReactNode }) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Feature detect before loading the worklet
    if (!("paintWorklet" in CSS)) return

    CSS.paintWorklet.addModule("/worklets/ring-particles.js").then(() => {
      // Worklet is registered — the CSS background will now render
    })

    const handlePointerMove = (e: PointerEvent) => {
      containerRef.current?.style.setProperty("--mouse-x", String(e.clientX))
      containerRef.current?.style.setProperty("--mouse-y", String(e.clientY))
    }

    window.addEventListener("pointermove", handlePointerMove, { passive: true })
    return () => window.removeEventListener("pointermove", handlePointerMove)
  }, [])

  return (
    <div
      ref={containerRef}
      className="relative min-h-screen"
      style={
        {
          "--mouse-x": "0",
          "--mouse-y": "0",
          "--particle-color": "var(--color-primary)",
          "--particle-count": "40",
          // The worklet name becomes a valid CSS background value
          background: "paint(ring-particles)",
        } as React.CSSProperties
      }
    >
      <div className="relative z-10">{children}</div>
    </div>
  )
}
```

### Worklet file — `/public/worklets/ring-particles.js`

```js
// Runs in a separate thread; no DOM access, no import
registerPaint("ring-particles", class {
  static get inputProperties() {
    return ["--mouse-x", "--mouse-y", "--particle-color", "--particle-count"]
  }

  paint(ctx, geom, props) {
    const x = parseFloat(props.get("--mouse-x").toString()) || 0
    const y = parseFloat(props.get("--mouse-y").toString()) || 0
    const count = parseInt(props.get("--particle-count").toString()) || 30
    const color = props.get("--particle-color").toString().trim()

    ctx.clearRect(0, 0, geom.width, geom.height)

    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2
      const radius = 60 + Math.sin(angle * 3) * 20
      const px = x + Math.cos(angle) * radius
      const py = y + Math.sin(angle) * radius
      const size = 2 + Math.sin(angle * 2) * 1.5

      ctx.beginPath()
      ctx.arc(px, py, size, 0, Math.PI * 2)
      ctx.fillStyle = color
      ctx.globalAlpha = 0.5 + Math.sin(angle) * 0.3
      ctx.fill()
    }
  }
})
```

### Non-Houdini fallback

For Firefox and Safari, render the same effect via a CSS custom property–driven radial gradient or a lightweight canvas overlay:

```tsx
const supportsHoudini = typeof CSS !== "undefined" && "paintWorklet" in CSS

function ParticleBackground({ children }: { children: React.ReactNode }) {
  if (!supportsHoudini) {
    // Fallback: static radial glow at center
    return (
      <div className="relative min-h-screen">
        <div
          aria-hidden="true"
          className="pointer-events-none fixed inset-0 z-0"
          style={{
            background:
              "radial-gradient(600px at 50% 40%, var(--color-primary) / 0.06), transparent 80%)",
          }}
        />
        <div className="relative z-10">{children}</div>
      </div>
    )
  }
  return <HoudiniParticleBackground>{children}</HoudiniParticleBackground>
}
```

---

## Technique 3 — `clip-path: shape()` for Concave Corner Notches

`border-radius` rounds corners outward only. `clip-path: shape()` follows SVG path commands inline in CSS, enabling **inward** concave cuts — notches, tab forms, and tongue shapes that are impossible with radius alone.

**Browser support (2026):** Chrome 116+, Edge 116+, Firefox 128+, Safari 17.2+.

### Contrast: `border-radius` vs `clip-path: shape()`

| Property | Corner direction | Shape capability | Browser support |
|---|---|---|---|
| `border-radius` | Outward convex only | Elliptic rounding | Universal |
| `clip-path: shape()` | Inward concave + outward | Any SVG-compatible path | Chrome 116+, FF 128+, Safari 17.2+ |

### Concave top-corner notch card

```tsx
function NotchedCard({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div
      className={cn(
        "bg-card border border-border p-5 shadow-sm",
        className
      )}
      style={{
        clipPath:
          "shape(from 0% 24px, curve to 24px 0% with 0% 0%, line to calc(100% - 24px) 0%, curve to 100% 24px with 100% 0%, line to 100% 100%, line to 0% 100%, close)",
      }}
    >
      {children}
    </div>
  )
}
```

### Reading the `shape()` syntax

```
shape(
  from 0% 24px              // start at left edge, 24px down
  curve to 24px 0%          // arc to 24px from left on top edge
    with 0% 0%              // control point at the corner → creates inward arc
  line to calc(100% - 24px) 0%  // across the top to where right notch begins
  curve to 100% 24px        // arc to right edge, 24px down
    with 100% 0%            // control point at right corner
  line to 100% 100%         // down the right side
  line to 0% 100%           // across the bottom
  close                     // back to start
)
```

The `with 0% 0%` control point is the key — placing the cubic bezier control at the exact corner forces the curve to pull inward.

### Tab notch (bottom-center cutout)

```tsx
function TabCard({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div
      className={cn("bg-card p-5 shadow-sm", className)}
      style={{
        clipPath:
          "shape(from 0% 0%, line to 100% 0%, line to 100% 100%, line to calc(50% + 24px) 100%, curve to calc(50% - 24px) 100% with 50% calc(100% - 24px), line to 0% 100%, close)",
      }}
    >
      {children}
    </div>
  )
}
```

### Progressive enhancement wrapper

```tsx
const supportsShape = typeof CSS !== "undefined" && CSS.supports("clip-path", "shape(from 0% 0%, close)")

function AdaptiveNotchedCard({ children, className }: { children: React.ReactNode; className?: string }) {
  if (!supportsShape) {
    // Fallback: standard rounded card
    return (
      <div className={cn("bg-card border border-border rounded-xl p-5 shadow-sm", className)}>
        {children}
      </div>
    )
  }
  return <NotchedCard className={className}>{children}</NotchedCard>
}
```

---

## Technique 4 — Glitch Text via Desynchronized Pseudo-Elements

The glitch effect uses two `::before` / `::after` pseudo-elements set to the same text content as the parent, each clipped to a different horizontal slice, and animated with desynchronized `@keyframes` — one lags behind the other, creating the impression of signal corruption or chromatic aberration.

**Browser support:** All modern browsers. No feature detection needed.

```tsx
function GlitchText({
  children,
  as: Tag = "span",
  intensity = "medium",
  className,
}: {
  children: string
  as?: "span" | "h1" | "h2" | "h3" | "p"
  intensity?: "subtle" | "medium" | "heavy"
  className?: string
}) {
  return (
    <Tag
      data-text={children}
      className={cn(
        "glitch-text relative inline-block select-none",
        {
          "glitch-subtle": intensity === "subtle",
          "glitch-medium": intensity === "medium",
          "glitch-heavy": intensity === "heavy",
        },
        className
      )}
    >
      {children}
    </Tag>
  )
}
```

```css
/* The pseudo-elements inherit content from the data-text attribute */
.glitch-text::before,
.glitch-text::after {
  content: attr(data-text);
  position: absolute;
  inset: 0;
  pointer-events: none;
}

/* ::before — clipped to the top slice, red channel offset */
.glitch-text::before {
  color: oklch(0.55 0.25 25);  /* destructive-adjacent hue */
  clip-path: inset(0 0 60% 0);
  animation: glitch-top 2.5s steps(1) infinite;
}

/* ::after — clipped to the bottom slice, blue channel offset */
.glitch-text::after {
  color: oklch(0.55 0.25 250); /* primary-adjacent hue */
  clip-path: inset(55% 0 0 0);
  animation: glitch-bottom 2.5s steps(1) infinite 0.4s; /* 0.4s offset = desync */
}

@keyframes glitch-top {
  0%   { clip-path: inset(0 0 80% 0); transform: translate(-2px, 0); }
  10%  { clip-path: inset(20% 0 60% 0); transform: translate(2px, 0); }
  20%  { clip-path: inset(0 0 75% 0); transform: translate(0, 0); }
  30%  { clip-path: inset(10% 0 65% 0); transform: translate(-3px, 0); }
  40%  { clip-path: inset(5% 0 70% 0); transform: translate(2px, 0); }
  100% { clip-path: inset(0 0 80% 0); transform: translate(0, 0); }
}

@keyframes glitch-bottom {
  0%   { clip-path: inset(70% 0 0 0); transform: translate(3px, 0); }
  15%  { clip-path: inset(60% 0 10% 0); transform: translate(-2px, 0); }
  30%  { clip-path: inset(75% 0 0 0); transform: translate(0, 0); }
  45%  { clip-path: inset(65% 0 5% 0); transform: translate(2px, 0); }
  60%  { clip-path: inset(70% 0 0 0); transform: translate(-3px, 0); }
  100% { clip-path: inset(70% 0 0 0); transform: translate(0, 0); }
}

/* Intensity variants */
.glitch-subtle::before,
.glitch-subtle::after {
  animation-duration: 5s;
}

.glitch-heavy::before {
  animation-duration: 1.5s;
}
.glitch-heavy::after {
  animation-duration: 1.5s;
}

/* Reduced motion: static, no animation */
@media (prefers-reduced-motion: reduce) {
  .glitch-text::before,
  .glitch-text::after {
    display: none;
  }
}
```

### How the desync works

- `::before` and `::after` use the same `@keyframes` shape but `::after` starts with a `0.4s` animation delay
- `animation-timing-function: steps(1)` makes the clip-path jump between values rather than interpolate — this is the "digital glitch" signature; interpolated clip-path looks like a morph, not corruption
- The horizontal `translate` offset simulates chromatic aberration (red channel left, blue channel right)
- Varying the slice positions between keyframes creates the "scanning artifact" aesthetic

### Usage guideline

Use glitch text on display headings only — `text-4xl` minimum. At body text sizes the clipped pseudo-elements become imperceptible and the desync reads as rendering error, not intentional effect.

```tsx
// Appropriate
<GlitchText as="h1" intensity="medium" className="text-6xl font-black">
  CORRUPTED
</GlitchText>

// Inappropriate — too small, reads as a bug
<GlitchText as="p" className="text-base">Read more</GlitchText>
```

---

## Browser Support Summary

| Technique | Chrome | Edge | Firefox | Safari |
|---|---|---|---|---|
| `border-radius` 8-value animation (blob morph) | All | All | All | All |
| CSS Houdini `paintWorklet` | 65+ | 79+ | No | No |
| `clip-path: shape()` | 116+ | 116+ | 128+ | 17.2+ |
| Glitch (`clip-path: inset()` + pseudo-elements) | All | All | All | All |
| `sibling-index()` (see direction-aware.md) | 117+ | 117+ | No | No |

Always pair techniques 2 and 3 with `@supports` or JS feature detection, and provide visually coherent fallbacks.

---

## Performance Constraints

- Blob morphing: `border-radius` animation runs on the compositor thread — it is safe and low-cost; no throttling needed
- Houdini worklets: the worklet runs in a separate thread; `pointermove` → CSS custom property → repaint is cheap; avoid worklets that do expensive computation on every paint call
- `clip-path` animation (glitch): runs on the compositor in modern browsers; avoid animating `clip-path` on large elements or elements with many children — it can force layer promotion and increase memory use
- `steps(1)` timing is intentional for glitch — do not replace with smooth easing; the discontinuous jump is the effect
- All effects: test on mobile CPU. Shape morphing and animated clip-paths on full-viewport elements can stutter on mid-range Android

---

## Accessibility

- **Decorative only:** all four techniques are decoration — never use them to convey state, information, or navigation
- All decorative containers must be `aria-hidden="true"` or carry `role="presentation"`; if the element is a background, add `pointer-events-none` as well
- **Glitch text:** the pseudo-elements duplicate the visible text; screen readers will read the `data-text` attribute content twice if it's exposed. Suppress with `::before { content: ""; }` approach *or* use `aria-hidden="true"` on the pseudo-elements' parent if the real text is nearby:

```tsx
// Accessible glitch pattern: visible text in DOM, glitch is purely visual overlay
<span aria-hidden="true" className="glitch-text" data-text="CORRUPTED">
  CORRUPTED
</span>
<span className="sr-only">CORRUPTED</span>
```

- **`prefers-reduced-motion`:** the glitch keyframes must be removed entirely under `prefers-reduced-motion: reduce` — discontinuous jumping is high-risk for vestibular disorders. Blob morphing can be frozen at keyframe 0 (static shape) rather than removed.

```css
@media (prefers-reduced-motion: reduce) {
  .glitch-text::before,
  .glitch-text::after {
    display: none;
  }

  @keyframes morphBlob {
    0%, 100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
  }
}
```

---

## Common Pitfalls

- **Glitch at body size:** pseudo-element clipping at small text sizes creates rendering artifacts that look like browser bugs, not intentional effects. Only apply to display text (`text-4xl`+).
- **Blob morph as foreground:** blob morphing used as a background element belongs in `ambient-background.md`. Used in the foreground it needs color contrast (4.5:1 against surrounding content) and `aria-hidden="true"`.
- **Houdini with no fallback:** shipping `background: paint(my-worklet)` without checking `CSS.paintWorklet` support leaves Firefox and Safari users with no background at all — provide a fallback `background` property before the `paint()` call (CSS property cascade handles this naturally).
- **`clip-path: shape()` with `overflow: visible`:** clipped elements still affect layout — their overflow box is computed before clipping. If neighboring elements don't account for the full unclipped box, layout gaps appear.
- **`steps(1)` forgotten on glitch:** using `ease` or `linear` timing on the glitch keyframes makes clip-path interpolate smoothly, creating a morph effect instead of the digital jump. The glitch requires `animation-timing-function: steps(1)`.
- **Hardcoded hex in pseudo-element colors:** glitch pseudo-elements must use semantic color tokens. Use `oklch()` values that map to `--color-destructive` and `--color-primary` from your theme — not raw hex values.
