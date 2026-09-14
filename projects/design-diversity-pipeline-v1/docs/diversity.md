# 多样性、explore 与 refine

## 批次先规划

同品类、同页面类型还要锁业务前提。住宿单单元和多房型为不同分支，不把功能变多算成风格差异。每个方向分配骨架、产品模式、Typography、Palette、Density、Surface、Image Direction、内容强调和必要 Motion。

十页是用户数量目标，不是“十个国际风格类别”。建议起点：从六个适用家族中形成十套具体 Profile、覆盖三到四个有业务依据的 PA。只作可调整策略。强约束品类允许更少 PA，用视觉身份拉开区别，不硬加装饰。

风格家族组织知识、Profile 定义协调组合、Visual DNA 支持计算、截图验证感知差异。极简、扁平、深色、Bento、奢华描述不同维度，不是互斥分类。禁止无目的随机混搭。

## 距离与覆盖

对预先定义的可比较维度：D(a,b)=sum(wj*dj)/sum(wj)。数值 dj=min(abs(a-b)/(max-min),1)，范围须由策略确定；类别用预定义距离表或明确相等/不等，不能直接比较 ID。报告 known_weight/total_weight，未知值不当作最大距离。

结构、界面视觉、素材、交互距离分别报告。阈值为项目策略，需截图人工校准。十候选共 45 对，重点检查最近的一对；高平均值不能掩盖重复。字体家族名字不同不代表视觉不同，颜色微变也不能独立证明新风格。

Coverage(d)=sum(wi*ci)/sum(wi)，ci 默认为0/1，部分覆盖先定义。无目标 N/A。Query/Evidence/Implementation Coverage 独立：要求写到了、证据支持了、实际实现验证了是三种事实。

Drift 记录目标外改动的类型和违反的约束。可选归一化惩罚=sum(wi*vi)/sum(wi)，规则权重事先锁定，硬违规独立阻塞。Duplicate penalty 可按等价 query_signature 分组后的多余条目权重/总权重计算；跨来源或状态的互补证据不直接去重。不要拼成未经校准的质量总分。

query_signature={category,page_type,business_branch,task,state,pattern,evidence_purpose,source_capability}。semantic duplicate 是表达近似；intent duplicate 是证据用途重复，分别审查。

## explore

1. 锁定业务、必要状态与事实。
2. 盘点适用 Profile 与架构，制定整个批次方向。
3. 针对缺口学习参考，不要求一版对应一个网站。
4. 检查兼容和素材前提，输出独立候选配置。
5. 通过 Gate 后基于实际参数筛选；不足在预算内补方向。
6. 冻结每个方向的 visual identity locks，再编译 handoff。
7. build 后同视口首屏、代表区域、手机对照，检查是否只是图片差异。

初版可采用可解释的贪心选择：先取质量合格的基准，再选与已选集合最小距离较大的兼容候选。不是完整 MAP-Elites/DPP 实现，也不承诺数学最优。强差异候选仍须通过质量底线。

## refine

输入：base resolved hash、issue evidence、preserve 字段、editable 字段、风险和允许范围。

输出：JSON patch、每项 issue_id、before/after、理由、预期效果、回归范围。对源配置修改再编译；实际代码 bug 可局部修实现。

程序确认 base hash 未过期、patch 不修改锁定字段；渲染确认问题解决且视觉身份不变。改一个 font-family 也可能越界，不能按修改行数判断。保守修复失败返回 requires_replan，经任务允许再走 explore，而不是偷偷换风格。

## 批次终止

分别记录 config_eligible_count、asset_ready_count、built_count、quality_pass_count、perceptually_distinct_count。missing 素材不否认配置间存在差异，但不能算完整视觉交付通过。

refine 默认每个 issue 两轮后根因复盘，不反复修改已合格版本；修完复核最近候选对。N 页未齐需写缺额与原因，预算结束不是完成。query_only 可交付条件性方案但明确允许的后续操作。
