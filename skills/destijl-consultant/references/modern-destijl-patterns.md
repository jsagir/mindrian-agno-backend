# Modern De Stijl Patterns: Dark Mode, Responsive, Accessibility

## Dark Mode De Stijl

### Why Dark-First is Authentically De Stijl

A common misconception: De Stijl = white backgrounds with colored rectangles. But Mondrian himself worked with black extensively — his compositions are defined by black lines, and many works feature dominant black regions. A dark-first approach is not a departure from De Stijl; it is an embrace of the non-color spectrum.

### The Dark Palette Strategy

The key insight: **in dark mode, the Mondrian black lines become the background itself**. Structure is revealed through lighter borders and color accents rather than black dividers on white.

```
LIGHT MODE (traditional De Stijl):
  Background = white (#FFFFFF)
  Lines = black (#000000)
  Colors = primary at full saturation

DARK MODE (Mindrian De Stijl):
  Background = near-black (#0D0D0D)
  Lines = dark gray (#2A2A2A)
  Colors = primary at controlled saturation (muted, not neon)
```

### Color Adaptation for Dark Backgrounds

Each section color has been chosen specifically for dark backgrounds:

| Color | Hex | Notes |
|-------|-----|-------|
| Cadmium Red `#A63D2F` | Desaturated from pure red. Reads as "warm danger" not "neon alert" |
| Cobalt Blue `#1E3A6E` | Dark enough to be subtle, light enough to read against #0D0D0D |
| Ochre Yellow `#C8A43C` | Warm gold, not bright yellow. Highest contrast of all section colors |
| Viridian Green `#2D6B4A` | Forest green, not emerald. Calm, grounded |
| Burnt Sienna `#B5602A` | Earth tone, not orange. Historical pigment accuracy |
| Warm Gray `#5C5A56` | Barely visible as "color" — structural, quiet |
| Amethyst `#6B4E8B` | Purple that doesn't vibrate against dark backgrounds |
| Deep Teal `#2A6B5E` | Distinct from Viridian Green — cooler, bluer |

### Light Mode Considerations

If Mindrian ever adds a light mode (feature flag `NEXT_PUBLIC_UI_LIGHT_MODE`):
- Background inverts to `#F5F0E8` (cream, not pure white)
- Surface becomes `#FFFFFF`
- Text becomes `#1A1A1A`
- Section colors increase saturation by 15-20%
- Borders become `#E5E0D8` (warm gray)

---

## Responsive Grid Patterns

### Breakpoints

Following the De Stijl principle that the grid adapts but never breaks:

| Name | Width | Columns | Behavior |
|------|-------|---------|----------|
| Mobile | < 768px | 1 | Stacked panels, chat-first |
| Tablet | 768-1024px | 1-2 | Chat + collapsible analysis |
| Desktop | 1024-1440px | 2 | Full split layout |
| Wide | > 1440px | 2-3 | Max content width: 1600px |

### Mobile Layout (Stacked Mondrian)

On mobile, the two-panel composition collapses to a single column with tab navigation:

```
┌─────────────────────┐
│ [Chat] [Data] [Map] │  ← Tab bar (Mondrian underline tabs)
├─────────────────────┤
│                     │
│   Active Tab        │
│   Content           │
│                     │
│                     │
├─────────────────────┤
│   Input / Actions   │
└─────────────────────┘
```

**Rules**:
- Tab bar uses 2px bottom borders, section color for active
- No drawer patterns (drawers break the grid)
- Data Room entries stack vertically, full-width
- Project Map is touch-enabled with pinch zoom
- Command Palette becomes full-screen

### Tablet Layout (Flexible Composition)

```
┌────────────────┬──────────┐
│                │          │
│   Chat         │ Analysis │  ← Analysis can collapse to icon bar
│                │  (340px) │
│                │          │
└────────────────┴──────────┘
```

**Rules**:
- Analysis panel collapses to 48px icon bar
- Chat panel takes remaining width
- Tap icon bar to expand analysis
- No overlay panels — everything is inline

### Desktop Layout (Full Composition)

The canonical Mondrian layout. Two panels with resizable divider.

**Rules**:
- Default split: 55% chat / 45% analysis (golden ratio approximation)
- Min chat: 400px, Min analysis: 320px
- Resize handle: 4px wide, `#2A2A2A`, `cursor: col-resize`
- Resize snaps to 8px grid

### Wide Layout

On very wide screens, add breathing room:

**Rules**:
- Max total width: 1600px, centered
- Side gutters: 32px minimum
- Consider: third column for persistent minimap or signal feed
- Background behind gutters: pure `#000000` (darker than #0D0D0D)

---

## Accessibility with Primary Colors

### The Challenge

De Stijl's primary colors were chosen for aesthetic and philosophical reasons, not accessibility. Several section colors have marginal contrast ratios against dark backgrounds. Here's how we solve this without compromising the visual identity.

### Contrast Ratios (WCAG 2.1)

| Color | On #0D0D0D | On #1A1A1A | Strategy |
|-------|-----------|-----------|----------|
| Cadmium Red `#A63D2F` | 4.5:1 AA | 3.8:1 | Use for icons/borders. Text uses lighter variant `#C95A4A` |
| Cobalt Blue `#1E3A6E` | 2.2:1 FAIL | 1.9:1 FAIL | NEVER use for text. Use lighter variant `#4A7BC8` for text, original for fills |
| Ochre Yellow `#C8A43C` | 7.2:1 AAA | 6.1:1 AAA | Safe for all uses |
| Viridian Green `#2D6B4A` | 3.5:1 | 3.0:1 | Text uses lighter variant `#4A9B72`. Original for icons/borders |
| Burnt Sienna `#B5602A` | 4.8:1 AA | 4.0:1 | Borderline. Text uses lighter variant `#D4804A` |
| Warm Gray `#5C5A56` | 3.5:1 | 3.0:1 | Non-critical text only. Never for important labels |
| Amethyst `#6B4E8B` | 3.8:1 | 3.2:1 | Text uses lighter variant `#9B7EB5` |
| Deep Teal `#2A6B5E` | 3.6:1 | 3.1:1 | Text uses lighter variant `#4A9B8E` |

### The Two-Variant Strategy

Each section color has two variants:
1. **Full** — the original hex, used for: backgrounds at 10% opacity, borders, icons, filled indicators
2. **Accessible** — lightened 30-40%, used for: any text that must be readable

```css
/* Example: Cadmium Red variants */
--ds-red: #A63D2F;           /* borders, icons, fills */
--ds-red-text: #C95A4A;      /* readable text on dark bg */
--ds-red-subtle: #A63D2F1A;  /* 10% opacity background tint */
```

### Focus Indicators

De Stijl focus indicators must be visible and geometrically precise:

| State | Treatment |
|-------|-----------|
| Focus | 2px outline, active section color, 2px offset |
| Focus-visible | Same as focus (no difference — consistency) |
| Active | Background shifts to `--ds-elevated` |
| Disabled | 40% opacity, `cursor: not-allowed` |

**Rule**: Never rely on color alone. Every colored indicator must also have a shape, position, or text difference.

### Keyboard Navigation

All Mindrian components must be fully keyboard navigable:

| Component | Keys |
|-----------|------|
| Chat messages | Arrow up/down to navigate, Enter to expand |
| Data Room list | Arrow up/down, Enter to open detail, Escape to close |
| Tabs | Arrow left/right, Enter to activate |
| Command Palette | Ctrl+K to open, Arrow keys to navigate, Enter to select |
| Project Map | Arrow keys to pan, +/- to zoom, Tab to focus nodes |
| Agent Switcher | Enter to open, Arrow up/down to navigate, Enter to select |

### Screen Reader Considerations

| Component | ARIA Pattern |
|-----------|-------------|
| Chat | `role="log"`, `aria-live="polite"` for new messages |
| Data Room | `role="tree"` with `role="treeitem"` for entries |
| Tabs | `role="tablist"` / `role="tab"` / `role="tabpanel"` |
| Agent Switcher | `role="listbox"` with `role="option"` |
| Confidence Score | `role="meter"`, `aria-valuenow`, `aria-label` |
| Phase Indicator | `role="progressbar"` |

---

## Animation Principles

### The Rietveld Rule

Gerrit Rietveld's furniture (the Red and Blue Chair, the Schroder House) moved along precise, mechanical axes. No organic curves. No springiness. Everything slides, rotates, or scales along grid lines.

### Allowed Animations

| Animation | Duration | Easing | Usage |
|-----------|----------|--------|-------|
| Fade in/out | 150ms | ease | Panel content, overlays |
| Slide horizontal | 200ms | ease-out | Panel expand/collapse |
| Slide vertical | 200ms | ease-out | Dropdown menus, accordions |
| Scale | 100ms | ease | Hover feedback on interactive elements |
| Border color | 150ms | ease | Focus states, tab selection |
| Background color | 150ms | ease | Hover states |

### Forbidden Animations

- **Spring/bounce physics** — too organic
- **Elastic easing** — implies rubber, not architecture
- **Parallax scrolling** — decorative, not structural
- **Rotation** — diagonals violate orthogonal principle (except loading spinners)
- **Blur transitions** — imprecise, anti-De Stijl
- **Staggered animations** — each element should move as part of the grid, not individually

### Loading States

Instead of spinners (circular = anti-De Stijl), use:

1. **Horizontal progress bar**: Thin line (2px) growing from left to right, section color
2. **Skeleton blocks**: Rectangular placeholders matching content layout, subtle pulse (opacity 0.3 → 0.7)
3. **Thinking indicator**: Three small rectangles appearing sequentially (left to right)

---

## Interaction Patterns

### Hover States

All hover states follow the same rule: **shift background one layer deeper**.

| Context | Default | Hover |
|---------|---------|-------|
| On `#0D0D0D` | transparent | `#1A1A1A` |
| On `#1A1A1A` | transparent | `#2A2A2A` |
| On `#2A2A2A` | transparent | `#333333` |

No other visual changes on hover (no transforms, no shadows, no color shifts).

### Click/Tap Feedback

On click, briefly flash the active section color at 10% opacity as background, then return to hover state. Duration: 100ms.

### Drag and Drop

Drag operations (e.g., moving Data Room entries, rearranging blocks):
- **Drag handle**: 16px tall, 4px wide, `#5C5A56` (Warm Gray), three stacked 1px lines
- **Drag preview**: Semi-transparent clone (80% opacity), 1px border in section color
- **Drop zone**: 2px dashed border in section color, section color at 5% opacity background
- **Drop indicator line**: 2px solid section color, full width of container

### Right-Click Context Menu

De Stijl context menu — rectangular, no shadow, 1px border:

```
┌──────────────────────────┐
│ Ask Agent About This     │
│ Challenge This Entry     │
│ Find Related Evidence    │
├──────────────────────────┤
│ Move to Section...       │
│ Add to Canvas            │
├──────────────────────────┤
│ Delete                   │
└──────────────────────────┘
```

| Property | Value |
|----------|-------|
| Background | `#1A1A1A` |
| Border | 1px `#2A2A2A` |
| Item padding | 8px 12px |
| Item hover | `#2A2A2A` background |
| Divider | 1px `#2A2A2A`, full width |
| Destructive items | Cadmium Red text (accessible variant) |
