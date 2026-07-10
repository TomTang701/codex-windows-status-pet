---
document_id: DEVELOPMENT-PLAN
status: active
document_version: 1.1.0
canonical_language: en
translation_pair: docs/product/ROADMAP.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 30
---
# Codex Windows 状态宠物路线图

本路线图只保留未来工作。已完成功能写入 `CHANGELOG.zh-CN.md`；当前证据写入兼容矩阵。测试数量由质量套件生成，不在这里手工维护。

## 当前

- 完成 Reset Credit 在展开悬浮窗中的实体可见性记录。
- 完成非法粘贴输入证据，并保持未来配置schema写保护。
- 保持日常Quality全绿；在实体行未验证前，严格Release Candidate继续阻止发布。

## 下一步

- 完成Windows 10、单显示器、混合DPI及顶部/左侧/右侧任务栏实体记录。
- 在无活动Codex任务时验证空闲收缩和悬停展开。
- 在独立干净Windows环境验证安装和启动。
- 执行并记录覆盖刷新、托盘、隐藏/显示、设置和关闭的8小时soak。

## 后续

- 在可复现制品和回滚稳定后评估签名打包。
- 只在经过测试的API边界后考虑其他本地展示模式。
- 审查键盘导航、对比度和缩放等无障碍改进。

## 阻塞

- v0.3.0 Release Candidate批准被阻塞，直到所有阻塞兼容行成为 `Physical pass`，或由维护者明确批准为 `Approved limitation`。
- 硬件专项验证依赖对应Windows版本、DPI拓扑和任务栏配置。

## 不在范围

- 读取 `auth.json`、访问令牌、账户ID、提示词/回答、项目内容或原始会话正文。
- 第三方额度provider、遥测、托管后端，或修改Codex核心和内置宠物。
- 从模拟、mock、无可复现步骤的截图或推断证据宣称实体兼容。
