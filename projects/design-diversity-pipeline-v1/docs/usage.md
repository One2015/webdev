# 使用方式

## 新开 Claude 对话

1. 解压本包，将整个项目文件提供给 Claude；能访问本地文件时直接提供项目路径。
2. 加载 prompts/system-prompt.md。若客户端没有真正 system 槽，把它作为首条项目工作约定，不声称其能覆盖客户端系统限制。
3. 使用 prompts/kickoff.md 作为任务消息，并填写 examples/task-batch.json。
4. 要求先报告当前阶段与计划产物，按已有授权继续；不因每个可逆默认值停下来审批。
5. query_only 接收 query.md 全文、长 Prompt、素材和报告。拿同一 handoff 到新对话即可执行，不依赖原会话。

## 第一轮：从零学习一个品类

选择一个 category + page_type + business_branch。例如住宿详情、单一可预订单元。先积累适用知识，按预算搜索 Mobbin/公开网页/DS。默认设计来源最多12候选、4–6深入参考、2轮补缺；如果十方向目标需要更大覆盖，可在任务中调整预算或报告不足。不要在同一轮无限扩大来源。

## 第二轮：十方向 Query

设置 operation=explore、compile_scope=demand、execution_end=query_only、target_count=10。批次表先于单页指令；展示十个方向的具体差异。冻结业务事实，允许根据方向换摄影语言但不得冒充同一真实房源。

素材搜索预算与设计参考预算分开。示例预算每方向最多20张候选、2轮，仅是成本上限，不保证可找齐。

## 第三轮：实现

只将 execution_end 改为 build，并指定获准实现目录。先交付 handoff，再按 Foundation→组件→核心体验→整页实现；不要把任意“继续”猜成从学习跳到开发。用户已明确 build 时不额外停下确认。

## 第四轮：局部修复

使用 examples/refine-request.json，填写真实 base hash 和 issue。锁 visual identity；不能在修复里把十个风格拉回统一模板。最多两轮后分析根因，必要时返回 requires_replan。

## 现有项目迁移

历史 design-kb 可以作为知识输入，原 compile.mjs 作为适配对象；本包不覆盖它。先在新目录验证映射，再修改获准项目。旧 CMB 仅覆盖住宿；切换品类需要重新检查业务和模块，不能直接改 category 字符串就宣称迁移完成。

## 校验本包

python3 scripts/validate.py

使用标准库，无需安装依赖。校验项目内容，不访问网络、不生成页面、不修改正式文件。修改内容后由维护者重新生成 manifest/hash；不能为掩盖错误自动刷新。

## 产物读取

每次 run 独立目录；下游只看 valid_outputs 和允许阶段。blocked/not_selected/decision_required 统一失效受管文件。模板、示例及先前 run 不能被误当本次成功产物。
