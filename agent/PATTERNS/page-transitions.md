# PATTERN — Page Transitions

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Route changes and view switches are moments of spatial navigation — the user is moving through the application. Page transitions make this movement legible, reduce perceived load time, and give the interface a sense of physical coherence.

---

## When to Use

- Multi-page SPAs with meaningful navigation between views
- Portfolios, case studies, or content-heavy sites where each page is a distinct context
- Applications with navigational depth (parent → child → detail)
- When content type changes significantly between routes (list → detail, index → article)

Do not use on: single-page utilities, dashboards with tab-based navigation, or any context where speed is the primary concern.

---

## Approach 1: View Transitions API (Native, Preferred)

The browser-native approach. Captures the current page state as a screenshot, navigates, then cross-fades between old and new states. Zero JS animation libraries.

```tsx
// Next.js App Router — wrap navigation calls
import { useRouter } from "next/navigation"

const useViewTransition = () => {
  const router = useRouter()

  const navigate = (href: string) => {
    if (!document.startViewTransition) {
      router.push(href)
      return
    }
    document.startViewTransition(() => {
      router.push(href)
    })
  }

  return navigate
}
```

```css
/* Default cross-fade — no additional CSS needed */

/* Custom: slide in from right */
@keyframes slide-in {
  from { translate: 100% 0; }
}
@keyframes slide-out {
  to { translate: -30% 0; }
}

::view-transition-old(root) {
  animation: 300ms ease-out both slide-out;
}

::view-transition-new(root) {
  animation: 300ms ease-out both slide-in;
}

@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) {
    animation: none;
  }
}
```

### Shared element transitions

Elements that exist on both pages can be named and will animate between their positions:

```css
/* On the list page: image thumbnail */
.article-thumbnail {
  view-transition-name: article-hero;
}

/* On the detail page: hero image */
.article-hero {
  view-transition-name: article-hero;
}
```

The browser automatically morphs the element between its two positions, sizes, and shapes. This is the most visually powerful feature of the View Transitions API.

**Constraint:** `view-transition-name` must be unique per page. Duplicate names break the transition.

---

## Approach 2: Framer Motion (React, Cross-Browser)

```tsx
import { AnimatePresence, motion } from "framer-motion"

// In the root layout — wrap page content
function Layout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.25, ease: "easeOut" }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

**`mode="wait"`** ensures the exit animation completes before the enter animation starts. This prevents overlapping content.

### Slide transitions (directional navigation)

```tsx
const variants = {
  enter: (direction: number) => ({
    x: direction > 0 ? "100%" : "-100%",
    opacity: 0,
  }),
  center: { x: 0, opacity: 1 },
  exit: (direction: number) => ({
    x: direction > 0 ? "-30%" : "30%",
    opacity: 0,
  }),
}

function PageTransition({ children, direction }: { children: React.ReactNode; direction: number }) {
  return (
    <motion.div
      custom={direction}
      variants={variants}
      initial="enter"
      animate="center"
      exit="exit"
      transition={{ duration: 0.35, ease: [0.32, 0, 0.67, 0] }}
    >
      {children}
    </motion.div>
  )
}
```

---

## Approach 3: CSS Classes (Lightweight, No Library)

For simpler transitions without Framer Motion:

```tsx
function Page({ children }: { children: React.ReactNode }) {
  const [visible, setVisible] = useState(false)
  useEffect(() => { setVisible(true) }, [])

  return (
    <div className={cn(
      "transition-all duration-300 ease-out",
      visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2"
    )}>
      {children}
    </div>
  )
}
```

This handles enter only. Exit requires unmounting the component before navigation, which requires coordination with the router.

---

## Transition Character by Style

Match the transition to the active STYLES/ file:

| Style | Enter | Exit | Duration | Easing |
|---|---|---|---|---|
| Minimalist | Fade only | Fade only | 250ms | `ease-out` |
| Editorial | Fade + translate up | Fade + translate up | 400ms | `ease-out` |
| Glassmorphism | Fade + scale from 0.98 | Fade + scale to 1.02 | 350ms | `ease-out` |
| Modernist | Slide from right (spatial) | Slide left | 300ms | `ease-in-out` |

---

## Loading State During Transition

Always provide feedback during route changes — especially for data-fetching routes:

```tsx
// Next.js loading.tsx — shown automatically during navigation
export default function Loading() {
  return (
    <div className="flex h-screen items-center justify-center">
      <div className="h-8 w-8 animate-spin rounded-full border-2 border-muted border-t-primary" />
    </div>
  )
}
```

For progress bars (NProgress-style):

```tsx
// Thin bar at top of viewport, animated width from 0 to 100% during navigation
<div
  className="fixed left-0 top-0 z-50 h-0.5 bg-primary transition-all duration-300"
  style={{ width: `${progress}%`, opacity: isNavigating ? 1 : 0 }}
/>
```

---

## Performance Constraints

- Exit + enter transitions combined should stay under 600ms total — users are waiting for new content
- Do not animate layout properties during transitions — use `transform` and `opacity` only
- View Transitions API is synchronous — keep navigation handlers fast to avoid perceptible freeze before transition starts
- Framer Motion `AnimatePresence` can cause layout shift if wrapper dimensions change between pages — use fixed-height containers or `layout` prop

---

## Accessibility

- Transitions must be disabled under `prefers-reduced-motion` — replace with instant navigation
- Page title must update immediately on navigation — don't delay the `<title>` update for the transition
- Focus must be managed on route change — move focus to the main content area after navigation completes
- Screen readers should announce the new page — ensure `<main>` or `aria-live` regions are updated

```tsx
// Focus management after navigation
useEffect(() => {
  const main = document.querySelector("main")
  if (main) main.focus()
}, [pathname])
```

---

## Common Pitfalls

- **Flash of unstyled content:** the new page renders before the transition — ensure initial state hides content (`opacity: 0`) before the animation begins
- **Scroll position not reset:** navigating to a new page but inheriting scroll position from the previous one. Call `window.scrollTo(0, 0)` on navigation.
- **View transition name collision:** two elements on the same page with the same `view-transition-name` break the API silently
- **Back button feels broken:** if only forward navigation has transitions, the back gesture feels inconsistent. Handle direction for both
- **Transition during rapid navigation:** user clicks twice quickly, causing transitions to collide. `mode="wait"` in AnimatePresence handles this — always use it

---

## Cross-Document Transitions (MPA — No JavaScript)

For multi-page applications (traditional server-rendered HTML, Astro, etc.) both the outgoing and incoming pages opt in with a single CSS rule. The browser handles the rest automatically on same-origin navigation — no `document.startViewTransition()` call required.

**Browser support (2026):** Chrome 126+, Edge 126+, Safari 18.2+. Firefox: not yet supported.

```css
/* Add to every page that should participate */
@view-transition {
  navigation: auto;
}
```

To scope transitions only to users who haven't requested reduced motion:

```css
@media (prefers-reduced-motion: no-preference) {
  @view-transition {
    navigation: auto;
  }
}
```

Placing the opt-in inside the `no-preference` media query means users who have enabled reduced motion never trigger the transition. This is the recommended pattern — simpler than JS feature-gating.

The default animation is a 250ms crossfade. Apply custom keyframes exactly as in the SPA approach:

```css
/* Cross-doc slide: same CSS as SPA, works for MPA too */
@keyframes slide-in-from-right  { from { transform: translateX(100%); opacity: 0; } }
@keyframes slide-out-to-left    { to   { transform: translateX(-30%); opacity: 0; } }

::view-transition-old(root) { animation: 300ms ease-out both slide-out-to-left; }
::view-transition-new(root) { animation: 300ms ease-out both slide-in-from-right; }
```

Named shared elements work identically across document boundaries — assign `view-transition-name` on the element in both the old and new document and the browser morphs between them.

---

## The Full Pseudo-Element Tree

The View Transitions API exposes the transition as a tree of CSS pseudo-elements. Understanding the full hierarchy is required to target specific layers or named elements precisely.

```
::view-transition
  └── ::view-transition-group(root)
        └── ::view-transition-image-pair(root)
              ├── ::view-transition-old(root)    ← outgoing snapshot
              └── ::view-transition-new(root)    ← incoming live content
```

For each **named element** (via `view-transition-name`), a parallel sub-tree is created:

```
::view-transition
  ├── ::view-transition-group(root)           ← whole page
  │     └── ::view-transition-image-pair(root)
  │           ├── ::view-transition-old(root)
  │           └── ::view-transition-new(root)
  └── ::view-transition-group(product-hero)   ← named shared element
        └── ::view-transition-image-pair(product-hero)
              ├── ::view-transition-old(product-hero)
              └── ::view-transition-new(product-hero)
```

### Targeting each layer

```css
/* The root overlay — covers the entire viewport during the transition */
::view-transition {
  /* Rarely targeted directly; useful for adding a backdrop overlay */
  background: transparent;
}

/* The group wraps old + new and handles position/size interpolation for named elements */
::view-transition-group(product-hero) {
  /* Controls the container that animates from thumbnail position to hero position */
  animation-duration: 400ms;
  animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* The image pair is the crossfade container — isolates old/new blending */
::view-transition-image-pair(root) {
  /* mix-blend-mode: normal is default; change to overlay for creative effects */
}

/* The outgoing snapshot — this is the "old" page rendered as an image */
::view-transition-old(root) {
  animation: 300ms ease-in both fade-and-scale-out;
}

/* The incoming live DOM — this is the "new" page */
::view-transition-new(root) {
  animation: 300ms ease-out both fade-and-scale-in;
}

/* Target a specific named element's old/new states independently */
::view-transition-old(product-hero) {
  /* Outgoing thumbnail */
  transform-origin: top left;
}
::view-transition-new(product-hero) {
  /* Incoming hero image */
  transform-origin: top left;
}
```

---

## Directional Back/Forward Transitions

Forward navigation should slide content in from the right; back navigation should reverse the direction. Use the Navigation API to detect direction, toggle a class on the document root, then write CSS for both directions.

### SPA (Navigation API + `startViewTransition`)

```tsx
function useDirectionalViewTransition() {
  const router = useRouter()
  const pathname = usePathname()

  const navigate = (href: string, direction: "forward" | "back" = "forward") => {
    if (!document.startViewTransition) {
      router.push(href)
      return
    }

    // Set direction class before the transition fires
    document.documentElement.dataset.navDirection = direction

    const transition = document.startViewTransition(() => {
      router.push(href)
    })

    // Clean up direction class after transition completes
    transition.finished.finally(() => {
      delete document.documentElement.dataset.navDirection
    })
  }

  return navigate
}
```

```css
/* Default: forward — slide right in, slide left out */
@keyframes slide-in-right  { from { transform: translateX(100%); opacity: 0; } }
@keyframes slide-out-left  { to   { transform: translateX(-30%); opacity: 0; } }
@keyframes slide-in-left   { from { transform: translateX(-100%); opacity: 0; } }
@keyframes slide-out-right { to   { transform: translateX(30%);  opacity: 0; } }

/* Forward navigation */
[data-nav-direction="forward"]::view-transition-new(root) {
  animation: 300ms ease-out both slide-in-right;
}
[data-nav-direction="forward"]::view-transition-old(root) {
  animation: 300ms ease-in  both slide-out-left;
}

/* Back navigation */
[data-nav-direction="back"]::view-transition-new(root) {
  animation: 300ms ease-out both slide-in-left;
}
[data-nav-direction="back"]::view-transition-old(root) {
  animation: 300ms ease-in  both slide-out-right;
}

@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) {
    animation: none;
  }
}
```

### MPA (cross-document, Navigation API)

For multi-page apps, use the Navigation API to intercept navigation events and set the direction class before the browser-handled transition fires:

```js
// In a shared script included on every page
navigation.addEventListener("navigate", (e) => {
  if (!e.canIntercept || e.hashChange || e.downloadRequest) return

  const isBack = e.navigationType === "traverse" &&
    navigation.currentEntry.index > e.destination.index

  e.intercept({
    handler() {
      document.documentElement.dataset.navDirection = isBack ? "back" : "forward"
    }
  })
})
```

The CSS rules above (`[data-nav-direction="..."]::view-transition-*`) work identically for cross-document transitions.

---

## Framework Integration

| Framework | View Transitions integration |
|---|---|
| **Next.js App Router** | `<Link unstable_viewTransition>` prop (experimental, 14+). Wraps navigation in `document.startViewTransition` automatically. |
| **React Router v7** | `<Link viewTransition>` and `useViewTransitionState()` hook. Adds `transitioning` class to matched routes for CSS targeting. |
| **Astro** | `<ViewTransitions />` component in `<head>` — wraps cross-doc transitions with JS fallback for older browsers; handles scroll restoration automatically. Most production-ready out of the box. |
| **SvelteKit** | `onNavigate` lifecycle hook: `onNavigate((nav) => { if (!document.startViewTransition) return; return new Promise(resolve => { document.startViewTransition(() => { nav.complete.then(resolve); }); }); })` |
| **Nuxt** | `useViewTransition()` composable (v3.10+). Set `viewTransition: true` in `nuxt.config.ts` to enable globally. |

### Astro example

```astro
---
// src/layouts/Layout.astro
---
<html>
  <head>
    <ViewTransitions />
  </head>
  <body>
    <slot />
  </body>
</html>
```

Named shared elements work out of the box — assign `transition:name` directive:

```astro
<!-- List page: thumbnail -->
<img src={post.thumbnail} transition:name={`post-${post.id}-hero`} />

<!-- Detail page: hero image -->
<img src={post.hero} transition:name={`post-${post.id}-hero`} />
```

### Next.js App Router example

```tsx
import Link from "next/link"

// unstable_viewTransition wraps the push() in document.startViewTransition
function ArticleCard({ article }: { article: Article }) {
  return (
    <Link href={`/articles/${article.slug}`} unstable_viewTransition>
      <img
        src={article.thumbnail}
        alt={article.title}
        style={{ viewTransitionName: `article-${article.id}` }}
      />
      <h2>{article.title}</h2>
    </Link>
  )
}
```

**Note:** The `unstable_` prefix indicates this API may change before stabilisation. Pin your Next.js version when using it in production.
