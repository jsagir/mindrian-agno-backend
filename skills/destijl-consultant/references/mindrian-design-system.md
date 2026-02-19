# Mindrian Design System: De Stijl Component Mapping

## Overview

This document maps every Mindrian UI component to De Stijl design principles. Each component has specific rules for color, spacing, typography, and behavior.

---

## Layout Shell

The top-level layout is a CSS Grid that creates the Mondrian-esque composition:

```css
.mindrian-shell {
  display: grid;
  grid-template-columns: var(--chat-width, 1fr) var(--analysis-width, 1fr);
  grid-template-rows: auto 1fr auto;
  height: 100vh;
  background: var(--color-bg); /* #0D0D0D */
}
```

### De Stijl Rules
- **No rounded corners** on the outer shell
- **1px borders** separate panels — these are Mondrian's black lines
- **Panels resize** but snap to 8px grid
- **Minimum chat width**: 400px (ensures readable message bubbles)
- **Minimum analysis width**: 320px

---

## Chat Panel Components

### Message Bubble (`message-bubble.tsx`)

**Current**: Rounded cards with background tints
**De Stijl**: Rectangular blocks with left-border accent

```
┌──────────────────────────────────┐
│ ■ Agent Name              12:34  │
│                                  │
│  Message content in Inter 14px.  │
│  Line height 1.6, max-width     │
│  72ch for readability.           │
│                                  │
│  [Evidence Block]   [Link]       │
└──────────────────────────────────┘
```

| Property | User Message | Agent Message |
|----------|-------------|---------------|
| Background | `#1A1A1A` (surface) | `#0D0D0D` (bg) |
| Left border | none | 3px, active agent color |
| Border radius | 0-2px max | 0-2px max |
| Text color | `#F5F0E8` (cream) | `#F5F0E8` (cream) |
| Padding | 12px 16px | 12px 16px |
| Margin bottom | 8px | 8px |

### Agent Switcher (`agent-switcher.tsx`)

**De Stijl**: Compact, architectural dropdown. No pill shapes. Categories separated by thin black lines.

| Property | Value |
|----------|-------|
| Trigger | Rectangular button, 1px border, agent color dot (2.5px circle) |
| Dropdown | No shadow, 1px border, sharp corners |
| Category headers | 10px uppercase, `--color-muted`, heavy tracking |
| Hover state | `--color-elevated` background, no animation |
| Selected state | Agent color at 10% opacity background |

### Ask/Tell Dial (`ask-tell-dial.tsx`)

**De Stijl**: Linear slider, not circular. The slider track is a black line. The thumb is a colored rectangle.

| Property | Value |
|----------|-------|
| Track | 2px height, `--color-border` |
| Filled track | 2px height, active agent color |
| Thumb | 12px x 12px rectangle, agent color fill, no border-radius |
| Labels | "Explore" / "Converge" in 12px Inter, muted |
| Mode label | 14px Inter semibold, cream |

### Filing Interrupt Card (`filing-interrupt-card.tsx`)

When the system identifies a Data Room entry, it shows an interrupt card in the chat.

**De Stijl**: High-contrast card with section-color top border (4px).

| Property | Value |
|----------|-------|
| Border top | 4px solid, section color |
| Background | `#1A1A1A` |
| Border | 1px `#2A2A2A` |
| Section indicator | 8px circle in section color + section name in caption style |
| Actions | Text buttons in section color, rectangular hover state |

---

## Data Room Components

### Data Room Sidebar (`data-room-sidebar.tsx`)

The primary list view of Data Room entries, organized by section.

**De Stijl**: Each section is a Mondrian rectangle — a colored region in the grid. Section headers are architectural (Bebas Neue uppercase).

```
┌──────────────────────────────────┐
│ PROBLEM                    (3)   │  ← Bebas Neue, Cadmium Red
├──────────────────────────────────┤
│ ■ First problem entry            │  ← 3px left border, red
│ ■ Second problem entry           │
│ ■ Third problem entry            │
├──────────────────────────────────┤
│ QUESTION                   (5)   │  ← Bebas Neue, Cobalt Blue
├──────────────────────────────────┤
│ ■ First question entry           │
│ ...                              │
└──────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Section header | Bebas Neue 20px, section color, uppercase |
| Entry count | 12px Inter, muted, right-aligned |
| Entry item | 14px Inter, cream, 3px left border in section color |
| Entry hover | Background `#2A2A2A`, no other change |
| Section divider | 1px `#2A2A2A` full-width |
| Spacing | 8px between entries, 16px between sections |

### Data Room Detail (`data-room-detail.tsx`)

Expanded view of a single entry.

**De Stijl**: Clean card with section color accent. Content blocks (claim, evidence, challenge) are visually distinct sub-blocks.

| Block Type | Visual Treatment |
|------------|-----------------|
| Claim | 2px left border in section color, surface background |
| Evidence | Amethyst (`#6B4E8B`) 2px left border, slightly elevated bg |
| Challenge | Cadmium Red (`#A63D2F`) 2px left border, surface bg |
| Source | Muted text, small icon, link style |

### Data Room Folder (`data-room-folder.tsx`)

Grouping mechanism for related entries.

| Property | Value |
|----------|-------|
| Folder icon | Simple geometric shape (rectangle), section color |
| Label | 14px Inter semibold |
| Expand/collapse | No animation, instant toggle |
| Indent | 16px per nesting level |

---

## Analysis Panel Components

### Analysis Panel (`analysis-panel.tsx`)

Tabbed container for Data Room, Signals, Routing, and Workshop.

**De Stijl**: Tabs are underline-only (Mondrian's black lines as selectors).

| Property | Value |
|----------|-------|
| Tab style | Text-only, no background |
| Active indicator | 2px bottom border in active section color |
| Inactive tab | Muted text, no border |
| Tab spacing | 16px gap |
| Content area | Full remaining height, no padding (each child provides own) |

### Intelligence Sidebar (`intelligence-sidebar.tsx`)

Displays agent reasoning, confidence scores, and routing decisions.

| Property | Value |
|----------|-------|
| Background | `#0D0D0D` (deepest layer) |
| Agent reasoning | 12px Inter, muted, monospace for structured data |
| Confidence score | Horizontal bar, section color fill, gray track |
| Routing indicator | Small colored dots showing active agents |

### Routing Panel (`routing-panel.tsx`)

Shows the 3-layer routing system.

| Property | Value |
|----------|-------|
| Layer labels | Bebas Neue 16px |
| Active route | Section color highlight |
| Inactive route | Muted, 50% opacity |
| Connection lines | 1px, `#2A2A2A` |

---

## Project Map Components

### Project Map (`project-map.tsx`) — React Flow

The graph visualization of the Data Room network.

**De Stijl**: Nodes are rectangles. Edges are straight lines (no curves). Colors follow section mapping.

| Property | Value |
|----------|-------|
| Node shape | Rectangle, no border-radius, 1px border |
| Node background | `#1A1A1A` |
| Node border | Section color, 1px |
| Node label | Inter 12px, cream |
| Edge style | Straight lines only (`type: 'straight'`) |
| Edge color | `#2A2A2A` default, section color when highlighted |
| Background | `#0D0D0D`, no dots/grid pattern |
| Minimap | Bottom-right, section colors for nodes |

### Map Node (`map-node.tsx`)

Custom React Flow node.

| Property | Value |
|----------|-------|
| Width | 160px (20 grid units) |
| Height | Auto, min 48px |
| Padding | 8px 12px |
| Title | 12px Inter semibold, cream |
| Subtitle | 10px Inter, muted |
| Ports | 6px circles, section color, centered on edges |

---

## Overlay Components

### Command Palette (`command-palette.tsx`)

**De Stijl**: Full-width at top of viewport, 4px black bottom border. No rounded corners. No shadow.

| Property | Value |
|----------|-------|
| Width | 100%, max 640px centered |
| Background | `#1A1A1A` |
| Border | 1px `#2A2A2A`, 4px bottom black accent |
| Input | Full-width, no border, large text (20px Inter) |
| Results | Clean list, 1px dividers, section color icons |
| Selected | `#2A2A2A` background |

### Splash Screen (`splash-screen.tsx`)

**De Stijl**: Dramatic Mondrian composition. Large colored rectangles forming an asymmetric grid with the Mindrian logo.

| Property | Value |
|----------|-------|
| Background | `#0D0D0D` |
| Grid | Asymmetric, uses all 8 section colors as rectangles |
| Logo | Bebas Neue, cream, centered in largest rectangle |
| Loading indicator | Thin horizontal line animation (grows from left to right) |
| Duration | 2 seconds max |

---

## Shared Components

### Agent Badge (`agent-badge.tsx`)

Small indicator showing which agent is active.

| Property | Value |
|----------|-------|
| Shape | Rectangle, 2px border-radius max |
| Background | Agent color at 10% opacity |
| Text | 10px Inter semibold, agent color |
| Dot | 6px circle, agent color, left of text |

### Voice Toggle (`voice-toggle.tsx`)

| Property | Value |
|----------|-------|
| Icon | Geometric microphone (rectangles only) |
| Active | Cadmium Red fill (recording = urgent) |
| Inactive | Muted, 1px border |
| Size | 32px square |

### Connection Status (`connection-status.tsx`)

| Property | Value |
|----------|-------|
| Connected | Viridian Green 6px circle |
| Disconnected | Cadmium Red 6px circle |
| Connecting | Ochre Yellow 6px circle, no animation |
| Label | 10px Inter, muted |

---

## CSS Custom Properties

All De Stijl tokens should be defined as CSS custom properties in `globals.css`:

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
}
```
