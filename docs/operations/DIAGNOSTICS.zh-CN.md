# 诊断

诊断日志写入 `%USERPROFILE%\.codex\codex-windows-status-pet.log`。日志不得包含auth token、项目文件、完整会话正文或原始provider响应。

诊断边界应覆盖启动、Codex查找、app-server生命周期、刷新失败、解析失败、托盘失败、窗口恢复、设置迁移和shutdown。面向用户的摘要应提供应用版本、Windows/显示器信息、经过脱敏的配置路径、数据源状态、最近一次成功刷新时间、当前状态和日志位置。

在总规范迁移到 `docs/governance/` 前，诊断和日志策略由 `Goal/ENGINEERING_STANDARD.zh-CN.md` 约束。
