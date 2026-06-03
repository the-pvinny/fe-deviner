# PATTERN — Ambient Background

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

A living, atmospheric background that gives depth and mood to the space behind content. Unlike decorative illustrations or static gradients, ambient backgrounds move slowly, shift subtly, or respond to cursor position — they create the sense of an environment rather than a surface. The foreground content is what matters; the background is atmosphere.

---

## When to Use

- Hero sections where the visual environment needs to feel alive
- Dark-mode interfaces where a flat background feels like a void
- Glassmorphism contexts where the background is the scene
- Landing pages for creative or tech products where atmosphere is part of the brand
- Anywhere a static gradient feels insufficient

Ambient backgrounds must never compete with content. If you're looking at the background instead of the content, the background is too loud.

---

## Pattern 1: Conic Gradient Mesh

Multiple layered radial or conic gradients creating a rich, multi-point color field:

```tsx
<div className="relative min-h-screen overflow-hidden bg-neutral-950">
  {/* Gradient blobs — each is a radial glow at different positions */}
  <div
    className="absolute -top-40 -right-40 h-[600px] w-[600px] rounded-full bg-violet-500/20 blur-[120px]"
    aria-hidden="true"
  />
  <div
    className="absolute top-1/3 -left-40 h-[500px] w-[500px] rounded-full bg-blue-500/15 blur-[100px]"
    aria-hidden="true"
  />
  <div
    className="absolute bottom-0 right-1/4 h-[400px] w-[400px] rounded-full bg-emerald-500/10 blur-[80px]"
    aria-hidden="true"
  />

  {/* Foreground content */}
  <div className="relative z-10">{children}</div>
</div>
```

**Adjusting character:**
- More saturated + smaller blur radius → neon, cyberpunk
- Less saturated + larger blur radius → soft, atmospheric
- Warm tones (amber, rose) → energetic, organic
- Cool tones (violet, blue) → technical, calm

---

## Pattern 2: Animated Blob (CSS Keyframes)

Slow, organic shape animation — blobs drift and shift over long durations:

```tsx
<div className="relative overflow-hidden bg-neutral-950">
  <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
    <div className="absolute top-1/4 left-1/4 h-72 w-72 animate-[blob_7s_infinite] rounded-full bg-violet-500/20 blur-3xl mix-blend-screen" />
    <div className="absolute top-1/3 right-1/4 h-72 w-72 animate-[blob_9s_infinite_2s] rounded-full bg-blue-500/20 blur-3xl mix-blend-screen" />
    <div className="absolute bottom-1/4 left-1/3 h-72 w-72 animate-[blob_8s_infinite_4s] rounded-full bg-pink-500/20 blur-3xl mix-blend-screen" />
  </div>
  <div className="relative z-10">{children}</div>
</div>
```

```css
@keyframes blob {
  0%   { translate: 0px 0px;   scale: 1; }
  33%  { translate: 30px -50px; scale: 1.1; }
  66%  { translate: -20px 20px; scale: 0.9; }
  100% { translate: 0px 0px;   scale: 1; }
}
```

**Performance note:** `blur-3xl` (or `filter: blur(64px)`) on animated elements is GPU-intensive. Limit to 2–3 blobs, test on mobile, provide a `prefers-reduced-motion` fallback (remove animation, keep static blur).

---

## Pattern 3: CSS Aurora / Northern Lights

Multiple blended gradients creating an aurora-like shimmer:

```css
.aurora {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 40%, oklch(0.606 0.250 292 / 0.3), transparent),
    radial-gradient(ellipse 60% 40% at 80% 60%, oklch(0.546 0.245 262 / 0.2), transparent),
    radial-gradient(ellipse 70% 40% at 50% 20%, oklch(0.627 0.130 168 / 0.15), transparent);
  filter: blur(40px);
  animation: aurora-shift 12s ease-in-out infinite alternate;
}

@keyframes aurora-shift {
  0%   { background-position: 0% 50%; transform: scale(1); }
  50%  { background-position: 100% 50%; transform: scale(1.05); }
  100% { background-position: 0% 50%; transform: scale(1); }
}
```

---

## Pattern 4: Dot / Grid Pattern

A subtle repeating pattern that adds texture without blob complexity:

```tsx
{/* CSS background pattern — no images, no JS */}
<div
  className="absolute inset-0 pointer-events-none"
  style={{
    backgroundImage: "radial-gradient(var(--color-border) 1px, transparent 1px)",
    backgroundSize: "24px 24px",
    opacity: 0.4,
  }}
  aria-hidden="true"
/>
```

Fade the edges with a radial gradient mask:

```tsx
<div
  className="absolute inset-0 pointer-events-none"
  style={{
    backgroundImage: "radial-gradient(var(--color-border) 1px, transparent 1px)",
    backgroundSize: "24px 24px",
    WebkitMaskImage: "radial-gradient(ellipse 80% 80% at 50% 50%, black 40%, transparent 100%)",
    maskImage: "radial-gradient(ellipse 80% 80% at 50% 50%, black 40%, transparent 100%)",
    opacity: 0.5,
  }}
  aria-hidden="true"
/>
```

---

## Pattern 5: Cursor-Reactive Background

Background that responds to cursor position — a spotlight follows the mouse:

```tsx
function CursorGlow() {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (ref.current) {
        ref.current.style.setProperty("--x", `${e.clientX}px`)
        ref.current.style.setProperty("--y", `${e.clientY}px`)
      }
    }
    window.addEventListener("mousemove", handleMouseMove, { passive: true })
    return () => window.removeEventListener("mousemove", handleMouseMove)
  }, [])

  return (
    <div
      ref={ref}
      className="pointer-events-none fixed inset-0 z-0 transition-opacity duration-300"
      style={{
        background: "radial-gradient(600px at var(--x, 50%) var(--y, 50%), oklch(0.541 0.281 293 / 0.08), transparent 80%)",
      }}
      aria-hidden="true"
    />
  )
}
```

This creates a soft violet spotlight that follows the cursor across the entire page — extremely low-cost (no animation loop, just CSS custom property updates) and high-impact.

---

## Pattern 6: Canvas-Based Particle Field

For maximum visual complexity — particles that float, drift, or react to cursor:

```tsx
function ParticleField() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext("2d")!
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const particles = Array.from({ length: 60 }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      size: Math.random() * 2 + 0.5,
      opacity: Math.random() * 0.4 + 0.1,
    }))

    let rafId: number
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      particles.forEach(p => {
        p.x += p.vx
        p.y += p.vy
        if (p.x < 0 || p.x > canvas.width) p.vx *= -1
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2)
        ctx.fillStyle = `oklch(0.7 0.1 280 / ${p.opacity})`
        ctx.fill()
      })
      rafId = requestAnimationFrame(animate)
    }
    rafId = requestAnimationFrame(animate)
    return () => cancelAnimationFrame(rafId)
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="pointer-events-none absolute inset-0"
      aria-hidden="true"
    />
  )
}
```

---

## Intensity Scale

| Level | Technique | VRAM impact | Use for |
|---|---|---|---|
| Subtle | Static gradient + dot pattern | None | Any style |
| Low | Cursor glow (CSS custom props) | None | Dark pages |
| Medium | CSS blob animation (2–3 elements) | Low | Hero sections |
| High | Canvas particles | Medium | Creative/portfolio |
| Maximum | WebGL shader | High | Product launches |

Default to the lowest intensity that achieves the desired atmosphere.

---

## Performance Constraints

- `filter: blur()` on animated elements is the most expensive operation — test on mobile before shipping
- Canvas particle fields: keep particle count under 80 for consistent 60fps
- Cursor-reactive effects: use CSS custom properties + direct style mutation, never `setState`
- Provide `prefers-reduced-motion` fallback: static gradient, no animation

---

## Accessibility

- All ambient background elements must be `aria-hidden="true"` and `pointer-events-none`
- Never convey information through the background — it is decoration only
- Ensure sufficient contrast between background and foreground content remains at all animation states
- `prefers-reduced-motion`: remove animation, keep static version

---

## Common Pitfalls

- **Too vivid:** background oversaturates and competes with content. Desaturate, reduce opacity, increase blur.
- **Horizontal scroll:** absolute-positioned large blobs can extend beyond the viewport. `overflow-hidden` on the container.
- **No reduced motion fallback:** animated backgrounds are high-motion. Non-negotiable fallback.
- **Performance on mobile:** full-screen blur animations can drop mobile to 15fps. Profile first.
- **White mode neglect:** most ambient backgrounds are designed for dark mode. Build a light-mode variant or disable on light mode.
