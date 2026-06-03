# SKILL — Footer

Applies within CONFIG.md and METHOD.md constraints. Works alongside any STYLES/ or PATTERNS/ file.

---

## Core Principle

The footer is the end of the page — not an afterthought. It serves three purposes: secondary navigation for users who scrolled past the main nav, legal and compliance anchors, and a closing compositional beat. The footer earns its space when it does these three jobs clearly; it fails when it becomes a dumped list of every page on the site.

---

## Anatomy

| Zone | Content | Required |
|---|---|---|
| Brand | Logo + tagline or brief description | Yes |
| Navigation columns | Grouped links by category | Contextual |
| Social links | Platform icons with accessible labels | Optional |
| Bottom bar | Copyright, legal links, locale selector | Yes |
| Newsletter / CTA | Optional signup or secondary CTA | Optional |

---

## Standard Multi-Column Footer

The most versatile footer — brand left, link columns right, bottom bar full-width.

```tsx
<footer className="border-t border-border bg-background">
  <div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
    <div className="grid grid-cols-2 gap-8 sm:grid-cols-3 lg:grid-cols-5">

      {/* Brand column — spans 2 at lg */}
      <div className="col-span-2 sm:col-span-3 lg:col-span-2">
        <a href="/" className="flex items-center gap-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-sm w-fit" aria-label="Home">
          <Logo className="size-6" aria-hidden="true" />
          <span className="font-semibold text-sm">{siteName}</span>
        </a>
        <p className="mt-4 text-sm text-muted-foreground max-w-xs leading-relaxed">
          {tagline}
        </p>
        {socialLinks && (
          <div className="mt-6 flex items-center gap-3">
            {socialLinks.map((link) => (
              <a
                key={link.platform}
                href={link.href}
                aria-label={`${siteName} on ${link.platform}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-foreground transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-sm"
              >
                <link.icon className="size-4" aria-hidden="true" />
              </a>
            ))}
          </div>
        )}
      </div>

      {/* Link columns */}
      {navColumns.map((column) => (
        <div key={column.label}>
          <h3 className="text-xs font-semibold uppercase tracking-wider text-foreground mb-4">
            {column.label}
          </h3>
          <ul role="list" className="flex flex-col gap-3">
            {column.links.map((link) => (
              <li key={link.href}>
                <a
                  href={link.href}
                  className="text-sm text-muted-foreground hover:text-foreground transition-colors duration-150"
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  </div>

  {/* Bottom bar */}
  <div className="border-t border-border">
    <div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
      <p className="text-xs text-muted-foreground">
        © {new Date().getFullYear()} {siteName}. All rights reserved.
      </p>
      <nav aria-label="Legal navigation">
        <ul role="list" className="flex items-center gap-4 sm:gap-6">
          {legalLinks.map((link) => (
            <li key={link.href}>
              <a href={link.href} className="text-xs text-muted-foreground hover:text-foreground transition-colors duration-150">
                {link.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  </div>
</footer>
```

---

## Minimal Footer

For single-product sites, landing pages, or apps where the footer is purely legal:

```tsx
<footer className="border-t border-border">
  <div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col sm:flex-row items-center justify-between gap-4">
    <a href="/" className="flex items-center gap-2 text-sm font-semibold focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-sm">
      <Logo className="size-5" aria-hidden="true" />
      {siteName}
    </a>
    <p className="text-xs text-muted-foreground order-last sm:order-none">
      © {new Date().getFullYear()} {siteName}
    </p>
    <nav aria-label="Footer navigation">
      <ul role="list" className="flex items-center gap-4">
        {links.map((link) => (
          <li key={link.href}>
            <a href={link.href} className="text-xs text-muted-foreground hover:text-foreground transition-colors duration-150">
              {link.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  </div>
</footer>
```

---

## Footer with Newsletter Signup

Place the signup above the navigation columns, not inside them — it has different visual weight.

```tsx
<footer className="border-t border-border bg-background">
  <div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-12">

    {/* Newsletter band */}
    <div className="mb-12 pb-12 border-b border-border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
      <div>
        <h3 className="text-sm font-semibold text-foreground">Stay up to date</h3>
        <p className="text-sm text-muted-foreground mt-1">Get the latest updates delivered to your inbox.</p>
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2 w-full sm:w-auto" aria-label="Newsletter signup">
        <label htmlFor="newsletter-email" className="sr-only">Email address</label>
        <input
          id="newsletter-email"
          type="email"
          placeholder="your@email.com"
          required
          className="flex-1 sm:w-64 h-9 rounded-md border border-input bg-background px-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
        />
        <Button type="submit" size="sm">Subscribe</Button>
      </form>
    </div>

    {/* ... rest of multi-column footer ... */}
  </div>
</footer>
```

The `sr-only` label is required even when placeholder text describes the field. Placeholder alone is not accessible labeling.

---

## Dark Footer Variant

Inverted footer on a light-background site — a compositional closing beat.

```tsx
<footer className="bg-foreground text-background">
  <div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
    {/* Brand */}
    <div className="mb-10 pb-10 border-b border-background/10">
      <a href="/" className="flex items-center gap-2 text-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-background focus-visible:ring-offset-2 focus-visible:ring-offset-foreground rounded-sm w-fit">
        <Logo className="size-6" aria-hidden="true" />
        <span className="font-semibold">{siteName}</span>
      </a>
    </div>

    {/* Columns using background/70 for muted text */}
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-8">
      {navColumns.map((column) => (
        <div key={column.label}>
          <h3 className="text-xs font-semibold uppercase tracking-wider text-background mb-4">
            {column.label}
          </h3>
          <ul role="list" className="flex flex-col gap-3">
            {column.links.map((link) => (
              <li key={link.href}>
                <a href={link.href} className="text-sm text-background/70 hover:text-background transition-colors duration-150">
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>

    <div className="mt-12 pt-8 border-t border-background/10 flex flex-col sm:flex-row justify-between gap-4">
      <p className="text-xs text-background/60">© {new Date().getFullYear()} {siteName}</p>
      <ul role="list" className="flex gap-6">
        {legalLinks.map((link) => (
          <li key={link.href}>
            <a href={link.href} className="text-xs text-background/60 hover:text-background transition-colors duration-150">
              {link.label}
            </a>
          </li>
        ))}
      </ul>
    </div>
  </div>
</footer>
```

**Never use `text-white` or `text-black`** — use `text-background` and `text-foreground` with opacity modifiers (`/70`, `/60`) to maintain semantic color usage in inverted contexts.

---

## Editorial / Large-Type Footer

For agencies, portfolios, and editorial sites where the footer is a design element:

```tsx
<footer className="border-t border-border overflow-hidden">
  {/* Large type statement */}
  <div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-8">
    <p className="text-5xl sm:text-7xl lg:text-8xl font-black tracking-tighter text-foreground leading-none mb-12">
      {closingStatement}
    </p>
    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 pt-8 border-t border-border">
      <div className="flex items-center gap-6">
        {socialLinks.map((link) => (
          <a key={link.platform} href={link.href} aria-label={link.platform} target="_blank" rel="noopener noreferrer" className="text-sm text-muted-foreground hover:text-foreground transition-colors duration-150">
            {link.platform}
          </a>
        ))}
      </div>
      <p className="text-xs text-muted-foreground">© {new Date().getFullYear()} {siteName}</p>
    </div>
  </div>
</footer>
```

---

## Navigation Column Groupings

Good grouping reflects how users think, not how the site is organized internally.

| Group label | What goes in it |
|---|---|
| Product | Features, pricing, changelog, roadmap |
| Company | About, blog, careers, press |
| Resources | Docs, tutorials, API reference, status |
| Legal | Privacy, Terms, Cookie policy, Licenses |
| Support | Help center, contact, community, status |

Keep each column to 4–7 links. More than 7 and the column reads as a sitemap, not navigation.

---

## Responsive Behavior

| Breakpoint | Layout |
|---|---|
| Mobile | Single column, brand on top, columns stacked |
| sm (640px) | 2-column link grid |
| lg (1024px) | Full multi-column layout with brand column |

On mobile, collapse long link columns into a single scroll list — do not use accordions unless column count exceeds 4.

---

## Accessibility

- `<footer>` is a landmark element — screen readers can jump to it directly. No `role` needed; the element semantics are sufficient.
- The main footer and any secondary footers (within an `<article>` for example) are distinct landmarks — the document `<footer>` relates to the whole page.
- `aria-label="Footer navigation"` distinguishes the footer `<nav>` from the header `<nav>` when both exist on the page.
- Social icons are icon-only links — they require `aria-label` with platform name and context: `aria-label="Follow us on Twitter"`.
- External links (`target="_blank"`): include `rel="noopener noreferrer"`. Consider adding a visually-hidden notice or `title` attribute that it opens in a new tab.
- Copyright year: use `{new Date().getFullYear()}` — never hardcode a year that will go stale.

---

## Common Pitfalls

- **Sitemap footer:** 50+ links in 8 columns is a maintenance burden and visual noise. Audit ruthlessly — if a page doesn't justify a footer link, it doesn't get one.
- **Missing legal links:** Privacy Policy and Terms of Service are legally required in most jurisdictions. They belong in the footer bottom bar.
- **Footer as design afterthought:** the footer is visible on every page. A `py-4 text-xs` afterthought looks like a site that ran out of budget. Give it proper padding and a compositional closing beat.
- **Social icon links with no accessible name:** icon-only links are invisible to screen readers without `aria-label`.
- **Hardcoded copyright year:** this becomes inaccurate as soon as the year changes. Always generate dynamically.
- **No footer `<nav>`:** link columns should live inside a `<nav>` with an accessible name, not in plain `<div>` containers.
