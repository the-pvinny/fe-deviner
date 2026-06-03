# PATTERN — Hover Micro-Interactions

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Micro-interactions are the tactile layer of a UI. They confirm that an element is interactive, provide feedback, communicate state, and add personality. Good micro-interactions are immediate, purposeful, and proportional — the feedback matches the weight of the action.

---

## When to Use

On every interactive element as a baseline. The question is not whether to use hover interactions — it is what character they should have. Micro-interactions should be calibrated per style (see STYLES/ files), but never absent.

---

## Baseline — Every Interactive Element

```tsx
// Minimum: transition on all state changes
className="transition-colors duration-150 ease-out"

// With focus
className="transition-colors duration-150 ease-out focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
```

Interactive elements without transitions feel broken. Even a `duration-100` color change is better than instant.

---

## Button Patterns

### Lift (depth simulation)

```tsx
className="shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 active:shadow-sm transition-all duration-200 ease-out"
```

### Fill sweep (background wipes in from one side)

```tsx
// Uses after: pseudo-element — requires Tailwind arbitrary variants or @layer
className={cn(
  "relative overflow-hidden",
  "after:absolute after:inset-0 after:bg-primary after:origin-left",
  "after:scale-x-0 hover:after:scale-x-100 after:transition-transform after:duration-300 after:ease-out",
  "hover:text-primary-foreground transition-colors duration-300"
)}
```

### Press (scale down on active)

```tsx
className="active:scale-[0.97] transition-transform duration-75 ease-in"
```

---

## Link and Text Patterns

### Underline reveal (slide in from left)

```tsx
className={cn(
  "relative",
  "after:absolute after:bottom-0 after:left-0 after:h-px after:w-full after:bg-current",
  "after:origin-left after:scale-x-0 hover:after:scale-x-100",
  "after:transition-transform after:duration-300 after:ease-out"
)}
```

### Underline thickness (grows on hover)

```tsx
className="underline underline-offset-2 decoration-1 hover:decoration-2 transition-all duration-200"
```

### Color shift

```tsx
className="text-muted-foreground hover:text-foreground transition-colors duration-200"
```

---

## Card Patterns

### Lift

```tsx
className="shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 ease-out"
```

### Border reveal (border appears on hover)

```tsx
className="border border-transparent hover:border-border transition-colors duration-200"
```

### Background shift

```tsx
className="bg-card hover:bg-accent/50 transition-colors duration-200"
```

### Image zoom (zoom inside a clipped container)

```tsx
<div className="overflow-hidden rounded-lg">
  <img
    className="w-full transition-transform duration-500 ease-out hover:scale-105"
    src={src}
    alt={alt}
  />
</div>
```

---

## Icon Patterns

### Rotate on hover

```tsx
<ChevronRight className="transition-transform duration-200 group-hover:translate-x-1" />
<ArrowRight className="transition-transform duration-300 group-hover:translate-x-2" />
<ExternalLink className="transition-transform duration-200 group-hover:rotate-12" />
```

Using `group` / `group-hover:` on the parent allows the icon to respond to hovering the parent:

```tsx
<a href={url} className="group flex items-center gap-2">
  <span>Read more</span>
  <ArrowRight className="transition-transform duration-300 group-hover:translate-x-1" />
</a>
```

---

## Reveal Patterns

### Content reveal on hover (caption, label, action)

```tsx
<div className="group relative overflow-hidden">
  <img src={src} alt={alt} className="w-full" />
  <div className={cn(
    "absolute inset-0 flex items-end bg-gradient-to-t from-foreground/80 to-transparent p-4",
    "translate-y-full transition-transform duration-300 ease-out",
    "group-hover:translate-y-0"
  )}>
    <p className="text-sm text-white">{caption}</p>
  </div>
</div>
```

### Tooltip reveal

```tsx
<div className="group relative">
  <button aria-describedby="tooltip">{children}</button>
  <div
    id="tooltip"
    role="tooltip"
    className={cn(
      "absolute bottom-full left-1/2 mb-2 -translate-x-1/2",
      "rounded-md bg-foreground px-2 py-1 text-xs text-background",
      "opacity-0 translate-y-1 transition-all duration-150 ease-out",
      "group-hover:opacity-100 group-hover:translate-y-0"
    )}
  >
    {label}
  </div>
</div>
```

---

## Cursor Proximity Effects

Elements that respond to cursor distance without requiring a direct hover target:

```tsx
const useProximity = (radius = 100) => {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      const el = ref.current
      if (!el) return
      const rect = el.getBoundingClientRect()
      const cx = rect.left + rect.width / 2
      const cy = rect.top + rect.height / 2
      const dx = e.clientX - cx
      const dy = e.clientY - cy
      const dist = Math.sqrt(dx * dx + dy * dy)
      const proximity = Math.max(0, 1 - dist / radius)

      el.style.setProperty("--proximity", String(proximity))
    }

    window.addEventListener("mousemove", handleMouseMove, { passive: true })
    return () => window.removeEventListener("mousemove", handleMouseMove)
  }, [radius])

  return ref
}
```

Use `var(--proximity)` in CSS to drive opacity, scale, or color intensity.

---

## Magnetic Elements

Element shifts toward the cursor when nearby — used on buttons and CTAs for high-end feel:

```tsx
const useMagnetic = (strength = 0.3) => {
  const ref = useRef<HTMLElement>(null)

  const handleMouseMove = (e: MouseEvent) => {
    const el = ref.current
    if (!el) return
    const rect = el.getBoundingClientRect()
    const x = (e.clientX - (rect.left + rect.width / 2)) * strength
    const y = (e.clientY - (rect.top + rect.height / 2)) * strength
    el.style.transform = `translate(${x}px, ${y}px)`
  }

  const handleMouseLeave = () => {
    if (ref.current) ref.current.style.transform = ""
  }

  return { ref, onMouseMove: handleMouseMove, onMouseLeave: handleMouseLeave }
}
```

Strength 0.2–0.4 feels natural. Above 0.5 feels glitchy. Always pair with `transition: transform 400ms ease-out` on mouse leave for smooth return.

---

## Performance Constraints

- Only animate `transform` and `opacity` — never `width`, `height`, `margin`, or `border-width`
- Throttle `mousemove` handlers with `requestAnimationFrame`
- Remove event listeners on unmount — memory leak risk in SPAs
- Test proximity/magnetic effects on low-end hardware — `mousemove` fires constantly

---

## Accessibility

- All hover interactions must also respond to focus (keyboard users don't hover)
- Use `focus-visible:` not `focus:` to avoid outline on mouse click
- Tooltip content must be accessible to screen readers via `role="tooltip"` and `aria-describedby`
- Never use hover as the only way to access content — tooltips must also be reachable via keyboard
- Respect `prefers-reduced-motion` — disable translate/scale effects, keep color transitions

```tsx
// Safe pattern: color always transitions, transform respects motion preference
className="transition-colors duration-200 motion-safe:hover:-translate-y-0.5 motion-safe:transition-all"
```

---

## Common Pitfalls

- **Too many simultaneous effects:** hover that changes color + shadow + scale + border all at once. Pick 1–2 properties per element.
- **Asymmetric timing:** hover-in at `duration-150` but hover-out at `duration-150` via CSS default (immediate). Add explicit transition on the base state so leave is also smooth.
- **Missing active state:** hover without an active/pressed state feels unresponsive. Always pair hover with `active:`.
- **Overflow not hidden on zoom:** image zoom without `overflow-hidden` on the container bleeds into surrounding layout.
- **Magnetic too strong:** shift > 10–15px feels like broken positioning to users.
