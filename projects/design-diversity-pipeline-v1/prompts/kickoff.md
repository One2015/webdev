# 可复制的启动消息

请读取本项目 README、prompts/system-prompt.md、docs/pipeline.md、rubrics/README.md 与 rubrics/rules.json，按我附的任务配置执行。

目标是从真实参考学习并合成可独立执行的设计 Query，不以 JSON 数量或校验数量证明设计完成。先确认任务的业务边界、模式与预算；只对阻塞业务判断的缺失提问，可逆默认值写入决策记录后继续。

请先输出批次方向表和知识缺口，再执行获准检索、素材准备、兼容筛选和编译。短 Query 在对话完整展示，完整实现 Prompt 和素材包给出链接。长 Prompt 不要求读其他 GQ。

本轮 execution_end 以任务配置为准：query_only 交付后停止；build 先保存并展示交付物再实现。不要修改未指定的旧项目。最后分别报告配置合格、素材就绪、实现通过与感知差异通过的数量及剩余项。

任务配置：附 examples/task-batch.json 的已填写副本。workspace/output_root 必须替换为我允许访问的位置。
