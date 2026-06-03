# STYLE — Modernist

Extends DESIGN.md. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Form follows function. Clean geometry, systematic structure, and deliberate visual order. Inspired by Swiss/International Style and Bauhaus — the grid is the design, typography is the hierarchy, and ornamentation is eliminated unless it serves communication.

---

## Color

- Restrained: a primary neutral palette with one or two accent colors
- Background: `background` — clean white or near-white in light mode
- Text: high-contrast `foreground` — `neutral-900` or `neutral-950`
- Accent: a single saturated hue used systematically — navigation markers, active states, key CTAs. Not decorative, functional.
- Color blocks: solid, flat fills — `bg-primary`, `bg-accent` — used as compositional rectangles, not gradients
- No gradients, no glow effects, no color transitions. Color is applied as solid planes.

---

## Typography

- **Sans-serif only** — grotesque or geometric families. No serifs, no scripts, no display fonts.
- Hierarchy is extreme and systematic:
  - Headlines: `text-5xl` to `text-8xl`, `font-bold` or `font-black`, `tracking-tight`
  - Subheadings: `text-lg` to `text-xl`, `font-medium`, `tracking-normal`
  - Body: `text-base`, `font-normal`, `leading-relaxed`
  - Labels: `text-xs`, `uppercase`, `tracking-widest`, `font-medium`
- **Scale contrast is the primary hierarchy tool** — the jump between heading and body should be dramatic
- Uppercase labels and navigation items with wide tracking: `uppercase tracking-widest text-xs font-medium`
- Text alignment: left-aligned. Centered text is rare — used only for hero headings or single-line labels.
- Line length controlled: `max-w-prose` for body, wider for headings

---

## Grid

- **The grid is sacred.** Every element aligns. Every margin is intentional.
- 12-column grid at `lg:`, 4-column at `sm:`, full-width stack at mobile
- Consistent gutters: `gap-4` to `gap-8`
- Elements snap to grid edges — no floating, no approximation
- Grid lines are implied through alignment, not drawn — avoid visible grid borders
- Column-spanning elements create deliberate asymmetry within the grid: a 7-column image next to a 5-column text block

---

## Space

- Systematic and proportional — spacing follows a clear mathematical rhythm
- Section spacing: large and consistent — `py-16`, `py-24`, or `py-32`
- Internal padding: moderate — `p-6` to `p-8`
- Whitespace is generous but structured — it follows grid proportions, not arbitrary amounts
- Avoid decorative spacing (extra-large gaps for atmosphere) — space serves structure

---

## Layout

- Asymmetric grid compositions: unequal column splits (7/5, 8/4, 3/9) create visual interest within strict alignment
- Modular: repeating grid cells with consistent sizing — card grids, image grids, content blocks
- Full-bleed color blocks: sections with solid background color changes, edge-to-edge
- Content pinned to top-left of containers — avoid centering unless the element is a singular focal point
- Navigation: horizontal, evenly spaced, minimal — a systematic list, not a decorative element

---

## Depth and Shadow

- **Flat.** No shadows, no elevation, no 3D effects.
- Separation through space, color blocks, and rules — not through simulated depth
- Borders: precise and functional — `border-b` or `border-l` as dividers, never decorative
- If depth is absolutely necessary, limit to `shadow-xs` — a whisper, not a statement

---

## Motion Character — The Machine

Motion in modernism is precise, geometric, and mechanical. Elements don't float or fade — they slide into position along grid axes, clip-reveal from edges, and transition between states with engineering precision. Motion serves the grid.

**Entrance and reveal:**
- Elements slide into their grid position — `translate-x` or `translate-y` from the nearest grid edge with `duration-300 ease-out`
- Clip-path reveals: content revealed by a geometric wipe — horizontal or vertical `clip-path` animation that "draws" the element on screen
- Stagger is systematic: uniform 50–75ms delays, not organic variation. Elements arrive in grid order (top-left to bottom-right, or column-by-column)
- Opacity is secondary — elements can arrive at full opacity via position or clip, which feels more mechanical than fading
- Text blocks: can reveal line-by-line or word-by-word for display headings, with tight 30–50ms stagger

**Hover and interaction:**
- Color state change is primary — `hover:bg-primary hover:text-primary-foreground` or `hover:text-primary`
- Background fill animations: color wipes in from one edge (`after:` pseudo-element with `transition-transform duration-300`) rather than instant color swap
- Underlines for links: slide in from left on hover (`after:scale-x-0 hover:after:scale-x-100 after:origin-left after:transition-transform after:duration-300`)
- No scale changes, no lifts, no shadows on hover — interaction stays in the plane

**Ambient motion:**
- Permitted when geometric and systematic — a grid of elements with a subtle sequenced pulse, a counter incrementing, a progress indicator advancing
- Rotating or translating geometric shapes (circles, lines) at constant speed: `ease-linear` is correct here — mechanical motion should feel like clockwork
- No organic motion, no sine waves, no float — if it looks biological, it doesn't belong
- Cycle duration: 3–6s for systematic pulses, constant for rotations

**Scroll behavior:**
- No parallax — everything moves at scroll speed, locked to the grid
- Scroll-triggered reveals use the slide/clip patterns above, fired by intersection observer
- Section transitions can use color-block wipes — the incoming section's background color slides over the previous section
- Sticky elements: snap into position with `duration-150`, no easing — mechanical stop

**Timing and easing:**
- Interactions: `duration-150 ease-out` — quick, decisive
- Reveals: `duration-300 ease-out` — elements arrive with purpose
- Clip/wipe reveals: `duration-500 ease-in-out` — the geometric reveal needs enough time to be perceived as a shape
- No spring, no bounce, no overshoot — motion terminates exactly at its target
- `ease-linear` permitted for ambient rotations and continuous motion — the one style where linear easing feels intentional

**Focus states:** sharp, geometric — `focus-visible:ring-2 focus-visible:ring-foreground focus-visible:ring-offset-2`

**The rule:** motion should feel engineered, not animated. If it could be described as "playful" or "organic," it's wrong for this style.

---

## Imagery

- Photography: if used, contained within grid cells — never free-floating or breaking alignment
- Black and white photography fits naturally
- Geometric shapes and diagrams as visual elements — circles, rectangles, lines
- No illustrations, icons only when functional (navigation, status indicators)
- Image sizing: precise — fills its grid cell exactly, no rounded corners (`rounded-none`)

---

## Signature Patterns

- **The oversized numeral:** section numbers displayed at `text-7xl`+ as a grid element alongside content
- **The color block section:** alternating full-width sections with solid background swaps (`bg-primary text-primary-foreground` → `bg-background text-foreground`)
- **The systematic list:** items arranged in grid cells, each with identical structure — label, heading, description, aligned to the same grid
- **The ruled header:** a horizontal rule above or below headings as a structural marker
- **The monospaced detail:** metadata or secondary information in a monospace face at small size

---

## Common Pitfalls

- **Corporate template:** modernist principles without personality. Fix by using dramatic scale contrast, asymmetric grid splits, and one strong accent color
- **Too rigid:** mechanical repetition without variation. Fix by varying grid proportions across sections while maintaining alignment
- **Sterile:** clean to the point of being cold. Fix by introducing one textural element — a photographic image, a color accent, or an oversized typographic detail
- **Mistaking minimalism for modernism:** minimalism reduces elements; modernism structures them. A modernist layout can be dense — a systematic grid of 20 cards is modernist if aligned and consistent
