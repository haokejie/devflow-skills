# DevFlow Skills

<img src="plugins/devflow-skills/assets/icon.png" alt="DevFlow Skills 图标" width="96" height="96" />

面向 Codex 与 Devin 的轻量开发流程插件，包含项目规范、设计方案、任务记录、Git 提交与禅道工作流五个 skill。

这是基于个人实践整理的社区项目，适合按自己的开发习惯调整。它提供可复用的流程说明和文档模板，具体执行依赖当前 AI 宿主与项目已有工具。非 OpenAI 或 Cognition 官方项目。

## 包含什么

| 调用 ID | 显示名称 | 用途 |
| --- | --- | --- |
| `project-conventions` | 项目开发规范 | 工程规范默认维护根目录 `CONVENTIONS.md`，UI 与交互规范默认维护 `DESIGN.md`；沿用已有明确入口 |
| `design-workflow` | 设计方案 | 用一份 `SPEC.md` 和必要图纸保存开发依据，供任务引用，并清理无有效引用的废弃方案 |
| `task-workflow` | 开发事项记录 | 用一份 `TASK.md` 记录目标、进度和验收，大型需求按需拆分 |
| `git-commit` | Git 提交 | 检查提交范围、相关规范和暂存内容，按授权生成信息或执行提交 |
| `zentao-workflow` | 禅道工作流 | 复用界面中已连接的禅道 MCP 分析 Bug 与附件，明确要求修复才修改业务代码 |

五个 skill 独立使用、独立启停，不要求每次开发都走完整流程，也不要求全部启用。仓库另提供可选的个人全局偏好模板，位于根目录 `profiles/`；导入与维护工具位于根目录 `scripts/`。插件目录只保留清单、skill 及其使用资源、展示图标和许可证。

禅道 skill 使用当前会话已有的 `zentao_*` 工具，连接名称由客户端决定。插件不分发 MCP 服务器，不创建第二个连接或额外的凭证配置；禅道连接仍在宿主原生界面管理。

### 显示与输出语言

插件与 skill 的显示名称和说明统一使用中文，调用 ID 使用英文。可用中文或英文描述需求，生成提交信息不代表授权执行提交。

回复优先遵循明确的语言要求及项目/全局约定，没有约定时跟随当前对话语言。已有文档保持原语言，新文档和提交信息优先沿用项目的语言约定；需要其他语言时可明确指定。配套全局偏好模板也采用对话语言默认值，更新插件不会覆盖你本机已有的全局规则。

## 安装插件

### Codex

需要支持 `codex plugin` 命令的 Codex。以下命令可在终端的任意目录执行，无需先下载项目源码：

```sh
codex plugin marketplace add haokejie/devflow-skills
codex plugin add devflow-skills@haokejie
```

安装后新建一个 Codex 任务使用。也可以在插件目录中选择此来源，找到 **开发流程**。**使用这些 skill 无需执行下面的全局偏好导入。** 禅道 skill 另需当前会话已有禅道 MCP 连接。

已将仓库克隆到本地时，也可在仓库根目录执行 `codex plugin marketplace add .`，然后运行相同的安装命令。市场名是 `haokejie`，插件 ID 是 `devflow-skills`。

### Devin Local / Devin CLI

需要已登录且支持 `devin plugins` 的 Devin CLI。Devin Desktop 的 Devin Local 使用同一套 Agent 插件能力。

仅安装在当前机器：

```sh
devin plugins install --local 'haokejie/devflow-skills#plugins/devflow-skills'
devin plugins info devflow-skills
```

`#plugins/devflow-skills` 指向真正的插件子目录。不要省略它：仓库根目录是 Codex 插件市场，技能包位于子目录中。`--local` 避免把安装同步到 Devin Cloud 的个人插件清单；确实希望账号同步时可省略此参数。插件管理需要正常的 Devin 登录及账号策略允许，安装前查看 CLI 显示的插件内容。

本地源码开发时，在仓库根目录运行：

```sh
devin plugins install --local ./plugins/devflow-skills
```

安装后新建 Devin Local / CLI 会话使用。这五个技能的显式调用方式为：

```text
/devflow-skills:project-conventions
/devflow-skills:design-workflow
/devflow-skills:task-workflow
/devflow-skills:git-commit
/devflow-skills:zentao-workflow
```

也可直接用下面的自然语言请求。单独显式调用提交技能表示要求提交；只想获取提交信息时请同时写明“仅生成提交信息”。技能正文与模板由 Codex 和 Devin 共用，无需维护两份。`agents/openai.yaml` 只提供 Codex 展示信息，Devin 使用 `SKILL.md`。

加载格式见 [Devin 插件文档](https://docs.devin.ai/cli/extensibility/plugins/overview)。

## 日常使用

- “使用 project-conventions 初始化项目规范”或“检查规范是否过期”。
- “整理 UI 设计规范”或“检查本次界面修改是否符合项目约定”。整理时没有现成设计规范就创建根目录 `DESIGN.md`，已有明确入口则沿用；`CONVENTIONS.md` 只保留链接。普通页面开发和只读检查不自动建文档。
- “整理这些设计图和说明，后续任务按它实现”使用 `design-workflow` 保存方案；“检查废弃设计”只读，“清理已废弃设计”才删除无有效引用的方案及专属资料。
- “规划开发事项”只记录计划；“处理开发事项”进入实施；普通修复不自动创建 `.task`。
- “生成提交信息”只读；“提交本次改动”才暂存和提交。
- 直接发送 `bug#1234` 或要求“使用 zentao-workflow 分析禅道 Bug 1234，先查看截图与附件”，会使用禅道 skill 做只读分析；“修复禅道 Bug 1234”才修改业务代码，回写禅道另需明确授权。

若存在同名 skill，确认插件可用后停用重复副本。

### 独立启用与停用

Codex 桌面客户端在插件详情的技能列表中提供每个 skill 的独立开关；插件总开关控制整个插件。其他宿主的启停入口以其实际功能为准，插件不会另建开关配置。Codex 的技能启停由宿主管理，见 [技能文档](https://learn.chatgpt.com/docs/build-skills) 与 [App Server 接口](https://learn.chatgpt.com/docs/app-server)。

| 单独启用 | 可以完成的工作 | 前提 |
| --- | --- | --- |
| `project-conventions` | 初始化、维护与检查项目通用规范 | 当前项目源码与配置 |
| `design-workflow` | 整理、引用、检查和清理设计方案 | 对应设计资料；不强制创建任务记录 |
| `task-workflow` | 规划、实施、继续与验收开发事项 | 当前项目；已有设计方案可直接引用 |
| `git-commit` | 生成提交信息或按授权提交 | Git 仓库；已有规范直接读取 |
| `zentao-workflow` | 分析禅道 Bug 与附件，按授权修复 | 已连接并可用的禅道 MCP |

跨 skill 协作只在对方已启用、可用且确有需要时发生；停用后不通过读取其指令间接恢复流程。已有 `CONVENTIONS.md`、`DESIGN.md`、设计方案与任务记录仍可按需读取，MCP 连接也由宿主单独管理。禅道 skill 停用后，不再自动触发单独 `bug#1234` 的编号工作流。

`allow_implicit_invocation: false` 只关闭自动匹配，显式调用仍可用，不能代替技能停用开关。全局模板已按启停状态约束入口；插件更新不会自动改写用户已导入的全局规则。

## 设计方案与开发事项

项目通用规范保存在根目录 `DESIGN.md`；具体功能的设计图与说明由 [design-workflow](plugins/devflow-skills/skills/design-workflow/SKILL.md) 维护，默认结构为：

```text
.design/order-management/
  SPEC.md              # 适用范围、采用情况、图纸链接、说明与验收
  assets/              # 有需要保存的图纸时才创建
.task/order-list/
  TASK.md              # 引用方案，记录进度与验证
```

一份方案可以供多个任务引用。任务记录链接方案、相关图纸和采用版本（有时），按设计开发前实际查看图纸，完成后检查渲染与交互；不重复抄写设计正文，也不强制建立审批、版本目录或任务集。已有明确入口和已确认方案直接沿用。

`.design` 默认用于本地资料，新建且没有明确共享约定时添加项目级 `/.design/` 忽略规则；已有 Git 策略沿用。清理时保留仍被任务或文档使用的方案和共享图片，不把任务完成直接当成设计废弃。

## 禅道连接与使用

已在界面中配置禅道 MCP 时，保留现有连接，安装或更新插件后在新会话使用 `zentao-workflow` 即可，无需重新填写凭证。

尚未连接时，在宿主原生 MCP 管理界面添加服务器。以 Codex 的本地 stdio 表单为例：

- 启动命令：`npx`。该服务需要本机 Node.js 20+ 与 npm/npx。
- 参数：分别添加 `--yes` 与 `zentao-bugfix-mcp@0.1.4`；这是已验证的服务版本示例，插件不固定或管理你的 MCP 版本。
- 环境变量：按下列用途在界面填写，真实值由客户端保存在本机。

- `ZENTAO_BASE_URL`：禅道站点根地址；部署在子目录时包含该子目录，不附加 `/api.php/v1`。
- `ZENTAO_TOKEN`：已有的 REST token；有值时优先使用。
- `ZENTAO_ACCOUNT` 与 `ZENTAO_PASSWORD`：token 为空时用于认证；仅使用 token 时可删除这两个键。
- `ZENTAO_ATTACHMENT_DIR`：可选附件保存目录；默认使用系统临时目录下的 `zentao-bugfix-mcp`。
- `ZENTAO_ALLOW_ALL_REST_WRITE`：通常填 `false`；需要真实写入时按已授权的用途在客户端显式配置。仅提供 Bug 编号或要求分析时保持只读。

保存后按界面提示重新连接或重启，再新建会话。无法发现 `zentao_*` 工具时，检查原生界面的 MCP 连接状态；安装本插件不会自动安装或连接禅道服务。不要把真实值写进插件源码、安装缓存或共享文档。

连接后先调用 `zentao_health_check` 检查认证，再按需调用 `zentao_get_workflow_guide`。例如：“分析禅道 Bug 1234，先查看截图与附件。”默认不修改 Bug 状态；明确要求修复才在目标业务仓库实施。

界面配置方式见 [Codex MCP 文档](https://learn.chatgpt.com/docs/extend/mcp)，服务参数见 [禅道 MCP 文档](https://github.com/haokejie/zentao-bugfix-mcp/tree/main/apps/mcp-stdio)。

## 可选：导入个人全局偏好

这一步把 [偏好模板](profiles/global-agents.md) 写入当前机器的全局 `AGENTS.md`，按需使用。模板包含浏览器、CDP 和 Go 工具链习惯，并保留设计方案与禅道 skill 的必要入口和边界，具体流程由相应 skill 维护。请先按自己的环境调整。项目私有资料默认存放在项目根目录的 `.devflow/local.md`，已有入口时沿用。

偏好模板与导入脚本都位于仓库层。要执行本节的导入，需要单独下载仓库；安装插件不会提供全局偏好模板或维护工具。

### 1. 下载源码并进入仓库

以下适用于尚未下载源码的新机器（需要 Git）。在终端逐行执行，每一步成功后再继续：

```sh
cd ~
git clone https://github.com/haokejie/devflow-skills.git
cd devflow-skills
```

这样源码位于当前用户的 `~/devflow-skills/`。如果已下载过，请直接进入实际仓库目录，无需重复克隆。后续命令都在这个仓库目录中执行。

### 2. 选择目录并预览导入

```sh
python3 scripts/install_profile.py
```

默认只预览，不修改配置。省略目录时使用 `CODEX_HOME`，未设置时使用 `~/.codex`。提示“内容已一致”时无需再导入。

通过 `--config-dir` 指定目标软件读取全局 `AGENTS.md` 的目录。例如 Devin 在 macOS / Linux 使用：

```sh
python3 scripts/install_profile.py --config-dir ~/.config/devin
```

Devin 在 Windows 使用 `%APPDATA%\devin`，PowerShell 示例为 `py -3 scripts/install_profile.py --config-dir "$env:APPDATA\devin"`。

### 3. 按需要写入或替换

首次导入、目标文件不存在时，在预览命令末尾加上 `--apply`；保留预览时选择的目录。例如：

```sh
python3 scripts/install_profile.py --config-dir ~/.config/devin --apply
```

如果提示已有不同规则，确认要替换后执行下面的命令；脚本会先备份原文件，并显示备份位置：

```sh
python3 scripts/install_profile.py --config-dir ~/.config/devin --apply --replace
```

`--apply` 表示实际写入，`--replace` 表示允许备份后替换已有不同规则。使用自定义目录时，在同一条命令中保留 `--config-dir` 并加上 `--apply --replace`；写入的是该目录下的 `AGENTS.md`。符号链接不会被覆盖，需要显式指定实际目标目录。全局规则在新会话开始时加载，见 [Devin 全局规则文档](https://docs.devin.ai/cli/extensibility/rules)。

Windows 可用 `py -3` 替换 `python3`。导入工具需要 Python 3.9+，仅使用标准库；安装或更新插件不会执行此导入，也不会改写现有全局配置。

如果报 `can't open file ... [Errno 2] No such file or directory`，说明 Python 没有找到脚本。检查是否完成了下载和 `cd devflow-skills`：`scripts/...` 是相对当前目录的路径，直接在 `~` 下运行会错误地寻找 `~/scripts/...`。这个报错发生在脚本启动前，不会修改全局规则。

账号密码、机器私有配置和第三方登录状态单独保存，不随插件分发。项目允许经授权保存本地凭证，但要求目标未被 Git 跟踪、已明确忽略，且真实值不能进入共享文档或提交。

## 更新与维护

Codex 使用 Git 仓库来源安装时：

```sh
codex plugin marketplace upgrade haokejie
codex plugin add devflow-skills@haokejie
```

Codex 更新后在新任务中使用。Devin 远端来源安装后使用 `devin plugins update devflow-skills` 更新，再新建会话；本地目录安装直接链接源码，改动在新会话加载，不需要复制缓存。

插件源码位于 `plugins/devflow-skills/`，维护工具位于仓库根目录 `scripts/`；不要直接修改安装缓存。名称、版本和共享展示信息只维护 [通用清单](plugins/devflow-skills/plugin.json)。修改后在仓库根目录运行：

```sh
python3 scripts/sync_manifest.py --write
```

此命令生成 `.codex-plugin/plugin.json`；默认或 `--check` 只检查是否已同步，不写文件。

通用清单采用 [Agent Plugins 1.0.0](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)，Codex 展示元数据位于 `extensions.com.openai.interface`。Devin 读取通用清单和同一份 `skills/`；规范、设计方案、任务和提交 skill 不依赖 MCP，禅道 skill 复用宿主已连接的 MCP。

## 开发与验证

```sh
python3 scripts/sync_manifest.py --check
python3 -m unittest discover -s tests -v
```

测试覆盖目录选择、参数别名、预览、幂等、备份与覆盖边界，以及清单一致性、五个 skill 的资源独立性和不分发禅道连接配置的边界。完整验证要求见 [CONVENTIONS.md](CONVENTIONS.md)。

反馈问题或提出改进可使用 [Issues](https://github.com/haokejie/devflow-skills/issues) 或 Pull Request。

## 许可证

使用 [MIT 许可证](LICENSE)。插件包内附带同一份许可证。

官方参考：[插件打包](https://developers.openai.com/plugins/build/plugins)、[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。
