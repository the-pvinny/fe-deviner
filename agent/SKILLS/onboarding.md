# SKILL — Onboarding

Applies within CONFIG.md and METHOD.md constraints. Works alongside any STYLES/ or PATTERNS/ file.

---

## Core Principle

Onboarding is not a feature — it is a time window. The window opens at signup and closes the moment a user reaches their first meaningful success. Everything in that window is a dropout opportunity.

**Activation** is the moment a user gets a result that matches why they signed up. Not "completed the tour," not "set a profile photo" — the actual first value:
- "sent first message" / "created first project" / "got first AI response"

Every onboarding decision must be measured against **time to first value** (TTFV). Shorter TTFV → higher activation → higher Day 1 retention. The SaaS industry median loses 40–60% of new users in the first week; most drop before activation.

The best onboarding is **passive**: clear labels, smart defaults, and strong empty states activate users before any guided experience fires. Add tours, checklists, and tooltips only when passive help is exhausted.

---

## When to Use Each Pattern

| Pattern | Best for | Avoid when |
|---|---|---|
| Welcome screen | Consumer apps, simple first action, B2C | Multi-step setup is required first |
| Onboarding checklist | B2B SaaS, multi-step setup, admin configuration | Single-use tools, consumer apps with immediate value |
| Product tour | Complex interfaces where key actions are non-obvious | Users can discover value immediately without guidance |
| Empty state as onboarding | Any screen that can be empty | It is never enough on its own for complex products |

---

## The Two Structural Approaches

### Progressive Disclosure (Recommended Default)

Users enter the product immediately. Complexity is introduced over time, triggered by behavior signals — not calendar schedules.

- Reduces early cognitive overload; users learn by doing
- Features are revealed when the user's behavior indicates readiness
- Best for: feature-rich tools, B2C apps, any product where a useful first session is achievable without setup

**Example (Canva):** Start designing within 30 seconds. Advanced features (brand kit, team sharing, resize) appear contextually as users reach those workflows.

### Front-Loaded Setup

Collect required configuration before the user can access core functionality. Justified only when the product cannot deliver any value without initial data.

- Appropriate for: analytics dashboards (need a data source), personalization engines (need preferences), multi-user products that require admin config before end users activate
- **Rule:** collect only what is required for *first* value; defer everything else; every required step loses users

---

## Pattern 1 — Welcome Screen

A single screen, one clear next action, no carousel. The welcome screen is the handshake — acknowledge the user is here, point at the first step, and get out of the way.

### When to use
- Consumer / B2C apps where value is immediately accessible
- Simple products with a single obvious starting action
- Optional: include a personalization question *only* if it meaningfully changes the first-run experience

### When not to use
- When meaningful setup is required before any value is possible (use a setup wizard instead)
- Never stack multiple welcome screens into a carousel — users swipe through without reading

```tsx
interface WelcomeScreenProps {
  userName?: string
  productName: string
  headline: string
  description: string
  primaryAction: { label: string; onClick: () => void }
  secondaryAction?: { label: string; onClick: () => void }
  className?: string
}

function WelcomeScreen({
  userName,
  productName,
  headline,
  description,
  primaryAction,
  secondaryAction,
  className,
}: WelcomeScreenProps) {
  return (
    <main
      className={cn(
        "flex min-h-screen flex-col items-center justify-center px-4 py-16",
        className
      )}
    >
      <div className="mx-auto w-full max-w-md text-center">
        {/* Brand mark */}
        <div
          className="mx-auto mb-8 flex size-16 items-center justify-center rounded-2xl bg-primary"
          aria-hidden="true"
        >
          <span className="text-2xl font-bold text-primary-foreground">
            {productName.charAt(0)}
          </span>
        </div>

        {/* Greeting */}
        <h1 className="text-3xl font-bold tracking-tight text-foreground">
          {userName ? `Welcome, ${userName}` : headline}
        </h1>
        <p className="mt-3 text-base text-muted-foreground leading-relaxed">
          {description}
        </p>

        {/* Actions */}
        <div className="mt-8 flex flex-col gap-3">
          <button
            type="button"
            onClick={primaryAction.onClick}
            className={cn(
              "inline-flex h-11 w-full items-center justify-center rounded-lg",
              "bg-primary px-6 text-sm font-semibold text-primary-foreground",
              "transition-colors duration-150 hover:bg-primary/90",
              "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            )}
          >
            {primaryAction.label}
          </button>
          {secondaryAction && (
            <button
              type="button"
              onClick={secondaryAction.onClick}
              className={cn(
                "inline-flex h-11 w-full items-center justify-center rounded-lg",
                "border border-border bg-background px-6 text-sm font-medium text-foreground",
                "transition-colors duration-150 hover:bg-accent hover:text-accent-foreground",
                "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              )}
            >
              {secondaryAction.label}
            </button>
          )}
        </div>
      </div>
    </main>
  )
}
```

---

## Pattern 2 — Onboarding Checklist

A persistent list of setup tasks with completion states. The checklist works because of **completion momentum**: completing one task strongly predicts completing subsequent ones. Once users have one checkmark, they feel invested.

### When to use
- B2B SaaS with multi-step setup requirements (connect data source, invite team, set notifications)
- Products where activation requires multiple sequential configuration steps
- Admin onboarding that must complete before end-user onboarding begins

### Rules
- No more than 5–7 items total; each item must be completable in under 2 minutes
- Show progress ("3 of 5 complete") — a percentage or filled dots
- Always make dismissible — experienced users re-onboarding or revisiting must not be forced through it
- Resurface as a dashboard widget or sidebar card, never as a blocking modal

```tsx
interface ChecklistItem {
  id: string
  title: string
  description: string
  completed: boolean
  href?: string
  onClick?: () => void
}

interface OnboardingChecklistProps {
  title?: string
  items: ChecklistItem[]
  onDismiss?: () => void
  className?: string
}

function OnboardingChecklist({
  title = "Get started",
  items,
  onDismiss,
  className,
}: OnboardingChecklistProps) {
  const completedCount = items.filter((i) => i.completed).length
  const progress = Math.round((completedCount / items.length) * 100)

  return (
    <section
      aria-label={title}
      className={cn(
        "rounded-xl border border-border bg-card p-5 shadow-sm",
        className
      )}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-4 mb-4">
        <div>
          <h2 className="text-sm font-semibold text-foreground">{title}</h2>
          <p className="text-xs text-muted-foreground mt-0.5">
            {completedCount} of {items.length} complete
          </p>
        </div>
        {onDismiss && (
          <button
            type="button"
            onClick={onDismiss}
            aria-label="Dismiss checklist"
            className={cn(
              "shrink-0 rounded-md p-1 text-muted-foreground",
              "transition-colors duration-150 hover:bg-accent hover:text-accent-foreground",
              "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            )}
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        )}
      </div>

      {/* Progress bar */}
      <div
        role="progressbar"
        aria-valuenow={progress}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`Onboarding ${progress}% complete`}
        className="mb-4 h-1.5 w-full rounded-full bg-muted overflow-hidden"
      >
        <div
          className="h-full rounded-full bg-primary transition-all duration-500 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Items */}
      <ol className="space-y-1" aria-label="Setup tasks">
        {items.map((item) => {
          const Tag = item.href ? "a" : "button"
          return (
            <li key={item.id}>
              <Tag
                href={item.href}
                onClick={item.onClick}
                type={item.href ? undefined : "button"}
                aria-current={item.completed ? undefined : "step"}
                className={cn(
                  "group flex w-full items-start gap-3 rounded-lg p-2 text-left",
                  "transition-colors duration-150 hover:bg-accent",
                  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
                  item.completed && "opacity-60"
                )}
              >
                {/* Completion indicator */}
                <div
                  className={cn(
                    "mt-0.5 flex size-5 shrink-0 items-center justify-center rounded-full border-2 transition-colors duration-200",
                    item.completed
                      ? "border-primary bg-primary"
                      : "border-border bg-background group-hover:border-primary/50"
                  )}
                  aria-hidden="true"
                >
                  {item.completed && (
                    <Check className="size-3 text-primary-foreground" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p
                    className={cn(
                      "text-sm font-medium",
                      item.completed
                        ? "line-through text-muted-foreground"
                        : "text-foreground"
                    )}
                  >
                    {item.title}
                  </p>
                  {!item.completed && (
                    <p className="text-xs text-muted-foreground mt-0.5 leading-relaxed">
                      {item.description}
                    </p>
                  )}
                </div>
                {!item.completed && (
                  <ChevronRight
                    className="size-4 shrink-0 mt-0.5 text-muted-foreground group-hover:text-foreground transition-colors duration-150"
                    aria-hidden="true"
                  />
                )}
              </Tag>
            </li>
          )
        })}
      </ol>
    </section>
  )
}
```

---

## Pattern 3 — Product Tour / Tooltip Sequence

A sequential guided walkthrough of the interface, pointing at specific UI elements one step at a time.

### When to use
- Complex interfaces where the core workflow is non-obvious
- When passive help (labels, empty states) is insufficient for first-run discovery
- Features that cannot be surfaced via empty states (e.g., keyboard shortcuts, hidden panel controls)

### Rules
- Maximum 3–5 steps — each step must point at a specific, visible UI element
- Trigger contextually when the user first arrives at the relevant screen — never at login
- Always allow skip; never block the UI behind a tour
- Never cover the target element itself — position the tooltip to the side or below
- After dismissal, do not resurface the same tour

```tsx
interface TourStep {
  id: string
  title: string
  description: string
  targetId: string
  placement?: "top" | "bottom" | "left" | "right"
}

interface ProductTourProps {
  steps: TourStep[]
  onComplete: () => void
  onSkip: () => void
}

function ProductTour({ steps, onComplete, onSkip }: ProductTourProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [position, setPosition] = useState({ top: 0, left: 0 })
  const tooltipRef = useRef<HTMLDivElement>(null)

  const current = steps[currentIndex]
  const isLast = currentIndex === steps.length - 1

  useEffect(() => {
    const target = document.getElementById(current.targetId)
    if (!target) return

    const rect = target.getBoundingClientRect()
    const placement = current.placement ?? "bottom"

    const positions: Record<string, { top: number; left: number }> = {
      bottom: { top: rect.bottom + 12 + window.scrollY, left: rect.left + rect.width / 2 },
      top:    { top: rect.top - 12 + window.scrollY,    left: rect.left + rect.width / 2 },
      right:  { top: rect.top + rect.height / 2 + window.scrollY, left: rect.right + 12 },
      left:   { top: rect.top + rect.height / 2 + window.scrollY, left: rect.left - 12 },
    }

    setPosition(positions[placement])

    // Highlight target
    target.setAttribute("data-tour-active", "true")
    target.scrollIntoView({ behavior: "smooth", block: "nearest" })

    // Move focus into tooltip after positioning
    tooltipRef.current?.focus()

    return () => target.removeAttribute("data-tour-active")
  }, [current])

  const handleNext = () => {
    if (isLast) onComplete()
    else setCurrentIndex((i) => i + 1)
  }

  return (
    <>
      {/* Backdrop */}
      <div
        aria-hidden="true"
        className="fixed inset-0 z-40 bg-foreground/30 motion-safe:animate-in motion-safe:fade-in motion-safe:duration-200"
        onClick={onSkip}
      />

      {/* Tooltip */}
      <div
        ref={tooltipRef}
        role="dialog"
        aria-modal="false"
        aria-label={`Tour step ${currentIndex + 1} of ${steps.length}: ${current.title}`}
        tabIndex={-1}
        className={cn(
          "fixed z-50 w-72 rounded-xl bg-background border border-border shadow-xl p-4",
          "-translate-x-1/2",
          "motion-safe:animate-in motion-safe:fade-in motion-safe:zoom-in-95 motion-safe:duration-150",
          "focus-visible:outline-none"
        )}
        style={{ top: position.top, left: position.left }}
      >
        {/* Step counter */}
        <div className="flex items-center gap-1.5 mb-2">
          {steps.map((_, i) => (
            <div
              key={i}
              aria-hidden="true"
              className={cn(
                "h-1 rounded-full transition-all duration-300",
                i === currentIndex
                  ? "w-6 bg-primary"
                  : i < currentIndex
                    ? "w-2 bg-primary/50"
                    : "w-2 bg-muted"
              )}
            />
          ))}
        </div>

        <h3 className="text-sm font-semibold text-foreground">{current.title}</h3>
        <p className="mt-1 text-xs text-muted-foreground leading-relaxed">
          {current.description}
        </p>

        <div className="mt-3 flex items-center justify-between gap-2">
          <button
            type="button"
            onClick={onSkip}
            className={cn(
              "text-xs text-muted-foreground transition-colors duration-150 hover:text-foreground",
              "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:rounded-sm"
            )}
          >
            Skip tour
          </button>
          <button
            type="button"
            onClick={handleNext}
            className={cn(
              "inline-flex h-7 items-center rounded-md bg-primary px-3 text-xs font-semibold text-primary-foreground",
              "transition-colors duration-150 hover:bg-primary/90",
              "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            )}
          >
            {isLast ? "Done" : "Next"}
          </button>
        </div>
      </div>
    </>
  )
}
```

### CSS — highlight the active tour target

```css
[data-tour-active="true"] {
  outline: 2px solid var(--color-primary);
  outline-offset: 4px;
  border-radius: var(--radius);
  position: relative;
  z-index: 41;
}
```

---

## Pattern 4 — Empty State as First-Run Onboarding

Every screen that can be empty is an onboarding opportunity. The empty state is **passive help** — it works without interrupting the user, fires automatically the first time they reach a screen, and persists until data exists.

### When to use
- Always — every screen with potential empty state should have a first-run version
- Especially powerful for list views, dashboards, and project containers
- Combine with other patterns: a checklist drives users to screens; empty states complete the journey

### First-run vs repeat empty state

First-run empty states explain and invite creation. Repeat empty states (e.g., after filtering to zero results) explain why the list is empty and how to fix it — they should not look identical.

```tsx
interface EmptyStateProps {
  icon?: React.ReactNode
  title: string
  description: string
  action?: {
    label: string
    onClick: () => void
  }
  secondaryAction?: {
    label: string
    onClick: () => void
  }
  isFirstRun?: boolean
  className?: string
}

function EmptyState({
  icon,
  title,
  description,
  action,
  secondaryAction,
  isFirstRun = false,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center text-center px-6 py-16",
        className
      )}
    >
      {/* Icon or illustration */}
      {icon && (
        <div
          className={cn(
            "mb-4 flex size-14 items-center justify-center rounded-full",
            isFirstRun ? "bg-primary/10" : "bg-muted"
          )}
          aria-hidden="true"
        >
          <div className={cn("size-7", isFirstRun ? "text-primary" : "text-muted-foreground")}>
            {icon}
          </div>
        </div>
      )}

      <h2 className="text-base font-semibold text-foreground">{title}</h2>
      <p className="mt-2 max-w-xs text-sm text-muted-foreground leading-relaxed">
        {description}
      </p>

      {(action || secondaryAction) && (
        <div className="mt-6 flex flex-col sm:flex-row items-center gap-3">
          {action && (
            <button
              type="button"
              onClick={action.onClick}
              className={cn(
                "inline-flex h-9 items-center rounded-lg bg-primary px-4 text-sm font-semibold text-primary-foreground",
                "transition-colors duration-150 hover:bg-primary/90",
                "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              )}
            >
              {action.label}
            </button>
          )}
          {secondaryAction && (
            <button
              type="button"
              onClick={secondaryAction.onClick}
              className={cn(
                "inline-flex h-9 items-center rounded-lg border border-border bg-background px-4 text-sm font-medium text-foreground",
                "transition-colors duration-150 hover:bg-accent hover:text-accent-foreground",
                "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              )}
            >
              {secondaryAction.label}
            </button>
          )}
        </div>
      )}
    </div>
  )
}
```

### Usage example

```tsx
// First-run empty state for a projects list
<EmptyState
  icon={<FolderPlus className="size-full" />}
  title="Create your first project"
  description="Projects keep your work organized. Create one to start collaborating with your team."
  action={{ label: "New project", onClick: handleCreateProject }}
  secondaryAction={{ label: "Import existing", onClick: handleImport }}
  isFirstRun={true}
/>

// Post-filter empty state (not first-run)
<EmptyState
  icon={<Search className="size-full" />}
  title="No results found"
  description='No projects match "design system". Try a different search term or clear your filters.'
  action={{ label: "Clear filters", onClick: clearFilters }}
  isFirstRun={false}
/>
```

---

## The Help Ladder

Good onboarding is a graduated response system — not a single-trigger event. Apply interventions at the right level before escalating.

| Level | Type | When it triggers | Examples |
|---|---|---|---|
| A | **Passive help** | Always present | Clear labels, smart defaults, inline helper text, strong empty states |
| B | **Gentle nudges** | First meaningful interaction | Tooltip on first focus, single-line contextual hint, welcome screen |
| C | **Active guidance** | First visit to a complex screen | Product tour, onboarding checklist |
| D | **Rescue help** | After observable friction | Error-triggered suggestion, chat prompt, help article |

Most products skip Level A improvements and jump to Level C. This is wrong: improving passive help (clearer labels, better defaults) lifts activation more than adding tours. Only escalate when lower levels are genuinely insufficient.

Trigger Level D only after observable friction signals: 3+ errors on the same field, stalled time on task, repeated back-navigation.

---

## Accessibility

- Tour tooltips use `role="dialog"` and `aria-label` including the step counter — screen readers announce position and total steps
- Tour tooltips must not use `aria-modal="true"` — the backdrop should not trap focus away from the highlighted UI element; users must be able to interact with the target
- Focus moves into each tooltip on step advance (`tooltipRef.current?.focus()` with `tabIndex={-1}`)
- Escape key dismisses any active tour or overlay — implement via `useEffect` + `document.addEventListener("keydown")`
- Checklist progress bars use `role="progressbar"` with `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, and an accessible label
- Empty states use semantic `<h2>` (not `<p>`) for the title — they are headings within the page structure
- Never convey onboarding state via color alone — use icons and text alongside color indicators
- Tours and highlights must respect `prefers-reduced-motion`: disable entrance animations on tooltips, keep positioning

```tsx
// Escape to skip tour
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Escape") onSkip()
  }
  document.addEventListener("keydown", handleKeyDown)
  return () => document.removeEventListener("keydown", handleKeyDown)
}, [onSkip])
```

---

## Measuring Onboarding Success

Measure activation, not completion:

| Metric | What it tells you |
|---|---|
| **Activation rate** | % of signups who reach the defined first-value event |
| **Day 1 retention** | % who return the next day — strongest signal of onboarding quality |
| **Time to activation** | Median minutes from signup to first value |
| **Checklist completion rate** | % who finish all items (proxy for setup friction) |
| **Tour skip rate** | High skip rate = tour triggers too early, or teaches the wrong thing |

Do not measure "tour completion rate" as a success metric — a user who skips a tour and immediately creates their first project is more activated than one who completes all five tour steps and never creates anything.

---

## Common Pitfalls

- **Mandatory blocking tour:** if a tour must be completed before the user can interact with the product, it will be abandoned — make every tour skippable and every step optional
- **Too many checklist items:** a checklist with 10 items signals that your product is complex, not that onboarding is thorough; cut ruthlessly to 5 or fewer
- **Personalization survey that adds no value:** asking role and use case upfront is only justified if it materially changes the first-run experience; otherwise it is friction before value
- **Tour that teaches features, not workflows:** showing the user where "Settings" is located is less valuable than showing them how to complete their first task — tours should map to jobs-to-be-done
- **Onboarding that ends:** when new features ship, existing users encounter them without context. Treat onboarding as continuous; surface new features via contextual hints, not a separate onboarding flow
- **Empty state that is actually blank:** a screen with no items and no empty state is a dead end. Every emptied state must have a title, description, and at least one action
- **Conflating admin and end-user onboarding:** in B2B products these are separate journeys; mixing them creates a setup experience that is too long for end users and too shallow for admins
