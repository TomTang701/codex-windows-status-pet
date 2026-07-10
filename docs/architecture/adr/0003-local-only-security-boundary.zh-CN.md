---
document_id: ADR-0003
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/adr/0003-local-only-security-boundary.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 180
---
# ADR 0003：仅本地安全边界

## 决策

不读取 `auth.json`、token、账户ID、提示词/回答/项目/会话正文，也不发送遥测。日志和诊断只包含脱敏派生状态。

## 后果

批准本地接口未提供的数据保持不可用，不进行推断。任何边界扩展都需要明确用户范围、威胁审查、负向测试、文档和新ADR。
