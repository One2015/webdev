# Query QA Agent & Design Evidence Pipeline — v1.0

2026-09-14 · 中文方案、系统指令与执行契约

目标：从真实参考学习设计知识，在同一业务边界内组合不同 PA 与视觉方向，准备素材，独立交付 Query＋实现 Prompt，并按授权实现与验证。重点是快速复用与重组，不是围绕 A/B 实验建设系统。

本项目是可交付的**方案与契约参考包**。含可运行的资料完整性校验器；不声称已经实现采集器、网页生成器或所有质量检测器。历史 design-kb 与 CMB-01 页面不在本包内，其状态未在本次重新验收。

## 阅读与使用

1. [使用指南](docs/usage.md)：如何在 Claude 新对话使用。
2. [完整 System Prompt](prompts/system-prompt.md)：持续行为约定。
3. [Pipeline](docs/pipeline.md)：节点、依赖、终止与状态。
4. [知识与数据契约](docs/data-contracts.md)：记录什么，如何绑定。
5. [多样性与 explore/refine](docs/diversity.md)：批量生成十页的操作方法。
6. [Rubric 指南](rubrics/README.md) 与 [规则数据](rubrics/rules.json)。
7. [论文索引与解读](research/reading-guide.md)。
8. [本对话决策记录](history/conversation-decisions.md) 与 [历史问题](history/review-lessons.md)。
9. [实施优先级](docs/implementation-plan.md)。

## 三分钟开始

将 prompts/system-prompt.md 作为系统指令（客户端没有 system 槽时，放在新对话首条说明中），附本项目文件。使用 prompts/kickoff.md，填写 examples/task-batch.json 的工作路径与业务需求。默认 query_only：先交付指令与素材，不自动生成网页。

```sh
python3 scripts/validate.py
```

该命令只验证本资料包的规则结构、引用、示例及文件 hash，不运行网页，也不替代节点 Gate。ZIP 中包含同样的项目文件、MANIFEST.json 和 SHA256SUMS。正文来源与自拟建议分开；10 个方向、6 个风格家族等数量均为任务策略，不是行业标准。

## 不覆盖旧内容

仓库：https://github.com/One2015/webdev

新增目录：projects/design-diversity-pipeline-v1/；独立分支：codex/design-diversity-pipeline-v1。既有 outputs、work、README 与归档保持原样。ZIP 在本地 archives 下；不把既有实现、图片、账户配置或聊天数据库混入本次发布。
