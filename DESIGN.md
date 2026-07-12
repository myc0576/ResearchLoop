# MycEvo Design

## Source of truth

- Status: Active
- Last refreshed: 2026-07-11
- Primary product surfaces: GitHub README architecture diagrams, design documentation, and project-facing visual assets.
- Evidence reviewed: `README.md`, `README.zh-CN.md`, `docs/architecture/`, the four `assets/readme/mycevo-*.svg` files, and the repository guidance files.

This document governs MycEvo's public visual language. It does not change the software architecture, CLI, MCP schema, registries, migrations, self-evolution gates, or scientific logic.

## Brand

- Personality: warm, editorial, rational, restrained, local-first, and scientifically credible.
- Trust signals: explicit evidence paths, visible validation gates, human promotion, provenance, and clear public/private boundaries.
- Avoid: copied third-party marks; literal fungi, trees, flames, or biological claims; neon blue-purple cyber aesthetics; glassmorphism; high-saturation red/green fields; decorative complexity that obscures workflow semantics.
- Inspiration boundary: Claude-inspired warmth and editorial restraint are mood references only. Do not copy Anthropic/Claude logos, proprietary shapes, page compositions, or trademarked assets.

## Product goals

- Make evidence-governed workflow evolution understandable at GitHub README scale.
- Make candidate-first status and the absence of silent promotion visually unavoidable.
- Distinguish the public MycEvo engine from the private research workspace without implying private-data upload.
- Keep final diagrams editable, theme-aware, accessible, and maintainable as native SVG.
- Non-goals: redesigning product behavior, inventing architecture, embedding OpenDesign runtime output, or turning MycEvo into an agent or design tool.
- Success signals: accurate arrow direction, readable main flow at 25% scale, equivalent light/dark information structure, and no ambiguous promotion or data-sharing path.

## Personas and jobs

- Primary personas: researchers evaluating MycEvo, maintainers reviewing architecture, and agent-tool users integrating CLI/MCP workflows.
- User jobs: understand the product loop quickly; verify governance boundaries; see where evidence, validation, human judgment, and reuse occur; assess local/private data handling.
- Key context: GitHub README on light and dark themes, often viewed at roughly 700–900 px content width.

## Information architecture

- Product mechanism: Real Research Tasks → Evidence Capture → Candidate Workflow Memory → Validation Gate → Reusable Workflow → Next Paper → Feedback Loop.
- Technical stack: external agents → CLI/stdio MCP → Shared MycEvo Core → Private Research Workspace.
- Evolution gate: Candidate → Held-out Validation → Evidence Gate → Human Promotion → Reusable Workflow Memory.
- Public improvement: Private real-world use → Sanitized candidate → Validation and review → Public MycEvo improvement.
- Content hierarchy: title and proposition; primary path; state/gate explanation; boundary note or feedback path.

## Design principles

1. Semantics before decoration: every line, color, and container must have an architectural meaning.
2. Growth with governance: organic paths may suggest learning, but gates and state changes remain explicit.
3. Warm credibility: paper-like neutrals and restrained earth colors should feel considered, not nostalgic or ornamental.
4. Boundary clarity: public/private and candidate/reusable distinctions must survive grayscale and reduced scale.
5. Theme equivalence: light and dark variants use the same layout, labels, and relationships; only tokens change.

## Visual language

- Light color tokens: Warm Cream `#F7F3EA`, Paper White `#FFFDF8`, Terracotta `#D97757`, Deep Charcoal `#2F2A26`, Sage Green `#68775A`, Forest Green `#405A47`, Warm Border `#D9CEC2`, Muted Text `#746B63`, Soft Gold `#C99A4A`.
- Dark color tokens: Background `#211F1C`, Card `#2B2824`, Terracotta `#E58A68`, Sage `#879879`, Primary Text `#F6F0E7`, Muted Text `#BDB3A8`, Border `#4A433C`.
- Typography: `Inter, Arial, system-ui, sans-serif`; Chinese fallback `Noto Sans SC, Microsoft YaHei, PingFang SC, sans-serif`. No font installation or remote font reference.
- Spacing/layout rhythm: generous outer margins, compact semantic clusters, and a consistent 8 px-derived rhythm.
- Shape/radius/elevation: light rounded corners, thin warm borders, and subtle restrained shadows; gates may use a stronger outline.
- Motion: none in README SVGs.
- Imagery/iconography: consistent native linear SVG icons; no emoji, raster images, remote assets, or literal tree/fire illustrations.
- Metaphor: sage branching nodes suggest wood/growth; terracotta and soft-gold checkpoints suggest heat/verification.

## Components

- Stage node: icon, eyebrow/status, primary label, and optional short note.
- Validation gate: visually dominant checkpoint with terracotta/soft-gold emphasis.
- State token: candidate uses neutral/light terracotta; validated/reusable uses forest/sage.
- Boundary container: explicit `Public MycEvo Engine` and `Private Research Workspace` labels.
- Flow connector: solid directional arrow for runtime/dependency; thin curved arrow for feedback; dashed directional arrow for sanitized public improvement.
- Legend/note: only when it clarifies status or privacy semantics at README scale.
- Token/component ownership: the final SVGs own their embedded color variables and native vector primitives; no external runtime.

## Accessibility

- Target: WCAG AA contrast for essential text and structural lines where practical.
- Each final SVG must include `<title>`, `<desc>`, `role="img"`, and `aria-labelledby`.
- Do not rely on color alone: candidate, validation, human review, and reusable states also use labels, icons, borders, or shapes.
- Minimum readable type is sized for 1600×900 source and audited at 800, 400, and README content widths.
- Arrowheads and line weight must remain visible at 25% scale.

## Responsive behavior

- Canonical canvas: 1600×900.
- GitHub rendering: one diagram per content column, with light/dark sources selected through `<picture>`.
- Layout does not reflow inside SVG; reduced-size QA determines whether secondary copy must be shortened.
- Light and dark diagrams remain structurally identical.

## Interaction states

These README assets are static. State is communicated semantically:

- Candidate: captured but not promoted.
- Validation: held out and evidence checked.
- Human decision: separate and explicit.
- Reusable: available only after gate completion.
- Failure/blocked: not represented as promotion; explanatory copy must preserve the candidate state.

## Content voice

- Tone: precise, calm, evidence-led, and non-promotional.
- README diagrams use a strict bilingual hierarchy: concise Simplified Chinese first, English second, stacked within the same text block.
- Every visible English label or explanatory line has a Chinese counterpart; agent product names remain unchanged but receive a Chinese role label above them.
- Bilingual nodes retain at least 18px of visual inset from their enclosing boundary at the 1600×900 source size.
- Use MycEvo terms exactly: `candidate`, `held-out validation`, `evidence gate`, `human promotion`, and `reusable workflow memory`.
- Never imply automatic promotion, private-data publication, scientific proof from visual polish, or an embedded LLM/agent.

## Implementation constraints

- Final assets are clean native SVG with editable `<text>`, `<path>`, `<rect>`, `<circle>`, and related primitives.
- No base64 images, external CSS, remote fonts, OpenDesign runtime, or untraceable assets.
- Exploration HTML/PNG is design evidence, not the final README implementation.
- SVG variants must pass XML parsing, structural checks, text-overflow review, and multi-scale raster QA.
- Changes stay within design/docs/README/closeout surfaces; code and scientific behavior are out of scope.

## Open questions

- [x] Product diagram uses Organic Evidence Network semantics with Warm Editorial typography and spacing.
- [x] Technical diagram uses Structured Research System boundaries with restrained evidence-network grouping.
- [x] All four light/dark assets use the same Chinese-first, English-second bilingual information structure.
