# STYLE — Minimalist

Extends DESIGN.md. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Reduction to essence. Every element must justify its existence. If removing something doesn't hurt the design, remove it. The goal is not emptiness — it is clarity through restraint.

---

## Color

- Monochromatic or near-monochromatic — `background`, `foreground`, `muted`, `border` carry the design
- Accent color appears once per viewport, maximum — a single `primary` button, a single `accent` highlight
- Avoid gradients, multi-color schemes, and decorative color usage
- Dark mode: invert lightness, preserve the same restraint — don't add color in dark mode that wasn't in light

---

## Typography

- One typeface family — do not mix serif and sans-serif
- Hierarchy through weight and size only — `font-normal` for body, `font-semibold` or `font-bold` for headings, nothing heavier
- Large display text uses tight tracking: `tracking-tight` at `text-4xl`+
- Body text is comfortable: `text-base leading-relaxed`, `max-w-prose`
- Avoid uppercase — if used, restrict to a single label or navigation element with `tracking-wider text-xs`
- Let whitespace create separation; avoid horizontal rules and dividers

---

## Space

- Generous, deliberate — this is the primary compositional tool
- Macro space (between sections) is dramatically large: `py-20` to `py-32`
- Micro space (within components) is tight but breathable: `p-4` to `p-6` for cards, `gap-2` to `gap-4` for internal rhythm
- Asymmetric padding is acceptable: `pt-24 pb-16` creates visual movement without decoration
- Avoid dense grids — prefer single-column or two-column layouts with generous gutters

---

## Layout

- Single column dominant — center-aligned content blocks on a narrow container (`max-w-2xl` or `max-w-3xl`)
- Grid used sparingly — 2 columns max for feature sections, with wide gaps (`gap-8` to `gap-12`)
- Full-bleed elements are rare — when used, they create maximum impact because the default is contained
- Vertical rhythm is paramount — consistent section spacing creates a meditation-like scroll experience
- Avoid sidebars, multi-panel layouts, or dashboard density

---

## Depth and Shadow

- Flat or near-flat — `shadow-none` or `shadow-xs` at most
- Borders are the primary separation method — `border` in `border-color` (muted, low-contrast)
- Avoid card stacking, overlapping elements, or z-index layering
- If elevation is needed, use a single level: background → one surface → done

---

## Motion Character — The Whisper

Motion in minimalism is quiet, slow, and deliberate. It draws attention through patience, not spectacle. Every animation earns its presence the same way every element does — by being essential.

**Entrance and reveal:**
- Content fades in on scroll — `motion-safe:animate-in fade-in` with `duration-700` or longer
- Staggered reveals for grouped elements (cards, list items) with 75–100ms delays between siblings
- Translate distance is small — `translate-y-2` to `translate-y-4` at most. Movement is a suggestion, not a gesture.
- Elements arrive from below, never from the sides — vertical only, matching the scroll direction

**Hover and interaction:**
- Hover states: subtle opacity or background shift — `hover:bg-muted` or `hover:opacity-80`
- Transitions: `duration-200 ease-out` — quick but not instant, the user should feel the shift
- Buttons: ghost or outline variants preferred — solid `primary` buttons are rare focal points
- Links and interactive text: underline reveals on hover via `transition-all duration-200`

**Ambient motion:**
- Permitted when extremely subtle — a slow pulse on a single accent element, a gentle opacity oscillation on a decorative dot
- Cycle duration: 4s+ — anything faster feels anxious in a minimalist context
- Limit to one ambient animation per viewport

**Scroll behavior:**
- Smooth scroll between sections (`scroll-smooth` on `<html>`)
- Parallax is forbidden — it contradicts the flatness principle
- Sticky headers fade in/out with `duration-300`, not slide

**Timing and easing:**
- Default: `duration-200 ease-out` for interactions, `duration-700 ease-out` for reveals
- Never use `ease-linear` — minimalist motion should decelerate naturally
- Never use spring/bounce — organic physics contradicts the restrained character

**Focus states:** visible but simple — `focus-visible:ring-2 focus-visible:ring-ring`

**The rule:** if the motion draws attention to itself, it's too much. Minimalist animation should be noticed only in its absence.

---

## Imagery

- Photography: high-contrast black and white, or muted desaturated color
- No decorative illustrations, patterns, or textures
- Icons: outline style, consistent stroke weight, used functionally (not decoratively)
- If an image appears, it should be large and intentional — no thumbnail grids

---

## Common Pitfalls

- **Sterile:** minimalism without personality. Fix by choosing one distinctive element — an unusual typeface, a specific color accent, asymmetric spacing
- **Bare:** insufficient visual hierarchy. Fix by increasing scale contrast between heading and body sizes
- **Monotonous:** everything at the same visual weight. Fix by varying section density — a full-bleed image between text sections, or an oversized pull quote
- **Pretentious:** excessive whitespace with insufficient content. Fix by ensuring the space serves readability, not just aesthetics
