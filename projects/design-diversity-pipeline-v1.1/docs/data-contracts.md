# 数据契约：记录、映射、编译

## 术语

Query 有三种：reference_retrieval（设计证据搜索）、asset_retrieval（交付图片搜索）、generation（面向实现的设计请求）。不要将长 implementation prompt 与搜索关键词混在一起。

历史 PA 曾指页面组织，也可能指产品模式来源；本包一律拆为 page_architecture / product_patterns。visual_style 表示视觉方向。没有国际统一的“十种网页风格”标准。

## 知识层

| 对象 | 必需内容 |
|---|---|
| Goal / Task / Journey | 业务前提、成功条件、步骤、必要状态、恢复、范围 |
| PageArchitecture | 区域树、顺序、列关系、导航、行动入口、端间重排、固定/可变项 |
| Pattern / Module | 目的、输入输出、事件 schema、接口版本、状态 owner/consumer、依赖、条件与缺失行为 |
| Component | anatomy、变体、能力、状态矩阵、焦点键盘、内容限制 |
| Foundation | Grid/Spacing/Typography/Sizing/Surface/Color/Density，单位、测量/推导来源 |
| StyleProfile | 主导特征、Token 关系、素材语言、适用/不适用、身份锁、反例 |
| Palette | 语义颜色角色、实际前景背景配对、透明度/图像条件、计算结果；商品色卡不混 UI 色板 |
| Motion | trigger/target/from/to/properties/duration/easing/interrupt/exit/focus/reduced_motion/source |
| Content / Asset | 字段、长度、事实来源、真实/合成；素材文件、尺寸、版本、授权、裁切与槽位 |
| QualityRule | 上下文、触发、例外、检查、失败影响、修复目标 |
| ImplementationMapping | 代码位置、接口版本、配置入口、依赖、验证环境及范围 |

## 字段级来源与状态

证据记录：reference_id、source_url、captured_at、viewport、device_environment、locale、auth_state、business_state、artifact_path/hash。

claim：object_id、claim_path、claim_text、evidence_id、observation_basis、support_status（supported/partially_supported/refuted_at_capture/unsupported_in_saved_evidence/unknown）、推导方法。

decision_status（proposed/selected/rejected/superseded）与 implementation_validation_status（spec_only/implementation_available/validated_in_scope）另存。失败检索用 search_status；缺口用 resolution_status，不能复用 evidence_status 表示 open。

来源对象 → claim → 知识字段 → 适配决策 → resolved 字段 → 组件/资产 → check result。所有正式引用必须精确存在，不用通配符、拼接字符串或散文表示外键。

## 映射与组合

业务条件 → 可用骨架；骨架 → required/optional/forbidden modules；骨架＋Style → compatible/incompatible/unknown；模块事件 → 状态 owner；Token → CSS/组件参数；内容字段/资产文件 → slot；质量规则 → 区域/状态；变体 → 相对基准实际 diff。

DS 用 Profile、Atomic Rules、Component Capability；binding_mode、适用范围与选择原因必须明确。Foundation System 只选一个基底，可补充兼容规则。不要用某系统的 chip 规范自动判定所有尺码控件违规。

State Matrix 每行说明 owner、进入条件、UI、可用动作、退出事件、错误恢复、焦点、检验方法。条件消费者只有条件成立时要求 owner 存在，条件不成立时明确缺失行为；条件必须结构化可判断。

## 唯一来源

人工/模型生成的版本化候选配置是源；resolved 是本次冻结的完全展开快照；query、prompt、manifest 是派生产物。不要同时手改两层。库中的全量知识不直接灌进每份 prompt，只选择本次适用内容。

## 素材的尺寸与评审

按 slot + viewport + crop 定义 required_width/height、DPR 目标（项目选择）与主体限制。实际资产记录 file_path/hash、pixel_width/height、crop、source/license。不同端可指向不同文件，不机械把跨端最大宽高拼成一份超大要求。

数量以满足条件的唯一资产统计；同一图片不同文件名不能重复充数。评审包含 asset_hashes、criteria_version、reviewer、verdict、理由。资产改动后对应评审失效。无图片的头像/地图文字回退须显式选择，不能造假地图或身份。
