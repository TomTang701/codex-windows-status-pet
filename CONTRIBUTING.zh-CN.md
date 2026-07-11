# 贡献

重大工作使用短期分支，并保持 `main` 可发布。变更应有需求、API/文件归属、测试、兼容性影响、安全影响、回滚计划；适用时同步更新中英文文档。

提交前运行相关测试、`scripts/check_doc_parity.py`、`scripts/run_quality_checks.py` 和 `git diff --check`。只有正式候选版本才运行 `scripts/run_release_candidate_checks.py`。每个提交只包含一个连贯变化并使用祈使语气，同时核验远程所有者和作者身份。不得混入无关用户改动。
