---
document_id: ADR-0002
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/adr/0002-tkinter-ui-framework.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 180
---
# ADR 0002：Tkinter UI框架

## 决策

悬浮窗/设置/右键菜单保留Tkinter，通知区域集成使用pystray。Tk在主线程拥有全部UI状态。

## 后果

Worker通过queue和 `after` callback通信。纯策略保持可headless测试。替换Tk需要迁移ADR、等价多屏/托盘行为和实体回归证据。
