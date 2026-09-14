# 生成 Pipeline 与数据契约

## 两条路径

知识学习：范围 → 缺口与检索 Query → Mobbin/公开网页/官方规范 → 证据保存 → 拆解 → 适用性与兼容关系 → 知识校验。

需求生成：Intent → Context → 业务候选 → 兼容组合 → 批次多样性规划 → 素材准备 → 确认或回退 → 已解析配置 → Spec Gate → Query/Prompt 交付 → 可选实现 → 截图/行为 QA → refine → 反馈。

不默认每次重新采集。知识充分时复用；未知交互或关键素材缺口才定向检索。

## 数据层级与唯一来源

| 对象 | 责任 |
|---|---|
| product-intent.md | 用户、任务、业务前提、成功条件、范围、必要状态 |
| design.md | 主次参考、COPY/ADAPT/IGNORE、区域、Foundation、跨端规则 |
| component.md | Anatomy、配置接口、事件负载、状态所有权、依赖与恢复 |
| 素材清单 | 来源、授权、实际尺寸、裁切版本、槽位绑定及评审 |
| resolved.json | 一次选择全部展开后的配置，作为编译输入的确定快照 |
| rubric | 适用条件、检查方法、优先级、阻塞性与修复目标 |
| review result | 某次实际检查结果、环境、证据、例外与剩余项 |

可使用 Markdown 中的结构化块承载数据，不要求另建重复 JSON。文件数量随任务规模，不能为每个普通描述机械分配 ID。

## 证据与规范

- Reference → Claim → Knowledge → Selection → Component/Token → Check 要可追溯。
- observed/inferred/chosen 与实现验证分开；原始截图或量测不因解释变化而改写。
- DS 按 Profile、Atomic Rules、Component Capability 组织，记录 applicable_context、anti_context、selection_reason；选一个 Foundation System，再补适用规则，不混合全套系统。
- Foundation 锁定 Grid/Spacing/Typography/Sizing/Surface/Color/Density。
- Motion 记录触发、对象、起止状态、时长、缓动、中断和减少动效；无动态证据标为项目决定或未知。
- 单图不能证明状态转移、交互因果、动效与断点。

## Query QA 与 Evidence QA

Query QA 检查意图、目标覆盖、冗余、来源适配、检索预算与补缺计划。
Evidence QA 检查实际来源是否支持具体 claim、观察环境、真实性和局部证据边界。
Implementation QA 检查实际页面。三者不能相互代替。

Coverage(d) = sum(w_i * c_i) / sum(w_i)。权重提前确定；c_i 默认 0/1，部分覆盖需要定义。无目标为 N/A。硬约束失败独立阻塞，不能被平均分抵消。

Semantic duplicate 是语义表达近似；intent duplicate 是针对同一场景、问题、模式和证据用途重复检索。两者分别判断。漂移与冗余优先报告具体违规项，不预设未经校准的罚分常数。

## 素材与最终交付

候选先规定素材需求 → 主动搜索 → 核验实际文件 → 协调性评审 → 绑定与裁切 → 重编译。

图片数量、最低宽高、响应式裁切、授权都需要实际记录。避免将不相关的真实房源照片伪装成同一住宿；演示可明确虚构。不要用随机真人充当房东或随机地图冒充地点。

handoff/<run-id>/ 包含 query.md、implementation-prompt.md、resolved.json、asset-manifest.json、assets/、report.json。

短 Query 说明本次目标与设计方向；长 Prompt 内联本次所需的布局、组件、状态、Motion、素材与验收。两者来自相同配置。query_only 交付后停止；build 先展示交付物再实施已授权工作。

## 编译产物管理

blocked、not_selected、decision_required 共用管理范围内的失效逻辑。下游只读本次 valid_outputs。校验和负向测试在临时目录执行，不覆盖正式产物；上游修改后相关 Gate 与产物重新编译。
