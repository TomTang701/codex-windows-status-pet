# 安装

English: [English version](INSTALLATION.md)

## 当前 v0.8.0 部署边界

已发布 ZIP 是当前普通用户路径：如需手动验证，请核对其 SHA-256；解压完整压缩包后，
运行 `CodexStatusPet\CodexStatusPet.exe`。该 EXE 是应用入口而不是安装器，
请勿将它从 onedir 运行时中单独复制出来。

本仓库为 private，因此只有 Tom 和已授权协作者可以通过认证 GitHub 路径获取
v0.8.0 Release。匿名公开 PowerShell 下载命令并不真实，项目不会提供。

以下带 ArtifactPath 的调用仅保留给源码验证和发布工程，不是普通用户的快速开始：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 `
  -ArtifactPath .\CodexStatusPet-v0.8.0-win11-x64.zip `
  -Sha256 <发布的-sha256>
```

安装器会在解压前校验 ZIP、验证发布清单，并将应用按用户安装到
`%LOCALAPPDATA%\Programs\CodexStatusPet`。它会创建一个名为
**Codex Windows Status Pet** 的开始菜单快捷方式。此产品路径不需要管理员权限、
Python、pip、Git、仓库检出、自动登录启动或后台更新器。

已安装 EXE 仍通过本地 Codex CLI 获取实时额度数据。若 Codex 不可用，应用会显示
既有的不可用诊断；不会使用第三方额度服务。

若安装器提示已有实例正在运行，请在应用托盘菜单中选择 **Exit**，然后重新运行安装器。
这样可以避免旧的源码或已安装进程被误认为新版本已经成功启动。

## 当前源码验证的升级和卸载边界

对更高版本且已验证的 ZIP 再次运行同一源码验证安装命令，即可执行按用户的就地升级。产品设置
文件仍位于 `%USERPROFILE%\.codex\codex-windows-status-pet.json`，升级时会保留。

要卸载已安装版本，请运行应用目录内随发布包复制的 `uninstall.ps1`。正常卸载会删除 EXE
和开始菜单快捷方式，但会保留设置。若要明确删除仅此产品设置文件：

```powershell
.\uninstall.ps1 -PurgeSettings
```

它绝不会删除整个 `.codex` 目录、Codex 会话、凭据或其他配置。

## 安全性和迁移边界

v0.8.0 二进制文件尚未签名。Windows SmartScreen 或组织策略可能显示警告；使用前请核验
发布的 SHA-256。`start_codex_status_pet.cmd` 源码启动器仅用于开发、调试、源码验证和
发布工程，不是普通用户入口。v0.9.0 会新增认证 Release 获取部署路径，但不会建立第二套安装器实现。
