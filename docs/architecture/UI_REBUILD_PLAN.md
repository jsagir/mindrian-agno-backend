# Mindrian V2: UI Rebuild Plan — De Stijl + Knowledge Layer

**Version**: 1.0
**Date**: 2026-02-19
**Branch**: `ui/destijl-rebuild`
**Feature Flag**: `NEXT_PUBLIC_UI_DESTIJL=false`

---

## Overview

This plan transforms Mindrian V2's UI from its current dark-mode design into a De Stijl-inspired visual system while simultaneously upgrading the Data Room from a flat list into a networked, multi-view, block-based knowledge structure.

**Core truth**: Chat → Populate Data Room → Validated Innovation

**Not a monolithic rewrite** — this is a three-layer approach:

```
RENDERING LAYER  (what draws pixels)
├─ Chat input/output:     BlockNote (@blocknote/react)
├─ Data Room list view:   React components (De Stijl enhanced)
├─ Data Room canvas view: BlockSuite Edgeless (spatial, read-only)
├─ Data Room graph view:  React Flow (existing)
└─ Data Room dashboard:   React components

KNOWLEDGE LAYER  (brain-support, pure data architecture)
├─ Inbox section (capture without classifying)
├─ Auto-bidirectional links (Neo4j-powered)
├─ Block-based entries (claim/evidence/challenge)
├─ Cross-section references (live-updating)
├─ Smart queries (saved filtered views)
└─ Right-click agent actions

INTELLIGENCE LAYER  (what Mindrian has, competitors don't)
├─ 25 methodology-trained agents
├─ 3-layer intelligent routing
├─ HSI Semantic Surprise discovery
├─ Red Team validation
└─ Saturation detection + grading
```

---

## Sacred Files — Intelligence Wiring Rules

These three files are the nervous system of Mindrian. **Every phase** must verify they remain untouched.

| File | LOC | Rule |
|------|-----|------|
| `use-mindrian.ts` | 57 | NEVER add new state fields |
| `use-mindrian-render.tsx` | 339 | Readable signals NEVER touched |
| `use-mindrian-actions.tsx` | 190 | NEVER modify — new actions go in separate files |

**Why**: These hooks manage the CopilotKit ↔ agent ↔ UI state bridge. Any modification risks breaking the intelligence pipeline that 25 agents depend on.

---

## Phase 0: Foundation (Days 1-2)

**Risk**: None
**Goal**: Design tokens, feature flag, config files

### Deliverables

1. **CSS Custom Properties** — Add all `--ds-*` variables to `globals.css`
2. **Tailwind Extension** — Add De Stijl colors to `tailwind.config.ts`
3. **Feature Flag** — `NEXT_PUBLIC_UI_DESTIJL=false` in `.env.local`
4. **Flag Utility** — `lib/feature-flags.ts` with `useDeStijl()` hook
5. **Font Loading** — Verify Inter + Bebas Neue are loaded (already in `layout.tsx`)

### Files Created/Modified

| File | Action |
|------|--------|
| `frontend/src/app/globals.css` | Add `--ds-*` custom properties |
| `frontend/tailwind.config.ts` | Extend colors, borderRadius, transitions |
| `frontend/.env.local` | Add `NEXT_PUBLIC_UI_DESTIJL=false` |
| `frontend/src/lib/feature-flags.ts` | Create flag utility |

### Intelligence Wiring Check

- [ ] `use-mindrian.ts` unchanged
- [ ] `use-mindrian-render.tsx` unchanged
- [ ] `use-mindrian-actions.tsx` unchanged

---

## Phase 1: De Stijl Layout Shell (Days 3-7)

**Risk**: Low
**Goal**: Replace layout with CSS Grid Mondrian composition

### Deliverables

1. **Grid Shell** — New `mindrian-shell` layout using CSS Grid
2. **Panel Resize** — Drag handle between chat and analysis, snaps to 8px
3. **Header Bar** — 48px, Bebas Neue title, agent status
4. **Status Bar** — 32px, connection status, phase indicator
5. **Responsive Layouts** — Mobile stacked, tablet collapsible, desktop split

### Architecture

```
<MindrianShell>          ← CSS Grid container
  <HeaderBar />          ← grid-row: 1
  <ChatPanel />          ← grid-column: 1
  <ResizeHandle />       ← between columns
  <AnalysisPanel />      ← grid-column: 2
  <StatusBar />          ← grid-row: 3
</MindrianShell>
```

### Files Created/Modified

| File | Action |
|------|--------|
| `components/layout/mindrian-shell.tsx` | Create - Grid shell |
| `components/layout/header-bar.tsx` | Create - Top bar |
| `components/layout/status-bar.tsx` | Create - Bottom bar |
| `components/layout/resize-handle.tsx` | Create - Panel divider |
| `app/page.tsx` | Modify - Wrap in shell (behind flag) |

### Intelligence Wiring Check

- [ ] `use-mindrian.ts` unchanged
- [ ] `use-mindrian-render.tsx` unchanged
- [ ] `use-mindrian-actions.tsx` unchanged
- [ ] Chat panel still receives messages correctly
- [ ] Agent switching still works
- [ ] CopilotKit provider not disrupted

---

## Phase 2: Knowledge Layer — Data Model (Days 8-15)

**Risk**: Medium
**Goal**: Block-based entry structure, inbox, bidirectional links

### Deliverables

1. **Block Entry Type** — TypeScript types for claim/evidence/challenge blocks
2. **Inbox Section** — Capture entries without classifying to a section
3. **Bidirectional Links** — Neo4j relationship queries for cross-references
4. **Block State** — New CopilotKit readable for block-structured entries
5. **Cross-Section References** — Entries that appear in multiple sections

### Data Model

```typescript
interface DataRoomBlock {
  id: string;
  type: 'claim' | 'evidence' | 'challenge' | 'question' | 'insight';
  content: string;           // Rich text (BlockNote JSON)
  sectionId: string;         // Primary section
  crossRefs: string[];       // IDs of related blocks
  sourceMessageId?: string;  // Chat message that created this
  agentId?: string;          // Agent that generated this
  confidence?: number;       // 0-1, from intelligence layer
  metadata: Record<string, unknown>;
  createdAt: string;
  updatedAt: string;
}

interface DataRoomSection {
  id: string;
  name: string;
  color: string;             // De Stijl section color
  blocks: DataRoomBlock[];
  completeness: number;      // 0-100, from saturation detection
}
```

### Key Decisions

- Block content uses **BlockNote JSON format** (not raw HTML, not Markdown)
- Cross-references stored in **Neo4j** (not in-memory), queried via existing GraphRAG
- Inbox is a real section with id `inbox`, color `--ds-muted`
- New actions for block CRUD go in `use-mindrian-blocks.tsx` (NEW file, NOT in use-mindrian-actions.tsx)

### Files Created/Modified

| File | Action |
|------|--------|
| `types/data-room.ts` | Create - Block types |
| `hooks/use-mindrian-blocks.tsx` | Create - Block CRUD actions |
| `lib/neo4j/cross-references.ts` | Create - Bidirectional link queries |
| `hooks/use-mindrian-render.tsx` | **READ-ONLY** — verify sections readable works |

### Intelligence Wiring Check

- [ ] `use-mindrian.ts` unchanged — NO new state fields
- [ ] `use-mindrian-render.tsx` unchanged
- [ ] `use-mindrian-actions.tsx` unchanged
- [ ] New block actions in SEPARATE file `use-mindrian-blocks.tsx`
- [ ] Existing section data still flows from agents correctly
- [ ] Filing interrupt card still works
- [ ] Data Room sidebar still renders current entries

---

## Phase 3: BlockNote Integration (Days 16-23)

**Risk**: HIGH
**Goal**: BlockNote for chat message rendering and Data Room entry editing

### Why HIGH Risk

- BlockNote has its own state management (Yjs-based internally)
- CopilotKit already manages message state
- Dual-state can cause render loops or stale data
- Must be ONE-WAY: CopilotKit state → BlockNote rendering (not bidirectional sync)

### Architecture

```
CopilotKit state (source of truth)
    │
    ▼
BlockNote Editor (read-only renderer for chat)
    • Receives content from CopilotKit messages
    • Does NOT write back to CopilotKit
    • Custom blocks for: evidence, claim, challenge, agent-action

BlockNote Editor (editable for Data Room entries)
    • Source from DataRoomBlock.content
    • Writes to use-mindrian-blocks.tsx actions
    • Does NOT touch use-mindrian-actions.tsx
```

### Deliverables

1. **Chat BlockNote** — Read-only BlockNote instance rendering agent messages
2. **Custom Block Types** — Evidence, Claim, Challenge, AgentAction blocks
3. **Data Room BlockNote** — Editable instance for entry content
4. **Block Serialization** — Convert between CopilotKit message format and BlockNote JSON
5. **De Stijl BlockNote Theme** — Custom theme matching De Stijl spec

### Custom Block Definitions

```typescript
// Evidence block: Amethyst left border, source citation
const EvidenceBlock = createReactBlockSpec({
  type: 'evidence',
  content: 'inline',
  propSchema: {
    source: { default: '' },
    confidence: { default: 0 },
  },
});

// Claim block: Section color left border
const ClaimBlock = createReactBlockSpec({
  type: 'claim',
  content: 'inline',
  propSchema: {
    sectionId: { default: '' },
  },
});

// Challenge block: Red left border
const ChallengeBlock = createReactBlockSpec({
  type: 'challenge',
  content: 'inline',
  propSchema: {
    severity: { default: 'medium' },
  },
});
```

### Files Created/Modified

| File | Action |
|------|--------|
| `components/blocknote/mindrian-theme.ts` | Create - De Stijl theme |
| `components/blocknote/custom-blocks.tsx` | Create - Evidence/Claim/Challenge blocks |
| `components/blocknote/chat-editor.tsx` | Create - Read-only chat renderer |
| `components/blocknote/entry-editor.tsx` | Create - Editable Data Room editor |
| `lib/blocknote/serialization.ts` | Create - Format converters |
| `components/chat/block-assistant-message.tsx` | Modify - Use BlockNote renderer |

### Intelligence Wiring Check

- [ ] `use-mindrian.ts` unchanged
- [ ] `use-mindrian-render.tsx` unchanged
- [ ] `use-mindrian-actions.tsx` unchanged
- [ ] Chat message rendering still works for ALL 25 agents
- [ ] Agent-generated content correctly populates BlockNote blocks
- [ ] Filing interrupt still triggers from agent actions
- [ ] Tool call cards still render inline
- [ ] Confidence scores still display
- [ ] LaTeX rendering still works (KaTeX integration)
- [ ] No render loops between CopilotKit and BlockNote state

---

## Phase 4: BlockSuite Edgeless Canvas (Days 24-28)

**Risk**: Medium
**Goal**: Spatial canvas view of Data Room using BlockSuite Edgeless

### Key Decision

Canvas is a **VIEW**, not a **source**. Data flows ONE WAY:

```
Data Room State (source of truth)
    │
    ▼
BlockSuite Edgeless (read-only spatial view)
    • Renders blocks as positioned rectangles
    • Allows spatial arrangement (position saved separately)
    • Does NOT modify block content
    • Does NOT use Yjs for state sync
```

This eliminates the Yjs ↔ CopilotKit sync problem entirely.

### Deliverables

1. **Canvas Panel** — BlockSuite Edgeless container
2. **Block → Surface Adapter** — Convert DataRoomBlocks to Edgeless surface elements
3. **Position Persistence** — Store spatial positions (localStorage or DB)
4. **Canvas De Stijl Theme** — Section colors for blocks, Mondrian grid background
5. **Canvas ↔ List Sync** — Clicking a canvas block opens its detail in list view

### Files Created/Modified

| File | Action |
|------|--------|
| `components/canvas/canvas-panel.tsx` | Create - Edgeless container |
| `components/canvas/block-adapter.ts` | Create - State → surface elements |
| `components/canvas/canvas-theme.ts` | Create - De Stijl canvas styling |
| `lib/canvas/position-store.ts` | Create - Spatial position persistence |
| `components/panels/analysis-panel.tsx` | Modify - Add canvas tab |

### Intelligence Wiring Check

- [ ] `use-mindrian.ts` unchanged
- [ ] `use-mindrian-render.tsx` unchanged
- [ ] `use-mindrian-actions.tsx` unchanged
- [ ] Canvas reads from same state as list view
- [ ] No new CopilotKit readables introduced
- [ ] Agent actions still work while canvas is open

---

## Phase 5: De Stijl Component Library (Days 29-35)

**Risk**: Low
**Goal**: Reskin all existing components to De Stijl spec

### Deliverables

Reskin each component category to match `DESTIJL_DESIGN_SPEC.md`:

1. **Message Bubbles** — Rectangular, left-border accent, no rounded corners
2. **Agent Switcher** — Architectural dropdown, category headers
3. **Data Room Sidebar** — Section-colored headers (Bebas Neue), block entries
4. **Data Room Detail** — Block-type visual hierarchy
5. **Analysis Tabs** — Underline-only, section color active
6. **Command Palette** — Full-width, 4px bottom accent
7. **Project Map Nodes** — Rectangular, straight edges, section colors
8. **Splash Screen** — Mondrian grid composition
9. **All Buttons** — Rectangular, primary/secondary/ghost variants
10. **All Inputs** — Zero border-radius, section-color focus
11. **All Cards** — No shadow, 1px border, optional 4px color accent

### Files Modified

Every component in `components/` directory. Each reskin:
- Replace `rounded-*` with `rounded-none` or `rounded-[2px]`
- Replace `shadow-*` with nothing
- Replace generic colors with `ds-*` palette
- Add section-color mapping where semantic
- Verify 8px grid alignment

### Intelligence Wiring Check

- [ ] `use-mindrian.ts` unchanged
- [ ] `use-mindrian-render.tsx` unchanged
- [ ] `use-mindrian-actions.tsx` unchanged
- [ ] All 25 agents still render their specialized outputs correctly
- [ ] HSI results panel displays correctly
- [ ] Workshop panel exercises still functional
- [ ] Tool call cards still readable

---

## Phase 6: Polish & Merge (Days 36-40)

**Risk**: Low
**Goal**: QA, accessibility audit, performance, feature flag flip

### Deliverables

1. **Accessibility Audit** — WCAG 2.1 AA for all components
2. **Keyboard Navigation** — Full keyboard support for all interactions
3. **Screen Reader Testing** — ARIA labels, roles, live regions
4. **Performance Profiling** — No regressions from BlockNote/BlockSuite
5. **Feature Flag Flip** — `NEXT_PUBLIC_UI_DESTIJL=true`
6. **Cleanup** — Remove old styles behind flag, remove flag itself
7. **Documentation** — Update component docs, storybook if applicable

### Final Intelligence Wiring Check (Complete 22-Point Checklist)

- [ ] 1. `use-mindrian.ts` byte-identical to main branch
- [ ] 2. `use-mindrian-render.tsx` byte-identical to main branch
- [ ] 3. `use-mindrian-actions.tsx` byte-identical to main branch
- [ ] 4. All 25 agents respond correctly in chat
- [ ] 5. Agent routing selects correct agent for query type
- [ ] 6. 3-layer routing displays correctly in routing panel
- [ ] 7. HSI Semantic Surprise produces results
- [ ] 8. Red Team validation triggers on claims
- [ ] 9. Saturation detection updates section completeness
- [ ] 10. Filing interrupt captures entries from agent responses
- [ ] 11. Data Room entries persist across sessions
- [ ] 12. Cross-section references display bidirectionally
- [ ] 13. Project Map (React Flow) renders all nodes and edges
- [ ] 14. Canvas view renders all Data Room blocks spatially
- [ ] 15. BlockNote chat rendering handles all message types
- [ ] 16. BlockNote Data Room editing saves correctly
- [ ] 17. Tool call cards render inline in chat
- [ ] 18. Confidence scores display for evidence blocks
- [ ] 19. Phase indicator tracks methodology progress
- [ ] 20. Voice input works (if enabled)
- [ ] 21. Authentication flow unaffected (Supabase)
- [ ] 22. No console errors, no React key warnings, no hydration mismatches

---

## Competitive Research Context

Research on 6 platforms informed this plan:

| Platform | What We Learned | What We DON'T Copy |
|----------|----------------|-------------------|
| AFFiNE | Block-based editing, Edgeless canvas | Full Yjs-dependent architecture |
| Logseq | Outliner + graph, bidirectional links | Text-file-first storage model |
| Notion | Block types, database views, templates | Complexity of full database engine |
| Obsidian | Plugin architecture, canvas view | Desktop-first, Electron dependency |
| Tana | Supertags, live queries, structured data | Proprietary lock-in, no self-host |
| Heptabase | Visual-first thinking, card-based canvas | Standalone tool, no AI integration |

**27 action items** distilled from this research are incorporated across Phases 2-5.

**Mindrian's differentiator**: None of these platforms have 25 trained agents, 3-layer routing, HSI discovery, Red Team validation, or saturation detection. We add knowledge structure features (from competitors) WITHOUT losing intelligence features (uniquely ours).

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| BlockNote ↔ CopilotKit state conflict | One-way data flow: CopilotKit → BlockNote (read-only for chat) |
| BlockSuite Yjs sync | Canvas is read-only VIEW, not source. No Yjs needed. |
| Sacred file modification | 22-point checklist after every phase. Byte-identical verification. |
| Feature flag complexity | Single boolean flag, clean conditional rendering |
| Performance regression | Profile before/after each phase. Lazy-load BlockSuite. |
| Mobile layout breaking | Responsive breakpoints defined in Phase 1, tested continuously |

---

## Dependencies

| Package | Version | Purpose | Phase |
|---------|---------|---------|-------|
| `@blocknote/core` | ^0.18 | Block editor core | 3 |
| `@blocknote/react` | ^0.18 | React integration | 3 |
| `@blocknote/mantine` | ^0.18 | Default styling (overridden by De Stijl) | 3 |
| `@blocksuite/blocks` | ^0.17 | Edgeless canvas blocks | 4 |
| `@blocksuite/store` | ^0.17 | Canvas state management | 4 |
| `@blocksuite/lit` | ^0.17 | Edgeless rendering | 4 |

Existing dependencies (already in stack):
- `@copilotkit/react-core`, `@copilotkit/react-ui` — Intelligence layer
- `reactflow` — Project Map graph view
- `@radix-ui/*` — Primitives (tabs, dialogs, tooltips)
- `lucide-react` — Icons
- `tailwindcss` — Styling
