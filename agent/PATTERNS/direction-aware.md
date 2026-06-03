# PATTERN — Direction-Aware Hover

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Direction-aware hover is distinct from proximity-based hover (see `hover-micro.md`). Here, the hover response of each element depends on its **spatial relationship to the currently hovered sibling** — items before the hovered element respond differently from items after it. The canonical form is the fan-out avatar stack: hover any member, and the items to its left push left while items to its right push right, creating a physical "spreading apart" effect.

This requires either:
1. **CSS `sibling-index()` / `sibling-count()`** — pure CSS, no JS, Chrome 2025+ only
2. **JavaScript fallback** — reads sibling position via `getBoundingClientRect`, works in all browsers

Always implement both: start with the CSS approach and detect support, falling back to JS where `sibling-index()` is unavailable.

---

## When to Use

- Avatar stacks (team members, collaborators, participant lists)
- Horizontal icon rows where spatial context between items is meaningful
- Card decks or image galleries where "spreading" the hovered item from its neighbors communicates selection

## When Not to Use

- Vertical lists (the axis of separation must match the axis of the layout)
- More than ~8–10 items in a stack (visual noise; user cannot parse the spatial relationship)
- Any context where exact item position matters (drag handles, precision UIs)
- Anywhere `hover-micro.md` patterns (lift, color shift) achieve the same goal with less complexity

---

## Approach 1: CSS `sibling-index()` (2025+, Progressive Enhancement)

The `sibling-index()` function returns the 0-based position of an element within its parent's children. `sibling-count()` returns the total count. Together they let each item calculate its own offset relative to the hovered sibling without any JavaScript.

**Browser support (2026):** Chrome 117+, Edge 117+. Firefox and Safari: not yet supported.

```css
.avatar-stack {
  display: flex;
  flex-direction: row;
}

/*
  When any child is hovered, each sibling knows its own index.
  Items before the hovered one translate left; items after translate right.
  The hovered item stays put (translateX(0)).

  Formula: each item pushes proportionally to its distance from the hovered item.
  CSS cannot directly know WHICH sibling is hovered, so we use :has() to detect
  that a sibling is being hovered and respond accordingly.
*/

.avatar-stack:has(.avatar:hover) .avatar {
  /* Default: all items push apart when any is hovered */
  translate: calc((sibling-index() - (sibling-count() / 2)) * 12px) 0;
  transition: translate 300ms ease-out, z-index 0s;
}

.avatar-stack .avatar:hover {
  /* The hovered item stays in place and comes to the front */
  translate: 0;
  z-index: 10;
}

/* Assign per-item hue using sibling-index() */
.avatar {
  --hue: calc(sibling-index() * 40);
  background-color: oklch(0.7 0.15 var(--hue));
}
```

**Limitation:** CSS cannot distinguish items *before* vs *after* the hovered sibling — it can only compute a distance from the center. For true directional response (left items push left, right items push right), the JS approach gives more precise control.

---

## Approach 2: JavaScript — Full Directional Control (All Browsers)

This approach reads the hovered item's index, then pushes each sibling by an offset proportional to its signed distance from the hovered item. Items to the left receive a negative offset; items to the right receive a positive offset.

```tsx
interface AvatarItem {
  id: string
  src: string
  name: string
}

interface AvatarStackProps {
  items: AvatarItem[]
  size?: number          // avatar diameter in px — must map to a token multiple
  overlap?: number       // how much avatars overlap when at rest (px)
  spread?: number        // max spread distance when a neighbor is hovered (px)
  className?: string
}

function AvatarStack({
  items,
  size = 40,
  overlap = 12,
  spread = 16,
  className,
}: AvatarStackProps) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null)
  const prefersReducedMotion =
    typeof window !== "undefined"
      ? window.matchMedia("(prefers-reduced-motion: reduce)").matches
      : false

  const getTranslateX = (index: number): number => {
    if (hoveredIndex === null || prefersReducedMotion) return 0
    const distance = index - hoveredIndex
    if (distance === 0) return 0
    // Items spread away from the hovered item, capped at max spread
    const direction = distance > 0 ? 1 : -1
    const magnitude = Math.min(Math.abs(distance) * spread * 0.5, spread)
    return direction * magnitude
  }

  return (
    <div
      role="group"
      aria-label={`${items.length} participants`}
      className={cn("flex items-center", className)}
    >
      {items.map((item, index) => (
        <div
          key={item.id}
          className="relative shrink-0"
          style={{
            marginLeft: index === 0 ? 0 : -overlap,
            zIndex: hoveredIndex === index ? items.length + 1 : index,
            transform: `translateX(${getTranslateX(index)}px)`,
            transition: prefersReducedMotion
              ? "none"
              : "transform 300ms ease-out, z-index 0s",
          }}
          onMouseEnter={() => setHoveredIndex(index)}
          onMouseLeave={() => setHoveredIndex(null)}
          onFocus={() => setHoveredIndex(index)}
          onBlur={() => setHoveredIndex(null)}
        >
          <img
            src={item.src}
            alt={item.name}
            width={size}
            height={size}
            className={cn(
              "rounded-full border-2 border-background object-cover block",
              "transition-shadow duration-200",
              hoveredIndex === index && "shadow-md ring-2 ring-ring ring-offset-1"
            )}
            style={{ width: size, height: size }}
          />
          {/* Tooltip on hover/focus */}
          {hoveredIndex === index && (
            <div
              role="tooltip"
              id={`avatar-tooltip-${item.id}`}
              className={cn(
                "absolute bottom-full left-1/2 -translate-x-1/2 mb-2 whitespace-nowrap",
                "rounded-md bg-foreground px-2 py-1 text-xs text-background shadow-md",
                "pointer-events-none",
                "motion-safe:animate-in motion-safe:fade-in motion-safe:duration-100"
              )}
            >
              {item.name}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
```

---

## Approach 3: Hybrid — CSS with JS Detection

Use `CSS.supports()` to detect `sibling-index()` support, then apply the CSS-only approach for modern browsers and fall back to the React component for others.

```tsx
const supportsSiblingIndex =
  typeof CSS !== "undefined" &&
  CSS.supports("translate", "calc(sibling-index() * 1px)")

function AvatarStackAdaptive(props: AvatarStackProps) {
  if (supportsSiblingIndex) {
    // Render plain <li>s; CSS handles the spread
    return <AvatarStackCSS {...props} />
  }
  return <AvatarStack {...props} />
}
```

```css
/* AvatarStackCSS — only loaded when sibling-index() is supported */
@supports (translate: calc(sibling-index() * 1px)) {
  .avatar-stack-css {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .avatar-stack-css:has(li:hover) li {
    translate: calc(
      (sibling-index() - (sibling-count() - 1) / 2) * 10px
    ) 0;
    transition: translate 300ms ease-out;
  }

  .avatar-stack-css li:hover {
    translate: 0;
    z-index: 10;
    position: relative;
  }
}
```

---

## Canonical Pattern — Fan-Out Card Row

Applying the same principle to larger elements — cards or feature tiles fan apart on sibling hover:

```tsx
interface CardItem {
  id: string
  title: string
  description: string
}

function DirectionalCardRow({ cards }: { cards: CardItem[] }) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null)
  const prefersReducedMotion =
    typeof window !== "undefined"
      ? window.matchMedia("(prefers-reduced-motion: reduce)").matches
      : false

  const getOffset = (index: number) => {
    if (hoveredIndex === null || prefersReducedMotion) return { x: 0, scale: 1 }
    const dist = index - hoveredIndex
    if (dist === 0) return { x: 0, scale: 1.02 }
    const push = Math.sign(dist) * Math.min(Math.abs(dist) * 24, 40)
    return { x: push, scale: 0.98 }
  }

  return (
    <div role="list" className="flex gap-4">
      {cards.map((card, index) => {
        const { x, scale } = getOffset(index)
        return (
          <article
            key={card.id}
            role="listitem"
            className={cn(
              "flex-1 rounded-xl border border-border bg-card p-5 cursor-default",
              "transition-shadow duration-200",
              hoveredIndex === index && "shadow-lg border-primary/30"
            )}
            style={{
              transform: prefersReducedMotion
                ? undefined
                : `translateX(${x}px) scale(${scale})`,
              transition: prefersReducedMotion
                ? "none"
                : "transform 300ms ease-out, box-shadow 200ms ease-out",
              zIndex: hoveredIndex === index ? 2 : 1,
            }}
            onMouseEnter={() => setHoveredIndex(index)}
            onMouseLeave={() => setHoveredIndex(null)}
            onFocus={() => setHoveredIndex(index)}
            onBlur={() => setHoveredIndex(null)}
            tabIndex={0}
          >
            <h3 className="text-sm font-semibold text-foreground">{card.title}</h3>
            <p className="mt-1 text-xs text-muted-foreground leading-relaxed">
              {card.description}
            </p>
          </article>
        )
      })}
    </div>
  )
}
```

---

## Motion Principles

From microinteraction theory, direction-aware effects sit in the **feedback** tier — they confirm spatial position and group membership. Key calibration:

- Spread distance: 12–20px per step for avatar stacks; 20–40px for cards. Above 40px reads as broken positioning.
- Transition duration: 250–350ms `ease-out` for enter; same duration `ease-out` for exit (CSS default is immediate return — always add a transition on the base state)
- Scale the hovered item up subtly (1.02–1.05×) to reinforce focus; scale neighbors down (0.97–0.99×) to reinforce the hierarchy

---

## Browser Support

| Feature | Chrome | Edge | Firefox | Safari |
|---|---|---|---|---|
| `sibling-index()` / `sibling-count()` | 117+ | 117+ | No | No |
| `:has()` (required for CSS approach) | 105+ | 105+ | 121+ | 15.4+ |
| JS `getBoundingClientRect` fallback | All | All | All | All |
| `CSS.supports()` detection | 28+ | 12+ | 22+ | 9+ |

Always treat `sibling-index()` as progressive enhancement. The JS fallback must be the baseline.

---

## Accessibility

- Avatar stacks: the container uses `role="group"` with an `aria-label` (e.g., "5 participants") — individual avatars use `alt` text with the person's name
- Hover-only interactions must also fire on `focus` and `blur` — keyboard users navigate with Tab and must see the spread effect
- Tooltips use `role="tooltip"` — associate each avatar's tooltip with `aria-describedby={tooltipId}` on the image
- The spread animation must respect `prefers-reduced-motion`: when reduced, skip the transform and render only color/ring changes on hover
- Never convey group membership information solely through the spatial spread — include visible names or accessible text

```tsx
// Image with tooltip association
<img
  src={item.src}
  alt={item.name}
  aria-describedby={`avatar-tooltip-${item.id}`}
  // ...
/>
```

---

## Common Pitfalls

- **No base-state transition:** without `transition: transform 300ms ease-out` on the default state, the return from hovered position is instant — jarring. CSS hover adds the transition to `:hover`; the base needs it too for exit animation.
- **Spread too large:** > 40px of spread feels like layout is breaking, not responding. Keep spread proportional to element size — avatars of 40px should spread 12–16px max.
- **Z-index not elevated on hover:** the hovered item can be clipped by its neighbors' overflow or shadows without explicit z-index elevation on hover.
- **JavaScript version without `focus` handlers:** keyboard users Tab through elements; if the spread fires only on `mouseenter` and not `focus`, keyboard users see no effect.
- **Using `sibling-index()` without feature detection:** CSS that uses `sibling-index()` in unsupported browsers causes the entire rule to be ignored silently — items layout as if no hover rule exists. Always wrap in `@supports` or detect via JS.
- **Forgetting `prefers-reduced-motion`:** translation-based effects are high-risk for vestibular disorders. The reduced-motion alternative (ring/shadow only, no translate) is mandatory.
