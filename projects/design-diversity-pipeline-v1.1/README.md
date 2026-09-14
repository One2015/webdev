# WebDev 2.0：网站配方、生成稳定性与多样性 — v1.1

2026-09-14 · 基于本 Chat 最新讨论与 DeepSeek 反馈整合。

**先固定业务，再规划不同的网站配方；先确认做得好，再判断是否明显不同。**

本包是系统指令、操作方式、数据约定与评估方案，可直接作为 Claude 新对话的项目材料。附资料完整性校验脚本；不是已经实现的网页生成引擎，不把资料校验通过当成页面质量通过。v1.0 原目录保留，本版为独立新增目录。

## 先读这四份

1. [System Prompt](prompts/system-prompt.md)：完整整合版，直接复制使用。
2. [操作方式](docs/usage.md)：学习、选方向、交付与实现的具体步骤。
3. [生成稳定性](docs/generation-stability.md)：layout、font、图片、状态与复现怎么检查。
4. [多样性评估](docs/diversity-evaluation.md)：两条筛选线、四张检查单、成对比较与终止条件。

## 其他材料

- [更新说明](CHANGELOG.md) / [团队大白话版](docs/team-brief.md)
- [生成流程](docs/pipeline.md) / [知识与数据契约](docs/data-contracts.md)
- [探索与局部修复](docs/diversity.md) / [实施顺序](docs/implementation-plan.md)
- [Rubric指南](rubrics/README.md) / [结构化规则](rubrics/rules.json)
- [启动消息](prompts/kickoff.md) / [网站配方模板](prompts/recipe-template.md)
- [批次任务示例](examples/task-batch.json) / [评估计划](examples/evaluation-plan.json)
- [稳定性契约示例](examples/stability-contract.json) / [成对评审示例](examples/pair-review.json)
- [论文阅读索引](research/reading-guide.md) / [稳定性技术依据](research/stability-sources.md)
- [本Chat决策摘要](history/conversation-decisions.md) / [历史修复经验](history/review-lessons.md)

## 使用与验证

给 Claude 本包，加载 System Prompt，填写批次任务并发送启动消息。默认 query_only，不生成业务页面。render preview 与 build 均需要任务配置中的授权。

```sh
python3 scripts/validate.py
```

标准库即可运行，只读资料文件并校验规则、示例、链接和hash。页面检测器及截图评审的实现要求写在文档里，不冒充已运行检测器。

论文为索引与摘要，不捆绑第三方全文。对话材料为基于可见记录整理的决策摘要，不是逐字会话导出。旧项目源码与captures不在本包内。
