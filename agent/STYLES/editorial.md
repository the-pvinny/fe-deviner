# STYLE — Editorial

Extends DESIGN.md. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Magazine-inspired design where typography and composition tell the story. The layout itself is content — column breaks, pull quotes, oversized drop caps, and dramatic type hierarchies create a reading experience, not just a display surface.

---

## Color

- Restrained palette with one editorial accent — a deep red, a dusty rose, an ochre, or a rich blue used as a signature color
- Background: `background` for the page, `card` for article surfaces — keep them quiet
- Body text in `foreground` — high contrast, optimized for long reading
- Accent color used typographically: colored drop caps, highlighted pull quotes, section markers
- Avoid saturated UI chrome — the content is the interface

---

## Typography

- **Serif + sans-serif pairing is expected** — this is the one style where mixing typeface categories is natural
- Headings: serif, dramatic scale (`text-4xl` to `text-7xl`), tight tracking (`tracking-tight`)
- Body: sans-serif or serif, `text-base` to `text-lg`, `leading-relaxed` to `leading-loose`
- Subheadings: sans-serif, `font-medium`, `text-sm uppercase tracking-widest` — the classic magazine kicker
- Pull quotes: oversized (`text-2xl` to `text-3xl`), italic or light weight, generous margin
- Drop caps: first letter of an article styled dramatically — oversized, floated, or colored
- Bylines and metadata: `text-xs` or `text-sm`, `text-muted-foreground`, `uppercase tracking-wider`
- **Measure is sacred:** body text never exceeds `max-w-prose`. Reading comfort is the priority.

---

## Space

- Generous vertical rhythm between sections: `py-16` to `py-24`
- Tight micro space within text blocks — comfortable `leading-relaxed` but not excessive
- Asymmetric margins: text blocks offset from center, creating a column structure with active negative space on one side
- Horizontal rules (`<hr>`) and ornamental dividers between sections are valid editorial devices

---

## Layout

- **Multi-column text layouts** — `columns-2` at `lg:` breakpoint for long-form articles
- Content width varies: narrow text columns (`max-w-xl`) punctuated by full-width images or pull quotes
- **Grid-breaking is expected:** an image that bleeds into the margin, a heading that spans columns, a sidebar that overlaps the main column
- Feature images: full-bleed or oversized, with caption as a design element (`text-xs italic text-muted-foreground`)
- Sidebar elements: marginalia, related links, or pull quotes positioned outside the main text flow at `lg:` breakpoints
- Sticky elements: table of contents or section markers that track scroll position

---

## Depth and Shadow

- Minimal depth — editorial design is flat by tradition
- Separation through space, rules, and typographic contrast, not shadows or borders
- If cards are used, they are simple: `border-b` or no border, never `shadow-lg`
- Layering happens through composition (overlapping text on image) not through z-index stacking

---

## Motion Character — The Page Turn

Motion in editorial design serves pacing. It controls the reading tempo — slowing the eye where content is important, sequencing reveals like chapters. The user should feel like they're moving through a curated experience, not scrolling a feed.

**Entrance and reveal:**
- Scroll-driven reveals are the primary animation tool — content appears as the reader reaches it (`motion-safe:`)
- Headlines arrive first, then body text, then supporting elements — stagger mirrors reading order with 100–150ms delays
- Fade + slight translate: `fade-in translate-y-3` with `duration-500 ease-out`
- Pull quotes and feature images can use longer reveals: `duration-700` to `duration-1000` — they are pacing beats, meant to slow the reader
- Section transitions: horizontal rules or markers can draw in (scale from 0 to full width) as scroll markers

**Hover and interaction:**
- Images: zoom on hover (`hover:scale-105 transition-transform duration-500 ease-out`) with overflow hidden on container — the classic editorial image reveal
- Caption reveals: fade in on image hover with `duration-300`
- Navigation links: underline slides in from left (`after:transition-transform after:duration-300`) or color shifts
- Footnotes and annotations: tooltip or margin note appears on hover/click with `duration-200 ease-out`

**Ambient motion:**
- Subtle and content-adjacent — a blinking cursor on a byline, a slow fade cycle on a "new" tag
- Decorative lines or dividers can animate their drawing on scroll (CSS `stroke-dashoffset` or `scale-x`)
- No background animation — the content is the scene, not a backdrop

**Scroll behavior:**
- Smooth scroll for anchor navigation (`scroll-smooth`)
- Sticky table of contents with active-section highlighting that transitions with `duration-200`
- Progress bar at top of page (reading progress) — thin, accent-colored, animated width with `duration-100 ease-linear`
- Parallax: permitted sparingly on feature images only — slow factor (0.2–0.3), never on text

**Timing and easing:**
- Default: `duration-300 ease-out` for interactions, `duration-500 ease-out` for reveals
- Feature elements: `duration-700` to `duration-1000` — dramatic pacing beats
- Easing is always decelerating (`ease-out`) — content settles into place like a page laid flat

**Navigation:** minimal, often hidden or condensed — a sticky header with just the publication name and a menu toggle. Menu open/close: `duration-300 ease-in-out`.

**The rule:** motion should feel like turning pages in a well-designed magazine — deliberate pacing, not decoration.

---

## Imagery

- Photography is central — large, high-quality, often with art-directed crops
- Images break the text rhythm intentionally — full-bleed between narrow text columns
- Caption treatment is a design element, not an afterthought
- Illustrations: editorial illustration style if used — not corporate or clip-art
- Consider `aspect-[3/4]` or `aspect-[4/5]` for portrait editorial photography

---

## Signature Patterns

- **The kicker:** a small, uppercase, tracked-out label above the main headline
- **The deck:** a subtitle below the headline in lighter weight, bridging headline and body
- **The pull quote:** extracted and enlarged mid-article, often with a decorative bar or accent color
- **The byline block:** author, date, and read-time clustered as metadata
- **The section marker:** numbered or labeled section transitions within long-form content

---

## Common Pitfalls

- **Blog template:** generic single-column with centered text. Fix by introducing asymmetry, column variation, and typographic drama
- **Over-designed:** so many typographic treatments that hierarchy collapses. Fix by limiting to 4–5 distinct type treatments max
- **Stock photo feel:** generic imagery with no editorial relationship to content. Fix by using images that respond to the text, not decorate it
- **Ignoring mobile:** multi-column editorial layouts must collapse gracefully — single column with maintained type hierarchy at `sm:` breakpoints
