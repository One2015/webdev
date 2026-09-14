# 实施优先级与可执行边界

## P0：形成可交付闭环

- 统一任务输入、状态与有效清单，接入现有知识和 compile.mjs。
- 单页生成短 Query 与长 Prompt，并完整绑定本地素材。
- 集成业务、兼容、状态、跨文件和尺寸 Gate；负向测试在临时目录。
- 实现模式跳转与旧产物失效；不新增通用平台或复杂服务。

## P1：批次与两种操作

- batch planner 输出 N 套有明确差异的配置；group by business_branch。
- explore 返回独立候选；refine 接受 base hash 和 issues，输出受限 patch。
- 保存 Visual DNA 与实际配置 diff；不以 ID 差异评分。
- 接入截图对照和最相似候选对复核，校准距离阈值。

## P2：规模化

- 来源检索缓存与证据版本；资产去重与评审失效。
- 候选池扩大后考虑 MAP-Elites 档案或 DPP 选择，先评估特征是否反映人眼差异。
- 跨品类只复用通用契约，业务逻辑和模块适用性重新核验。

## 模块接口建议（待实现）

parseIntent(request) → brief
buildContext(brief,kb) → targets,gaps
planRetrieval(targets,budget) → queryBundle
assessEvidence(captures) → claims,knowledgeDelta
explore(brief,kb,batchPlan) → candidateConfigs
resolveAssets(candidate,assetPolicy) → assetBindings,readiness
compile(candidate,snapshot) → handoff
refine(base,issues,preserveRules) → patch | requires_replan
validatePage(build,contract) → results
publishRun(stagedOutputs) → validOutputs

候选模型可以是 LLM；确定性 Gate 与发布逻辑是程序；视觉评审需要截图和理由。无需多 Agent 也能实现。CLI 示例仅为未来接口，不声称本包已实现上述函数。

## 必需回归场景

1. 引用错位、未知 Style、缺失条件 owner 被拦下。
2. 同目录 library→unspecified demand→multi-unit→library→multi-unit，磁盘与清单一致。
3. 1240 容纳1200+48失败；1248通过；所有断点下限检查。
4. 有渲染规格无实际图片仍失败；小图、重复图片、错裁切、无授权、过期评审失败。
5. 与其他 GQ 同上的必要内容被拒绝；短长 Query 与 resolved 不一致被拒绝。
6. refine 变更锁定的字体身份或业务状态被拒绝；过期 base hash 被拒绝。
7. 十个仅换名/图片的方案不算十种感知风格。

## 本包已有代码

scripts/validate.py：资料包自身检查、JSON一致性、规则字段与 hash 校验。其他检测器均是本方案的待实现集成项。不能把该脚本通过理解为网页生成 pipeline 全部实现。

## v1.1实施增量

优先实现候选方向表、授权的局部预览、视觉身份锁和四张检查单。接着接入真实字体/布局压力检测；避免先实现一个未经校准的总分系统。脚本检查与渲染检查分开，模板数据不计真实结果。
