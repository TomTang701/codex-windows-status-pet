---
document_id: DEVELOPMENT-PLAN
status: active
document_version: 1.2.0
canonical_language: en
translation_pair: docs/product/ROADMAP.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 30
---
# Codex Windows 状态宠物路线图

已完成功能写入 `CHANGELOG.zh-CN.md`；证据写入兼容矩阵。自动测试数量不在这里手工维护。

## 当前基线

Windows 11 x64、Python 3.11 CI/Python 3.12.x本地、根CMD启动器、Tkinter悬浮窗、通知区域图标和正常底部任务栏构成v0.3.0支持基线。退出条件：每项支持声明都有结构化兼容行。

## 当前

- 完成Reset Credit可见记录。退出条件：Windows 11带日期证据显示 `HH:MM M/D`。
- 减少Tk窗口协调职责并拆分稳定额度行。退出条件：controller和行契约测试通过。
- 保持Quality全绿及严格阻塞确定。退出条件：脚本输出匹配矩阵明确列。

## 下一步

- 完成单显示器和实际可行的显示器重连记录。退出条件：存在Windows 11带日期证据。
- 验证空闲收缩和悬停展开。退出条件：带日期记录显示两种转换。
- 完成设置事务、backup/restore和重复shutdown证据。退出条件：声明范围内行通过。

## 后续

- 在可复现制品和回滚稳定后评估签名打包。
- 只在经过测试的API边界后考虑其他本地展示模式。
- 审查无障碍和可选8小时soak证据。

## 阻塞

- v0.3.0只被明确标记 `Blocking: Yes` 的未完成Windows 11行阻塞；每行都说明下一步。

## 延期

- Windows 10兼容调查；不宣称支持，也不阻塞v0.3.0。
- ARM64、32位Windows、混合DPI认证、其他任务栏边缘实体测试和8小时soak。

## 不在范围

- 读取 `auth.json`、token、账户ID、提示词/回答/项目/会话正文或原始额度响应。
- 第三方额度provider、遥测、托管后端，或修改Codex核心/内置宠物。
- 从模拟或推断证据宣称实体兼容。
