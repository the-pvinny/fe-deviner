# SKILL — Notification

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Notifications are interruptions by design. Every notification type is a tradeoff between urgency and disruption. The design challenge is not how to make notifications visible — it is how to make them **appropriate**. The wrong pattern for a given severity trains users to ignore everything, including critical alerts.

**Always map severity first, then choose the component.** Never the other way around.

---

## Severity Levels

| Severity | Attention level | User action required? | Example |
|---|---|---|---|
| **High** | Immediate, potentially blocking | Yes — cannot proceed without response | Payment failed, session expired, destructive confirmation |
| **Medium** | Prominent, non-blocking | Optional — user should acknowledge | Warning about data loss risk, completed async action |
| **Low** | Ambient, passive | No action needed | Badge count, background sync complete, auto-save indicator |

---

## When to Use Each Type

### Toast / Snackbar

Non-critical, auto-dismissing feedback. Slides in from a corner (bottom-right desktop, bottom-center mobile).

**Use for:**
- Confirming completed actions ("File saved", "Item added to cart")
- Non-critical system status ("Auto-saved", "Sync complete")
- Providing Undo after a reversible destructive action (include the undo action inside the toast)

**Do not use for:**
- High-priority errors — will auto-dismiss before the user can act
- Information the user must retain — it disappears
- Long or complex messages — toast is skimmable in one glance or it has failed

**Duration:** 3–5s for short confirmations; up to 8s if an action is included. Pause on hover/focus.

### Banner / System Alert

Persistent horizontal bar at the top of the content area. Does not auto-dismiss.

**Use for:**
- System-wide announcements (service degradation, scheduled maintenance)
- Account-level warnings that persist across the session ("Your trial ends in 3 days")
- Legal or compliance notices requiring acknowledgement

**Rules:**
- Maximum one banner visible at a time
- Place directly below the primary navigation
- Must be dismissible unless it represents a blocking system state
- Color-code by status: informational (blue), warning (amber), error (red), success (green) — always paired with an icon

### Inline Notification

Embedded within the content area, near the element it describes. Not a floating overlay.

**Use for:**
- Field-level validation errors (most common use)
- Section-level warnings (incomplete profile section, deprecated feature within a panel)
- Status of a specific item ("This item is out of stock")

**Advantage:** Stays visible, impossible to miss, collocated with the relevant element. Persists until the user resolves the condition.

### Modal Dialog (notification use)

Blocking overlay requiring explicit action before the user can continue. Severity: **high only**.

**Use when:**
- Critical errors where proceeding would cause data loss
- Irreversible confirmations ("Delete 47 files?" with explicit confirmation text typed out)
- Security events (session timeout warning with extend/logout choice)

**Do not use for** success messages, informational updates, or anything the user did not trigger.

### Badge

Small numeric counter or dot indicator on an icon or navigation item. Severity: **low only**.

**Use for:** Unread message count, pending tasks, new items since last visit.

**Rules:**
- If the count routinely exceeds 99, the badge has lost meaning
- Dot badge (no number) for simpler "something new" signals
- Never for urgent information — badges don't interrupt and are easily missed

### Notification Panel / Inbox

Dedicated panel (drawer or page) listing historical notifications. For products with high notification volume.

**Works in conjunction with:** Toasts (real-time alerts) + the panel (persistent record). Requires: read/unread state distinction, bulk actions (mark all read), filter by type/severity, direct links to the relevant resource.

---

## Decision Matrix

```
Is the event caused by a user action in this session?
  YES → Toast (success/confirmation) or Inline (error/validation)
  NO  → Is it a blocking system event?
          YES → Modal or Banner (high severity)
          NO  → Is it system-wide or session-wide?
                  YES → Banner (persists until resolved)
                  NO  → Badge or Notification panel entry
```

---

## Toast — Component

```tsx
import { useState, useEffect, useRef } from "react"
import { X, CheckCircle, AlertCircle, AlertTriangle, Info } from "lucide-react"
import { cn } from "@/lib/utils"

type ToastVariant = "success" | "error" | "warning" | "info"

interface ToastProps {
  id: string
  message: string
  description?: string
  variant?: ToastVariant
  duration?: number
  action?: { label: string; onClick: () => void }
  onDismiss: (id: string) => void
}

const variantStyles: Record<ToastVariant, string> = {
  success: "border-success/30 bg-card",
  error:   "border-destructive/30 bg-card",
  warning: "border-warning/30 bg-card",
  info:    "border-border bg-card",
}

const variantIcons: Record<ToastVariant, React.ElementType> = {
  success: CheckCircle,
  error:   AlertCircle,
  warning: AlertTriangle,
  info:    Info,
}

const variantIconColors: Record<ToastVariant, string> = {
  success: "text-success",
  error:   "text-destructive",
  warning: "text-warning",
  info:    "text-muted-foreground",
}

export function Toast({
  id,
  message,
  description,
  variant = "info",
  duration = 4000,
  action,
  onDismiss,
}: ToastProps) {
  const [visible, setVisible] = useState(false)
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const Icon = variantIcons[variant]

  const startTimer = () => {
    timerRef.current = setTimeout(() => setVisible(false), duration)
  }

  const clearTimer = () => {
    if (timerRef.current) clearTimeout(timerRef.current)
  }

  useEffect(() => {
    // Trigger entrance on mount
    requestAnimationFrame(() => setVisible(true))
    startTimer()
    return clearTimer
  }, [])

  const handleDismiss = () => setVisible(false)

  return (
    <div
      role={variant === "error" ? "alert" : "status"}
      aria-live={variant === "error" ? "assertive" : "polite"}
      aria-atomic="true"
      onMouseEnter={clearTimer}
      onMouseLeave={startTimer}
      onFocus={clearTimer}
      onBlur={startTimer}
      onTransitionEnd={() => { if (!visible) onDismiss(id) }}
      className={cn(
        "pointer-events-auto w-full max-w-sm rounded-lg border p-4 shadow-lg",
        "motion-safe:transition-all motion-safe:duration-300",
        variantStyles[variant],
        visible
          ? "motion-safe:translate-y-0 opacity-100"
          : "motion-safe:translate-y-2 opacity-0"
      )}
    >
      <div className="flex gap-3">
        <Icon
          className={cn("mt-0.5 h-4 w-4 shrink-0", variantIconColors[variant])}
          aria-hidden="true"
        />
        <div className="flex-1 space-y-1">
          <p className="text-sm font-medium text-foreground">{message}</p>
          {description && (
            <p className="text-sm text-muted-foreground">{description}</p>
          )}
          {action && (
            <button
              onClick={action.onClick}
              className="text-sm font-medium text-primary underline-offset-2 hover:underline focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:outline-none"
            >
              {action.label}
            </button>
          )}
        </div>
        <button
          onClick={handleDismiss}
          aria-label="Dismiss notification"
          className="shrink-0 rounded-sm text-muted-foreground opacity-70 hover:opacity-100 focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:outline-none"
        >
          <X className="h-4 w-4" aria-hidden="true" />
        </button>
      </div>
    </div>
  )
}
```

### Toast Provider and Hook

```tsx
import { createContext, useContext, useState, useCallback } from "react"
import { createPortal } from "react-dom"

interface ToastItem {
  id: string
  message: string
  description?: string
  variant?: "success" | "error" | "warning" | "info"
  duration?: number
  action?: { label: string; onClick: () => void }
}

interface ToastContextValue {
  toast: (item: Omit<ToastItem, "id">) => void
}

const ToastContext = createContext<ToastContextValue | null>(null)

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([])

  const toast = useCallback((item: Omit<ToastItem, "id">) => {
    const id = crypto.randomUUID()
    setToasts(prev => [...prev, { id, ...item }])
  }, [])

  const dismiss = useCallback((id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      {createPortal(
        <div
          aria-label="Notifications"
          className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 sm:bottom-6 sm:right-6"
        >
          {toasts.map(t => (
            <Toast key={t.id} {...t} onDismiss={dismiss} />
          ))}
        </div>,
        document.body
      )}
    </ToastContext.Provider>
  )
}

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error("useToast must be used within ToastProvider")
  return ctx
}

// Usage
// const { toast } = useToast()
// toast({ message: "File saved", variant: "success" })
// toast({ message: "Cannot delete", description: "Item is in use", variant: "error" })
// toast({ message: "Item deleted", action: { label: "Undo", onClick: handleUndo } })
```

---

## Banner — Component

```tsx
import { X, AlertTriangle, AlertCircle, CheckCircle, Info } from "lucide-react"
import { cn } from "@/lib/utils"

type BannerVariant = "info" | "success" | "warning" | "error"

interface BannerProps {
  message: string
  description?: string
  variant?: BannerVariant
  action?: { label: string; onClick: () => void }
  onDismiss?: () => void
  className?: string
}

const bannerVariants: Record<BannerVariant, { container: string; icon: React.ElementType; iconClass: string }> = {
  info:    { container: "bg-primary/5 border-primary/20",    icon: Info,          iconClass: "text-primary" },
  success: { container: "bg-success/5 border-success/20",    icon: CheckCircle,   iconClass: "text-success" },
  warning: { container: "bg-warning/5 border-warning/20",    icon: AlertTriangle, iconClass: "text-warning" },
  error:   { container: "bg-destructive/5 border-destructive/20", icon: AlertCircle, iconClass: "text-destructive" },
}

export function Banner({
  message,
  description,
  variant = "info",
  action,
  onDismiss,
  className,
}: BannerProps) {
  const { container, icon: Icon, iconClass } = bannerVariants[variant]

  return (
    <div
      role="banner"
      aria-live="polite"
      className={cn(
        "w-full border-b px-4 py-3",
        container,
        className
      )}
    >
      <div className="mx-auto flex max-w-screen-xl items-start gap-3 sm:items-center">
        <Icon className={cn("mt-0.5 h-4 w-4 shrink-0 sm:mt-0", iconClass)} aria-hidden="true" />
        <div className="flex flex-1 flex-col gap-1 sm:flex-row sm:items-center sm:gap-4">
          <p className="text-sm font-medium text-foreground">{message}</p>
          {description && (
            <p className="text-sm text-muted-foreground">{description}</p>
          )}
          {action && (
            <button
              onClick={action.onClick}
              className="text-sm font-semibold text-foreground underline underline-offset-2 hover:no-underline focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:outline-none"
            >
              {action.label}
            </button>
          )}
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            aria-label="Dismiss"
            className="shrink-0 rounded-sm text-muted-foreground opacity-70 hover:opacity-100 focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:outline-none"
          >
            <X className="h-4 w-4" aria-hidden="true" />
          </button>
        )}
      </div>
    </div>
  )
}
```

---

## Inline Notification — Component

```tsx
import { AlertCircle, AlertTriangle, CheckCircle, Info } from "lucide-react"
import { cn } from "@/lib/utils"

type InlineVariant = "info" | "success" | "warning" | "error"

interface InlineNotificationProps {
  message: string
  description?: string
  variant?: InlineVariant
  className?: string
}

const inlineVariants: Record<InlineVariant, { container: string; icon: React.ElementType; iconClass: string }> = {
  info:    { container: "bg-primary/5 text-primary border-primary/20",        icon: Info,          iconClass: "text-primary" },
  success: { container: "bg-success/5 text-success border-success/20",        icon: CheckCircle,   iconClass: "text-success" },
  warning: { container: "bg-warning/5 text-warning-foreground border-warning/20", icon: AlertTriangle, iconClass: "text-warning" },
  error:   { container: "bg-destructive/5 text-destructive border-destructive/20", icon: AlertCircle, iconClass: "text-destructive" },
}

export function InlineNotification({
  message,
  description,
  variant = "info",
  className,
}: InlineNotificationProps) {
  const { container, icon: Icon, iconClass } = inlineVariants[variant]

  return (
    <div
      role="alert"
      className={cn(
        "flex gap-3 rounded-lg border p-3",
        container,
        className
      )}
    >
      <Icon className={cn("mt-0.5 h-4 w-4 shrink-0", iconClass)} aria-hidden="true" />
      <div className="space-y-0.5">
        <p className="text-sm font-medium leading-snug">{message}</p>
        {description && (
          <p className="text-sm opacity-80">{description}</p>
        )}
      </div>
    </div>
  )
}
```

---

## Badge — Component

```tsx
import { cn } from "@/lib/utils"

interface BadgeCountProps {
  count: number
  max?: number
  className?: string
  "aria-label"?: string
}

export function BadgeCount({
  count,
  max = 99,
  className,
  "aria-label": ariaLabel,
}: BadgeCountProps) {
  if (count <= 0) return null

  const display = count > max ? `${max}+` : String(count)

  return (
    <span
      aria-label={ariaLabel ?? `${count} notification${count !== 1 ? "s" : ""}`}
      className={cn(
        "inline-flex h-5 min-w-5 items-center justify-center rounded-full",
        "bg-destructive px-1 text-xs font-medium text-white",
        className
      )}
    >
      {display}
    </span>
  )
}

// Dot badge — ambient "something new" signal
export function BadgeDot({ className }: { className?: string }) {
  return (
    <span
      aria-label="New activity"
      className={cn(
        "inline-block h-2 w-2 rounded-full bg-destructive",
        className
      )}
    />
  )
}

// Usage: positioned on a nav icon
// <div className="relative">
//   <Bell className="h-5 w-5" aria-hidden="true" />
//   <BadgeCount count={unreadCount} className="absolute -right-1.5 -top-1.5" />
// </div>
```

---

## Notification Anatomy

Every notification (regardless of type) should contain:

1. **Status icon** — visual encoding of severity; never color-only
2. **Title** — short, declarative; answers "what happened?"
3. **Body** — 1–2 lines maximum; explains "why it matters" or "what to do next"
4. **Action** (if needed) — 1 primary action + optional dismiss; never more than 2 buttons
5. **Timestamp** — for panel notifications; relative ("2 min ago") vs. absolute based on recency threshold

---

## Notification Strategy

**Default to fewer.** Start with a slow default — let users opt into more notifications, never start at maximum. A study by Facebook showed reducing notification frequency improved long-term engagement because users stopped muting everything.

**Avoid notification barrages on sign-up.** The first minute after account creation is when users are most sensitive to being spammed.

**Provide modes, not toggles.** Offer predefined profiles rather than per-notification controls:
- "Calm" — critical alerts only
- "Regular" — important updates + task completions
- "All" — full activity feed

**Don't notify what the user can see.** Don't send activity notifications when the user is actively engaged with the product — they can observe the event directly.

---

## Accessibility

| Requirement | Implementation |
|---|---|
| Screen reader announcement | `role="alert"` for errors/urgent; `role="status"` for informational |
| Keyboard access | Toast must be focusable before dismissal; all actions keyboard-operable |
| Auto-dismissal | Must pause on hover/focus; WCAG 2.2.1 requires timing to be adjustable |
| Motion | Entrance/exit animations inside `motion-safe:` wrapper |
| Color | Status must not be conveyed by color alone — use icon + label alongside color |
| Contrast | Toast text must meet 4.5:1 WCAG AA; icons 3:1 |

```tsx
// Correct ARIA role selection
<div role="alert" aria-live="assertive">  {/* errors — announces immediately */}
<div role="status" aria-live="polite">   {/* confirmations — waits for quiet moment */}
```

---

## Common Pitfalls

- **Alert fatigue** — too many notifications trains users to ignore everything, including critical ones. Start with fewer.
- **Auto-dismissing errors** — using a toast for a payment failure or validation error that disappears before the user reads it. Errors must use inline notifications or modals.
- **Stacking banners** — more than one system banner at a time makes both look equally unimportant.
- **Color-only status** — red toast for error, green for success, no icon or text difference — fails color-blind users. Always pair color with an icon.
- **Generic copy** — "Something went wrong" is not a notification; it is an apology. Every notification must answer "what happened" and "what to do next."
- **Undismissable toasts** — if a toast overlaps interactive UI the user needs to reach and can't be dismissed or moved, the task has been blocked.
- **Toast for errors** — the exception to toast-for-action-feedback: errors must stay visible until the user resolves them. Inline or modal, not toast.
