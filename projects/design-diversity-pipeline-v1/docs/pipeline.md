# Pipeline：两个生命周期与十个节点

## 知识学习（增量）

范围 → Context 目标 → 检索 Query QA → Retrieval（Mobbin / 公开网页 / DS / 视觉与模式来源）→ Evidence QA / Reference Ranker → Reference Analyzer → 知识与兼容关系。

## 需求生成

Intent Parser → Context Builder → Batch Planner / explore → 候选兼容 Gate → 素材检索与适配 → Foundation / Component / Pattern / Design Spec → Spec Gate → Query Compiler → 生成前交付 → 可选 Prototype Generation → Screenshot / Visual Comparator → Targeted Repair / refine → Final Review → Data Feedback。

素材反馈可以回退组合；实现反馈只回到问题所属层。流程不是每次全量执行：已有证据充分时跳过采集，query_only 不执行页面实现。

| 节点 | 输入 | 输出 | 核心 Gate | 失败路由 |
|---|---|---|---|---|
| intent | 用户需求 | brief、业务条件、假设 | R01 | 关键缺失 decision_required |
| context | brief、知识 | 目标覆盖与缺口 | R02 | 定向检索 |
| retrieval | 目标、预算 | 检索记录、原始证据 | R03 | 换候选或保留缺口 |
| evidence | 原始证据 | claim、可复用单元 | R04/R05 | 降级 claim，不改源证据 |
| explore | 知识、批次计划 | 独立候选 | R06/R07/R08 | 淘汰、适配或补方向 |
| assets | 槽位要求 | 实际素材绑定 | R09/R10 | 换图、降级、回退 |
| compile | 最终候选 | handoff | R11/R12/R13 | 修源配置或编译器 |
| build | 有效 handoff | 页面 | R14/R15 | 实现修复 |
| refine | issue、当前配置 | patch、新版本 | R16 | 回退或 requires_replan |
| final | 各结果、截图 | 交付与反馈 | R17/R18 | 报告缺额/未验证项 |

## 模式

compile_scope = library/demand；execution_end = query_only/build；operation = explore/refine；knowledge_mode = reuse_only/reuse_with_targeted_learning；asset_mode = provided_only/search_and_prepare。用户要求批量 explore，不代表要求并行 Agent 或允许新建十个任务。

## 就绪状态不要混合

- selection_status：eligible/conditional/blocked/not_selected/decision_required。
- structure_behavior_ready：规格可用于结构行为实现，尚不表示行为已经运行通过。
- asset_condition：met/unmet/unknown。
- implementation_validation：not_run/partial/pass，附环境与 checks。
- perceptual_diversity：not_run/partial/pass，附候选集合、视口与比较证据。

素材 unmet 的方案可能具备结构实现条件；摄影依赖方向只能条件性交付。配置差异可被报告，但不计入完整视觉交付数量。

## 原子发布与失效

先生成到新临时目录并验证 → 发布本次 manifest / valid_outputs → 清除同一受管目录内不再有效的已登记产物。对中途中断保留上一完整 run；不要写一半即更新有效清单。不同 run 目录可保留历史，但不得让下游将旧版当成本次有效版本。相同输入、策略版本、seed 与素材 hash 应生成相同编译产物；LLM 候选产生过程可能不确定，必须保存其结果快照。
