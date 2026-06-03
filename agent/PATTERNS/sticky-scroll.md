# PATTERN — Sticky Scroll

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Elements that remain fixed in the viewport while the rest of the page scrolls — creating spatial layers, maintaining context across a long scroll journey, and linking scroll position to visible state. Sticky scroll tells a sequential story where position in the page maps directly to position in the narrative.

---

## When to Use

- Step-by-step product or feature explanations
- Scrollytelling — narrative that unfolds as you scroll
- Long-form case studies where a progress indicator adds value
- Sidebars with table of contents or section navigation
- Any layout where context needs to persist across a long content block

---

## Foundation: CSS Sticky

```css
.sticky-element {
  position: sticky;
  top: 0; /* or top: var(--nav-height) if there's a fixed nav */
}
```

In Tailwind:

```tsx
<div className="sticky top-0 h-screen">
  {/* This stays in view while siblings scroll */}
</div>
```

The sticky element must have a scrollable parent — it sticks within its nearest scrollable ancestor.

---

## Pattern 1: Sticky Visual + Scrolling Steps

The classic product showcase — visual on one side stays fixed, steps reveal on the other:

```tsx
<section className="grid grid-cols-1 gap-0 lg:grid-cols-2">
  {/* Sticky visualization */}
  <div className="lg:sticky lg:top-0 lg:h-screen flex items-center justify-center bg-muted overflow-hidden">
    <div className="relative w-full max-w-sm aspect-square">
      {/* Visual content — changes based on active step (see intersection approach below) */}
      {steps.map((step, i) => (
        <div
          key={i}
          className={cn(
            "absolute inset-0 flex items-center justify-center transition-opacity duration-500",
            activeStep === i ? "opacity-100" : "opacity-0"
          )}
        >
          {step.visual}
        </div>
      ))}
    </div>
  </div>

  {/* Scrolling steps */}
  <div>
    {steps.map((step, i) => (
      <div
        key={i}
        ref={el => stepRefs.current[i] = el}
        className="flex min-h-[80vh] items-center px-8 py-16 lg:px-12"
      >
        <div className="max-w-md">
          <span className="text-xs uppercase tracking-widest text-muted-foreground font-medium">
            {String(i + 1).padStart(2, "0")}
          </span>
          <h3 className="mt-3 text-3xl font-bold">{step.title}</h3>
          <p className="mt-4 text-muted-foreground leading-relaxed">{step.description}</p>
        </div>
      </div>
    ))}
  </div>
</section>
```

### Intersection-based active step tracking

```tsx
const [activeStep, setActiveStep] = useState(0)
const stepRefs = useRef<(HTMLDivElement | null)[]>([])

useEffect(() => {
  const observers = stepRefs.current.map((el, i) => {
    if (!el) return null
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setActiveStep(i) },
      { threshold: 0.5, rootMargin: "-20% 0px -20% 0px" }
    )
    observer.observe(el)
    return observer
  })
  return () => observers.forEach(o => o?.disconnect())
}, [])
```

---

## Pattern 2: Sticky Header with Active Navigation

Section markers update as the user scrolls:

```tsx
<header className="sticky top-0 z-30 border-b border-border bg-background/95 backdrop-blur-sm">
  <nav className="mx-auto flex max-w-screen-xl items-center justify-between px-6 h-14">
    <span className="font-semibold">{currentSection}</span>
    <div className="flex gap-6">
      {sections.map(section => (
        <a
          key={section.id}
          href={`#${section.id}`}
          className={cn(
            "text-sm transition-colors duration-200",
            activeSection === section.id
              ? "text-foreground"
              : "text-muted-foreground hover:text-foreground"
          )}
        >
          {section.label}
        </a>
      ))}
    </div>
  </nav>
</header>
```

---

## Pattern 3: Sticky Sidebar (Table of Contents)

```tsx
<div className="grid grid-cols-12 gap-8 py-16 px-6 max-w-screen-xl mx-auto">
  {/* Sticky ToC sidebar */}
  <aside className="hidden lg:block lg:col-span-3">
    <div className="sticky top-24 space-y-1">
      <p className="mb-3 text-xs uppercase tracking-widest text-muted-foreground">Contents</p>
      {headings.map(heading => (
        <a
          key={heading.id}
          href={`#${heading.id}`}
          className={cn(
            "block text-sm py-1 transition-colors duration-200",
            activeHeading === heading.id
              ? "text-foreground font-medium"
              : "text-muted-foreground hover:text-foreground",
            heading.level === 3 && "pl-4"
          )}
        >
          {heading.text}
        </a>
      ))}
    </div>
  </aside>

  {/* Main content */}
  <main className="col-span-12 lg:col-span-9">
    {content}
  </main>
</div>
```

---

## Pattern 4: Scroll Progress Indicator

A progress bar or number that reflects scroll position within a section:

```tsx
function ScrollProgress({ sectionRef }: { sectionRef: RefObject<HTMLElement> }) {
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const handleScroll = () => {
      const el = sectionRef.current
      if (!el) return
      const { top, height } = el.getBoundingClientRect()
      const scrolled = Math.max(0, -top)
      const total = height - window.innerHeight
      setProgress(Math.min(1, scrolled / total))
    }
    window.addEventListener("scroll", handleScroll, { passive: true })
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <div className="fixed right-8 top-1/2 -translate-y-1/2 flex flex-col items-center gap-1" aria-hidden="true">
      <div className="h-32 w-px bg-border">
        <div
          className="w-full bg-primary transition-none"
          style={{ height: `${progress * 100}%` }}
        />
      </div>
      <span className="text-xs text-muted-foreground tabular-nums">
        {Math.round(progress * 100)}%
      </span>
    </div>
  )
}
```

---

## Pattern 5: Sticky CTA

A CTA that persists at the bottom of the viewport until the user reaches a specific point:

```tsx
function StickyCTA({ showUntilRef }: { showUntilRef: RefObject<HTMLElement> }) {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => setVisible(!entry.isIntersecting),
      { threshold: 0.1 }
    )
    if (showUntilRef.current) observer.observe(showUntilRef.current)
    return () => observer.disconnect()
  }, [])

  return (
    <div className={cn(
      "fixed bottom-6 left-1/2 z-50 -translate-x-1/2 transition-all duration-300",
      visible ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0 pointer-events-none"
    )}>
      <a href="#signup" className="rounded-full bg-primary px-8 py-3 text-sm font-semibold text-primary-foreground shadow-lg">
        Get Started
      </a>
    </div>
  )
}
```

---

## Performance Constraints

- `position: sticky` is compositor-threaded — cheap. Prefer it over `position: fixed` + JS scroll tracking.
- Avoid scroll event listeners when `IntersectionObserver` can achieve the same result
- Sticky elements with `backdrop-blur` or complex paint are expensive — test on mobile
- `will-change: transform` on sticky elements can prevent compositing optimizations — use only if profiling shows jank

---

## Accessibility

- Sticky navigation must not cover content: ensure adequate `scroll-margin-top` on section anchors equal to sticky height
  ```css
  [id] { scroll-margin-top: 4rem; } /* matches sticky nav height */
  ```
- Sticky sidebars and ToC must be navigable by keyboard — all links in the correct tab order
- Progress indicators and decorative sticky elements must be `aria-hidden="true"`
- Ensure the sticky element doesn't trap focus — it's a persistent layer, not a modal

---

## Common Pitfalls

- **Sticky without scrollable parent:** element doesn't stick because its parent doesn't overflow. The sticky element needs a parent taller than itself.
- **Covering content:** sticky nav with insufficient `scroll-margin-top` on anchor targets causes section headings to hide behind the nav.
- **z-index conflicts:** sticky elements need explicit `z-*` to stay above content that scrolls beneath them.
- **Height not set:** `sticky top-0` on a sidebar without `h-screen` — the sidebar only occupies its content height and sticky has no room to operate.
- **Mobile layout broken:** sticky sidebars that don't account for mobile stack into the content flow. Hide them on mobile or convert to a different pattern.
