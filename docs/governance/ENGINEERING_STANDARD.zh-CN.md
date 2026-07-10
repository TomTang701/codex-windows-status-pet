---
document_id: ENGINEERING-STANDARD
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/governance/ENGINEERING_STANDARD.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# Codex Windows Status Pet 工程开发总规范

> **Document-Version:** 1.0.0  
> **Status:** 当前生效的中文翻译副本
> **Canonical-Language:** English  
> **Translation-Source:** `ENGINEERING_STANDARD.md`  
> **Applies-To:** `TomTang701/codex-windows-status-pet`  
> **Baseline:** `main` 分支文档框架采用基线
> **Owner:** 项目维护者  
> **Review-Cadence:** 每个次版本至少检查一次，并且至少每90天检查一次  
> **Last-Reviewed:** 2026-07-10

---

## 1. 目的

本文档是 Codex Windows Status Pet 的最高层级工程规范，定义在功能扩展、重构、UI变化、打包方式变化以及未来协作者加入时仍应保持稳定的规则。

本文档刻意与以下文件分离：

- `docs/product/ROADMAP.md`：描述路线优先级；
- `docs/architecture/API_SPEC.md`：记录具体API契约和不变量；
- `docs/architecture/REPOSITORY_STRUCTURE.md`和`docs/architecture/CONFIGURATION.md`：记录仓库布局和持久化格式；
- `docs/quality/COMPATIBILITY_MATRIX.md`：记录测试证据；
- `CHANGELOG.md`：记录已发布和未发布变更。

文件发生冲突时，优先级如下：

1. 本规范中的安全和隐私要求；
2. 本规范中的运行时不变量；
3. 已批准的架构决策记录；
4. `docs/architecture/API_SPEC.md`；
5. `docs/architecture/CONFIGURATION.md`；
6. `docs/product/ROADMAP.md`；
7. README和示例。

---

## 2. 规范用语

关键词 **MUST**、**MUST NOT**、**REQUIRED**、**SHOULD**、**SHOULD NOT** 和 **MAY** 具有规范含义。

- **MUST / MUST NOT：** 合并或发布的强制要求；
- **SHOULD / SHOULD NOT：** 除非存在已批准例外，否则应遵守；
- **MAY：** 可根据上下文选择。

任何违反MUST的例外必须包含：

1. 书面理由；
2. 适用范围和到期日期；
3. 风险分析；
4. 维护者批准；
5. 跟踪Issue或ADR。

---

## 3. 产品契约

### 3.1 产品目标

本产品是一个低干扰的Windows桌面伴侣工具，应当：

- 报告真实的本地Codex活动；
- 显示真实可信的额度和重置信息；
- 在Windows多显示器环境中始终可恢复；
- 不修改Codex核心文件；
- 不依赖项目自建后端；
- 保持狭窄的本地数据边界。

### 3.2 核心差异化

以下能力定义了产品价值，必须受到回归测试保护：

1. 活动状态来自本地Codex会话事件，而不是只通过额度变化推测。
2. 额度通过本机Codex app-server边界读取。
3. 悬浮窗可通过托盘和显示恢复路径重新找回。
4. 用户设置经过校验、具有事务语义并可恢复。
5. 支持包含负坐标的Windows虚拟桌面坐标。
6. 数据源缺失或损坏时不得伪造数值。

### 3.3 明确排除范围

除非完成安全评审并批准ADR，否则以下内容不进入范围：

- 直接读取 `auth.json`；
- 提取或保存access token；
- 第三方额度服务；
- 遥测或分析；
- 云同步；
- 修改Codex核心或内置宠物文件；
- 收集提示词、回答或项目内容；
- 自动使用Reset Credit；
- macOS或Linux支持；
- Tauri或其他框架的整体重写。

---

## 4. 文档架构

### 4.1 必需的规范文件

仓库应当维护以下文件体系：

| 文档 | 用途 | 更新触发条件 |
|---|---|---|
| `ENGINEERING_STANDARD.md` | 稳定的全项目工程规则 | 政策或治理变化 |
| `ARCHITECTURE.md` | 组件、依赖方向、生命周期、并发 | 架构变化 |
| `docs/architecture/API_SPEC.md` | API契约、类型、不变量、错误行为 | API行为变化 |
| `docs/architecture/REPOSITORY_STRUCTURE.md`和`docs/architecture/CONFIGURATION.md` | 仓库布局、配置schema、文件归属 | 文件或schema变化 |
| `SECURITY.md` | 威胁模型、隐私边界、漏洞流程 | 安全边界变化 |
| `TESTING.md` | 测试分层、fixture、命令、证据规则 | 测试策略变化 |
| `RELEASE.md` | 版本、门禁、打包、回滚 | 发布流程变化 |
| `CONTRIBUTING.md` | 分支、提交、PR、审查流程 | 协作流程变化 |
| `docs/product/ROADMAP.md` | 当前路线和优先级 | 计划变化 |
| `docs/quality/COMPATIBILITY_MATRIX.md` | Windows实体和自动证据 | 兼容性结果变化 |
| `CHANGELOG.md` | 发布历史 | 用户可见变化 |
| `README.md` | 用户介绍和安装 | 用户流程变化 |

### 4.2 文档分类

文档分为：

- **规范类：** 定义必须遵守的行为或流程；
- **描述类：** 解释当前设计；
- **证据类：** 记录测试结果；
- **生成类：** 由工具生成。

规范类英文文档必须拥有同步的中文翻译副本。证据和生成文件在重复维护没有价值时，可以保持语言中立或只使用英文。

### 4.3 唯一事实来源

英文为原版。中文文档：

- 必须是英文配对文件的翻译；
- 不得加入英文原版中不存在的要求；
- 必须保持标题、API名称、ID、表格、版本和代码示例一致；
- 英文发生实质变化时，必须在同一提交中更新中文。

---

## 5. 架构原则

### 5.1 依赖方向

依赖必须向内流动：

```text
Windows/Tk适配层
        ↓
应用控制层
        ↓
领域服务和状态机
        ↓
纯模型、校验、格式化和策略
```

规则：

- 领域API不得导入Tkinter或pystray。
- 纯API不得执行文件系统、子进程、网络或Windows UI调用。
- UI适配层可以调用领域API。
- 传输适配层可以返回领域值，但不得修改UI。
- 后台worker必须通过队列或主线程调度回调与Tk通信。
- 禁止循环导入。

### 5.2 模块归属

每个模块必须具有：

- 一个主要职责；
- 明确的公开接口；
- 已记录的副作用；
- 已记录的线程要求；
- 在可行时具备确定性测试；
- 明确归属：领域、传输、平台、应用或UI。

当模块同时负责以下两个或更多内容时，应当拆分：

- 持久化；
- 传输；
- 解析；
- 状态转换；
- 调度；
- Windows平台调用；
- UI控件。

### 5.3 UI适配层规则

UI代码可以：

- 创建和排列控件；
- 绑定用户操作；
- 渲染领域状态；
- 调用应用控制层；
- 显示已经校验的警告。

UI代码不得：

- 解析原始额度payload；
- 直接读写配置文件；
- 实现重试或退避策略；
- 管理token或凭据；
- 执行阻塞的子进程或文件系统操作；
- 包含唯一正式的校验或几何算法。

### 5.4 架构决策记录

重要架构选择必须在以下目录创建ADR：

```text
docs/adr/NNNN-short-title.md
```

以下情况必须使用ADR：

- 更换UI框架；
- 增加新的provider；
- 修改凭据边界；
- 修改配置格式；
- 更换打包技术；
- 修改支持的Windows版本；
- 引入数据库或后端；
- 更换并发模型；
- 破坏既有API。

已批准ADR不可修改。后续ADR通过“取代”关系更新决策。

---

## 6. API契约标准

### 6.1 契约要求

每个公开API必须记录：

- 目的；
- 接受的输入；
- 返回值；
- 副作用；
- 线程安全；
- 错误行为；
- 安全边界；
- 兼容性承诺；
- 测试边界。

### 6.2 输入与输出设计

API应优先使用带类型的dataclass、enum和明确结果对象，而不是无结构dict。

原始provider字典：

- 必须停留在传输/解析边界；
- 不得进入UI代码；
- 不得持久化；
- 不得完整写入日志。

领域层中的时间应使用带时区的 `datetime`。显示格式属于格式化API。

### 6.3 错误契约

预期错误应通过带类型结果或已记录的异常类型表达。

API必须区分：

- 调用者输入非法；
- 外部数据损坏；
- 临时传输失败；
- 登录失效；
- 不支持的协议响应；
- 内部编程错误。

只有进程、worker或UI安全边界可以使用宽泛的 `except Exception`，并且必须记录经过脱敏的诊断信息并保留恢复能力。

### 6.4 向后兼容

出现以下情况时，公开API变更属于破坏性变更：

- 删除或重命名公开函数或字段；
- 修改单位或值的含义；
- 修改错误语义；
- 修改持久化行为；
- 修改线程安全保证。

破坏性变更必须包含：

- ADR；
- 主版本变化或1.0前明确迁移说明；
- 迁移说明；
- 兼容性测试；
- 同步文档。

---

## 7. 领域模型与状态

### 7.1 类型化领域值

额度、活动、设置事务、刷新通道和窗口状态应使用带类型的不可变值。

建议核心模型：

- `UsageWindow`；
- `ResetCreditSummary`；
- `QuotaSnapshot`；
- `QuotaDisplayState`；
- `ActivitySnapshot`；
- `DisplaySnapshot`；
- `SettingsSnapshot`；
- `WindowPlacement`；
- `RefreshChannelState`。

### 7.2 状态机要求

存在实质状态转换的行为必须建模为状态机，而不是散落的布尔变量。

候选状态机包括：

- 额度loading/ok/stale/signed-out/unavailable；
- 设置persisted/runtime/draft/opening状态；
- compact/expanded/hovered/dragging/menu-open；
- 托盘starting/running/failed/restarting/stopped；
- 刷新idle/running/cancelled/shutdown。

每个状态机必须定义：

- 状态；
- 事件；
- 合法转换；
- 非法转换行为；
- 持久化行为；
- 恢复行为；
- 每个转换的测试。

---

## 8. 配置与持久化

### 8.1 配置schema

持久化配置必须包含schema版本：

```json
{
  "schema_version": 1
}
```

每个设置必须定义：

- 类型；
- 默认值；
- 最小/最大值或允许值；
- 是否可由用户编辑；
- 是否涉及安全；
- 迁移行为；
- 对应UI控件。

### 8.2 校验层级

可编辑设置必须经过三层校验：

1. 按键或候选值校验；
2. Apply/Save提交校验；
3. 配置加载校验。

任何单独一层都不足够。

### 8.3 事务语义

设置必须区分：

- 持久化设置；
- 当前运行设置；
- 草稿设置；
- 打开设置窗口时的快照。

要求：

- Apply只预览，不持久化；
- Save应用并持久化；
- 未保存时Close恢复打开时快照；
- Restore Defaults先修改草稿；
- 保存失败不得破坏上一个有效文件。

### 8.4 原子性与恢复

写入必须使用：

- 同目录临时文件；
- flush和 `fsync`；
- 原子替换；
- 脱敏错误。

引入schema迁移后，项目应保留一个last-known-good备份。

### 8.5 Schema迁移

任何schema变化必须包含：

- 旧版本和新版本；
- 确定性迁移；
- 幂等测试；
- 损坏/部分输入测试；
- 降级或回滚说明；
- Changelog条目。

禁止静默破坏性迁移。

---

## 9. 并发、调度与生命周期

### 9.1 线程归属

- Tk API必须在Tk主线程执行。
- pystray归属必须与Tk隔离。
- 传输和文件系统工作必须离开Tk线程。
- 共享可变状态必须受保护或限制在单一线程。
- 队列payload必须具有已记录的schema。

### 9.2 刷新通道

Activity和Quota刷新必须保持独立。

每个刷新通道必须定义：

- 间隔来源；
- single-flight行为；
- generation/token行为；
- 取消行为；
- shutdown行为；
- 错误退避；
- 成功恢复；
- 最大worker数量。

延迟callback在继续安排任务前必须验证generation仍为当前版本。

### 9.3 Shutdown

Shutdown必须是幂等的。

建议顺序：

1. 标记应用正在关闭；
2. 使所有调度generation失效；
3. 阻止新worker；
4. 停止托盘；
5. 停止app-server；
6. 刷新安全的持久化状态；
7. 释放mutex；
8. 销毁Tk。

开始shutdown后，任何callback都不得再次安排自身。

### 9.4 单实例

应用必须使用命名mutex或同等所有权机制。

不得：

- 只根据进程名或窗口标题杀死其他进程；
- 创建重复托盘图标；
- 在第二次启动失败时覆盖设置。

未来如需“第二次启动显示已有窗口”，必须设计明确IPC并创建ADR。

---

## 10. 可靠性与恢复

### 10.1 可靠性目标

程序必须以可见且可恢复的方式失败，而不是静默消失。

关键恢复路径：

- 托盘可恢复隐藏悬浮窗；
- 设置可恢复屏幕外悬浮窗；
- 损坏设置按字段回退；
- app-server失败不停止Activity更新；
- 临时额度失败保留last-good；
- 显示器拓扑变化不会永久丢失窗口。

### 10.2 Last-good和stale策略

额度状态模型必须定义：

- 第一次成功前为loading；
- 有效成功后为ok；
- 临时失败后保留last-good；
- 超过明确时间后为stale；
- 明确检测到未登录时为signed-out；
- provider不支持或数据损坏时为unavailable。

UI必须同时表达数据年龄和错误状态。

### 10.3 重试与退避

重试策略必须集中管理。

必须定义：

- 初始重试间隔；
- 最大间隔；
- 倍率或序列；
- 成功后重置；
- 不可重试错误；
- 用户手动刷新行为。

重试不得产生重叠worker或无限日志。

### 10.4 窗口恢复

窗口定位必须：

- 保留合法副屏和负坐标；
- 检测窗口是否完全离开所有当前work area；
- 恢复到最近的可见work area；
- 考虑任务栏保留区域；
- 定义显示器断开时行为；
- 可在没有实体显示器的测试中验证。

---

## 11. 安全与隐私

### 11.1 安全边界

默认产品必须：

- 使用本机Codex app-server数据；
- 不读取 `auth.json`；
- 不保存access token或account ID；
- 不向第三方发送提示词、回答、项目文件或会话正文；
- 不记录原始额度响应；
- 未经明确的选择加入设计和安全评审，不得增加遥测。

### 11.2 威胁模型

`SECURITY.md`必须考虑：

- 恶意或损坏配置；
- 恶意session JSONL；
- 协议响应变化；
- 可执行文件路径替换；
- 命令注入；
- 相关情况下的符号链接/reparse point；
- 日志泄露；
- 依赖被入侵；
- 未签名程序警告；
- 不安全更新机制。

### 11.3 敏感数据处理

敏感值必须排除在：

- 日志；
- 崩溃报告；
- 测试fixture；
- 截图；
- Git历史。

数据在进入诊断API前应完成脱敏。

### 11.4 外部Provider

任何外部provider必须具备：

1. Provider接口契约；
2. ADR；
3. 威胁模型更新；
4. 权限和凭据设计；
5. Token存储决定；
6. Endpoint allowlist；
7. 超时和响应大小限制；
8. 脱敏测试；
9. 失败回退；
10. 用户可见披露。

---

## 12. 诊断与可观测性

### 12.1 日志要求

日志必须足以诊断：

- 启动；
- Codex查找；
- app-server生命周期；
- 刷新错误；
- 解析错误；
- 托盘错误；
- 窗口恢复；
- 设置迁移；
- shutdown。

日志不得包含敏感内容。

### 12.2 结构化事件

诊断应使用稳定事件ID，例如：

```text
APP-START-001
QUOTA-TRANSPORT-002
CONFIG-MIGRATION-003
TRAY-RECOVERY-004
DISPLAY-RECOVERY-005
```

每个事件应包含：

- 时间；
- 严重等级；
- 组件；
- 事件ID；
- 脱敏消息；
- 相关时的异常类型。

### 12.3 日志生命周期

项目必须定义：

- 日志路径；
- 编码；
- 最大大小；
- 轮换数量；
- 保留期；
- 日志失败时行为。

正常成功轮询不应产生重复日志。

### 12.4 诊断摘要

面向用户的诊断摘要应包含：

- 应用版本；
- Windows版本；
- 显示器数量和DPI；
- 不含敏感内容的配置路径；
- app-server状态；
- 最后一次额度成功时间；
- 最后一次Activity刷新；
- 当前状态；
- 日志位置。

---

## 13. 编码规范

### 13.1 Python基线

项目必须记录最低和已测试Python版本。

代码应：

- 为公开API使用类型标注；
- 为领域值使用dataclass/enum；
- 使用 `pathlib.Path`；
- 避免可变默认参数；
- 避免隐藏全局状态；
- 保持函数职责集中；
- 显式指定编码；
- 使用monotonic time计算持续时间；
- 使用带时区时间记录时间戳。

### 13.2 命名

- 模块：`snake_case`；
- 函数和变量：`snake_case`；
- 类：`PascalCase`；
- 常量：`UPPER_SNAKE_CASE`；
- 私有实现：前导下划线；
- 测试名称尽量使用：`test_<behavior>_<condition>_<expected>`。

### 13.3 函数质量

出现以下情况时应拆分函数：

- 超过一个职责；
- 混合平台调用和策略；
- 同时进行校验、持久化和渲染；
- 控制流嵌套过深；
- 测试时必须构造无关基础设施。

### 13.4 注释与docstring

注释应解释原因、约束或平台行为，而不是重复代码。

公开API必须有docstring说明行为和错误契约。

必须删除死代码、不可到达代码、注释掉的旧实现和过期兼容路径。

---

## 14. 依赖与供应链策略

### 14.1 引入依赖条件

新增运行时依赖必须记录：

- 用途；
- 维护活跃度；
- 许可证兼容性；
- 安全历史；
- 包体积影响；
- 启动影响；
- 干净机器安装测试；
- 项目废弃时的移除计划。

### 14.2 固定策略

项目必须明确依赖采用：

- 最低兼容版本；
- 已测试锁定版本；
- 可重复构建constraints。

Release构建应使用经过审查的lock或constraints文件。

### 14.3 更新策略

依赖更新应使用独立提交或PR，并必须运行：

- 单元测试；
- 干净导入测试；
- 打包smoke test；
- 可用时的安全扫描；
- UI/运行时依赖的Windows启动smoke test。

---

## 15. 测试标准

### 15.1 测试分层

测试策略必须区分：

| 层级 | 目的 | 示例 |
|---|---|---|
| Unit | 纯确定性行为 | 格式化、校验、状态转换 |
| Contract | 适配器/provider假设 | app-server payload和错误矩阵 |
| Integration | 多组件协作 | 设置事务和持久化 |
| UI contract | Tk适配行为 | 菜单关闭、Apply/Close语义 |
| Platform | Windows特定API | mutex、work area、DPI |
| Physical | 真实桌面证据 | mixed DPI、任务栏边缘、托盘 |
| Packaging | 干净机器执行 | EXE/安装器启动 |
| Soak | 长时间稳定性 | timer、线程、资源增长 |

### 15.2 变更对应测试

| 变更 | 最低测试要求 |
|---|---|
| 纯领域API | Unit测试 |
| Parser/transport | Unit + contract |
| 设置schema | Unit + migration + integration |
| 线程/调度 | Unit + race/lifecycle |
| UI行为 | API测试 + Windows人工证据 |
| 显示/DPI | 几何测试 + 实体矩阵 |
| 打包 | 干净机器smoke |
| 安全边界 | 负向/脱敏测试 |
| 性能变化 | benchmark或有界fixture |

### 15.3 确定性

测试应注入：

- 时钟；
- 文件系统根目录；
- payload；
- 显示器布局；
- scheduler generation；
- 进程factory。

除明确标记为manual外，测试不得依赖维护者的真实Codex账户。

### 15.4 测试证据

模拟通过不得记录为实体通过。

实体证据应记录：

- 日期；
- Windows build；
- 显示器拓扑；
- DPI；
- 任务栏位置；
- 应用版本/commit；
- 结果；
- 安全情况下的截图或probe输出。

### 15.5 覆盖率策略

覆盖率是信号，不是发布标准。即使总体行覆盖率较高，关键状态转换和失败路径仍必须有明确测试。

---

## 16. Windows与UI兼容

### 16.1 支持平台策略

发布文档必须列出：

- 支持的Windows版本；
- 已测试Windows build；
- 支持架构；
- 最低显示分辨率；
- 支持的Python/runtime模式；
- 已知未签名程序行为。

### 16.2 显示要求

应用必须考虑：

- 单屏和多屏；
- 负虚拟坐标；
- 显示器间隙；
- mixed DPI；
- 每个边缘的任务栏；
- 自动隐藏任务栏；
- 显示器断开/重连；
- work area而不是完整monitor bounds；
- popup大于可用work area。

### 16.3 无障碍

UI应支持：

- 可读的最小字体；
- 高对比度；
- 除颜色外的状态文字；
- Escape键关闭；
- 减少动画；
- 关键操作不能只依赖hover；
- 明确焦点行为。

### 16.4 本地化

用户可见文本应逐步迁移到本地化目录，而不是长期硬编码在UI中。

格式规则必须定义：

- 本地时区；
- 需要时使用无前导零的 `M/D`；
- 24小时或12小时时间政策；
- 单复数；
- fallback文本；
- 最大显示长度。

---

## 17. 性能与资源预算

项目必须定义可衡量预算。初始目标：

| 指标 | 目标 |
|---|---|
| Tk callback阻塞工作 | 不执行文件系统、子进程或网络阻塞 |
| 并发Quota worker | 最大1个 |
| 并发Activity worker | 最大1个 |
| UI队列轮询 | 100–500 ms |
| 正常Quota刷新 | 用户设置1–10秒 |
| Activity刷新 | 约1秒 |
| Popup几何计算 | 支持硬件上低于5 ms |
| 配置加载 | 正常文件低于50 ms |
| 空闲CPU | 发布前记录和测量 |
| 空闲内存 | 发布前记录和测量 |
| 日志增长 | 受轮换限制 |
| Soak test | 稳定版前至少8小时 |

任何性能结论必须记录环境和方法。

---

## 18. 版本、发布与回滚

### 18.1 版本

采用Semantic Versioning：

- patch：兼容修复；
- minor：兼容功能；
- major：破坏契约。

即使在1.0前，破坏性变化也必须明确记录并设计迁移。

所有版本来源必须一致：

- 应用常量；
- plugin manifest；
- Changelog；
- 包元数据；
- artifact名称；
- Release tag；
- 诊断输出。

### 18.2 发布门禁

以下条件未完成时不得发布：

- 自动检查通过；
- 必需实体矩阵通过或有已批准限制；
- 所有版本来源一致；
- 中英文规范同步；
- Changelog定稿；
- 敏感文件扫描通过；
- 干净机器或干净环境启动通过；
- 存在回滚说明；
- 已知问题已记录。

### 18.3 发布通道

建议通道：

- development build；
- preview/beta；
- stable。

Preview必须明确标记，不得被描述为release-ready。

### 18.4 回滚

每个Release应定义：

- 上一个稳定版本；
- 配置兼容性；
- 卸载/重装路径；
- 降级限制；
- 备份/恢复路径；
- 紧急撤回流程。

---

## 19. Git、提交与审查流程

### 19.1 分支

建议：

- 保护 `main`；
- 短期feature/fix分支；
- 重大变化使用PR；
- 不直接进行未经审查的发布修改。

### 19.2 提交质量

每个提交应：

- 只包含一个连贯变化；
- 可编译并通过相关测试；
- 避免无关格式化；
- 需要时同步文档；
- 使用祈使语气标题；
- 不包含生成secret或本地路径。

### 19.3 PR要求

重大PR必须包含：

- 问题描述；
- 范围和非范围；
- 设计摘要；
- API/文件变化；
- 测试；
- 人工证据；
- 安全/隐私影响；
- 性能影响；
- 兼容性影响；
- 文档变化；
- 回滚计划。

### 19.4 审查清单

审查者必须检查：

- 需求到代码可追踪性；
- API边界；
- 线程归属；
- 错误处理；
- 设置迁移；
- 敏感数据；
- 测试和负向场景；
- 死代码；
- 文档真实性；
- 发布影响。

---

## 20. 变更分类与治理

### 20.1 变更等级

| 等级 | 示例 | 必需治理 |
|---|---|---|
| C0 文档 | 不改变行为的文字 | parity检查 |
| C1 内部重构 | 不改变契约 | 测试，不宣称新行为 |
| C2 兼容行为 | 新设置或状态 | spec、测试、changelog |
| C3 性能/并发 | scheduler、缓存、线程 | benchmark、生命周期测试 |
| C4 兼容/平台 | DPI、Windows版本、打包 | 矩阵证据 |
| C5 安全边界 | provider、凭据、日志 | ADR、威胁评审 |
| C6 破坏性变化 | schema/API删除 | 迁移、版本决定 |

### 20.2 可追踪性

重大工作应具有Issue或路线ID。

推荐链路：

```text
需求 → Issue/ADR → API契约 → 测试 → Changelog → 兼容性证据
```

### 20.3 风险登记

项目应维护简要风险表：

- 风险；
- 可能性；
- 影响；
- 缓解；
- 负责人；
- 检查日期；
- 当前状态。

---

## 21. 弃用与删除

公开功能、设置、文件格式或API不得静默删除。

弃用必须包含：

1. Changelog公告；
2. 替代方案；
3. 兼容期；
4. 适当情况下的警告；
5. 删除版本；
6. 迁移测试。

不再被支持路径使用的内部旧代码应及时删除。

---

## 22. Definition of Ready

功能满足以下条件后才可进入开发：

- 用户结果明确；
- 范围和非范围已写明；
- 依赖已识别；
- 已建议API归属；
- 已考虑安全/隐私；
- 已考虑兼容性；
- 验收条件可测试；
- 已识别需要更新的中英文文档；
- 有回滚或关闭策略。

---

## 23. Definition of Done

功能只有在以下条件全部满足后才算完成：

1. 行为符合已批准验收条件；
2. API边界已记录；
3. 公开类型和错误已记录；
4. Unit及必要Integration测试通过；
5. 负向和失败路径已测试；
6. Tk线程保持非阻塞；
7. Scheduler和shutdown安全；
8. 相关设置迁移/持久化已测试；
9. 不包含敏感数据；
10. 相关性能影响已测量；
11. 相关兼容矩阵已更新；
12. 英文规范已更新；
13. 中文翻译同提交更新；
14. Changelog已更新；
15. 死代码已删除；
16. 发布检查通过；
17. 需要时存在实体证据；
18. 版本描述真实。

---

## 24. 例外流程

例外请求必须包含：

```text
Rule:
Reason:
Scope:
Risk:
Mitigation:
Owner:
Expiration:
Tracking issue:
```

到期例外如果未续期，将自动变为违规。

安全和敏感数据规则不应获得永久例外。

---

## 25. 维护周期

### 每次重大变更

- 运行相关测试；
- 运行文档一致性检查；
- 更新Changelog/规范；
- 检查staged文件；
- 确认无敏感数据；
- 创建聚焦提交。

### 每个次版本

- 检查本规范；
- 检查Windows支持矩阵；
- 检查依赖；
- 检查未解决P0/P1；
- 运行soak test；
- 验证干净安装；
- 检查日志是否包含敏感数据；
- 统一所有版本来源。

### 每90天

- 归档过期路线项；
- 检查ADR；
- 检查风险登记；
- 检查依赖健康；
- 测试恢复/回滚；
- 验证双语配对；
- 删除死亡兼容路径。

---

# 附录A — API契约模板

```markdown
## API Name

**Module:**  
**Owner layer:**  
**Purpose:**  
**Public symbols:**  
**Inputs:**  
**Outputs:**  
**Side effects:**  
**Thread model:**  
**Errors:**  
**Security boundary:**  
**Compatibility promise:**  
**Tests:**  
**Observability:**  
```

---

# 附录B — ADR模板

```markdown
# ADR-NNNN: Title

- Status: Proposed / Accepted / Superseded
- Date:
- Decision owners:

## Context

## Decision

## Alternatives considered

## Consequences

## Security and privacy impact

## Compatibility and migration

## Test and rollout plan

## Rollback plan
```

---

# 附录C — 功能规范模板

```markdown
# Feature: Name

## User outcome

## Scope

## Non-scope

## Current behavior

## Required behavior

## State transitions

## API changes

## Persistence changes

## Error behavior

## Security/privacy impact

## Compatibility impact

## Performance budget

## Acceptance tests

## Manual Windows evidence

## Rollback/disable strategy

## Documentation changes
```

---

# 附录D — 发布清单

```text
[ ] Version sources match
[ ] Automated release checks pass
[ ] Unit/contract/integration tests pass
[ ] Required physical matrix rows pass
[ ] Clean-machine startup passes
[ ] Soak test passes
[ ] English/Chinese documents match
[ ] Changelog finalized
[ ] No sensitive files or logs included
[ ] Known issues documented
[ ] Upgrade/downgrade behavior documented
[ ] Artifacts named and checksummed
[ ] Rollback path verified
```

---

# 附录E — 严重等级

| 等级 | 含义 | 预期响应 |
|---|---|---|
| P0 | 安全泄露、破坏性损坏或阻止发布的崩溃 | 阻止发布，立即修复 |
| P1 | 核心流程失败、错误状态、恢复路径丢失 | 稳定版前修复 |
| P2 | 可恢复缺陷或重大维护风险 | 当前或下一次版本安排 |
| P3 | 体验、文档或低风险边界 | 有理由地进入Backlog |

---

# 附录F — 采用计划

逐步采用本规范：

### Phase 1 — 治理基线

1. 添加英文文件和中文副本。
2. 将其加入文档一致性检查。
3. 声明本文件为最高层级规范。
4. 修正现有文件中的过期描述。

### Phase 2 — 拆分专项规范

创建配对文件：

- `ARCHITECTURE.md`；
- `SECURITY.md`；
- `TESTING.md`；
- `RELEASE.md`；
- `CONTRIBUTING.md`。

在不改变运行时行为的前提下，将详细内容从 `docs/architecture/API_SPEC.md` 和 `docs/product/ROADMAP.md` 移出。

### Phase 3 — 自动化门禁

增加以下检查：

- 文档版本和配对；
- API名称；
- Changelog版本标题；
- 配置schema版本；
- 版本来源一致；
- 敏感文件模式；
- 测试和打包smoke结果。

### Phase 4 — PR强制执行

保护 `main`，要求CI，并使用基于本规范的PR模板。
