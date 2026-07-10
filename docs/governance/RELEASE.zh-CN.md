# 发布

## 门禁

发布前必须完成自动检查、必需实体矩阵、版本来源一致性、双语一致性、敏感文件扫描、干净环境启动、更新日志、已知问题和回滚说明。当前实体阻塞项由 `scripts/check_release_readiness.py` 报告。

运行时依赖策略在 `requirements.txt` 中使用最低兼容版本。发布门禁会检查每项声明已安装、满足最低版本并且可以导入；当前已验证环境为 Pillow 12.2.0 和 pystray 0.19.5。

## 版本和回滚

采用Semantic Versioning。应用、manifest、更新日志、包、制品和诊断中的版本必须一致。记录上一个稳定版本、配置兼容性、重装路径、降级限制和备份/恢复路径。

重大变更使用聚焦提交，且只有在 `scripts/run_release_checks.py` 和 `git diff --check` 通过后推送。远程所有者必须保持为 `TomTang701`。
