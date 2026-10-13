import json
from pathlib import Path
import re
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "devflow-skills"
sys.path.insert(0, str(ROOT / "scripts"))

from sync_manifest import sync_manifest


class PackageTests(unittest.TestCase):
    def test_distributed_plugin_contains_license(self):
        self.assertEqual((ROOT / "LICENSE").read_bytes(), (PLUGIN / "LICENSE").read_bytes())

    def test_marketplace_resolves_to_actual_plugin(self):
        catalog = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(1, len(catalog["plugins"]))
        entry = catalog["plugins"][0]
        self.assertEqual(PLUGIN.resolve(), (ROOT / entry["source"]["path"]).resolve())
        manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(PLUGIN.name, manifest["name"])
        self.assertEqual(entry["name"], manifest["name"])

    def test_hosts_share_identity_and_skills(self):
        portable = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
        codex = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual("https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", portable["$schema"])
        for key in ["name", "version", "description", "author", "homepage", "repository", "license"]:
            self.assertEqual(portable[key], codex[key], key)
        self.assertNotIn("interface", portable)
        self.assertNotIn("skills", portable)
        self.assertEqual(portable["extensions"]["com.openai"]["interface"], codex["interface"])
        self.assertEqual(PLUGIN / "skills", PLUGIN / codex["skills"])
        sync_manifest(PLUGIN)

    def test_stale_compatibility_manifest_requires_explicit_write(self):
        with tempfile.TemporaryDirectory() as folder:
            plugin = Path(folder)
            source = plugin / "plugin.json"
            source.write_text(json.dumps({
                "name": "example", "version": "1.0.0",
                "extensions": {"com.openai": {"interface": {"displayName": "Example"}}},
            }))
            with self.assertRaises(ValueError):
                sync_manifest(plugin)
            self.assertFalse((plugin / ".codex-plugin").exists())
            sync_manifest(plugin, write=True)
            target = plugin / ".codex-plugin" / "plugin.json"
            self.assertEqual("1.0.0", json.loads(target.read_text())["version"])
            updated = json.loads(source.read_text())
            updated["version"] = "1.1.0"
            source.write_text(json.dumps(updated))
            with self.assertRaises(ValueError):
                sync_manifest(plugin)
            self.assertEqual("1.0.0", json.loads(target.read_text())["version"])
            sync_manifest(plugin, write=True)
            self.assertEqual("1.1.0", json.loads(target.read_text())["version"])
            mtime = target.stat().st_mtime_ns
            sync_manifest(plugin, write=True)
            self.assertEqual(mtime, target.stat().st_mtime_ns)
            self.assertEqual(updated, json.loads(source.read_text()))

    def test_zentao_connection_is_not_bundled(self):
        for filename in ["mcp.json", ".mcp.json", ".app.json"]:
            self.assertFalse((PLUGIN / filename).exists(), filename)
        codex = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
        self.assertNotIn("mcpServers", codex)
        self.assertNotIn("apps", codex)

    def test_all_five_skills_are_shipped_with_resources(self):
        skills = PLUGIN / "skills"
        expected = {"project-conventions", "design-workflow", "task-workflow", "git-commit", "zentao-workflow"}
        self.assertEqual(expected, {p.name for p in skills.iterdir() if p.is_dir()})
        for name in expected:
            skill = (skills / name).resolve()
            self.assertTrue((skill / "SKILL.md").is_file())
            self.assertTrue((skill / "agents/openai.yaml").is_file())
            for path in skill.rglob("*.md"):
                if "templates" in path.parts:
                    continue
                content = re.sub(r"```[\s\S]*?```", "", path.read_text(encoding="utf-8"))
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
                    if "://" not in target and not target.startswith("#"):
                        resource = (path.parent / target.split("#", 1)[0]).resolve()
                        self.assertTrue(resource.is_relative_to(skill), (path, target, "资源必须属于本 skill"))
                        self.assertTrue(resource.is_file(), (path, target))


if __name__ == "__main__":
    unittest.main()
