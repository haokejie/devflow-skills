#!/usr/bin/env python3
"""Import the bundled global preferences only when explicitly requested."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile


PROFILE = Path(__file__).resolve().parents[1] / "profiles" / "global-agents.md"


def default_codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".codex"


def default_config_dir(agent: str) -> Path:
    if agent == "codex":
        return default_codex_home()
    if agent != "devin":
        raise ValueError(f"不支持的 agent：{agent}")
    if sys.platform == "win32":
        app_data = os.environ.get("APPDATA")
        if not app_data:
            raise ValueError("APPDATA 未设置，请通过 --config-dir 指定 Devin 配置目录。")
        return Path(app_data) / "devin"
    return Path.home() / ".config" / "devin"


def install_profile(codex_dir: Path, *, apply: bool = False, replace: bool = False) -> str:
    # Preserve the original keyword argument; the directory can belong to either host.
    target = codex_dir.expanduser() / "AGENTS.md"
    if target.is_symlink():
        raise ValueError(f"目标是符号链接，未修改：{target}。请显式指定实际配置目录。")
    if target.exists() and not target.is_file():
        raise ValueError(f"目标不是普通文件：{target}")

    desired = PROFILE.read_bytes()
    current = target.read_bytes() if target.is_file() else None
    if current == desired:
        return f"内容已一致，无需更新：{target}"
    if not apply:
        action = "新建" if current is None else "替换并备份"
        flags = "--apply" if current is None else "--apply --replace"
        return f"预览：将{action} {target}。确认后使用 {flags} 执行。"
    if current is not None and not replace:
        raise ValueError(f"已有不同规则，未覆盖：{target}。确认替换时使用 --apply --replace。")

    target.parent.mkdir(parents=True, exist_ok=True)
    if current is None:
        # Exclusive creation preserves a file created by another process after preview.
        with target.open("xb") as handle:
            handle.write(desired)
        return f"已写入：{target}"

    backup_fd, backup_name = tempfile.mkstemp(prefix="AGENTS.md.backup-", dir=target.parent)
    with os.fdopen(backup_fd, "wb") as handle:
        handle.write(current)
    replacement_fd, replacement_name = tempfile.mkstemp(prefix=".AGENTS-", dir=target.parent)
    replacement = Path(replacement_name)
    try:
        with os.fdopen(replacement_fd, "wb") as handle:
            handle.write(desired)
        os.replace(replacement, target)
    finally:
        replacement.unlink(missing_ok=True)
    return f"已更新：{target}\n原规则备份：{backup_name}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="预览或导入 DevFlow Skills 全局偏好")
    parser.add_argument("--agent", choices=["codex", "devin"], default="codex", help="目标宿主（默认 codex）")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--config-dir", type=Path, help="显式指定目标宿主的配置目录")
    group.add_argument("--codex-home", type=Path, help="Codex 配置目录（保留原参数，仅适用于 codex）")
    parser.add_argument("--apply", action="store_true", help="实际写入；默认只预览")
    parser.add_argument("--replace", action="store_true", help="允许备份后替换已有不同规则")
    args = parser.parse_args(argv)
    if args.codex_home is not None and args.agent != "codex":
        parser.error("--codex-home 仅适用于 --agent codex；Devin 请使用 --config-dir。")
    try:
        if args.config_dir is not None:
            config_dir = args.config_dir
        elif args.codex_home is not None:
            config_dir = args.codex_home
        else:
            config_dir = default_config_dir(args.agent)
        print(install_profile(config_dir, apply=args.apply, replace=args.replace))
    except (OSError, ValueError) as error:
        parser.exit(1, f"导入失败：{error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
