# Figure Intake Workflow

Use this workflow for paper figures, visual layouts, reference styles, and figure ideas that should influence future scientific visualization.

## Rules

- Save useful visual references under `visual_refs/`.
- Every saved visual reference must have a matching `templates/figure_card.md`.
- Paper figure outputs, final panels, editable figure sources, and submission-ready images default to `G:\docs\小论文\<paper_id>`, not `visual_refs/` and not ResearchLoop's local harness directory.
- Do not treat attractive style as scientific evidence.
- Do not publish third-party figures unless rights and citation requirements are satisfied.
- Keep original experimental image data in the project tree, not in `visual_refs/`.
- When a flat visual needs editable outputs, route it through
  `workflows/visual_to_editable/README.md` and
  `scripts/visual_to_editable_router.py` before reconstruction.
- ResearchLoop stores reconstruction prompts, manifests, QA summaries, and
  reproduction notes. It does not store raw screenshots, private experiment
  figures, PDFs, generated PPTX files, or final paper figures.

## Suggested Layout

```text
visual_refs/
  <project_or_topic>/
    README.md
    <YYYYMMDD_short_source_or_style>/
      reference.png
      figure_card.md
```

For copyrighted papers, prefer a small internal reference crop, citation metadata, and a clear note that it is not a release asset.

## Intake Steps

1. Save or reference the visual material in `visual_refs/`.
2. Create a figure card with:
   - source and citation;
   - visual purpose;
   - linked paper claim or figure slot;
   - what to imitate and what not to imitate;
   - release restrictions;
   - reviewer risk.
3. Register the card in `registry/figures.yaml`.
4. If the figure is part of the user's own paper, bind it back to `templates/paper_contract.md` and `templates/evidence_table.md`.
5. If editable reconstruction succeeds, add the reconstruction prompt, output
   manifest, reproduction entry, QA report, and any route-changing decision
   record to closeout.

## Domain Lens

For spray optical tomography figures, the card must say whether the visual is:

- an optical layout;
- a reconstruction pipeline;
- a volume rendering;
- a slice/isosurface comparison;
- a residual or error metric panel;
- a failure-case or uncertainty panel.
