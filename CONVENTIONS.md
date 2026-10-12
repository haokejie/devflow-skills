# 项目开发规范

## 项目与边界

- 本仓库是社区维护的轻量 Codex 与 Devin 插件项目，包含一个 `devflow-skills` 插件和三个独立 skill，不依赖 MCP 服务。Devin 指支持 Agent Plugins 的 Devin Local / CLI。
- 仓库为 `haokejie/devflow-skills`，市场名为 `haokejie`，仓库说明以中文维护；插件与 skill 的显示名称和说明统一使用中文，英文调用 ID 保持稳定，执行时按用户和项目语言约定输出。
- 插件源码在 `plugins/devflow-skills/`；`.agents/plugins/marketplace.json` 是仓库级插件目录，来源路径相对仓库根目录。
- 插件根目录 `plugin.json` 是唯一维护的清单，采用 Agent Plugins 1.0.0；名称、版本和共享元数据在此维护，Codex 展示信息放在 `extensions.com.openai.interface`。三个 skill 和参考资源跨宿主共用，不复制正文。
- `.codex-plugin/plugin.json` 是提交到仓库的生成兼容文件，通过 `scripts/sync_manifest.py --write` 同步，不手工编辑。保留它兼容已有 Codex 市场和清单工具；相关入口全部支持通用格式后才评估删除。默认或 `--check` 只检查一致性。
- `profiles/global-agents.md` 是全局偏好的分发模板，不是本项目的开发指令；导入工具显式执行后才会写入用户配置。

## 维护约定

- 本仓库是维护源；安装缓存是运行副本，不反向覆盖源码。
- 三个 skill 继续各自负责规范、任务记录和提交，按需加载参考资料；同一规则只在负责它的文档中维护。
- 导入和清单同步工具使用 Python 3.9+ 标准库。`--config-dir` 指定目录，默认使用 `CODEX_HOME` 或 `~/.codex`；`--codex-home` 是同一参数的别名。不写死用户名。项目私有资料的位置与保存边界见 [全局模板的本地私有信息规则](plugins/devflow-skills/profiles/global-agents.md#本地私有信息)。
- 导入默认只预览；`--apply` 才写入。已有不同内容需要 `--replace`，替换前备份；相同内容重复导入不产生备份。
- 不把真实账号密码、token、机器私有配置或生成缓存打包进插件。具体边界见全局模板，项目示例只使用虚构值。

- 根目录 `LICENSE` 是许可证正文；插件内保留相同的分发副本，修改时校验两者一致。

## 验证

- `python3 plugins/devflow-skills/scripts/sync_manifest.py --check`：核对生成清单与通用清单是否一致。
- `python3 -m unittest discover -s tests -v`：验证目录选择、参数别名、预览、幂等、备份和覆盖边界，以及插件资源结构和双格式清单契约。
- 通用清单按 `$schema` 指向的官方 schema 校验；不得把 Codex 专有字段放到通用清单根层级。
- 交付前使用当前内置 plugin-creator 的 `validate_plugin.py` 校验插件目录，使用 skill-creator 的 `quick_validate.py` 校验三个 skill。
- 安装验收在新会话中确认插件和 skill 已加载；源码校验验证结构与格式。
