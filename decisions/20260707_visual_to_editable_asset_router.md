# Decision Record: Visual-To-Editable Asset Router

```yaml
id: 20260707_visual_to_editable_asset_router
project_id: researchloop
date: 2026-07-07
status: pending validation
allowed_status:
  - validated
  - hypothesis
  - pending validation
changed_route_or_assumption: true
```

## Decision

ResearchLoop will treat visual-to-editable reconstruction as a Figure Loop and
closeout extension, not as a standalone conversion product. The repository owns
the router, manifests, prompts, QA records, examples, registries, and safety
rules. External agents or external skills own the actual reconstruction work.

## Context

The existing Figure Loop already routes visual references through figure cards
and `registry/figures.yaml`. The closeout loop already requires reusable prompts,
research assets, decisions, and registry updates when a task produces reusable
workflow material. Visual reconstruction needs the same discipline because flat
screenshots, PDFs, chart images, formulas, and UI captures can easily become
untraceable binary artifacts.

## Rationale

- A lightweight router preserves ResearchLoop's role as an external workflow
  brain and avoids embedding an LLM or a conversion backend.
- A manifest and QA contract make editable reconstruction auditable: text
  editability, OCR alignment, layout overlap, render comparison, and residual
  full-slide backgrounds can be recorded without committing source binaries.
- Candidate external skill entries allow agents to choose known reconstruction
  tools while keeping third-party code, credentials, and generated payloads
  outside this repository.

## Consequences

- Future Figure Loop closeout can require a reconstruction prompt, manifest,
  reproduction note, QA report, and figure card after a successful editable
  rebuild.
- New skill entries remain `pending validation` until a sanitized real case is
  run and reviewed.
- Raw large images, private experimental figures, PDFs, final submission
  figures, generated PPTX files, and tool traces remain outside ResearchLoop.

## Verification

Planned verification:

- `python scripts\visual_to_editable_router.py validate-case --case-dir examples\visual_to_editable_minimal --json`
- `python scripts\registry_tool.py validate`
- `python scripts\evaluator.py evaluate --target all --json`
- `python scripts\closeout_check.py`

The decision stays `pending validation` until those checks pass in this branch
and at least one real sanitized reconstruction later confirms the QA contract.
