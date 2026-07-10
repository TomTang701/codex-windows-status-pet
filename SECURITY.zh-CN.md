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

## 威胁模型和敏感数据

威胁包括恶意或损坏的设置/JSONL/provider数据、命令或参数注入、可执行路径替换、日志/诊断泄漏凭据、不安全第三方endpoint和被篡改发布制品。敏感数据包括token、账户标识、提示词、回答、项目/会话内容、原始额度payload、私有文件内容，以及包含这些信息的截图或日志。

所有parser使用字段allowlist、限定遍历，并在适用处限制大小/时间且安全回退。子进程使用参数array和批准的可执行发现；不得将不可信值插入shell命令。可执行路径变化和新provider需要独立安全审查、contract fixture和维护者批准。

## 日志、报告和制品

运行日志只包含脱敏状态、错误类型和安全路径。诊断不得包含原始payload或正文。漏洞通过仓库owner私密联系方式或GitHub private security advisory报告；公开Issue不得包含利用secret或个人数据。

发布候选通过敏感文件/依赖检查、严格证据门禁、package检查和checksum生成。未签名制品必须明确说明；checksum证明发布字节完整性，但不是代码签名。
