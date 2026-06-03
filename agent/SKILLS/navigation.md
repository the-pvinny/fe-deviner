# SKILL — Navigation

Applies within CONFIG.md and METHOD.md constraints. Works alongside any STYLES/ or PATTERNS/ file.

---

## Core Principle

Navigation is infrastructure. It should always be findable, never surprising, and never compete with the content it serves. The best navigation disappears when the user is engaged with a page and reappears instantly when they need to move. Clarity beats cleverness.

---

## Top Navigation — Structure

```tsx
<header className="sticky top-0 z-30 w-full border-b border-border bg-background/95 backdrop-blur-sm supports-[backdrop-filter]:bg-background/60">
  <nav
    aria-label="Main navigation"
    className="max-w-screen-xl mx-auto flex h-16 items-center px-4 sm:px-6 lg:px-8"
  >
    {/* Brand */}
    <a href="/" className="flex items-center gap-2 shrink-0 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-sm" aria-label="Home">
      <Logo className="size-6" aria-hidden="true" />
      <span className="font-semibold text-sm">{siteName}</span>
    </a>

    {/* Desktop links */}
    <ul role="list" className="hidden md:flex items-center gap-1 ml-8">
      {links.map((link) => (
        <li key={link.href}>
          <a
            href={link.href}
            aria-current={isActive(link.href) ? "page" : undefined}
            className={cn(
              "px-3 py-1.5 rounded-md text-sm transition-colors duration-150",
              "hover:bg-accent hover:text-accent-foreground",
              "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
              isActive(link.href)
                ? "bg-accent text-accent-foreground font-medium"
                : "text-muted-foreground"
            )}
          >
            {link.label}
          </a>
        </li>
      ))}
    </ul>

    {/* Actions — right side */}
    <div className="ml-auto flex items-center gap-2">
      <Button variant="ghost" size="sm" className="hidden md:inline-flex">Sign in</Button>
      <Button size="sm" className="hidden md:inline-flex">Get started</Button>
      {/* Mobile menu trigger */}
      <MobileMenuToggle />
    </div>
  </nav>
</header>
```

**`sticky top-0 z-30`** — nav sits above content (`z-30`) but below modals (`z-40+`). Always sticky by default; use `fixed` only for edge cases requiring full-viewport layering.

**`backdrop-blur-sm`** — frosted glass effect when scrolling beneath. Pair with slightly transparent background (`bg-background/95`). The `supports-[backdrop-filter]` prefix ensures fallback to solid background on browsers without support.

---

## Mobile Menu — Toggle Pattern

```tsx
function MobileMenuToggle({ isOpen, onToggle }) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-expanded={isOpen}
      aria-controls="mobile-menu"
      aria-label={isOpen ? "Close menu" : "Open menu"}
      className={cn(
        "md:hidden flex items-center justify-center size-9 rounded-md",
        "transition-colors duration-150 hover:bg-accent",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
      )}
    >
      {isOpen
        ? <X className="size-5" aria-hidden="true" />
        : <Menu className="size-5" aria-hidden="true" />
      }
    </button>
  )
}
```

```tsx
{/* Mobile menu panel */}
<div
  id="mobile-menu"
  role="dialog"
  aria-modal="true"
  aria-label="Navigation menu"
  className={cn(
    "md:hidden fixed inset-x-0 top-16 z-30 border-b border-border bg-background",
    "transition-all duration-300 ease-out",
    isOpen ? "opacity-100 translate-y-0" : "opacity-0 -translate-y-2 pointer-events-none"
  )}
>
  <nav className="px-4 py-4 flex flex-col gap-1">
    {links.map((link) => (
      <a
        key={link.href}
        href={link.href}
        aria-current={isActive(link.href) ? "page" : undefined}
        className={cn(
          "px-3 py-2.5 rounded-md text-sm transition-colors duration-150",
          "hover:bg-accent hover:text-accent-foreground",
          isActive(link.href) ? "bg-accent font-medium" : "text-muted-foreground"
        )}
        onClick={() => setIsOpen(false)}
      >
        {link.label}
      </a>
    ))}
    <div className="pt-3 mt-3 border-t border-border flex flex-col gap-2">
      <Button variant="outline" className="w-full">Sign in</Button>
      <Button className="w-full">Get started</Button>
    </div>
  </nav>
</div>
```

Close the mobile menu when a link is clicked (`onClick={() => setIsOpen(false)}`), when Escape is pressed, and when the viewport widens past `md:`.

---

## Dropdown Navigation (Mega Menu)

For nav items with sub-pages, use a dropdown anchored to the nav item:

```tsx
<li className="relative" role="none">
  <button
    type="button"
    aria-expanded={isDropdownOpen}
    aria-haspopup="true"
    className={cn(navItemClasses, "flex items-center gap-1")}
  >
    {label}
    <ChevronDown
      className={cn("size-3.5 transition-transform duration-150", isDropdownOpen && "rotate-180")}
      aria-hidden="true"
    />
  </button>
  {isDropdownOpen && (
    <div
      role="menu"
      className={cn(
        "absolute top-full left-0 mt-1 w-56 rounded-lg border border-border bg-popover shadow-lg",
        "py-1 z-20"
      )}
    >
      {subLinks.map((sub) => (
        <a
          key={sub.href}
          href={sub.href}
          role="menuitem"
          className="flex items-center gap-3 px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground transition-colors duration-150"
        >
          {sub.icon && <sub.icon className="size-4 text-muted-foreground shrink-0" aria-hidden="true" />}
          <span>{sub.label}</span>
        </a>
      ))}
    </div>
  )}
</li>
```

ARIA pattern: `role="menu"` on the container, `role="menuitem"` on each option. Keyboard: Arrow Down opens dropdown and moves to first item; Arrow Up/Down navigate items; Enter/Space activates; Escape closes and returns focus to trigger.

---

## Sidebar Navigation

For app-level navigation — dashboards, settings, admin interfaces.

```tsx
<aside
  aria-label="Sidebar navigation"
  className={cn(
    "flex flex-col w-64 shrink-0 border-r border-border bg-sidebar h-svh sticky top-0",
    "transition-all duration-300 ease-out",
    isCollapsed && "w-16"
  )}
>
  {/* Brand header */}
  <div className="flex h-16 items-center px-4 border-b border-border shrink-0">
    <a href="/" className="flex items-center gap-2 min-w-0">
      <Logo className="size-6 shrink-0" aria-hidden="true" />
      {!isCollapsed && <span className="font-semibold text-sm truncate">{siteName}</span>}
    </a>
  </div>

  {/* Navigation groups */}
  <nav className="flex-1 overflow-y-auto px-2 py-4 flex flex-col gap-6">
    {navGroups.map((group) => (
      <section key={group.label} aria-label={group.label}>
        {!isCollapsed && (
          <p className="px-2 mb-1 text-xs font-medium uppercase tracking-wider text-muted-foreground">
            {group.label}
          </p>
        )}
        <ul role="list" className="flex flex-col gap-0.5">
          {group.items.map((item) => (
            <li key={item.href}>
              <a
                href={item.href}
                aria-current={isActive(item.href) ? "page" : undefined}
                aria-label={isCollapsed ? item.label : undefined}
                className={cn(
                  "flex items-center gap-3 px-2 py-2 rounded-md text-sm transition-colors duration-150",
                  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
                  isActive(item.href)
                    ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                    : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
                )}
              >
                <item.icon className="size-4 shrink-0" aria-hidden="true" />
                {!isCollapsed && <span className="truncate">{item.label}</span>}
                {!isCollapsed && item.badge && (
                  <span className="ml-auto text-xs bg-primary text-primary-foreground rounded-full px-1.5 py-0.5">
                    {item.badge}
                  </span>
                )}
              </a>
            </li>
          ))}
        </ul>
      </section>
    ))}
  </nav>

  {/* Footer actions */}
  <div className="shrink-0 border-t border-border p-2">
    {/* user avatar + settings */}
  </div>
</aside>
```

When collapsed (`w-16`), show only icons. Use `aria-label` on icon-only links to preserve screen reader names.

---

## Breadcrumb

```tsx
<nav aria-label="Breadcrumb">
  <ol role="list" className="flex items-center gap-1.5 text-sm text-muted-foreground">
    {crumbs.map((crumb, i) => {
      const isLast = i === crumbs.length - 1
      return (
        <li key={crumb.href} className="flex items-center gap-1.5">
          {isLast ? (
            <span aria-current="page" className="font-medium text-foreground truncate max-w-40">
              {crumb.label}
            </span>
          ) : (
            <>
              <a href={crumb.href} className="hover:text-foreground transition-colors duration-150">
                {crumb.label}
              </a>
              <ChevronRight className="size-3.5 shrink-0" aria-hidden="true" />
            </>
          )}
        </li>
      )
    })}
  </ol>
</nav>
```

The current page is `<span aria-current="page">` — not a link, not an anchor. Never make the last breadcrumb a link to the current page.

---

## Tab Navigation

For within-page section switching (not routing):

```tsx
<div role="tablist" aria-label="Section tabs" className="flex gap-1 border-b border-border">
  {tabs.map((tab) => (
    <button
      key={tab.id}
      role="tab"
      aria-selected={activeTab === tab.id}
      aria-controls={`panel-${tab.id}`}
      id={`tab-${tab.id}`}
      onClick={() => setActiveTab(tab.id)}
      className={cn(
        "px-4 py-2.5 text-sm font-medium transition-colors duration-150 border-b-2 -mb-px",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
        activeTab === tab.id
          ? "border-primary text-foreground"
          : "border-transparent text-muted-foreground hover:text-foreground hover:border-border"
      )}
    >
      {tab.label}
    </button>
  ))}
</div>

{tabs.map((tab) => (
  <div
    key={tab.id}
    role="tabpanel"
    id={`panel-${tab.id}`}
    aria-labelledby={`tab-${tab.id}`}
    hidden={activeTab !== tab.id}
    className="py-4"
  >
    {tab.content}
  </div>
))}
```

Keyboard: Arrow Left/Right moves between tabs; Home/End jumps to first/last; Tab moves into the panel. Use `hidden` attribute (not `display:none` via class) so screen readers skip inactive panels.

---

## Active State Detection

```tsx
// Framework-agnostic helper
const isActive = (href: string) => {
  // Exact match
  if (href === "/") return pathname === "/"
  // Prefix match for nested routes
  return pathname.startsWith(href)
}
```

Always apply `aria-current="page"` to the active link — this is how screen readers identify the current page in navigation.

---

## Accessibility

- `<nav>` must have an accessible name via `aria-label`. Multiple `<nav>` elements on a page must have distinct labels ("Main navigation", "Footer navigation", "Breadcrumb").
- Active links: `aria-current="page"` — not just a visual style change
- Icon-only buttons (hamburger, collapse): `aria-label` describing the action
- Mobile menu: `aria-expanded` on the toggle, `aria-controls` pointing to the menu id
- Dropdown menus: `aria-haspopup="true"`, `aria-expanded` on trigger; `role="menu"` on container; `role="menuitem"` on items
- Skip navigation link: `<a href="#main-content" className="sr-only focus:not-sr-only">Skip to main content</a>` as the first focusable element in the page

---

## Common Pitfalls

- **`<div onClick>` as a link:** nav items must be `<a>` — screen readers, keyboard users, and right-click context menus all depend on it
- **No `aria-current` on active item:** visually obvious but invisible to screen readers
- **Mobile menu that doesn't close:** must close on link click, Escape, viewport resize to `md:`, and click-outside
- **Missing skip link:** keyboard users must be able to bypass the nav on every page load
- **Active detection too broad:** a prefix match for `"/"` marks every page as active on the home nav item. Always handle the root path as an exact match.
- **Sidebar overflow:** without `overflow-y-auto` on the nav section and `h-svh` on the sidebar, long nav lists overflow the viewport
