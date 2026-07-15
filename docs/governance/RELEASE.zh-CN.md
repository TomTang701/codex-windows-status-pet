# 发布

English: [English version](RELEASE.md)

## 门禁

日常 `run_quality_checks.py` 只提供快速自动化代码质量反馈，绝不批准发布。
`run_release_candidate_checks.py` 是唯一正式自动化发布命令。它会各执行一次
Quality、固定版本 onedir 构建、静态 ZIP/SHA 校验、打包 EXE 生命周期 smoke、README 截图校验、
严格兼容性就绪和空白检查，并分别报告通过项、阻塞项和限制。规范事实分类与权威检查记录在
`docs/quality/verification-inventory.json`。

运行时依赖策略在 `requirements.txt` 中使用最低兼容版本。Quality 会检查每项声明已安装、满足
最低版本并且可以导入；当前已验证环境为 Pillow 12.2.0 和 pystray 0.19.5。

## 支持的运行时声明

- 支持系统：Windows 11 x64 已完成实体测试并声明支持；Windows 10 为延后、不声明支持、非阻塞。
- 已安装运行时：受支持的已安装产品是 PyInstaller onedir EXE，目标机器不需要 Python、pip、Git
  或仓库检出。Python 3.11 仍是 CI 基线，Python 3.12.13 仅作为源码开发的本地验证环境。
- 架构：已测试架构为 x64 Windows；不声明支持 ARM64 或 32 位 Windows。
- 未签名行为：项目不提供已签名二进制；打包发布时可能出现 Windows SmartScreen 或策略警告，
  必须记录。

## 版本和回滚

采用 Semantic Versioning。应用、manifest、更新日志、包、制品和诊断中的版本必须一致。
记录上一个稳定版本、配置兼容性、重装路径、降级限制和备份/恢复路径。

重大变更使用聚焦提交，且只有在 `scripts/run_quality_checks.py` 和 `git diff --check` 通过后才推送。
远程所有者必须保持为 `TomTang701`。绿色 Quality 结果不得描述为正式发布批准。

当前候选工作流上传 `CodexStatusPet-v…-win11-x64.zip` 及其 `.sha256` 校验文件，
而不是源码 ZIP。发布说明必须披露未签名二进制、按用户安装路径、设置保留行为、Codex CLI
依赖和任何干净环境证据的分类。
