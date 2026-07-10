# Codex Goal：修复 Reset Credit 日期显示并完成仓库长期治理加固

> **Repository:** `TomTang701/codex-windows-status-pet`  
> **Target branch:** 从最新 `main` 创建短期工作分支  
> **Goal type:** Bug fix + reliability hardening + governance follow-up  
> **Priority:** P0 → P1 → P2  
> **Execution rule:** 必须按阶段提交；不得把所有修改压进一个超大提交  
> **Primary language:** 代码和英文规范为原版；中文文档在同一提交中同步  
> **Current known baseline:** 应用版本仍为 `0.2.0`，仓库已具备分层文档、manifest、Windows CI、约88项自动测试、配置schema v1、设置备份、模块化UI和实体兼容矩阵

---

# 1. 总目标

完成以下工作：

1. **首先修复主界面最下面的 Reset Credit 行。**
   - `5h` 行只显示时间；
   - `周` 行维持当前契约；
   - `重置 N 次` 行在存在有效到期时间时，必须同时显示本地时间和日期；
   - 示例：`重置 2 次 / 18:40 7/12`。

2. 修复后增加解析、格式化和主显示快照回归测试，防止日期再次消失。

3. 按仓库最新审计结果继续处理：
   - 未知未来配置schema被旧程序覆盖的风险；
   - 日常质量门禁与正式Release门禁混淆；
   - 兼容矩阵状态不规范；
   - 编译门禁没有覆盖全部Python文件；
   - 工程总规范尚未正式生效；
   - manifest字段尚未真正执行；
   - 双语检查过于浅层；
   - Roadmap仍混入大量已完成工作；
   - 专项规范仍过于简略；
   - 剩余Windows实体测试未完成。

4. 所有修改必须保持：
   - 不读取 `auth.json`；
   - 不读取、保存或记录access token；
   - 不发送prompt、response、project或session正文到第三方；
   - 不修改Codex核心或内置宠物；
   - Tk主线程不执行阻塞I/O；
   - Activity和Quota刷新继续独立；
   - 单实例、托盘和shutdown继续可恢复且幂等。

---

# 2. 强制执行顺序

必须按以下顺序推进：

```text
Phase 0  重现和锁定Reset Credit日期问题
Phase 1  修复Reset Credit解析和显示契约
Phase 2  增加回归测试和文档同步
Phase 3  修复未来schema覆盖风险
Phase 4  拆分质量门禁和正式Release门禁
Phase 5  完善文档治理和manifest强制规则
Phase 6  精简Roadmap并补强专项规范
Phase 7  完成实体兼容测试和v0.3.0候选评估
```

在Phase 0–2完成、测试通过并提交之前，不要开始后续大规模治理重构。

---

# 3. Phase 0：重现并锁定“重置 N 次”日期问题

## 3.1 预期显示契约

主界面额度区域应满足：

```text
5h 80% / 18:30
周 65% / 09:00 7/15
重置 2 次 / 18:40 7/12
```

要求：

- `5h`：只显示 `HH:MM`，不显示日期；
- `周`：保持当前产品契约，不因本修复发生无关变化；
- `重置 N 次`：存在有效到期时间时，必须显示 `HH:MM M/D`；
- 月和日不得补前导零；
- 使用本地时区；
- 不存在有效到期时间时，只显示 `重置 N 次`；
- 不得伪造日期；
- 不得因为窗口宽度、解析别名或provider结构改变而静默只剩时间。

## 3.2 先检查以下文件

```text
scripts/api/quota_format_api.py
scripts/api/quota_parse_api.py
scripts/api/quota_provider_api.py
scripts/api/status_snapshot_api.py
scripts/ui/main_window.py
tests/test_quota_format_api.py
tests/test_quota_parse_api.py
tests/test_status_snapshot.py
```

## 3.3 必须确认的事实

执行前确认：

1. 当前 `reset_credit_line()` 是否调用完整的日期时间格式化函数；
2. 当前 `local_time_date()` 是否在Windows上正确回退到 `HH:MM M/D`；
3. `status_snapshot_api.py` 是否把完整到期值传给 `reset_credit_line()`；
4. 严格parser是否丢弃了嵌套的 `expiresAt`、`resetsAt` 或 `resetAt`；
5. app-server真实payload中Reset Credit到期时间的结构；
6. 主界面是否因固定 `wraplength` 或过窄窗口裁掉行尾日期；
7. 正在运行的是否为最新仓库进程，而不是旧副本或旧 `pythonw.exe` 进程。

## 3.4 调试纪律

- 不要直接打印原始quota payload到普通日志；
- 如需检查结构，只记录字段名、类型和脱敏结构；
- 不记录token、account ID、prompt、response或session正文；
- 不因无法访问真实账号而硬编码假数据；
- 对真实payload不确定时，使用最小脱敏fixture补充测试。

---

# 4. Phase 1：修复Reset Credit时间和日期

## 4.1 格式化层

`quota_format_api.py`必须提供清晰、单一职责的格式化行为。

推荐契约：

```python
def local_time_only(value) -> str:
    """Return local HH:MM or --."""

def local_time_date(value) -> str:
    """Return local HH:MM M/D or --."""

def reset_credit_line(count, expiration) -> str:
    """Return Reset Credit count and, when valid, local time plus date."""
```

要求：

- `5h`调用 `local_time_only()`；
- `重置 N 次`调用 `local_time_date()`；
- 不允许通过字符串切片从完整日期中截取时间；
- Windows不得依赖 `%-m` / `%-d`；
- Unix和Windows输出必须一致；
- 无效epoch、溢出和损坏ISO字符串必须返回安全fallback。

推荐实现方式：

```python
current = datetime.fromtimestamp(timestamp).astimezone()
return f"{current.hour:02d}:{current.minute:02d} {current.month}/{current.day}"
```

避免仅依赖平台相关的：

```python
strftime("%H:%M %-m/%-d")
```

## 4.2 Reset Credit解析层

当前严格parser必须保留经过批准的Reset Credit字段，但需要支持实际provider形状。

必须支持的候选名称：

```text
availableCount
available_count

expiresAt
expires_at
resetsAt
resets_at
resetAt
reset_at
expirations
```

必须支持的合理形状：

```json
{
  "rateLimitResetCredits": {
    "availableCount": 2,
    "resetsAt": [1893456000]
  }
}
```

```json
{
  "rateLimitResetCredits": {
    "availableCount": 2,
    "expirations": [
      {"expiresAt": 1893456000}
    ]
  }
}
```

```json
{
  "rateLimitResetCredits": {
    "available_count": 2,
    "credits": [
      {"expires_at": "2030-01-01T00:00:00Z"}
    ]
  }
}
```

不要无边界递归接受所有字段。应当：

- 明确允许的字段名；
- 只遍历Reset Credit容器；
- 限制嵌套深度；
- 忽略未知字段；
- 不复制原始provider对象到UI；
- 输出稳定、最小的规范化结构。

推荐规范化结果：

```python
{
    "availableCount": 2,
    "expirations": [
        1893456000,
        "2030-01-01T00:00:00Z",
    ],
}
```

或使用现有约定：

```python
{
    "availableCount": 2,
    "resetsAt": [...],
}
```

但整个仓库只能选择一种正式字段名。

## 4.3 最早未来到期时间

`earliest_future_expiry()`必须：

- 忽略过去时间；
- 忽略损坏时间；
- 接受epoch和ISO 8601；
- 使用可注入 `now`；
- 返回最早的未来到期时间；
- 不返回当前时间或过去时间；
- 不读取provider之外的数据。

## 4.4 主显示快照

`status_snapshot_api.py`必须保证：

```text
5h ... / HH:MM
周 ... / HH:MM M/D
重置 N 次 / HH:MM M/D
```

`Reset Credit`日期不得在presentation层被再次缩短。

建议移除含义模糊的 `_short_time()`，改名为明确的：

```python
format_primary_reset_time()
```

或直接调用公共格式化API。

## 4.5 UI布局保护

如果问题来源包括UI裁切，则同时处理：

- 展开模式最小宽度不得低到无法显示正式状态契约；
- Reset Credit行不得被静默裁掉日期；
- 可以将状态行拆成独立Label；
- 若暂不拆分，至少动态设置 `wraplength`；
- 不要通过增大整个窗口掩盖解析问题；
- Compact模式可以隐藏文本，但Expanded模式必须显示完整正式字段。

推荐最低展开宽度：

```text
280–300 px
```

具体数值必须通过字体8、10、12、16、20的布局测试或人工检查决定。

---

# 5. Phase 2：回归测试与文档同步

## 5.1 必须新增的格式化测试

在 `tests/test_quota_format_api.py` 增加：

```python
def test_reset_credit_line_includes_local_time_and_date():
    ...

def test_reset_credit_line_without_expiry_omits_separator():
    ...

def test_local_time_date_has_no_leading_zero():
    ...

def test_local_time_date_accepts_iso_timestamp():
    ...

def test_earliest_future_expiry_ignores_past_and_invalid_values():
    ...
```

不要断言当前机器的固定时区结果，除非注入时区或只断言格式。

推荐正则：

```python
r"^重置 2 次 / \d{2}:\d{2} \d{1,2}/\d{1,2}$"
```

## 5.2 必须新增的解析测试

在 `tests/test_quota_parse_api.py` 增加：

```text
顶层resetsAt列表
顶层resetAt单值
嵌套expiresAt
snake_case别名
混合过去和未来时间
损坏对象
未知字段不泄漏
凭据字段被丢弃
```

## 5.3 必须新增的presentation测试

在 `tests/test_status_snapshot.py` 增加：

```python
def test_snapshot_reset_credit_line_contains_time_and_date():
    ...

def test_snapshot_primary_5h_line_contains_time_only():
    ...

def test_snapshot_does_not_expose_raw_provider_fields():
    ...
```

测试应分别提取行：

```python
lines = result["text"].splitlines()
primary_line = ...
reset_line = lines[-1]
```

不要只使用 `assertIn("重置", text)`，必须验证完整格式。

## 5.4 UI契约测试

若修改Label布局：

- 测试Expanded模式存在Reset Credit行；
- 测试Compact模式可隐藏文本；
- 测试退出Compact后恢复完整文本；
- 测试字体和窗口宽度变化不会删除字符串内容；
- 不要求headless测试精确测量像素，像素可见性进入Windows实体记录。

## 5.5 文档更新

同步更新：

```text
CHANGELOG.md
CHANGELOG.zh-CN.md
docs/architecture/API_SPEC.md
docs/architecture/API_SPEC.zh-CN.md
docs/product/ROADMAP.md
docs/product/ROADMAP.zh-CN.md
docs/quality/COMPATIBILITY_MATRIX.md
docs/quality/COMPATIBILITY_MATRIX.zh-CN.md
```

API规范必须明确：

```text
Primary 5h reset uses local HH:MM only.
Weekly and Reset Credit expiry use local HH:MM M/D without leading zeroes.
Missing provider dates are not invented.
```

中文同步表达相同契约。

## 5.6 Phase 1–2验收条件

以下全部通过后才能继续：

```text
[ ] Reset Credit存在未来到期日时显示 HH:MM M/D
[ ] 5h仍只显示HH:MM
[ ] 日期使用本地时区
[ ] 月/日无前导零
[ ] 损坏日期安全fallback
[ ] parser保留实际Reset Credit到期字段
[ ] raw provider字段不进入UI
[ ] 新增格式化、解析、snapshot回归测试
[ ] 中英文API规范和Changelog同步
[ ] 全部自动检查通过
[ ] Windows手工启动确认完整可见
```

建议独立提交：

```text
Fix reset-credit expiry date display
```

---

# 6. Phase 3：修复未知未来schema覆盖风险

## 6.1 当前风险

当前配置加载遇到未知schema时会返回默认设置和warning；应用退出时又可能无条件保存默认设置，导致旧版本覆盖较新版本配置。

这是数据兼容性P0风险。

## 6.2 新配置加载结果

不要继续只返回：

```python
(settings, warnings)
```

建议引入：

```python
@dataclass(frozen=True)
class ConfigLoadResult:
    settings: dict
    warnings: tuple[str, ...]
    schema_status: str
    writable: bool
```

`schema_status`至少包括：

```text
current
legacy
unsupported_future
malformed
missing
```

## 6.3 行为要求

### current

- 正常加载；
- 可保存；
- 可备份。

### legacy

- 内存迁移到当前schema；
- 可保存；
- 保存后写入schema v1。

### unsupported_future

- 可以使用默认值或只读兼容值启动；
- `writable=False`；
- 退出时不得覆盖原文件；
- 隐藏、拖动、恢复窗口等自动保存路径也不得覆盖；
- UI或日志给出明确提示；
- 用户只有明确选择“重置为当前版本配置”后才能写入。

### malformed

- 保留损坏文件；
- 不将损坏文件覆盖为默认值，除非明确策略允许；
- 应考虑创建 `.corrupt-<timestamp>` 备份；
- 必须记录脱敏warning。

## 6.4 所有保存入口必须检查writable

包括：

```text
正常退出
拖动结束
隐藏窗口
切换topmost
切换locked
设置Save
窗口自动恢复
恢复backup后保存
```

不得只修复 `close()`。

## 6.5 测试

必须增加：

```text
未知未来schema加载后writable=False
退出不覆盖原文件
拖动/隐藏不覆盖原文件
legacy配置可迁移并保存
current配置正常备份
用户明确重置后可写入
```

建议独立提交：

```text
Protect future configuration schemas from downgrade overwrite
```

---

# 7. Phase 4：区分日常质量门禁与正式Release门禁

## 7.1 当前问题

当前日常检查会运行发布就绪报告，但未使用strict模式，所以即使存在实体阻塞项，整体quality gate仍可通过。

这在日常CI可以接受，但命名和发布流程必须区分。

## 7.2 建议脚本

保留或创建：

```text
scripts/run_quality_checks.py
scripts/run_release_candidate_checks.py
```

### 日常Quality

执行：

```text
manifest
文档链接
版本一致
敏感文件
依赖
双语结构
compileall
unit/integration tests
startup audit
non-strict release readiness report
package smoke
```

### Release Candidate

在Quality基础上增加：

```text
check_release_readiness.py --strict
版本tag一致
Changelog正式版本存在
不存在Unreleased阻塞项
完整package artifact
checksum
clean-machine evidence
rollback说明
```

## 7.3 GitHub Actions

建议：

```text
.github/workflows/quality.yml
.github/workflows/release-candidate.yml
```

### quality.yml

触发：

```text
push main
pull_request main
```

### release-candidate.yml

触发：

```text
workflow_dispatch
tag v*
```

正式Release workflow必须使用strict门禁。

## 7.4 编译门禁

把显式枚举少数文件改为：

```powershell
python -m compileall -q scripts
```

确保覆盖：

```text
scripts/api/**/*.py
scripts/ui/**/*.py
scripts/*.py
```

## 7.5 提交

建议独立提交：

```text
Separate quality and release-candidate gates
```

---

# 8. Phase 5：完善兼容矩阵和文档治理

## 8.1 兼容矩阵状态enum

停止使用自由状态文本。

正式允许值：

```text
Pending
Automated pass
Physical pass
Partial
Not applicable
Approved limitation
Blocked
```

每一行必须包含稳定ID：

```text
WIN-10
WIN-11
DISPLAY-1
DISPLAY-2
DPI-MIXED
TASKBAR-TOP
TASKBAR-LEFT
TASKBAR-RIGHT
COMPACT-HOVER
CLEAN-MACHINE
```

建议矩阵：

| ID | Area | Coverage | Status | Evidence | Blocking |
|---|---|---|---|---|---|

`check_release_readiness.py`不得通过模糊字符串查找 `partial` 或 `pending`，应解析正式列。

## 8.2 Engineering Standard正式生效

完成review后：

```json
{
  "status": "active",
  "required_for_release": true
}
```

同时在以下文件声明它是最高层规范：

```text
README
CONTRIBUTING
RELEASE
docs/README
```

## 8.3 Manifest执行能力

增加文档front matter：

```yaml
---
document_id: API-SPEC
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: API_SPEC.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
```

新增检查：

```text
scripts/check_doc_metadata.py
scripts/check_doc_review_age.py
scripts/check_orphan_documents.py
```

检查：

- manifest和front matter ID一致；
- 中英文document version一致；
- Active规范必须登记；
- required_for_release文档必须存在；
- last_reviewed超过周期时warning或阻止Release；
- Archived文件不参与Active门禁；
- 不允许孤立的Active规范文件。

## 8.4 双语语义检查加强

在现有标题、代码块、表格行数基础上，增加：

```text
API名称集合
版本号集合
Test ID集合
表格第一列key
front matter document_version
代码块语言标签
配置schema版本
兼容矩阵ID集合
```

不要试图要求中英文逐行完全一致。

## 8.5 提交

建议拆成：

```text
Normalize compatibility evidence states
Activate engineering governance standard
Enforce document metadata and review policy
Strengthen bilingual semantic checks
```

---

# 9. Phase 6：精简Roadmap并补强专项规范

## 9.1 Roadmap改造

将当前大量已完成P0/P1移入Changelog或Release Notes。

Roadmap只保留：

```text
Now
Next
Later
Blocked
Out of scope
```

不要持续手工维护：

```text
88 automated tests
89 automated tests
90 automated tests
```

测试数量应由脚本输出或自动生成，不作为多个文档中的手工事实。

## 9.2 专项规范补强

扩充但不要重复Engineering Standard。

### ARCHITECTURE.md

补充：

- 组件图；
- 依赖方向；
- 启动顺序；
- shutdown顺序；
- queue payload；
- Activity/Quota刷新通道；
- Tk/pystray线程边界；
- settings生命周期；
- app-server生命周期；
- 失败恢复路径。

### TESTING.md

补充：

- Unit/Contract/Integration/UI/Platform/Physical/Packaging/Soak；
- fixture注入；
- 真实账号禁用原则；
- Windows实体记录模板；
- 最低测试要求矩阵；
- race和shutdown测试；
- soak test标准。

### SECURITY.md

补充：

- 威胁模型；
- 敏感数据定义；
- 日志脱敏；
- 恶意配置；
- 恶意JSONL；
- 命令注入；
- 可执行路径替换；
- provider审批；
- 漏洞私密报告流程；
- release artifact安全。

### CONTRIBUTING.md

补充：

- 分支和PR规则；
- 提交粒度；
- 必需检查；
- API/文档/测试同步；
- 变更分类；
- rollback；
- 不允许直接把重大变更堆入main。

### RELEASE.md

补充：

- quality与release-candidate区别；
- tag流程；
- artifact；
- checksum；
- signed/unsigned说明；
- clean-machine；
- rollback；
- known issues；
- 版本来源。

## 9.3 ADR

至少为以下当前决策补写ADR：

```text
0001-local-app-server-provider.md
0002-tkinter-ui-framework.md
0003-local-only-security-boundary.md
0004-independent-activity-and-quota-refresh.md
0005-schema-versioned-settings.md
```

ADR不得用来记录普通bug修复。

---

# 10. Phase 7：完成剩余Windows实体测试

根据当前兼容矩阵，至少完成：

```text
Windows 10启动和完整UI smoke
单显示器完整实体记录
混合DPI
顶部任务栏
左侧任务栏
右侧任务栏
compact空闲收缩
compact hover展开
独立干净Windows环境安装和启动
非法粘贴输入
显示器断开/重连
任务栏工作区运行时变化
8小时soak test
```

每次测试新建日期记录，不覆盖旧证据：

```text
docs/quality/test-records/YYYY-MM-DD-<scenario>.md
```

记录：

```text
Date
Commit
App version
Windows version/build
Monitor topology
DPI
Taskbar
Steps
Expected
Actual
Result
Limitations
Safe evidence
```

模拟测试不得标记为Physical pass。

---

# 11. 代码质量要求

所有新代码必须：

- 公共API使用类型标注；
- 领域模型优先使用dataclass/enum；
- 不引入UI层原始dict解析；
- 不在Tk主线程执行文件、子进程或通信阻塞；
- 不添加宽泛 `except Exception`，除非是明确安全边界；
- 安全边界catch必须记录脱敏信息；
- 不增加重复版本常量；
- 不增加第二套日期格式逻辑；
- 不通过复制粘贴实现中英文两套行为；
- 删除死代码和过期兼容路径；
- 不降低已有测试覆盖的失败路径；
- 不修改与本Goal无关的用户行为。

---

# 12. 每个提交前必须执行

```powershell
python -m compileall -q scripts
python -m unittest discover -s tests -q
python scripts/check_doc_manifest.py
python scripts/check_doc_links.py
python scripts/check_doc_parity.py
python scripts/check_version_sources.py
python scripts/check_sensitive_files.py
python scripts/check_dependencies.py
python scripts/run_release_checks.py
python scripts/package_smoke_test.py
git diff --check
```

当正式执行Release Candidate检查时：

```powershell
python scripts/check_release_readiness.py --strict
```

若已拆分脚本，则使用新的：

```powershell
python scripts/run_quality_checks.py
python scripts/run_release_candidate_checks.py
```

---

# 13. 推荐提交序列

必须保持聚焦，建议：

```text
1. Fix reset-credit expiry date display
2. Add reset-credit parser and presentation regressions
3. Protect future configuration schemas from downgrade overwrite
4. Separate quality and release-candidate gates
5. Compile all Python modules in release checks
6. Normalize compatibility evidence states
7. Activate engineering governance standard
8. Enforce document metadata and review policy
9. Strengthen bilingual semantic checks
10. Simplify roadmap to active future work
11. Expand architecture testing security and contribution standards
12. Record remaining Windows physical evidence
13. Prepare v0.3.0 release candidate
```

不得把Phase 1的显示bug与Phase 5的大规模文档治理放进同一提交。

---

# 14. Definition of Done

整个Goal完成必须满足：

## Reset Credit

```text
[ ] “重置 N 次”存在有效到期日时显示HH:MM M/D
[ ] 5h只显示HH:MM
[ ] 本地时区正确
[ ] 月/日无前导零
[ ] parser支持实际provider Reset Credit字段
[ ] 不存在日期时不伪造
[ ] Expanded模式完整显示
[ ] 自动回归测试通过
[ ] Windows实体确认通过
```

## 配置安全

```text
[ ] 未来schema不会被旧版本覆盖
[ ] 所有自动保存入口尊重writable状态
[ ] legacy迁移有测试
[ ] malformed和unsupported行为已记录
```

## Release治理

```text
[ ] 日常Quality和Release Candidate门禁已分离
[ ] 正式Release使用strict实体门禁
[ ] compile覆盖所有scripts Python文件
[ ] version、敏感文件、依赖、文档和package门禁继续通过
```

## 文档治理

```text
[ ] Engineering Standard为active
[ ] required_for_release被实际执行
[ ] manifest metadata可验证
[ ] 文档过期和孤立文件可检测
[ ] 双语检查覆盖关键语义标识
[ ] Roadmap只描述未来工作
[ ] 专项规范不再只是摘要
```

## 实体兼容

```text
[ ] 所有v0.3.0阻塞行已Physical pass或Approved limitation
[ ] 每项Physical pass都有带日期证据
[ ] clean-machine启动通过
[ ] mixed-DPI和任务栏边缘通过
[ ] compact idle/hover通过
[ ] soak test通过
```

## 最终质量

```text
[ ] 全部自动测试通过
[ ] GitHub Actions通过
[ ] 中英文文档同步
[ ] Changelog准确
[ ] 无敏感文件
[ ] 无已知P0/P1未记录风险
[ ] v0.3.0发布状态真实
```

---

# 15. 停止条件

遇到以下情况时，不得猜测或硬编码：

- app-server Reset Credit payload结构与现有fixture不一致；
- 到期时间单位可能是秒或毫秒但无法确认；
- 日期缺失可能来自provider而非UI；
- 真实运行程序路径与仓库路径不一致；
- 发现正在运行旧副本；
- 修改可能触及token、auth或外部provider；
- 配置schema行为可能导致用户数据覆盖；
- 实体测试无法证明某项兼容结论。

应当：

1. 保留当前安全行为；
2. 输出脱敏诊断；
3. 创建最小失败fixture；
4. 在Issue/ADR中记录未知项；
5. 不将未验证结果标记为Pass。

---

# 16. 最终输出要求

Codex完成后必须输出：

1. 修改摘要；
2. Root cause；
3. 修改文件列表；
4. 新增测试列表；
5. 自动检查结果；
6. Windows实体测试结果；
7. 尚未完成的阻塞项；
8. 每个提交SHA；
9. 是否满足v0.3.0 Release Candidate；
10. 若不满足，明确列出剩余工作。

不得只回复“已修复”或“测试通过”，必须提供可验证证据。
