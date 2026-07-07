# Figure Card: Minimal Visual-To-Editable Flowchart

```yaml
id: fig_20260707_visual_to_editable_minimal_flowchart
title: Minimal visual-to-editable flowchart route example
source_project: researchloop
status: pending validation
figure_type: visual_to_editable_workflow_example
visual_ref_dir: G:\BaiduSyncdisk\ResearchLoop\examples\visual_to_editable_minimal
claim_id: visual_to_editable_example_no_scientific_claim
paper_id: ''
updated_at: 2026-07-07
```

## Source

- Own project output or external reference: ResearchLoop sanitized text fixture
- Citation or source path: `examples/visual_to_editable_minimal/request.yaml`
- Rights/release note: no third-party image or paper figure is included

## Visual Purpose

Show how a flat workflow diagram request is routed to Mermaid/SVG editable
assets and closed out with prompt, manifest, reproduction note, and QA result.

## Evidence Use

| Claim/Figure Slot | Evidence Role | Data/Code Path | Validation Status |
|---|---|---|---|
| visual_to_editable_example_no_scientific_claim | workflow example only | `scripts/visual_to_editable_router.py` | pending validation |

## What To Imitate

- Route selection based on input type plus visual signals.
- Manifest-first closeout.
- Text-only sanitized example payload.

## What Not To Imitate

- Do not store raw screenshots or final paper figures in ResearchLoop.
- Do not treat this minimal fixture as proof of real reconstruction quality.

## Reviewer Risk

- The example is intentionally synthetic and must not be promoted as a validated reconstruction backend.

## Linked Files

- visual reference: `examples/visual_to_editable_minimal/request.yaml`
- figure output: `examples/visual_to_editable_minimal/outputs/minimal_flowchart.svg`
- caption draft: not applicable
