# MycEvo MCP

本目录提供本地 stdio MCP 服务，用于让 Codex、Claude Code 等外部 Agent 访问当前 workspace 的检索、健康状态和候选反馈记录。

## Tools

- `search_kb(query, limit)`：查询 SQLite FTS5 知识索引。
- `search_knowledge(query, limit)`：按 utility metadata 和证据等级排序的知识检索。
- `search_workflows(query, limit)`：按证据和复用效用排序的 workflow/decision/asset 检索；无可靠结果返回 `reuse: null`。
- `read_kb_doc(path)`：读取白名单内文档。
- `get_closeout_health()`：读取最新 closeout health。
- `get_project_health(project_id?)`：读取项目级体检。
- `list_proposals(status?)`：列出 evolution proposals。
- `record_feedback(target_id, feedback_type, note)`：唯一写接口，只写 `registry\feedback.yaml` 并追加 ledger。
- `list_candidates()`、`create_intake()`、`run_closeout()`、`propose_workflow_change()`：调用共享 CLI/service 层，自动写回保持 candidate-first。

Self-evolution 的写入入口不是 MCP，而是可审计 CLI：

```powershell
mycevo recall --query "<task>" --project-root <cwd>
mycevo intake --project-root <cwd> --trigger "closeout" --out <intake.yaml>
```

MCP 继续负责检索和健康状态读取；候选写回必须通过 CLI 留下 `contract.yaml`、`state.json` 和 `trace.jsonl`。

## Boundary

- 不依赖 OpenViking。
- 不需要网络。
- 不提供任意文件写入。
- 不写入 workspace 之外的知识库路径。
- 不通过 MCP 自动提升 `candidate` / `pending validation` 为 `validated` 或 `reusable`。

## Self Test

```powershell
mycevo mcp self-test
```
