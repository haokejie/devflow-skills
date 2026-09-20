# DevFlow Skills

面向 Codex 的轻量开发流程插件，包含项目规范、任务记录和 Git 提交三个 skill。

这是基于个人实践整理的社区项目，适合按自己的开发习惯调整。它提供可复用的流程说明和文档模板，具体执行仍依赖 Codex 与项目已有工具。非 OpenAI 官方项目。

## 包含什么

| Skill | 用途 |
| --- | --- |
| `project-conventions` | 维护根目录 `CONVENTIONS.md`，随代码校准稳定约定，检查共享文档是否遗漏 |
| `task-workflow` | 用一份 `TASK.md` 记录目标、进度和验收，大型需求按需拆分 |
| `git-commit` | 检查提交范围、相关规范和暂存内容，按授权生成信息或执行提交 |

三个 skill 独立使用，不要求每次开发都走完整流程。另附可选的个人全局偏好模板与导入工具。

## 安装插件

需要支持 `codex plugin` 命令的 Codex。添加此仓库为插件来源，再安装插件：

```sh
codex plugin marketplace add haokejie/devflow-skills
codex plugin add devflow-skills@haokejie
```

安装后新建一个 Codex 任务使用。也可以在插件目录中选择此来源，找到 **DevFlow Skills · 开发流程**。

已将仓库克隆到本地时，也可在仓库根目录执行 `codex plugin marketplace add .`，然后运行相同的安装命令。市场名是 `haokejie`，插件 ID 是 `devflow-skills`。

## 日常使用

- “使用 project-conventions 初始化项目规范”或“检查规范是否过期”。
- “规划开发事项”只记录计划；“处理开发事项”进入实施；普通修复不自动创建 `.task`。
- “生成提交信息”只读；“提交本次改动”才暂存和提交。

安装插件不会覆盖原有独立 skill。若以前安装过同名 skill，确认插件可用后再停用旧副本，避免重复发现。

## 可选：导入个人全局偏好

插件安装不会自动修改全局 `AGENTS.md`。共享的 [偏好模板](plugins/devflow-skills/profiles/global-agents.md) 包含个人浏览器、CDP、禅道和 Go 工具链习惯；建议先检查并按自己的环境调整。

下面的命令在克隆后的仓库根目录执行：

```sh
# 默认预览，不修改配置
python3 plugins/devflow-skills/scripts/install_profile.py

# 目标不存在时写入；内容已一致时不重复处理
python3 plugins/devflow-skills/scripts/install_profile.py --apply

# 明确替换已有不同规则，自动保留备份
python3 plugins/devflow-skills/scripts/install_profile.py --apply --replace
```

默认使用已设置的 `CODEX_HOME`，否则使用用户目录下的 `.codex`；通过 `--codex-home /path/to/config` 可以指定其他位置。Windows 可用 `py -3` 替换 `python3`。导入工具需要 Python 3.9+，仅使用标准库。

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
