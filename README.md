# DevFlow Skills

<img src="plugins/devflow-skills/assets/icon.png" alt="DevFlow Skills 图标" width="96" height="96" />

面向 Codex 的轻量开发流程插件，包含项目规范、任务记录和 Git 提交三个 skill。

这是基于个人实践整理的社区项目，适合按自己的开发习惯调整。它提供可复用的流程说明和文档模板，具体执行仍依赖 Codex 与项目已有工具。非 OpenAI 官方项目。

## 包含什么

| 调用 ID | 显示名称 | 用途 |
| --- | --- | --- |
| `project-conventions` | 项目开发规范 | 工程规范默认维护根目录 `CONVENTIONS.md`，UI 与交互规范默认维护 `DESIGN.md`；沿用已有明确入口 |
| `task-workflow` | 开发事项记录 | 用一份 `TASK.md` 记录目标、进度和验收，大型需求按需拆分 |
| `git-commit` | Git 提交 | 检查提交范围、相关规范和暂存内容，按授权生成信息或执行提交 |

三个 skill 独立使用，不要求每次开发都走完整流程。另附可选的个人全局偏好模板与导入工具。

### 显示与输出语言

插件与 skill 的显示名称和说明统一使用中文；英文调用 ID 保持不变，原有调用方式继续有效。仍可用中文或英文描述需求，生成提交信息不代表授权执行提交。

回复优先遵循明确的语言要求及项目/全局约定，没有约定时跟随当前对话语言。已有文档保持原语言，新文档和提交信息优先沿用项目的语言约定；需要其他语言时可明确指定。配套全局偏好模板也采用对话语言默认值，更新插件不会覆盖你本机已有的全局规则。

## 安装插件

需要支持 `codex plugin` 命令的 Codex。以下命令可在终端的任意目录执行，无需先下载项目源码：

```sh
codex plugin marketplace add haokejie/devflow-skills
codex plugin add devflow-skills@haokejie
```

安装后新建一个 Codex 任务使用。也可以在插件目录中选择此来源，找到 **开发流程**。**如果只想使用三个 skill，到这里就完成了，无需执行下面的全局偏好导入。**

已将仓库克隆到本地时，也可在仓库根目录执行 `codex plugin marketplace add .`，然后运行相同的安装命令。市场名是 `haokejie`，插件 ID 是 `devflow-skills`。

## 日常使用

- “使用 project-conventions 初始化项目规范”或“检查规范是否过期”。
- “整理 UI 设计规范”或“检查本次界面修改是否符合项目约定”。整理时没有现成设计规范就创建根目录 `DESIGN.md`，已有明确入口则沿用；`CONVENTIONS.md` 只保留链接。普通页面开发和只读检查不自动建文档。
- “规划开发事项”只记录计划；“处理开发事项”进入实施；普通修复不自动创建 `.task`。
- “生成提交信息”只读；“提交本次改动”才暂存和提交。

安装插件不会覆盖原有独立 skill。若以前安装过同名 skill，确认插件可用后再停用旧副本，避免重复发现。

## 可选：导入个人全局偏好

这一步用于把提供的规则模板写入**当前执行命令这台机器**的全局 `AGENTS.md`，不是安装插件的必要步骤。共享的 [偏好模板](plugins/devflow-skills/profiles/global-agents.md) 包含个人浏览器、CDP、禅道和 Go 工具链习惯；请先检查并按自己的环境调整。

安装插件只会把插件文件放进 Codex 管理的安装目录，**不会在终端当前目录创建 `plugins/devflow-skills/` 源码路径**。要运行本节的脚本，需要单独下载仓库。

### 1. 下载源码并进入仓库

以下适用于尚未下载源码的新机器（需要 Git）。在终端逐行执行，每一步成功后再继续：

```sh
cd ~
git clone https://github.com/haokejie/devflow-skills.git
cd devflow-skills
```

这样源码位于当前用户的 `~/devflow-skills/`。如果已下载过，请直接进入实际仓库目录，无需重复克隆。后续命令都在这个仓库目录中执行。

### 2. 预览导入

```sh
python3 plugins/devflow-skills/scripts/install_profile.py
```

默认只显示目标位置和计划操作，不修改配置。提示“内容已一致”时无需再导入。

### 3. 按需要写入或替换

首次导入、目标文件不存在时：

```sh
python3 plugins/devflow-skills/scripts/install_profile.py --apply
```

如果提示已有不同规则，确认要替换后执行下面的命令；脚本会先备份原文件，并显示备份位置：

```sh
python3 plugins/devflow-skills/scripts/install_profile.py --apply --replace
```

`--apply` 表示实际写入，`--replace` 表示允许备份后替换已有不同规则。默认目标是 `~/.codex/AGENTS.md`；设置了 `CODEX_HOME` 时使用该目录下的 `AGENTS.md`，也可通过 `--codex-home /path/to/config` 指定目录。Windows 可用 `py -3` 替换 `python3`。导入工具需要 Python 3.9+，仅使用标准库。

如果报 `can't open file ... [Errno 2] No such file or directory`，说明 Python 没有找到脚本。检查是否完成了下载和 `cd devflow-skills`：`plugins/...` 是相对当前目录的路径，直接在 `~` 下运行会错误地寻找 `~/plugins/...`。这个报错发生在脚本启动前，不会修改全局规则。

账号密码、机器私有配置和第三方登录状态单独保存，不随插件分发。项目允许经授权保存本地凭证，但要求目标未被 Git 跟踪、已明确忽略，且真实值不能进入共享文档或提交。

## 更新与维护

使用 Git 仓库来源安装时：

```sh
codex plugin marketplace upgrade haokejie
codex plugin add devflow-skills@haokejie
```

更新后在新任务中使用。源码位于 `plugins/devflow-skills/`；本地开发时使用 plugin-creator 的缓存刷新和重装流程，不直接修改安装缓存。发布版本只在插件清单中维护。

本项目采用内置 plugin-creator 支持的 `.codex-plugin/plugin.json` 兼容清单，三个 skill 不依赖 MCP 服务。

## 开发与验证

```sh
python3 -m unittest discover -s tests -v
```

测试覆盖偏好导入的预览、重复执行、覆盖与备份边界，以及插件目录和资源引用。发布前还需使用内置 plugin-creator 和 skill-creator 校验清单与 skill。项目约定见 [CONVENTIONS.md](CONVENTIONS.md)。

反馈问题或提出改进可使用 [Issues](https://github.com/haokejie/devflow-skills/issues) 或 Pull Request。

## 许可证

使用 [MIT 许可证](LICENSE)。插件包内附带同一份许可证。

官方参考：[插件打包](https://developers.openai.com/plugins/build/plugins)、[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。
