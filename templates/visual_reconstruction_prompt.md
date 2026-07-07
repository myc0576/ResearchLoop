# Visual Reconstruction Prompt

```yaml
id: YYYYMMDD_visual_reconstruction_prompt
title: ''
category: visual_to_editable
source_project: ''
status: pending validation
selected_route: ''
model: Codex / Claude Code / Cursor external agent
updated_at: YYYY-MM-DD
```

## Task

Describe the visual-to-editable task and why the source needs editable assets.

## Input

- Source reference:
- Input type:
- Visual signals:
- Sensitivity:
- Commit policy:
- Target outputs:

## Output

- Editable asset types:
- Required manifest:
- Required QA:
- Required closeout files:

## Prompt Body

```text
Reconstruct the referenced visual source as editable assets.

Route: <selected_route>
Do not invent scientific content, data values, labels, formulas, units, or
workflow steps. Preserve the meaning of the source. Keep source images, PDFs,
private experiment figures, final paper figures, and generated PPTX outputs
outside ResearchLoop unless they are explicitly sanitized text examples.

Required deliverables:
- editable output inventory;
- visual reconstruction manifest;
- QA report with editability, OCR/text alignment, layout overlap, render
  comparison, and full-slide background residue checks;
- reproduction note;
- figure card or visual reference card when the result influences Figure Loop.
```

## Model

- Recommended model:
- Tested model:

## Notes

- Claim boundaries:
- Safety boundary:
- Reuse conditions:
- Failure modes:

## Revision History

| Date | Change | Reason |
|---|---|---|
| YYYY-MM-DD | Initial version |  |
