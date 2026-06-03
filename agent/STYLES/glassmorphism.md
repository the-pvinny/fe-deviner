# STYLE — Glassmorphism

Extends DESIGN.md. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Frosted glass surfaces floating over rich backgrounds. Depth, translucency, and light define the visual language. Surfaces feel physical — like layered panes of frosted glass with light passing through.

---

## Color

- Background: rich, deep, or gradient — this is the "scene" behind the glass. Dark backgrounds (`neutral-900`, `neutral-950`) or deep saturated tones work best.
- Surfaces: semi-transparent — `bg-background/60` to `bg-background/80` over the background
- Foreground text: `text-foreground` with high contrast against the frosted surface
- Accent color: visible through the glass as subtle glow or tint — use sparingly
- Borders: semi-transparent — `border border-white/10` or `border border-white/20` to catch the light
- Avoid opaque surfaces — every card, panel, and modal should have some transparency

---

## The Glass Effect

The core technique — a combination of background blur, transparency, and subtle border:

```
bg-white/10 backdrop-blur-xl border border-white/20 shadow-lg
```

**Variations by elevation:**

| Level | Blur | Opacity | Border | Shadow | Use for |
|---|---|---|---|---|---|
| Ground | `backdrop-blur-sm` | `bg-white/5` | `border-white/10` | `shadow-none` | Subtle overlays |
| Surface | `backdrop-blur-md` | `bg-white/10` | `border-white/15` | `shadow-sm` | Cards, panels |
| Elevated | `backdrop-blur-xl` | `bg-white/15` | `border-white/20` | `shadow-lg` | Modals, popovers |
| Floating | `backdrop-blur-2xl` | `bg-white/20` | `border-white/25` | `shadow-xl` | Primary surfaces |

**Dark mode variation:** Use `bg-black/20` instead of `bg-white/10` — the glass tints toward the background.

---

## Typography

- Clean sans-serif — glass surfaces need legible type
- Headings: `font-semibold` or `font-bold`, `text-foreground` — must cut through the translucency
- Body: `font-normal`, ensure sufficient contrast against the frosted background
- Avoid thin weights (`font-light`, `font-thin`) — they disappear against translucent surfaces
- Display text can use `text-white` on dark glass backgrounds — document the contrast ratio

---

## Space

- Comfortable padding inside glass surfaces: `p-6` to `p-8` — the frosted area needs room to breathe
- Gap between glass panels: `gap-4` to `gap-6` — background should be visible between panels
- Don't pack glass surfaces tightly — the gaps between them are where the background shows through, which is the point

---

## Layout

- Layered composition — background, mid-ground glass surfaces, foreground elements
- Cards float visually — use `rounded-xl` to `rounded-2xl` for soft, physical edges
- Centered or asymmetric layouts both work — the glass panels are the composition
- Background should be visible — don't cover it entirely with glass surfaces
- Consider a large background image, gradient, or animated mesh as the scene

---

## Depth and Shadow

- Shadows are essential — they create the illusion of floating glass
- Use colored or tinted shadows when the background is saturated: `shadow-blue-500/10`
- Layer shadows: combine `shadow-lg` with a subtle inner glow (`ring-1 ring-inset ring-white/10`)
- Borders catch light — the `border-white/20` is simulating light refraction on the glass edge
- Depth ordering matters: higher glass surfaces are more opaque and more blurred

---

## Motion Character — The Drift

Motion in glassmorphism is ambient, fluid, and continuous. The world behind the glass is alive — light shifts, shapes float, surfaces breathe. Interaction motion is smooth and physical, as if touching real glass.

**Entrance and reveal:**
- Glass surfaces fade in and float up simultaneously: `fade-in translate-y-6` with `duration-500 ease-out`
- Stagger glass panels with 100–150ms delays — they should feel like panes being placed, not appearing at once
- Blur can animate on entrance: start at `backdrop-blur-none` and transition to `backdrop-blur-xl` with `duration-700` — the glass "frosts" as it appears
- Scale subtly on entrance: from `scale-95` to `scale-100` with `duration-500` — the surface materializes

**Hover and interaction:**
- Hover: increase opacity slightly — `hover:bg-white/15` from `bg-white/10`
- Hover: subtle shadow increase — `hover:shadow-xl` from `shadow-lg`
- Hover: micro-lift — `hover:-translate-y-0.5` — the glass surface rises toward the user
- Active: slight scale reduction — `active:scale-[0.98]` to simulate pressing into the glass
- All interaction transitions: `duration-200 ease-out` — smooth, no snapping

**Ambient motion (the signature):**
- Background gradient shifts continuously: slow hue rotation or position drift over 8–15s cycles
- Floating shapes (blobs, orbs) behind the glass move on slow sine-wave paths — CSS `@keyframes` with `duration-[10s]`+ (exception: ambient cycles require long durations)
- Light effects: a subtle traveling highlight across glass borders simulating light refraction, via animated gradient position
- Glassmorphism without background motion feels static and dead — ambient motion is what makes the glass read as glass
- Respect `prefers-reduced-motion`: reduce to static gradient or single slow pulse

**Scroll behavior:**
- Glass surfaces can have subtle parallax relative to the background — different scroll speeds reinforce the layered depth
- Background elements shift at 0.3–0.5× scroll speed; glass surfaces at 1× (normal)
- Scroll-triggered reveals with the frost-in effect described above

**Timing and easing:**
- Interactions: `duration-200 ease-out` — responsive, physical
- Reveals: `duration-500 ease-out` — surfaces materialize
- Ambient: `duration-[8s]` to `duration-[15s]` with `ease-in-out` — slow, continuous, unnoticed until you look for it
- Spring easing is acceptable here — glassmorphism has a physical, organic character that benefits from slight overshoot on hover lifts

**Focus states:** glowing ring — `focus-visible:ring-2 focus-visible:ring-primary/50` — softer than solid rings, matches the translucent aesthetic.

**The rule:** the glass is a window into a living scene. If the background is static, the illusion breaks. Motion is what separates glassmorphism from "divs with blur."

---

## Backgrounds

The background is critical — glassmorphism only works with something interesting behind the glass.

**Options:**
- Gradient mesh: `bg-gradient-to-br from-violet-500/30 via-blue-500/20 to-emerald-500/30`
- Deep solid: `bg-neutral-950` with subtle noise texture
- Photography: blurred or desaturated background image
- Abstract: geometric shapes or blobs positioned behind the glass surfaces
- Animated: slow-moving gradient or floating shapes (respect `prefers-reduced-motion`)

---

## Performance

- `backdrop-blur` is GPU-intensive — limit the number of simultaneously blurred elements
- Avoid stacking multiple `backdrop-blur` elements on top of each other (compounding blur is expensive)
- Provide a fallback for browsers/devices with reduced capability: `@supports not (backdrop-filter: blur(1px))` with a solid background
- Test on mobile — backdrop-blur can cause frame drops on lower-end devices

---

## Common Pitfalls

- **Illegible text:** insufficient contrast between text and translucent surface. Fix by increasing surface opacity or adding a subtle text shadow
- **Boring background:** glass over a flat white or gray background looks like a mistake. Fix by adding a gradient, image, or color field
- **Over-frosted:** too many glass layers or too much blur creates visual mud. Fix by limiting to 2–3 glass surfaces per viewport
- **Flat glass:** glass without shadow and border doesn't read as glass. Fix by ensuring every glass surface has blur + transparency + border + shadow
- **No depth variation:** all surfaces at the same opacity and blur. Fix by using the elevation system above — ground, surface, elevated, floating
