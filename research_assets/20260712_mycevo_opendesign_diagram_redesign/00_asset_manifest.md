# Research Asset Manifest

```yaml
id: 20260712_mycevo_opendesign_diagram_redesign
project_id: mycevo
task_name: opendesign_readme_diagram_redesign
status: pending validation
allowed_status:
  - validated
  - hypothesis
  - pending validation
created_at: 2026-07-12
```

## 素材清单

| File | Type | Purpose | Notes |
|---|---|---|---|
| `assets/readme/mycevo-product-light.svg` | editable SVG | README 双语产品机制图 | 浅色主题，中文在上、英文在下 |
| `assets/readme/mycevo-product-dark.svg` | editable SVG | README 双语产品机制图 | 深色主题，同构 |
| `assets/readme/mycevo-technical-light.svg` | editable SVG | README 双语技术架构图 | 浅色主题，中文在上、英文在下 |
| `assets/readme/mycevo-technical-dark.svg` | editable SVG | README 双语技术架构图 | 深色主题，同构 |
| `design/explorations/mycevo-diagrams/` | HTML + PNG previews | OpenDesign 三方向探索证据 | 不作为最终 SVG |
| `docs/design/mycevo-diagram-qa.md` | QA report | 设计选择与多尺度审计 | 人工批准前 pending validation |

## 来源路径

- Source files: previous committed `assets/readme/mycevo-*.svg`, `README.md`, `README.zh-CN.md`, `docs/architecture/`.
- Derived files: OpenDesign exploration HTML, preview PNGs, final native SVGs, and multi-scale QA renders.

## 用途

- GitHub: README 产品与技术架构说明。
- Douyin: 不适用。
- Article: 可作为 MycEvo 架构说明素材。
- Paper figure: 不作为科学论文证据图。
- PPT: 可引用 SVG，但应保留候选/门禁语义。

## 复现入口

见 `reproduction_entry.md`。

## 证据

- 指标：关键文本对比度达到 WCAG AA；112 个双语 text、224 个语言 tspan、144 个 vector shape、0 个 raster background。
- 对比图：`docs/design/previews/before/` 与 `docs/design/previews/qa/`。
- 运行日志：OpenDesign run IDs 记录于探索 README。
- 复现命令：见 `reproduction_entry.md`。

## 不得复制的大数据说明

本任务没有使用实验大数据、私密实验图、论文最终图、模型权重或外部图片；未向 knowledge 复制任何二进制科研数据。
