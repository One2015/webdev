# 稳定性技术依据与边界

2026-09-14查阅，以下为技术机制参考；本包的测试矩阵与任务数量是工程建议。

- [MDN Document.fonts](https://developer.mozilla.org/en-US/docs/Web/API/Document/fonts)：返回FontFaceSet；fonts.ready可用于等待已用字体的加载与布局操作完成。它不独立证明设计指定字体已实际覆盖所有字符。
- [MDN font-synthesis](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-synthesis)：控制缺少字形变体时的字体合成行为。是否禁用须结合实际字体资源决定。
- [web.dev Optimize CLS](https://web.dev/articles/optimize-cls)：无尺寸媒体、字体等可造成布局位移；预留空间与资源加载策略有助于改善。单次本地测量不等于真实用户现场指标。

字体真实呈现需要综合资源与渲染证据。无法测量时报告限制，不用一个布尔API替代全部检查。浏览器支持、执行工具能力和跨平台渲染可能不同，按任务环境实测。
