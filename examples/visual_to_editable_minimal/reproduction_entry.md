# Reproduction Entry

## Commands

```powershell
python scripts\visual_to_editable_router.py classify --request examples\visual_to_editable_minimal\request.yaml --json
python scripts\visual_to_editable_router.py validate-manifest --manifest examples\visual_to_editable_minimal\visual_reconstruction_manifest.yaml --json
python scripts\visual_to_editable_router.py validate-case --case-dir examples\visual_to_editable_minimal --json
```

## Expected Result

- The request routes to `flowchart_to_mermaid_svg`.
- The manifest passes required field and safety checks.
- The case has no committed image, PDF, or PPTX binaries.

## Files

- `request.yaml`
- `expected_route.yaml`
- `visual_reconstruction_prompt.md`
- `visual_reconstruction_manifest.yaml`
- `visual_reconstruction_qa.md`
- `figure_card.md`
- `outputs/minimal_flowchart.mmd`
- `outputs/minimal_flowchart.svg`
