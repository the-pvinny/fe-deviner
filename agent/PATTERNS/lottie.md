# PATTERN — Lottie / DotLottie

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Lottie plays After Effects animations exported as lightweight JSON — enabling complex, frame-accurate, vector-quality animation in the browser without video files or hand-coded CSS. The canonical use cases are: animated illustrations, icon micro-animations, loading indicators, and success/error state transitions. DotLottie (`.lottie` format) is the modern successor — smaller file size, better tooling.

---

## When to Use

- Animated illustrations that would be impossible to replicate in CSS
- Icon animations (animated send button, animated checkmark, animated menu-to-close)
- Complex loading animations beyond a spinner
- Success/error state transitions with character (confetti burst, sad face)
- Onboarding illustrations that walk through a flow step by step
- Branded motion that was designed in After Effects by a motion designer

Do not use for: simple transitions, hover effects, or anything achievable with CSS. Lottie has a non-trivial JS payload and should not replace basic animation.

---

## Formats

| Format | Extension | Notes |
|---|---|---|
| Lottie JSON | `.json` | Original format. Human-readable. Large files. |
| DotLottie | `.lottie` | Modern format. ~10x smaller. Binary. Preferred. |

Use DotLottie wherever possible. Most major design tools and Lottie platforms export both.

---

## Installation

```bash
# DotLottie (preferred — smaller, faster)
npm install @lottiefiles/dotlottie-react

# Classic Lottie JSON
npm install lottie-react
```

---

## Pattern 1: Basic DotLottie Playback

```tsx
import { DotLottieReact } from "@lottiefiles/dotlottie-react"

function AnimatedIcon() {
  return (
    <DotLottieReact
      src="/animations/success.lottie"
      loop={false}
      autoplay
      style={{ width: 120, height: 120 }}
    />
  )
}
```

---

## Pattern 2: Controlled Playback (Trigger on Event)

Play an animation in response to a user action — form submission success, button click, etc.:

```tsx
import { DotLottieReact, type DotLottie } from "@lottiefiles/dotlottie-react"
import { useRef, useCallback } from "react"

function SuccessAnimation({ show }: { show: boolean }) {
  const dotLottieRef = useRef<DotLottie | null>(null)

  const onLoad = useCallback((dotLottie: DotLottie) => {
    dotLottieRef.current = dotLottie
  }, [])

  // Play when `show` becomes true
  useEffect(() => {
    if (show && dotLottieRef.current) {
      dotLottieRef.current.play()
    }
  }, [show])

  return (
    <DotLottieReact
      src="/animations/success.lottie"
      loop={false}
      autoplay={false}
      dotLottieRefCallback={onLoad}
      style={{ width: 160, height: 160 }}
    />
  )
}
```

---

## Pattern 3: Hover-Triggered Icon Animation

An icon that plays its animation on hover and reverses on mouse leave:

```tsx
import { DotLottieReact, type DotLottie } from "@lottiefiles/dotlottie-react"

function AnimatedSendButton() {
  const dotLottieRef = useRef<DotLottie | null>(null)

  const handleMouseEnter = () => {
    dotLottieRef.current?.play()
  }

  const handleMouseLeave = () => {
    dotLottieRef.current?.stop()
  }

  return (
    <button
      className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <DotLottieReact
        src="/animations/send-icon.lottie"
        loop={false}
        autoplay={false}
        dotLottieRefCallback={ref => { dotLottieRef.current = ref }}
        style={{ width: 20, height: 20 }}
      />
      Send
    </button>
  )
}
```

---

## Pattern 4: Scroll-Triggered Animation

Play a Lottie animation when it enters the viewport:

```tsx
function ScrollLottie({ src }: { src: string }) {
  const [play, setPlay] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setPlay(true)
          observer.disconnect()
        }
      },
      { threshold: 0.4 }
    )
    if (containerRef.current) observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [])

  return (
    <div ref={containerRef}>
      <DotLottieReact
        src={src}
        autoplay={play}
        loop={false}
        style={{ width: "100%", maxWidth: 400 }}
      />
    </div>
  )
}
```

---

## Pattern 5: Lottie as Loading State

A branded loading animation instead of a generic spinner:

```tsx
function BrandLoader() {
  return (
    <div
      className="flex h-full items-center justify-center"
      role="status"
      aria-label="Loading"
    >
      <DotLottieReact
        src="/animations/loader.lottie"
        loop
        autoplay
        style={{ width: 80, height: 80 }}
      />
      <span className="sr-only">Loading...</span>
    </div>
  )
}
```

---

## Pattern 6: Segment Playback (Multi-State Animation)

A single Lottie file with multiple named segments — different states play different frame ranges:

```tsx
function MultiStateIcon({ state }: { state: "idle" | "loading" | "success" | "error" }) {
  const dotLottieRef = useRef<DotLottie | null>(null)

  const segments: Record<typeof state, [number, number]> = {
    idle:    [0, 30],
    loading: [31, 90],
    success: [91, 130],
    error:   [131, 170],
  }

  useEffect(() => {
    const instance = dotLottieRef.current
    if (!instance) return
    const [start, end] = segments[state]
    instance.setSegment(start, end)
    instance.play()
  }, [state])

  return (
    <DotLottieReact
      src="/animations/button-states.lottie"
      autoplay={false}
      loop={false}
      dotLottieRefCallback={ref => { dotLottieRef.current = ref }}
      style={{ width: 32, height: 32 }}
    />
  )
}
```

Segmented animations require the motion designer to export all states into a single file with documented frame ranges.

---

## Sourcing Animations

| Source | Format | License |
|---|---|---|
| [LottieFiles](https://lottiefiles.com) | `.json` / `.lottie` | Free + premium, check individual licenses |
| [IconScout](https://iconscout.com/lottie-animations) | `.json` | Free + premium |
| Custom (After Effects + Bodymovin plugin) | `.json` → `.lottie` | Fully owned |
| AI-generated (LottieFiles AI) | `.lottie` | Check terms |

For production use, prefer custom animations or animations with a clear commercial license. LottieFiles free tier allows personal use; commercial use requires verification per animation.

---

## Performance Constraints

- **File size:** JSON Lottie can be 50–500KB. DotLottie averages ~10× smaller. Always prefer `.lottie`.
- **Complexity:** Lottie renders via Canvas or SVG. Highly complex After Effects compositions (many layers, expressions, effects) can be slow. Request simplified exports from motion designers.
- **Multiple simultaneous Lottie instances:** each instance runs its own rendering loop. Avoid 5+ Lottie animations visible at once.
- **Lazy load:** don't fetch Lottie files until they're needed. Trigger load on scroll proximity or interaction.
- **Canvas vs SVG renderer:** Canvas is faster for complex animations; SVG is sharper for simple ones. DotLottie uses Canvas by default — good choice.

```tsx
// Lazy load — only fetch when near the viewport
const [shouldLoad, setShouldLoad] = useState(false)
// ... IntersectionObserver sets shouldLoad = true when element enters viewport

{shouldLoad && <DotLottieReact src="/animation.lottie" ... />}
```

---

## Accessibility

- Lottie animations are purely visual — no semantic content
- Wrap in a `role="img"` container with `aria-label` if the animation conveys information
- For decorative animations: `aria-hidden="true"` on the container
- Respect `prefers-reduced-motion` — pause or hide animation entirely:

```tsx
function AccessibleLottie({ src, label }: { src: string; label?: string }) {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches

  if (prefersReducedMotion) {
    // Show static fallback (first frame or an SVG/PNG alternative)
    return label ? <img src="/fallback.png" alt={label} style={{ width: 80 }} /> : null
  }

  return (
    <div role={label ? "img" : undefined} aria-label={label} aria-hidden={!label}>
      <DotLottieReact src={src} loop autoplay style={{ width: 80, height: 80 }} />
    </div>
  )
}
```

---

## Common Pitfalls

- **After Effects features that don't export:** expressions, certain effects, and 3D layers don't translate to Lottie. The motion designer must verify export in LottieFiles preview before delivering.
- **Large JSON files:** request that motion designers run files through the [LottieFiles optimizer](https://lottiefiles.com/tools/optimizer) before delivery — typically reduces file size 30–60%.
- **No reduced motion fallback:** Lottie is motion-heavy. Always provide a static fallback.
- **Using Lottie for what CSS can do:** a spinner, a simple fade, a color transition — CSS is always the right choice for these. Lottie's value is in After Effects-complexity animation.
- **Multiple loops competing for attention:** 3+ looping Lottie animations on screen simultaneously is visually chaotic and expensive. Loop only the one that's meant to be noticed.
