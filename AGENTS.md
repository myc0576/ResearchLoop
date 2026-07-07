# ResearchLoop Agent Instructions

ResearchLoop 是 paper-driven research 的本地工作流底座，不是普通知识库，也不是又一个 AI agent。它负责跨项目沉淀 reusable knowledge、reusable prompts、figure/research assets、decision records 和 feedback loops。

项目品牌名和当前 canonical 本地入口都是 ResearchLoop：`G:\BaiduSyncdisk\ResearchLoop`。历史名称 `research-harness` 只作为旧路径或兼容性标识出现，不再作为推荐工作目录。

当前主科研项目是：

```text
G:\projects\SC-NMT
```

旧体系 `G:\知识库\_harness` 已迁移为 canonical harness 中的 candidate assets 和 legacy cleanup report；不要重建该目录，不要把它作为写入目标。

## Canonical ResearchLoop Path

在 `G:\` 工作区内，用户说“沉淀到 harness”“写入 harness”“更新 harness”“harness closeout”时，默认且唯一的写入目标是：

```text
G:\BaiduSyncdisk\ResearchLoop
```

不要把 `harness` 解析为 `G:\knowledge\_harness`。该路径属于废弃/歧义路径，不是本工作区的写入目标。

`G:\知识库\_harness` 也不是写入目标。若历史 memory、旧会话或其他项目说明提到 `_harness`，必须先按本节规则纠偏，再继续执行；旧目录内容以 `reports\legacy_cleanup\20260626_zhishiku_harness_inventory.md` 和 `registry\asset_evolution.yaml` 中的 candidate seed 为准。

知识库写入目标只有：

```text
G:\knowledge\reusable_knowledge
G:\knowledge\reusable_prompts
```

项目素材写入当前项目的 `research_assets\YYYYMMDD_task_name`。ResearchLoop 规则、skills、templates、reports、registries、decisions 只写入 `G:\BaiduSyncdisk\ResearchLoop`。

## Task Closeout

每次完成 SC-NMT 或其他科研项目任务后，必须执行 task closeout。只有当任务确实产生可复用内容、证据、素材或路线变化时，才写入对应沉淀文件；不要为了整理而整理。

## Visual-To-Editable Skills

`visual-to-editable-skills` 是 Figure Loop 和 research asset closeout 的扩展，不是独立图片转 PPT 工具。它负责把图片、截图、PDF、图表、科研图、流程图、公式图、UI 图等不可编辑视觉输入路由到可编辑 PPT/SVG/HTML/Mermaid/Figma 风格资产的工作流。

标准入口：

```powershell
python G:\BaiduSyncdisk\ResearchLoop\scripts\visual_to_editable_router.py classify --request <request.yaml> --json
python G:\BaiduSyncdisk\ResearchLoop\scripts\visual_to_editable_router.py validate-manifest --manifest <visual_reconstruction_manifest.yaml> --json
python G:\BaiduSyncdisk\ResearchLoop\scripts\visual_to_editable_router.py validate-case --case-dir <case_dir> --json
```

ResearchLoop 只保存 router、模板、manifest、prompt、QA、registry 和脱敏示例；不内置 LLM，不 vendor 外部转换项目，不提交原始大图、私密实验图、最终投稿图、PDF、生成 PPTX、大文件或工具 trace。实际重建由 Codex、Claude Code、Cursor 或外部 skill 执行。

每次成功重建后，必须沉淀：

- visual reference 或 figure card；
- reconstruction prompt；
- output manifest；
- reproduction note；
- QA result；
- registry 更新；
- 如果改变路线、标准或安全边界，补 decision record。

## One-Click Self-Evolution

当用户在 `G:\` 工作区任务中说 `自进化`、`沉淀`、`更新`、`更新 harness`、`写回`、`写入 harness`、`知识库`、`复用`、`资产化`、`候选资产`、`经验沉淀`、`closeout`、`harness closeout`、`调用历史`、`查历史`、`参考之前`、`loop`、`一键 loop`、`retro`、`写入知识库`、`更新知识库`、`同步 harness` 或 `沉淀到 harness` 时，先走 self-evolution loop，而不是只做口头总结。

标准入口：

```powershell
python G:\BaiduSyncdisk\ResearchLoop\scripts\self_evolution_loop.py recall --query "<当前任务>" --project-root <当前项目路径> --json
python G:\BaiduSyncdisk\ResearchLoop\scripts\self_evolution_loop.py init --project-root <当前项目路径> --trigger "自进化" --out <intake.yaml>
python G:\BaiduSyncdisk\ResearchLoop\scripts\self_evolution_loop.py run --intake <intake.yaml> --apply-candidates --json
python G:\BaiduSyncdisk\ResearchLoop\scripts\self_evolution_loop.py resume --run-id <run_id> --json
```

Agent 负责把当前对话、改动、证据和验证结果整理成 `templates\self_evolution_intake.yaml`；runner 负责候选写回、registry 更新、trace/state/contract 落盘和验证。自动写回只允许 `candidate` 或 `pending validation`；不得自动晋升为 `validated`、`reusable`、`approved`、`pass` 或 `paper_ready`。

1. Goal alignment

   - 本次任务服务于哪个 research goal？
   - 是否改变 project route、assumption 或 system design？

2. Process review

   - 输入是什么？
   - 执行了什么流程？
   - 输出了什么结果？
   - 哪些 code、config、prompt、workflow 可复用？

3. Verification

   - 是否有指标、残差、相关系数、对比图、运行日志或复现命令？
   - 未验证结论必须标记为 `hypothesis` 或 `pending validation`。

4. Knowledge capture

   - 若产生可复用知识，写入 `G:\knowledge\reusable_knowledge\对应分类`。
   - 使用 `templates\knowledge_card_template.md`。
   - 只保存结论、适用条件、步骤、关键参数、风险、验证依据。

5. Prompt capture

   - 若产生可复用 Prompt，写入 `G:\knowledge\reusable_prompts\对应分类`。
   - 使用 `templates\prompt_card_template.md`。
   - 必须记录 task、input、output、prompt body、model、notes、revision history。

6. Research asset harvest

   - 若产生可用于 GitHub、Douyin、article、paper figure、PPT 的原始素材，写入当前项目 `research_assets\YYYYMMDD_task_name`。
   - 不需要精修，只保留原始素材、说明和复现入口。
   - 必须生成 `00_asset_manifest.md` 和 `reproduction_entry.md`。

7. Registry update

   - 更新 `registry\knowledge.yaml`。
   - 更新 `registry\prompts.yaml`。
   - 更新 `registry\research_assets.yaml`。
   - 若有路线变化，更新 `registry\decisions.yaml`。

## Forbidden Actions

- 不移动旧项目。
- 不删除旧文件。
- 不复制原始实验大数据到 knowledge。
- 不把临时垃圾文件沉淀为知识。
- 不把未经验证的判断写成确定结论。
- 不把所有内容都塞进 knowledge。
- 不为了整理而整理。

## Operating Notes

- 文件名和目录名使用英文；文件内容可以使用中文简体。
- 沉淀内容必须可追溯到任务、输入、输出和验证证据。
- `validated` 只用于已有明确验证证据的内容。
- `hypothesis` 用于合理但尚未验证的判断。
- `pending validation` 用于需要后续指标、图像、日志或复现命令确认的内容。
- 大文件、原始实验数据和生成中间垃圾文件留在项目或数据目录，不进入 `G:\knowledge`。

## G Drive Workspace Closeout

ResearchLoop 适用于整个 `G:\` 科研工作区，不只适用于 `G:\projects\SC-NMT`。

每次在 `G:\` 下完成任务并准备最终回复前，必须执行 workspace closeout 检查：

- 如果产生可复用 knowledge，写入 `G:\knowledge\reusable_knowledge\<category>` 并更新 `registry\knowledge.yaml`。
- 如果产生可复用 prompt，写入 `G:\knowledge\reusable_prompts\<category>` 并更新 `registry\prompts.yaml`。
- 如果产生项目素材、脚本、报告、图、PPT、CAD 文件、日志或复现入口，写入当前项目 `research_assets\YYYYMMDD_task_name` 的 manifest/reproduction entry，并更新 `registry\research_assets.yaml`。
- 如果产生可编辑化视觉资产，必须记录 visual reconstruction manifest、prompt、QA 和 reproduction entry；只保存脱敏文本示例或本地路径引用。
- 如果改变路线、假设、设计标准或 closeout 规则，写入 decision record 并更新 `registry\decisions.yaml`。
- 如果没有可沉淀内容，最终回复必须明确说明：`closeout checked: no reusable assets`。

非 SC-NMT 项目的当前项目优先取最近的 `G:\projects\<project_name>` 目录；找不到项目目录时使用 `g-workspace`。二进制大文件、原始实验大数据、CAD 二进制、模型权重和临时文件不得复制到 `G:\knowledge`，只在 manifest 中引用其原始项目路径。
