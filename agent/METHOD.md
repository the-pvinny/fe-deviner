# METHOD — Component Structure & Patterns

This file defines how components are built. CONFIG.md defines what tokens to use; this file defines how to use them. These rules are non-negotiable regardless of style or pattern context.

---

## Output Format

Default output is **React (TSX) with Tailwind v4 utility classes**. When HTML is explicitly requested, output semantic HTML with the same Tailwind classes. Never mix React and plain HTML in a single output.

### React Component Structure

```tsx
function ComponentName({ variant = "default", size = "md", className, ...props }) {
  return (
    <div
      className={cn("rounded-md border bg-card", variantClasses[variant], className)}
      {...props}
    >
      {/* content */}
    </div>
  )
}
```

**Rules:**

- One component per output unless composing a layout
- Props use destructuring with defaults
- `className` is always accepted and merged last via `cn()` (clsx + tailwind-merge)
- Spread remaining props with `{...props}` for composability
- Export as named export, not default export
- Component name is PascalCase, descriptive, no abbreviations

### Composition over Monoliths

Break complex UI into composable parts. A card is `Card`, `CardHeader`, `CardContent`, `CardFooter` — not a single component with 12 props. Follow shadcn/ui's compound component pattern:

```tsx
function Card({ className, ...props }) {
  return <div className={cn("rounded-lg border bg-card text-card-foreground shadow-sm", className)} {...props} />
}

function CardHeader({ className, ...props }) {
  return <div className={cn("flex flex-col gap-1.5 p-6", className)} {...props} />
}

function CardContent({ className, ...props }) {
  return <div className={cn("p-6 pt-0", className)} {...props} />
}

function CardFooter({ className, ...props }) {
  return <div className={cn("flex items-center p-6 pt-0", className)} {...props} />
}
```

### Variant Pattern

Use a variant map object when a component has distinct visual modes. Do not use ternaries for more than 2 states.

```tsx
const buttonVariants = {
  default: "bg-primary text-primary-foreground shadow-xs hover:bg-primary/90",
  destructive: "bg-destructive text-primary-foreground shadow-xs hover:bg-destructive/90",
  outline: "border border-input bg-background shadow-xs hover:bg-accent hover:text-accent-foreground",
  secondary: "bg-secondary text-secondary-foreground shadow-xs hover:bg-secondary/80",
  ghost: "hover:bg-accent hover:text-accent-foreground",
  link: "text-primary underline-offset-4 hover:underline",
}

const buttonSizes = {
  sm: "h-8 rounded-md px-3 text-xs",
  md: "h-9 rounded-md px-4 text-sm",
  lg: "h-10 rounded-md px-6 text-base",
  icon: "size-9 rounded-md",
}
```

For complex variant logic spanning many dimensions, use `cva` (class-variance-authority) or an equivalent.

---

## Semantic HTML

Use the right element for the job. Styling does not replace semantics.

| Content | Element | Not this |
|---|---|---|
| Page section | `<section>` with heading | `<div>` |
| Navigation | `<nav>` | `<div className="nav">` |
| Main content | `<main>` | `<div id="main">` |
| Article/post | `<article>` | `<div>` |
| Side content | `<aside>` | `<div className="sidebar">` |
| Page footer | `<footer>` | `<div>` |
| Heading | `<h1>`–`<h6>` in order | `<p className="text-3xl font-bold">` |
| Button that does something | `<button>` | `<div onClick>` |
| Link that navigates | `<a>` or framework `<Link>` | `<button onClick={navigate}>` |
| List of items | `<ul>` / `<ol>` + `<li>` | Stacked `<div>`s |
| Form field label | `<label htmlFor>` | `<span>` next to input |
| Image | `<img>` with `alt` | Background image for content |
| Data | `<table>` with `<thead>`/`<tbody>` | Grid of divs |

**Heading hierarchy:** Never skip levels. Every `<section>` should start with a heading. `<h1>` appears once per page.

---

## Accessibility

Non-optional. Every component must meet WCAG 2.1 AA as a baseline.

### Interactive Elements

- Every `<button>` and `<a>` must have accessible text (visible label, `aria-label`, or `aria-labelledby`)
- Every form input must have an associated `<label>` — either wrapping the input or using `htmlFor`/`id`
- Custom interactive elements (dropdowns, tabs, modals) must use appropriate ARIA roles and keyboard patterns
- Focus must be visible — `focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2` as minimum
- Focus order must follow visual order — no `tabindex` hacks unless absolutely necessary

### Keyboard Navigation

- All interactive elements reachable via Tab
- Escape closes modals/popovers/dropdowns
- Enter/Space activates buttons and links
- Arrow keys navigate within composite widgets (tabs, menus, listboxes)
- Focus trapping in modals — Tab cycles within the modal, not behind it

### Screen Reader Support

- Decorative images: `alt=""`and `aria-hidden="true"`
- Icon-only buttons: `aria-label` describing the action, not the icon
- Live regions for dynamic content: `aria-live="polite"` for non-urgent updates, `aria-live="assertive"` for errors
- Status messages use `role="status"` or `role="alert"`
- Loading states announced with `aria-busy="true"`

### Color and Contrast

- Text contrast ratio: minimum 4.5:1 (normal text), 3:1 (large text ≥18px or ≥14px bold)
- UI component contrast: minimum 3:1 against adjacent colors
- Never rely on color alone to convey information — pair with icons, text, or patterns
- Ensure all states (hover, focus, active, disabled) maintain sufficient contrast

### Motion

- Respect `prefers-reduced-motion` — wrap animations in `motion-safe:` or disable via media query
- No auto-playing animations that cannot be paused
- No content that flashes more than 3 times per second

---

## Responsive Design

Mobile-first. Base classes target mobile; use breakpoint prefixes to layer up.

### Breakpoints (Tailwind v4 defaults)

| Prefix | Min-width | Target |
|---|---|---|
| (none) | 0px | Mobile phones |
| `sm:` | 640px | Large phones, small tablets |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Small laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large screens |

### Layout Rules

- Stack vertically on mobile, reflow to horizontal on `md:` or `lg:`
- Touch targets: minimum 44×44px on mobile (use `min-h-11 min-w-11` or `p-3` on small targets)
- No horizontal scroll on any breakpoint — if content overflows, the layout is wrong
- Typography scales down on mobile — don't use `text-7xl` without a responsive reduction
- Images are responsive by default — `w-full` or `max-w-*` with aspect ratio preservation
- Container: use `max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8` as standard page wrapper

---

## Naming Conventions

- **Components:** PascalCase — `UserProfileCard`, `NavigationMenu`
- **Props:** camelCase — `isLoading`, `onSubmit`, `initialValue`
- **Variants:** lowercase strings — `"default"`, `"destructive"`, `"outline"`
- **CSS variables:** kebab-case — `--primary-foreground`, `--sidebar-accent`
- **Files:** kebab-case matching component — `user-profile-card.tsx`
- **Event handlers:** `on` + action — `onClick`, `onSubmit`, `onDismiss`

---

## State Patterns

### Loading

```tsx
<button
  type="button"
  disabled
  aria-busy="true"
  className="inline-flex h-9 items-center justify-center gap-2 rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
>
  <Loader2 className="size-4 animate-spin" aria-hidden="true" />
  <span>Loading...</span>
</button>
```

### Empty State

Always provide an empty state — never render a blank area. Include an action when possible.

### Error State

Show inline errors near the source. Use `role="alert"` for form validation. Destructive color for error text. Include recovery guidance, not just the error.

### Disabled State

Reduce opacity (`opacity-50`), remove pointer events (`pointer-events-none`), add `aria-disabled="true"`. Disabled elements must still be visible and identifiable.

---

## Data Attributes

Use `data-slot` on component root elements for external styling hooks (shadcn/ui convention). Use `data-state` for stateful components (open/closed, active/inactive).

```tsx
<div data-slot="card" data-state={isOpen ? "open" : "closed"}>
  {/* card content */}
</div>
```

---

## Eval Gate (required before shipping output)

Run the deterministic validators on every generated file. See **`agent/EVAL.md`** for the workflow, common failure clusters, and reference samples in `samples/`.

```bash
python -m eval path/to/component.tsx -v --fail-on-violations
```

---

## Import Conventions

- UI primitives from `@/components/ui/*`
- Utility functions from `@/lib/utils`
- Icons from `lucide-react` (default) — always tree-shakeable named imports
- No default imports for libraries — use named imports for clarity
- Keep imports sorted: external packages → internal aliases → relative paths
