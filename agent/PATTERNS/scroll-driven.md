# PATTERN — Scroll-Driven Animation

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

The scroll position drives visual state. As the user moves through the page, elements respond — revealing, transforming, progressing. Scroll animation is not decoration; it creates narrative pacing and rewards engaged reading.

---

## When to Use

- Long-form pages where progression needs to feel earned
- Landing pages where section transitions carry meaning
- Storytelling or sequential disclosure of content
- When the page itself is the primary interactive surface

Do not use on: dashboards, dense data UIs, utility pages, or anywhere rapid access to content matters. Scroll animation penalizes users who need to jump to a section.

---

## Two Implementation Approaches

### 1. CSS Scroll-Driven Animations (Native, Preferred)

The native CSS approach — zero JavaScript, compositor-threaded, performant.

```css
@keyframes fade-up {
  from { opacity: 0; translate: 0 2rem; }
  to   { opacity: 1; translate: 0 0; }
}

.scroll-reveal {
  animation: fade-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 40%;
}
```

**Key APIs:**
- `animation-timeline: scroll()` — ties animation to the root scroll position
- `animation-timeline: view()` — ties animation to the element's position within the viewport
- `animation-range: entry 0% entry 40%` — defines when in the element's viewport journey the animation runs
- `scroll-timeline-name` — named timelines for coordinating multiple elements to the same scroll

**Browser support note:** Chromium-based browsers only as of 2026. Requires fallback.

### 2. Intersection Observer (Fallback + Cross-Browser)

```tsx
const useScrollReveal = (options = {}) => {
  const ref = useRef(null)
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible")
          observer.unobserve(entry.target) // trigger once
        }
      },
      { threshold: 0.15, ...options }
    )
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])
  return ref
}
```

Pair with CSS classes:

```css
.reveal {
  opacity: 0;
  translate: 0 1.5rem;
  transition: opacity 600ms ease-out, translate 600ms ease-out;
}
.reveal.is-visible {
  opacity: 1;
  translate: 0 0;
}
```

---

## Stagger Pattern

For grouped elements (card grids, list items, feature rows):

```tsx
{items.map((item, i) => (
  <div
    key={item.id}
    ref={revealRef}
    className="reveal"
    style={{ transitionDelay: `${i * 75}ms` }}
  >
    {/* content */}
  </div>
))}
```

Keep stagger delays tight: 50–100ms between siblings. Longer delays make users wait.

---

## Parallax

Scroll position drives different translate speeds for layered elements:

```tsx
const useParallax = (speed = 0.3) => {
  const ref = useRef(null)
  useEffect(() => {
    const handleScroll = () => {
      if (!ref.current) return
      const rect = ref.current.parentElement.getBoundingClientRect()
      ref.current.style.transform = `translateY(${-rect.top * speed}px)`
    }
    window.addEventListener("scroll", handleScroll, { passive: true })
    return () => window.removeEventListener("scroll", handleScroll)
  }, [speed])
  return ref
}
```

**Parallax constraints:**
- Use only on decorative background elements, never on content text
- Speed factor 0.2–0.4 — subtle depth, not disorienting drift
- Never apply to elements with critical information
- Must be completely disabled under `prefers-reduced-motion`

---

## Progress Indicators

Scroll-linked progress bar (reading indicator):

```css
.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 2px;
  background: var(--color-primary);
  animation: progress linear;
  animation-timeline: scroll(root);
  animation-range: 0% 100%;
  transform-origin: left;
  scale: 0 1; /* scales from 0 to 1 on x-axis */
}

@keyframes progress {
  to { scale: 1 1; }
}
```

---

## Scroll-Snapping

When the page is divided into discrete sections meant to be consumed one at a time:

```css
.snap-container {
  height: 100dvh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
}

.snap-section {
  height: 100dvh;
  scroll-snap-align: start;
}
```

Use `mandatory` only when every section fills the full viewport. Use `proximity` when sections vary in height.

---

## Performance Constraints

- Animate only `opacity`, `transform` (`translate`, `scale`, `rotate`), and `filter` — these run on the compositor thread and don't trigger layout
- Never animate `height`, `width`, `top`, `left`, `margin`, or `padding` — these force layout recalculation
- Keep the number of simultaneously animated elements under 20 per viewport
- Use `will-change: transform` sparingly and only on elements actively animating — it consumes GPU memory
- `{ passive: true }` on all scroll event listeners — prevents blocking the main thread

---

## Accessibility

- Wrap all scroll animations in `@media (prefers-reduced-motion: no-preference)` in CSS, or check `window.matchMedia("(prefers-reduced-motion: reduce)")` before applying JS animations
- Content must be fully readable without animation — never use animation as the sole means of disclosure
- Avoid auto-scrolling or scroll hijacking — users control scroll position
- Parallax specifically must be fully disabled under reduced motion

---

## Fallback Requirements

- Pages must be fully readable and functional with JavaScript disabled
- Elements in `.reveal` state must still be visible (opaque, untranslated) without JS
- CSS scroll-driven animations must fall back gracefully in non-supporting browsers — use `@supports` or feature detection

---

## Common Pitfalls

- **Scroll jank:** animating layout properties instead of transforms. Profile with DevTools before shipping.
- **Too much at once:** every element on the page revealing simultaneously creates visual noise. Stagger and threshold carefully.
- **Permanent hiding:** reveal animations that never trigger because the threshold is too high, or elements are off-screen in a way IntersectionObserver misses.
- **Ignoring reduced motion:** the single most common accessibility violation in scroll animation.
- **Scroll hijacking:** overriding scroll behavior so the user loses control. Never do this.
