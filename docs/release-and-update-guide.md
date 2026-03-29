# 发布与更新说明

本文档说明 `astra-studio-plugins` 的发布、首次安装和版本升级流程。

## 基本原则

- `claude plugin install` 只用于首次安装。
- `claude plugin marketplace update` + `claude plugin update` 用于升级已安装插件。
- 远端仓库如果没有 bump `version`，即使刷新 marketplace，本地也可能识别不到新版本。
- marketplace 清单只应声明真实存在且可安装的插件目录。

## Astra Studio Plugins

### 仓库

- GitHub: [VanLengs/astra-studio-plugins](https://github.com/VanLengs/astra-studio-plugins)
- Marketplace 名称: `astra-studio`

### 发布方检查项

发布前确认以下文件的版本号已经同步更新：

- [marketplace.json](/Users/liuyameng/.codex/worktrees/6741/astra-studio-plugins/.claude-plugin/marketplace.json)
- [plugin.json](/Users/liuyameng/.codex/worktrees/6741/astra-studio-plugins/.claude-plugin/plugin.json)
- [studio-core plugin.json](/Users/liuyameng/.codex/worktrees/6741/astra-studio-plugins/studio-core/.claude-plugin/plugin.json)
- [studio-insight plugin.json](/Users/liuyameng/.codex/worktrees/6741/astra-studio-plugins/studio-insight/.claude-plugin/plugin.json)
- [studio-planner plugin.json](/Users/liuyameng/.codex/worktrees/6741/astra-studio-plugins/studio-planner/.claude-plugin/plugin.json)
- [studio-quality plugin.json](/Users/liuyameng/.codex/worktrees/6741/astra-studio-plugins/studio-quality/.claude-plugin/plugin.json)

当前工作流语义升级版本为 `0.2.0`。

### 首次安装

```bash
claude plugin marketplace add github:VanLengs/astra-studio-plugins
claude plugin install studio-core@astra-studio
claude plugin install studio-insight@astra-studio
claude plugin install studio-planner@astra-studio
claude plugin install studio-quality@astra-studio
```

### 升级已安装插件

```bash
claude plugin marketplace update astra-studio
claude plugin update studio-core@astra-studio
claude plugin update studio-insight@astra-studio
claude plugin update studio-planner@astra-studio
claude plugin update studio-quality@astra-studio
```

### 升级失败时的排查顺序

1. 确认使用的是 `update`，不是再次执行 `install`。
2. 先刷新 marketplace 缓存，再更新插件。
3. 确认远端 `plugin.json` 与 `marketplace.json` 的版本号已经 bump。

如本地 CLI 对 `update` 支持不稳定，可使用强制安装兜底：

```bash
claude plugin install --force studio-core@astra-studio
```

## 一句话总结

- 首次安装用 `install`
- 升级用 `marketplace update` + `plugin update`
- 发布前必须 bump 版本
- marketplace 只登记真实存在的插件
