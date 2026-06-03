# CONFIG — Tailwind Token Reference

This file is the authoritative source of allowed design tokens. Every class used in output must resolve to a token defined here or in Tailwind v4's default utility set. No exceptions.

---

## Color System

Two layers: **primitives** (raw scales) and **semantic tokens** (purpose-driven, what you actually use in components).

### Primitive Color Scales

Defined in `:root` as CSS variables. These exist as a palette — do not use primitives directly in component classes. Always go through semantic tokens.

| Scale Step | Purpose |
|---|---|
| 50 | Lightest tint — subtle backgrounds |
| 100 | Light background |
| 200 | Light border, hover background |
| 300 | Border, disabled text |
| 400 | Placeholder text, icons |
| 500 | Mid-tone — body text on light, icons |
| 600 | Strong text, active states |
| 700 | Headings, high-contrast text |
| 800 | Heavy emphasis |
| 900 | Near-black |
| 950 | Deepest — dark mode backgrounds |

**Neutral** (gray, achromatic)

```css
--neutral-50:  oklch(0.985 0 0);
--neutral-100: oklch(0.970 0 0);
--neutral-200: oklch(0.922 0 0);
--neutral-300: oklch(0.870 0 0);
--neutral-400: oklch(0.708 0 0);
--neutral-500: oklch(0.556 0 0);
--neutral-600: oklch(0.439 0 0);
--neutral-700: oklch(0.371 0 0);
--neutral-800: oklch(0.269 0 0);
--neutral-900: oklch(0.205 0 0);
--neutral-950: oklch(0.145 0 0);
```

**Blue** (information, links, primary actions)

```css
--blue-50:  oklch(0.970 0.014 254);
--blue-100: oklch(0.932 0.032 255);
--blue-200: oklch(0.882 0.059 254);
--blue-300: oklch(0.809 0.105 251);
--blue-400: oklch(0.707 0.165 254);
--blue-500: oklch(0.623 0.214 259);
--blue-600: oklch(0.546 0.245 262);
--blue-700: oklch(0.488 0.243 264);
--blue-800: oklch(0.424 0.199 265);
--blue-900: oklch(0.379 0.146 265);
--blue-950: oklch(0.282 0.091 267);
```

**Red** (errors, destructive actions, danger)

```css
--red-50:  oklch(0.971 0.013 17);
--red-100: oklch(0.936 0.032 17);
--red-200: oklch(0.885 0.062 18);
--red-300: oklch(0.808 0.114 19);
--red-400: oklch(0.704 0.191 22);
--red-500: oklch(0.637 0.237 25);
--red-600: oklch(0.577 0.245 27);
--red-700: oklch(0.505 0.213 27);
--red-800: oklch(0.444 0.177 26);
--red-900: oklch(0.396 0.141 25);
--red-950: oklch(0.258 0.092 26);
```

**Green** (success, confirmation, positive)

```css
--green-50:  oklch(0.982 0.018 166);
--green-100: oklch(0.962 0.044 164);
--green-200: oklch(0.925 0.084 164);
--green-300: oklch(0.871 0.119 166);
--green-400: oklch(0.792 0.145 165);
--green-500: oklch(0.723 0.150 166);
--green-600: oklch(0.627 0.130 168);
--green-700: oklch(0.527 0.109 169);
--green-800: oklch(0.448 0.089 172);
--green-900: oklch(0.393 0.074 172);
--green-950: oklch(0.266 0.050 172);
```

**Amber** (warning, caution, attention)

```css
--amber-50:  oklch(0.987 0.022 95);
--amber-100: oklch(0.962 0.059 95);
--amber-200: oklch(0.924 0.120 95);
--amber-300: oklch(0.879 0.169 91);
--amber-400: oklch(0.828 0.189 84);
--amber-500: oklch(0.769 0.188 70);
--amber-600: oklch(0.666 0.179 58);
--amber-700: oklch(0.555 0.163 49);
--amber-800: oklch(0.473 0.137 46);
--amber-900: oklch(0.414 0.112 45);
--amber-950: oklch(0.279 0.077 45);
```

**Violet** (creative, accent, decorative)

```css
--violet-50:  oklch(0.969 0.016 293);
--violet-100: oklch(0.943 0.029 294);
--violet-200: oklch(0.894 0.057 293);
--violet-300: oklch(0.811 0.111 293);
--violet-400: oklch(0.702 0.183 293);
--violet-500: oklch(0.606 0.250 292);
--violet-600: oklch(0.541 0.281 293);
--violet-700: oklch(0.491 0.270 292);
--violet-800: oklch(0.432 0.232 292);
--violet-900: oklch(0.383 0.189 293);
--violet-950: oklch(0.283 0.141 292);
```

### Semantic Color Tokens

These are the tokens you use in Tailwind classes. Each maps to a primitive via CSS variable.

```css
@theme inline {
  /* Surface */
  --color-background: var(--background);
  --color-foreground: var(--foreground);

  /* Card */
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);

  /* Popover */
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);

  /* Primary — main actions, active states */
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);

  /* Secondary — supporting actions, less emphasis */
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);

  /* Muted — subdued content, disabled states */
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);

  /* Accent — highlights, hover states, visual interest */
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);

  /* Destructive — deletions, errors, irreversible actions */
  --color-destructive: var(--destructive);

  /* Success — confirmations, positive outcomes */
  --color-success: var(--success);
  --color-success-foreground: var(--success-foreground);

  /* Warning — caution states, non-blocking alerts */
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);

  /* Structural */
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);

  /* Chart palette */
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);

  /* Sidebar */
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);
}
```

**Default semantic-to-primitive mapping (light mode):**

| Semantic Token | Maps To | Purpose |
|---|---|---|
| `background` | `neutral-50` | Page background |
| `foreground` | `neutral-950` | Default text |
| `card` | `neutral-50` | Card surfaces |
| `card-foreground` | `neutral-950` | Card text |
| `popover` | `neutral-50` | Popover surfaces |
| `popover-foreground` | `neutral-950` | Popover text |
| `primary` | `neutral-900` | Primary buttons, links |
| `primary-foreground` | `neutral-50` | Text on primary |
| `secondary` | `neutral-100` | Secondary buttons |
| `secondary-foreground` | `neutral-900` | Text on secondary |
| `muted` | `neutral-100` | Muted backgrounds |
| `muted-foreground` | `neutral-500` | Subdued text |
| `accent` | `neutral-100` | Hover/focus backgrounds |
| `accent-foreground` | `neutral-900` | Text on accent |
| `destructive` | `red-600` | Delete, error actions |
| `success` | `green-600` | Confirmation, positive |
| `success-foreground` | `neutral-50` | Text on success |
| `warning` | `amber-500` | Caution states |
| `warning-foreground` | `neutral-950` | Text on warning |
| `border` | `neutral-200` | Default borders |
| `input` | `neutral-200` | Input borders |
| `ring` | `neutral-400` | Focus rings |

**Dark mode** inverts the lightness axis — `background` → `neutral-950`, `foreground` → `neutral-50`, etc.

---

## Spacing

Uses Tailwind v4's default spacing scale. Base unit: `0.25rem` (4px at default font size).

| Token | Value | Use for |
|---|---|---|
| `0` | `0` | Reset |
| `px` | `1px` | Hairline borders |
| `0.5` | `0.125rem` | Micro spacing |
| `1` | `0.25rem` | Tight internal padding |
| `1.5` | `0.375rem` | Small gap |
| `2` | `0.5rem` | Compact padding |
| `2.5` | `0.625rem` | — |
| `3` | `0.75rem` | Component internal padding |
| `3.5` | `0.875rem` | — |
| `4` | `1rem` | Standard padding |
| `5` | `1.25rem` | Comfortable padding |
| `6` | `1.5rem` | Section internal gap |
| `7` | `1.75rem` | — |
| `8` | `2rem` | Component gap |
| `9` | `2.25rem` | — |
| `10` | `2.5rem` | Large gap |
| `11` | `2.75rem` | — |
| `12` | `3rem` | Section padding |
| `14` | `3.5rem` | — |
| `16` | `4rem` | Large section padding |
| `20` | `5rem` | Page section spacing |
| `24` | `6rem` | Major section gap |
| `28` | `7rem` | — |
| `32` | `8rem` | Hero padding |
| `36` | `9rem` | — |
| `40` | `10rem` | — |
| `44` | `11rem` | — |
| `48` | `12rem` | — |
| `52` | `13rem` | — |
| `56` | `14rem` | — |
| `60` | `15rem` | — |
| `64` | `16rem` | — |
| `72` | `18rem` | — |
| `80` | `20rem` | — |
| `96` | `24rem` | — |

**Rule:** Do not mix spacing scales within a single component. Pick a rhythmic subset and stay consistent.

---

## Typography

### Font Size

| Token | Size | Line Height | Use for |
|---|---|---|---|
| `text-xs` | `0.75rem` | `1rem` | Labels, captions, fine print |
| `text-sm` | `0.875rem` | `1.25rem` | Secondary text, metadata |
| `text-base` | `1rem` | `1.5rem` | Body text |
| `text-lg` | `1.125rem` | `1.75rem` | Lead paragraphs |
| `text-xl` | `1.25rem` | `1.75rem` | Subheadings |
| `text-2xl` | `1.5rem` | `2rem` | Section headings |
| `text-3xl` | `1.875rem` | `2.25rem` | Page headings |
| `text-4xl` | `2.25rem` | `2.5rem` | Hero subheading |
| `text-5xl` | `3rem` | `1` | Display text |
| `text-6xl` | `3.75rem` | `1` | Large display |
| `text-7xl` | `4.5rem` | `1` | Extra large display |
| `text-8xl` | `6rem` | `1` | Statement type |
| `text-9xl` | `8rem` | `1` | Poster type |

### Font Weight

| Token | Weight | Use for |
|---|---|---|
| `font-thin` | 100 | Decorative display only |
| `font-extralight` | 200 | Light display text |
| `font-light` | 300 | Elegant body text |
| `font-normal` | 400 | Default body text |
| `font-medium` | 500 | Subtle emphasis, labels |
| `font-semibold` | 600 | Subheadings, buttons |
| `font-bold` | 700 | Headings, strong emphasis |
| `font-extrabold` | 800 | Impact headings |
| `font-black` | 900 | Display/poster use only |

### Tracking (Letter Spacing)

| Token | Value |
|---|---|
| `tracking-tighter` | `-0.05em` |
| `tracking-tight` | `-0.025em` |
| `tracking-normal` | `0em` |
| `tracking-wide` | `0.025em` |
| `tracking-wider` | `0.05em` |
| `tracking-widest` | `0.1em` |

### Leading (Line Height)

| Token | Value |
|---|---|
| `leading-none` | `1` |
| `leading-tight` | `1.25` |
| `leading-snug` | `1.375` |
| `leading-normal` | `1.5` |
| `leading-relaxed` | `1.625` |
| `leading-loose` | `2` |

---

## Border Radius

Derived from `--radius` base variable. shadcn/ui default: `--radius: 0.625rem`.

```css
@theme inline {
  --radius-sm:  calc(var(--radius) * 0.6);   /* ~0.375rem */
  --radius-md:  calc(var(--radius) * 0.8);   /* ~0.5rem   */
  --radius-lg:  var(--radius);                /* 0.625rem  */
  --radius-xl:  calc(var(--radius) * 1.4);   /* ~0.875rem */
  --radius-2xl: calc(var(--radius) * 1.8);   /* ~1.125rem */
  --radius-3xl: calc(var(--radius) * 2.2);   /* ~1.375rem */
  --radius-4xl: calc(var(--radius) * 2.6);   /* ~1.625rem */
}
```

| Token | Use for |
|---|---|
| `rounded-sm` | Subtle rounding — tags, badges |
| `rounded-md` | Inputs, small cards |
| `rounded-lg` | Cards, dialogs, primary surfaces |
| `rounded-xl` | Large cards, hero sections |
| `rounded-2xl` | Feature cards, image containers |
| `rounded-3xl` | Decorative, pill-adjacent |
| `rounded-4xl` | Pill shapes, full rounding |
| `rounded-full` | Circles, avatars, pill buttons |

---

## Shadows

| Token | Use for |
|---|---|
| `shadow-xs` | Subtle depth — inputs, tags |
| `shadow-sm` | Cards at rest |
| `shadow-md` | Elevated cards, dropdowns |
| `shadow-lg` | Modals, popovers |
| `shadow-xl` | Floating elements |
| `shadow-2xl` | Maximum elevation |
| `shadow-none` | Flat — reset shadow |

---

## Transitions

| Token | Duration | Use for |
|---|---|---|
| `duration-75` | 75ms | Micro feedback — opacity, color |
| `duration-100` | 100ms | Quick state change |
| `duration-150` | 150ms | Default hover/focus transitions |
| `duration-200` | 200ms | Standard UI transitions |
| `duration-300` | 300ms | Enter/leave, expand/collapse |
| `duration-500` | 500ms | Slow reveals, page-level |
| `duration-700` | 700ms | Dramatic entrance |
| `duration-1000` | 1000ms | Ambient, background |

**Easing:**

| Token | Use for |
|---|---|
| `ease-linear` | Progress bars, continuous motion |
| `ease-in` | Exit animations only |
| `ease-out` | Enter animations only |
| `ease-in-out` | Symmetric transitions, toggle states |

---

## Z-Index

| Token | Value | Use for |
|---|---|---|
| `z-0` | 0 | Base layer |
| `z-10` | 10 | Sticky elements, raised cards |
| `z-20` | 20 | Dropdowns, tooltips |
| `z-30` | 30 | Fixed navigation |
| `z-40` | 40 | Modal overlays |
| `z-50` | 50 | Toasts, notifications |

---

## Never Do This

- **No arbitrary values** — `w-[247px]`, `text-[13px]`, `bg-[#ff5733]`, `p-[1.3rem]` are all forbidden. If a token doesn't exist for your need, the design is wrong, not the token set.
- **No inline styles** — `style={{ }}` bypasses the design system entirely. Never use it.
- **No `!important`** — if specificity is a problem, fix the cascade, don't brute-force it.
- **No mixing spacing scales** — don't use `p-3` next to `p-5` in the same component with no rhythmic logic. Pick a spacing rhythm and hold it.
- **No primitive colors in classes** — use semantic tokens (`bg-primary`, `text-muted-foreground`), never raw scale values in component code. Primitives exist only to feed the theme.
- **No omitting focus states** — every interactive element must have a visible focus indicator. `focus-visible:ring` or equivalent is mandatory.
- **No unapproved component patterns** — follow METHOD.md structure. Don't invent structural patterns ad-hoc.
- **No hardcoded color values in CSS** — all colors flow through the variable system. Direct `oklch()` or `hsl()` in component styles is a violation.
- **No `text-black` or `text-white`** — use `text-foreground`, `text-primary-foreground`, etc. Raw black/white bypasses the theme.
