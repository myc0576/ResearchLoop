# Visual Reconstruction QA: Minimal Flowchart

```yaml
id: 20260707_visual_to_editable_minimal_qa
status: pending validation
selected_route: flowchart_to_mermaid_svg
updated_at: 2026-07-07
```

## Source And Output

- Source reference: `local_only:sanitized_flowchart_placeholder`
- Editable output: `outputs/minimal_flowchart.mmd`, `outputs/minimal_flowchart.svg`
- Manifest: `visual_reconstruction_manifest.yaml`
- Prompt: `visual_reconstruction_prompt.md`

## Editability

- Editability score: 0.90
- Editable text count: 5
- Editable shapes/charts/tables/formulas: Mermaid nodes and SVG text/vector elements
- Remaining raster backgrounds: 0

## OCR And Text Alignment

- OCR/text alignment status: not applicable for text-only fixture
- Missing text: none known
- Extra text: none known
- Font/size issues: not reviewed against a source screenshot

## Layout Comparison

- Layout overlap score: 0.85 placeholder score
- Render-before-after comparison status: text fixture, no source render diff
- Major offsets: none known
- Cropping or overflow: none known

## Background Residue

- Full-slide background residue: false
- Residual baked-in labels: none
- Screenshot-only regions: none

## Manual Review

- Reviewer: pending
- Manual review status: pending
- Required fixes: run against a real sanitized source before promotion
- Promotion decision: keep pending validation

## Evidence

- Commands:
  - `python scripts\visual_to_editable_router.py validate-case --case-dir examples\visual_to_editable_minimal --json`
- Logs: pending validation run
- Render previews: not committed
- Object inventory: Mermaid source and SVG text/vector elements
