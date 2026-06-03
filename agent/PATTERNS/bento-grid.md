# PATTERN — Bento Grid

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

A grid of cards with varied sizes — some spanning multiple columns or rows — arranged to create visual rhythm, hierarchy, and density. Named after the Japanese bento box: compartments of different sizes, all fitting together without gaps. Popular for feature showcases, portfolio grids, and product marketing.

---

## When to Use

- Feature sections with 4–8 features of varying importance
- Portfolio or product galleries with mixed content formats
- Dashboard-style marketing pages
- Showcasing diverse capabilities or content types in a single section

---

## Foundation: CSS Grid with Named Areas

The most robust approach for complex bento layouts:

```tsx
<section className="grid auto-rows-[minmax(200px,auto)] grid-cols-4 gap-4 p-4">
  {/* Spanning cells */}
  <div className="col-span-4 rounded-xl bg-card p-8 lg:col-span-2">Hero feature</div>
  <div className="col-span-2 rounded-xl bg-card p-8 lg:col-span-1">Small feature</div>
  <div className="col-span-2 rounded-xl bg-card p-8 lg:col-span-1">Small feature</div>
  <div className="col-span-4 rounded-xl bg-card p-8 lg:col-span-2 lg:row-span-2">Tall feature</div>
  <div className="col-span-4 rounded-xl bg-card p-8 lg:col-span-1">Compact</div>
  <div className="col-span-4 rounded-xl bg-card p-8 lg:col-span-1">Compact</div>
</section>
```

---

## Common Bento Configurations

### 2-1-1 (Hero + two small)

```tsx
<div className="grid grid-cols-3 gap-4">
  <div className="col-span-3 lg:col-span-2 rounded-xl bg-card p-8 aspect-[2/1]">
    {/* Hero — 2/3 width */}
  </div>
  <div className="col-span-3 lg:col-span-1 rounded-xl bg-card p-6">
    {/* Small — 1/3 width */}
  </div>
</div>
```

### 1-2-1 (Three columns, center spans two rows)

```tsx
<div className="grid grid-cols-3 grid-rows-2 gap-4" style={{ height: "600px" }}>
  <div className="col-span-1 row-span-1 rounded-xl bg-card p-6">Top left</div>
  <div className="col-span-1 row-span-2 rounded-xl bg-card p-6">Tall center</div>
  <div className="col-span-1 row-span-1 rounded-xl bg-card p-6">Top right</div>
  <div className="col-span-1 row-span-1 rounded-xl bg-card p-6">Bottom left</div>
  <div className="col-span-1 row-span-1 rounded-xl bg-card p-6">Bottom right</div>
</div>
```

### 4-column mixed

```tsx
<div className="grid grid-cols-4 auto-rows-[280px] gap-4">
  <div className="col-span-4 md:col-span-2 rounded-xl bg-card p-8">2-col wide</div>
  <div className="col-span-4 md:col-span-1 rounded-xl bg-card p-6">1-col</div>
  <div className="col-span-4 md:col-span-1 rounded-xl bg-card p-6">1-col</div>
  <div className="col-span-4 md:col-span-1 rounded-xl bg-card p-6">1-col</div>
  <div className="col-span-4 md:col-span-3 rounded-xl bg-card p-8">3-col wide</div>
</div>
```

---

## Card Content Patterns

### Stat card

```tsx
<div className="flex flex-col justify-between rounded-xl bg-card p-8 h-full">
  <span className="text-xs uppercase tracking-widest text-muted-foreground">{label}</span>
  <div>
    <p className="text-6xl font-black tabular-nums">{value}</p>
    <p className="mt-1 text-sm text-muted-foreground">{description}</p>
  </div>
</div>
```

### Visual card (image fills, text overlays)

```tsx
<div className="relative overflow-hidden rounded-xl h-full">
  <img src={src} alt={alt} className="w-full h-full object-cover" />
  <div className="absolute inset-0 bg-gradient-to-t from-foreground/80 to-transparent" />
  <div className="absolute bottom-0 p-6">
    <h3 className="text-xl font-semibold text-white">{title}</h3>
    <p className="mt-1 text-sm text-white/70">{description}</p>
  </div>
</div>
```

### Feature card (icon + text)

```tsx
<div className="flex flex-col gap-4 rounded-xl border bg-card p-8 h-full">
  <div className="rounded-lg bg-primary/10 p-3 w-fit">
    <Icon className="h-5 w-5 text-primary" />
  </div>
  <div>
    <h3 className="font-semibold">{title}</h3>
    <p className="mt-1 text-sm text-muted-foreground leading-relaxed">{description}</p>
  </div>
</div>
```

### Interactive/demo card (live element inside bento)

```tsx
<div className="rounded-xl bg-card p-8 h-full flex flex-col gap-4 overflow-hidden">
  <div className="flex items-center justify-between">
    <h3 className="font-semibold text-sm">{title}</h3>
    <span className="text-xs text-muted-foreground">{label}</span>
  </div>
  {/* Live interactive element: chart, toggle, animation */}
  <div className="flex-1 rounded-lg bg-muted/50 overflow-hidden">
    {demoContent}
  </div>
</div>
```

---

## Visual Hierarchy in Bento

- The largest cell is always the most important feature
- Use background color, imagery, or size to establish hierarchy across cells
- One cell can have a contrasting background (`bg-primary text-primary-foreground`) to create a focal anchor
- All cells should have equal visual weight per unit area — a large empty card and a small packed card feel unbalanced

```tsx
{/* Accent cell for hierarchy */}
<div className="col-span-2 rounded-xl bg-primary p-8 text-primary-foreground">
  <p className="text-4xl font-black">The main claim</p>
  <p className="mt-2 text-sm text-primary-foreground/70">Supporting detail</p>
</div>
```

---

## Hover Interactions

Bento cards benefit from subtle hover responses:

```tsx
<div className="group rounded-xl border bg-card p-8 transition-all duration-300 hover:shadow-lg hover:-translate-y-1 hover:border-primary/30">
  {/* Content */}
  <div className="h-8 w-8 rounded-lg bg-primary/10 p-1.5 transition-colors duration-300 group-hover:bg-primary/20">
    <Icon className="text-primary" />
  </div>
</div>
```

---

## Responsive Collapse

Bento grids must degrade gracefully to single-column or simple 2-column on mobile:

```tsx
<div className={cn(
  "grid gap-4",
  "grid-cols-1",           // Mobile: single column
  "sm:grid-cols-2",        // Tablet: 2 column
  "lg:grid-cols-4",        // Desktop: full bento
)}>
  {/* On mobile, all col-span-* revert to full width automatically if grid-cols is 1 */}
  <div className="sm:col-span-2 lg:col-span-2">Hero</div>
  <div className="sm:col-span-1 lg:col-span-1">Small</div>
  <div className="sm:col-span-1 lg:col-span-1">Small</div>
</div>
```

---

## Common Pitfalls

- **Uniform cells:** every cell the same size defeats the purpose. Vary size aggressively — the contrast is the point.
- **Too many cells:** 10+ items in a bento becomes overwhelming. 4–8 is the sweet spot.
- **Content doesn't match cell size:** small text in a large hero cell feels sparse; complex diagrams in tiny cells feel cramped. Design content for its cell size.
- **Gap too small:** tight gaps remove the visual separation that defines individual cells. `gap-4` minimum; `gap-6` or `gap-8` for breathing room.
- **No hierarchy:** all cells equal visual weight — no way to know where to start. Use size, color, or position to establish one clear dominant cell.
- **Forgetting auto-rows:** without `auto-rows`, row heights depend on content and rows collapse inconsistently. Set `auto-rows` to a base height and let spanning cells multiply it.
