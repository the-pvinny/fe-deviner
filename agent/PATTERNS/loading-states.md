# PATTERN — Loading States

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Loading states are interfaces. A blank screen or spinner with no context is a failure. Good loading states communicate what is loading, approximately how long it will take, and that the system is working. The best loading states make the wait feel shorter than it is.

---

## When to Use

On every asynchronous operation: initial page loads, data fetching, form submissions, file uploads, route transitions. A loading state is never optional — the only question is which kind.

---

## Pattern 1: Skeleton Screen (Content Placeholder)

Renders the approximate shape of the incoming content before data arrives. Dramatically reduces perceived load time compared to spinners.

```tsx
function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-md bg-muted",
        "after:absolute after:inset-0",
        "after:bg-gradient-to-r after:from-transparent after:via-white/20 after:to-transparent",
        "after:animate-[shimmer_1.5s_infinite]",
        className
      )}
    />
  )
}

// CSS for shimmer
// @keyframes shimmer { from { translate: -100% 0 } to { translate: 100% 0 } }
```

### Card skeleton example

```tsx
function CardSkeleton() {
  return (
    <div className="rounded-lg border bg-card p-6 space-y-4">
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-4 w-1/2" />
      <Skeleton className="h-32 w-full" />
      <div className="flex gap-3">
        <Skeleton className="h-8 w-24" />
        <Skeleton className="h-8 w-16" />
      </div>
    </div>
  )
}
```

**Rule:** skeleton shapes should roughly approximate the actual content layout. A generic rectangle skeleton for a card with an avatar and two lines of text is better than nothing but worse than a skeleton with an avatar circle and two line-shapes.

---

## Pattern 2: Spinner

For indeterminate operations where duration is unknown and a skeleton isn't appropriate (actions, mutations, page transitions):

```tsx
function Spinner({ size = "md", className }: { size?: "sm" | "md" | "lg"; className?: string }) {
  const sizes = { sm: "h-4 w-4 border-2", md: "h-6 w-6 border-2", lg: "h-8 w-8 border-[3px]" }

  return (
    <div
      role="status"
      aria-label="Loading"
      className={cn(
        "animate-spin rounded-full border-muted border-t-primary",
        sizes[size],
        className
      )}
    />
  )
}
```

Never use a spinner as a full-page loading state for content — use skeleton instead. Reserve spinners for actions (button states, inline fetches).

---

## Pattern 3: Progress Bar

For operations with measurable progress (file upload, multi-step form, download):

```tsx
function ProgressBar({ value, max = 100, className }: { value: number; max?: number; className?: string }) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100))

  return (
    <div
      role="progressbar"
      aria-valuenow={value}
      aria-valuemin={0}
      aria-valuemax={max}
      className={cn("h-1.5 w-full overflow-hidden rounded-full bg-muted", className)}
    >
      <div
        className="h-full rounded-full bg-primary transition-all duration-300 ease-out"
        style={{ width: `${pct}%` }}
      />
    </div>
  )
}
```

For indeterminate progress (processing without known end point):

```tsx
function IndeterminateBar({ className }: { className?: string }) {
  return (
    <div className={cn("h-1 w-full overflow-hidden bg-muted", className)} role="status" aria-label="Loading">
      <div className="h-full w-1/3 rounded-full bg-primary animate-[indeterminate_1.5s_ease-in-out_infinite]" />
    </div>
  )
}
// @keyframes indeterminate { 0% { translate: -100% 0 } 100% { translate: 400% 0 } }
```

---

## Pattern 4: Optimistic UI

Update the UI immediately, before the server confirms — then reconcile:

```tsx
function LikeButton({ postId, initialLiked }: { postId: string; initialLiked: boolean }) {
  const [liked, setLiked] = useState(initialLiked)
  const [count, setCount] = useState(0)

  const handleLike = async () => {
    // Optimistic update — instant feedback
    setLiked(prev => !prev)
    setCount(prev => liked ? prev - 1 : prev + 1)

    try {
      await toggleLike(postId)
    } catch {
      // Rollback on failure
      setLiked(prev => !prev)
      setCount(prev => liked ? prev + 1 : prev - 1)
    }
  }

  return (
    <button onClick={handleLike}>
      <Heart className={cn("transition-colors duration-200", liked && "fill-red-500 text-red-500")} />
      <span>{count}</span>
    </button>
  )
}
```

Use for: likes, bookmarks, follows, read status, any low-stakes toggle. Do not use for: payments, destructive actions, or anything where rollback would be jarring.

---

## Pattern 5: Button Loading State

```tsx
function SubmitButton({ loading, children, ...props }: { loading: boolean } & React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      disabled={loading}
      aria-busy={loading}
      aria-disabled={loading}
      className={cn(
        "inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground",
        "transition-opacity duration-200",
        loading && "opacity-70 cursor-not-allowed"
      )}
      {...props}
    >
      {loading && <Spinner size="sm" className="border-primary-foreground/30 border-t-primary-foreground" />}
      {children}
    </button>
  )
}
```

**Key:** keep the button text visible during loading rather than replacing it entirely — this preserves context for the user.

---

## Pattern 6: Content Fade-In (on Data Arrival)

When data arrives, fade content in rather than popping it in:

```tsx
function DataCard({ data, loading }: { data: Item | null; loading: boolean }) {
  return (
    <div className="relative">
      {loading && <CardSkeleton />}
      <div className={cn(
        "transition-opacity duration-300",
        loading ? "opacity-0 absolute inset-0 pointer-events-none" : "opacity-100"
      )}>
        {data && <ActualCard item={data} />}
      </div>
    </div>
  )
}
```

---

## Pattern 7: Page Loading Bar (Navigation)

Thin bar at the top of the viewport that progresses during route changes:

```tsx
function NavigationProgress() {
  const [progress, setProgress] = useState(0)
  const [visible, setVisible] = useState(false)

  // Fake progress: jumps quickly at start, slows toward 90%, completes on navigation end
  useEffect(() => {
    // Hook into router events (Next.js App Router: use usePathname + useEffect)
  }, [])

  return (
    <div
      className={cn(
        "fixed left-0 top-0 z-[100] h-0.5 bg-primary transition-all",
        visible ? "opacity-100" : "opacity-0 duration-500"
      )}
      style={{ width: `${progress}%`, transition: visible ? "width 300ms ease-out" : undefined }}
    />
  )
}
```

---

## Timing Guidelines

| Operation | Loading pattern | Duration signal |
|---|---|---|
| < 100ms | None — instant | — |
| 100ms–1s | Spinner on button | None needed |
| 1s–3s | Skeleton screen | None needed |
| 3s–10s | Skeleton + progress bar | "Estimated time" text |
| > 10s | Progress bar + status text | Step count ("Step 2 of 5") |

**Jakob's Law of perception:** anything under 1 second feels instant. Anything over 10 seconds needs a progress indicator and the ability to cancel.

---

## Accessibility

- All loading indicators need `role="status"` or `role="progressbar"` with appropriate ARIA attributes
- Screen readers must be informed when loading completes — use `aria-live="polite"` on the region that receives the data
- Spinners need `aria-label="Loading"` — the spinning visual is meaningless to screen readers
- Never disable the entire page during loading — users should still be able to navigate away
- Progress bars: `aria-valuenow`, `aria-valuemin`, `aria-valuemax` are mandatory

---

## Common Pitfalls

- **Generic spinner for everything:** a full-page spinner for content that has a predictable shape is always worse than a skeleton
- **Shimmer on wrong axis:** shimmer should travel in the direction of content reading (left-to-right for LTR languages)
- **No error state:** loading that can fail must have a corresponding error state with a retry action
- **Optimistic UI with no rollback:** if the server fails, the UI is now wrong with no way to recover
- **Loading flash:** content that loads in < 100ms but still shows a skeleton flashes awkwardly. Use a minimum display time of 300ms for skeletons, or debounce the loading state.
