# SKILL — Modal & Dialog

Applies within CONFIG.md and METHOD.md constraints. Works alongside any STYLES/ or PATTERNS/ file.

---

## Core Principle

A modal interrupts. Use it only when the user must respond before continuing — a destructive confirmation, a critical form, a decision gate. Modals for non-critical content (tooltips, drawers, inline expansions) should use less intrusive patterns. When in doubt, ask: "Does the user _have_ to deal with this right now?" If no, don't use a modal.

---

## When to Use Modal vs Alternatives

| Situation | Use |
|---|---|
| Destructive action confirmation | Modal — blocks until decided |
| Short required form (2–5 fields) | Modal |
| Error that requires acknowledgment | Modal |
| Long form or multi-step flow | Page or full-screen panel |
| Additional info without action | Tooltip, popover, or drawer |
| Settings panel / profile edit | Drawer (side sheet) |
| Context details (detail view) | Drawer or inline expansion |

---

## Structure — Compound Component

```tsx
function Dialog({ open, onClose, children }) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose()
    }
    if (open) {
      document.addEventListener("keydown", handleKeyDown)
      document.body.style.overflow = "hidden"
    }
    return () => {
      document.removeEventListener("keydown", handleKeyDown)
      document.body.style.overflow = ""
    }
  }, [open, onClose])

  if (!open) return null

  return (
    <div role="presentation">
      {/* Backdrop */}
      <div
        aria-hidden="true"
        onClick={onClose}
        className="fixed inset-0 z-40 bg-foreground/50 backdrop-blur-sm motion-safe:animate-in motion-safe:fade-in motion-safe:duration-200"
      />
      {/* Panel */}
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
        aria-describedby="dialog-description"
        className={cn(
          "fixed left-1/2 top-1/2 z-50 -translate-x-1/2 -translate-y-1/2",
          "w-full max-w-lg rounded-xl bg-background shadow-2xl",
          "motion-safe:animate-in motion-safe:fade-in motion-safe:zoom-in-95 motion-safe:duration-200"
        )}
      >
        {children}
      </div>
    </div>
  )
}

function DialogHeader({ className, ...props }) {
  return <div className={cn("flex flex-col gap-1.5 p-6 pb-0", className)} {...props} />
}

function DialogTitle({ className, ...props }) {
  return <h2 id="dialog-title" className={cn("text-base font-semibold leading-tight", className)} {...props} />
}

function DialogDescription({ className, ...props }) {
  return <p id="dialog-description" className={cn("text-sm text-muted-foreground", className)} {...props} />
}

function DialogContent({ className, ...props }) {
  return <div className={cn("p-6", className)} {...props} />
}

function DialogFooter({ className, ...props }) {
  return (
    <div
      className={cn("flex flex-col-reverse sm:flex-row sm:justify-end gap-2 p-6 pt-0", className)}
      {...props}
    />
  )
}

function DialogClose({ onClose, className, ...props }) {
  return (
    <button
      type="button"
      onClick={onClose}
      aria-label="Close dialog"
      className={cn(
        "absolute top-4 right-4 rounded-md p-1 text-muted-foreground",
        "transition-colors duration-150 hover:bg-accent hover:text-accent-foreground",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
      )}
      {...props}
    >
      <X className="size-4" aria-hidden="true" />
    </button>
  )
}
```

---

## Confirmation Dialog

The most common modal pattern — a destructive action requires explicit confirmation.

```tsx
<Dialog open={open} onClose={onClose}>
  <div className="relative">
    <DialogClose onClose={onClose} />
    <DialogHeader>
      <div className="flex items-center gap-3 mb-2">
        <div className="flex size-10 items-center justify-center rounded-full bg-destructive/10 shrink-0">
          <AlertTriangle className="size-5 text-destructive" aria-hidden="true" />
        </div>
        <DialogTitle>Delete project?</DialogTitle>
      </div>
      <DialogDescription>
        This will permanently delete <strong className="text-foreground">{projectName}</strong> and all
        its data. This action cannot be undone.
      </DialogDescription>
    </DialogHeader>
    <DialogFooter className="pt-6">
      <Button variant="outline" onClick={onClose}>Cancel</Button>
      <Button
        variant="destructive"
        onClick={onConfirm}
        disabled={isDeleting}
        aria-busy={isDeleting}
      >
        {isDeleting && <Loader2 className="size-4 animate-spin" aria-hidden="true" />}
        Delete project
      </Button>
    </DialogFooter>
  </div>
</Dialog>
```

**Cancel is always on the left; destructive action is on the right.** This is muscle memory across all major operating systems.

---

## Form Dialog

A short form in a modal — account creation, invite user, create item.

```tsx
<Dialog open={open} onClose={onClose}>
  <form onSubmit={handleSubmit} noValidate>
    <div className="relative">
      <DialogClose onClose={onClose} />
      <DialogHeader>
        <DialogTitle>Invite team member</DialogTitle>
        <DialogDescription>
          They'll receive an email invitation to join your workspace.
        </DialogDescription>
      </DialogHeader>
      <DialogContent>
        <div className="flex flex-col gap-4">
          <FormField id="invite-email" label="Email address" required error={errors.email}>
            <input
              id="invite-email"
              type="email"
              autoFocus
              aria-invalid={!!errors.email}
              className={inputClasses}
            />
          </FormField>
          <FormField id="invite-role" label="Role">
            <select id="invite-role" className={inputClasses}>
              <option value="member">Member</option>
              <option value="admin">Admin</option>
            </select>
          </FormField>
        </div>
      </DialogContent>
      <DialogFooter>
        <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
        <Button type="submit" disabled={isSubmitting} aria-busy={isSubmitting}>
          {isSubmitting && <Loader2 className="size-4 animate-spin" aria-hidden="true" />}
          Send invite
        </Button>
      </DialogFooter>
    </div>
  </form>
</Dialog>
```

`autoFocus` on the first input — focus moves into the dialog automatically on open.

---

## Drawer (Side Sheet)

For panels with more content, settings, or contextual detail views — enters from the side, not centered.

```tsx
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="drawer-title"
  className={cn(
    "fixed inset-y-0 right-0 z-50 w-full max-w-md bg-background shadow-2xl",
    "flex flex-col border-l border-border",
    "motion-safe:animate-in motion-safe:slide-in-from-right motion-safe:duration-300 motion-safe:ease-out"
  )}
>
  <div className="flex items-center justify-between p-6 border-b border-border shrink-0">
    <h2 id="drawer-title" className="text-base font-semibold">{title}</h2>
    <button
      type="button"
      onClick={onClose}
      aria-label="Close panel"
      className={closeButtonClasses}
    >
      <X className="size-4" aria-hidden="true" />
    </button>
  </div>
  <div className="flex-1 overflow-y-auto p-6">
    {children}
  </div>
  {footer && (
    <div className="shrink-0 border-t border-border p-4 flex gap-2 justify-end">
      {footer}
    </div>
  )}
</div>
```

---

## Focus Management

Focus trapping is mandatory. When the modal opens, focus moves inside. Tab cycles through focusable elements within the modal. Escape closes the modal and returns focus to the trigger.

```tsx
function useFocusTrap(containerRef: RefObject<HTMLElement>, isActive: boolean) {
  useEffect(() => {
    if (!isActive || !containerRef.current) return
    const focusable = containerRef.current.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    const first = focusable[0]
    const last = focusable[focusable.length - 1]

    first?.focus()

    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== "Tab") return
      if (e.shiftKey) {
        if (document.activeElement === first) { e.preventDefault(); last?.focus() }
      } else {
        if (document.activeElement === last) { e.preventDefault(); first?.focus() }
      }
    }

    document.addEventListener("keydown", handleTab)
    return () => document.removeEventListener("keydown", handleTab)
  }, [isActive])
}
```

Store the trigger element reference before opening, and restore focus to it on close:

```tsx
const triggerRef = useRef<HTMLButtonElement>(null)

const handleOpen = () => {
  setOpen(true)
}
const handleClose = () => {
  setOpen(false)
  triggerRef.current?.focus()
}
```

---

## Stacked Modals

Avoid stacked modals. If a modal needs to spawn another modal, redesign the flow:
- Replace the second modal with content that expands inside the first
- Move to a multi-step flow within a single modal
- Reconsider if the nested action belongs in the modal at all

If stacking is unavoidable, each modal must independently manage focus trapping and z-index (`z-50`, `z-60`...).

---

## Animation

```tsx
// Backdrop
"motion-safe:animate-in motion-safe:fade-in motion-safe:duration-200"

// Panel enter
"motion-safe:animate-in motion-safe:fade-in motion-safe:zoom-in-95 motion-safe:duration-200"

// Drawer enter (right)
"motion-safe:animate-in motion-safe:slide-in-from-right motion-safe:duration-300 motion-safe:ease-out"

// Drawer enter (bottom — mobile sheet)
"motion-safe:animate-in motion-safe:slide-in-from-bottom motion-safe:duration-300 motion-safe:ease-out"
```

Use Tailwind's `animate-in`/`animate-out` utilities (via `tailwindcss-animate`). Never animate modals with `height` or layout properties — only `opacity`, `scale`, and `translate`.

---

## Sizing

| Content | `max-w-*` |
|---|---|
| Confirmation / simple alert | `max-w-sm` |
| Short form (2–4 fields) | `max-w-md` |
| Standard form or detail view | `max-w-lg` |
| Rich content / multi-column form | `max-w-2xl` |
| Never | `max-w-full` — use a drawer instead |

On mobile (`< sm:`), modals should take `w-full` and anchor to the bottom as a sheet:

```tsx
className="w-full sm:max-w-lg rounded-xl sm:rounded-xl rounded-b-none sm:rounded-b-xl fixed bottom-0 sm:bottom-auto sm:top-1/2 sm:-translate-y-1/2"
```

---

## Accessibility

- `role="dialog"` + `aria-modal="true"` — tells screen readers this is an interactive overlay
- `aria-labelledby` pointing to the dialog title element id — every dialog must have a visible title
- `aria-describedby` pointing to the description element id — for supplementary context
- Focus trap: Tab cycles within the dialog only
- Escape closes: always, without exceptions
- Return focus: close → focus returns to the element that opened the dialog
- Backdrop click: should close the dialog (treat as Escape). Exception: forms with unsaved data — confirm intent before closing
- `document.body.style.overflow = "hidden"` on open to prevent background scroll

---

## Common Pitfalls

- **Modal without focus trap:** Tab escapes the modal and interacts with background content — a critical accessibility failure
- **No Escape key handler:** keyboard users expect Escape to always close a modal
- **Backdrop not closing the dialog:** closing on backdrop click is expected behavior — always implement it (except for unsaved-data guards)
- **Missing `aria-modal`:** without `aria-modal="true"`, some screen readers will still read background content
- **Scroll not locked:** background content scrolls while the modal is open. Set `overflow: hidden` on `body` on open and restore on close
- **Focus not returned on close:** users lose their place in the page when focus isn't restored to the trigger element
- **Stacked modals:** redesign instead of stacking
- **Bottom sheet not used on mobile:** a centered modal on a small screen is harder to reach than a bottom sheet. Consider adapting at `sm:` breakpoint
