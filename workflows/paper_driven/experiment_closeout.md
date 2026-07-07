# Experiment Closeout Workflow

Run this workflow at the end of every research task, including literature-only, figure-only, code-only, reconstruction, calibration, validation, and writing tasks.

## Closeout Questions

1. Goal alignment
   - Which research goal did this task serve?
   - Did it change the project route, assumption, or system design?
2. Evidence
   - What data, metric, residual, plot, log, or reproduction command exists?
   - Which claim and figure does it support or weaken?
   - What is still missing?
3. Reuse decision
   - Did this produce reusable knowledge?
   - Did this produce a reusable prompt?
   - Did this produce project research assets?
   - Did this reconstruct a flat visual into editable PPT/SVG/HTML/Mermaid/Figma-style assets?
   - Did this require a decision record?
4. Registry update
   - Update `registry/papers.yaml` when a paper contract changes.
   - Update `registry/literature.yaml` when a literature card is created or revised.
   - Update `registry/figures.yaml` when a figure card or visual reference is created.
   - Update `registry/prompts.yaml` for reusable prompt cards.
   - Update `registry/decisions.yaml` for route, claim-boundary, or workflow decisions.

## Sink Rules

- Reusable knowledge goes to `G:\knowledge\reusable_knowledge\<category>`.
- Reusable prompts go to `G:\knowledge\reusable_prompts\<category>`.
- Project research assets go to the current project's `research_assets\YYYYMMDD_task_name`.
- Small-paper正文、图件、投稿文件 go to `G:\docs\小论文\<paper_id>` by default.
- ResearchLoop workflow rules, templates, registries, and decisions stay in `G:\BaiduSyncdisk\ResearchLoop`.
- ResearchLoop stores paper templates, workflows, indexes, registry cards, and decision records only; it is not the manuscript or submission package directory.
- Raw experiment data, PDFs, large binaries, and temporary intermediate outputs are not copied into knowledge.
- Visual-to-editable reconstruction outputs must keep raw source visuals,
  private figures, final submission figures, generated PPTX files, and tool
  traces outside ResearchLoop. Store only local references, prompts, manifests,
  QA summaries, reproduction notes, registry entries, and sanitized examples.

## Status Discipline

- Use `validated` only when evidence exists and can be cited.
- Use `hypothesis` for plausible but unverified scientific statements.
- Use `pending validation` when evidence is planned, partial, or not yet reproduced.
- Keep paper-readiness and approval state human-controlled.
- Do not auto-promote visual-to-editable skill candidates or reconstruction
  manifests to `validated`; promotion requires evidence and human review.
