# 对话脉络与当前结论

## 最初目标与演变

1. 从 Query Diversity 出发，升级为 Design Evidence Coverage：Query 数量和换词不代表覆盖充分。
2. 加入 Mobbin、公开网页、产品视频、Design System，建立参考学习与知识沉淀。
3. 受 Blender 建模加贴图启发，网页也应先建立骨架、视觉 Foundation、组件接口与素材，再实现。
4. 从单一主参考扩展到按品类建设 Category Knowledge Pack；用户要求沉淀 Goal、Journey、模块、状态、Style、Palette、Motion、Anti-slop 和映射。
5. 用户明确：目标不是围绕 A/B 实验建系统，而是快速拆解、重组多样网页。
6. 多轮 review 暴露：引用正确不等于证据支持；JSON 能解析不等于契约可执行；参数不同不等于页面感知差异。
7. 增加素材主动搜索与独立交付：短 Query、完整实现 Prompt、resolved、素材包。
8. 新增批次规划与 explore/refine，避免十次独立生成得到十个近似页面。
9. 最新结论：product-intent.md、design.md、component.md 需要单文件与跨文件 Spec Gate；页面还需独立运行与视觉验收。

## 已确认方向

- 保留业务前提、核心任务和必要状态，在允许范围内探索 PA 与风格。
- 当前 skill 中 SD 指视觉语言来源，PA 指产品模式来源。前期讨论曾暂用 PA 表示页面结构；实施时显式分开 product_patterns 和 page_architecture，不依赖缩写猜测。
- library/demand 是编译范围；query_only/build 是执行终点，不混成一个模式。
- 采用真实参考作为依据，但新组合及跨端推导可以是明确的项目假设。
- 不以文件数、ID 数、检查数或模型主观总分证明完成。
- 缺素材允许某些方案做结构行为验证；不能据此宣称完整视觉通过。
- 只对关键业务缺失请求澄清，可逆技术选择可记录默认值。

## 两组历史项目必须区分

### 时尚电商 PDP pack

路径：`/Users/apple/Documents/ChatGPT/copula官网/forge-review-handoff/forge/v2/category-knowledge-pack/`。

历史发现包括 Everlane 抽屉可见性误判、EvidenceSupport 错位、通配引用、状态语义混用、候选参数未解析、把共存写成已验证组合。后来拆分 claim、修正引用和适用性。此路径不在本包内。

### 住宿详情页 design-kb

路径：`/Users/apple/webdev2/design-kb/`；实现路径：`/Users/apple/webdev2/impl-cmb-01/`。

- CMB-01：单一可预订单元，图库与粘性预订卡。
- CMB-02：编辑型混合变体，依赖高质量素材，不能标成纯视觉变体。
- CMB-03：多房型业务分支，不能作为单一房源需求的自由替代。
- 修复涉及自包含 Query、布局加总、遮罩文字保护范围、Style 兼容、素材核验、需求分支、旧产物失效及临时目录测试。
- 用户最后报告：素材记录核验及失效路径已修复；CMB-01 已实现，占位素材下 15 项通过、1 项部分通过，完整视觉与部分真实设备/辅助技术验证仍未覆盖。这些是历史报告，不是本次打包重新验收结果。

## GitHub 备份历史

仓库：https://github.com/One2015/000

- `webdev/`：Webdev 工作目录备份，提交 c36470c646ac93a570093a4d57b3f4da2ae17f0d。
- `skills/`：两个当前个人 skill 独立备份，提交 e68f4e0fff896baa622eda6dc6902707c67692e3。
- 当时推送均已核对远端提交。当前仓库可能有后续变化，本次未联网检查。
- 上述备份不含 webdev2 项目，也不是多个 chat 的完整会话导出。
