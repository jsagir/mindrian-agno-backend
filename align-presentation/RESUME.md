# ALIGN Minisite — Session Resume Prompt

Copy everything below the line and paste it after restarting Claude Code:

---

## Context: ALIGN Intelligence Responsive Minisite

I'm building a responsive minisite for the ALIGN Intelligence pitch deck. Here's where we are:

### Completed
1. **site.html built** — Full responsive minisite at `/home/jsagi/align-presentation/site.html`
   - 10 sections (Hero, Why IMEC, De-Risking, The Cortex, Forces, Deliverables, Team, Ecosystem, Roadmap, CTA/Close)
   - Sticky nav with hamburger mobile menu
   - Scroll reveal animations (Intersection Observer)
   - All 23 LinkedIn links, 8 partner logos, 4 SVG diagrams, 11 icons, 24 team members
   - Responsive: 375px / 768px / 1200px breakpoints
   - Design system: Navy #0a1628, Gold #c9a84c, Cyan #4fc3f7
   - Fonts: Cormorant Garamond + IBM Plex Sans + IBM Plex Mono

2. **Nano Banana Pro MCP configured** — Added to `.claude.json` with Google AI Studio key

### Next Steps — Generate Visual Assets
Now that Nano Banana Pro MCP is available, generate custom visual assets for the minisite and save them into `/home/jsagi/align-presentation/assets/`. Targets:

1. **Hero background texture** — Dark navy abstract grid/corridor pattern, subtle, for hero section overlay
2. **Section background patterns** — Subtle geometric patterns for alternating sections
3. **Living Organism illustration** — Abstract visualization of skeleton/nervous-system/muscle metaphor
4. **Round Table visual** — Circular/orbital diagram showing ALIGN at center with partner nodes
5. **Convergence graphic** — Three forces merging into one (for Cortex section)
6. **Pipeline sector icons** — Custom icons for the 8 investment sectors if current ones need enhancement
7. **CTA visual** — Premium, institutional-grade graphic for the "Join the Cortex" section

Use `generate_image` from the nanobanana-pro-mcp tools. Save outputs into `assets/backgrounds/`, `assets/photos/`, or `assets/diagrams/` as appropriate. Then update site.html to reference the new assets.

### Key Files
- `/home/jsagi/align-presentation/site.html` — The minisite (single file)
- `/home/jsagi/align-presentation/final.html` — Original 17-slide deck (reference)
- `/home/jsagi/align-presentation/assets/` — All assets directory
- `/home/jsagi/align-presentation/CLAUDE.md` — Project context
