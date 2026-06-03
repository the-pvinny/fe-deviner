# DESIGN — Design Literacy & Fundamentals

This file teaches design thinking that applies across all styles. It is not about a specific aesthetic — it is about the principles that make any aesthetic work. CONFIG.md constrains your palette; METHOD.md constrains your structure; this file shapes your judgment.

---

## Visual Hierarchy

Every screen has a story. Hierarchy is how you tell the reader where to start, what matters, and what to ignore.

**Establishing dominance:** One element leads. It is larger, bolder, higher-contrast, or more spatially isolated than everything else. If two elements compete for dominance, the hierarchy is broken.

**Methods of contrast (in order of strength):**
1. Scale — size difference is the loudest signal
2. Weight — bold against light
3. Color — saturated against neutral, or light against dark
4. Space — isolation draws the eye
5. Position — top-left (LTR) gets seen first; center gets seen on scroll-stop
6. Motion — movement pulls focus (use sparingly — it's a cheat code with side effects)

**The squint test:** Blur the screen or step back. If the hierarchy still reads — dominant element first, supporting content second, tertiary last — the design works. If everything looks the same, it doesn't.

---

## Grid — Making and Breaking

A grid is not a prison. It is a baseline of trust — the user's eye learns the rhythm, and then you can play with it.

**Making the grid:**
- Establish consistent column structure (12-column for flexibility, 4-column for simplicity)
- Align elements to grid lines — text baselines, image edges, card boundaries
- Maintain consistent gutters (gap between columns)
- The grid should be felt, not seen

**Breaking the grid:**
- Only break a grid that has been established — random placement without a grid is not "creative," it is noise
- Break with intention: an oversized image bleeds past the column, a pull quote extends into the margin, a hero ignores columns entirely
- The break must serve hierarchy — it makes the breaking element more important
- Document the intent in a comment: `{/* breaks grid to create visual emphasis */}`
- Limit breaks to 1–2 per viewport — too many breaks and the grid ceases to exist

---

## Negative Space

Space is not emptiness. It is a design element with weight and purpose.

**Macro space:** The breathing room between major sections. Generous macro space communicates confidence and clarity. Cramped macro space communicates anxiety or low quality.

**Micro space:** The gaps between related elements — padding within cards, margin between label and input, line height in body text. Tight micro space groups elements together; loose micro space separates them.

**Active negative space:** Intentionally shaped to create visual tension or balance. The space around a centered heading on an otherwise empty hero is active — it is doing work.

**Passive negative space:** The natural consequence of layout — margins, padding, gutters. It should be consistent and rhythmic.

**Principle:** When in doubt, add more space. Crowding is almost always worse than excess breathing room. Novice designs are too tight; mature designs breathe.

---

## Typography as Design Element

Text is not just content to be read. At display sizes, text is a visual element to be *seen*.

**Functional typography (to be read):**
- Body text: optimize for readability — `text-base`, `leading-relaxed`, comfortable measure (45–75 characters per line)
- Use weight and size hierarchy to create scannable structure
- Left-align body text (centered body text is harder to read)
- Sufficient contrast against background

**Expressive typography (to be seen):**
- Display text can be oversized, tightly tracked, dramatically weighted
- At large sizes (`text-5xl`+), tighten tracking (`tracking-tight` or `tracking-tighter`) — large text looks loose at default spacing
- Use weight contrast between heading and body — `font-bold` heading over `font-normal` body, or `font-light` heading over `font-normal` body
- Consider type as compositional element — a large word can anchor a layout as strongly as an image
- Mixed case, all-caps (`uppercase tracking-wider`), or small-caps are stylistic choices with semantic weight — uppercase shouts, lowercase whispers

**The measure rule:** Lines of text wider than 75 characters become hard to track. Use `max-w-prose` (65ch) for body text or constrain with `max-w-xl`/`max-w-2xl`.

---

## Color Relationships

Individual colors don't matter. Relationships between colors matter.

**Contrast creates hierarchy:** High contrast between text and background makes it readable. Low contrast makes it recede. Use contrast deliberately — not everything should scream.

**Temperature creates mood:** Warm tones (amber, red-orange) advance and feel energetic. Cool tones (blue, violet) recede and feel calm. Neutral tones (gray) are structural — they don't compete.

**Saturation creates focus:** A single saturated element on a desaturated page is a focal point. Saturation everywhere is visual noise.

**The 60-30-10 guideline:**
- 60% dominant color (usually background/neutral)
- 30% secondary color (supporting surfaces, secondary text)
- 10% accent color (CTAs, highlights, interactive elements)

This is a guideline, not a rule. Maximalist styles break it intentionally. But if you break it, know you're breaking it.

**Dark mode is not an inversion.** It is a re-composition. Shadows work differently (subtle or absent), elevation uses lighter surfaces instead of shadows, and saturated colors need to be adjusted for dark backgrounds.

---

## Rhythm and Repetition

Rhythm is the consistent recurrence of a visual pattern. It creates predictability and comfort.

**Spatial rhythm:** Consistent spacing creates a beat. If cards are spaced `gap-6`, all cards should be `gap-6`. If section padding is `py-16`, all sections use `py-16` (or a harmonic multiple like `py-24`, `py-32`).

**Typographic rhythm:** A consistent type scale creates hierarchy that the reader internalizes. If `text-3xl font-bold` means "section heading," use it consistently — don't switch to `text-2xl font-extrabold` for another heading at the same level.

**Breaking rhythm:** Intentional rhythm breaks create emphasis. A card that is 2× the size of its siblings stands out because the rhythm set the expectation. Without established rhythm, there is nothing to break.

---

## Alignment and Proximity

**Alignment creates invisible lines** that the eye follows. Elements aligned to the same edge or baseline feel related, even without explicit grouping.

**Proximity creates grouping.** Elements close together are perceived as related. Elements far apart are perceived as separate. This is Gestalt — use space to group, not borders and boxes.

**The alignment audit:** Draw vertical and horizontal lines through your layout. Every element should sit on a shared line. Stray elements that don't align to anything feel accidental — they undermine trust in the design.

---

## Minimalism and Maximalism

These are compositional philosophies, not value judgments. Neither is inherently better.

**Minimalism:**
- Reduce to essential elements — every element must earn its place
- Space is the primary compositional tool
- Hierarchy through scale and weight, not color or decoration
- Risk: sterility, lack of personality, looking like every other minimal design

**Maximalism:**
- Layer, overlap, saturate — fill the frame with intentional visual density
- Texture, pattern, and decoration are valid design elements
- Hierarchy through contrast and isolation within density
- Risk: visual chaos, unclear hierarchy, inaccessibility

**The key:** Both require intention. Minimal is not "I removed things." Maximal is not "I added things." Both are deliberate compositional choices about what to emphasize and how.

---

## Rule-Breaking with Intent

Design rules exist because they solve common problems. Breaking them is valid when you have a reason.

**How to break a rule well:**
1. Know the rule and why it exists
2. Have a specific reason why breaking it serves this design
3. Break it confidently — half-broken rules look like mistakes
4. Document the intent in a comment when the break is non-obvious

**Common intentional breaks:**
- Overlapping elements (breaks alignment) → creates depth and visual interest
- Asymmetric layouts (breaks balance) → creates dynamism and movement
- Oversized type beyond scale (breaks type hierarchy) → creates impact
- Reduced contrast (breaks readability) → creates atmosphere (with accessible fallback)
- Mixing serif and sans-serif (breaks consistency) → creates tension and editorial feel

**The test:** If someone looking at your design asks "is this a bug or intentional?", the break wasn't confident enough.

---

## Default Style Posture

When no style is specified in the prompt, generate output with these characteristics:

- **Clean and typographically-led** — hierarchy through type scale and weight, not decoration
- **Generous space** — comfortable padding and margins, nothing feels cramped
- **Neutral palette** — semantic colors from CONFIG.md, minimal accent usage
- **Subtle depth** — `shadow-sm` on cards, `border` for separation, no heavy shadows
- **Functional over decorative** — every element serves a purpose
- **Responsive by default** — stacks cleanly on mobile, expands on desktop
- **Accessible by default** — proper contrast, focus states, semantic HTML

This posture is shadcn/ui's implied aesthetic: clean, professional, invisible design system that stays out of the way. When a STYLES/ file is activated, it overrides this posture for the properties it addresses.
