# Visual Reconstruction Prompt: Minimal Flowchart

```yaml
id: 20260707_visual_to_editable_minimal_prompt
title: Minimal flowchart to Mermaid/SVG prompt
category: visual_to_editable
source_project: researchloop
status: pending validation
selected_route: flowchart_to_mermaid_svg
model: Codex / Claude Code / Cursor external agent
updated_at: 2026-07-07
```

## Task

Reconstruct a sanitized workflow diagram as editable Mermaid and SVG assets.

## Input

- Source reference: `local_only:sanitized_flowchart_placeholder`
- Input type: `flowchart`
- Visual signals: arrow, node, connector, process_flow
- Sensitivity: sanitized example
- Commit policy: sanitized text only
- Target outputs: Mermaid and SVG

## Output

- `outputs/minimal_flowchart.mmd`
- `outputs/minimal_flowchart.svg`
- `visual_reconstruction_manifest.yaml`
- `visual_reconstruction_qa.md`

## Prompt Body

```text
Convert the referenced workflow diagram into Mermaid first, then export or
hand-author an SVG that preserves the node order and arrow direction. Do not
add new process steps. Do not commit any original screenshot or PDF. Record the
route, output inventory, QA status, and reproduction command.
```

## Model

- Recommended model: Codex / Claude Code / Cursor external agent
- Tested model: not yet run against a real image

## Notes

- Claim boundaries: visual topology only, no scientific claim.
- Safety boundary: no source image is stored in this example.
- Reuse conditions: use as a minimal router and closeout fixture.
- Failure modes: missing arrows, changed node names, or committed source image.

## Revision History

| Date | Change | Reason |
|---|---|---|
| 2026-07-07 | Initial version | Minimal visual-to-editable route example |
