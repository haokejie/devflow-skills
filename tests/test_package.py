import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "devflow-skills"


class PackageTests(unittest.TestCase):
    def test_distributed_plugin_contains_license(self):
        self.assertEqual((ROOT / "LICENSE").read_bytes(), (PLUGIN / "LICENSE").read_bytes())

    def test_marketplace_resolves_to_actual_plugin(self):
        catalog = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(1, len(catalog["plugins"]))
        entry = catalog["plugins"][0]
        self.assertEqual(PLUGIN.resolve(), (ROOT / entry["source"]["path"]).resolve())
        manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(PLUGIN.name, manifest["name"])
        self.assertEqual(entry["name"], manifest["name"])

    def test_all_three_skills_are_shipped_with_resources(self):
        skills = PLUGIN / "skills"
        expected = {"project-conventions", "task-workflow", "git-commit"}
        self.assertEqual(expected, {p.name for p in skills.iterdir() if p.is_dir()})
        for name in expected:
            self.assertTrue((skills / name / "SKILL.md").is_file())
            self.assertTrue((skills / name / "agents/openai.yaml").is_file())
        for path in skills.rglob("*.md"):
            if "templates" in path.parts:
                continue
            content = re.sub(r"```[\s\S]*?```", "", path.read_text(encoding="utf-8"))
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
                if "://" not in target and not target.startswith("#"):
                    self.assertTrue((path.parent / target.split("#", 1)[0]).is_file(), (path, target))


if __name__ == "__main__":
    unittest.main()
