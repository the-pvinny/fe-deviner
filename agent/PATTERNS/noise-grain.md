# PATTERN — Noise and Grain

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

A subtle texture layer that adds tactility and warmth to digital surfaces. Noise and grain simulate the physical imperfection of printed or photographic media — making flat digital color feel less synthetic, more material. Used well, it makes a design feel hand-crafted. Used poorly, it looks like a rendering artifact.

---

## When to Use

- Any design that should feel warm, crafted, or physical rather than sterile
- Retro, editorial, and print-inspired aesthetics
- Over flat color fields that feel too clean or corporate
- Glassmorphism surfaces for added realism
- Minimalist designs that need a single textural element to avoid sterility

Do not use on: data tables, dense UIs, small text, or elements where legibility is paramount. Grain reduces contrast slightly — test on text elements before applying.

---

## Technique 1: CSS Filter (SVG Turbulence)

The most flexible approach — generates noise procedurally via SVG filter:

```tsx
{/* SVG filter definition — placed once, typically in the document head or an SVG at the top of the page */}
<svg style={{ position: "absolute", width: 0, height: 0 }} aria-hidden="true">
  <filter id="noise">
    <feTurbulence
      type="fractalNoise"
      baseFrequency="0.65"
      numOctaves="3"
      stitchTiles="stitch"
    />
    <feColorMatrix type="saturate" values="0" />
  </filter>
</svg>

{/* Apply to an overlay element */}
<div
  className="pointer-events-none absolute inset-0"
  style={{ filter: "url(#noise)", opacity: 0.08 }}
  aria-hidden="true"
/>
```

**`baseFrequency`:** Controls grain size. 0.65 = medium fine grain. 0.4 = coarser, more visible. 0.9 = very fine, almost invisible.

**`numOctaves`:** Controls complexity. 3 is standard. Higher = more detail but slower to render.

---

## Technique 2: CSS Pseudo-Element (Background Image)

Using a pre-generated noise texture as a background — performant, no SVG filter rendering cost:

```css
/* In globals.css */
.noise::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image: url("data:image/svg+xml,..."); /* or /noise.png */
  opacity: 0.04;
  border-radius: inherit;
}
```

Or generate a repeating noise texture via CSS background:

```css
.grain {
  position: relative;
}

.grain::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("/textures/grain.png"); /* tileable 200x200px PNG */
  background-size: 200px 200px;
  opacity: 0.06;
  pointer-events: none;
  border-radius: inherit;
  z-index: 1;
}
```

---

## Technique 3: Tailwind Component

A reusable noise overlay component that wraps any surface:

```tsx
function Grainy({ children, intensity = "subtle", className }: {
  children: React.ReactNode
  intensity?: "subtle" | "medium" | "heavy"
  className?: string
}) {
  const opacities = { subtle: 0.04, medium: 0.08, heavy: 0.15 }

  return (
    <div className={cn("relative", className)}>
      {children}
      <div
        className="pointer-events-none absolute inset-0 rounded-[inherit]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
          opacity: opacities[intensity],
        }}
        aria-hidden="true"
      />
    </div>
  )
}
```

Usage:

```tsx
<Grainy className="rounded-xl bg-card p-8" intensity="subtle">
  <CardContent />
</Grainy>
```

---

## Technique 4: Animated Grain (Film Grain Effect)

Grain that shifts each frame — simulates photographic film grain. Higher visual impact, higher performance cost:

```css
@keyframes grain {
  0%, 100% { transform: translate(0, 0); }
  10%       { transform: translate(-2%, -3%); }
  20%       { transform: translate(3%, 2%); }
  30%       { transform: translate(-3%, 1%); }
  40%       { transform: translate(1%, -2%); }
  50%       { transform: translate(2%, 3%); }
  60%       { transform: translate(-1%, 2%); }
  70%       { transform: translate(3%, -1%); }
  80%       { transform: translate(-2%, 3%); }
  90%       { transform: translate(1%, -3%); }
}

.film-grain::before {
  content: "";
  position: absolute;
  inset: -50%; /* oversized so translate doesn't reveal edges */
  background-image: url("/textures/grain.png");
  background-size: 200px 200px;
  opacity: 0.12;
  animation: grain 0.8s steps(1) infinite;
  pointer-events: none;
}
```

The `steps(1)` timing function snaps between frames rather than interpolating — giving genuine film grain flicker rather than a smooth translation.

**`prefers-reduced-motion`:** Must be disabled. This is high-motion content.

---

## Application Contexts

| Surface | Intensity | Notes |
|---|---|---|
| Page background | Subtle (0.03–0.05) | Barely perceptible — adds warmth |
| Card surfaces | Subtle (0.04–0.06) | Makes surfaces feel material |
| Hero section | Medium (0.06–0.10) | More presence, sets atmosphere |
| Color field sections | Medium (0.05–0.08) | Softens flat color |
| Glassmorphism surfaces | Medium (0.08–0.12) | Reinforces frosted glass feel |
| Retro/editorial hero | Heavy (0.12–0.18) | Deliberate print aesthetic |
| Body text areas | Avoid | Reduces contrast, harms readability |

---

## Mixing Grain with Color

Grain on colored surfaces interacts with the color's value:

- **Dark surfaces:** grain is more visible (light grain on dark base). Reduce opacity slightly.
- **Light surfaces:** grain is less visible. Slightly higher opacity needed for the same effect.
- **Saturated colors:** grain can look like compression artifacts at high intensity. Keep subtle.
- **Gradients:** grain unifies gradient surfaces beautifully — prevents banding and adds material feel.

---

## Performance Constraints

- SVG filter (`url(#noise)`) is re-rendered every frame when applied to animated elements — use only on static surfaces
- Animated grain (`animation: grain`) runs at high frequency — limit to a single element per page
- Pre-generated PNG texture tiles are the most performant option for large surfaces — the browser caches the image and tiles it in CSS
- `opacity` on the grain overlay does not affect the performance significantly — `filter: blur()` on the same element would

---

## Accessibility

- All grain overlays must be `aria-hidden="true"` and `pointer-events: none`
- Ensure grain does not reduce text contrast below WCAG minimums — test with grain applied on the actual combination
- Animated grain must be disabled under `prefers-reduced-motion`
- Color information must not depend on the grain texture — it is decoration only

---

## Common Pitfalls

- **Too heavy on text:** grain over body text feels like a rendering error to modern users. Never apply grain to text containers.
- **Wrong blending:** grain with `mix-blend-mode: multiply` on a white surface becomes invisible. Test the actual combination.
- **Performance from SVG filter on large elements:** rendering noise via `feTurbulence` on a full-viewport element is expensive. Pre-generate the texture.
- **Animated grain on mobile:** the grain animation is high-frequency and high-cost. Disable on mobile or reduce to static.
- **So subtle it's pointless:** grain at `opacity: 0.02` is invisible to most users in most contexts. Start at 0.05 and reduce from there.
