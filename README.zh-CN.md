# MycEvo

**科研自进化工作流外置大脑**

把每一次科研任务转成证据，把每一条经过验证的经验转成更好的工作流。

> **MycEvo 不替你科研，而是让你的科研工作流随着使用持续进化。**

[English README](README.md)

## 快速安装

```bash
git clone https://github.com/myc0576/MycEvo.git
cd MycEvo
python -m pip install -e .
```

## 60 秒闭环

在新的或已有科研工作区中运行：

```bash
mycevo init
mycevo demo
mycevo doctor
mycevo mcp install codex --workspace . --dry-run
# 或：mycevo mcp install claude --workspace . --dry-run
```

`init` 创建完整、可运行且不会覆盖已有文件的 workspace。`demo` 在本地执行脱敏闭环：

```text
task -> intake -> candidate writeback -> validation -> closeout -> recall
```

自动写回只能停留在 `candidate` 或 `pending validation`。`validated`、`reusable`、`approved` 和 `paper_ready` 必须经过人工或证据门禁。

## 产品架构

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/mycevo-product-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/readme/mycevo-product-light.svg">
  <img alt="MycEvo 通过证据、候选记忆、验证门禁、复用和反馈持续改进科研工作流的中英双语图" src="assets/readme/mycevo-product-light.svg">
</picture>

图中候选经验不会自动晋升；只有经过证据与人工门禁的经验才能成为可复用工作流。

## 技术架构

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/mycevo-technical-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/readme/mycevo-technical-light.svg">
  <img alt="MycEvo 公共引擎、私有科研工作区、证据门禁与脱敏公共改进路径的中英双语图" src="assets/readme/mycevo-technical-light.svg">
</picture>

MycEvo 是公共、版本化引擎；私有科研 workspace 保存真实状态、知识和实验扩展。私有实践只能先形成脱敏 candidate，经验证后才能反哺公共引擎。

## MCP 与兼容层

MycEvo 通过官方 `codex mcp` / `claude mcp` 命令安装本地 stdio MCP，并显式绑定 workspace。它不内置 Agent、LLM 或额外 API key。

正式命令是 `mycevo`。旧 `resevo` 和 `researchloop` 命令仍可转发，但会显示迁移提示。新环境变量为 `MYCEVO_*`；旧变量继续兼容读取。

使用 `mycevo migrate resevo` 预览 `.resevo/` 迁移，使用 `--apply` 备份并复制到 `.mycevo/`。历史 trace、ledger、schema ID 和科研数据不会被批量改写。

## 品牌说明

`MYC` 是项目作者的个人缩写，`Evo` 表示 Evolution。品牌视觉借用知识网络生长与经验演化的隐喻；MycEvo 不声称与真菌、生物学或 MYC 基因存在技术关系。
