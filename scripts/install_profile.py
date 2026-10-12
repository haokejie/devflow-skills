#!/usr/bin/env python3
"""Import the repository's global preferences only when explicitly requested."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile


PROFILE = Path(__file__).resolve().parents[1] / "profiles" / "global-agents.md"


def default_config_dir() -> Path:
    configured = os.environ.get("CODEX_HOME")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".codex"


def install_profile(config_dir: Path, *, apply: bool = False, replace: bool = False) -> str:
    target = config_dir.expanduser() / "AGENTS.md"
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
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--config-dir", type=Path, help="目标配置目录（默认 CODEX_HOME 或 ~/.codex）")
    group.add_argument("--codex-home", dest="config_dir", type=Path, help="--config-dir 的兼容别名")
    parser.add_argument("--apply", action="store_true", help="实际写入；默认只预览")
    parser.add_argument("--replace", action="store_true", help="允许备份后替换已有不同规则")
    args = parser.parse_args(argv)
    config_dir = args.config_dir
    if config_dir is None:
        config_dir = default_config_dir()
    try:
        print(install_profile(config_dir, apply=args.apply, replace=args.replace))
    except (OSError, ValueError) as error:
        parser.exit(1, f"导入失败：{error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
