# 相关论文与阅读路线

这是一份有针对性的阅读索引，不是全面系统综述。附原文链接与原创短摘要，不捆绑第三方全文；离线包可完整阅读本方法和摘要，论文原文需联网。迁移建议不等于论文已经验证本系统。

## 优先阅读

| 论文 | 读什么 | 对应节点 |
|---|---|---|
| [DesignScape (CHI 2015)](https://www.dgp.toronto.edu/~donovan/design/designscape.pdf) | Refinement / Brainstorming / Style Sampling | explore/refine |
| [Scout (CHI 2020)](https://arxiv.org/abs/2001.05424) | 高层约束与布局替代 | PA候选与兼容Gate |
| [MAP-Elites (2015)](https://arxiv.org/abs/1504.04909) | 特征区域内保留高质量解 | 候选档案与覆盖 |
| [DPP (2012)](https://arxiv.org/abs/1207.6083) | Quality versus Diversity | 从候选池选择集合 |
| [Webzeitgeist (CHI 2013)](https://hci.stanford.edu/publications/2013/Webzeitgeist/webzeitgeist.pdf) | 设计数据挖掘 | 参考学习与知识库 |
| [Parallel Prototyping (TOCHI 2010)](https://hci.stanford.edu/publications/2010/parallel-prototyping/ParallelPrototyping2010-final.pdf) | 平行与串行设计比较 | 批次探索流程 |
| [Design2Code (NAACL 2025)](https://aclanthology.org/2025.naacl-long.199/) | 截图还原评估 | 实现视觉验证 |

## 原方法与本项目迁移的区别

DesignScape 使用对齐、对称、重叠等布局目标；Refinement 接近当前布局并支持元素锁定，Brainstorming 从示例学习的低维参数空间采样。本包将其迁移为受限配置补丁与独立候选，不复现其GPU优化器，也不宣称其风格空间覆盖完整网页视觉语言。

Scout 将分组、顺序和强调等约束转换成布局选择。本包保留业务语义、开放空间组织；需要另补状态、素材和响应式验证。

MAP-Elites 返回不同特征区域的优秀解。本包初版用可解释候选档案借鉴其质量与差异兼顾的思想，未运行原算法。DPP 可在候选池较大时帮助选择低重复集合；如果特征只编码照片，选择结果仍可能只体现图片变化。

Webzeitgeist 说明保存渲染与结构特征能支持设计挖掘。Parallel Prototyping 的广告研究支持探索多个方向，但不能推出每品类十种的标准。Design2Code 检查参考到代码的相似性，应与候选间差异指标分开。

## 设计分类与规范

- [DTCG Format 2025.10](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/)：Token交换社区规范，不是网页风格分类，也非W3C正式标准。
- [USWDS Tokens](https://designsystem.digital.gov/design-tokens/)：颜色、字体、间距等离散参数组织。
- [NN/g 极简特征](https://www.nngroup.com/articles/characteristics-minimalism/)：极简可拆成多个特征，名称不是单一数值。
- [NN/g Mood Boards](https://www.nngroup.com/articles/mood-boards/)：建立整体视觉方向，再解析为具体参数。

本次未发现全球统一的网页风格数目标准。6–8家族、每品类4–6家族、十套Profile等均为当前项目规划建议，需按品类和输出评审调整。

## 查阅范围

2026-09-14 重新访问 DesignScape 全文及 Scout/MAP-Elites/DPP 原始摘要页；其他条目依据本对话此前检索与原文链接整理。未把页面抓取日期当论文出版年份。没有复制论文全文或长段原文。
