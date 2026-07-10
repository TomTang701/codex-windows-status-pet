---
document_id: ADR-0001
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/adr/0001-local-app-server-provider.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 180
---
# ADR 0001：本地app-server额度provider

## 决策

使用 `codex app-server --stdio` 作为唯一额度transport。批准字段由 QuotaProviderAPI 规范化；UI代码不管理transport。

## 后果

应用复用官方本地Codex边界，不需要token reader或backend。Provider结构变化需要脱敏fixture和parser更新。第三方endpoint需要新ADR和安全审查。
