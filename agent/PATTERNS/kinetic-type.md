# PATTERN — Kinetic Typography

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Text that moves, transforms, or reveals over time. Kinetic type treats the heading or display text not just as content to be read, but as a visual event — the arrival of text is part of the experience. Used on hero sections, section headings, loading screens, and anywhere language is a primary design material.

---

## When to Use

- Hero headings where brand voice must land before anything else
- Section reveals where the heading is the first focal point
- Loading/splash screens where text filling time is itself the UI
- Portfolios and creative work where the type IS the design
- Anywhere a static heading feels insufficient for the weight of the content

Do not use on: body text, navigation, form labels, data tables, or any text that users need to scan repeatedly.

---

## Pattern 1: Character Stagger Reveal

Each character appears in sequence. High impact. Best for short display headings (1–5 words).

```tsx
function SplitText({ text, className }: { text: string; className?: string }) {
  return (
    <span className={cn("inline-flex flex-wrap", className)} aria-label={text}>
      {text.split("").map((char, i) => (
        <span
          key={i}
          className="inline-block animate-in fade-in slide-in-from-bottom-2 fill-mode-both"
          style={{
            animationDelay: `${i * 30}ms`,
            animationDuration: "400ms",
          }}
          aria-hidden="true"
        >
          {char === " " ? "\u00A0" : char}
        </span>
      ))}
    </span>
  )
}
```

**Stagger timing:** 20–40ms per character for fast reveals, 50–80ms for deliberate pacing. Above 100ms per character feels like lag.

**Accessibility:** The full text lives in the `aria-label` on the container; `aria-hidden="true"` on each span prevents screen readers from announcing each character individually.

---

## Pattern 2: Word Stagger Reveal

Each word appears in sequence. Better for longer headings (5–12 words). More readable than character stagger at longer lengths.

```tsx
function WordReveal({ text, className }: { text: string; className?: string }) {
  return (
    <span className={cn("inline-flex flex-wrap gap-x-[0.25em]", className)} aria-label={text}>
      {text.split(" ").map((word, i) => (
        <span key={i} className="overflow-hidden inline-block">
          <span
            className="inline-block animate-in fade-in slide-in-from-bottom-full fill-mode-both"
            style={{ animationDelay: `${i * 80}ms`, animationDuration: "500ms" }}
            aria-hidden="true"
          >
            {word}
          </span>
        </span>
      ))}
    </span>
  )
}
```

The outer `overflow-hidden` span clips the translate, so words appear to rise up from behind a line — the classic editorial reveal.

---

## Pattern 3: Scramble / Decrypt Effect

Text starts as random characters and resolves to the real text. Best for tech, cyberpunk, or editorial contexts. Never for formal or accessible-first UIs.

```tsx
const CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

function Scramble({ text, duration = 1000 }: { text: string; duration?: number }) {
  const [display, setDisplay] = useState(text.replace(/./g, () => CHARS[Math.floor(Math.random() * CHARS.length)]))

  useEffect(() => {
    const start = performance.now()
    const chars = text.split("")

    const tick = () => {
      const elapsed = performance.now() - start
      const progress = Math.min(elapsed / duration, 1)
      const resolvedCount = Math.floor(progress * chars.length)

      setDisplay(
        chars.map((char, i) =>
          i < resolvedCount
            ? char
            : CHARS[Math.floor(Math.random() * CHARS.length)]
        ).join("")
      )

      if (progress < 1) requestAnimationFrame(tick)
    }

    requestAnimationFrame(tick)
  }, [text, duration])

  return <span aria-label={text} aria-live="off">{display}</span>
}
```

---

## Pattern 4: Typewriter

Text types out character by character. Classic effect. Works for single lines or sequential multi-line reveals.

```tsx
function Typewriter({ text, speed = 50 }: { text: string; speed?: number }) {
  const [displayed, setDisplayed] = useState("")

  useEffect(() => {
    let i = 0
    const interval = setInterval(() => {
      setDisplayed(text.slice(0, ++i))
      if (i >= text.length) clearInterval(interval)
    }, speed)
    return () => clearInterval(interval)
  }, [text, speed])

  return (
    <span aria-label={text}>
      <span aria-hidden="true">{displayed}</span>
      <span className="animate-pulse">|</span>
    </span>
  )
}
```

Pair with `aria-live="polite"` on a visually-hidden span for screen reader announcement of the complete text on finish.

---

## Pattern 5: Clip-Path Reveal

Text revealed by an animated clip, as if being uncovered by a passing bar — editorial and geometric.

```css
@keyframes clip-reveal {
  from { clip-path: inset(0 100% 0 0); }
  to   { clip-path: inset(0 0% 0 0); }
}

.clip-reveal {
  animation: clip-reveal 700ms cubic-bezier(0.77, 0, 0.175, 1) forwards;
}
```

For a left-to-right reveal where a color bar passes over the text:

```tsx
<div className="relative overflow-hidden">
  <h1 className="text-6xl font-bold">{heading}</h1>
  {/* The bar that sweeps across and away */}
  <div className="absolute inset-0 bg-foreground animate-[reveal-bar_700ms_ease-in-out_forwards]" />
</div>
```

```css
@keyframes reveal-bar {
  0%   { translate: -100% 0; }
  50%  { translate: 0 0; }
  100% { translate: 100% 0; }
}
```

---

## Pattern 6: Counter / Number Animation

Numeric values count up from 0 (or a lower number) to their target — for statistics, metrics, pricing.

```tsx
function Counter({ target, duration = 1500 }: { target: number; duration?: number }) {
  const [count, setCount] = useState(0)
  const ref = useRef<HTMLSpanElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return
      observer.disconnect()

      const start = performance.now()
      const tick = () => {
        const elapsed = performance.now() - start
        const progress = Math.min(elapsed / duration, 1)
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3)
        setCount(Math.floor(eased * target))
        if (progress < 1) requestAnimationFrame(tick)
      }
      requestAnimationFrame(tick)
    })
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [target, duration])

  return <span ref={ref} aria-label={String(target)}>{count.toLocaleString()}</span>
}
```

---

## Pattern 7: Variable Font Animation

CSS-animated variable font axes — weight, width, slant change over time or on hover.

```css
.variable-heading {
  font-variation-settings: "wght" 300;
  transition: font-variation-settings 400ms ease-out;
}

.variable-heading:hover {
  font-variation-settings: "wght" 800;
}

@keyframes weight-pulse {
  0%, 100% { font-variation-settings: "wght" 300; }
  50%       { font-variation-settings: "wght" 700; }
}

.breathing-type {
  animation: weight-pulse 3s ease-in-out infinite;
}
```

**Requires:** a variable font with the relevant axes. Confirm the font supports `wght`, `wdth`, `slnt` etc. before using.

---

## Scroll-Triggered Activation

All kinetic type patterns should trigger on scroll intersection, not on page load:

```tsx
function ScrollKineticText({ children }: { children: React.ReactNode }) {
  const [active, setActive] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setActive(true); observer.disconnect() } },
      { threshold: 0.3 }
    )
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])

  return <div ref={ref} data-active={active}>{children}</div>
}
```

Use `data-active` as a CSS hook: `.element { opacity: 0 } [data-active="true"] .element { animation: ... }`.

---

## Performance Constraints

- Character and word stagger on long headings (20+ characters at 30ms delay) adds up — cap total animation time at 1.2s
- Variable font animations can cause text reflow if the weight change affects glyph width — test on all breakpoints
- Scramble effect calls `setState` on every frame — use `useRef` for the interval and only update DOM directly for high-frequency effects
- Never kinetic-animate body text — only display/heading sizes

---

## Accessibility

- Always provide the complete text in an `aria-label` on the wrapper
- Mark individual animated spans with `aria-hidden="true"` to prevent character-by-character announcement
- Typewriter and scramble effects must be `aria-live="off"` during animation, then announce the complete text on finish
- All animations must be disabled or instant under `prefers-reduced-motion` — the text should appear immediately, fully formed

---

## Common Pitfalls

- **Too long:** character stagger on a 15-word heading takes 12+ seconds. Strictly for short display text.
- **No reduced motion fallback:** kinetic type with no fallback is inaccessible and often nauseating
- **Scramble on important content:** scramble reads as error or corruption to users unfamiliar with it — use in clearly creative contexts only
- **Re-triggering on scroll:** if reveal re-runs every time the element enters the viewport, use `.disconnect()` after first trigger
- **Variable font not loading:** if the variable font fails to load, axis animations have no effect — ensure font loading is robust
