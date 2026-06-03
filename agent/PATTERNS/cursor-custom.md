# PATTERN — Custom Cursor

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

A custom cursor replaces or augments the browser's default cursor with a designed element that responds to context, hover targets, and interaction state. When done well, it makes the entire interface feel hand-crafted. When done poorly, it creates friction, lag, and confusion.

This pattern is for creative, portfolio, agency, and high-design contexts. It is inappropriate for functional applications, dashboards, or any UI where speed of interaction is primary.

---

## When to Use

- Portfolio sites and creative work where the cursor itself communicates personality
- Agency and studio sites where every detail is considered
- Product launches or event pages with a specific aesthetic world
- Anywhere the default cursor is aesthetically jarring relative to the design

Do not use on: SaaS applications, e-commerce checkout flows, data dashboards, or any UI where users need reliable, fast cursor feedback.

---

## Foundation: Cursor Component

Hide the native cursor, position a custom element at the mouse location:

```tsx
function CustomCursor() {
  const pos = useRef({ x: -100, y: -100 })
  const cursorRef = useRef<HTMLDivElement>(null)
  const rafId = useRef<number>()

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      pos.current = { x: e.clientX, y: e.clientY }

      // Use rAF for smooth positioning without setState overhead
      if (rafId.current) cancelAnimationFrame(rafId.current)
      rafId.current = requestAnimationFrame(() => {
        if (cursorRef.current) {
          cursorRef.current.style.transform = `translate(${pos.current.x}px, ${pos.current.y}px)`
        }
      })
    }

    window.addEventListener("mousemove", handleMouseMove, { passive: true })
    return () => {
      window.removeEventListener("mousemove", handleMouseMove)
      if (rafId.current) cancelAnimationFrame(rafId.current)
    }
  }, [])

  return (
    <div
      ref={cursorRef}
      className="pointer-events-none fixed left-0 top-0 z-[9999] -translate-x-1/2 -translate-y-1/2"
      aria-hidden="true"
    >
      <div className="h-4 w-4 rounded-full bg-foreground" />
    </div>
  )
}
```

Apply to `<html>` or the cursor wrapper: `cursor: none` in global CSS. Re-enable on the root and all children.

---

## Pattern 1: Dot + Ring (Classic Two-Layer)

A small dot at the exact cursor position, and a larger ring that follows with a lag:

```tsx
function CustomCursor() {
  const dotRef = useRef<HTMLDivElement>(null)
  const ringRef = useRef<HTMLDivElement>(null)
  const mouse = useRef({ x: -100, y: -100 })
  const ring = useRef({ x: -100, y: -100 })

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      mouse.current = { x: e.clientX, y: e.clientY }
    }
    window.addEventListener("mousemove", handleMouseMove, { passive: true })

    // Ring follows mouse with lerp (linear interpolation)
    const lerp = (a: number, b: number, t: number) => a + (b - a) * t
    const animate = () => {
      ring.current.x = lerp(ring.current.x, mouse.current.x, 0.12)
      ring.current.y = lerp(ring.current.y, mouse.current.y, 0.12)

      if (dotRef.current) {
        dotRef.current.style.transform = `translate(${mouse.current.x}px, ${mouse.current.y}px)`
      }
      if (ringRef.current) {
        ringRef.current.style.transform = `translate(${ring.current.x}px, ${ring.current.y}px)`
      }
      requestAnimationFrame(animate)
    }
    const id = requestAnimationFrame(animate)
    return () => {
      window.removeEventListener("mousemove", handleMouseMove)
      cancelAnimationFrame(id)
    }
  }, [])

  return (
    <>
      {/* Dot — exact position */}
      <div
        ref={dotRef}
        className="pointer-events-none fixed left-0 top-0 z-[9999] -translate-x-1/2 -translate-y-1/2"
        aria-hidden="true"
      >
        <div className="h-2 w-2 rounded-full bg-foreground" />
      </div>
      {/* Ring — lagged */}
      <div
        ref={ringRef}
        className="pointer-events-none fixed left-0 top-0 z-[9998] -translate-x-1/2 -translate-y-1/2"
        aria-hidden="true"
      >
        <div className="h-10 w-10 rounded-full border border-foreground/50" />
      </div>
    </>
  )
}
```

The lerp factor (0.12) controls lag — lower = more trailing, higher = more snappy. 0.08–0.15 is the natural-feeling range.

---

## Pattern 2: Cursor State Changes

Cursor transforms based on what it's hovering over — communicates interactive context:

```tsx
type CursorState = "default" | "hover" | "drag" | "text" | "link"

const CursorContext = createContext<{ setState: (s: CursorState) => void }>({ setState: () => {} })

function CustomCursor() {
  const [state, setState] = useState<CursorState>("default")
  // ... positioning logic from above

  const sizes: Record<CursorState, string> = {
    default: "h-4 w-4",
    hover: "h-12 w-12 mix-blend-difference bg-foreground",
    drag: "h-16 w-16 border-2 border-foreground bg-transparent",
    text: "h-0.5 w-5 rounded-none",
    link: "h-3 w-3",
  }

  return (
    <CursorContext.Provider value={{ setState }}>
      <div className={cn(
        "pointer-events-none fixed left-0 top-0 z-[9999] -translate-x-1/2 -translate-y-1/2 rounded-full bg-foreground transition-all duration-200",
        sizes[state]
      )} />
    </CursorContext.Provider>
  )
}

// On interactive elements
function InteractiveCard({ children }) {
  const { setState } = useContext(CursorContext)
  return (
    <div
      onMouseEnter={() => setState("hover")}
      onMouseLeave={() => setState("default")}
    >
      {children}
    </div>
  )
}
```

---

## Pattern 3: Mix-Blend-Mode Cursor

Cursor inverts or shifts colors based on what's behind it — no explicit state management needed:

```tsx
<div className="pointer-events-none fixed left-0 top-0 z-[9999] -translate-x-1/2 -translate-y-1/2">
  <div className="h-8 w-8 rounded-full bg-white mix-blend-difference" />
</div>
```

`mix-blend-difference` subtracts the cursor's color from the background — white cursor becomes black on white background, white on dark background. Visually guaranteed to be visible regardless of what's beneath it.

---

## Pattern 4: Text/Label Cursor

Cursor shows contextual text on hover — "view", "play", "drag", "read":

```tsx
function LabelCursor({ label }: { label: string | null }) {
  return (
    <div className="flex h-20 w-20 items-center justify-center rounded-full bg-foreground">
      <span className="text-xs font-medium text-background">{label}</span>
    </div>
  )
}
```

Expand the cursor smoothly: `transition: width 250ms, height 250ms, border-radius 250ms` to grow from dot to circle.

---

## Hiding the Native Cursor

```css
/* Global — hide on all elements */
*, *::before, *::after {
  cursor: none !important;
}
```

Or scoped to the page wrapper:

```tsx
<div className="[&_*]:cursor-none cursor-none">
  {/* page content */}
</div>
```

**Critical:** restore the native cursor on form inputs and text areas where selection is needed, or implement a custom text cursor variant.

---

## Performance Constraints

- Never use `useState` for cursor position — triggers re-render on every mousemove (60+ times/second)
- Use `ref` + direct DOM manipulation + `requestAnimationFrame` for all position updates
- The ring/lerp animation runs in a `requestAnimationFrame` loop — ensure cleanup on unmount to prevent memory leaks
- Keep the cursor element's DOM complexity minimal — complex SVGs or layered elements compound the rendering cost

---

## Accessibility

- Custom cursors are purely visual — they do not affect keyboard or screen reader behavior
- `aria-hidden="true"` on the cursor element at all times
- `pointer-events: none` on the cursor element — it must never intercept clicks
- Restore functional cursors (`cursor-text`, `cursor-pointer`) in the OS/browser accessibility settings — some users depend on OS-level cursor customization. Test with high-contrast mode.
- On touch devices, mouse events don't fire — hide the custom cursor entirely on touch devices

```tsx
// Hide on touch devices
useEffect(() => {
  const isTouch = window.matchMedia("(hover: none)").matches
  if (isTouch && cursorRef.current) cursorRef.current.style.display = "none"
}, [])
```

---

## Common Pitfalls

- **Lag/jank:** using `setState` for position. Use refs and direct DOM manipulation exclusively.
- **Visible on touch screens:** touch devices show a stray cursor at 0,0. Detect and hide.
- **Native cursor visible:** forgetting `cursor: none` on the root, leaving both cursors visible.
- **Not entering viewport:** cursor initialized at `(-100, -100)` but not transitioning smoothly on first entry — animate opacity in on first `mousemove`.
- **Blocking clicks:** cursor element without `pointer-events: none` intercepts all mouse events.
- **Wrong creative context:** a custom cursor on a checkout flow or form-heavy UI creates friction. Calibrate to context.
