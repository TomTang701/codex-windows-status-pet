# ACTIVE GOAL — 专业、精简、连续的小版本发布列车

> **Repository:** `TomTang701/codex-windows-status-pet`  
> **Authority:** 本文件是 `Goal/` 中唯一具有执行效力的Goal，并内置完整启动协议  
> **Current main baseline:** `477acc20e635e76a98fb3e4579bd796b264bd12e`  
> **Current product version:** `0.2.0`  
> **Existing oversized draft PR:** `#2`  
> **Current target version:** `0.2.1`  
> **Supported platform:** Windows 11 x64  
> **Execution mode:** 可以持续运行，但任何时刻只能有一个活动版本  
> **Release model:** 一个版本、一个主题、一个分支、一个PR、一个tag  
> **Product character:** 被动显示、界面简洁、本地运行、低资源占用、不易误触  
> **Authorized release train:** `0.2.1` → `0.2.2` → `0.2.3` → `0.2.4` → `0.2.5` → `0.2.6` → `0.3.0` → `0.3.1` → `0.3.2`

---

# 0. Codex启动协议

本节是每次Codex开始执行本Goal时的强制入口。

Codex收到类似以下任一指令时：

```text
请读取并执行 Goal/ACTIVE_GOAL.md
```

或：

```text
继续执行当前ACTIVE_GOAL
```

必须自动完成本节，不需要用户再次粘贴详细说明。

## 0.1 权威来源

执行优先级：

```text
1. Goal/ACTIVE_GOAL.md
2. Goal/ACTIVE_VERSION_BRIEF.md
3. Goal/EXECUTION_STATE.md
4. 当前版本直接相关的规范文件
5. 当前PR描述
6. Roadmap
7. 历史归档和Git历史
```

规则：

- `Goal/ACTIVE_GOAL.md`是唯一规范性开发目标；
- 旧Goal、归档计划、旧PR描述与本文件冲突时，必须忽略旧内容；
- 不得从历史Goal推导新的活动任务；
- 仓库事实比文件中陈旧的SHA、版本或分支信息优先，但必须记录差异；
- 产品方向、资源红线和版本范围不得因仓库状态变化而自动放宽。

## 0.2 启动检查

开始编码前自动执行：

```powershell
git fetch --all --prune
git status
git branch --show-current
git log -5 --oneline
git diff
```

并检查：

```text
最新main SHA
当前产品版本
开放PR
相关分支
远程tag
是否存在未完成merge/rebase/cherry-pick
Goal目录内容
ACTIVE_VERSION_BRIEF状态
EXECUTION_STATE状态
当前授权版本
```

## 0.3 Goal目录清理

确认`Goal/`只包含：

```text
ACTIVE_GOAL.md
ACTIVE_VERSION_BRIEF.md
EXECUTION_STATE.md
README.md
```

处理规则：

- 多余旧Goal移入`docs/archive/plans/`或删除；
- 归档文件必须是非规范性；
- 不得保留多个`ACTIVE_GOAL`副本；
- `ACTIVE_VERSION_BRIEF.md`只描述当前活动版本；
- 已完成版本的`EXECUTION_STATE.md`必须删除或重置。

## 0.4 基线校准

如果本文件记录的：

```text
main SHA
产品版本
PR状态
分支状态
tag状态
```

与GitHub实际情况不同：

1. 以最新远程仓库事实为准；
2. 不直接假设旧计划仍可执行；
3. 更新Brief中的实际基线；
4. 检查当前版本是否已经部分或全部完成；
5. 避免重复实现；
6. 记录差异及处理方式；
7. 不因基线变化混入下一版本内容。

## 0.5 创建当前版本Brief

编码前创建或更新：

```text
Goal/ACTIVE_VERSION_BRIEF.md
```

必须完成：

```text
Product
Applicability Matrix
Visual/UI/UX（适用时）
Frontend（适用时）
Backend（适用时）
QA/Release
Security/Resource
Scope Lock
```

只有以下条件同时满足才能开始生产代码：

```text
Product Decision = GO
适用角色Decision = PASS
Scope Lock完整
分支从最新main建立
当前版本明确
```

## 0.6 首次启动汇报

第一次读取本Goal，或仓库基线发生显著变化时，先向用户汇报：

```text
当前main SHA和产品版本
开放PR和相关分支
远程tag状态
Goal目录清理结果
当前活动版本
Product Decision
允许范围
明确非目标
第一个安全执行步骤
```

完成这次汇报后：

- 普通开发步骤无需逐项等待确认；
- 可以按本Goal持续串行执行；
- 只有遇到红线、权限不足、产品方向变化、无法保持单一范围或不可逆风险时暂停。

## 0.7 自动持续执行

当当前版本完成后，不需要用户再次发送整段启动指令。

若官方服务仍允许，必须：

1. 完成当前版本Transition Gate；
2. 确认远程tag；
3. 清理当前分支和Brief；
4. 从最新main创建下一授权版本分支；
5. 创建新的ACTIVE_VERSION_BRIEF；
6. 重新进行专业角色适用性评审；
7. 只开发下一版本；
8. 重复完整发布生命周期。

## 0.8 中断恢复

收到：

```text
继续执行当前ACTIVE_GOAL
```

时必须：

1. 读取`Goal/EXECUTION_STATE.md`；
2. fetch远程状态；
3. 核对branch和last pushed SHA；
4. 检查未完成Git操作；
5. 重新运行最后一个已记录测试；
6. 从`Next exact action`继续；
7. 不重新开始已经验证并推送的工作。

## 0.9 禁止事项

启动指令不得被解释为授权：

```text
绕过平台额度
同时开发多个版本
跳过PR或tag
直接批量修改main
忽略资源红线
自动开始0.4.0
执行归档Goal
运行无意义任务消耗额度
```

---

# 1. 为什么需要更新专业开发流程

旧流程存在以下风险：

1. 每个角色在每个版本都产生大量材料，容易形成形式主义。
2. 产品、视觉、前端和后端的职责存在重叠，决策责任不够清晰。
3. 一份Goal同时详细描述很多未来版本，容易让Codex提前实施后续任务。
4. 长时间连续运行时，容易把“持续执行”误解为“批量完成多个版本”。
5. 没有明确规定哪些专业评审是必需的、哪些可标记为不适用。
6. 资源安全虽有原则，但缺少每个PR都必须回答的具体检查项。
7. 版本完成后的观察、回滚和下一版本重新确认不够轻量化。

新版采用：

```text
精简跨职能Stage Gate
+ 按需角色评审
+ 单一责任人
+ 单版本范围锁
+ 连续但严格串行的发布列车
```

目标是在保持专业标准的同时，不让流程本身拖慢产品。

---

# 2. 最高优先级规则

## 2.1 Goal目录

`Goal/`只允许以下文件：

```text
Goal/
├─ ACTIVE_GOAL.md
├─ ACTIVE_VERSION_BRIEF.md
├─ EXECUTION_STATE.md
└─ README.md
```

规则：

- `ACTIVE_GOAL.md`：唯一有效Goal。
- `ACTIVE_VERSION_BRIEF.md`：当前版本的精简跨职能说明。
- `EXECUTION_STATE.md`：仅在执行中断或需要checkpoint时存在。
- `README.md`：只描述Goal目录规则。

禁止：

```text
Goal/CODEX_GOAL_*.md
Goal/v0.2.1.md
Goal/v0.2.2.md
多个ACTIVE_GOAL副本
归档计划留在Goal目录
```

旧Goal：

- 有长期参考价值的移入 `docs/archive/plans/`；
- 其余删除；
- Git历史已经保留旧内容；
- 归档文件必须标记为 `status: archived` 和 `normative: false`。

## 2.2 单活动版本

任何时刻只能有：

```text
一个活动版本
一个release分支
一个活动PR
一个版本Brief
一个锁定范围
```

不得：

- 同时开发两个版本；
- 当前PR未合并就开始下一版本；
- 当前版本夹带下一版本代码；
- 一个PR包含多个版本号；
- 使用大型integration PR替代多个小版本；
- 因为运行时间充足而扩大版本范围。

## 2.3 连续运行

Codex可以持续运行，只要官方服务允许。

连续运行的含义是：

```text
完成版本A的完整生命周期
→ 关闭版本A
→ 从最新main创建版本B
→ 完成版本B
```

不代表：

```text
同时编码A和B
一次性合并A到D
一个PR打多个tag
```

每个版本之间必须经过正式Transition Gate。

---

# 3. 精简跨职能Stage Gate

每个版本使用七个阶段。

```text
Gate 0  Repository Sync
Gate 1  Product Scope
Gate 2  Design & Technical Applicability
Gate 3  Implementation
Gate 4  Verification
Gate 5  Release
Gate 6  Post-release Observation
```

只有当前Gate通过，才能进入下一个Gate。

---

# 4. Gate 0 — Repository Sync

开始任何版本前执行：

```powershell
git fetch --all --prune
git status
git branch --show-current
git log -5 --oneline
git diff
```

确认：

```text
[ ] main是最新远程main
[ ] 工作区干净
[ ] 没有未完成merge/rebase/cherry-pick
[ ] 上一个版本tag存在于远程
[ ] 没有第二个活动release分支
[ ] Goal目录只有一个ACTIVE_GOAL
[ ] EXECUTION_STATE没有指向已完成版本
```

如果任一项失败，先修复仓库状态，不得开始产品开发。

---

# 5. Gate 1 — 产品经理范围锁

产品经理视角始终必需。

产品经理不是要求Codex写长篇分析，而是要求形成明确决策。

每个版本必须在 `Goal/ACTIVE_VERSION_BRIEF.md` 中填写：

```markdown
## Product

- Version:
- One-sentence outcome:
- Target user:
- User problem:
- Why now:
- Success criteria:
- Explicit non-goals:
- Misuse risk:
- User-resource impact:
- Decision: GO / SPLIT / DEFER / REMOVE
```

## 5.1 产品经理职责

必须判断：

- 这个版本是否解决真实问题；
- 是否与Codex内置功能重复；
- 是否增加不必要的按钮或设置；
- 是否容易误触；
- 是否消耗CPU、内存、磁盘、网络、用户注意力或金钱；
- 是否可以通过删除功能而不是增加功能来解决；
- 是否可以用一句话解释；
- 是否应拆成更小版本。

## 5.2 GO条件

只有同时满足以下条件才能GO：

```text
一个主要结果
明确用户价值
明确非目标
可独立测试
可独立回滚
不越过资源/隐私红线
没有夹带下一版本任务
```

## 5.3 自动拆分条件

出现任何一项必须选择`SPLIT`：

- PR描述需要用“以及”连接两个独立结果；
- 同时包含用户功能和CI治理；
- 同时包含UI功能和架构重构；
- 同时修改两个无直接依赖的产品区域；
- 需要选择性回滚；
- 一个版本内出现两个不同用户故事；
- 预计无法在一个短PR中完成专业review。

---

# 6. Gate 2 — 专业角色适用性评审

采用“按需参与”，避免每个版本都制造无关文档。

## 6.1 始终必需

以下角色每个版本都参与：

```text
Product Manager
QA / Release Engineer
Security & Resource Reviewer
```

## 6.2 按变更类型参与

| 变更类型 | 视觉/UI | 前端 | 后端 |
|---|---:|---:|---:|
| 菜单、布局、颜色、字体、交互 | 必需 | 必需 | 视情况 |
| Tk状态、事件、窗口、托盘 | 视情况 | 必需 | 视情况 |
| Quota解析、Activity扫描 | 不适用 | 视情况 | 必需 |
| 设置schema、保存、备份 | 不适用 | 视情况 | 必需 |
| CI、Release脚本 | 不适用 | 不适用 | 必需 |
| 纯文档治理 | 视情况 | 不适用 | 视情况 |
| Windows实体测试记录 | 视情况 | 必需 | 必需 |

不适用时只记录：

```text
Not applicable — no impact in this version.
```

不得为了体现“专业”而编造无关评审。

---

# 7. 专业角色标准

## 7.1 产品经理

负责：

- 用户问题；
- 优先级；
- 版本范围；
- 非目标；
- 成功条件；
- 是否删除或延期功能；
- 最终`GO/SPLIT/DEFER/REMOVE`决定。

产品原则：

- 功能少而准确；
- 不重复Codex已有控制；
- 不把开发者工具放入普通菜单；
- 不以消耗额度、提升使用时长或增加互动为目标；
- 不为了Roadmap而开发没有真实价值的功能。

## 7.2 视觉/UI/UX设计师

仅在用户可见变化时必需。

检查：

```text
视觉层级
字体和间距
对齐
颜色对比
菜单长度
控件分组
误触风险
Windows 11一致性
支持的字体大小
窗口最小尺寸
单屏/双屏表现
Compact/Expanded状态
```

设计原则：

- 安静、紧凑、清晰；
- 不增加无价值动画；
- 不增加装饰性阴影、渐变或闪烁；
- 不通过颜色作为唯一信息；
- 不新增图片素材，除非确实提升理解；
- 不让状态宠物看起来像Codex官方操作按钮；
- 恢复、诊断和危险操作不进入普通菜单。

Brief字段：

```markdown
## Visual/UI/UX

- Applicable: Yes / No
- Affected component:
- Before:
- After:
- Labels:
- Layout/spacing:
- Interaction states:
- Accessibility:
- Misclick prevention:
- Windows 11 physical check:
- Decision: PASS / REVISE / N/A
```

## 7.3 前端工程师

负责：

```text
Tk组件
事件绑定
窗口/菜单/对话框
Compact状态
显示器和DPI
UI主线程
布局和渲染
键盘和鼠标行为
```

红线：

- Tk调用只能在主线程；
- UI线程不能做文件、子进程或阻塞IPC；
- 子Widget必须保留必要拖动、hover和右键事件；
- 首次点击必须有效；
- 关闭菜单必须释放grab；
- 设置窗口不能让主窗口丢失；
- 不为内部机制增加普通用户按钮。

Brief字段：

```markdown
## Frontend

- Applicable: Yes / No
- Components:
- State transitions:
- Event flow:
- Thread boundary:
- Layout impact:
- Tests:
- Physical verification:
- Decision: PASS / REVISE / N/A
```

## 7.4 后端工程师

负责：

```text
本地app-server
Quota规范化
Activity扫描
刷新调度
配置schema
原子保存
线程和队列
日志
缓存和资源边界
shutdown
```

红线：

- 不读取`auth.json`；
- 不提取或记录token；
- 不把原始provider payload送入UI；
- 最多一个Quota worker和一个Activity worker；
- 无界重试禁止；
- 缓存、日志和备份必须有边界；
- Activity与Quota保持独立；
- 不添加第三方endpoint；
- 不添加遥测或云日志；
- 不添加付费API；
- 故障时不得伪造数据。

Brief字段：

```markdown
## Backend

- Applicable: Yes / No
- Data/API contract:
- Ownership:
- Concurrency:
- Persistence:
- Failure modes:
- Network/IPC:
- CPU/memory/disk:
- Tests:
- Rollback:
- Decision: PASS / REVISE / N/A
```

## 7.5 QA / Release工程师

每个版本都必需。

负责：

```text
正向测试
负向测试
回归测试
资源检查
安全检查
Windows 11实体检查
CI
版本一致
Changelog
tag
rollback
```

Brief字段：

```markdown
## QA / Release

- Positive cases:
- Negative cases:
- Regression cases:
- Resource checks:
- Security/privacy checks:
- Windows 11 checks:
- Quality commands:
- Rollback:
- Decision: PASS / FAIL
```

## 7.6 Security & Resource Reviewer

每个版本都必须回答：

```text
是否新增网络或IPC？
是否新增worker或subprocess？
是否增加刷新频率？
是否增加磁盘写入？
是否保留更多数据？
是否增加日志或缓存？
是否增加UI注意力成本？
是否可能花费用户金钱？
是否可能消耗更多Codex额度？
```

任一答案为`Yes`时必须给出：

- 业务必要性；
- 上限；
- 测试或测量；
- 回滚方案；
- 维护者明确批准。

---

# 8. ACTIVE_VERSION_BRIEF长度限制

`Goal/ACTIVE_VERSION_BRIEF.md`必须简洁。

建议上限：

```text
不超过150行
不超过约2–3页
```

它必须包含：

```text
Identity
Product
Applicability Matrix
Visual/UI/UX（适用时）
Frontend（适用时）
Backend（适用时）
QA/Release
Security/Resource
Scope Lock
```

禁止：

- 复制完整Roadmap；
- 重复API规范；
- 长篇理论说明；
- 粘贴测试日志；
- 写隐藏推理过程；
- 包含用户私密数据。

详细设计应进入对应规范文件或代码测试，而不是无限扩展Brief。

---

# 9. Gate 3 — 实施标准

## 9.1 开始条件

实施前必须满足：

```text
[ ] Product Decision = GO
[ ] 适用角色已PASS
[ ] Scope Lock完整
[ ] 分支从最新main建立
[ ] 当前版本号明确
```

## 9.2 开发纪律

- 只修改当前版本允许的文件；
- 发现独立问题时记录到未来版本，不顺手修复；
- 每个commit只有一个可验证目的；
- 不创建WIP噪声commit；
- 不大范围格式化无关文件；
- 不修改远程owner和Git身份；
- 不直接推送重大变更到main。

## 9.3 资源纪律

禁止：

```text
忙循环
频繁无意义轮询
无限日志
无限缓存
无限重试
为耗额度而生成任务
外部遥测
广告
云同步
后台付费API
自动下载更新
```

---

# 10. Gate 4 — Verification

每个版本使用分层测试。

## 10.1 必需层

```text
Focused unit/contract tests
Relevant integration tests
Full Quality gate
git diff --check
```

## 10.2 按需层

```text
Tk adapter tests
Windows 11 physical verification
resource measurement
package smoke
strict Release Candidate
```

## 10.3 通用命令

根据仓库当前可用脚本执行：

```powershell
python -m compileall -q scripts
python -m unittest discover -s tests -q
python scripts/check_doc_manifest.py
python scripts/check_doc_links.py
python scripts/check_doc_parity.py
python scripts/check_version_sources.py
python scripts/check_sensitive_files.py
python scripts/check_dependencies.py
python scripts/package_smoke_test.py
git diff --check
```

存在统一Quality runner后优先执行：

```powershell
python scripts/run_quality_checks.py
```

不得为了让CI变绿而降低检查标准。

---

# 11. Gate 5 — Release

每个版本必须完成：

```text
版本源更新
正式Changelog章节
commit
push
版本PR
CI
review
merge
更新本地main
main复测
tag
push tag
远程tag确认
删除release分支
```

## 11.1 分支和PR

```text
Branch: release/vX.Y.Z-short-topic
PR: [vX.Y.Z] One-sentence outcome
Tag: vX.Y.Z
```

推荐squash merge，使一个版本可以整体revert。

## 11.2 PR必须包含

```text
版本
单句结果
用户问题
范围
明确非目标
角色适用性
文件
测试
资源影响
安全隐私
Windows 11证据
回滚
```

## 11.3 Tag规则

不得给以下状态打tag：

- 未合并分支；
- 测试失败；
- 版本源不一致；
- Changelog缺失；
- PR范围混入下一版本；
- main尚未复测。

---

# 12. Gate 6 — Post-release Observation

每个版本发布后做最小观察：

```text
启动应用
确认核心显示
确认本版本结果
检查是否有明显错误日志
确认退出
确认再次启动
```

只记录真实缺陷。

发现问题：

- 严重数据/隐私/启动问题：立即建立patch版本；
- 非严重问题：进入后续版本候选；
- 不在下一版本中偷偷修复。

---

# 13. 版本Transition Gate

版本A完成后，进入版本B前必须全部满足：

```text
[ ] A只有一个主要结果
[ ] A的Brief完整
[ ] A没有夹带B代码
[ ] A测试通过
[ ] A Quality通过
[ ] A PR已合并
[ ] 最新main已获取
[ ] A Changelog正式章节存在
[ ] A版本源一致
[ ] A远程tag存在
[ ] A post-release smoke通过
[ ] A分支已关闭或删除
[ ] A release报告完成
[ ] 工作区干净
[ ] 没有未完成Git操作
[ ] B从最新tagged main创建
[ ] B建立全新Brief
```

任一项失败：

```text
留在A
修复、revert或明确失败
不得开始B
```

---

# 14. 持续运行与额度中断

## 14.1 正常持续执行

只要官方服务允许，可以连续完成多个**串行**小版本。

必须保持：

```text
任何时刻一个版本
任何时刻一个分支
任何时刻一个活动PR
```

## 14.2 禁止额度规避

不得：

- 使用提示词绕过额度；
- 伪装工作规避计量；
- 轮换账号规避限制；
- 修改客户端或时钟欺骗服务；
- 创建无意义任务消耗额度；
- 把“用尽额度”当作成功标准。

## 14.3 硬限制checkpoint

平台硬性中断前或预计即将中断时：

1. 不启动新任务；
2. 完成当前安全文件/Git操作；
3. 不留下冲突或半完成rebase；
4. 运行最小相关测试；
5. 只提交已验证内容；
6. push当前分支；
7. 更新 `Goal/EXECUTION_STATE.md`；
8. 记录下一条精确命令；
9. 下一窗口从checkpoint恢复。

---

# 15. 现有大型PR #2处理

PR #2包含多个独立主题，不应整体作为一个版本合并。

执行：

1. 验证当前head SHA；
2. 建立只读归档分支：

```text
archive/pr2-reset-credit-hardening-2026-07-10
```

3. 在PR #2说明它被小版本发布列车替代；
4. 关闭PR #2，不合并；
5. 保留原分支直到有用改动全部重新分配；
6. 不在该分支继续开发；
7. 后续版本按需重新实现或选择性提取hunk；
8. 禁止盲目cherry-pick混合commit。

---

# 16. 当前版本：v0.2.1 — 精简右键菜单

## 16.1 单一结果

将状态宠物右键菜单精简为普通用户真正需要的窗口控制。

移除：

```text
立即刷新
复制诊断摘要
恢复上次设置
```

保留：

```text
显示设置
置顶
锁定位置
隐藏窗口
退出
```

## 16.2 产品经理判断

用户问题：

- 菜单过长；
- 内部维护功能会增加误触；
- 手动刷新与Codex内置能力重复；
- 恢复设置属于高级操作；
- 复制诊断不属于普通使用场景。

版本价值：

```text
更简单
更清晰
更低误触风险
不改变自动刷新
不移除后台安全机制
```

Decision：

```text
GO
```

## 16.3 角色适用性

| 角色 | 适用 |
|---|---|
| Product | Yes |
| Visual/UI/UX | Yes |
| Frontend | Yes |
| Backend | Limited |
| QA/Release | Yes |
| Security/Resource | Yes |

## 16.4 允许范围

优先修改：

```text
scripts/ui/context_menu.py
相关菜单测试
CHANGELOG中英文
直接受影响的产品/API说明
版本源
```

只有确认无调用者时才允许删除：

```text
copy_diagnostics
diagnostic_summary_api
```

后台保留：

```text
自动Quota刷新
本地脱敏日志
原子设置保存
内部.bak备份
```

## 16.5 明确非目标

本版本禁止包含：

```text
Reset Credit日期修复
配置schema写入保护
独立状态行
控制器重构
Windows支持范围
CI拆分
文档治理
新功能
```

## 16.6 设计要求

菜单最终只有五项。

要求：

- 分组清晰；
- 不添加图标或装饰；
- 不添加确认弹窗；
- 首次点击有效；
- Escape关闭；
- FocusOut关闭；
- grab正确释放；
- 菜单不被任务栏裁切。

## 16.7 前端要求

验证：

```text
显示设置调用show_settings
置顶调用toggle_topmost
锁定调用toggle_locked
隐藏调用hide_window
退出调用close
```

删除所有已移除动作的Widget和绑定。

## 16.8 后端要求

确认：

- 自动refresh没有变化；
- 不增加worker；
- 不增加IPC；
- 不增加磁盘写入；
- 删除UI入口不破坏后台日志和备份；
- 不重新暴露任何维护按钮。

## 16.9 测试

必须验证：

```text
菜单恰好包含五个批准项
不存在立即刷新
不存在复制诊断摘要
不存在恢复上次设置
first-click有效
close释放grab
Escape关闭
FocusOut关闭
自动refresh路径未改变
```

## 16.10 版本和发布

```text
Branch: release/v0.2.1-minimal-context-menu
Version: 0.2.1
Tag: v0.2.1
```

完成后执行Transition Gate，再进入`0.2.2`。

---

# 17. 后续授权版本大纲

每次进入新版本前必须重新创建Brief，但无需等待人工回复，只要原计划仍然符合本Goal且没有红线变化。

## v0.2.2 — Reset Credit日期正确性

单一结果：

```text
重置 N 次 / HH:MM M/D
```

保持5h只显示`HH:MM`。

主要角色：

```text
Product
Backend
Frontend（仅展示验证）
QA/Release
Security/Resource
```

禁止夹带状态行重构。

## v0.2.3 — 配置写入保护

单一结果：

```text
未来schema或损坏配置不会被旧版本自动覆盖
```

主要角色：

```text
Product
Backend
Frontend（高级reset流程适用时）
QA/Release
Security/Resource
```

禁止恢复普通菜单按钮。

## v0.2.4 — Windows 11支持和矩阵正确性

单一结果：

```text
支持声明和可执行发布阻塞规则一致
```

Windows 10：

```text
Deferred
Not claimed
Non-blocking
```

## v0.2.5 — Quality和Release Candidate分离

单一结果：

```text
日常Quality不冒充正式发布批准
```

只修改CI、检查脚本、测试和发布说明。

## v0.2.6 — 文档治理

单一结果：

```text
建立一个足够但不过度的可执行文档治理系统
```

必须确保：

- 只有ACTIVE_GOAL有效；
- 旧Goal不污染执行；
- 归档计划不阻塞发布；
- 不增加无价值文档门禁。

## v0.3.0 — 独立稳定状态行

单一用户能力：

```text
五行状态各自独立渲染
```

不得同时做控制器重构。

## v0.3.1 — 控制器重构

单一内部结果：

```text
降低Tk主窗口协调职责，不改变用户行为
```

## v0.3.2 — Windows 11稳定化

单一结果：

```text
完成声明范围内的实体验证并通过严格Release Candidate
```

不增加新功能。

---

# 18. 长期路线

## 18.1 0.2.x

目标：

```text
正确性
配置安全
支持契约
发布基础
Goal治理
```

## 18.2 0.3.x

目标：

```text
UI稳定
内部职责清晰
Windows 11发布就绪
```

## 18.3 0.4.x–0.6.x

不预先批准具体功能。

候选必须满足：

- 被动显示价值；
- 不重复Codex；
- 不增加高误触控制；
- 不增加外部网络；
- 不增加付费依赖；
- 一个版本一个能力。

## 18.4 0.7.x–0.8.x

可能方向：

```text
可复现打包
安装说明
卸载和回滚
日志边界
升级/降级验证
```

禁止：

- 强制开机启动；
- 静默安装；
- 自动后台下载；
- 虚假签名声明。

## 18.5 0.9.x

功能冻结。

重点：

```text
资源测量
稳定性
升级恢复
Release Candidate缺陷
```

## 18.6 1.0.0

达到以下条件：

```text
核心显示稳定
Windows 11范围真实验证
配置迁移/降级策略明确
没有已知数据丢失
没有凭据/隐私问题
资源占用经过测量
日志缓存有界
安装/卸载/回滚明确
artifact可复现
已有多个成功小版本
```

---

# 19. 资源红线

## 网络

允许：

```text
已批准的本地Codex app-server
```

禁止：

```text
第三方Quota API
遥测
分析
广告
远程配置
云日志
账号同步
隐藏网络流量
```

## CPU

禁止：

```text
忙循环
无延迟轮询
无限subprocess重启
重复全量扫描
为了耗额度运行任务
```

## 内存

禁止：

```text
保存完整原始provider历史
保存prompt/response/session正文
无界缓存
Widget或tray泄漏
```

## 磁盘

禁止：

```text
无限日志
原始quota dump
复制项目/session
无限备份代数
未管理build文件
```

## 用户注意力

禁止：

```text
不必要通知
重复弹窗
闪烁
重复Codex按钮
普通菜单里的恢复/诊断动作
```

## 用户金钱

禁止：

```text
付费外部API
订阅依赖
自动调用计费服务
以消耗用户周额度为目标
```

---

# 20. 每版本发布报告

每个版本完成后，在PR和最终输出中报告：

```text
版本
一句话结果
Product决定
角色适用性
Visual结论
Frontend结论
Backend结论
QA/Release结论
明确非目标是否遵守
文件
测试
Windows 11证据
资源影响
安全隐私
PR URL
merge SHA
远程tag
post-release smoke
rollback
下一授权版本
```

明确写出：

```text
No work from the next version was included.
```

---

# 21. 本Goal结束条件

Codex可以连续按顺序推进至：

```text
v0.3.2
```

本Goal结束于以下任一条件：

1. `v0.3.2`完成合并、验证、tag和报告；
2. 官方平台硬性中断，已建立安全checkpoint；
3. 出现安全、隐私、资源红线；
4. 当前版本不能保持单一范围，需要重新规划；
5. GitHub权限阻止必要的push、merge或tag；
6. 真实仓库状态与本Goal基线不一致且无法安全解决。

禁止在本Goal中开始`v0.4.0`。

`v0.4.0`必须由新的唯一`ACTIVE_GOAL.md`选择一个明确产品能力。
