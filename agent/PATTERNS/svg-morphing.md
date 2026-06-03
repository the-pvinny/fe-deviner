# PATTERN — SVG Morphing

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

SVG morphing animates between two vector shapes by interpolating the path data (`d` attribute) of an SVG `<path>` element. The result is an organic, fluid shape transition — a circle becoming a star, a hamburger icon becoming a close icon, a blob reforming on scroll.

The fundamental constraint: **both shapes must have the same number of path commands and command types** for simple interpolation to work. Mismatched paths produce distorted or broken morphs. This constraint is what makes morphing harder than other SVG animations, and why specialized libraries exist to solve it.

---

## When to Use

- Icon state transitions (hamburger → close, play → pause, search → back)
- Logo reveals and morph sequences in brand animations
- Ambient blob backgrounds that slowly reform over time
- Scroll-driven shape transformations tied to `ScrollTrigger`
- Data visualisation transitions where bars or areas change shape

Do not use when:
- A simple opacity swap or slide transition would communicate the state change equally well
- The animation will run on low-powered mobile devices with complex paths (CPU-intensive)
- Safari/Firefox compatibility is required for CSS `d` property animation

---

## How It Works

An SVG path is defined by its `d` attribute: a string of commands (`M`, `L`, `C`, `Q`, `A`, `Z`) and coordinate pairs. Morphing interpolates those coordinates — at each frame, every control point moves toward its target position.

The constraint: both paths must have compatible structures for direct interpolation. Libraries solve this in two ways:
1. **Normalizing** — converting all path commands to a common type (cubic beziers) then redistributing points
2. **Perimeter sampling** — resampling both shapes along their perimeter at the same density, bypassing command-type constraints entirely (Flubber's approach)

---

## Approach 1: CSS `d` Property

The platform-native approach — no JavaScript required:

```css
.icon-path {
  transition: d 300ms ease-in-out;
}

.icon-path.is-open {
  d: path("M18 6L6 18M6 6l12 12");  /* ✕ close icon */
}
```

```tsx
<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true">
  <path
    className={cn(
      "fill-none stroke-current stroke-2",
      "transition-[d] duration-300 ease-in-out",
      isOpen ? "[d:path('M18_6L6_18M6_6l12_12')]" : "[d:path('M3_12h18M3_6h18M3_18h18')]"
    )}
    strokeLinecap="round"
  />
</svg>
```

**Browser support (2025):** Chrome 52+, Edge 79+ ✅ — Firefox ❌ — Safari ❌

- Paths must have identical point counts and command types — no automatic normalization
- Not GPU-accelerated — `d` mutations are CPU-bound repaints
- Feature-detect before using: `CSS.supports("d", 'path("")')`
- **Not suitable for production without a JS fallback** — use Approach 3 for cross-browser work

---

## Approach 2: SMIL `<animate>`

The original SVG animation spec — self-contained, zero JavaScript:

```tsx
<path d="M10,10 L90,10 L50,90 Z">
  <animate
    attributeName="d"
    from="M10,10 L90,10 L50,90 Z"
    to="M50,10 L90,90 L10,90 Z"
    dur="1s"
    repeatCount="indefinite"
  />
</path>
```

Broad browser support but not recommended for new work: no programmatic control, difficult to pause or tie to user interaction, same point-count constraint applies.

---

## Approach 3: JavaScript Libraries (Production Recommended)

The practical choice. Libraries handle path normalization, point redistribution, and cross-browser compatibility.

### Library Comparison

| Library | Mismatched point counts | License | Bundle size | ~Desktop fps |
|---|---|---|---|---|
| GSAP MorphSVGPlugin | ✅ Automatic | Club GreenSock (paid) | ~8 KB | ~59 fps |
| Flubber | ✅ Perimeter redistribution | MIT | ~12 KB | ~55 fps |
| anime.js | ❌ Must match manually | MIT | ~17 KB | ~55 fps |
| Motion + Flubber | ✅ Via Flubber | MIT | ~22 KB total | ~55 fps |

Performance note: morphing drops significantly on mobile (~28 fps at 85% CPU for complex GSAP morphs). Simplify paths for mobile targets.

---

## GSAP MorphSVGPlugin

The most capable solution. Automatically converts all paths to cubic beziers, adds anchor points as needed, and supports `shapeIndex` tuning to control how sub-paths align — eliminating the "tangling" artefact where morphing paths twist through each other.

Requires a Club GreenSock membership (~$150/yr; free for CodePen/development use):

```tsx
import { useEffect, useRef } from "react"
import { gsap } from "gsap"
import { MorphSVGPlugin } from "gsap/MorphSVGPlugin"

gsap.registerPlugin(MorphSVGPlugin)

function MorphIcon({ isActive }: { isActive: boolean }) {
  const pathRef = useRef<SVGPathElement>(null)

  useEffect(() => {
    if (!pathRef.current) return

    gsap.to(pathRef.current, {
      duration: 0.5,
      morphSVG: isActive ? "#target-shape" : "#source-shape",
      ease: "power2.inOut",
    })
  }, [isActive])

  return (
    <svg viewBox="0 0 100 100" width="40" height="40">
      {/* Hidden target shape for GSAP to read */}
      <path id="source-shape" d="M50,10 L90,90 L10,90 Z" style={{ display: "none" }} />
      <path id="target-shape" d="M10,10 L90,10 L90,90 L10,90 Z" style={{ display: "none" }} />

      {/* Animating path */}
      <path ref={pathRef} d="M50,10 L90,90 L10,90 Z" className="fill-primary" />
    </svg>
  )
}
```

### `shapeIndex` — eliminating the twist

When two shapes morph, GSAP must decide which points correspond to which. The wrong mapping produces a shape that twists through itself during the transition. `shapeIndex` controls the rotational alignment:

```tsx
gsap.to("#shape", {
  morphSVG: {
    shape: "#target",
    shapeIndex: 3,      // try 0–9 to find the least-twist alignment
    type: "rotational", // or "linear"
  },
  duration: 1,
})
```

Tune `shapeIndex` visually — scrub through the animation at slow speed, pick the value that produces the cleanest path.

### Scroll-driven morph

```tsx
gsap.to("#blob", {
  morphSVG: "#blob-alt",
  ease: "none",
  scrollTrigger: {
    trigger: ".morph-section",
    start: "top center",
    end: "bottom center",
    scrub: true,  // ties morph progress directly to scroll position
  },
})
```

---

## Flubber (Open Source)

Noah Veltman's MIT-licensed library. Works by resampling both shapes' perimeters at equal density before interpolating — a 3-point triangle can morph to a 10-point star without manual matching:

```bash
npm install flubber
```

```tsx
import { interpolate } from "flubber"
import { useEffect, useRef } from "react"

function FlubberMorph({
  from,
  to,
  duration = 800,
}: {
  from: string
  to: string
  duration?: number
}) {
  const pathRef = useRef<SVGPathElement>(null)

  useEffect(() => {
    if (!pathRef.current) return

    const mixPaths = interpolate(from, to, {
      maxSegmentLength: 2, // lower = smoother but more CPU; 2–4 is a good range
    })

    let start: number | null = null
    let frame: number

    const animate = (timestamp: number) => {
      if (!start) start = timestamp
      const progress = Math.min((timestamp - start) / duration, 1)
      pathRef.current!.setAttribute("d", mixPaths(progress))
      if (progress < 1) frame = requestAnimationFrame(animate)
    }

    frame = requestAnimationFrame(animate)
    return () => cancelAnimationFrame(frame)
  }, [from, to, duration])

  return (
    <svg viewBox="0 0 100 100" width="60" height="60">
      <path ref={pathRef} d={from} className="fill-primary" />
    </svg>
  )
}
```

`maxSegmentLength` is the key tuning parameter — it controls how densely points are sampled along each shape's perimeter. Lower values produce smoother morphs at higher CPU cost. A value of 2–4 is a practical starting point.

---

## anime.js (Icon Toggles)

For simple icon toggles where both states can be authored with matching path structures, anime.js is lightweight and dependency-free from the paid GSAP ecosystem:

```bash
npm install animejs
```

```tsx
import anime from "animejs"
import { useEffect, useRef } from "react"

function HamburgerToggle({ isOpen }: { isOpen: boolean }) {
  const pathRef = useRef<SVGPathElement>(null)

  useEffect(() => {
    if (!pathRef.current) return

    anime({
      targets: pathRef.current,
      d: [
        { value: "M3 12h18M3 6h18M3 18h18" },  // hamburger (matching point count)
        { value: "M18 6L6 18M6 6l12 12" },       // close ✕
      ][isOpen ? 1 : 0],
      easing: "easeInOutQuad",
      duration: 250,
    })
  }, [isOpen])

  return (
    <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true">
      <path
        ref={pathRef}
        d="M3 12h18M3 6h18M3 18h18"
        className="fill-none stroke-current stroke-2"
        strokeLinecap="round"
      />
    </svg>
  )
}
```

**Important:** anime.js requires manually matched point counts. Both the hamburger and close paths above must have the same number of commands — verify before animating.

---

## Use Case Reference

| Use case | Recommended approach | Notes |
|---|---|---|
| Icon toggle (hamburger, play/pause) | CSS `d` with fallback, or anime.js | Same-structure paths; keep it simple |
| Logo reveal / complex morph | GSAP MorphSVGPlugin | Handles incompatible points; `shapeIndex` needed |
| Ambient blob background | CSS `border-radius` 8-value animation (see `ambient-background.md`) or Flubber | Low fps (15–24fps) is acceptable for blobs |
| Scroll-driven state change | GSAP MorphSVG + ScrollTrigger `scrub` | Ties morph progress to scroll position |
| Data visualisation transitions | D3 + `d3-interpolate-path` | Topology-preserving; integrates with D3 scales |
| Character or face animation | GSAP MorphSVGPlugin | Multiple sub-paths; `shapeIndex` critical |

---

## Authoring Paths for Morphing

SVG files exported from Illustrator or Figma rarely have morph-compatible paths by default:

- **Simplify before export** — reduce anchor points in Illustrator (`Object → Path → Simplify`) or Figma's vector edit mode. Fewer points = faster morph = better mobile performance.
- **Match structure intentionally** — for simple icon toggles, author both states with the same number of points in the same order.
- **Use SVGOMG** to optimize exported SVGs and inspect the resulting `d` commands.
- **Avoid compound paths** for morph targets — split into individual `<path>` elements and morph them independently.
- GSAP's `MorphSVGPlugin.convertToPath()` converts primitives (`<circle>`, `<rect>`, `<polygon>`) to path strings for use as morph targets.

---

## Performance

Animating the `d` attribute is **not GPU-accelerated** — it triggers CPU-bound repaint on every frame, unlike `transform` or `opacity`.

| Scenario | ~Desktop CPU | ~Mobile CPU | Mobile fps |
|---|---|---|---|
| Complex GSAP morph (20+ points) | ~20% | ~85% | ~28 fps |
| Simple Flubber morph (6–8 points) | ~8% | ~40% | ~45 fps |
| CSS `d` property (4 points) | ~5% | ~25% | ~55 fps |

Mitigation:
- For blob backgrounds: keep paths to 5–8 anchor points; set duration to 2–4s; drop to 15fps with `setInterval` instead of `requestAnimationFrame`
- For interactive morphs: simplify paths before use; prefer durations under 500ms
- `will-change: d` does not GPU-accelerate the `d` attribute but hints browser to pre-composite the layer — use sparingly

---

## Accessibility

```tsx
const motionOK = !window.matchMedia("(prefers-reduced-motion: reduce)").matches

function AnimatedIcon({ isPlaying }: { isPlaying: boolean }) {
  const pathRef = useRef<SVGPathElement>(null)

  useEffect(() => {
    if (!pathRef.current) return

    if (motionOK) {
      // Animate morphing
      gsap.to(pathRef.current, {
        morphSVG: isPlaying ? "#pause-shape" : "#play-shape",
        duration: 0.35,
      })
    } else {
      // Instant swap for reduced-motion users
      pathRef.current.setAttribute("d", isPlaying ? pausePath : playPath)
    }
  }, [isPlaying])

  return (
    // ARIA label must update — the visual morph alone is insufficient for screen readers
    <button aria-label={isPlaying ? "Pause" : "Play"} aria-pressed={isPlaying}>
      <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true">
        <path ref={pathRef} d={playPath} />
      </svg>
    </button>
  )
}
```

Two requirements:
1. **Gate morphing behind `prefers-reduced-motion`** — replace with an instant `setAttribute` for users who have motion sensitivity
2. **Update `aria-label` independently** — the visual shape change communicates nothing to screen readers; the accessible name must change separately

---

## Common Pitfalls

- **Mismatched point counts without a normalizing library** — produces distorted, broken morphs. Either author matching paths manually or use GSAP/Flubber.
- **CSS `d` in production without a fallback** — Firefox and Safari do not support CSS `d` property animation. Feature-detect or use a JS library.
- **Complex path on mobile** — a 20-point path morphing at 0.3s duration runs at 85% CPU on mobile. Test on a mid-range Android before shipping.
- **GSAP elastic as a morph substitute** — elastic easing makes an element bounce; it does not morph a shape. These are unrelated techniques.
- **Forgetting `aria-label` update** — the icon changes visually but the button name stays "Play" while it is now the pause icon. Always update accessible names to match the new state.
- **Morphing compound paths** — a shape with multiple disconnected sub-paths (a letter with a counter, an icon with separate parts) does not morph cleanly as a single element. Split into individual `<path>` elements.
- **`shapeIndex` not tuned** — when using GSAP on complex shapes, the default `shapeIndex` often produces a twist artefact. Always tune `shapeIndex` visually for multi-point morphs.
