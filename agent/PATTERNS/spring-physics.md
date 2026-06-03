# PATTERN — Spring Physics Animation

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Most web animation is duration-based: define a start state, an end state, a duration in milliseconds, and an easing curve. The browser interpolates for exactly that duration. This works for designed sequences — page-load reveals, branded intros, staggered lists.

Physics-based animation works differently. Instead of a fixed duration, you define the physical properties of a spring — stiffness, damping, mass — and the animation runs until the spring settles. There is no predetermined end time. The result: motion that feels organic, handles interruptions gracefully, and inherits velocity from preceding gestures.

**Use spring physics for anything the user can interrupt.** Use duration-based animation for designed sequences.

---

## When to Use

- Interactive elements the user can hover, click, tap, or drag
- Gesture-driven interactions where the animation must inherit drag velocity
- List reordering and layout shifts where position changes are unpredictable
- Modal, drawer, and sheet enter/exit that should feel physical
- Any element that needs to respond gracefully when the user changes their mind mid-animation

Do not reach for spring physics when:
- The animation must match precise timing (audio sync, step-by-step tutorial)
- The element is decorative and the user cannot interrupt it
- The project already uses GSAP for everything — GSAP's `elastic` easing approximates springs adequately for non-interactive sequences

---

## The Core Distinction

| | Duration-based (tween) | Spring / physics-based |
|---|---|---|
| Defined by | Duration + easing curve | Mass + tension + friction |
| Duration | Fixed, predictable | Variable — runs until settled |
| Interruption | Jumps or resets abruptly | Continues with current velocity into new target |
| Overshoot | Never (easing reaches target exactly) | Natural — spring bounces past then settles |
| Gesture integration | Awkward — drag velocity is discarded | Natural — spring inherits gesture velocity |
| Best for | Designed sequences, reveals, brand animation | Interactive elements, gestures, list reordering |

The failure mode of duration-based animation under interaction: hover over a card, triggering a scale-up; move away halfway through. A tween resets abruptly. A spring carries the current upward momentum into the new target — the reversal feels like a physical object, not a state machine resetting.

---

## Spring Parameters

Three parameters govern all spring behaviour:

| Parameter | Alias | Effect |
|---|---|---|
| **Tension** | Stiffness | Higher = faster, snappier spring. Lower = slower, lazier |
| **Friction** | Damping | Higher = less overshoot, settles faster. Lower = more bounce |
| **Mass** | — | Higher = heavier, takes longer to accelerate and decelerate |

**Personalities:**
- **High tension + high friction** — snappy, no bounce. Good iOS tap feedback character.
- **High tension + low friction** — fast with significant overshoot and oscillation.
- **Low tension + low friction** — slow, floaty, bouncy.

---

## React Spring

A React animation library built entirely around spring physics. Every animated value is a spring. Bypasses React reconciliation per frame — writes to the DOM directly via `useRef`. Extremely performant for rapid continuous updates.

```bash
npm install @react-spring/web @use-gesture/react
```

### Built-in presets

```tsx
import { config } from "@react-spring/web"

config.default   // { tension: 170, friction: 26 }  — general purpose
config.gentle    // { tension: 120, friction: 14 }  — soft, organic
config.wobbly    // { tension: 180, friction: 12 }  — bouncy
config.stiff     // { tension: 210, friction: 20 }  — snappy, no bounce
config.slow      // { tension: 280, friction: 60 }  — heavy, deliberate
config.molasses  // { tension: 280, friction: 120 } — very slow
```

### `useSpring` — single element

```tsx
import { useSpring, animated } from "@react-spring/web"

function Card({ isOpen }: { isOpen: boolean }) {
  const styles = useSpring({
    scale: isOpen ? 1.05 : 1,
    opacity: isOpen ? 1 : 0.7,
    config: { tension: 200, friction: 20 },
  })

  return (
    <animated.div style={styles} className="rounded-xl border border-border bg-card p-6">
      {/* content */}
    </animated.div>
  )
}
```

### `useTrail` — staggered spring chain

Each element's spring starts when the previous one has moved — creating an organic cascade rather than a mechanical uniform delay:

```tsx
import { useTrail, animated } from "@react-spring/web"

function List({ items, open }: { items: string[]; open: boolean }) {
  const trail = useTrail(items.length, {
    opacity: open ? 1 : 0,
    y: open ? 0 : 20,
    config: config.gentle,
  })

  return (
    <ul className="space-y-2">
      {trail.map((styles, i) => (
        <animated.li key={i} style={styles} className="rounded-lg border border-border bg-card p-3">
          {items[i]}
        </animated.li>
      ))}
    </ul>
  )
}
```

### `useTransition` — enter and exit

```tsx
import { useTransition, animated } from "@react-spring/web"

function ToastList({ toasts }: { toasts: Array<{ id: string; message: string }> }) {
  const transitions = useTransition(toasts, {
    keys: t => t.id,
    from:  { opacity: 0, y: -16, scale: 0.96 },
    enter: { opacity: 1, y: 0,   scale: 1 },
    leave: { opacity: 0, y: 8,   scale: 0.96 },
    config: config.stiff,
  })

  return (
    <div className="fixed bottom-4 right-4 flex flex-col gap-2">
      {transitions((styles, toast) => (
        <animated.div
          style={styles}
          className="rounded-lg border border-border bg-card px-4 py-3 shadow-lg"
        >
          {toast.message}
        </animated.div>
      ))}
    </div>
  )
}
```

### Gesture integration with `@use-gesture`

Spring + gesture is where physics animation pays off most clearly. On release, the spring inherits the gesture's velocity — the card throws in the direction of the swipe and snaps back:

```tsx
import { useSpring, animated } from "@react-spring/web"
import { useDrag } from "@use-gesture/react"

function DraggableCard() {
  const [{ x, y }, api] = useSpring(() => ({ x: 0, y: 0 }))

  const bind = useDrag(({ offset: [ox, oy], velocity: [vx, vy], last }) => {
    if (last) {
      // Release: snap back with inherited velocity
      api.start({
        x: 0,
        y: 0,
        config: { velocity: [vx, vy], tension: 180, friction: 30 },
      })
    } else {
      api.start({ x: ox, y: oy, immediate: true })
    }
  })

  return (
    <animated.div
      {...bind()}
      style={{ x, y, touchAction: "none" }}
      className="cursor-grab rounded-xl border border-border bg-card p-6 shadow-md active:cursor-grabbing"
    />
  )
}
```

---

## Framer Motion

Framer Motion supports both duration-based tweens and spring physics through its `transition` prop. Springs are accessed by setting `type: "spring"`.

```bash
npm install framer-motion
```

### Spring transition

```tsx
import { motion } from "framer-motion"

function Modal({ isOpen }: { isOpen: boolean }) {
  return (
    <motion.div
      initial={{ scale: 0.92, opacity: 0 }}
      animate={{ scale: isOpen ? 1 : 0.92, opacity: isOpen ? 1 : 0 }}
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 30,
        mass: 1,
      }}
      className="rounded-xl border border-border bg-card p-6 shadow-xl"
    />
  )
}
```

Framer Motion's `stiffness` and `damping` map to React Spring's `tension` and `friction` concepts — the numeric ranges differ but the behaviour model is identical.

### Layout animations — springs by default

Framer Motion's layout animation system, which animates elements when their DOM position changes, uses springs automatically. This is one of the most compelling use cases: layout shifts where the destination position is unknown at authoring time.

```tsx
// When this element's size or position changes (filtering, reordering),
// it animates there via spring — no position calculation needed
<motion.div layout className="rounded-lg border border-border bg-card p-4">
  {content}
</motion.div>
```

### Shared layout with `layoutId`

The most visually powerful spring pattern — an element morphs between its positions in two different render contexts:

```tsx
// List view: thumbnail
<motion.div layoutId={`card-${id}`} className="rounded-lg overflow-hidden">
  <motion.h2 layoutId={`title-${id}`} className="text-sm font-medium">{title}</motion.h2>
</motion.div>

// Expanded modal view: the browser animates between the two via spring
<motion.div layoutId={`card-${id}`} className="fixed inset-4 rounded-2xl overflow-hidden">
  <motion.h2 layoutId={`title-${id}`} className="text-2xl font-bold">{title}</motion.h2>
</motion.div>
```

### Reduced motion configuration

```tsx
import { MotionConfig } from "framer-motion"

// Wrap your app — all children automatically respect OS reduced-motion preference
<MotionConfig reducedMotion="user">
  <App />
</MotionConfig>
```

---

## GSAP Elastic — Spring Approximation

GSAP is duration-based at its core. Its `elastic` easing family approximates spring behaviour within a fixed duration — it **looks** like a spring but cannot inherit gesture velocity:

```tsx
// Use for designed sequences where timing is known
gsap.to(".button", {
  scale: 1.1,
  duration: 0.6,
  ease: "elastic.out(1, 0.3)",
  // amplitude: 1, period: 0.3
  // period is roughly inverse tension; amplitude controls overshoot
})
```

Use GSAP elastic for designed sequences. Use React Spring or Framer Motion for interactive, interruptible elements.

---

## CSS Spring — Zero Dependencies

A `cubic-bezier` with y-values outside the 0–1 range creates an overshoot effect without any JavaScript:

```css
.button {
  transition: transform 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.button:hover {
  transform: scale(1.05);
}
```

The `1.56` y-value is above 1, causing the scale to overshoot 1.05 slightly before settling — a spring-like feel with zero dependencies. Valid for simple hover states on non-interactive sequences.

Useful cubic-bezier spring presets:
```css
/* Gentle overshoot */
cubic-bezier(0.34, 1.56, 0.64, 1)

/* More bounce */
cubic-bezier(0.175, 0.885, 0.32, 1.275)

/* Very bouncy */
cubic-bezier(0.68, -0.6, 0.32, 1.6)
```

---

## Choosing an Approach

| Scenario | Reach for |
|---|---|
| Designed page-load sequence (reveal, hero) | Duration-based: GSAP or CSS |
| Interactive element user can hover or tap | Spring: Framer Motion or React Spring |
| Animation must match precise timing (audio sync) | Duration-based: GSAP timeline |
| Gesture-driven (drag, swipe, throw) | Spring: React Spring + `@use-gesture` |
| List reordering or layout shifts | Spring: Framer Motion `layout` |
| State machine with multiple entry/exit paths | Spring: Framer Motion `useTransition` or variants |
| No React, no library | CSS `cubic-bezier` with y > 1 |

---

## Performance

- React Spring bypasses React's render cycle per frame — animated values go directly to the DOM via `useRef`. Very performant for continuous interactions.
- Framer Motion uses WAAPI (Web Animations API) where available for GPU-accelerated animation; falls back to `requestAnimationFrame`.
- Spring animations that animate `transform` and `opacity` are GPU-accelerated. Springs driving layout properties (`width`, `height`, `top`) cause reflow every frame — never do this.
- Use `will-change: transform` on elements during continuous spring animation; remove it after settling.
- `config: { clamp: true }` in React Spring stops exactly at the target — useful on low-end devices where oscillation adds CPU cost.

---

## Accessibility

All spring animations are motion and must respect `prefers-reduced-motion`:

```tsx
// React Spring — manual check
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches

const styles = useSpring({
  opacity: visible ? 1 : 0,
  y: visible ? 0 : 20,
  config: prefersReducedMotion ? { duration: 0 } : config.gentle,
})
```

```tsx
// Framer Motion — automatic via MotionConfig
<MotionConfig reducedMotion="user">
  <App />
</MotionConfig>
```

For reduced-motion users: remove translate and scale animations; keep opacity transitions at short durations (100–150ms). The interface must remain fully functional without motion.

---

## Common Pitfalls

- **Spring on layout properties** — `width`, `height`, `top`, `left` cause layout reflow every frame. Always spring `transform` and `opacity`.
- **GSAP elastic as a substitute** — GSAP's elastic easing looks like a spring but discards gesture velocity on interruption. Use true spring physics (React Spring, Framer Motion) for any element the user can interrupt.
- **Infinite oscillation** — very low friction combined with small mass causes visible oscillation that never settles. Use `config.stiff` or `config.gentle` presets as a starting point rather than manual parameters.
- **Missing reduced-motion gate** — spring animations, especially those with overshoot, are intense for users with vestibular disorders. Always gate on `prefers-reduced-motion`.
- **Overusing spring everywhere** — spring is the right choice for interactive elements. Designed sequences (hero reveals, page entrance) don't benefit from physics and the variable duration makes them harder to choreograph.
- **React Spring without `animated.*`** — using `useSpring` but applying values to a regular `<div>` bypasses the performance optimization. Always use `animated.div`, `animated.span`, etc.
