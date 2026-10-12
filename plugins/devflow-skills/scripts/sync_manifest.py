#!/usr/bin/env python3
"""Generate the Codex compatibility manifest from the portable plugin manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]


def compatibility_manifest(portable: dict) -> dict:
    manifest = {key: value for key, value in portable.items() if key not in {"$schema", "extensions"}}
    manifest["skills"] = "./skills/"
    manifest["interface"] = portable["extensions"]["com.openai"]["interface"]
    return manifest


def sync_manifest(plugin: Path, *, write: bool = False) -> str:
    portable = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
    target = plugin / ".codex-plugin" / "plugin.json"
    expected = compatibility_manifest(portable)
    current = json.loads(target.read_text(encoding="utf-8")) if target.is_file() else None
    if current == expected:
        return "Codex 兼容清单已同步。"
    if not write:
        raise ValueError("Codex 兼容清单未同步；运行 scripts/sync_manifest.py --write。")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return "已从通用清单生成 Codex 兼容清单。"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="同步 Codex 兼容清单；默认只检查")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="只检查是否同步（默认）")
    group.add_argument("--write", action="store_true", help="写入生成的兼容清单")
    args = parser.parse_args(argv)
    try:
        print(sync_manifest(PLUGIN, write=args.write))
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"清单同步失败：{error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
