# PATTERN — GSAP

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

GSAP (GreenSock Animation Platform) is the professional standard for complex, coordinated, timeline-based animation. Use it when CSS transitions and `@keyframes` are insufficient: multi-element sequences, scroll-scrubbed timelines, physics-based motion, or SVG path animation. Don't reach for GSAP for simple hover transitions — CSS is cheaper and sufficient for those.

---

## When to Use GSAP Over CSS

| Scenario | CSS | GSAP |
|---|---|---|
| Hover color/opacity | ✅ | Overkill |
| Scroll reveal (simple fade in) | ✅ | Overkill |
| Multi-step sequence (A then B then C) | Awkward | ✅ |
| Scroll-scrubbed animation (tied to scroll position) | Partial (CSS scroll-driven) | ✅ ScrollTrigger |
| SVG path drawing | Fragile | ✅ |
| Stagger with complex easing | Possible | ✅ |
| Physics / inertia / momentum | ❌ | ✅ |
| Drag with momentum release | ❌ | ✅ Draggable |

---

## Installation

```bash
npm install gsap
```

GSAP core is free. ScrollTrigger, SplitText, and most plugins are included in the free tier. Club GSAP plugins (MorphSVG, DrawSVG, etc.) require a paid license.

---

## Foundation: Tweens and Timelines

```tsx
import { gsap } from "gsap"

// Single tween
gsap.to(".element", { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" })
gsap.from(".element", { opacity: 0, y: 20, duration: 0.6, ease: "power2.out" })
gsap.fromTo(".element",
  { opacity: 0, y: 20 },
  { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }
)

// Timeline — sequential animation
const tl = gsap.timeline()
tl.from(".heading",  { opacity: 0, y: 30, duration: 0.5, ease: "power2.out" })
  .from(".subtext",  { opacity: 0, y: 20, duration: 0.4, ease: "power2.out" }, "-=0.2") // overlap by 0.2s
  .from(".cta",      { opacity: 0, scale: 0.95, duration: 0.3, ease: "back.out(1.7)" }, "-=0.1")
```

The timeline position argument (`"-=0.2"`, `"+=0.1"`, `"<"`) controls timing relative to previous animation:
- `"-=0.2"` — start 0.2s before the previous animation ends (overlap)
- `"<"` — start at the same time as the previous animation
- `"+=0.3"` — start 0.3s after the previous animation ends (delay)

---

## React Integration

Always use `useGSAP` from `@gsap/react` — it handles cleanup automatically and works correctly with React's render cycles.

```bash
npm install @gsap/react
```

```tsx
import { useGSAP } from "@gsap/react"
import { gsap } from "gsap"
import { useRef } from "react"

function AnimatedHero() {
  const container = useRef<HTMLDivElement>(null)

  useGSAP(() => {
    // All GSAP code inside useGSAP is automatically cleaned up on unmount
    gsap.from(".hero-heading", {
      opacity: 0,
      y: 40,
      duration: 0.8,
      ease: "power3.out",
    })
    gsap.from(".hero-body", {
      opacity: 0,
      y: 20,
      duration: 0.6,
      delay: 0.4,
      ease: "power2.out",
    })
  }, { scope: container }) // scope limits selectors to this container

  return (
    <div ref={container}>
      <h1 className="hero-heading text-6xl font-bold">Heading</h1>
      <p className="hero-body text-lg text-muted-foreground">Body text.</p>
    </div>
  )
}
```

---

## ScrollTrigger

The most powerful feature — animation tied precisely to scroll position.

```tsx
import { ScrollTrigger } from "gsap/ScrollTrigger"
gsap.registerPlugin(ScrollTrigger)
```

### Scroll-triggered entrance

```tsx
useGSAP(() => {
  gsap.from(".feature-card", {
    opacity: 0,
    y: 60,
    duration: 0.7,
    ease: "power2.out",
    stagger: 0.1,
    scrollTrigger: {
      trigger: ".features-section",
      start: "top 75%",    // animation starts when top of section hits 75% from top of viewport
      end: "bottom 25%",
      toggleActions: "play none none reverse", // onEnter onLeave onEnterBack onLeaveBack
    },
  })
}, { scope: container })
```

**`toggleActions` options:** `play`, `pause`, `resume`, `reset`, `restart`, `complete`, `reverse`, `none`

Common combinations:
- `"play none none none"` — play once, never reverse (most common for reveals)
- `"play none none reverse"` — play on enter, reverse on leave up
- `"play pause resume none"` — pause when scrolled past

### Scroll-scrubbed animation (pinned)

Animation tied directly to scroll position — the user controls the playback by scrolling:

```tsx
useGSAP(() => {
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: ".scroll-section",
      start: "top top",
      end: "+=2000",           // pin for 2000px of scroll
      pin: true,               // pin the element while the timeline plays
      scrub: 1,                // smooth scrub — 1 = 1 second lag behind scroll
      anticipatePin: 1,
    },
  })

  tl.from(".step-1", { opacity: 0, x: -100 })
    .from(".step-2", { opacity: 0, x: 100 })
    .from(".step-3", { opacity: 0, scale: 0.8 })
}, { scope: container })
```

`scrub: true` — animation locks exactly to scroll position (no lag)
`scrub: 1` — animation lags 1 second behind scroll (smoother feel)

### Parallax with ScrollTrigger

More control than CSS parallax:

```tsx
useGSAP(() => {
  gsap.to(".parallax-element", {
    yPercent: -30,
    ease: "none",
    scrollTrigger: {
      trigger: ".parallax-section",
      start: "top bottom",
      end: "bottom top",
      scrub: true,
    },
  })
})
```

---

## Stagger Patterns

```tsx
// Basic stagger
gsap.from(".card", {
  opacity: 0,
  y: 40,
  duration: 0.5,
  ease: "power2.out",
  stagger: 0.08, // 80ms between each element
})

// Stagger from center outward
gsap.from(".grid-item", {
  opacity: 0,
  scale: 0.9,
  duration: 0.4,
  stagger: {
    amount: 0.6,       // total stagger duration shared across all elements
    from: "center",    // "start" | "end" | "center" | "random" | index number
    grid: "auto",      // enables 2D grid stagger
    axis: "x",         // for grid: stagger along x or y axis
  },
})
```

---

## SplitText (Free Tier)

GSAP's built-in text splitting — more robust than hand-rolled character splitting:

```tsx
import { SplitText } from "gsap/SplitText"
gsap.registerPlugin(SplitText)

useGSAP(() => {
  const split = new SplitText(".headline", { type: "chars,words,lines" })

  gsap.from(split.chars, {
    opacity: 0,
    y: 40,
    duration: 0.5,
    ease: "power3.out",
    stagger: 0.025,
  })

  // Clean up split on component unmount — useGSAP handles this if returned
  return () => split.revert()
}, { scope: container })
```

---

## GSAP Easing Reference

GSAP's easing is more expressive than CSS easing:

| GSAP ease | Character |
|---|---|
| `power1.out` | Subtle deceleration |
| `power2.out` | Standard, smooth |
| `power3.out` | More dramatic stop |
| `power4.out` | Heavy deceleration |
| `back.out(1.7)` | Slight overshoot on stop |
| `elastic.out(1, 0.3)` | Spring bounce |
| `bounce.out` | Physical bounce |
| `expo.out` | Fast start, long slow stop |
| `circ.out` | Circular easing |
| `none` / `linear` | Constant velocity (scrub) |

Match easing to style character:
- **Minimalist:** `power2.out` — clean, no overshoot
- **Editorial:** `power3.out` — deliberate, weighted stop
- **Glassmorphism:** `power2.inOut` or `back.out(1.2)` — physical, slight spring
- **Modernist:** `power1.inOut` or `none` (for scrub) — mechanical precision

---

## Performance Constraints

- GSAP animates `transform` and `opacity` by default — compositor-thread safe
- Never animate `width`, `height`, `top`, `left`, `margin` with GSAP any more than with CSS
- ScrollTrigger pinning (`pin: true`) changes layout significantly — test on all breakpoints
- `scrub` animations should be kept simple — complex timelines with scrub on low-end devices can drop frames
- Use `gsap.set()` for instant initial state rather than CSS — ensures consistency across browsers
- Kill ScrollTrigger instances on unmount: `useGSAP` handles this automatically; without it, use `return () => trigger.kill()`

---

## Accessibility

- Always check `prefers-reduced-motion` before initializing GSAP animations:

```tsx
useGSAP(() => {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches
  if (prefersReducedMotion) return // skip all animation, content is already visible

  gsap.from(".element", { opacity: 0, y: 30, duration: 0.6 })
}, { scope: container })
```

- Or set initial states via CSS and only animate when motion is preferred:

```css
.animate-in { opacity: 1; transform: none; } /* default: visible */
@media (prefers-reduced-motion: no-preference) {
  .animate-in { opacity: 0; transform: translateY(20px); } /* override for animatable contexts */
}
```

- GSAP's SplitText breaks text into spans — ensure screen readers still read the full text via `aria-label` on the parent

---

## Common Pitfalls

- **Using GSAP for simple hover transitions:** CSS `transition` is lighter and sufficient. GSAP for one-property hover is overkill.
- **Forgetting `useGSAP`:** using `useEffect` with GSAP in React causes double-firing in Strict Mode and memory leaks on unmount. Always use `useGSAP`.
- **Not registering plugins:** `ScrollTrigger`, `SplitText` must be registered with `gsap.registerPlugin()` before use. Do this at the module level, not inside the component.
- **Scrub on complex timelines:** timeline with 10+ tweens and `scrub: true` calculates positions on every scroll event. Keep scrubbed timelines simple.
- **Pin layout shift:** `pin: true` temporarily changes element positioning — test that surrounding content reflows correctly.
- **Selector scope:** without `{ scope: container }` in `useGSAP`, class selectors like `.card` match all `.card` elements on the page, not just the current component's.
