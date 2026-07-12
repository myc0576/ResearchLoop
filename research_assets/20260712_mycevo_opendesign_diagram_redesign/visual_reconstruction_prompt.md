# Visual Reconstruction Prompt

```yaml
id: 20260712_mycevo_opendesign_diagram_redesign_prompt
title: MycEvo README product and technical architecture diagrams
category: visual_to_editable
source_project: mycevo
status: pending validation
selected_route: flowchart_to_mermaid_svg
model: OpenDesign with Codex CLI, followed by Codex native SVG implementation
updated_at: 2026-07-12
```

## Task

Explore and reconstruct the two MycEvo README architecture diagrams as warm, editorial, professional, editable assets without changing their software or research semantics.

## Input

- Source reference: four existing `assets/readme/mycevo-*.svg` files.
- Input type: product workflow and technical architecture diagrams.
- Visual signals: directional arrows, state nodes, validation gates, public/private boundaries, feedback loop, sanitized improvement path.
- Sensitivity: public repository assets.
- Commit policy: sanitized public design artifacts and QA only.
- Target outputs: OpenDesign HTML explorations, PNG previews, and four final native SVGs.

## Output

- Editable asset types: HTML/inline SVG exploration and final standalone SVG.
- Required manifest: `visual_reconstruction_manifest.yaml`.
- Required QA: theme parity, XML structure, multi-scale rendering, contrast, overlap, arrow direction, and semantic checks.
- Required closeout files: prompt, manifest, QA, figure card, reproduction entry, and research asset manifest.

## Prompt Body

```text
Use a Claude-inspired warm editorial technology mood without copying any
Claude or Anthropic mark, trademark, proprietary graphic, or layout.

Product semantics:
Real Research Tasks -> Evidence Capture -> Candidate Workflow Memory ->
Validation Gate -> Reusable Workflow -> Next Paper -> Feedback Loop.
Candidate memory must never appear to promote silently.

Technical semantics:
Codex / Claude Code / Cursor -> CLI / stdio MCP -> Shared MycEvo Core ->
Private Research Workspace. Show eight private modules, the complete
candidate-first evolution gate, and a dashed sanitized-only public improvement
path that cannot be mistaken for raw private data upload.

Generate three independent HTML exploration directions: Warm Editorial Flow,
Organic Evidence Network, and Structured Research System. Keep stable 1600x900
product and technical SVG board IDs. Do not use remote assets, remote fonts,
scripts, gradients, glassmorphism, emoji, or runtime dependencies.

Codex must then rebuild the selected direction as clean native SVG with text,
rect, circle, line, and path primitives; light and dark variants must have
identical information structure. Every visible label and explanatory line must
be bilingual, with concise Simplified Chinese above the English source text.
Keep at least 18px of visual inset between bilingual text and its enclosing
card, and re-render at 1600, 800, 400, and representative GitHub widths to
detect clipping, overlap, or boundary contact.
```

## Model

- Recommended model: OpenDesign `frontend-design` with Codex `gpt-5.5`.
- Tested model: Codex `gpt-5.5` through OpenDesign, then the active Codex session for SVG implementation.

## Notes

- Claim boundaries: visual polish is not scientific validation and cannot alter gate status.
- Safety boundary: no private research data, credentials, external images, or untraceable visual assets.
- Reuse conditions: reuse the design contract and semantic checks for later MycEvo public architecture diagrams.
- Failure modes: generated HTML may overflow; do not promote it directly to README. Rebuild and render-review final SVG.

## Revision History

| Date | Change | Reason |
|---|---|---|
| 2026-07-12 | Added Chinese-first bilingual and safe-inset requirements | Prevent text overflow and make both READMEs independently readable. |
| 2026-07-12 | Initial version | Record the OpenDesign-to-native-SVG reconstruction workflow. |
