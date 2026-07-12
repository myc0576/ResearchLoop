# MycEvo Diagram Explorations

These artifacts record the OpenDesign exploration stage for the MycEvo GitHub README diagrams. They are design evidence, not production README assets. The final SVGs under `assets/readme/` were rebuilt by Codex as clean native vectors after reviewing these directions.

## Shared brief

- Design system: OpenDesign `warm-editorial`, overridden where necessary by the MycEvo tokens in [`DESIGN.md`](../../../DESIGN.md).
- OpenDesign skill: `frontend-design`.
- Agent: Codex CLI, model `gpt-5.5`.
- Output contract: one self-contained `index.html` per direction, two fixed 1600×900 inline-SVG boards, no remote resources, and stable `#product-board` / `#technical-board` screenshot targets.
- Required semantics: candidate-first workflow memory, evidence gate, human promotion, public/private separation, and a sanitized-only public improvement path.

## 1. Warm Editorial Flow

[Open HTML](warm-editorial-flow/index.html) · [Product preview](warm-editorial-flow/product-preview.png) · [Technical preview](warm-editorial-flow/technical-preview.png)

Uses a field-guide/editorial spread, generous paper-like whitespace, varied document forms, and a dominant terracotta checkpoint.

- Strengths: strongest title treatment; calm brand tone; clear public/private boundary framing.
- Limitations: the exploratory product board crowds the validation/next-paper area; the technical bottom path is visually busy.
- Semantic fit: strong on governance and local/private boundaries, moderate on reduced-scale flow clarity.

## 2. Organic Evidence Network

[Open HTML](organic-evidence-network/index.html) · [Product preview](organic-evidence-network/product-preview.png) · [Technical preview](organic-evidence-network/technical-preview.png)

Uses controlled branching nodes, sage accumulation paths, and terracotta/gold checkpoints to express “evidence grows, governance decides” without literal botanical imagery.

- Strengths: most distinctive MycEvo product metaphor; strongest candidate-versus-reusable state contrast; memorable evidence network.
- Limitations: generated labels overlap in places; the technical network is denser and less linear than the architecture requires.
- Semantic fit: best product-mechanism direction; technically useful mainly for the eight-module workspace relationship.

## 3. Structured Research System

[Open HTML](structured-research-system/index.html) · [Product preview](structured-research-system/product-preview.png) · [Technical preview](structured-research-system/technical-preview.png)

Uses explicit layers, swimlanes, bounded modules, and compact gate stages. Warmth comes from paper, typography, and sparse earth-color accents rather than decorative softness.

- Strengths: clearest technical hierarchy; most accurate agent → access → core → workspace dependency; strongest evolution-gate scanability.
- Limitations: the exploratory source has several long-label overflows; its product direction feels more procedural and less ownable.
- Semantic fit: best technical-architecture direction and strongest auditability.

## Weighted selection

Each score is already weighted to the requested maximum: information accuracy 30, GitHub readability 25, brand distinctiveness 20, visual hierarchy 15, editability 10.

| Direction | Board | Accuracy | Readability | Brand | Hierarchy | Editability | Total |
|---|---|---:|---:|---:|---:|---:|---:|
| Warm Editorial Flow | Product | 28 | 16 | 17 | 11 | 8 | 80 |
| Organic Evidence Network | Product | 29 | 19 | 19 | 11 | 8 | **86** |
| Structured Research System | Product | 29 | 15 | 15 | 14 | 8 | 81 |
| Warm Editorial Flow | Technical | 28 | 16 | 16 | 13 | 8 | 81 |
| Organic Evidence Network | Technical | 28 | 17 | 19 | 11 | 8 | 83 |
| Structured Research System | Technical | 30 | 20 | 16 | 14 | 8 | **88** |

## Final direction

The final product diagram uses Organic Evidence Network for state/growth semantics and Warm Editorial Flow for typography and whitespace. The final technical diagram uses Structured Research System for boundaries and lanes, with the organic direction informing the private workspace module grouping. This is an explicit hybrid rather than a direct export: generated overlap and overflow were removed, all arrows were rebuilt, and light/dark SVGs share identical structure.

OpenDesign run provenance:

- Warm Editorial Flow: `6efe7289-fd32-480b-baa6-cb6b44ec11e0`
- Organic Evidence Network: `b25a8a3c-b417-4f5f-80b5-e3cb86ad531d`
- Structured Research System: `a76b0f21-b55a-4e62-a42d-928bd0c7153a`
