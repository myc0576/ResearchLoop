# Self-Evolution Loop Workflow

This workflow turns G drive closeout into a one-click loop. It is designed for
the trigger family `自进化`, `沉淀`, `更新`, `写回`, `复用`, `调用 harness`,
`closeout`, `loop`, and related phrases.

## Loop Contract

The loop is intentionally small:

```text
recall -> intake -> contract -> candidate writeback -> validation -> next bottleneck
```

- `recall`: search current reusable knowledge, prompts, assets, decisions, and
  backlog before creating new material.
- `intake`: the active Agent writes `templates/self_evolution_intake.yaml` from
  the current task context. The runner does not read chat history directly.
- `contract`: `scripts/self_evolution_loop.py run` copies the intake into
  `runs/YYYYMMDD/<run_id>/` and writes `contract.yaml`.
- `candidate writeback`: automatic writes are limited to `candidate` or
  `pending validation`. Human-only states such as `validated`, `reusable`,
  `approved`, `pass`, and `paper_ready` are never emitted automatically.
- `validation`: run registry and closeout checks after any writeback.
- `next bottleneck`: report the next missing evidence, weak rule, or review
  dependency so the next loop has a concrete target.

## Roles

- Planner: converts a user task into a bounded intake file and names evidence
  paths.
- Generator: runs the deterministic CLI and writes only canonical files.
- Evaluator: reads diffs, registry output, validator output, and trace files.

The same model may perform more than one role, but the artifacts must remain
separate: intake, contract, state, trace, written files, and validation reports.

## Restart Policy

Every run must be restorable from three files in the run directory:

- `contract.yaml`
- `state.json`
- `trace.jsonl`

If a session crashes, run:

```powershell
python G:\BaiduSyncdisk\ResearchLoop\scripts\self_evolution_loop.py resume --run-id <run_id> --json
```

`resume` must not duplicate registry entries. Completed runs are reported as
already complete.

## Candidate-First Policy

The runner may create:

- `G:\knowledge\reusable_knowledge\<category>\<id>.md` with status
  `pending validation`
- `G:\knowledge\reusable_prompts\<category>\<id>.md` with status
  `pending validation`
- `G:\projects\<project>\research_assets\<id>` with status `candidate`
- `G:\BaiduSyncdisk\ResearchLoop\decisions\<id>.md` with status
  `pending validation`
- `registry/workflow_improvement_backlog.yaml` entries with status
  `pending validation`
- visual-to-editable prompts, manifests, QA summaries, and reproduction notes
  with candidate or pending-validation status only

Promotion to `validated`, `reusable`, `approved`, `pass`, or `paper_ready`
requires explicit human review or a separate evidence-backed promotion gate.

## Trace Reading

The evaluator reads `trace.jsonl` before claiming completion. Useful trace
events include:

- `start`
- `recall`
- `validate_intake`
- `snapshot`
- `write_candidate`
- `skip_candidate`
- `validation_step`
- `complete`

If output looks wrong, search the trace for the first point where expected and
actual behavior diverged, then update the intake or runner rule for that exact
moment.

## Subjective Score Rubric

Subjective quality may be scored only when the rubric is written down:

| Axis | Weight | Question |
|---|---:|---|
| usefulness | 0.35 | Will this help a future related G drive task? |
| traceability | 0.25 | Are source paths, commands, and evidence clear? |
| boundary safety | 0.25 | Are claims conservative and statuses non-promoted? |
| retrieval fit | 0.15 | Will recall find this with likely trigger words? |

Scores are advisory. They do not promote candidate material by themselves.

## Trigger Table

Agents should activate recall or self-evolution when the user says any of:

`自进化`, `沉淀`, `更新`, `更新 harness`, `写回`, `写入 harness`, `知识库`,
`复用`, `资产化`, `候选资产`, `经验沉淀`, `closeout`, `harness closeout`,
`调用历史`, `查历史`, `参考之前`, `loop`, `一键 loop`, `retro`,
`写入知识库`, `更新知识库`, `同步 harness`, `沉淀到 harness`.

For visual-to-editable work, the loop should recall router rules, candidate
external skills, figure cards, prompts, and prior QA before adding new assets.
The runner should never copy raw visual payloads into knowledge or promote a
skill candidate solely because a conversion completed.

## Commands

```powershell
python scripts\self_evolution_loop.py recall --query "<task>" --project-root <cwd> --json
python scripts\self_evolution_loop.py init --project-root <cwd> --trigger "自进化" --out <intake.yaml>
python scripts\self_evolution_loop.py run --intake <intake.yaml> --apply-candidates --json
python scripts\self_evolution_loop.py resume --run-id <run_id> --json
```
