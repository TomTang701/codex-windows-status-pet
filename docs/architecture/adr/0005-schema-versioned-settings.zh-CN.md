---
document_id: ADR-0005
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/adr/0005-schema-versioned-settings.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 180
---
# ADR 0005：带schema版本的设置

## 决策

持久化 `schema_version`，加载分类为current、legacy、missing、malformed或unsupported future。损坏和未来文件保持只读，直到明确重置。

## 后果

旧设置安全迁移，旧应用不能静默降级新数据。所有自动保存使用统一writable guard；schema变化需要migration、fallback和覆盖回归测试。
