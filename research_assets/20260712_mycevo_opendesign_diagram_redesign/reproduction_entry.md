# Reproduction Entry

## Commands

```powershell
python scripts\visual_to_editable_router.py classify --request research_assets\20260712_mycevo_opendesign_diagram_redesign\request.yaml --json
python scripts\visual_to_editable_router.py validate-manifest --manifest research_assets\20260712_mycevo_opendesign_diagram_redesign\visual_reconstruction_manifest.yaml --json
python scripts\visual_to_editable_router.py validate-case --case-dir research_assets\20260712_mycevo_opendesign_diagram_redesign --json
python scripts\registry_tool.py validate
git diff --check
```

## Expected Result

- Router selects `flowchart_to_mermaid_svg` for workflow-diagram input and SVG/HTML targets.
- Manifest and closeout case pass safety and required-field validation.
- Four final SVGs parse as 1600×900 XML with accessible metadata.
- Every visible SVG text block contains paired Simplified Chinese and English spans, with Chinese above English.
- Device-scaled Chrome renders cover 1600×900, 800×450, 400×225, and 840×472 without clipping or boundary contact.
- No external asset, remote font, base64 image, script, or OpenDesign runtime is embedded.
- Registry state remains `pending validation` until human approval.

## Files

- `request.yaml`
- `expected_route.yaml`
- `visual_reconstruction_prompt.md`
- `visual_reconstruction_manifest.yaml`
- `visual_reconstruction_qa.md`
- `figure_card.md`
- `00_asset_manifest.md`
- final outputs under `assets/readme/`
- rendered QA under `docs/design/previews/qa/`
