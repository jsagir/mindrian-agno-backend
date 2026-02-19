# De Stijl Design Specification — Mindrian V2

**Version**: 1.0
**Date**: 2026-02-19
**Status**: Active
**Branch**: `ui/destijl-rebuild`

---

## 1. Design Philosophy

Mindrian V2 adopts the De Stijl visual identity — not as pastiche, but as a living design system rooted in Mondrian's principles of universal harmony through reduction, orthogonal structure, and dynamic equilibrium.

**Core thesis**: Universal beauty is achieved through the dynamic equilibrium of unequal but equivalent oppositions.

**Applied to product**: Every pixel earns its place. Structure emerges from the grid. Color carries meaning. White space is active, not empty.

---

## 2. Color Palette

### 2.1 Section Colors (8)

Each color maps to a Data Room section. Color is semantic — it tells the user what *kind* of knowledge they're looking at.

| # | Name | Hex | RGB | Section | Semantic |
|---|------|-----|-----|---------|----------|
| 1 | Cadmium Red | `#A63D2F` | 166, 61, 47 | Problem | Pain, urgency, what's broken |
| 2 | Cobalt Blue | `#1E3A6E` | 30, 58, 110 | Question | What we need to know |
| 3 | Ochre Yellow | `#C8A43C` | 200, 164, 60 | Future | Where things are going |
| 4 | Viridian Green | `#2D6B4A` | 45, 107, 74 | Customer | Who we serve |
| 5 | Burnt Sienna | `#B5602A` | 181, 96, 42 | Challenge | Who/what opposes |
| 6 | Warm Gray | `#5C5A56` | 92, 90, 86 | Systems | How things connect |
| 7 | Amethyst | `#6B4E8B` | 107, 78, 139 | Evidence | What validates |
| 8 | Deep Teal | `#2A6B5E` | 42, 107, 94 | Timing | When to act |

### 2.2 Accessible Text Variants

For text on dark backgrounds, each section color has a lightened variant:

| Section Color | Text Variant | Contrast on #0D0D0D |
|---------------|-------------|---------------------|
| `#A63D2F` | `#C95A4A` | 5.8:1 AA |
| `#1E3A6E` | `#4A7BC8` | 5.2:1 AA |
| `#C8A43C` | `#C8A43C` | 7.2:1 AAA (no change needed) |
| `#2D6B4A` | `#4A9B72` | 5.5:1 AA |
| `#B5602A` | `#D4804A` | 6.1:1 AA |
| `#5C5A56` | `#8A8780` | 4.5:1 AA |
| `#6B4E8B` | `#9B7EB5` | 5.0:1 AA |
| `#2A6B5E` | `#4A9B8E` | 5.3:1 AA |

### 2.3 Non-Colors

| Role | Hex | CSS Variable | Usage |
|------|-----|-------------|-------|
| Background | `#0D0D0D` | `--ds-bg` | Page background |
| Surface | `#1A1A1A` | `--ds-surface` | Panel backgrounds, cards |
| Elevated | `#2A2A2A` | `--ds-elevated` | Hover states, raised elements |
| Cream | `#F5F0E8` | `--ds-cream` | Primary text |
| Muted | `#A09A90` | `--ds-muted` | Secondary text, labels |
| Border | `#2A2A2A` | `--ds-border` | Structural dividers (1px) |
| Black | `#000000` | `--ds-black` | Deepest background (behind app on wide screens) |

### 2.4 Color Usage Rules

1. Section colors are **semantic only** — never use for generic UI states
2. Danger/success/warning derive from section colors, not standard red/green/yellow
3. Color at **10% opacity** for background tints: `{color}1A`
4. Color at **100%** for small accents: borders, icons, indicators
5. Maximum **2 section colors visible simultaneously** in one panel
6. Active section color pervades the current view

---

## 3. Grid System

### 3.1 Base Unit

**8px** — all spacing, sizing, and positioning uses multiples of 8.

| Multiple | Pixels | Usage |
|----------|--------|-------|
| 0.5x | 4px | Micro spacing (icon gaps) |
| 1x | 8px | Tight spacing (list items) |
| 1.5x | 12px | Component padding |
| 2x | 16px | Standard padding, gutters |
| 3x | 24px | Section spacing |
| 4x | 32px | Major section gaps |
| 6x | 48px | Panel header height |
| 8x | 64px | Hero spacing |

### 3.2 Layout Grid

Desktop canonical layout:

```
┌─────────────────────────────────────────────────┐
│                Header Bar (48px)                 │
├──────────────────────┬──────────────────────────┤
│                      │                           │
│    Chat Panel        │    Analysis Panel         │
│    (55% default)     │    (45% default)          │
│                      │                           │
│    min: 400px        │    min: 320px             │
│                      │                           │
├──────────────────────┴──────────────────────────┤
│              Status Bar (32px)                    │
└─────────────────────────────────────────────────┘
```

- Panels separated by **1px border** (Mondrian's black line)
- Resize handle: **4px** wide, cursor col-resize
- Resize snaps to **8px** increments
- Max content width: **1600px** (centered on wide screens)

### 3.3 Responsive Breakpoints

| Name | Width | Columns | Layout |
|------|-------|---------|--------|
| Mobile | < 768px | 1 | Stacked, tab navigation |
| Tablet | 768-1024px | 1-2 | Chat + collapsible analysis |
| Desktop | 1024-1440px | 2 | Full split |
| Wide | > 1440px | 2-3 | Max-width centered |

---

## 4. Typography

### 4.1 Font Stack

| Role | Family | Variable |
|------|--------|----------|
| Body | Inter | `--font-inter` |
| Display | Bebas Neue | `--font-display` |
| Code | JetBrains Mono | `--font-mono` |

### 4.2 Type Scale

| Level | Font | Size | Weight | Line Height | Tracking | Usage |
|-------|------|------|--------|-------------|----------|-------|
| Display | Bebas Neue | 48px | 400 | 1.0 | 0.05em | Hero, splash |
| H1 | Bebas Neue | 32px | 400 | 1.1 | 0.04em | Page titles |
| H2 | Bebas Neue | 24px | 400 | 1.2 | 0.03em | Section titles |
| H3 | Inter | 20px | 600 | 1.3 | 0.01em | Panel titles |
| H4 | Inter | 16px | 600 | 1.4 | 0 | Sub-sections |
| Body | Inter | 14px | 400 | 1.6 | 0 | Default text |
| Body SM | Inter | 12px | 400 | 1.5 | 0 | Secondary info |
| Caption | Inter | 10px | 500 | 1.4 | 0.05em | Labels, tags |
| Mono | JetBrains Mono | 13px | 400 | 1.5 | 0 | Code, data |

### 4.3 Typography Rules

1. **Never italic** for emphasis — use weight (semibold) or color
2. **Uppercase** reserved for Bebas Neue headings and 10px captions
3. **Max line length**: 72ch for body text
4. **Alignment**: Left-aligned always. Center only for single-line display headings.
5. **Truncation**: Single-line overflow uses ellipsis. Never wrap action labels.

---

## 5. Component Rules

### 5.1 Universal Rules

| Property | Rule |
|----------|------|
| Border radius | 0-2px maximum. Never rounded. |
| Shadows | Never. Zero box-shadow. |
| Borders | 1px only (except 3-4px accent borders) |
| Hover | Background shifts one layer deeper |
| Focus | 2px outline in section color, 2px offset |
| Transitions | 150ms ease. No spring/bounce. |
| Opacity on disabled | 40% |

### 5.2 Cards

```
┌─────────────────────────────┐
│ 4px section-color top border │  ← accent cards only
├─────────────────────────────┤
│  Padding: 12px 16px         │
│  Background: --ds-surface   │
│  Border: 1px --ds-border    │
│  Border-radius: 2px max     │
└─────────────────────────────┘
```

### 5.3 Buttons

| Variant | Background | Text | Border | Hover |
|---------|-----------|------|--------|-------|
| Primary | Section color | Cream | none | 10% lighter |
| Secondary | Transparent | Cream | 1px border | Elevated bg |
| Ghost | Transparent | Muted | none | Elevated bg |
| Danger | Red at 10% | Red text variant | 1px red | Red at 20% |

### 5.4 Inputs

| Property | Value |
|----------|-------|
| Background | `--ds-bg` |
| Border | 1px `--ds-border` |
| Border radius | 0 |
| Focus border | Section color |
| Placeholder | `--ds-muted` |
| Padding | 8px 12px |

### 5.5 Tabs

Underline-only. Never pill-shaped, never boxed.

| State | Visual |
|-------|--------|
| Active | 2px bottom border in section color, cream text |
| Inactive | No border, muted text |
| Hover | Muted text becomes cream, no border |

### 5.6 Lists

| Property | Value |
|----------|-------|
| Item height | 40px minimum |
| Divider | 1px `--ds-border` |
| Selected | Section color at 10% bg + 3px left border |
| Hover | `--ds-elevated` bg |

### 5.7 Tooltips

| Property | Value |
|----------|-------|
| Background | `--ds-elevated` |
| Border | 1px `--ds-border` |
| Border radius | 2px |
| Text | 12px Inter, cream |
| Arrow | 6px, matching bg |
| Delay | 500ms |

---

## 6. Animation

### 6.1 Allowed

| Type | Duration | Easing |
|------|----------|--------|
| Fade | 150ms | ease |
| Slide (horizontal) | 200ms | ease-out |
| Slide (vertical) | 200ms | ease-out |
| Scale | 100ms | ease |
| Color transition | 150ms | ease |

### 6.2 Forbidden

- Spring/bounce physics
- Elastic easing
- Parallax scrolling
- Rotation (except loading)
- Blur transitions
- Staggered entry animations

### 6.3 Loading States

| Pattern | Usage |
|---------|-------|
| Horizontal progress bar (2px) | Page load, long operations |
| Skeleton blocks (rectangular) | Content loading |
| Sequential rectangles (3x) | Thinking/processing (replaces dots) |

---

## 7. Iconography

### 7.1 Style

Use Lucide icons (already in stack). When possible, prefer geometric variants:
- Square over circle shapes
- Straight lines over curves
- 1.5px stroke weight
- 16px default size (2 grid units)

### 7.2 Icon Colors

| Context | Color |
|---------|-------|
| Default | `--ds-muted` |
| Active | Section color |
| Interactive | Cream on hover |
| Disabled | `--ds-muted` at 40% |

---

## 8. Spacing Quick Reference

```
4px   ■        micro (icon gaps, tight inline)
8px   ■■       tight (list items, compact)
12px  ■■■      component padding
16px  ■■■■     standard padding, gutters
24px  ■■■■■■   section spacing
32px  ■■■■■■■■ major gaps
48px  ■■■■■■■■■■■■ panel headers
64px  ■■■■■■■■■■■■■■■■ hero spacing
```

---

## 9. CSS Custom Properties

```css
:root {
  /* Section Colors */
  --ds-red: #A63D2F;
  --ds-blue: #1E3A6E;
  --ds-yellow: #C8A43C;
  --ds-green: #2D6B4A;
  --ds-sienna: #B5602A;
  --ds-gray: #5C5A56;
  --ds-amethyst: #6B4E8B;
  --ds-teal: #2A6B5E;

  /* Accessible Text Variants */
  --ds-red-text: #C95A4A;
  --ds-blue-text: #4A7BC8;
  --ds-yellow-text: #C8A43C;
  --ds-green-text: #4A9B72;
  --ds-sienna-text: #D4804A;
  --ds-gray-text: #8A8780;
  --ds-amethyst-text: #9B7EB5;
  --ds-teal-text: #4A9B8E;

  /* Non-Colors */
  --ds-bg: #0D0D0D;
  --ds-surface: #1A1A1A;
  --ds-elevated: #2A2A2A;
  --ds-cream: #F5F0E8;
  --ds-muted: #A09A90;
  --ds-border: #2A2A2A;

  /* Grid */
  --ds-unit: 8px;
  --ds-gutter: 16px;

  /* Typography */
  --ds-font-body: var(--font-inter), system-ui, sans-serif;
  --ds-font-display: var(--font-display), 'Bebas Neue', sans-serif;
  --ds-font-mono: 'JetBrains Mono', monospace;

  /* Transitions */
  --ds-transition: 150ms ease;
  --ds-transition-slow: 200ms ease-out;
}
```

---

## 10. Tailwind Configuration

Map De Stijl tokens to Tailwind in `tailwind.config.ts`:

```ts
{
  theme: {
    extend: {
      colors: {
        'ds-red': '#A63D2F',
        'ds-blue': '#1E3A6E',
        'ds-yellow': '#C8A43C',
        'ds-green': '#2D6B4A',
        'ds-sienna': '#B5602A',
        'ds-gray': '#5C5A56',
        'ds-amethyst': '#6B4E8B',
        'ds-teal': '#2A6B5E',
        'ds-bg': '#0D0D0D',
        'ds-surface': '#1A1A1A',
        'ds-elevated': '#2A2A2A',
        'ds-cream': '#F5F0E8',
        'ds-muted': '#A09A90',
      },
      borderRadius: {
        'ds': '2px',
      },
      transitionDuration: {
        'ds': '150ms',
        'ds-slow': '200ms',
      },
    },
  },
}
```
