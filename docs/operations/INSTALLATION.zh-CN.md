# 安装

English: [English version](INSTALLATION.md)

## 支持的 v0.8.0 产品安装路径

在 Windows 11 x64 上，使用版本化的
`CodexStatusPet-v…-win11-x64.zip` 发布包及其发布的 SHA-256 值安装：

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

## 升级和卸载

对更高版本且已验证的 ZIP 再次运行同一安装命令，即可执行按用户的就地升级。产品设置
文件仍位于 `%USERPROFILE%\.codex\codex-windows-status-pet.json`，升级时会保留。

要卸载已安装版本，请运行应用目录内随发布包复制的 `uninstall.ps1`。正常卸载会删除 EXE
和开始菜单快捷方式，但会保留设置。若要明确删除仅此产品设置文件：

```powershell
.\uninstall.ps1 -PurgeSettings
```

它绝不会删除整个 `.codex` 目录、Codex 会话、凭据或其他配置。

## 安全性和迁移边界

v0.8.0 二进制文件尚未签名。Windows SmartScreen 或组织策略可能显示警告；安装前请核验
发布的 SHA-256。旧的 `start_codex_status_pet.cmd` 源码启动器仅保留为开发回退路径，
不再是受支持的已安装产品路径。
