# MycEvo Diagram Redesign Brief

## Status and scope

- Status: approved implementation brief
- Date: 2026-07-11
- Repository: `myc0576/MycEvo`
- Local checkout: current Git worktree (machine-specific path intentionally omitted)
- Working branch: `design/opendesign-claude-diagrams`
- Design contract: [`DESIGN.md`](../../DESIGN.md)

This task refreshes the GitHub README's product-mechanism and technical-architecture diagrams. It changes visual hierarchy, brand expression, theme behavior, and documentation only. It must not alter the CLI, stdio MCP contract, Python package structure, registry schema, migrations, self-evolution gates, or scientific workflow logic.

## Evidence reviewed

- `README.md` and `README.zh-CN.md`
- `docs/architecture/target-architecture.md`
- `docs/architecture/reference-projects.md`
- `assets/readme/mycevo-product-light.svg`
- `assets/readme/mycevo-product-dark.svg`
- `assets/readme/mycevo-technical-light.svg`
- `assets/readme/mycevo-technical-dark.svg`
- OpenDesign official README, QUICKSTART, AGENTS, package metadata, daemon CLI, and MCP installer sources.

## Current-state audit

The existing SVGs are lightweight, editable 1600×900 assets, but they do not yet form a coherent design system. The light and dark variants remove or merge different information; all primary flows lack arrowheads; validation is not a sufficiently distinct checkpoint; and the technical view does not fully enumerate the private workspace or clearly separate public and private boundaries. At 25% scale, secondary text becomes unreadable. The two dark SVGs also lack complete accessible title/description metadata.

## Brand direction

Use a warm editorial technology style: paper-like neutral fields, generous whitespace, fine borders, light rounding, restrained depth, and a quiet contrast between sage growth nodes and terracotta/gold validation points. The result may share Claude's broad sense of warmth and editorial restraint, but must not copy the Claude/Anthropic logo, trademarked forms, proprietary illustrations, or page layouts.

The diagrams should feel like a serious research tool: organic enough to communicate accumulation and evolution, structured enough to make gates and dependencies auditable.

## Required semantics

### Product mechanism

```text
Real Research Tasks
→ Evidence Capture
→ Candidate Workflow Memory
→ Validation Gate
→ Reusable Workflow
→ Next Paper
→ Feedback Loop
```

The composition must show that every real task creates evidence, experience first becomes a candidate, validation is mandatory, reuse occurs only after the gate, the next paper consumes the reusable workflow, and subsequent work creates new evidence. There is no silent promotion.

Recommended title: `How MycEvo Evolves a Research Workflow`

Recommended subtitle: `Every task creates evidence. Only validated lessons become reusable.`

### Technical architecture

```text
Codex / Claude Code / Cursor
            ↓
CLI / stdio MCP
            ↓
Shared MycEvo Core
            ↓
Private Research Workspace
```

The private workspace must explicitly contain Registry, Retrieval, Provenance, Validators, Claims, Evidence, Artifacts, and Decisions.

The evolution gate is:

```text
Candidate
→ Held-out Validation
→ Evidence Gate
→ Human Promotion
→ Reusable Workflow Memory
```

The public-improvement path is:

```text
Private real-world use
→ Sanitized candidate
→ Validation and review
→ Public MycEvo improvement
```

The visual must distinguish `Public MycEvo Engine` and `Private Research Workspace`, use solid one-way arrows for runtime/dependency relationships, and use a dashed explicitly sanitized path for public improvement. It must never resemble raw private-data upload.

Recommended title: `MycEvo Technical Architecture`

Recommended subtitle: `A local CLI and MCP external brain with evidence-gated evolution`

## Exploration matrix

Create each direction for both diagram subjects under `design/explorations/mycevo-diagrams/`.

1. **Warm Editorial Flow** — horizontal narrative, paper-like card rhythm, strongest README legibility.
2. **Organic Evidence Network** — branching evidence nodes and controlled growth, strongest wood/fire metaphor.
3. **Structured Research System** — bounded layers and swimlanes, strongest technical precision.

Each direction must include a previewable HTML or OpenDesign-native asset, PNG preview, rationale, design-system summary, strengths, limitations, and semantic-fit assessment. Generated exploration HTML must not be copied directly into final README SVG.

## Selection rubric

| Criterion | Weight |
|---|---:|
| Information accuracy | 30% |
| GitHub scale readability | 25% |
| Brand distinctiveness | 20% |
| Visual hierarchy | 15% |
| Editability | 10% |

Scores must be recorded before final SVG implementation. A hybrid is allowed only when the component sources and reasons are explicit.

## Final asset contract

- Four required SVGs at the existing `assets/readme/` paths.
- 1600×900; structural parity across themes.
- Text remains SVG text; vectors remain native primitives.
- No embedded raster/base64 data, remote CSS/font, runtime script, or OpenDesign dependency.
- `<title>`, `<desc>`, `role="img"`, and `aria-labelledby` required.
- No clipping, overlap, incorrect arrows, silent-promotion implication, or private-upload implication.
- README should use theme-aware `<picture>` markup after QA passes.

## QA plan

Rasterize all four SVGs at 1600×900, 800×450, 400×225, and representative GitHub README width. Audit typography, contrast, line weight, icon consistency, arrow direction, semantic completeness, theme parity, and accessible metadata. Record before/after comparisons and known limitations in `docs/design/mycevo-diagram-qa.md`.

## OpenDesign and Codex responsibilities

OpenDesign is an external exploration workspace installed outside this repository. It is used to develop and compare visual directions. Codex translates the selected direction into maintainable native SVG, performs multi-scale QA, updates README references, and records provenance. No OpenDesign dependency or personal absolute path may be committed to MycEvo.

## OpenDesign environment handoff

The external tool checkout is intentionally referenced through `<canonical-tools-root>\open-design`; its machine-specific absolute path is not stored in this repository.

- Official source: `https://github.com/nexu-io/open-design.git`
- Verified commit: `443e31319c954402db1ffb02c41d63db138c854b`
- OpenDesign/daemon version: `0.14.2`
- Required runtime: Node `~24`, pnpm `>=10.33.2 <11`
- Verified runtime: Node `v24.12.0`, Corepack `0.34.5`, pnpm `10.33.2`
- Build verification: `corepack pnpm --filter @open-design/daemon build`
- CLI verification: `node apps\daemon\dist\cli.js --help`
- Daemon binding: loopback only, default port `7456`, browser opening disabled
- Credentials: none added or stored

Native Windows notes:

- `corepack enable` could not write system shims under Program Files, so all pnpm commands were run explicitly through `corepack pnpm` without changing system permissions.
- Electron and Playwright binary downloads were skipped because the daemon/CLI/MCP build does not require the desktop runtime.
- OpenDesign's current `od mcp install codex` executor cannot spawn the local PowerShell Codex shim after its `shell:true` security hardening. The zero-write dry-run remained authoritative; its exact plan was executed with Codex's official `codex.cmd mcp add` command instead of editing configuration files.

The registered server is named `open-design`. Its stdio command uses the absolute Node executable and the verified daemon CLI inside the external checkout, passes `mcp --daemon-url http://127.0.0.1:7456`, sets only `OD_DATA_DIR`, and has no working-directory dependency. Verification uses:

```powershell
codex mcp get open-design
```

Removal uses:

```powershell
codex mcp remove open-design
```

The running Codex App session did not hot-load the newly registered server. Restart Codex, confirm the `open-design` tools are present, and resume at **Exploration matrix**. No OpenDesign-generated exploration or final diagram work is claimed before that restart.
