# Webdev 文档归档

本仓库保存 Webdev 工作区的全部 Markdown、Word 和 PDF 文档，保留原始目录结构和历史版本。

## 目录

- `outputs/`：实验方案完整版和精简版 Word 文档、Query QA 设计文档，以及对话资料包中的 Markdown 文档和技能快照。
- `work/`：方案 PDF、产品设计工作规范和技能文档副本。
- `SHA256SUMS`：文档及归档说明的 SHA-256 校验清单；不包含该清单自身。

## 归档范围

归档日期：2026-09-14。

Git 上传范围为当前 Webdev 目录中的全部 `.md`、`.docx` 和 `.pdf` 文件，以及本说明、`.gitignore` 和校验清单。Word 文档中的嵌入图片完整保留。独立素材、制作脚本、二进制依赖及已有 ZIP 保留在本地完整目录备份中。

本地归档：

- `archives/webdev-documents-2026-09-14.zip`：与本次 Git 提交内容一致的文档包。
- `archives/webdev-workspace-2026-09-14.zip`：完整目录备份，包含文档、素材、制作脚本、依赖及已有 ZIP，并附独立的完整校验清单。

两个压缩包解压后根目录均为 `Webdev/`；压缩包本身不重复提交到 Git。排除 Git 内部数据、macOS `.DS_Store` 文件及 `archives/` 输出目录。工作区之外的账户配置、聊天数据库和已安装技能不在本次范围内。

解压后可在 `Webdev/` 目录验证文件完整性：

```sh
shasum -a 256 -c SHA256SUMS
```

原始工作文件保留其原有环境路径和依赖配置；本次归档未改写内容。
