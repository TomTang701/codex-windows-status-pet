# 安装

推荐入口是 `start_codex_status_pet.cmd`。可用时它使用内置 `pythonw.exe`，不会创建命令提示符窗口，也不会写入启动文件夹。回退Python环境必须安装 `requirements.txt`。

已测试的回退版本为CI上的Python 3.11和本地Python 3.12.13。受支持路径为 Windows 11 x64。Windows 10 为延后、不声明支持、非阻塞；ARM64 和 32 位 Windows 也不声明支持。

本程序是外部伴侣，不修改Codex核心或内置宠物文件。停止程序请使用托盘Exit动作或文档规定的进程所有者；不得按名称杀死无关进程。
