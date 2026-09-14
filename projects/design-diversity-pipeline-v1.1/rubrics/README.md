# Rubric 使用与评分

rules.json 是规则定义，examples/review-result.json 是运行结果模板。规则的 checker_kind 表示应如何执行，不代表本包已有检测器。

各规则包含 node、applies_when、severity、required_inputs、assertion、pass_condition、on_unknown、repair_target、exceptions。运行结果另存 rule_id、run_id、status、actual、expected、evidence、environment、repair。

状态 pass/fail/unknown/not_run/not_applicable。blocking 失败阻塞其适用的阶段；视觉素材不足不一定阻塞结构开发，但必须阻塞完整视觉通过。not_applicable 必须给出上下文理由。视觉模型评审不生成伪精确总分。

## 方法与解释

- 确定性：引用、类型、布局算术、对比度的已知色值输入、依赖、schema、hash。
- 执行验证：实际点击、状态转换、键盘、焦点、网络、图片、viewport、reduce motion。
- 视觉评审：品类气质、层级、图像协调、结构与视觉多样性，记录区域和证据。
- 人工产品判断：业务分支和品牌等关键决策，默认值不得冒充授权。

权重和阈值在运行前锁定版本；不能为让结果通过而倒推权重。必须项不能被平均分抵消。每条评分报告已知维度覆盖比例。

## Anti-slop 例子

不是“禁止渐变”，而是“若渐变降低当前文字对比度或掩盖主要操作，则调整其使用区域/强度”。不是“禁止卡片”，而是“相同层级的内容被无必要多层容器包裹，打断阅读时合并”。

素材灰框适用于结构验证，但不能算视觉完成；synthetic 文案须标演示，不能制造真实评价。动效必须有任务作用，允许静态方向，不强制十页使用十种 Motion。

## 三种覆盖

Query覆盖：规格有没有写；Evidence覆盖：记录是否支持；Implementation覆盖：执行是否通过。结果用不同命名空间保存。对全体方案的顶层 not_run 不能掩盖某一页已有验证，按 run/candidate/check 保存并在汇总中说明未覆盖集合。

## v1.1四张检查单

功能R14；单页R11/R15/R20/R21/R22；同站R23/R25；方向R08/R17/R24。R19管理候选表和预览授权。R24声明完整批次前要求成对覆盖，0–3等级为有证据的主观量表，不是精确分数。规则是实现契约，本包校验器不自动执行浏览器检测。
