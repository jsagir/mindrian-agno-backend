# Mondrian Principles: De Stijl Theory for Digital Design

## Historical Foundation

De Stijl ("The Style") was founded in 1917 in the Netherlands by Piet Mondrian, Theo van Doesburg, and others. It was not merely an art movement — it was a philosophical program for achieving universal harmony through the reduction of visual language to its most fundamental elements.

### The Neo-Plasticism Manifesto (1920)

Mondrian's core thesis: **Universal beauty is achieved through the dynamic equilibrium of unequal but equivalent oppositions.**

Key tenets:
1. **Line**: Only horizontal and vertical. Diagonals introduce chaos and subjectivity.
2. **Color**: Only primary colors (red, blue, yellow) plus non-colors (black, white, gray). These are universal, not personal.
3. **Form**: Only rectangles. The rectangle is the purest meeting of horizontal and vertical force.
4. **Balance**: Asymmetric. Symmetry is static — it resolves tension. Asymmetry maintains dynamic equilibrium.
5. **Space**: Positive and negative space are equally compositional. White is not "background" — it is an active element.

### Van Doesburg's Extension

Theo van Doesburg later introduced diagonals (which he called "Elementarism"), leading to a famous split with Mondrian. For Mindrian's purposes, we follow Mondrian's orthogonal discipline, but acknowledge van Doesburg's insight: **tension can be introduced through scale and proportion, not just color and placement.**

---

## The Grid System

### Mondrian's Compositional Grid

Mondrian's paintings are not random divisions of a rectangle. They follow discoverable rules:

1. **Primary divisions**: The canvas is first divided by dominant lines into major regions
2. **Subdivision**: Some regions are further subdivided, creating hierarchy
3. **Asymmetric proportions**: No two adjacent regions share the same dimension
4. **Color placement**: Color appears in smaller regions, creating visual weight that balances larger neutral regions
5. **Edge tension**: Lines that terminate at the canvas edge create implied continuation — the composition extends beyond the frame

### Application to UI Layout

```
┌─────────────────────────────────────────────────┐
│                 HEADER (thin)                     │
├──────────────────┬──────────────────────────────┤
│                  │                               │
│   CHAT PANEL     │     ANALYSIS PANEL            │
│   (flexible)     │     (flexible)                │
│                  │                               │
│                  │  ┌─────────┬───────────────┐  │
│                  │  │ Section │  Detail View   │  │
│                  │  │ List    │               │  │
│                  │  │         │               │  │
│                  │  └─────────┴───────────────┘  │
│                  │                               │
├──────────────────┴──────────────────────────────┤
│              STATUS BAR (thin)                    │
└─────────────────────────────────────────────────┘
```

**Grid rules for Mindrian**:
- Base unit: **8px** (all spacing is multiples of 8)
- Column count: responsive (12 columns on desktop)
- Gutter: 16px (2 units)
- Panel min-width: 320px
- Panel resize snaps to 8px increments

---

## Color Theory

### Mondrian's Color Philosophy

Mondrian chose red, blue, and yellow not because they are "pretty" but because they are **irreducible**. They cannot be created by mixing other colors. They are primary — fundamental — essential.

In De Stijl, color is never decorative. It is **semantic**: each color carries meaning by virtue of its relationships within the composition.

### Mindrian's Extended Palette

We extend Mondrian's three primaries to eight section colors, each an authentic pigment from the De Stijl era or adjacent Dutch painting tradition:

| Pigment | Hex | RGB | HSL | WCAG on #0D0D0D |
|---------|-----|-----|-----|-----------------|
| Cadmium Red | `#A63D2F` | 166, 61, 47 | 7°, 56%, 42% | 4.5:1 AA |
| Cobalt Blue | `#1E3A6E` | 30, 58, 110 | 219°, 57%, 27% | 3.8:1 (use lighter for text) |
| Ochre Yellow | `#C8A43C` | 200, 164, 60 | 45°, 54%, 51% | 7.2:1 AAA |
| Viridian Green | `#2D6B4A` | 45, 107, 74 | 148°, 41%, 30% | 4.1:1 AA |
| Burnt Sienna | `#B5602A` | 181, 96, 42 | 23°, 62%, 44% | 4.8:1 AA |
| Warm Gray | `#5C5A56` | 92, 90, 86 | 40°, 3%, 35% | 3.5:1 (use for non-critical) |
| Amethyst | `#6B4E8B` | 107, 78, 139 | 268°, 28%, 43% | 4.2:1 AA |
| Deep Teal | `#2A6B5E` | 42, 107, 94 | 168°, 44%, 29% | 4.0:1 AA |

### Non-Colors

| Role | Hex | Usage |
|------|-----|-------|
| Background | `#0D0D0D` | Page background, deepest layer |
| Surface | `#1A1A1A` | Panel backgrounds, cards |
| Elevated | `#2A2A2A` | Hover states, elevated cards, borders |
| Cream | `#F5F0E8` | Primary text (warm, not harsh white) |
| Muted | `#A09A90` | Secondary text, labels, placeholders |
| Border | `#2A2A2A` | Structural dividers |

### Color Usage Rules

1. **Section colors are semantic** — never use Cadmium Red for a "delete" button. It means "Problem section."
2. **Danger/success/warning** use desaturated variants of section colors, never pure green/red
3. **Color at 10% opacity** for backgrounds: `#A63D2F1A` creates a subtle tint
4. **Color at 100%** for accents: borders, icons, small indicators
5. **Never more than 2 section colors visible simultaneously** in the same panel
6. **The active section's color** pervades the current view as the dominant accent

---

## Typography

### Mondrian's Relationship to Type

Mondrian himself rarely used typography, but the De Stijl movement had strong typographic opinions. Vilmos Huszar and Piet Zwart developed a typographic style characterized by:
- **Geometric sans-serif** forms
- **Strong hierarchy** through size and weight, never through decoration
- **Horizontal and vertical** text orientation (no italics for emphasis)
- **Uppercase for headings** — architectural, monumental

### Mindrian Type System

| Level | Font | Size | Weight | Tracking | Usage |
|-------|------|------|--------|----------|-------|
| Display | Bebas Neue | 48px | 400 | 0.05em | Hero headings, splash |
| H1 | Bebas Neue | 32px | 400 | 0.04em | Page titles |
| H2 | Bebas Neue | 24px | 400 | 0.03em | Section titles |
| H3 | Inter | 20px | 600 | 0.01em | Panel titles |
| Body | Inter | 14px | 400 | 0 | Default text |
| Body Small | Inter | 12px | 400 | 0 | Secondary info |
| Caption | Inter | 10px | 500 | 0.05em | Labels, tags |
| Mono | JetBrains Mono | 13px | 400 | 0 | Code, data |

### Typography Rules

1. **Never use italic** for emphasis. Use weight (semibold) or color.
2. **Uppercase is reserved** for Bebas Neue headings and tiny labels (10px captions)
3. **Line height**: Body text = 1.6. Headings = 1.2. Tight = 1.0 (for data displays)
4. **Maximum line length**: 72ch for body text. No exceptions.
5. **Alignment**: Always left-aligned. Never center large blocks of text. Center only for single-line headings in specific contexts.

---

## Composition Principles

### Dynamic Equilibrium

The central concept. Every composition must feel balanced without being symmetrical. Achieve this through:

1. **Weight through color**: A small red element balances a large gray area
2. **Weight through density**: Dense text balances a large image
3. **Weight through position**: Elements near edges have more visual weight
4. **Weight through contrast**: High-contrast elements draw the eye first

### The Rule of Unequal Division

Never divide space equally. A 50/50 split is visually dead. Preferred ratios:
- **Golden ratio** (~61.8% / 38.2%) — for major panel splits
- **2:1** — for simple hierarchies
- **3:5** — for content/sidebar relationships

### Implied Lines and Continuation

Mondrian's compositions extend beyond the canvas. Lines that reach the edge imply continuation into infinite space. In UI:
- Elements can bleed to panel edges
- Scroll indicators suggest content beyond the viewport
- The Data Room graph (React Flow) extends infinitely — nodes at the edge imply a larger network

### Negative Space Hierarchy

Three levels of negative space in Mindrian:
1. **Macro**: Space between major panels (16-32px)
2. **Meso**: Space within panels between sections (12-16px)
3. **Micro**: Space within components between elements (4-8px)

Each level must be consistently applied. Never mix macro spacing within a micro context.
