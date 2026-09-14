# Query QA Agent & Design Evidence Pipeline

> 中文产品与工程方案 · v1.2 · 2026-09-07  
> 用途：团队方案评审、数据建模、MVP 拆解，以及 Codex 后续实现依据。  
> 来源：[《查询审查输出》对话](chatgpt-conversation://6a9eeab9-d7c4-83ea-ac84-2c30625c69ce)。本文整合当前可读取的全部讨论并去重；公式的边界处理、数据契约、测试与终止策略属于工程化补充建议。所有权重、阈值、尺寸及预算均为示例或待校准初值，不代表已有系统的实测结果。本文不验证外部产品当前的 API 能力。

> v1.1 补充：第 19–21 节明确参考库沉淀、证据需求驱动的 Query Builder，以及六项执行契约。具体字段与运行规则以补充章节为准；其他章节的 JSON 仍是局部示例，不是完整运行实例。

> v1.2 更新：将 Category Blueprint、Asset Brief、素材定向搜索 / 制作、Asset Pack 和页面内验证接入主流程；第 22–25 节定义建设方法、数据契约、QA 与对照实验。新增对象是建议设计，未表示已建设骨架库、采集素材或验证模型效果。

## 1. 背景问题与目标

原有链路主要依靠原始需求与 SD / PA 的自由组合生成查询，再进入 UI 生成。它暴露出三个相互关联的问题：

1. **查询数量不等于有效多样性。** 多条查询可能只是替换形容词，仍然都在寻找同一种漂亮首页。原对话提及 593 条数据中的 style collapse，但没有提供原始数据，本文将其作为问题背景，不据此推导统计结论。
2. **设计依据不完整。** 视觉风格和普通页面容易被过度覆盖，首次使用、空数据、权限、部分失败、离线及恢复流程容易缺失。产品分类也不能替代真实使用场景。
3. **参考图到代码之间缺少约束。** 直接把截图交给生成器，会让它同时猜布局、间距、字号、密度、组件比例与交互，导致“语义相似，视觉不像”，后续依赖人工多轮修正。

目标是建立一条可追溯的链路：**需求 → 证据需求 → 查询 → 实际证据 → 设计决策 → 明确规格 → 可运行原型 → 验证与局部修复**。

成功标准包括：核心任务和关键状态有依据；有效视觉探索没有坍塌；每项设计决定能找到来源；首轮实现更接近目标；修复次数、检索成本与回归问题可被记录。不要用一个总分替代这些目标。

## 2. 从 Query Diversity 到 Design Evidence Coverage

**Query Diversity** 关注查询之间是否不同。**Design Evidence Coverage** 关注为了完成当前设计，系统是否取得足够完整、多样、适配需求且不过度重复的证据。Query 是获取证据的手段。

| 概念 | 定义与边界 |
|---|---|
| Task | 用户要完成的动作，如发现目的地、搜索、收藏、继续行程 |
| Scene | 任务发生的使用情境，如首次打开、回访、规划途中；不同于产品 category |
| Pattern | 可复用的产品组织或交互方式，如发现 feed、搜索入口、保存列表 |
| State | 特定场景或组件的运行状态，如 loading、empty、error、offline |
| Context | 产品、平台、受众、旅程、风险、密度等约束；同时包含固定条件与待覆盖情境 |
| Reference Intent | 获取证据的目的：screen / flow / interaction / state / component / visual / design_system reference |
| Visual DNA | 对构图、密度、字体、颜色、表面、图像、导航及必要时动效的结构化描述 |
| SD / PA | 沿用原对话缩写：SD 承担视觉语言检索，PA 承担产品 pattern 检索；原讨论未明确其全称或存储实现 |
| Evidence | 可定位的截图、流程、组件规范、规则或设计记录，附来源、适用范围与验证状态 |

统一维护三层 coverage，禁止混用：

- `planned_coverage`：通过 QA 的查询计划是否尝试获取目标证据。
- `verified_evidence_coverage`：实际返回且通过检查的证据是否支持目标。
- `implemented_coverage`：规格和原型是否实现目标，并通过相应验证。

最终关注 `Scene × UX Problem × Reference Intent × State` 的覆盖关系，而不只是标签数量。场景、状态之间的有效组合由 Context Builder 明确列出，避免对所有标签做无意义的笛卡尔积。

## 3. 完整 Pipeline 与节点契约

```text
Original Request
  → Intent Parser
  → Context Builder
  → Blueprint 候选匹配 + 已有证据检查 → EvidenceNeed
  → Query Builder
  → Query QA Agent ──未通过──→ Targeted Query Repair → Re-QA
  → Retrieval（参考库 / Mobbin / Design System / SD / PA / 网页 / 录屏）
  → Evidence QA / Reference Ranker ──缺证据──→ 定向重检索或补 Query
  → Reference Analyzer
  → Blueprint 选择与项目适配 → Design Foundation
  → Design Spec 草案（含 State Matrix、Content Contract、素材槽位）
  → Asset Brief → 素材定向搜索 / 获取 / 制作 → Asset QA → Asset Pack
  → 设计稿或页面骨架 + 真实内容装配 → Design Spec 锁定
  → Prototype Generation
  → Screenshot Capture / Visual Comparator
  → Targeted Repair ──→ 重新截图与相关回归检查
  → Final Review
  → Data Feedback
```

| 节点 | 主要职责 | 输出 |
|---|---|---|
| Intent Parser | 提取显式需求、核心任务、硬约束与待确认假设 | IntentProfile |
| Context Builder | 定义场景、UX 问题、目标权重、关键项、来源需求及探索预算 | ContextProfile、CoverageTarget、DiversityBudget |
| Query Builder | 围绕目标生成查询，按来源转换表达 | QueryBundle |
| Query QA Agent | 防偏题、查缺口、去重、检查来源可执行性、规划补洞 | QueryQAReport、RepairPlan |
| Retrieval | 执行获批查询，保留请求与返回结果关系 | RetrievalRun、EvidenceItem |
| Evidence QA | 验证实际相关性、完整性、可用性与证据支持范围 | EvidenceQAReport |
| Reference Ranker | 在合格证据中选整体参考与局部参考 | ReferenceSet |
| Reference Analyzer | 分解结构、比例、视觉层级与可继承规则，记录推断不确定性 | ReferenceAnalysis、VisualContract 草案 |
| Blueprint Selector / Adapter | 匹配品类、页面任务与内容结构，选择已验证骨架并记录项目差异 | BlueprintSelection、OverrideLog |
| Design Foundation | 解决参考与规范冲突，锁定项目基础 tokens | DesignFoundation |
| Spec Builder | 明确组件能力、页面组合、行为、状态和验收标准 | DesignSpec、StateMatrix |
| Asset Planner | 将真实内容与页面区域转为可检索、可制作的素材需求 | AssetBrief、AssetSlots |
| Asset Retrieval / Production | 获取候选素材，缺口按范围与预算定向制作 | AssetCandidate、素材文件、来源记录 |
| Asset QA / Pack Builder | 检查内容、使用条件、尺寸、整组一致性与页面适配 | AssetQAReport、AssetPack |
| Prototype Generation | 按规格实现页面与必要交互 | 可运行实现、构建记录 |
| Visual Comparator | 在规定视口和状态下比较实现与契约，输出可定位差异 | ComparisonReport |
| Targeted Repair | 仅修改差异指向的范围，保留已通过项 | Patch、RepairResult |
| Final Review | 汇总任务、状态、视觉、交互与运行检查 | FinalReview、已知限制 |
| Data Feedback | 记录缺口、选择理由、修复效果与版本 | FeedbackEvent、评估数据 |

每个节点必须保存输入版本、输出版本、失败原因和上游 ID。执行失败、内容不合格、没有结果必须分开编码，便于选择正确的修复入口。

这是完整逻辑顺序，不要求每次都调用全部节点。已有骨架、已核验证据和素材可直接复用；没有素材需求的工具页面可将 Asset 阶段标为不适用。骨架代码可先占位搭建，但最终视觉验证必须使用已锁定素材；素材影响比例或内容结构时，返回 Spec 做版本化调整。

## 4. Query Builder：Query Bundle、约束与来源适配

### 4.1 硬约束与软变量

硬约束通常包括产品目标、平台、核心任务、页面范围、受众，以及用户明确指定的要求。软变量包括允许探索的构图、密度、视觉表达、pattern 变体和参考产品。

“软”不意味着随意：例如用户锁定高密度工具型页面后，density 就成为硬约束。Context Builder 在生成前给每项标注 `fixed` 或 `explorable`。不能为了多样性把旅行发现首页变成酒店支付流程。

允许跨领域借鉴，但必须显式声明 `analogy_scope`：例如只借鉴上传失败的重试规则，不继承对方的产品业务与整体导航。来源查询不必逐字包含全部上下文，结构化适配范围必须保留，且不能隐含矛盾。

### 4.2 Query Bundle 的基本单位

每条 query 至少记录：ID、检索文本、来源、预算类别、场景、获取目的、目标 ID、硬约束继承关系、signature、预期结果类型和选择理由。`covers` 应由 QA 验证，不能直接相信 Builder 的自报标签。

```json
{
  "id": "qb_travel_v1",
  "context_id": "ctx_travel_v1",
  "target_version": "1.0",
  "budget_id": "budget_16_v1",
  "queries": [
    {
      "id": "q01",
      "text": "travel mobile app destination discovery home",
      "source": "mobbin",
      "budget_bucket": "primary_task",
      "reference_intent": "screen_reference",
      "target_ids": ["task.discover_destination", "pattern.discovery_feed"],
      "context_scope": "inherit_all",
      "expected_evidence": "screen",
      "selection_reason": "寻找旅行发现首页的信息组织与入口层级",
      "signature": {
        "task": "discover_destination",
        "scene": "returning",
        "pattern": "discovery_feed",
        "reference_intent": "screen_reference",
        "visual_direction_id": null
      }
    }
  ]
}
```

### 4.3 数据源适配

| 来源 | 要解决的问题 | 查询适配方向 | 不能据此认定 |
|---|---|---|---|
| Mobbin | 真实产品如何组织 screen、flow、状态 | 平台、场景、页面、UI element、流程词 | 截图相似就证明交互完整 |
| Design System | 组件能力、状态、行为及设计规则 | 系统版本、组件、规则类型、适用平台 | 找到系统名称就完成规范覆盖 |
| SD | 视觉语言与可控方向探索 | Visual DNA、允许变化的维度、排除条件 | style ID 不同就视觉不同 |
| PA | 产品 pattern、任务流程和组合 | 用户任务、场景、UX problem、状态 | pattern 名称存在就适配当前业务 |

统一接口建议为 `search(request) → results + execution_metadata`；具体来源支持哪些筛选项由 adapter 的 capability 配置声明。Source QA 检查 capability，不能编造来源不支持的参数。状态可从 Mobbin、DS 或 PA 取得，不必另建一个强制来源。

## 5. Query QA Agent 架构

输入为 `IntentProfile + ContextProfile + CoverageTarget + QueryBundle + SourceCapabilities + ScoringPolicy`。

| 子模块 | 判定内容 | 结构化输出 |
|---|---|---|
| Intent QA | 是否违背硬约束；跨领域借鉴是否限定范围 | constraint_checks、drift、rejected_query_ids |
| Coverage QA | 获批查询覆盖哪些任务、pattern、场景、状态、context、reference intent | covered、missing、critical_missing |
| Diversity QA | 语义重复、意图重复、边际贡献、视觉方向集中 | duplicate_clusters、overrepresented、visual_report |
| Source QA | 来源可用、参数可执行、预期证据类型受支持 | source_checks、unsupported_requests |
| Repair Planner | 保留有效查询，删除或替换重复项，补齐具体目标 | keep、drop、replace、generate |

执行顺序建议：结构校验 → 标签归一化 → Intent/Source 检查 → 候选重复检测 → 选择有效子集 → 重新计算 coverage → gate → repair。报告同时保留提交时与筛选后的重复率，避免通过删除记录掩盖 Builder 的重复问题。

LLM 可以提出标签、解释匹配理由、拆解参考图和提出 repair；**分数由固定规则代码计算**。标签仍可能出错，因此必须附输入依据、提取器版本和 `verified / unknown / rejected` 状态。关键项的 `unknown` 不能按覆盖计分，应定向验证或报告阻塞。

## 6. 可计算的 Coverage Score

### 6.1 先固定目标，再计算集合覆盖

令维度 \(d\) 的有效目标集合为 \(T_d\)，权重 \(w_t>0\)。不适用目标在评估前排除，并记录理由；不能在失败后删除目标来提高分数。

对获批查询集合 \(Q\)，定义：

```text
m(q,t) = 1：query 的文本或有效结构化筛选确实尝试检索目标 t，且通过适用范围检查
         0：不支持、冲突或尚未验证

c(t) = max_{q∈Q} m(q,t)
C_d = Σ_{t∈T_d} w_t × c(t) / Σ_{t∈T_d} w_t
```

同一目标被十条查询覆盖，仍然只计一次。`Q` 为空且目标非空时为 0；目标为空时输出 `null / not_applicable`，不自动算 1。每个维度同时输出加权结果、覆盖数量、目标数量、缺失 ID 与 supporting query IDs。

Evidence QA 使用同一公式，但把 `m(q,t)` 替换为“实际证据是否经核验支持 t”。一条查询要求 offline，不等于搜回来的截图证明了 offline。

### 6.2 task / pattern / states / context 示例

| 维度 | 目标与权重 | 已覆盖 | 原始加权覆盖 |
|---|---|---|---|
| task | discover .35、search .25、save .25、continue .15 | 前三项 | .85 |
| pattern | discovery_feed .25、search_entry .20、destination_card .20、saved_trip_entry .20、personalization .15 | 除 saved_trip_entry 外 | .80 |
| states | loading .20、empty .20、error .25、offline .20、first_time .15 | loading、empty、error | .65 |
| context | audience .20、platform .20、journey .20、product .20、density .10、risk .10 | 前四项 | .80 |

以上为原讨论的简化例。实际 states 应使用 `scene × state` ID，例如 `search.error` 和 `save.error` 分别计算；一个普通 error 查询不能自动覆盖二者。`first_time` 通常建模为 scene，`first_time.empty` 才是具体状态组合；不得因重复命名两次加权。

Context 中固定约束的“保留程度”与多场景的“覆盖程度”分开记录。层级 context 推荐只给叶节点计权，父节点用于汇总，防止同时给 mobile 和其子项重复加分。继承的上下文无需全部放入检索文本，但继承本身不能证明来源会返回该受众或风险级别的结果。

### 6.3 drift penalty 与 intent preservation

为每条查询定义适用约束集合 \(H_q\)，约束权重为 \(a_h\)，明确冲突标记为 \(v_{qh}\in\{0,1\}\)：

```text
D_q = Σ a_h × v_qh / Σ a_h
D_bundle = Σ b_q × D_q / Σ b_q
intent_preservation = 1 - D_bundle
context_adjusted = clamp(C_context - λ_drift × D_bundle, 0, 1)
```

`b_q` 默认为等权；任何其他加权方式写入 policy。适用约束由完整上下文或显式 analogy scope 决定。`unknown` 单列，不假装为“已匹配”；关键约束未知会阻止通过。

例如覆盖 .92、已计算的惩罚项 .08，则调整后为 .84。此处 .08 必须能展开为冲突检查和系数，不能由模型直接给出。**任何硬约束冲突直接拒绝该查询**，不能用高 coverage 抵消。提交集合的 drift 留作诊断，筛选后的集合用于下游 gate。

### 6.4 duplicate penalty：覆盖与效率分开

集合并集已防止重复查询刷高 coverage；重复惩罚衡量的是预算浪费，不意味着已覆盖的目标消失。

对于 N 条查询，经固定规则分成 K 个重复簇：

```text
duplicate_ratio = (N - K) / N
adjusted_score_d = C_d × (1 - λ_dup × intent_duplicate_ratio)
```

`N=0` 时比例报告为 0，同时 `empty_bundle` gate 失败。语义重复与意图重复各算一次并分别报告；不要将两种惩罚直接相加，避免同一问题双重扣分。示例：`.90 × (1 - .30 × .30) = .819`。

推荐 MVP 以原始 coverage + 独立 drift/duplicate gate 为准。若展示 adjusted score，必须说明是效率修正值。关键项缺失采用硬 gate；如另加 `missing_critical_penalty`，必须显示明细，不能隐式重复扣罚。

### 6.5 visual：方向覆盖、实际距离与维度覆盖

先定义允许探索的方向，而非只规定“生成三个 style”。例如 A 为 editorial / spacious / high-imagery，B 为 utility / compact / low-imagery，C 为 modular / medium-density / neutral。被硬约束锁定的维度不进入多样性要求。

Visual DNA 的距离采用固定分类表与权重：

```text
distance(i,j) = Σ β_k × δ_k(x_ik, x_jk) / Σ β_k
```

- 类别维度：相同为 0，不同为 1；细粒度相似关系使用预先定义的距离表。
- 有序维度：如 density 使用序数差除以最大跨度。
- 数值维度：如图像面积比例使用归一化差值。
- 未知值不能当成一种新的视觉风格；必需字段未齐全的样本不参与完整方向匹配，并报告缺失。仅剩不足两项有效样本时，不计算虚构距离。

给定目标方向集合和去重后的有效候选，采用带阈值的确定性一对一匹配；例如距离 ≤ .25 才能匹配。一条候选只能占一个目标方向，A 与 A′ 不能同时填满两个方向。

```text
C_direction = 已匹配目标方向权重 / 全部目标方向权重
D_pair = 有效代表样本两两 distance 的平均值
C_dimension = 已覆盖的目标 DNA 属性值权重 / 全部目标属性值权重
Visual Score = .50 × C_direction + .30 × D_pair + .20 × C_dimension
```

例如 `.50 × .67 + .30 × .72 + .20 × .75 = .701 ≈ .70`。这里三个输入都由匹配、距离和集合计算得到。少于两个有效代表且要求多方向时，`D_pair=0`。只要求单方向时，pairwise diversity 标为不适用，并按 policy 重新归一化其余项权重。

附加记录 `visual_concentration = 最大视觉簇大小 / 视觉查询数`。它用于发现过度集中，不能机械套用 .40：若预算只有两个视觉查询，最低可能集中度就是 .50。若只要求一个方向，不启用集中度 gate。

七个常用 DNA 维度为 composition、density、typography、color、surface、imagery、navigation；只有任务需要动效且来源提供流程或动态证据时才加入 motion。静态截图无法证明时长或 easing。换紫、蓝、绿通常只改变 color，不能充当完整视觉探索。

## 7. Diversity Budget、Query Signature 与去重

### 7.1 预算分配

原讨论的 16 条示例：primary task 4、product patterns 3、scenes 3、states / edge cases 3、visual exploration 2、design system 1。

每条查询只占一个预算 bucket，可覆盖多个目标。来源预算与目的预算独立，不要求每一类都平均分给四个来源。若要求至少三个视觉方向，应把 visual 调到至少 3，或明确其他 bucket 中哪些查询负责第三方向；Context Builder 应在生成前检查预算可行性。

缺少关键状态时，优先从重复的视觉查询回收预算。跨来源验证可保留同一意图的重复检索，但必须有 `corroboration_group` 和检索目的，分别报告获准验证开销与可避免重复。

### 7.2 两类重复

| 类型 | 检测方法 | 解释 |
|---|---|---|
| semantic duplicate | 固定文本归一化、固定 embedding 版本与相似度阈值，或 MVP 词面规则 | 查询文本意义近似 |
| intent duplicate | 比较 task、scene、pattern、reference_intent，以及适用时的 visual DNA | 用词不同，但解决同一证据获取问题 |

Signature 使用受控词表、排序后的集合、显式空值与版本号。不要只比较可变的自然语言描述。

```text
signature_similarity(i,j)
  = Σ γ_k × match_k(i,j) / Σ γ_k
```

原讨论“80% 相同算重复”仅是启发式初值。工程实现需增加条件：相同核心目标、相同 reference intent、没有新增关键覆盖，才构成可删除候选。状态查询与视觉查询即使词面接近也不能直接合并。

MVP 可先按精确归一化 signature 聚类。近似聚类采用固定排序、固定代表选择和确定性算法，避免 A≈B、B≈C 就误认为 A≈C。embedding 只用于候选发现；阈值必须在标注样本上校准。

### 7.3 保留策略：覆盖贡献与距离

计算 `ΔC(q|S)=C(S∪{q})-C(S)`，并考虑与已有集合的距离。先过滤偏题，再保留增加关键覆盖的查询；新增覆盖低且高度相似的候选删除。为尚未覆盖的视觉方向保留预算。距离远本身不构成价值。

多样性存在于探索与证据获取阶段。进入单个原型实现后，需要收敛为一个一致方向，而不是把多个方向混合到一个页面。

## 8. Query QA 与 Retrieval / Evidence QA 的职责区别

| 检查 | Query QA | Retrieval / Evidence QA |
|---|---|---|
| 核心问题 | 搜索计划是否合理且完整 | 是否真正取得可用证据 |
| 能检查什么 | 意图、目标覆盖、重复、来源参数与获取目的 | 实际内容相关性、截图可读性、流程完整性、状态证据、规范适配 |
| 不能证明什么 | 查询写了 loading 就真的有 loading 证据 | 偶然取得好结果就说明 Query Builder 稳定 |
| 失败处理 | 补查询、改适配、删除重复 | 重检索、换来源、补局部证据、报告证据缺口 |

EvidenceItem 至少应保存来源定位、获取时间、来源版本（若可取得）、关联 query、截图或内容位置、覆盖目标、适用与反适用上下文、证据核验状态。无法访问与“访问成功但不相关”分开报告。

Reference Ranker 先剔除不适用项，再比较任务匹配、场景匹配、平台适配、状态完整性及可分析程度。可使用规则匹配加权排序，并给出逐项依据；视觉偏好可以有人工选择，不能伪装成客观置信度。状态截图即使不足以担任 Primary，仍可能是合格的局部证据。

## 9. Mobbin Reference：角色、继承策略与 Visual Priority

### 9.1 Primary / Secondary

针对一个页面或一致页面族，默认选择 **1 个 Primary reference，最多 2 个 Secondary references**：

- Primary 控制宏观结构、层级、密度、比例与视觉节奏。
- Secondary #1 只解决某个局部 pattern。
- Secondary #2 只解决状态或交互问题。

参考检索库可以更大，最终生成上下文必须精简。多页面 flow 可以保留更多证据，但每个页面要有明确的主参考及一致性规则；不能让不同参考争夺同一设计属性。

### 9.2 COPY / ADAPT / IGNORE

| 标记 | 使用方式 | 典型内容 |
|---|---|---|
| COPY | 提取并尽量保留可复用结构 | 布局比例、信息层级、密度、间距节奏、组件组合 |
| ADAPT | 保留解决问题的方法，适配业务 | 内容、数据、文案、动作、状态、工作流 |
| IGNORE | 不进入生成规格 | 品牌 logo、不相关导航、无关功能、未获授权的专有素材 |

COPY 是设计属性的继承策略，不表示所有像素和素材都需要直接复制。业务约束与项目规范仍优先。

### 9.3 Visual Priority

| 优先级 | 验证范围 |
|---|---|
| P0：必须接近 | 宏观布局、容器宽度、组件比例、间距节奏、字体层级、信息密度 |
| P1：尽量接近 | 圆角、边框、图标尺寸、按钮与行高、颜色层级 |
| P2：业务适配 | 文案、产品数据、标签与图像内容 |
| P3：不继承 | 品牌标识与专有资产 |

```json
{
  "reference_id": "ref_home_01",
  "source": "mobbin",
  "role": "primary",
  "scope": "home",
  "applicable_context": ["consumer_mobile", "destination_discovery"],
  "anti_context": ["enterprise_admin"],
  "selection_reason": "发现内容与继续行程入口的层级符合当前任务",
  "copy": ["layout_proportions", "hierarchy", "spacing_rhythm"],
  "adapt": ["content", "actions", "states"],
  "ignore": ["branding", "proprietary_assets"],
  "visual_priority": {"layout": "P0", "density": "P0", "typography": "P0", "surface": "P1"}
}
```

## 10. Design System 知识组织与选择

Design System 是约束来源。数量增加不会自动提升设计质量。建议组织为三类可检索对象，并按当前页面动态取用。

| 对象 | 关键字段 | 用途 |
|---|---|---|
| Profile | id、version、platform、design principles、foundation 摘要、applicable_context、anti_context | 判断是否适合作为基础系统 |
| Atomic Rules | rule_id、scope、trigger、requirement、severity、source_locator、例外条件 | 提供可执行或可检查的单条规则 |
| Component Capability | component_id、variants、supported_states、interaction、content limits、可访问性规则引用 | 判断组件能否支持当前业务及状态 |

`selection_reason` 是一次选择与当前 Context 的关联记录，不应只有“现代”“好看”等描述。`anti_context` 表示不优先或不适用条件，应说明是软偏好还是硬冲突，不能把某个 DS 永久贴上简单标签。

```json
{
  "foundation_system": {"id": "project_mobile_system", "version": "1.0"},
  "supplemental_rules": [
    {"rule_id": "internal.retry.recovery", "scope": "search.error", "selection_reason": "补齐搜索失败后的恢复行为"}
  ],
  "selection": {
    "applicable_context": ["consumer_mobile", "state_heavy"],
    "anti_context": [],
    "selection_reason": "基础 tokens 与目标平台一致，并支持本页所需组件状态"
  }
}
```

默认采用 **1 个 Foundation System + 0–2 个补充规则来源**。补充的是局部规则，不是第二套完整 token 体系。若基础来源只提供原则而没有可直接使用的数值 tokens，则在项目 Foundation 中显式定义数值，保留推导来源。

冲突处理顺序建议：用户明确约束与项目必须遵循的规则 → 既有项目 Foundation → 当前 Primary 的视觉目标 → Supplemental Rules 的局部补充。新建项目可由 Primary 推导 Foundation。出现无法同时满足的冲突时，记录 decision，而不是平均两个值或静默覆盖。

## 11. Reference Analyzer 与 Design Foundation

Analyzer 先输出页面 anatomy：视口、区域边界、容器、层级、主要组件、图文比例、密度、间距节奏及状态证据。截图量测应标记 `measured / estimated / unknown`；单张图无法可靠确定字体名称、响应式规则或完整交互。

原始像素需结合截图尺寸与 DPR 换算；DPR 不明时优先使用相对比例，不能把图片像素直接当 CSS px。记录推测值及容差，再将它们转化为项目明确决策。

Foundation 在写页面代码前锁定七类：

| 类别 | 必须明确的内容 |
|---|---|
| Grid | 目标 viewport、内容宽度、列数、gutter、边距、导航宽度或移动端安全区处理 |
| Spacing | 基准单位、页面 padding、section gap、组件 gap、card padding |
| Typography | 字体或替代字体、字号、行高、字重、title / body / label / metadata 层级 |
| Sizing | 按钮、输入、行、图标、头像等当前页面所需尺寸 |
| Surface | radius、border、shadow、elevation |
| Color | background、surface、text、border、accent、semantic roles |
| Density | compact / default / spacious，以及支持该密度的具体数值 |

```json
{
  "id": "foundation_mobile_v1",
  "version": "1.0",
  "status": "locked",
  "unit": "css_px",
  "grid": {"viewport": {"width": 390, "height": 844}, "columns": 4, "page_margin": 16, "gutter": 12},
  "spacing": {"xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 32},
  "typography": {
    "family": "system-ui",
    "title": {"size": 28, "line_height": 34, "weight": 600},
    "body": {"size": 16, "line_height": 24, "weight": 400},
    "metadata": {"size": 12, "line_height": 16, "weight": 400}
  },
  "sizing": {"button_height": 48, "input_height": 48, "icon": 24},
  "surface": {"radius_card": 12, "border_width": 1, "shadow": "none"},
  "color": {"background": "#FFFFFF", "surface": "#F5F5F5", "text_primary": "#171717", "text_secondary": "#525252", "border": "#D4D4D4", "accent": "#1D4ED8", "error": "#B91C1C"},
  "density": "default",
  "provenance": [{"path": "grid.page_margin", "reference_id": "ref_home_01", "method": "estimated_then_decided", "tolerance": 2}]
}
```

以上为演示性 tokens，并非某个公开 DS 的标准。实现优先使用已锁定 tokens；需要例外时记录用途和影响。局部修复不能静默修改全局 Foundation。修复若确需改 Foundation，应递增版本并重新检查所有受影响组件。

## 12. Component / Pattern / Design Spec 与 State Matrix

三层规格各有职责：

- **Component Spec**：组件 anatomy、变体、token 引用、内容边界、交互、适用状态及规则。
- **Pattern Spec**：多个组件如何共同完成任务，包括导航、筛选、保存、反馈与恢复路径。
- **Design Spec**：页面区域、组件实例、数据契约、路由或流程、响应式行为、参考绑定、状态矩阵与验收标准。

只定义当前页面需要的组件，避免先建设完整 DS。移动端无需硬套 hover；桌面键盘 focus 也不能漏掉。组件状态按实际交互能力选择，业务状态与组件状态分别建模。

| 场景 / 状态 | 触发条件 | 必要呈现与行为 | 恢复 / 后继 | 验证方式 |
|---|---|---|---|---|
| home.default | 已有推荐数据 | 推荐区、搜索、保存与继续入口按层级显示 | 进入目的地或行程 | 截图 + 点击 |
| home.loading | 首次请求未完成 | 占位区域稳定，避免明显布局跳动 | 成功或错误 | 固定 loading fixture |
| home.first_time.empty | 无历史行程 | 首次引导，不显示伪造历史 | 开始规划 | 场景 fixture |
| search.error | 搜索请求失败 | 可理解的反馈、保留输入与重试 | 重试成功 / 再次失败 | 失败注入 |
| home.offline | 网络不可用 | 说明可用缓存范围及限制 | 联网后恢复 | 离线模拟 |
| save.pending / failed | 保存请求未完成或失败 | 明确状态、防止重复提交、失败后可恢复 | saved / retry | 交互断言 |

矩阵示例不代表所有页面必须实现这些状态；适用性由 Context 决定。没有参考证据时可依据项目规则补全，但要标记为设计推导，不能声称来自截图。

每条验收项必须可定位，例如：`home.header.title` 引用 typography.title；搜索错误时保留输入；目标视口下主要 CTA 不被底部导航遮挡。避免仅写“视觉接近、体验良好”。

## 13. Screenshot / Visual Comparator 与 Targeted Repair

### 13.1 建立稳定比较条件

固定 viewport、DPR、页面状态、数据 fixture、字体加载和截图范围；对动画、时间、随机内容采用可重复处理。Primary 与截图尺寸不一致时，先明确缩放或区域映射。浏览器渲染不具备对原生行为的完整证明能力，原型的验证范围应写入报告。

Comparator 比较的是 **Visual Contract**。被 ADAPT / IGNORE 的内容不按像素一致要求评分；动态图片和文案可 mask，但必须保留其区域大小及视觉重量检查。

### 13.2 量测方法

对数值约束 j，目标值为 `t_j`、观测值为 `o_j`、容差为 `τ_j`：

```text
error_j = abs(o_j - t_j)
pass_j = error_j <= τ_j
normalized_error_j = error_j / scale_j
```

`scale_j` 与容差由契约预先指定，避免用同一误差标准比较字号和页面宽度。布局使用归一化 bounding boxes，间距与字号优先读取 DOM / computed styles，截图补充检查裁切、遮挡、换行和视觉面积比例。像素差或感知相似度可辅助，但不能替代任务、状态与结构检查。

视觉重量可用明确区域占比等 proxy；难以可靠量化的审美判断标为人工复核项，不伪造精确得分。最终也不应输出没有基准定义的“90% 像”。

```json
{
  "id": "comparison_01",
  "spec_version": "1.0",
  "viewport": {"width": 390, "height": 844},
  "state": "home.default",
  "findings": [
    {"id": "f01", "path": "home.content.padding_inline", "priority": "P0", "expected": 16, "actual": 24, "unit": "css_px", "tolerance": 2, "status": "fail", "measurement": "computed_style"},
    {"id": "f02", "path": "home.title.font_size", "priority": "P0", "expected": 28, "actual": 28, "unit": "css_px", "tolerance": 1, "status": "pass", "measurement": "computed_style"}
  ]
}
```

### 13.3 Targeted Repair

RepairPlan 应列出 finding IDs、允许改动的文件/组件/token、期望值、保留项、依赖和验证步骤。例如只把页面 padding 从 24 改为 16，不同时替换配色或重排导航。

先修 P0 的宏观布局、比例、间距、层级和密度，再修 P1。修复共享 token 时检查使用该 token 的相关页面；局部错误优先局部修复。每轮保存 patch 和前后截图，检查旧问题是否解决及是否产生回归。重新设计或更换 Primary 属于重新建立规格，不能伪装成小修。

## 14. Reference-to-Mobile-Prototype Skill 与日常轻量流程

本节是拟建 Skill 的职责说明，不表示本次已经创建或安装该 Skill。

输入：1–3 张参考图、页面需求、目标移动端视口、必要状态与现有项目约束。输出：参考分析、Foundation、组件/页面规格、可运行原型、目标视口截图和差异报告。

固定流程建议：

1. 查看参考图，确定 Primary 与局部参考；输入不足时明确假设。
2. 提取 anatomy、比例、层级、密度与组件 inventory。
3. 标记 COPY / ADAPT / IGNORE，并锁定当前页面的七类 Foundation。
4. 定义本页组件、核心交互及 State Matrix。
5. 实现原型，生成固定视口与状态截图。
6. 根据契约比较，执行有上限的局部修复，交付结果与未解决项。

Web 品类页面可在步骤 2–4 中复用 Category Blueprint，并生成 Asset Brief；在实现前准备对应素材包和接近真实的内容。只有需要新视觉方向时才额外制作完整设计稿，已有验证骨架可直接配置。素材必须经过页面内裁切与窄屏验证，不能只检查单张图片。

日常不用启动完整多来源检索：用户已给参考图时可以从 Reference Analyzer 进入；缺失状态或规则时再定向补证据。简单页面可把分析与规格合并为一份短文档，但不能跳过参考检查、基础值决定和截图验证。

建议产物路径如下，具体由项目约定：

```text
design/reference-analysis.json
design/design-foundation.json
design/design-spec.json
implementation/
qa/screenshots/
qa/reference-comparison.md
```

职责分工：`AGENTS.md` 放项目长期规则与入口；Skill 放重复执行步骤；DS Library 放可检索规则；Project Prompt 放本次业务需求；ReferenceSet 放此次参考及选择理由。避免把所有知识放进一份巨型提示词。涉及具体运行环境或工具能力的实现，应在真正建设 Skill 时验证。

## 15. MVP 节点与实施优先级

### P0：先解决“参考图到原型不稳定”

优先建设 **Reference Analyzer → Design Foundation → Design Spec → Screenshot / Visual Comparator → Targeted Repair**。用人工选定的 Primary 跑通闭环，减少检索变化带来的干扰。Foundation 首轮重点验证 Grid、Spacing、Typography、Density、Component Sizing，同时仍给 Surface 与 Color 明确值。

验收：相同参考与 fixture 可以重复生成和比较；差异能定位到属性；P0 修复不破坏已通过项；记录首轮缺陷数与修复轮次。此阶段不需要建设大型参考数据库。

v1.2 的首个 Web 试点：选一个图片驱动的品类页面，沉淀一个 Blueprint 和一套 Asset Brief / Pack，跑通上述闭环；再用第二套品牌与内容复用。建设与评估细节见第 22–25 节，不在首轮扩建全品类库或自动化全网素材采集。

### P1：补齐最小 Query QA

实现 Context / CoverageTarget、受控 QueryBundle、精确 signature 去重、weighted coverage、硬约束 gate、Source QA 和最多两轮 targeted query repair。接入一个实际可用的产品参考来源和一个规则来源；其他 adapter 按需求逐步加入，不用来源数量充当质量指标。

验收：分数可重算、缺口可定位、重复不能提高 raw coverage、偏题不能靠覆盖抵消、关键状态缺失不能通过。

### P2：Evidence QA 与选择闭环

建立 EvidenceItem、实际覆盖矩阵、Reference Ranker、DS 的 Profile / Atomic Rules / Component Capability，以及来源与设计决策追溯。

验收：能区分“计划覆盖但没找到”与“证据已核验”；Primary 与 Secondary scope 无冲突；未知证据不会被标记已完成。

### P3：扩展多样性与数据反馈

加入 embedding 候选去重、Visual DNA 近似距离、层级 context、多来源预算优化及离线评估。先保留固定规则，再用标注数据校准，不让线上反馈直接改写 gate。

建议追踪：关键证据覆盖率、重复查询率、无效检索率、首轮 P0 缺陷数、平均修复轮次、修复后回归率、成本和时延。评估固定样本集并保留独立验证集，避免调参只改善同一批案例。

## 16. 推荐数据对象与 JSON Schema

### 16.1 对象关系

```text
IntentProfile → ContextProfile → CoverageTarget
    → QueryBundle → QueryQAReport → RetrievalRun → EvidenceItem
    → EvidenceQAReport → ReferenceSet → ReferenceAnalysis
    → DesignFoundation → DesignSpec / StateMatrix
    → PrototypeBuild → ComparisonReport → RepairPlan / RepairResult
    → FinalReview → FeedbackEvent
```

v1.2 新增关系：`CategoryBlueprint → BlueprintSelection → DesignSpec`；`DesignSpec 素材槽位 → AssetBrief → AssetCandidate → AssetQAReport → AssetPack → PrototypeBuild`。`AssetQuery` 与原有证据查询共享 adapter、执行日志和预算设施，但分开记录目标与覆盖率，详见第 24 节。

通用字段建议：`id、schema_version、run_id、created_at、parent_ids、status`。可计算报告追加 `policy_version、input_hash、extractor_version`；来源内容追加 `source_locator`。不同维度统一使用 `task / pattern / scene / states / context / visual / reference_intent`，避免 `state` 与 `states` 在接口中混用。

### 16.2 CoverageTarget 的可校验最小 Schema

以下为 JSON Schema Draft 2020-12 的核心对象示例；其他对象按同样方式补充。权重之和、跨对象引用、关键项与预算可行性仍需应用层验证。

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "CoverageTarget",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "schema_version", "context_id", "targets"],
  "properties": {
    "id": {"type": "string", "minLength": 1},
    "schema_version": {"type": "string"},
    "context_id": {"type": "string"},
    "targets": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "dimension", "weight", "critical", "applicable", "acceptance_rule"],
        "properties": {
          "id": {"type": "string", "minLength": 1},
          "dimension": {"enum": ["task", "pattern", "scene", "states", "context", "visual", "reference_intent"]},
          "weight": {"type": "number", "exclusiveMinimum": 0},
          "critical": {"type": "boolean"},
          "applicable": {"type": "boolean"},
          "exclusion_reason": {"type": "string", "minLength": 1},
          "acceptance_rule": {"type": "string", "minLength": 1}
        },
        "allOf": [
          {
            "if": {"properties": {"applicable": {"const": false}}},
            "then": {"required": ["exclusion_reason"]}
          }
        ]
      }
    }
  }
}
```

目标实例片段：

```json
{
  "id": "ct_travel_v1",
  "schema_version": "1.0",
  "context_id": "ctx_travel_v1",
  "targets": [
    {"id": "task.discover_destination", "dimension": "task", "weight": 0.35, "critical": true, "applicable": true, "acceptance_rule": "query 必须明确寻找目的地发现任务的证据"},
    {"id": "states.search.error", "dimension": "states", "weight": 0.25, "critical": true, "applicable": true, "acceptance_rule": "证据目标必须是搜索失败反馈及恢复路径"}
  ]
}
```

此实例仅展示字段，不是第 6 节完整分母。不同阶段根据规则定义分别核验计划、证据与实现，不能用同一个 boolean 混记。

### 16.3 QA Report 与 RepairPlan 示例

```json
{
  "id": "qa_travel_v1",
  "stage": "query",
  "policy_version": "mvp-1",
  "qa_status": "repair_required",
  "approved_query_ids": ["q01", "q02", "q03"],
  "rejected_queries": [{"query_id": "q07", "reason_code": "intent_duplicate", "duplicate_of": "q01"}],
  "coverage_report": {
    "task": {"raw_score": 0.85, "covered_count": 3, "required_count": 4, "missing": ["task.continue_trip"]},
    "pattern": {"raw_score": 0.8, "missing": ["pattern.saved_trip_entry"]},
    "states": {"raw_score": 0.65, "missing": ["states.home.offline", "states.home.first_time_empty"]}
  },
  "repair_plan": {
    "scope": "query_bundle",
    "keep": ["q01", "q02", "q03"],
    "drop": ["q07"],
    "generate": [{"target_id": "states.home.offline", "target_source": "mobbin", "reference_intent": "state_reference", "reason": "补齐离线浏览证据计划"}],
    "max_rounds": 2
  }
}
```

该报告为结构示例，省略了支持映射与完整目标明细。正式报告必须记录所有 `target_id → query_id / evidence_id / check_id` 关系，使每个分数都可由保存的输入重算。

关键应用层约束：ID 唯一且引用存在；已拒绝查询不计入有效 coverage；state 绑定具体 scene；一个页面只有一个 Primary；Secondary scope 不冲突；实现引用的 token 存在；修复只能消费当前版本的 finding；不得把过期截图用于当前版本的 gate。

## 17. QA Gate 与修复终止条件

### 17.1 Gate 建议初值

| Gate | 建议规则 | 失败处理 |
|---|---|---|
| Context Ready | 目标、权重、关键项、适用状态与预算一致；无影响核心任务的未决冲突 | 完善 Context，必要时请求产品决策 |
| Query QA | 无硬约束冲突、无关键未知；关键目标全部覆盖；task ≥ .90、pattern ≥ .80、scene ≥ .80、states ≥ .75、context ≥ .90 | 定向补 query，最多两轮 |
| Diversity | 可避免 intent duplicate ≤ .20、semantic duplicate ≤ .25；视觉探索满足已声明方向与可行集中度上限 | 回收重复预算、补缺失方向 |
| Source | 当前目标要求的来源角色均有可执行计划 | 更换适配或显式记录来源缺口 |
| Evidence QA | 关键目标有已验证支持；Primary 可用；规则与参考适配范围明确 | 局部重检索，不能沿用 planned score 放行 |
| Foundation / Spec | 七类基础值明确；无未解决硬冲突；关键 State Matrix 与验收项齐全 | 补规则或设计决策 |
| Visual / UX | P0 必须通过；P1 按项目 policy；关键交互与恢复路径通过；未知检查不得视为 pass | Targeted Repair |
| Final Review | 当前实现可运行；所需视口与状态验证完成；无阻断项；限制如实记录 | 修复或交付未完成状态及原因 |

原讨论的 `intent preservation ≥ .90` 可保留为提交质量诊断，但下游必须剔除所有硬约束冲突项。原讨论的四来源全部覆盖与 concentration ≤ .40 不作为通用硬要求，必须根据任务、可用来源和方向数配置。

**分数不能相互抵消。** task 高分不能抵消关键 error 状态缺失。阈值、目标和优先级在一轮评估前固定；更改必须版本化并说明原因。

### 17.2 终止与升级策略

Query repair 默认最多两轮；visual repair 建议默认最多两轮，可按任务预先配置。检索重试也要有独立的请求数、时延与成本上限。

满足任一条件即停止自动循环，并输出明确状态：

1. 所有必须 gate 通过：`passed`。
2. 达到轮次、请求或成本上限且仍有缺陷：`budget_exhausted`，保留最佳有效版本与未解决项。
3. 连续两次比较没有有效进展，或相同 finding 反复出现：`stalled`，回到根因分析，不继续随机重做。
4. 需要更换 Primary、修改硬约束或大幅调整 Foundation：`decision_required`，列出具体冲突、影响和建议。
5. 来源不可用、缺失必要素材或验证环境失败：`blocked`，区分工具问题与设计问题。

进展定义应固定：关键缺口减少，或 P0 违规数量下降；同数量下可比较归一化误差，且不能引入新关键回归。达到上限不等于通过。最终输出完成项、失败项、证据、版本及下一步动作，禁止用泛化高分掩盖未完成工作。

## 18. Codex 实现交接与数据反馈

建议按纯函数评分器、来源 adapter、状态编排器、参考分析与规格、原型验证五个边界拆分。评分器不调用 LLM；它只消费已归一化并带验证状态的输入，返回分数明细和 finding。编排器控制修复次数与版本流转，避免任意节点自行无限重试。

最低必要测试用例：

- task 示例计算 .85、pattern .80、states .65；空集合与不适用维度处理正确。
- 新增重复 query 不提高 raw coverage；意图重复与语义重复能够分别报告。
- 单个 error 查询不自动覆盖全部场景；只有 planned evidence 的目标不进入 verified coverage。
- 硬约束冲突和关键未知均不能通过；analogy scope 只豁免明确无关的上下文检查。
- A / A′ / B 不能覆盖要求的 A / B / C 三个方向；两个方向的预算不会被 .40 集中度阈值永久阻塞。
- 修复仅影响允许范围；过期 finding 被拒绝；共享 token 修改触发相关回归检查；达到上限输出未通过状态。

FeedbackEvent 建议记录需求类型、Query 与证据缺口、参考选择及弃用理由、实际 token 决策、首轮差异、每轮 repair、成本、时延、最终接受情况和策略版本。用户偏好、规则核验结果、模型推断分字段保存，避免把“用户喜欢”当成“规则正确”。

闭环优化顺序是：先找稳定复现的失败类别，再调整目标词表、adapter、提取规则或预算；用固定验证集确认改善后发布新 policy。沉淀的核心资产应是可复用的场景—证据映射、Foundation 决策和修复案例，而不只是更多查询文本。

## 19. 参考库建设与单次项目执行

参考库建设持续进行，不是每个项目必须先完成的前置工程。产品网页、Mobbin、Design System、视频提供不同类型的证据，统一进入参考资产层，再按项目需要检索。

| 来源 | 建议沉淀 | 证据边界 |
|---|---|---|
| 网页 | URL、时间、视口、状态截图、页面区域、必要操作记录 | 单个视口不能证明响应式规则；实际操作才能验证交互 |
| 产品视频 / 录屏 | 原始定位、时间段、操作、前后状态、反馈时序 | 宣传剪辑不能直接证明真实产品行为 |
| Mobbin | 来源定位、screen / flow、截图、任务与场景标注 | 单张静态图不能证明完整流程 |
| Design System | 系统与版本、规则原文定位、适用组件和条件 | 规则存在不等于当前实现已经遵守 |

每项资产先建立 Reference Card，记录 UX problem、applicable_context、anti_context、patterns、Visual DNA 和采集信息；再把有复用价值的局部提取成 Pattern Card 或 Atomic Rule。所有提取结论关联截图区域、视频时间段或规则位置，并区分 observed、measured、inferred、unknown。

网页中的 spacing、字号、颜色先存为 Foundation 候选。被具体项目选中并解决冲突后才成为锁定 tokens。Primary / Secondary、COPY / ADAPT / IGNORE 和 selection_reason 也应在项目选择层确定；资产层可以保留建议，不能永久固定其角色。

```text
持续资产建设：来源 → 原始证据 → Reference Card → Pattern / Rule / Foundation 候选

单次项目执行：需求 → CoverageTarget → 已有资产轻量匹配 → EvidenceNeed
            → QueryBundle → Query QA → Retrieval → Evidence QA
            → ReferenceSet + DecisionLog → Foundation + Spec → 实现与验证
```

已有资产轻量匹配仅查询项目已绑定证据与库内结构化索引，不要求先跑完整外部搜索。元数据匹配只能产生 candidate_available；内容核验完成后才算 verified。用户给定的参考可以直接进入核验与分析，没有缺口时允许跳过 Query Builder。

## 20. 六项执行契约补充

### 20.1 CoverageTarget：目标如何产生、接受与变更

Context Builder 根据四类来源提出目标，并保存明确理由：

| origin | 依据 | 接受方式 |
|---|---|---|
| user_explicit | 用户明确需求 | 直接纳入；有矛盾时记录冲突 |
| task_dependency | 完成任务必需的行为或状态 | 由可追溯的任务依赖或状态规则推导 |
| project_rule | 项目业务规范、组件规则 | 记录规则 ID 与适用条件后纳入 |
| exploration | 可选视觉或产品方向 | 在探索预算内纳入，不挤占关键目标 |

LLM 可以提出候选，接受判定由明确需求、项目规则与已配置的决策权限完成。常规可推导项可自动接受，不要求每项都询问用户；涉及业务范围、互相冲突的硬约束或关键未知项时，交给指定产品负责人决策。

状态使用 proposed / accepted / rejected / superseded。每项记录 accepted_by（用户、规则或配置的角色）、acceptance_basis 和 target_version。critical 表示缺失会阻断，不等同于“权重比较高”。权重与适用性在当前评估前固定；更新需产生新目标版本，并使依赖它的 QA 报告失效。

建议在第 16 节 CoverageTarget 的 item schema 中新增 origin、origin_ref、reason、decision_status、accepted_by、acceptance_basis 字段；若继续使用 additionalProperties=false，必须同步升级 schema，不能只在实例中添加字段。

```json
{
  "id": "states.save.error",
  "target_version": "1.1",
  "dimension": "states",
  "scene_id": "save_destination",
  "origin": "task_dependency",
  "origin_ref": "task.save_destination",
  "reason": "收藏需要持久化，失败后应有反馈与恢复路径",
  "critical": true,
  "weight": 0.25,
  "applicable": true,
  "decision_status": "accepted",
  "accepted_by": "rule:async_mutation_recovery_v1",
  "acceptance_basis": "本项目保存动作依赖异步请求",
  "acceptance_rules": {
    "query": ["明确寻找收藏或等价保存操作的失败反馈与恢复证据"],
    "evidence": ["实际支持失败提示", "实际支持状态恢复或重试行为"],
    "implementation": ["失败时正确呈现反馈", "保留可恢复状态并支持规定动作"]
  }
}
```

该对象是扩展字段示例，需使用升级后的 schema。不能因状态难找就删除目标，也不能因低风险产品就假设网络请求永远成功。

### 20.2 Taxonomy / Schema：统一词表与关系

正式接口固定如下关系：

- task：用户动作；scene：动作所处情境；state：该场景或组件的状态。
- pattern：解决问题的设计组织方式；reference_intent：要取得的证据类型。
- source：检索渠道；artifact_type：返回载体，例如 screenshot、flow、video_segment、rule。

`reference_intent` 统一为 screen_reference、flow_reference、interaction_reference、state_reference、component_reference、visual_reference、design_system_reference。此前对话中的 pattern_reference 不纳入枚举；要找 pattern 时应同时指定相应证据类型和 pattern 字段，例如：

```json
{
  "reference_intent": "screen_reference",
  "pattern": "continue_trip_entry"
}
```

报告维度使用 states，单个场景记录中的状态字段可使用 state；它们各司其职，不能在同一接口中随意替换。词表保存 taxonomy_version、别名映射和弃用记录。未知标签先标注待归一化，不能临时创造标签并自动参与评分。

所有对象必须引用稳定 ID，禁止靠自由文本串联。一个 CoverageTarget 可以对应多个 EvidenceNeed；每个 need 聚焦一个目标与一种获取目的。一个 EvidenceItem 可以支持多个 need，但每条支持关系必须单独核验。

### 20.3 EvidenceNeed 与 EvidenceItem：缺口不是证据

EvidenceNeed 是“目标要求与已核验证据之间的差距”。建议字段如下：

```json
{
  "id": "need_save_error",
  "target_id": "states.save.error",
  "target_version": "1.1",
  "reference_intent": "interaction_reference",
  "pattern": "save_failure_recovery",
  "status": "missing",
  "priority": "high",
  "required_claims": ["failure_feedback", "recoverable_state", "retry_behavior"],
  "candidate_evidence_ids": [],
  "verified_support_ids": [],
  "source_preferences": ["design_system", "product_recording"],
  "allowed_analogy_scope": ["equivalent_async_save_action"]
}
```

状态为 missing / candidate_available / partially_supported / verified / unavailable / not_applicable。not_applicable 必须引用目标变更决定，unavailable 不能当作已覆盖。

EvidenceItem 保存原始材料及来源；EvidenceSupport 保存“材料是否支持当前 need”的判断。两者分离，避免一张图被笼统标为 verified 后自动支持全部目标。

```json
{
  "evidence_item": {
    "id": "ev_save_01",
    "source": "product_recording",
    "source_locator": "asset:recording_01",
    "artifact_type": "video_segment",
    "segment": {"start_seconds": 12, "end_seconds": 20},
    "query_ids": ["q_save_error_01"],
    "content_version": "capture_01",
    "observed_claims": ["failure_feedback", "recoverable_state"],
    "unknown_claims": ["retry_behavior"]
  },
  "evidence_support": {
    "id": "support_01",
    "evidence_id": "ev_save_01",
    "need_id": "need_save_error",
    "target_version": "1.1",
    "status": "partially_supported",
    "verified_claims": ["failure_feedback", "recoverable_state"],
    "missing_claims": ["retry_behavior"],
    "verification_method": "observed_recording",
    "verification_policy": "evidence-v1"
  }
}
```

以上定位为示意资产引用，不代表已经采集该视频。生产对象还需时间、采集与审核记录。目标是否完成按 required_claims 的核验并集判定，可由多个证据共同满足，不能因为搜到一个结果就置为 verified。

### 20.4 ReferenceSet + DecisionLog：从找到资料到作出选择

ReferenceSet 保存页面级 Primary、Secondary、适用范围和项目继承策略；DecisionLog 保存为何采用、拒绝或调整某条参考规则。

最小 DecisionLog 字段：decision_id、scope、issue、options、selected_option、reason、support_ids、constraint_refs、affected_spec_paths、decision_owner、status、version。

例如主参考卡片比例与现有项目 token 不一致，应先判断比例是否属于必须继承的 P0、是否允许项目级覆盖、影响哪些组件，再给出明确决定。不要自动取平均值。无法解决的硬冲突进入 decision_required；可以按既定优先级解决的常规选择自动执行并留痕。

### 20.5 DesignFoundation + DesignSpec：让证据进入可验收实现

每条关键规格都应关联来源或设计决定，以及验证方式。至少记录 spec_path、value / behavior、support_ids、decision_id、priority、verification_method、tolerance 或 interaction assertion。

例如收藏失败的规格应明确：触发条件、显示反馈、是否回滚乐观状态、输入或选择保留规则、重试入口、重复提交控制。不能只写“参考视频实现错误状态”。

没有直接产品证据但有可靠项目规则时，可以记录 rule-derived 决策；缺少两者时标记 assumption。关键 assumption 按 gate 处理，不得借由规格生成把未知变成已验证。

实现后的验证需要明确以下链路：

```text
target_id → need_id → evidence_support_id → decision_id
          → spec_path → implementation_locator → verification_check_id
```

### 20.6 RunState + RepairPolicy：控制执行与版本失效

编排器维护当前节点、输入版本、尝试次数、预算使用、未解决 finding、最佳有效产物与下一步动作。运行状态使用 queued / running / repair_required / passed / blocked / decision_required / budget_exhausted / stalled；恢复执行沿用已有产物，不能重新生成整套来绕开失败。

RepairPolicy 分别配置 query_repair、retrieval_attempts、visual_repair 和总成本上限。第 17 节的两轮是 query 与 visual 的默认修复次数，不等于总共只能发出两条检索请求。

核心控制规则：

- 重试之前确定失败类型：工具异常、无结果、不相关、部分证据、规格冲突或实现偏差。
- 相同请求使用规范化请求与来源版本形成缓存键；外部瞬时失败按策略重试，无效结果不无条件重复请求。
- need 已 verified 且内容与上下文版本仍有效时，不重复检索。
- target 变更使相关 coverage 与 support 重新评估；Foundation 变更使相关实现检查失效；代码变更使受影响截图失效。
- 达预算上限输出未解决项；只有当前版本的必须 gate 全部通过才能 passed。

## 21. Query Builder 的可执行最小流程

输入为 ContextProfile、已接受的 CoverageTarget、EvidenceNeed、已有资产索引、SourceCapabilities、DiversityBudget 和 RepairPolicy。Query Builder 不负责自行调整产品目标，也不把自己的 covers 标签作为最终核验结果。

1. 对已接受目标检查已有 EvidenceSupport；生成缺失或部分支持的 needs。
2. 按 critical、业务优先级和缺口排序；可选视觉探索使用独立预算。
3. 为 need 选择来源角色、预期证据与必要适配；允许受控跨领域借鉴。
4. 生成查询表达与结构化过滤；每条关联 need_ids、expected_claims、预算 bucket 和失败后策略。
5. Query QA 校验 schema、意图、来源能力、重复与 planned coverage，再执行检索。
6. Evidence QA 核验具体 claims；缺失部分成为 repair 输入，保留其余有效查询和证据。

```json
{
  "id": "q_save_error_01",
  "need_ids": ["need_save_error"],
  "source": "design_system",
  "query": "asynchronous save failure feedback retry state recovery",
  "reference_intent": "interaction_reference",
  "pattern": "save_failure_recovery",
  "expected_claims": ["failure_feedback", "recoverable_state", "retry_behavior"],
  "budget_bucket": "states",
  "priority": "high",
  "analogy_scope": "equivalent_async_save_action",
  "fallback_policy": "if_incomplete_search_product_flow"
}
```

fallback 是条件计划，不应与主请求无条件同时执行；具体参数仍以 source adapter 能力为准。若已经找到反馈和回滚证据，下一轮只寻找重试行为。

MVP 实现顺序补充为：先锁定 taxonomy 与三个核心对象 CoverageTarget / EvidenceNeed / EvidenceItem，并建立 EvidenceSupport 关系；再实现规则评分与 Query 编排；最后接通项目参考选择、规格和验证追溯。这是数据底座的实施顺序，不改变第 15 节优先解决参考图到原型质量的产品目标。

新增验收用例：目标不能为提高分数被静默删除；pattern_reference 被 schema 拒绝或经显式迁移；候选资产不等于核验证据；多项证据可以共同满足一个 need；部分支持只产生剩余缺口；跨项目参考角色互不污染；输入版本变化会使下游过期结果失效；无需检索时可直接进入参考选择与规格阶段。

## 22. 从 3D 资产准备迁移到 Web 品质建设

用户在 3D 工作中观察到“Blender 建模 + 图像生成贴图 + 代码模型组装”比直接给代码模型 prompt 更稳定。Web 可采用类似的职责分解；本文将其视为待验证的方法假设，不宣称已测得同等提升，也不推断不同模型间的胜负。

| 3D 环节 | Web 对应产物 | 减少的临时设计决策 |
|---|---|---|
| 建模 | Category Blueprint、结构化设计稿或经过验证的代码骨架 | 页面区域、比例、层级、组件组合 |
| 贴图制作 | 按槽位准备的摄影、产品图、插画、纹理 | 主体、色调、裁切、画面留白 |
| 材质与灯光设定 | Typography、Color、Surface 与视觉层级 | 整体视觉语言与视觉重量 |
| 导入组装 | 将规格、真实内容和素材接入组件 | 数据、状态、交互、响应式 |
| 渲染检查 | 浏览器截图、实际操作和局部修复 | 实现与设计目标之间的偏差 |

重点是让中间产物真正确定设计信息，不是单纯增加一次模型调用。把模糊 prompt 原样转为设计图，仍可能留下尺寸、状态、内容和交互的大量未知。

图片驱动的电商、旅游、餐饮、建筑和作品集页面，优先建设骨架与素材包；工具类产品优先建设密度、排版、数据结构、组件与状态。Figma 设计稿可作为结构化交接载体，但不是所有项目的必经阶段。已有成熟代码骨架时可直接配置，随后验证项目差异。

## 23. Category Blueprint：建设、复用与验证

### 23.1 定义及与其他资产的区别

Category Blueprint 是某类页面在特定任务和内容条件下的可复用结构，包含设计规格，最好附带可运行代码样板。命名范围采用“品类 × 页面类型 × 结构变体”，例如“时尚电商 × 商品列表 × 图片优先”。不能用一个泛化“电商模板”覆盖首页、列表与详情。

| 对象 | 决定什么 |
|---|---|
| Design System | 基础 tokens、组件规则与状态能力 |
| Pattern | 一个局部 UX 问题的解决方式 |
| Category Blueprint | 页面任务、区域组织、内容契约、组件组合与响应式规则 |
| ReferenceSet | 本项目采用的证据及其主次、继承范围 |
| Asset Pack | 本项目实际装配的视觉内容 |

品类还原度来自与任务匹配的结构和内容。例如服饰列表应体现商品浏览、筛选、图片与价格层级；不能靠通用落地页更换配色来证明品类适配。品类本身也允许不同变体，不应把单个品牌习惯上升为通用规则。

### 23.2 建设步骤

1. **限定任务与边界。** 写明页面类型、主要任务、内容特征、适用及反适用条件。
2. **检查真实参考。** 初期使用一个主参考及两三个同类页面；分别查看宽屏、窄屏和关键交互。这是起步采样方案，不代表足以证明全行业规律。
3. **提取五部分。** 页面区域、内容字段与优先级、比例尺寸、组件联动、响应式行为。每条结论关联来源和 observed / measured / inferred 状态。
4. **区分共性与变体。** 将任务必需结构与品牌表达分开；不同筛选布局保留为变体，不取平均值。
5. **形成配置边界。** 标明固定结构、可配置项和可选模块；写明模块依赖和不兼容组合。
6. **制作真实内容样板。** 实现代码骨架，使用具有长短文本、不同图片与数据规模的 fixtures，检查内容极端值和状态。
7. **浏览器验证并版本化。** 记录视口、断点、截图、交互结果和限制；验证通过后才能标为 validated。
8. **第二次复用。** 更换品牌、内容和素材，检查原配置是否足够；若大量重写，调整边界后再验证。

### 23.3 固定、配置与可选内容

以图片优先的时尚商品列表为例：

- 固定结构：筛选结果与列表一致、商品信息层级稳定、空结果有恢复路径。
- 可配置项：内容宽度、列数、图像比例、字体、颜色、间距、信息密度。
- 可选模块：品牌简介、促销横幅、快速购买、收藏、编辑推荐。

固定项描述这个变体的承诺；需要改变时应明确创建变体或升级版本，而不是隐式破坏验收条件。断点根据内容何时无法合理容纳来决定，再保存为数值与布局切换规则。

```json
{
  "id": "fashion_listing_image_first",
  "schema_version": "1.0",
  "version": "0.1",
  "status": "draft",
  "category": "fashion_commerce",
  "page_type": "product_listing",
  "primary_tasks": ["browse", "filter", "compare", "open_product"],
  "applicable_context": ["image_led_apparel_browsing"],
  "anti_context": ["complex_spec_comparison"],
  "regions": ["header", "category_nav", "heading", "filter_sort", "product_grid", "pagination"],
  "layout": {
    "wide": {"columns": 4, "filter_mode": "sidebar"},
    "narrow": {"columns": 2, "filter_mode": "drawer"},
    "switch_at_css_px": 960,
    "breakpoint_status": "proposed"
  },
  "content_contract": {
    "image_ratio": "3:4",
    "required_fields": ["image", "name", "price"],
    "optional_fields": ["colors", "badge"],
    "title_max_lines": 2
  },
  "required_states": ["loading", "results", "no_results", "error"],
  "optional_modules": ["collection_intro", "quick_add", "wishlist"],
  "reference_ids": ["ref_listing_primary"],
  "implementation_ref": null,
  "validation_run_ids": []
}
```

该 JSON 是草案实例，尺寸和断点未验证。进入 validated 必须补齐真实引用、可运行实现、Foundation 绑定和验证记录；所有示例 ID 在实际项目中必须能够解析。

建议目录：

```text
blueprints/fashion-product-listing/
  blueprint.json
  foundation.json
  content-contract.json
  state-matrix.json
  references.md
  implementation/
  validation/
```

BlueprintSelection 保存 blueprint_id / version、项目 Context、适配理由、参数值、已启用模块和 OverrideLog。选择先检查硬兼容性，再比较目标覆盖和改动成本；没有合适骨架时允许新建，不为了复用而改变用户任务。项目修改不会自动回写通用库，需独立验证后发布新版本。

## 24. Asset Brief → 定向搜索 / 制作 → Asset Pack

### 24.1 先定义槽位，再寻找素材

模型可以对网页、图库或已连接资产库进行多轮定向搜索，搜索目标由 Asset Brief 约束。网页设计参考检索与可交付素材检索是两种工作：前者解释设计，后者提供实际要装配的文件。搜索结果缩略图、来源页面和可使用的原始素材也不能混为同一对象。

每个 slot 至少记录页面位置、内容主体、是否绑定真实实体、比例与分辨率需求、主体位置、文字留白、整组视觉要求、移动端适配及使用范围。真实商品、酒店或项目的详情图必须关联同一 entity_id，不能用视觉相近的不同对象拼接成一个真实实体。

```json
{
  "id": "brief_architecture_home_v1",
  "schema_version": "1.0",
  "spec_version": "1.0",
  "visual_direction_id": "warm_natural_architecture",
  "slots": [
    {
      "id": "home.hero",
      "required": true,
      "subject": "architecture_exterior",
      "entity_id": null,
      "truth_requirement": "concept_visual_allowed",
      "desktop_ratio": "16:9",
      "min_width_px": 2400,
      "composition": {"subject_position": "right", "text_safe_area": "left"},
      "set_constraints": ["natural_light", "warm_neutral", "consistent_photography"],
      "mobile_strategy": "separate_crop_or_variant",
      "allowed_production": ["owned_asset", "licensed_asset", "generated_concept"],
      "usage_scope": "public_website"
    }
  ]
}
```

上述为概念品牌演示需求。若页面展示真实建筑项目，必须提供对应 entity_id，并改为事实素材要求；生成图不能冒充真实案例。分辨率应结合最终显示尺寸和 DPR 计算，2400 不是所有页面的通用要求。

### 24.2 搜索与生产流程

1. 检查用户自有、已授权素材和既有 Asset Pack，复用仍有效的资产。
2. 将缺失 slot 转为 AssetQuery，按来源能力生成查询与筛选条件。
3. 收集候选，保留来源页面、原始素材定位、尺寸、实体信息和使用条件依据。
4. 先过滤内容错误、尺寸不足或使用条件不满足的候选，再检查构图与整组一致性。
5. 将候选装入页面，在目标视口检查主体裁切、文字可读性、真实内容密度和加载表现。
6. 不满足的 slot 定向重搜；允许制作且预算范围内时，使用同一 Brief 生成或制作缺失素材。
7. 保存最终文件、变体、裁切配置、来源及验证记录，生成 Asset Pack manifest。

整页生成图可用于方向探索，进入实现前仍需拆解；正文、按钮、表单和动态数据保持为真实网页元素。生成素材记录生成方式、输入参考和版本；实际使用条件仍需核对，不能因“生成”就自动认定 usable。

### 24.3 与 Query Builder 的接口边界

设计证据查询继续使用第 20 节的 reference_intent 枚举；AssetQuery 使用独立 kind 和字段，不新增 asset_reference 来污染原词表。

```json
{
  "id": "aq_hero_01",
  "kind": "asset_query",
  "brief_id": "brief_architecture_home_v1",
  "slot_ids": ["home.hero"],
  "source": "licensed_asset_catalog",
  "query": "architecture exterior natural light subject right copy space left",
  "hard_filters": {"min_width_px": 2400},
  "expected_checks": ["subject_match", "usable_for_project", "desktop_crop", "mobile_crop"],
  "budget_bucket": "hero_assets"
}
```

来源名称为示例 adapter，不代表已连接服务或支持该筛选。Source QA 按实际 capability 判定；不支持的筛选改为结果后检验，不能静默假定已执行。

两类查询共享运行日志、缓存、版本控制、候选去重和预算设施，但分别计算 evidence coverage 与 asset readiness。同一图片可以同时是参考和交付素材，但需独立保存这两种用途的判定。素材被选中不代表其证明了产品交互。

### 24.4 使用条件、真实性与集合质量

素材使用状态为 reference_only / permission_unknown / usable / rejected。公开可访问不等于允许交付使用；usable 必须记录适用于本次用途的依据，包括适用时的署名要求与限制。用户提供的素材也要保留其提供来源和已知使用范围，不凭空声称授权。

对素材做三组检查：

| 检查 | 内容 | 结果表达 |
|---|---|---|
| 单项可用性 | 文件可读取、尺寸、格式、主体、实体、用途条件 | pass / fail / unknown，附证据 |
| 整组一致性 | 色调、光线、背景、主体尺度、裁切、重复与内容覆盖 | 按 Brief 逐项判断；主观项保留理由 |
| 页面内适配 | 槽位尺寸、主体保留、标题可读性、宽窄屏、性能预算 | 视口与截图绑定的检查结果 |

不能用一个不透明的“美感 0.9”代替检查。可测量项由代码计算，审美适配用明确 rubric、证据与必要人工选择。颜色接近的图片仍可能内容错误；真实实体与使用条件属于硬 gate，不能由一致性高分抵消。

### 24.5 Asset Pack 契约

```json
{
  "id": "pack_architecture_v1",
  "schema_version": "1.0",
  "brief_id": "brief_architecture_home_v1",
  "spec_version": "1.0",
  "status": "candidate",
  "assets": [
    {
      "id": "asset_hero_01",
      "slot": "home.hero",
      "source_locator": "asset:owned_photo_01",
      "local_file": "assets/hero-desktop.webp",
      "usage_status": "permission_unknown",
      "usage_basis_ref": null,
      "dimensions": {"width": 2400, "height": 1600},
      "focal_point": {"x": 0.72, "y": 0.48},
      "variants": [{"viewport_role": "mobile", "file": "assets/hero-mobile.webp"}],
      "selection_reason": "主体在右侧，左侧具备放置标题的空间",
      "alt_strategy": "contextual_description",
      "qa_status": "pending",
      "check_ids": []
    }
  ]
}
```

这里是未通过 QA 的结构示例，文件名为 manifest 内相对路径，不表示已生成文件。生产版本需补真实文件、来源 / 获取时间、文件 hash、使用依据、变体尺寸与验证 ID。只有当前必需 slot 均通过才能将 Pack 置为 ready；装饰性图片的替代文本策略也应明确。

## 25. Blueprint / Asset QA、修复与实施验证

### 25.1 新增 Gate 与可计算指标

| Gate | 通过条件 | 修复入口 |
|---|---|---|
| Blueprint Fit | 核心任务与内容契约兼容；版本可用；项目差异明确 | 改配置、换变体或新建骨架 |
| Blueprint Validation | 规定视口、内容边界、状态与交互通过，来源和推断可追溯 | 骨架实现与规则修复 |
| Asset Brief Ready | 必需槽位、主体、实体真实性、显示需求与使用范围明确 | 补 Brief |
| Asset Pack Ready | 必需素材可用；使用条件已核验；文件及变体存在 | 定向搜索、获取或制作 |
| In-page Asset Fit | 当前 Spec 下裁切、可读性、窄屏与性能检查通过 | 改素材变体或局部布局 |

定义每个必需或适用 slot 的权重 w_s，全部必要单项检查通过时 a_s=1，否则为 0：

```text
asset_readiness = Σ(w_s × a_s) / Σ(w_s)
```

没有适用 slot 时为 null / not_applicable。必需 slot 必须全部通过，不能靠可选素材数量提高分数；permission_unknown、文件缺失和实体不符均不计为 ready。页面内检查单独记录，Pack Ready 不能代替 In-page Fit。

Blueprint 的品类任务与结构目标由 CoverageTarget 预先确定，沿用加权覆盖计算，不重新发明一个无依据的“品类还原度分数”。视觉接近程度仍按 Visual Contract 验证；主观品类感可以作为独立盲评结果，不能冒充客观量测。

### 25.2 失败分类与停止规则

沿用 RunState / RepairPolicy，为素材增加 max_search_requests、max_candidates_per_slot、max_generation_attempts、总成本与时间上限，数值在运行前配置。

- 检索内容不匹配：调整该 slot 的查询或来源。
- 尺寸或裁切不合适：寻找高分辨率版本、改变体；确需改布局则版本化 Spec。
- 整组不协调：只替换不满足集合规则的素材，不重做全部页面。
- 使用条件未知：核验原始来源或换候选，不能转存图片后跳过检查。
- 真实实体素材缺失：请求对应素材或明确缺口，不能用概念图冒充。
- 所有候选都不适合：检查 Brief 是否不合理，并记录修改决定。

素材 hash 或变体变化使相关页面检查失效；Blueprint / Spec 更新使受影响 slot 重新检查。达到预算或连续无进展时按第 17 节停止，保留最佳候选与缺口，不标记完成。获取素材和调用生成能力均限于当前授权及预算，不自动购买资产或订阅服务。

### 25.3 首轮对照实验

选择一个图片驱动页面，使用同一模型、产品需求、验收目标、目标视口与实现修复预算，比较：

| 组别 | 输入 |
|---|---|
| A | 直接产品 prompt |
| B | 主参考 + 明确 Design Spec |
| C | 品类 Blueprint + Design Spec + Asset Pack |

记录首轮 P0 违规数、任务 / 状态覆盖、素材适配问题、修复次数、回归数、总时延和成本。准备 Blueprint 与素材包的成本也计入端到端成本，另外记录复用后的边际成本，避免只统计代码生成阶段。

若 C 更好，仍不能据此单独证明是骨架还是素材带来提升。需要归因时，再补“Spec + Blueprint”和“Spec + Asset Pack”两组。多个案例及重复运行用于观察稳定性，不能用单次成功推断所有品类。通过质量门槛后，再用第二套品牌和内容验证骨架复用边界。

### 25.4 给实现团队的最小交接包

首次建设只需一个窄范围 Blueprint、一个项目选择记录、一个 Asset Brief、一套可用素材、可运行页面和一份验证报告。数据层新增 CategoryBlueprint、BlueprintSelection、AssetBrief、AssetQuery、AssetCandidate、AssetPack、AssetQAReport；所有对象按第 16 节的通用字段保存版本与上游引用。

上述 JSON 是接口实例，不是已实现的 JSON Schema。实现时需为新增对象建立 schema 与应用层校验，特别验证：slot ID 唯一、路径与 hash 有效、引用存在、usage_basis 与项目用途匹配、真实实体一致、必需变体齐全、过期检查不可用于放行。

新增回归样例：长商品名与价格变化不破坏网格；筛选转抽屉后状态保留；不同项目图片不能混作一个案例；reference_only 素材不能进入交付包；窄屏裁切失败会阻断相关检查；无需素材的工具页能够跳过 Asset 阶段；更换品牌后仍满足 Blueprint 的固定契约。
