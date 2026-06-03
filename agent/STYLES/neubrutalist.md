# STYLE — Neubrutalist

Extends DESIGN.md. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Neo-brutalism translates architectural brutalism's ideology — honesty of materials, structure visible in form — into a repeatable interface grammar. The rawness is **intentional and structured**, not accidental. The goal is to make an interface that says "I did not reach for a Tailwind template" by making every design decision a small act of defiance against the polished startup aesthetic.

Its most important principle: **performance as virtue**. Minimal assets, system fonts, no decorative resources that cost load time. Speed is an ethical statement about respecting user time, not just an optimisation target.

The mature pattern (2025–2026) is **hybridisation**: full neubrutalism on marketing surfaces, calmer conventional interaction models inside the product. Brutalist accents on one CTA button signal authenticity without alienating users who need the product to feel trustworthy.

---

## Where It Works / Where It Fails

**Works:**
- Creator tools, portfolio sites, developer SaaS landing pages
- Cultural and editorial sites: music, art, events, streetwear
- Products differentiating from the Tailwind/shadcn template sea
- Audiences who recognise and value the cultural reference (designers, developers)

**Fails:**
- Trust-sensitive contexts: banking, healthcare, legal, enterprise B2B — rawness reads as incompetence
- Data-heavy dashboards and utility applications — friction impedes in-task users
- E-commerce with a broad audience — hard borders signal low production quality outside creative demographics

---

## Color

The neubrutalist palette is **maximum contrast, flat, and intentional**:

- Background: `bg-background` (white in light mode) — the page surface is raw, unadorned
- Text: `text-foreground` (near-black) — maximum contrast
- Accent: **one bold flat color** as the single saturated element. Common: pure yellow, electric blue, hot pink, lime green. Applied to CTAs, active states, and key badges only.
- Borders: `border-foreground` — always opaque black/dark, no softness
- **No gradients** — color is applied as solid planes
- **No opacity washes** — colors are either fully on or fully off
- Surfaces alternate between white and the accent: a section background in the accent color with black text is a neubrutalist composition move

Dark mode: invert the contrast — dark background (`neutral-950`), white text, same bold accent. The hard shadows shift to `box-shadow: 4px 4px 0 oklch(var(--foreground))`.

---

## Typography

- **System fonts as a statement**: Arial, Helvetica, Courier New. Not loading a Google Font is itself part of the aesthetic — the font download is an unnecessary frivolity.
  - In Tailwind: `font-sans` (system sans-serif) or explicit `font-["Courier_New",_monospace]`
- **Weight contrast is extreme**: display text at `font-black` (900), body at `font-normal` or `font-medium`
- **Scale is aggressive**: headings at `text-5xl` to `text-8xl` in hero sections
- **All-caps labels** with `tracking-widest` for category markers, section headings, button text
- **Tight leading** on large display text: `leading-none` or `leading-tight`
- Text alignment: left-aligned by default; full-width centered headings as compositional statements
- Monospaced (`font-mono`) for metadata, prices, counts — the machine aesthetic

```tsx
// Neubrutalist display heading
<h1 className="font-black uppercase leading-none tracking-tight text-6xl md:text-8xl text-foreground">
  Build Different
</h1>

// Category label
<span className="font-bold uppercase tracking-widest text-xs text-foreground">
  Case Studies
</span>
```

---

## Borders and Shadows — The Signature

The defining visual property. All interactive elements carry a thick border and a hard, flat, no-blur shadow.

```tsx
// The neubrutalist shadow utility
// box-shadow: 4px 4px 0 [foreground color]
// Note: no blur radius, no spread, solid offset — this is the non-negotiable move

// In Tailwind, express as a custom class in your @layer utilities:
// .shadow-brutal { box-shadow: 4px 4px 0 hsl(var(--foreground)); }
// .shadow-brutal-sm { box-shadow: 2px 2px 0 hsl(var(--foreground)); }
// .shadow-brutal-lg { box-shadow: 6px 6px 0 hsl(var(--foreground)); }

// Or inline for accent-colored shadows:
// style={{ boxShadow: "4px 4px 0 hsl(var(--foreground))" }}
```

```tsx
// Neubrutalist card
<div className="border-2 border-foreground bg-card p-6"
     style={{ boxShadow: "4px 4px 0 hsl(var(--foreground))" }}>
  {/* content */}
</div>

// With accent background
<div className="border-2 border-foreground bg-warning p-6"
     style={{ boxShadow: "4px 4px 0 hsl(var(--foreground))" }}>
  {/* content */}
</div>
```

**Border radius:** `rounded-none` is the default philosophical position. Rounded corners = softness = the polished startup aesthetic = the thing being rejected. Some neubrutalist work uses `rounded-sm` or `rounded-md` as a concession to usability — this is the hybrid approach.

---

## The Canonical Button

The neubrutalist button interaction is a signature: on hover, the element "lifts" (moves up-left) as the shadow grows. On active/press, the element "presses down" into the shadow.

```tsx
interface BrutalButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "accent" | "ghost"
  children: React.ReactNode
  className?: string
}

const variantClasses = {
  primary: "bg-primary text-primary-foreground",
  accent:  "bg-warning text-warning-foreground",
  ghost:   "bg-background text-foreground",
}

export function BrutalButton({
  variant = "primary",
  children,
  className,
  ...props
}: BrutalButtonProps) {
  return (
    <button
      {...props}
      className={cn(
        "inline-flex items-center justify-center",
        "border-2 border-foreground px-5 py-2.5",
        "font-bold uppercase tracking-wide text-sm",
        "rounded-none",
        // No transition by default — interactions are immediate
        // Lift on hover, press on active
        "hover:-translate-x-0.5 hover:-translate-y-0.5",
        "active:translate-x-1 active:translate-y-1",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
        variantClasses[variant],
        className
      )}
      style={{ boxShadow: "4px 4px 0 hsl(var(--foreground))" }}
    >
      {children}
    </button>
  )
}

// The hover shadow change requires inline style update — use a hover state:
// hover:shadow = { boxShadow: "6px 6px 0 hsl(var(--foreground))" }
// active:shadow = { boxShadow: "none" }
// Implement via onMouseEnter/onMouseLeave or a CSS class with @apply
```

For the full lift-shadow interaction in CSS (add to `@layer utilities`):

```css
.btn-brutal {
  box-shadow: 4px 4px 0 hsl(var(--foreground));
  transition: transform 100ms ease-out, box-shadow 100ms ease-out;
}
.btn-brutal:hover {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 hsl(var(--foreground));
}
.btn-brutal:active {
  transform: translate(4px, 4px);
  box-shadow: none;
}
```

---

## Grid

- Exposed structure: grid lines are often **visible** as `border-r` or `border-b` separators — not decorative, structural
- Unequal column splits with visible borders between them: a 5-column content block next to a 7-column feature with a hard border between
- Elements that bleed to edges with no rounded corners — content runs to the container boundary
- Dense composition: padding is measured, not generous. `p-4` or `p-6`, not the lavish `p-12` of minimalism
- No invisible breathing room — neubrutalism does not fear density

---

## Space

- **Generous macro space between sections** to provide relief — section `py-16` or `py-24`
- **Tight micro space within components** — elements pack close together; borders do the separation work, not padding
- White space as a grid element: empty cells in a grid layout are intentional voids, not oversights

---

## Depth and Shadow

- **No `box-shadow` with blur** — all depth comes from the hard 4px/4px/0 offset shadow
- **No elevation system** — there are no layers, no floating surfaces, no ambient shadows
- The hard shadow is the only depth cue; the element either has it or doesn't
- Depth hierarchy: elements with `shadow-brutal-lg` appear more important than elements with `shadow-brutal-sm`

---

## Motion Character — Immediate and Honest

Motion in neubrutalism is **immediate, minimal, and honest about being mechanical**. Transitions are absent or near-instant. Interaction should feel like flipping a physical switch, not gliding through a polished UI.

**The neubrutalist motion principles:**
- No entrance animations for content — it is there or it isn't
- Hover interactions: instant color change, or the lift-and-shadow sequence (100ms max)
- No easing that suggests softness (`ease-out` is acceptable; `ease-in-out` is borderline; spring physics are wrong for this style)
- Page transitions: cut or instant crossfade — no sliding panels, no morphing
- Loading states: text-based ("Loading...") or a monospaced spinner — never a decorative skeleton

**Acceptable motion:**
```tsx
// Lift interaction — the one permitted animation
"transition-transform duration-100 ease-out hover:-translate-y-0.5 hover:-translate-x-0.5"
"active:translate-x-1 active:translate-y-1"

// Color swap — instant or 100ms
"transition-colors duration-100 hover:bg-foreground hover:text-background"
```

**Not acceptable:**
- Fade-in on scroll — content is there when it loads
- Spring physics or bounce — too soft
- Animated gradients, aurora effects — antithetical to the philosophy
- Skeleton screens with gradient animation — too polished

**Focus states:** high contrast, box-offset — `focus-visible:ring-2 focus-visible:ring-foreground focus-visible:ring-offset-2`. The focus ring should be indistinguishable from the component's own border vocabulary.

---

## Imagery

- Photography is used raw: no rounded corners, no border-radius, hard edges
- Black and white photography fits naturally — color photography sits inside color-block containers
- No decorative illustrations — everything is functional
- Icons: use sparingly, always `lucide-react`, always paired with a text label
- Figures and screenshots treated like editorial photography: full-bleed or hard-bordered, never softly shadowed

---

## Signature Patterns

**The hard-shadow card grid** — a 2 or 3-column grid of cards with `border-2 border-foreground shadow-brutal`, each card a composition in itself with an accent-colored label, bold heading, and text.

**The accent section** — a full-bleed section with the accent color as background (`bg-warning` or `bg-success`) and `text-foreground`. One solid plane of color with content on it. No gradient, no image.

**The exposed input** — form fields with `border-2 border-foreground rounded-none` and focus state `shadow-brutal`:
```tsx
<input
  className={cn(
    "w-full border-2 border-foreground bg-background px-3 py-2",
    "font-sans text-base text-foreground placeholder:text-muted-foreground",
    "rounded-none",
    "focus-visible:outline-none focus-visible:shadow-[4px_4px_0_hsl(var(--foreground))]"
  )}
/>
```

**The tag/badge** — flat, hard-bordered, uppercase, accent-colored:
```tsx
<span className="inline-block border border-foreground bg-warning px-2 py-0.5 font-bold uppercase tracking-wide text-xs text-foreground">
  New
</span>
```

**The stacked feature list** — items with a visible left border `border-l-4 border-foreground` acting as a bullet, tight padding, no background — the structure is the list.

---

## Common Pitfalls

- **Accidental brutalism** — using hard shadows or system fonts without commitment to the rest of the vocabulary produces something that looks broken, not intentional. Apply the full grammar or none of it.
- **Rounded corners + hard shadow** — mixing `rounded-xl` with a brutal shadow creates a contradiction that reads as a mistake. Choose one register.
- **Too many accent colors** — neubrutalism works with one accent, used systematically. Two accents competing create visual noise, not energy.
- **Brutalism on utility UI** — applying the full style to data tables, settings panels, or dashboards creates friction where users need clarity. Use brutalist accents on marketing surfaces only.
- **Forget the performance ethic** — if the page loads slowly because of a heavy font or large JS bundle, the style has been applied without its philosophy. System fonts and minimal assets are not optional decoration; they are the point.
- **Mistaking chaos for brutalism** — the style is structured and systematic. Random misalignment is not brutalism; it is a bug. Everything must be intentional.
