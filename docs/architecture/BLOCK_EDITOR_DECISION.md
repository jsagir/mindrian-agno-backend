# Architecture Decision Record: Block Editor Selection

**ADR-001**: BlockNote for Text Editing + BlockSuite Edgeless for Spatial Canvas
**Date**: 2026-02-19
**Status**: Accepted
**Branch**: `ui/destijl-rebuild`

---

## Context

Mindrian V2 needs block-based editing for two distinct use cases:

1. **Rich text editing** — Chat message rendering and Data Room entry editing
2. **Spatial canvas** — A visual/spatial arrangement of Data Room blocks (like a whiteboard)

The current stack uses CopilotKit for state management, React Flow for graph visualization, and plain React components for text rendering. We need to choose block editor(s) that integrate with this stack without breaking the intelligence layer.

### Constraints

- **CopilotKit is the state authority** — Any editor must receive data FROM CopilotKit, not manage its own state independently
- **React-native integration** — Must work within Next.js App Router, React 18+
- **Sacred files untouched** — `use-mindrian.ts`, `use-mindrian-render.tsx`, `use-mindrian-actions.tsx` cannot be modified
- **25 agents produce content** — The editor must handle diverse output formats (text, evidence blocks, tool calls, LaTeX, tables)
- **Dark-first De Stijl theming** — Must be fully themeable with custom colors, no border-radius, Mondrian aesthetics

---

## Options Evaluated

### Option A: BlockNote Only

**@blocknote/react** — React-native block editor, 143K weekly downloads.

| Pros | Cons |
|------|------|
| Pure React, excellent Next.js integration | No spatial/canvas mode |
| Already partially integrated in feature branch | Limited to linear document editing |
| Simple API, custom block types | No whiteboard/Edgeless equivalent |
| Active development, growing ecosystem | |
| 143K downloads/week = strong community | |

### Option B: BlockSuite Only

**@blocksuite** — Full editor framework with Doc mode + Edgeless (canvas) mode.

| Pros | Cons |
|------|------|
| Both text AND canvas in one framework | @blocksuite/react is deprecated and removed |
| Edgeless mode is unique — no React equivalent | Lit-based, not React-native |
| Used by AFFiNE (proven at scale) | Yjs-dependent — conflicts with CopilotKit state model |
| Rich block types out of the box | Complex integration with React |
| | Theming requires deep CSS override |

### Option C: Plate.js Only

**@udecode/plate** — Slate.js-based rich text editor, React-native.

| Pros | Cons |
|------|------|
| Pure React (Slate.js foundation) | No spatial/canvas mode |
| Highly modular plugin system | More complex API than BlockNote |
| Active development (v52+) | Heavier bundle for basic use cases |
| Uses @dnd-kit (already in stack) | Less opinionated = more setup work |

### Option D: BlockNote + BlockSuite Edgeless (Selected)

Hybrid approach: BlockNote for all text editing, BlockSuite Edgeless ONLY for the spatial canvas view.

| Pros | Cons |
|------|------|
| Best text editor (BlockNote) + best canvas (Edgeless) | Two editor dependencies |
| Canvas is read-only from state — no Yjs sync needed | Must maintain adapter between data models |
| Each tool does exactly what it's best at | Larger total bundle size |
| Eliminates the hardest problem (Yjs ↔ CopilotKit) | |
| BlockNote is React-native, Edgeless is isolated | |

---

## Decision

**Option D: BlockNote + BlockSuite Edgeless**

### Rationale

The key insight: **the canvas is a VIEW, not a SOURCE**.

In the traditional BlockSuite architecture (as used in AFFiNE), Edgeless mode is bidirectional — you edit in the canvas and changes flow back to the document. This requires Yjs for conflict-free state sync, which directly conflicts with CopilotKit's state management model.

By making the canvas **read-only** — it renders Data Room blocks in spatial positions but does NOT modify their content — we get the visual benefit of BlockSuite Edgeless without the state sync complexity.

```
Data Flow:

                CopilotKit State
                (source of truth)
                       │
           ┌───────────┼───────────┐
           │           │           │
           ▼           ▼           ▼
      BlockNote    React Flow   BlockSuite
      (chat +      (graph       Edgeless
       editing)     view)       (canvas view)
           │                       │
           │                       │ (read-only)
           ▼                       │
      CopilotKit              Position data
      Actions                  only stored
      (writes)                (not content)
```

### Why Not Full BlockSuite?

1. **@blocksuite/react is dead** — The React wrapper was deprecated and removed from the package. Integration requires raw Lit web components.
2. **Yjs dependency** — BlockSuite's Doc mode requires Yjs for state management. CopilotKit uses its own state model. Running both creates dual-source-of-truth problems.
3. **Theming complexity** — BlockSuite's Doc mode theming requires deep CSS shadow DOM piercing, while BlockNote exposes a clean React theming API.

### Why Not Plate.js?

1. **BlockNote is already partially integrated** — A feature branch has BlockNote work in progress
2. **Simpler API** — BlockNote's `createReactBlockSpec` is more straightforward than Plate's plugin system for our custom block types
3. **Lower setup cost** — BlockNote works out of the box; Plate requires extensive plugin configuration
4. **Community momentum** — 143K downloads/week vs Plate's more fragmented ecosystem

### Why Not BlockNote Only (No Canvas)?

The spatial canvas view is a key differentiator identified in competitive research. AFFiNE's Edgeless mode and Heptabase's card canvas demonstrate that spatial arrangement of ideas significantly enhances thinking. No React-native equivalent to BlockSuite Edgeless exists.

---

## Implementation Details

### BlockNote Usage

**Chat rendering** (read-only):
```tsx
<BlockNoteView editor={chatEditor} editable={false} theme={deStijlTheme} />
```
- Editor receives content from CopilotKit message state
- Custom blocks: Evidence, Claim, Challenge, AgentAction, ToolCall
- Theme: De Stijl (no rounded corners, section colors, Mondrian borders)

**Data Room editing** (editable):
```tsx
<BlockNoteView editor={entryEditor} editable={true} theme={deStijlTheme} />
```
- Editor loads from `DataRoomBlock.content` (BlockNote JSON)
- On change: writes via `use-mindrian-blocks.tsx` (NEW hook, not existing actions)
- Custom blocks same as chat

### BlockSuite Edgeless Usage

**Canvas view** (read-only spatial):
```tsx
<EdgelessEditor surface={surface} readonly={true} />
```
- Surface elements generated from `DataRoomBlock[]` via adapter
- Spatial positions stored separately (not in block content)
- Click on canvas block → opens detail in list view
- De Stijl styling: rectangular blocks, section color borders, straight connection lines

### Packages

| Package | Version | Size Impact | Usage |
|---------|---------|-------------|-------|
| `@blocknote/core` | ^0.18 | ~150KB gzipped | Core editor |
| `@blocknote/react` | ^0.18 | ~30KB gzipped | React bindings |
| `@blocknote/mantine` | ^0.18 | ~20KB gzipped | Base styles (overridden) |
| `@blocksuite/blocks` | ^0.17 | ~200KB gzipped | Edgeless blocks |
| `@blocksuite/store` | ^0.17 | ~80KB gzipped | Canvas state |
| `@blocksuite/lit` | ^0.17 | ~50KB gzipped | Rendering |

**Total additional bundle**: ~530KB gzipped (acceptable for a desktop-focused app)

**Mitigation**: BlockSuite is lazy-loaded (only loaded when canvas tab is opened).

---

## Consequences

### Positive

- Clean separation of concerns: text editor vs spatial canvas
- No Yjs ↔ CopilotKit state conflict
- BlockNote's React integration is seamless with existing stack
- Canvas as read-only view simplifies architecture significantly
- Each tool does exactly one thing well

### Negative

- Two editor dependencies increase bundle size
- Must maintain adapter layer between data models
- BlockSuite upgrades may break the Edgeless API (less stable than BlockNote)
- Team must understand two editor APIs

### Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| BlockNote API breaking change | Low | Medium | Pin to specific version, test on upgrade |
| BlockSuite Edgeless API instability | Medium | Medium | Isolate behind adapter, lazy-load, can remove if needed |
| Performance with many blocks | Low | High | Virtualize lists, limit canvas to 200 blocks |
| Theming drift between editors | Low | Low | Shared CSS custom properties, single source of truth |

---

## Alternatives Rejected

| Alternative | Reason for Rejection |
|------------|---------------------|
| Tiptap | Less opinionated than BlockNote, more setup required, comparable features |
| Lexical (Meta) | Low-level, would require building block UI from scratch |
| Prosemirror (raw) | Even lower-level than Lexical, inappropriate for our timeline |
| Excalidraw | Already in stack for canvas but not block-aware, hand-drawn aesthetic conflicts with De Stijl |
| Custom canvas (HTML Canvas) | Massive development effort, no block awareness |
| React Flow for canvas | Already used for graph view, node-based not block-based, different UX paradigm |

---

## Review

This decision should be revisited if:
1. BlockNote drops React support or is abandoned
2. BlockSuite releases a stable React wrapper
3. A new editor emerges that does both text AND canvas natively in React
4. CopilotKit adds native block editor integration
5. Performance issues require consolidating to a single editor
