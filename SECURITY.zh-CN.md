---
document_id: SECURITY
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: SECURITY.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# 安全

默认产品仅限本地：使用本机Codex app-server边界，不读取 `auth.json`，不保存access token/account ID，不向第三方发送提示词、回答或项目文件，不记录原始额度响应，也不会在未经选择加入和评审的情况下增加遥测。

发现疑似漏洞时，应在公开披露前私下联系维护者。不得提交凭据、会话正文、日志、含敏感信息的截图或未经评审的数据源地址。
