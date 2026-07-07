# Visual-To-Editable Minimal Example

This example demonstrates a safe text-only visual-to-editable closeout. The
source is a sanitized placeholder for a workflow diagram. No original image,
PDF, PPTX, private figure, or final paper figure is committed.

Expected route:

```text
flowchart_to_mermaid_svg
```

Validation:

```powershell
python scripts\visual_to_editable_router.py classify --request examples\visual_to_editable_minimal\request.yaml --json
python scripts\visual_to_editable_router.py validate-case --case-dir examples\visual_to_editable_minimal --json
```
