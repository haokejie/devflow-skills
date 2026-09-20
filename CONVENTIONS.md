# 项目开发规范

## 项目与边界

- 本仓库是社区维护的轻量 Codex 插件项目，包含一个 `devflow-skills` 插件和三个独立 skill，不依赖 MCP 服务。
- 仓库为 `haokejie/devflow-skills`，市场名为 `haokejie`，用户说明与插件介绍使用中文。
- 插件源码在 `plugins/devflow-skills/`；`.agents/plugins/marketplace.json` 是仓库级插件目录，来源路径相对仓库根目录。
- `.codex-plugin/plugin.json` 是当前唯一插件清单，采用内置 plugin-creator 支持的兼容格式；名称、版本和展示信息在此维护。
- `profiles/global-agents.md` 是全局偏好的分发模板，不是本项目的开发指令；导入工具显式执行后才会写入用户配置。

## 维护约定

- 本仓库是后续维护源；已安装插件缓存及旧独立 skill 是运行副本，不反向覆盖源码。
- 三个 skill 继续各自负责规范、任务记录和提交，按需加载参考资料；同一规则只在负责它的文档中维护。
- 导入工具使用 Python 3.9+ 标准库；通过 `Path.home()`、已设置的 `CODEX_HOME` 或 `--codex-home` 定位配置，不写死用户名或操作系统路径。
- 导入默认只预览；`--apply` 才写入。已有不同内容需要 `--replace`，替换前备份；相同内容重复导入不产生备份。
- 不把真实账号密码、token、机器私有配置或生成缓存打包进插件。具体边界见全局模板，项目示例只使用虚构值。

- 根目录 `LICENSE` 是许可证正文；插件内保留相同的分发副本，修改时校验两者一致。

## 验证

- `python3 -m unittest discover -s tests -v`：验证导入的预览、幂等、备份和覆盖边界，以及插件资源结构。
- 交付前使用当前内置 plugin-creator 的 `validate_plugin.py` 校验插件目录，使用 skill-creator 的 `quick_validate.py` 校验三个 skill。
- 安装检查需区分“源码校验通过”和“已安装并在新会话启用”；创建项目本身不会替换现有全局配置或停用旧 skill。
