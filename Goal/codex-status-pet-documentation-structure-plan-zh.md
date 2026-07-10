# Codex Windows Status Pet 文档结构优化方案

> **方案版本：** 1.0  
> **适用仓库：** `TomTang701/codex-windows-status-pet`  
> **制定日期：** 2026-07-10  
> **目标：** 在保留双语维护、GitHub可读性和现有开发门禁的前提下，建立适合长期开发的分层文档体系。

---

# 1. 当前文档结构的主要问题

当前仓库已经拥有较多工程文档，包括：

- `README.md` / `README.zh-CN.md`
- `API_SPEC.md` / `API_SPEC.zh-CN.md`
- `FILE_SPEC.md` / `FILE_SPEC.zh-CN.md`
- `CHANGELOG.md` / `CHANGELOG.zh-CN.md`
- `PRODUCT_REVIEW.md` / `PRODUCT_REVIEW.zh-CN.md`
- `DEVELOPMENT_PLAN.md` / `DEVELOPMENT_PLAN.zh-CN.md`
- `COMPATIBILITY_MATRIX.md` / `COMPATIBILITY_MATRIX.zh-CN.md`
- `TEST_ERROR_REPORT.md`

随着项目继续增长，当前结构会出现以下问题。

## 1.1 根目录文档过多

所有文档位于根目录时：

- 用户无法快速判断哪些是安装文档、开发规范或历史报告；
- README中的链接越来越长；
- 每增加一个中英文配对，根目录增加两个文件；
- 规范、路线图、测试证据在视觉上处于同一等级；
- 历史审计报告容易被误认为当前有效规范。

## 1.2 单个文件混合多种职责

### `FILE_SPEC.md`

目前同时包含：

- 仓库文件布局；
- 配置JSON示例；
- 配置位置；
- 日志位置；
- 运行时不变量。

这些内容应分别属于：

- 仓库结构；
- 配置schema；
- 诊断；
- 架构或API契约。

### `API_SPEC.md`

目前同时包含：

- API目录；
- 不变量；
- 测试命令；
- Windows实体证据要求；
- 变更分类；
- Git门禁。

长期应拆分为：

- API契约；
- 测试规范；
- 贡献和Git流程；
- 兼容性证据规则。

### `DEVELOPMENT_PLAN.md`

目前同时包含：

- 当前进度；
- 未来路线；
- API目录；
- 兼容矩阵要求；
- 文档规则；
- Git流程。

路线图不应成为API和Git规则的第二份事实来源。

## 1.3 规范文件与证据文件没有分开

例如：

- `API_SPEC`是规范；
- `COMPATIBILITY_MATRIX`是持续更新的证据；
- `TEST_ERROR_REPORT`是某个日期的审计历史；
- `PRODUCT_REVIEW`同时包含产品定位和风险观察。

如果不分类，维护者容易修改错误文件，或把历史问题继续当作当前问题。

## 1.4 双语检查依赖硬编码文件名

当前 `check_doc_parity.py` 在代码中直接维护：

```python
PAIRS = (
    "README",
    "API_SPEC",
    "FILE_SPEC",
    "CHANGELOG",
    "PRODUCT_REVIEW",
    "DEVELOPMENT_PLAN",
    "COMPATIBILITY_MATRIX",
)
```

这意味着：

- 新增文件必须修改脚本；
- 移动文件必须修改脚本；
- 无法为不同文档设置不同维护政策；
- 无法区分规范文档、证据文档和历史文档；
- 无法检测未登记的孤立文档。

## 1.5 缺少统一导航和文档生命周期

当前没有一个中心文件明确说明：

- 每个文档的读者是谁；
- 哪个文件是唯一事实来源；
- 哪些文档是Active、Draft、Deprecated或Archived；
- 谁负责维护；
- 多久检查一次；
- 中文是否必须配对；
- 某份历史报告是否还有效。

---

# 2. 优化目标

目标结构应满足：

1. 根目录保持简洁；
2. 用户、开发者和维护者能快速找到所需内容；
3. 规范、设计、证据和历史文件分层；
4. 每项规则只有一个事实来源；
5. 中英文文件继续就近成对；
6. 文档移动后仍可自动检查；
7. 支持未来增加ADR、测试记录和Release记录；
8. 不依赖立即引入MkDocs等新工具；
9. 将来可以平滑生成文档网站；
10. 适合一个人维护，也适合未来多人协作。

---

# 3. 推荐总体结构

```text
codex-windows-status-pet/
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
├── CHANGELOG.zh-CN.md
├── CONTRIBUTING.md
├── CONTRIBUTING.zh-CN.md
├── SECURITY.md
├── SECURITY.zh-CN.md
├── LICENSE
│
├── docs/
│   ├── README.md
│   ├── README.zh-CN.md
│   ├── document_manifest.json
│   │
│   ├── governance/
│   │   ├── ENGINEERING_STANDARD.md
│   │   ├── ENGINEERING_STANDARD.zh-CN.md
│   │   ├── RELEASE.md
│   │   ├── RELEASE.zh-CN.md
│   │   ├── SUPPORT_POLICY.md
│   │   └── SUPPORT_POLICY.zh-CN.md
│   │
│   ├── architecture/
│   │   ├── ARCHITECTURE.md
│   │   ├── ARCHITECTURE.zh-CN.md
│   │   ├── API_SPEC.md
│   │   ├── API_SPEC.zh-CN.md
│   │   ├── CONFIGURATION.md
│   │   ├── CONFIGURATION.zh-CN.md
│   │   ├── REPOSITORY_STRUCTURE.md
│   │   ├── REPOSITORY_STRUCTURE.zh-CN.md
│   │   └── adr/
│   │       ├── README.md
│   │       ├── 0001-local-app-server-provider.md
│   │       ├── 0002-tkinter-ui-framework.md
│   │       └── 0003-local-only-security-boundary.md
│   │
│   ├── product/
│   │   ├── PRODUCT_OVERVIEW.md
│   │   ├── PRODUCT_OVERVIEW.zh-CN.md
│   │   ├── ROADMAP.md
│   │   ├── ROADMAP.zh-CN.md
│   │   ├── UI_PRINCIPLES.md
│   │   └── UI_PRINCIPLES.zh-CN.md
│   │
│   ├── quality/
│   │   ├── TESTING.md
│   │   ├── TESTING.zh-CN.md
│   │   ├── COMPATIBILITY_MATRIX.md
│   │   ├── COMPATIBILITY_MATRIX.zh-CN.md
│   │   ├── RISK_REGISTER.md
│   │   ├── RISK_REGISTER.zh-CN.md
│   │   ├── benchmarks/
│   │   │   └── README.md
│   │   └── test-records/
│   │       ├── README.md
│   │       ├── 2026-07-10-win11-dual-monitor.md
│   │       └── 2026-07-10-display-probe.json
│   │
│   ├── operations/
│   │   ├── INSTALLATION.md
│   │   ├── INSTALLATION.zh-CN.md
│   │   ├── TROUBLESHOOTING.md
│   │   ├── TROUBLESHOOTING.zh-CN.md
│   │   ├── DIAGNOSTICS.md
│   │   ├── DIAGNOSTICS.zh-CN.md
│   │   ├── PACKAGING.md
│   │   └── PACKAGING.zh-CN.md
│   │
│   └── archive/
│       ├── README.md
│       ├── audits/
│       │   └── 2026-07-09-test-error-report.md
│       ├── plans/
│       └── retired-specs/
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   └── config.yml
│   ├── pull_request_template.md
│   ├── CODEOWNERS
│   └── workflows/
│       └── ci.yml
│
├── scripts/
├── tests/
├── skills/
└── .codex-plugin/
```

---

# 4. 为什么采用这种结构

## 4.1 根目录只保留高频入口

根目录保留：

- README；
- Changelog；
- License；
- Security；
- Contributing。

原因：

- GitHub能够直接识别Security和Contributing；
- 新用户无需进入docs即可开始；
- Release历史保持明显；
- 根目录不会被内部规范淹没。

不建议把所有工程规范继续放在根目录。

## 4.2 中英文文件就近配对

推荐：

```text
docs/architecture/API_SPEC.md
docs/architecture/API_SPEC.zh-CN.md
```

而不是：

```text
docs/en/API_SPEC.md
docs/zh-CN/API_SPEC.md
```

原因：

- 一眼可以看到中文是否存在；
- 移动或删除时不容易漏掉另一语言；
- Git diff和PR审查更直观；
- 与当前 `.zh-CN.md` 习惯兼容；
- 自动配对逻辑简单；
- 项目目前文档数量还不需要按语言完全分目录。

只有未来支持三种以上语言，才考虑 `docs/<locale>/`。

## 4.3 规范与证据分离

### 规范

说明“必须怎么做”：

```text
ENGINEERING_STANDARD
ARCHITECTURE
API_SPEC
TESTING
SECURITY
RELEASE
CONTRIBUTING
```

### 描述

说明“当前产品是什么”：

```text
PRODUCT_OVERVIEW
REPOSITORY_STRUCTURE
CONFIGURATION
INSTALLATION
DIAGNOSTICS
```

### 证据

说明“已经测试过什么”：

```text
COMPATIBILITY_MATRIX
test-records/
benchmarks/
```

### 历史

说明“过去发生过什么”：

```text
CHANGELOG
archive/audits/
archive/plans/
retired-specs/
```

证据不能定义规范，历史报告不能覆盖当前事实。

---

# 5. 现有文件迁移映射

| 当前文件 | 建议目标 | 处理方式 |
|---|---|---|
| `README.md` | 根目录保留 | 精简为用户入口和文档导航 |
| `README.zh-CN.md` | 根目录保留 | 与英文同步 |
| `CHANGELOG.md` | 根目录保留 | 继续作为英文发布历史 |
| `CHANGELOG.zh-CN.md` | 根目录保留 | 同步翻译 |
| `API_SPEC.md` | `docs/architecture/API_SPEC.md` | 只保留API契约和不变量 |
| `API_SPEC.zh-CN.md` | 同目录中文副本 | 同步移动 |
| `FILE_SPEC.md` | 拆成两个文件 | 不建议继续保留混合职责 |
| `FILE_SPEC.zh-CN.md` | 同步拆分 | 与英文结构相同 |
| `PRODUCT_REVIEW.md` | `docs/product/PRODUCT_OVERVIEW.md` | 保留定位；风险移到Risk Register |
| `PRODUCT_REVIEW.zh-CN.md` | 中文副本 | 同步重命名 |
| `DEVELOPMENT_PLAN.md` | `docs/product/ROADMAP.md` | 只保留当前与未来路线 |
| `DEVELOPMENT_PLAN.zh-CN.md` | 中文副本 | 同步重命名 |
| `COMPATIBILITY_MATRIX.md` | `docs/quality/COMPATIBILITY_MATRIX.md` | 继续作为Living Evidence |
| `COMPATIBILITY_MATRIX.zh-CN.md` | 中文副本 | 同步移动 |
| `TEST_ERROR_REPORT.md` | `docs/archive/audits/2026-07-09-test-error-report.md` | 标记为历史审计 |
| 新 `ENGINEERING_STANDARD.md` | `docs/governance/` | 作为最高工程规范 |
| 新中文总规范 | 同目录中文副本 | 加入manifest和检查 |

---

# 6. `FILE_SPEC.md`的具体拆分

当前 `FILE_SPEC.md`不建议直接移动后继续使用，而应拆成：

## 6.1 `REPOSITORY_STRUCTURE.md`

内容：

- 根目录结构；
- `scripts/api`职责；
- `scripts/ui`职责；
- `tests`结构；
- `docs`结构；
- `.github`结构；
- 文件命名规则；
- 新增文件放置规则；
- 生成文件和忽略文件。

不应包含具体配置值。

## 6.2 `CONFIGURATION.md`

内容：

- 配置文件路径；
- schema version；
- 每个字段的类型；
- 默认值；
- 范围；
- 用户是否可编辑；
- 保存语义；
- Apply/Save/Close；
- migration；
- recovery；
- 配置示例。

## 6.3 移出FILE_SPEC的内容

- 日志位置和日志策略 → `DIAGNOSTICS.md`
- 单实例、Tk线程、不变量 → `ARCHITECTURE.md`或`API_SPEC.md`
- 发布提交规则 → `CONTRIBUTING.md`和`RELEASE.md`

完成拆分后可删除 `FILE_SPEC.md`，避免同一内容存在两份。

---

# 7. `API_SPEC.md`的具体精简

`API_SPEC.md`应只负责：

- API名称；
- 模块路径；
- 所属层；
- 公开符号；
- 输入；
- 输出；
- 副作用；
- 错误；
- 线程模型；
- 安全边界；
- 不变量；
- 测试边界；
- 兼容承诺。

以下内容应移出：

| 当前内容 | 新位置 |
|---|---|
| 测试命令 | `docs/quality/TESTING.md` |
| Windows实体证据要求 | `TESTING.md`和`COMPATIBILITY_MATRIX.md` |
| Git change gate | 根目录`CONTRIBUTING.md` |
| Release gate | `docs/governance/RELEASE.md` |
| 文档双语规则 | `ENGINEERING_STANDARD.md` |
| 路线优先级 | `ROADMAP.md` |

`API_SPEC`不能成为所有规则的汇总文件。

---

# 8. `DEVELOPMENT_PLAN.md`的具体精简

建议改名：

```text
DEVELOPMENT_PLAN.md → ROADMAP.md
```

ROADMAP只保留：

- 当前版本状态；
- 正在进行；
- 下一版本；
- 后续版本；
- 明确排除；
- 每阶段目标；
- 完成标准链接。

从ROADMAP移除：

- API目录；
- 测试命令；
- Git流程；
- 双语政策；
- 全量兼容矩阵；
- 已完成的详细历史。

已完成内容进入：

- `CHANGELOG`；
- `COMPATIBILITY_MATRIX`；
- 对应API规范；
- 必要时进入archive。

这样路线图不会不断膨胀。

---

# 9. `PRODUCT_REVIEW.md`的处理

`PRODUCT_REVIEW`这个名称容易让文件同时承担：

- 产品定位；
- 当前风险；
- 竞品比较；
- 路线建议；
- 一次性审查。

推荐拆分：

## `PRODUCT_OVERVIEW.md`

长期维护：

- 用户是谁；
- 核心场景；
- 核心价值；
- 非目标；
- 产品契约；
- 关键差异化。

## `RISK_REGISTER.md`

持续维护：

| ID | 风险 | 可能性 | 影响 | 缓解 | 负责人 | 状态 |
|---|---|---|---|---|---|---|

## 一次性产品比较

放入：

```text
docs/archive/audits/
```

或保留为外部下载报告，不作为运行规范。

---

# 10. 文档索引设计

## 10.1 根README

只包含：

1. 项目简介；
2. 截图；
3. 功能；
4. 快速启动；
5. 安全边界；
6. 文档入口；
7. License。

文档入口示例：

```markdown
## Documentation

- [Installation](docs/operations/INSTALLATION.md)
- [Troubleshooting](docs/operations/TROUBLESHOOTING.md)
- [Development documentation](docs/README.md)
- [中文文档](README.zh-CN.md)
```

## 10.2 `docs/README.md`

作为开发文档首页：

```text
New user
Maintainer
Contributor
Architecture
Testing
Release
Evidence
Historical documents
```

建议表格：

| 读者 | 首先阅读 |
|---|---|
| 普通用户 | Installation、Troubleshooting |
| 新开发者 | Contributing、Architecture、Testing |
| 维护者 | Engineering Standard、Release、Risk Register |
| UI开发 | UI Principles、Architecture |
| API开发 | API Spec、Testing |
| 发布负责人 | Release、Compatibility Matrix |

`docs/README.zh-CN.md`保持对应翻译。

---

# 11. 文档Manifest设计

不再在Python脚本中硬编码文件配对。

新建：

```text
docs/document_manifest.json
```

示例：

```json
{
  "schema_version": 1,
  "documents": [
    {
      "id": "ENG-STD",
      "class": "normative",
      "status": "active",
      "canonical": "docs/governance/ENGINEERING_STANDARD.md",
      "translations": {
        "zh-CN": "docs/governance/ENGINEERING_STANDARD.zh-CN.md"
      },
      "owner": "maintainer",
      "review_cycle_days": 90
    },
    {
      "id": "COMPAT-MATRIX",
      "class": "evidence",
      "status": "active",
      "canonical": "docs/quality/COMPATIBILITY_MATRIX.md",
      "translations": {
        "zh-CN": "docs/quality/COMPATIBILITY_MATRIX.zh-CN.md"
      },
      "owner": "maintainer",
      "review_cycle_days": 30
    }
  ]
}
```

Manifest应支持：

```text
id
class
status
canonical
translations
owner
review_cycle_days
required_for_release
```

文档状态：

```text
draft
active
deprecated
archived
generated
```

---

# 12. 文档头部元数据

每份维护中的Markdown建议使用YAML front matter：

```yaml
---
document_id: API-SPEC
status: active
document_version: 1.2.0
canonical_language: en
translation_pair: API_SPEC.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
```

中文：

```yaml
---
document_id: API-SPEC
status: active
document_version: 1.2.0
canonical_language: en
translation_source: API_SPEC.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
```

优点：

- checker可以自动读取；
- 不依赖文件名推测；
- 可以检测版本不一致；
- 可以产生文档索引；
- 可以提醒过期规范；
- 可以区分active和archive。

---

# 13. 双语维护政策

## 13.1 必须配对

以下Active文档必须中英文成对：

- README；
- Engineering Standard；
- Architecture；
- API Spec；
- Configuration；
- Repository Structure；
- Product Overview；
- Roadmap；
- Testing；
- Compatibility Matrix；
- Installation；
- Troubleshooting；
- Diagnostics；
- Release；
- Security；
- Contributing。

## 13.2 可以不翻译

以下内容可以只使用英文或机器格式：

- 原始probe JSON；
- benchmark CSV；
- 自动生成报告；
- GitHub Actions日志；
- 截图；
- 临时调试记录；
- ADR（首版可英文单语）；
- 已归档的一次性原始证据。

规则是：

> 不要求每个英文证据文件都必须存在中文版本；但只要存在中文副本，就必须与英文同步且不得增加独立要求。

## 13.3 防止翻译变成第二套规范

中文文件不得：

- 添加英文没有的功能；
- 修改数值范围；
- 修改API名称；
- 修改测试ID；
- 修改版本；
- 修改发布门禁；
- 修改状态含义。

---

# 14. 改进 `check_doc_parity.py`

新的checker应从manifest读取文件，而不是硬编码。

建议检查：

1. Manifest JSON合法；
2. document ID唯一；
3. canonical文件存在；
4. required translation存在；
5. 文档metadata ID一致；
6. document version一致；
7. heading层级结构一致；
8. code fence数量和语言标签一致；
9. 表格数量和第一列key一致；
10. API名称集合一致；
11. test ID集合一致；
12. Changelog版本标题一致；
13. Markdown内部链接存在；
14. 没有未登记的Active规范文档；
15. archived文件不参与release parity；
16. last_reviewed过期时产生warning。

建议脚本拆成：

```text
scripts/docs/
├── load_manifest.py
├── check_doc_metadata.py
├── check_doc_parity.py
├── check_doc_links.py
└── build_doc_index.py
```

初期也可以继续使用一个脚本，但内部应按函数分层。

---

# 15. Archive规则

`docs/archive/`不是垃圾桶，应具有明确规则。

## 15.1 允许归档

- 已被新规范取代的文件；
- 一次性审计报告；
- 已完成且不再维护的计划；
- 旧版本架构设计；
- 已废弃provider方案；
- 历史竞品比较。

## 15.2 归档文件头部

```yaml
---
status: archived
archived_on: 2026-07-10
superseded_by: ../quality/TESTING.md
reason: Findings have been resolved and incorporated into active specifications.
---
```

## 15.3 禁止行为

- Active README链接到archive作为正式规则；
- 在archive中继续修改当前行为要求；
- 将尚未解决的问题归档以隐藏风险；
- 让archive参与正式release gate。

---

# 16. 测试证据结构

建议：

```text
docs/quality/test-records/
├── README.md
├── 2026-07-10-win11-dual-monitor.md
├── 2026-07-10-display-probe.json
├── 2026-07-15-mixed-dpi.md
└── 2026-07-20-windows10-clean-install.md
```

每份人工记录模板：

```markdown
# Test Record: Mixed DPI

- Date:
- Commit:
- App version:
- Windows version/build:
- Monitor topology:
- DPI:
- Taskbar:
- Tester:
- Result:
- Known limitations:

## Steps

## Expected

## Actual

## Evidence

## Follow-up
```

`COMPATIBILITY_MATRIX.md`只汇总结果并链接到详细记录，不承载所有细节。

---

# 17. ADR目录规则

```text
docs/architecture/adr/
```

文件：

```text
0001-local-app-server-provider.md
0002-tkinter-ui-framework.md
0003-local-only-security-boundary.md
```

ADR适用于：

- 为什么继续使用Tkinter；
- 为什么不读取auth.json；
- 为什么Activity和Quota分开；
- 为什么使用命名mutex；
- 为什么使用本地app-server；
- 将来为什么迁移PySide6；
- 为什么改变配置schema。

ADR一旦Accepted，不直接重写历史；新ADR通过Supersedes字段取代。

---

# 18. GitHub目录优化

建议增加：

```text
.github/
├── ISSUE_TEMPLATE/
├── pull_request_template.md
├── CODEOWNERS
└── workflows/
```

PR模板应链接：

- Engineering Standard；
- Testing；
- Security；
- Compatibility Matrix；
- Documentation manifest。

PR清单：

```text
[ ] API contract updated
[ ] Tests added
[ ] English/Chinese pair updated
[ ] Changelog updated
[ ] Compatibility evidence updated
[ ] Security impact reviewed
[ ] Rollback documented
```

---

# 19. 推荐迁移步骤

不要在一个提交中同时移动、拆分、改写和新增全部文档。

## Commit 1：建立文档框架

新增：

```text
docs/README.md
docs/README.zh-CN.md
docs/document_manifest.json
docs/governance/
docs/architecture/
docs/product/
docs/quality/
docs/operations/
docs/archive/
```

同时让checker能够读取路径，但暂不移动旧文件。

## Commit 2：纯移动文件

使用 `git mv`：

```text
API_SPEC → docs/architecture/
DEVELOPMENT_PLAN → docs/product/ROADMAP
COMPATIBILITY_MATRIX → docs/quality/
PRODUCT_REVIEW → docs/product/PRODUCT_OVERVIEW
TEST_ERROR_REPORT → docs/archive/audits/
```

本提交只移动和修复链接，不大幅改写正文。

## Commit 3：拆分FILE_SPEC

创建：

```text
REPOSITORY_STRUCTURE
CONFIGURATION
DIAGNOSTICS
```

把原内容逐段迁移，确认没有内容丢失后删除FILE_SPEC。

## Commit 4：精简API_SPEC和ROADMAP

- 测试命令移至TESTING；
- Git流程移至CONTRIBUTING；
- 发布规则移至RELEASE；
- 双语规则保留在ENGINEERING_STANDARD；
- Roadmap删除已完成细节。

## Commit 5：加入总规范

加入：

```text
docs/governance/ENGINEERING_STANDARD.md
docs/governance/ENGINEERING_STANDARD.zh-CN.md
```

声明文件优先级。

## Commit 6：补齐专项文档

按优先级新增：

1. `ARCHITECTURE`
2. `TESTING`
3. `SECURITY`
4. `RELEASE`
5. `CONTRIBUTING`
6. `INSTALLATION`
7. `TROUBLESHOOTING`
8. `DIAGNOSTICS`

## Commit 7：加强CI

加入：

- manifest校验；
- 双语版本校验；
- Markdown链接检查；
- 文档索引生成检查；
- Active文档孤儿检查；
- 版本来源一致性检查。

---

# 20. 不建议的方案

## 20.1 不建议所有文件继续留在根目录

项目只会越来越难导航。

## 20.2 不建议直接使用 `docs/en` 和 `docs/zh-CN`

目前只有两种语言，分开后会增加漏改概率。

## 20.3 不建议把所有规范写成一个超大文件

Engineering Standard负责稳定原则，专项细节必须拆出。

## 20.4 不建议每个API创建一个Markdown文件

当前项目规模下，单个 `API_SPEC` 配合清晰章节已经足够。只有某个子系统复杂到需要独立协议时再拆分。

## 20.5 不建议让Roadmap记录全部已完成历史

已完成历史属于Changelog和Release，不属于未来路线。

## 20.6 不建议让测试证据决定规范

Compatibility Matrix只能证明测试结果，不能自行定义产品行为。

---

# 21. 最终推荐的最小可行结构

如果暂时不想一次建立完整体系，至少先采用：

```text
/
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
├── CHANGELOG.zh-CN.md
├── CONTRIBUTING.md
├── CONTRIBUTING.zh-CN.md
├── SECURITY.md
├── SECURITY.zh-CN.md
├── LICENSE
└── docs/
    ├── README.md
    ├── README.zh-CN.md
    ├── document_manifest.json
    ├── governance/
    │   ├── ENGINEERING_STANDARD.md
    │   ├── ENGINEERING_STANDARD.zh-CN.md
    │   ├── RELEASE.md
    │   └── RELEASE.zh-CN.md
    ├── architecture/
    │   ├── ARCHITECTURE.md
    │   ├── ARCHITECTURE.zh-CN.md
    │   ├── API_SPEC.md
    │   ├── API_SPEC.zh-CN.md
    │   ├── CONFIGURATION.md
    │   └── CONFIGURATION.zh-CN.md
    ├── product/
    │   ├── PRODUCT_OVERVIEW.md
    │   ├── PRODUCT_OVERVIEW.zh-CN.md
    │   ├── ROADMAP.md
    │   └── ROADMAP.zh-CN.md
    ├── quality/
    │   ├── TESTING.md
    │   ├── TESTING.zh-CN.md
    │   ├── COMPATIBILITY_MATRIX.md
    │   └── COMPATIBILITY_MATRIX.zh-CN.md
    ├── operations/
    │   ├── INSTALLATION.md
    │   ├── INSTALLATION.zh-CN.md
    │   ├── TROUBLESHOOTING.md
    │   └── TROUBLESHOOTING.zh-CN.md
    └── archive/
        └── audits/
```

这已经可以解决当前大多数结构问题。

---

# 22. 最终结论

最适合当前项目的方案是：

> **根目录保留用户入口和GitHub标准文件；`docs/`按治理、架构、产品、质量、运维和历史分区；中英文配对文件放在同一目录；使用manifest管理配对和生命周期；将历史审计和实体证据与正式规范分离。**

最先应执行的三项工作：

1. 建立 `docs/README` 和 `document_manifest.json`；
2. 将 `API_SPEC`、`ROADMAP`、`COMPATIBILITY_MATRIX`等按类别移动；
3. 将混合职责的 `FILE_SPEC`拆成 `REPOSITORY_STRUCTURE`、`CONFIGURATION`和`DIAGNOSTICS`。

完成后，仓库的文档会从“多个根目录Markdown文件”升级为一套具有：

- 单一事实来源；
- 明确生命周期；
- 双语同步；
- 自动门禁；
- 历史可追踪；
- 适合长期扩展

的工程文档系统。
