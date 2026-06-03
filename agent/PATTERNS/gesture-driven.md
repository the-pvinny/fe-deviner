# PATTERN — Gesture-Driven Interaction

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Touch gestures are the native interaction language of mobile devices. Gesture-driven UI responds to swipe, drag, pinch, and pull the way the user already expects the device to behave. When implemented well, it feels like the interface has physical weight.

---

## When to Use

- Carousels, galleries, and slideshows
- Drawers, bottom sheets, and side panels on mobile
- Pull-to-refresh on scrollable content
- Swipe-to-dismiss for notifications, cards, list items
- Horizontal navigation between tabs or pages on touch devices

Always pair touch events with pointer/keyboard equivalents — gestures are a layer on top of, not a replacement for, standard interaction.

---

## Foundation: Pointer Events (Unified API)

Use Pointer Events over Touch Events — they unify mouse, touch, and stylus into one model.

```tsx
const useDrag = (onDrag: (delta: { x: number; y: number }) => void, onEnd?: () => void) => {
  const start = useRef<{ x: number; y: number } | null>(null)

  const handlePointerDown = (e: React.PointerEvent) => {
    e.currentTarget.setPointerCapture(e.pointerId) // keep tracking even if cursor leaves element
    start.current = { x: e.clientX, y: e.clientY }
  }

  const handlePointerMove = (e: React.PointerEvent) => {
    if (!start.current) return
    onDrag({
      x: e.clientX - start.current.x,
      y: e.clientY - start.current.y,
    })
  }

  const handlePointerUp = () => {
    start.current = null
    onEnd?.()
  }

  return {
    onPointerDown: handlePointerDown,
    onPointerMove: handlePointerMove,
    onPointerUp: handlePointerUp,
    onPointerCancel: handlePointerUp,
  }
}
```

`setPointerCapture` is critical — without it, fast swipes that leave the element boundary stop tracking.

---

## Pattern 1: Swipeable Carousel

```tsx
function Carousel({ items }: { items: React.ReactNode[] }) {
  const [index, setIndex] = useState(0)
  const [dragX, setDragX] = useState(0)
  const [dragging, setDragging] = useState(false)
  const THRESHOLD = 80 // px to trigger slide change

  const handlers = useDrag(
    ({ x }) => { setDragging(true); setDragX(x) },
    () => {
      if (Math.abs(dragX) > THRESHOLD) {
        setIndex(i => dragX < 0
          ? Math.min(i + 1, items.length - 1)
          : Math.max(i - 1, 0)
        )
      }
      setDragX(0)
      setDragging(false)
    }
  )

  return (
    <div className="overflow-hidden touch-pan-y" {...handlers}>
      <div
        className={cn("flex", !dragging && "transition-transform duration-300 ease-out")}
        style={{ transform: `translateX(calc(-${index * 100}% + ${dragX}px))` }}
      >
        {items.map((item, i) => (
          <div key={i} className="w-full flex-shrink-0">{item}</div>
        ))}
      </div>
    </div>
  )
}
```

`touch-action: pan-y` tells the browser the element handles horizontal gestures itself, preventing scroll conflicts.

---

## Pattern 2: Swipe-to-Dismiss

```tsx
function DismissibleCard({ onDismiss, children }: { onDismiss: () => void; children: React.ReactNode }) {
  const [offsetX, setOffsetX] = useState(0)
  const THRESHOLD = 120

  const handlers = useDrag(
    ({ x }) => setOffsetX(x),
    () => {
      if (Math.abs(offsetX) > THRESHOLD) {
        onDismiss()
      } else {
        setOffsetX(0)
      }
    }
  )

  const opacity = Math.max(0, 1 - Math.abs(offsetX) / 200)
  const rotate = offsetX * 0.05 // slight rotation on drag

  return (
    <div
      className="transition-[opacity,transform] duration-300 ease-out cursor-grab active:cursor-grabbing"
      style={{
        transform: `translateX(${offsetX}px) rotate(${rotate}deg)`,
        opacity,
        transition: offsetX !== 0 ? "none" : undefined,
      }}
      {...handlers}
    >
      {children}
    </div>
  )
}
```

---

## Pattern 3: Bottom Sheet / Drawer

A panel that slides up from the bottom of the screen on mobile, draggable to dismiss.

```tsx
function BottomSheet({ open, onClose, children }: { open: boolean; onClose: () => void; children: React.ReactNode }) {
  const [dragY, setDragY] = useState(0)
  const DISMISS_THRESHOLD = 120

  const handlers = useDrag(
    ({ y }) => { if (y > 0) setDragY(y) }, // only allow dragging down
    () => {
      if (dragY > DISMISS_THRESHOLD) onClose()
      setDragY(0)
    }
  )

  return (
    <>
      {/* Backdrop */}
      <div
        className={cn(
          "fixed inset-0 z-40 bg-foreground/50 transition-opacity duration-300",
          open ? "opacity-100" : "opacity-0 pointer-events-none"
        )}
        onClick={onClose}
      />
      {/* Sheet */}
      <div
        className={cn(
          "fixed bottom-0 left-0 right-0 z-50 rounded-t-2xl bg-card shadow-2xl",
          "transition-transform duration-300 ease-out",
          !open && "translate-y-full"
        )}
        style={{ transform: open ? `translateY(${dragY}px)` : "translateY(100%)" }}
        {...handlers}
      >
        {/* Drag handle */}
        <div className="flex justify-center pt-3 pb-1">
          <div className="h-1 w-10 rounded-full bg-muted-foreground/30" />
        </div>
        {children}
      </div>
    </>
  )
}
```

---

## Pattern 4: Pull-to-Refresh

```tsx
function PullToRefresh({ onRefresh, children }: { onRefresh: () => Promise<void>; children: React.ReactNode }) {
  const [pullY, setPullY] = useState(0)
  const [refreshing, setRefreshing] = useState(false)
  const THRESHOLD = 80
  const MAX_PULL = 120

  const handleDrag = ({ y }: { y: number }) => {
    // Only activate when at top of scroll
    if (window.scrollY > 0) return
    setPullY(Math.min(y, MAX_PULL))
  }

  const handleEnd = async () => {
    if (pullY >= THRESHOLD) {
      setRefreshing(true)
      await onRefresh()
      setRefreshing(false)
    }
    setPullY(0)
  }

  const handlers = useDrag(handleDrag, handleEnd)

  return (
    <div {...handlers}>
      <div
        className="flex items-center justify-center overflow-hidden transition-all duration-300"
        style={{ height: pullY || refreshing ? 48 : 0 }}
      >
        <div className={cn("h-5 w-5 rounded-full border-2 border-primary border-t-transparent", refreshing && "animate-spin")} />
      </div>
      {children}
    </div>
  )
}
```

---

## touch-action Control

Critical for preventing browser scroll interference:

| Value | Use when |
|---|---|
| `touch-action: pan-y` | Element handles horizontal swipes; browser handles vertical scroll |
| `touch-action: pan-x` | Element handles vertical swipes; browser handles horizontal scroll |
| `touch-action: none` | Element handles all gestures (carousels, canvas) |
| `touch-action: manipulation` | Allow tap and pinch-zoom; disable double-tap-to-zoom delay |

Set on the drag container, not the whole page.

---

## Performance Constraints

- All gesture handlers must be `passive: true` when using `addEventListener` — or use pointer events (always passive for move/up)
- Apply transforms with `style` directly, not Tailwind classes, during active drag — class-based transitions fight gesture responsiveness
- Disable CSS transitions during active drag; re-enable on release (see carousel example above)
- Use `will-change: transform` on drag targets only during active drag — set and unset programmatically

---

## Accessibility

- Gestures are invisible to keyboard and screen reader users — always provide a non-gesture equivalent
  - Carousel: prev/next arrow buttons
  - Swipe-to-dismiss: a visible close/delete button
  - Bottom sheet: keyboard-accessible open/close trigger, Escape key to dismiss
  - Pull-to-refresh: a manual refresh button
- Focus management: when a drawer opens, move focus inside. When it closes, return focus to the trigger.
- Drag-and-drop: provide an alternative keyboard interface using `aria-grabbed` and arrow key movement

---

## Common Pitfalls

- **Scroll conflict:** drag handler on a scrollable container without `touch-action` causes the browser to fight your gesture. Always set `touch-action`.
- **Missing pointer capture:** fast swipes leave the element and the drag stops tracking. `setPointerCapture` is the fix.
- **Instant snap on cancel:** when a user releases mid-drag below the threshold, the element snapping back instantly feels wrong. Always transition the reset.
- **No keyboard alternative:** gesture-only UI is inaccessible. Non-negotiable.
- **Threshold too sensitive:** THRESHOLD < 50px triggers accidental dismissals on natural scroll movement. 80–120px is the right range.
