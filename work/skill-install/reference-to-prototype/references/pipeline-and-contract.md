## 3. 完整生成 pipeline

```text
Intent / Context
  → Query Builder → Diversity Review ↺ 仅补缺失 query
  → Retrieval：Mobbin / Design System / SD / PA
  → Reference Ranker → Reference Analyzer
  → Design Foundation → Component / Pattern Spec
  → Prototype → Screenshot Capture / Comparator
  → Targeted Repair ↺ 重新截图比较
  → Final Review → Data feedback
```

SD 沿用原对话中的“视觉语言来源”，PA 沿用“产品模式来源”；具体库名、字段和连接方式由项目配置，不假定缩写全称。

| 阶段 | 必要输出与检查 |
|---|---|
| Intent / Context | 用户、核心任务、场景、平台/实现形态、页面、状态、品牌、内容和成功条件；明确硬约束 |
| Query Builder | 每条 query 绑定 scene、UX problem、reference intent、来源；区分 screen、flow、state、component、visual、DS |
| Diversity Review | 检查任务、模式、场景、状态、视觉方向、参考用途覆盖；输出 covered/missing/over-represented/conflicting 和补搜 query |
| Retrieval | Mobbin 提供真实产品 screen/flow 证据；DS 提供规则；SD 提供视觉方向；PA 提供产品模式；保留来源、截图/片段及访问状态 |
| Reference Ranker | 先过滤硬约束，再比较任务、平台、密度、状态证据及可实现性；给出主次角色和选择/淘汰理由 |
| Reference Analyzer | 拆出区域、比例、对齐、留白、文字层级、组件组成、视觉重心、首屏密度；标注证据与未知项 |
| Design Foundation | 将分析转换成有单位、来源和端差异的 tokens；锁定优先级与容差，形成 Visual Contract |
| Component / Pattern Spec | 结构、内容、token 引用、状态转移、响应式和交互验收项 |
| Prototype | 先搭整体尺寸与层级，再填组件和内容；复用现有技术栈；核心操作能跑通，模拟数据明确标注 |
| Screenshot Comparator | 同条件截图，对照 reference + contract，逐项输出 PASS/FAIL/UNVERIFIED、差异证据和优先级 |
| Targeted Repair | 每轮修最重要的少量差异；明确范围和回归项，重新截图，不整页重新设计 |
| Final Review / Data feedback | 验证视觉、核心任务、状态和多端；保存结果、偏差原因、可复用经验 |

Coverage 必须有分母和证据：`已覆盖必需项数 / 必需项总数`，没有必需项则为 N/A。Query 覆盖只代表检索计划，不能等同于已找到参考或已实现状态；三者分别记录。重复度可用“同一场景 × UX 问题 × 参考用途 × 模式”的冗余条目占比辅助判断，不只比较关键词或 embedding。缺关键场景时，即使总覆盖率高也要补齐。

### 3.1 COPY / ADAPT / IGNORE 与 visual priority

| 决策 | 应写明的范围 |
|---|---|
| COPY | 高保真保留的布局比例、对齐、层级、密度和视觉节奏 |
| ADAPT | 按本产品重写的内容、数据、标签、操作、业务流程及跨端交互 |
| IGNORE | 无关导航、功能、参考品牌标识及未指定复用的专有素材 |

COPY 是视觉约束，不是自动复用素材的授权。用户提供且指定使用的品牌资源按任务处理。

Visual priority 与上述决策分开记录：

- **P0**：宏观布局、容器/组件比例、间距节奏、文字层级、信息密度。
- **P1**：按钮/行高、圆角、边框、图标、颜色层级。
- **P2**：细微装饰与不影响任务的细节。

这是默认排序，可按目标调整。文字和图片虽常为 ADAPT，仍要维持长度、行数、占位比例和视觉重量；不能随意填内容后要求像素一致。

### 3.2 最小 Visual Contract

```yaml
page: trip-home
platform: mobile-web
viewport: {width: 390, height: 844, unit: css_px} # 示例
references:
  primary: {id: A, scope: [layout, hierarchy, density, rhythm]}
  secondary: [{id: B, scope: filter_sheet}]
copy: [section_order, alignment, card_proportions]
adapt: [copy, data, actions]
ignore: [reference_logo, unrelated_navigation]
tokens:
  page_padding:
    value: 20
    unit: css_px
    source: A
    evidence: inferred
    confidence: medium
responsive:
  narrow: 单列；底部操作不遮挡正文
  wide: 按内容需求扩展，保持阅读宽度和信息顺序
acceptance:
  - {item: page_padding, priority: P0, target: 20, tolerance: 2, unit: css_px}
  - {item: primary_action, requirement: 可完成筛选并更新结果}
unknowns: [参考字体待识别]
```

执行时补上本页其余关键 tokens、比较环境和区域验收项。容差在比较前按任务确定；示例的 2px 不是所有项目的门槛。
