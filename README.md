# WebDev 2.0 — 网站配方、生成稳定性与多样性

当前版本：**v1.1**（2026-09-14）。

先固定业务，再规划不同的网站配方；先确认做得好，再判断是否明显不同。

## 最新资料

- [v1.1 完整项目与目录](projects/design-diversity-pipeline-v1.1/README.md)
- [完整 System Prompt](projects/design-diversity-pipeline-v1.1/prompts/system-prompt.md)
- [操作方式](projects/design-diversity-pipeline-v1.1/docs/usage.md)
- [Layout / Font 等生成稳定性](projects/design-diversity-pipeline-v1.1/docs/generation-stability.md)
- [多样性评估](projects/design-diversity-pipeline-v1.1/docs/diversity-evaluation.md)
- [Rubric](projects/design-diversity-pipeline-v1.1/rubrics/README.md)
- [完整 ZIP 下载](downloads/webdev2-system-prompt-stability-diversity-v1.1-2026-09-14.zip)

包括系统指令、使用模板、25条规则、评估示例、论文索引与本Chat决策摘要。资料包包含30个文件；是方案与执行契约，不是已实现的完整网页生成引擎。

## 校验

```sh
python3 projects/design-diversity-pipeline-v1.1/scripts/validate.py
shasum -a 256 -c SHA256SUMS
```

前者只读校验资料完整性；后者校验仓库跟踪文件（不包含根校验清单自身）。ZIP有同目录独立.sha256。页面测试需要另按任务实际执行。

## 历史内容

- [v1.0](projects/design-diversity-pipeline-v1/README.md)
- `outputs/`、`work/`：原有文档和研究归档。
- `archives/`：本地历史备份，不提交Git；最新可下载包单独放在`downloads/`。

本次main通过正常提交更新到v1.1，保留历史文档和提交记录。未将工作区外的源码、素材、账户或聊天数据库加入发布。
