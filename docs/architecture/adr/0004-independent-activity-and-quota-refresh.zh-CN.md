---
document_id: ADR-0004
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/adr/0004-independent-activity-and-quota-refresh.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 180
---
# ADR 0004：独立Activity和Quota刷新

## 决策

Activity和Quota使用独立single-flight channel、generation、clock、worker和失败状态。两者不互相等待或取消。

## 后果

缓慢app-server I/O不能冻结Activity或Tk。过期callback被丢弃，shutdown取消两个channel。跨channel耦合需要明确架构review和race测试。
