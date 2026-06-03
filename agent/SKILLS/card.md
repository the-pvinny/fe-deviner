# SKILL — Card

Applies within CONFIG.md and METHOD.md constraints. Works alongside any STYLES/ or PATTERNS/ file.

---

## Core Principle

A card is a bounded surface that groups related content and optionally triggers an action. It is a container, not a component — its power comes from what you put in it and how the parts relate. Always compose from parts; never jam everything into a monolith.

---

## Anatomy — Compound Structure

```tsx
function Card({ className, ...props }) {
  return (
    <div
      data-slot="card"
      className={cn("rounded-lg border bg-card text-card-foreground shadow-sm", className)}
      {...props}
    />
  )
}

function CardHeader({ className, ...props }) {
  return <div data-slot="card-header" className={cn("flex flex-col gap-1.5 p-6", className)} {...props} />
}

function CardTitle({ className, ...props }) {
  return <h3 data-slot="card-title" className={cn("text-base font-semibold leading-tight", className)} {...props} />
}

function CardDescription({ className, ...props }) {
  return <p data-slot="card-description" className={cn("text-sm text-muted-foreground", className)} {...props} />
}

function CardContent({ className, ...props }) {
  return <div data-slot="card-content" className={cn("p-6 pt-0", className)} {...props} />
}

function CardFooter({ className, ...props }) {
  return (
    <div data-slot="card-footer" className={cn("flex items-center p-6 pt-0 gap-2", className)} {...props} />
  )
}
```

**Never** put `CardTitle` directly inside `Card` — always via `CardHeader`. The slot chain must be respected so external styles and data attributes target the correct layer.

---

## Core Variants

### Default (informational, no action)

```tsx
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Supporting description at a glance.</CardDescription>
  </CardHeader>
  <CardContent>
    <p className="text-sm text-foreground">Body content lives here.</p>
  </CardContent>
</Card>
```

### Interactive (full-card click target)

Wrap in an anchor or button. Make the entire surface the hit target — not a small "Read more" buried in the footer.

```tsx
<a href={href} className="group block focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-lg">
  <Card className="transition-all duration-200 hover:shadow-md hover:-translate-y-0.5 group-focus-visible:ring-2 group-focus-visible:ring-ring">
    <CardHeader>
      <CardTitle>{title}</CardTitle>
    </CardHeader>
    <CardContent>{children}</CardContent>
  </Card>
</a>
```

### Media card (image + content)

```tsx
<Card className="overflow-hidden">
  <div className="overflow-hidden aspect-video">
    <img
      src={src}
      alt={alt}
      className="w-full h-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
    />
  </div>
  <CardHeader>
    <CardTitle>{title}</CardTitle>
    <CardDescription>{description}</CardDescription>
  </CardHeader>
  <CardFooter>
    <button
      type="button"
      className="inline-flex h-8 items-center justify-center rounded-md border border-input bg-background px-3 text-xs font-medium shadow-xs transition-colors duration-150 hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
    >
      Read more
    </button>
  </CardFooter>
</Card>
```

Use `aspect-video` (16:9) as default. Use `aspect-square` for product grids and portrait tiles. Do not use arbitrary aspect ratios (`aspect-[4/5]`) — they fail CONFIG validation.

### Stat / metric card

```tsx
<Card>
  <CardHeader className="flex flex-row items-center justify-between pb-2">
    <CardTitle className="text-sm font-medium text-muted-foreground">{label}</CardTitle>
    <Icon className="size-4 text-muted-foreground" aria-hidden="true" />
  </CardHeader>
  <CardContent>
    <p className="text-2xl font-bold">{value}</p>
    <p className="text-xs text-muted-foreground mt-1">{trend}</p>
  </CardContent>
</Card>
```

---

## Card Grids

```tsx
// Responsive 3-column grid
<ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6" role="list">
  {items.map((item) => (
    <li key={item.id}>
      <Card>{/* ... */}</Card>
    </li>
  ))}
</ul>
```

Use `<ul>` + `<li>` for card grids — they are a list of items. Use `role="list"` to restore list semantics in Safari when `list-style: none` is applied.

Gap hierarchy: `gap-4` for dense/compact, `gap-6` for standard, `gap-8` for editorial.

---

## Horizontal Card

Content alongside media — common for search results, news items, or compact product rows:

```tsx
<Card className="flex flex-row overflow-hidden">
  <div className="w-32 shrink-0 sm:w-48">
    <img src={src} alt={alt} className="w-full h-full object-cover" />
  </div>
  <div className="flex flex-col justify-between min-w-0">
    <CardHeader>
      <CardTitle className="line-clamp-2">{title}</CardTitle>
      <CardDescription>{meta}</CardDescription>
    </CardHeader>
    <CardFooter>{action}</CardFooter>
  </div>
</Card>
```

`min-w-0` on the flex child prevents text from overflowing the card boundary. `line-clamp-2` on titles prevents multi-line overflow in list contexts.

---

## Loading State

Replace content with skeleton shapes — never show empty structure.

```tsx
<Card>
  <CardHeader>
    <div className="h-4 w-3/4 rounded-md bg-muted animate-pulse" />
    <div className="h-3 w-1/2 rounded-md bg-muted animate-pulse mt-1" />
  </CardHeader>
  <CardContent>
    <div className="space-y-2">
      <div className="h-3 w-full rounded-md bg-muted animate-pulse" />
      <div className="h-3 w-5/6 rounded-md bg-muted animate-pulse" />
      <div className="h-3 w-4/6 rounded-md bg-muted animate-pulse" />
    </div>
  </CardContent>
</Card>
```

Wrap the entire skeleton card in `aria-hidden="true"` and provide a visually-hidden loading announcement elsewhere via `aria-live="polite"`.

---

## Empty State Card

When a card grid has no items — never render a blank space.

```tsx
<Card className="flex flex-col items-center justify-center py-16 text-center">
  <CardContent>
    <Icon className="size-10 text-muted-foreground mx-auto mb-4" aria-hidden="true" />
    <p className="text-sm font-medium text-foreground mb-1">No items yet</p>
    <p className="text-sm text-muted-foreground mb-4 max-w-xs">
      When items appear, they will show up here.
    </p>
    <Button size="sm">Add item</Button>
  </CardContent>
</Card>
```

---

## Depth and Elevation

Elevation signals interactivity and hierarchy — not decoration.

| Situation | Classes |
|---|---|
| Flat / non-interactive | `border bg-card` — no shadow |
| Default / resting | `border bg-card shadow-sm` |
| Hover / lifted | `shadow-md -translate-y-0.5` |
| Raised / prominent | `shadow-lg` |
| Overlay / modal surface | `shadow-xl` |

Never use `shadow-2xl` on a card inside a page — reserve it for modals and drawers that float above the whole layout.

---

## Accessibility

- Cards that are purely informational require no special ARIA — they are `<div>` containers
- Interactive cards with a single action: wrap in `<a>` or `<button>`, not a `<div onClick>`
- Cards with multiple actions: keep the card as a container, put focus on individual actions inside
- Never duplicate a link/button label — if the card title is also the link text, use `aria-label` on the link to include context: `aria-label="Read more about {title}"`
- Image alt text must describe the image content, not the card topic (different things)

---

## Common Pitfalls

- **Nested interactive elements:** an `<a>` wrapping a `CardFooter` that contains another `<button>` creates invalid HTML (interactive inside interactive). Pick one: full-card link or individual actions, not both.
- **Overflow without hidden:** images at the top of a card without `overflow-hidden` on the card will ignore `rounded-lg` at the corner. Set `overflow-hidden` on the card, or on a wrapping div inside.
- **Forgotten `pt-0`:** `CardContent` has `pt-0` to avoid double-padding with `CardHeader`. Removing it is a padding bug waiting to happen.
- **Title as `<h1>`:** `CardTitle` defaults to `<h3>`. Override with `as` prop or wrapping heading if context requires, but never use `<h1>` in a card — there is only one per page.
- **Flat skeletons look like content:** always animate skeleton states with `animate-pulse`. Static gray blocks read as content.
