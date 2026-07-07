# Visual-To-Editable Workflow

`visual-to-editable-skills` is a ResearchLoop router and closeout protocol for
turning flat visual material into editable research assets. It is not a
standalone picture-to-PPT tool. It tells an external agent which reconstruction
path to use, what evidence to keep, and what must be written back after a
successful conversion.

ResearchLoop stays the workflow brain:

- no embedded LLM;
- no vendored external skill repositories;
- no raw large images, private experiment figures, PDFs, final paper figures, or
  generated PPTX outputs committed to this repository;
- only templates, manifests, prompts, reproduction notes, QA summaries, and
  sanitized examples are kept here.

## Router Contract

The router reads a request with:

- source path or local-only reference;
- input type;
- visual signals observed by the agent;
- desired editable output types;
- sensitivity and commit policy;
- intended use.

It returns one route:

| Route | Use When | Preferred Outputs |
|---|---|---|
| `scientific_figure_tracing` | Paper or research figure images need editable labels, vectors, or figure-source reconstruction | PPT/SVG/HTML plus figure card |
| `ppt_screenshot_reconstruction` | Slide screenshot, image-based PPTX, or PDF page should become editable PPT | PPTX plus page manifest and render QA |
| `native_chart_rebuild` | Bar/line/scatter chart should become a native chart or plotting source | Native chart, CSV pointer, script |
| `editable_table_rebuild` | Table screenshot should become editable table data | CSV/XLSX/Markdown table/PPT table |
| `flowchart_to_mermaid_svg` | Workflow, pipeline, or process diagram should become Mermaid/SVG | Mermaid, SVG, optional PPT |
| `formula_to_latex_ppt` | Formula screenshot should become LaTeX/PPT equation objects | LaTeX, PPT equation/text objects |
| `ui_to_html_figma_ppt` | UI screenshot or dashboard should become editable UI/design assets | HTML/Figma/PPT layout |
| `manual_review` | Inputs are ambiguous, sensitive, or unsafe for automatic routing | Human route decision |

The deterministic route table lives in
[`router_rules.yaml`](router_rules.yaml).

## Closeout Requirements

Every successful reconstruction must preserve:

- visual reference or figure card;
- reconstruction prompt;
- output manifest;
- reproduction note;
- QA result;
- registry entries;
- decision record when the workflow route, quality standard, or safety boundary
  changed.

Suggested project-local closeout shape:

```text
<project>/research_assets/YYYYMMDD_visual_to_editable_<topic>/
  00_asset_manifest.md
  reproduction_entry.md
  visual_reconstruction_manifest.yaml
  visual_reconstruction_qa.md
  visual_reconstruction_prompt.md
```

Large or private source material stays in the project tree, a secure local
folder, or the external tool work directory. ResearchLoop records references and
QA evidence, not the payload.

## Quality Checks

Minimum QA fields:

- editability score;
- editable text count;
- OCR/text alignment status;
- layout overlap score;
- render-before-after comparison status;
- full-slide background residue flag;
- manual review status.

Accepting an editable reconstruction means the important text, labels, simple
geometry, formulas, or table cells can be selected and edited in the chosen
target format. Complex scientific images may remain image objects, but they must
not retain baked-in labels when the route requires editable annotation.

## Commands

```powershell
python scripts\visual_to_editable_router.py classify --request examples\visual_to_editable_minimal\request.yaml --json
python scripts\visual_to_editable_router.py validate-manifest --manifest examples\visual_to_editable_minimal\visual_reconstruction_manifest.yaml --json
python scripts\visual_to_editable_router.py validate-case --case-dir examples\visual_to_editable_minimal --json
```

Run the usual ResearchLoop gates after adding or changing examples, registries,
or closeout records:

```powershell
python scripts\registry_tool.py validate
python scripts\evaluator.py evaluate --target all --json
python scripts\closeout_check.py
```
