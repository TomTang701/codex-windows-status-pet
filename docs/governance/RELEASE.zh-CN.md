# 发布

English: [English version](RELEASE.md)

## 门禁

日常 `run_quality_checks.py` 只提供快速自动化代码质量反馈，绝不批准发布。`run_release_candidate_checks.py` 是唯一正式自动化发布命令；它只执行一次 Quality、打包 smoke、严格兼容性就绪和空白检查，并分别报告通过项、阻塞项和限制。规范事实分类与权威检查记录在 `docs/quality/verification-inventory.json`。

运行时依赖策略在 `requirements.txt` 中使用最低兼容版本。Quality 会检查每项声明已安装、满足最低版本并且可以导入；当前已验证环境为 Pillow 12.2.0 和 pystray 0.19.5。

## 支持的运行时声明

- 支持系统：Windows 11 x64 已完成实体测试并声明支持；Windows 10 为延后、不声明支持、非阻塞。
- Python/运行时：CI基线为Python 3.11；本地已验证Python 3.12.13。回退运行时必须提供 `pythonw.exe` 并安装 `requirements.txt`。
- 架构：已测试架构为x64 Windows；不宣称支持ARM64或32位Windows。
- 未签名行为：项目不提供已签名二进制；打包发布时可能出现Windows SmartScreen或策略警告，必须记录。

## 版本和回滚

采用Semantic Versioning。应用、manifest、更新日志、包、制品和诊断中的版本必须一致。记录上一个稳定版本、配置兼容性、重装路径、降级限制和备份/恢复路径。

重大变更使用聚焦提交，且只有在 `scripts/run_quality_checks.py` 和 `git diff --check` 通过后推送。远程所有者必须保持为 `TomTang701`。绿色 Quality 结果不得描述为正式发布批准。
