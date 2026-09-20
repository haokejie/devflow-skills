from pathlib import Path
import sys
import tempfile
import unittest


PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "devflow-skills"
sys.path.insert(0, str(PLUGIN / "scripts"))

from install_profile import PROFILE, install_profile, main


class ProfileImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "config"
        self.target = self.root / "AGENTS.md"

    def test_preview_leaves_missing_directory_untouched(self):
        install_profile(self.root)
        self.assertFalse(self.root.exists())

    def test_apply_creates_profile_and_repeating_is_noop(self):
        install_profile(self.root, apply=True)
        self.assertEqual(PROFILE.read_bytes(), self.target.read_bytes())
        before = self.target.stat().st_mtime_ns
        install_profile(self.root, apply=True)
        self.assertEqual(before, self.target.stat().st_mtime_ns)
        self.assertEqual(["AGENTS.md"], [p.name for p in self.root.iterdir()])

    def test_existing_preferences_are_not_overwritten_implicitly(self):
        self.root.mkdir()
        self.target.write_text("existing preferences\n")
        install_profile(self.root, replace=True)
        with self.assertRaises(ValueError):
            install_profile(self.root, apply=True)
        self.assertEqual("existing preferences\n", self.target.read_text())
        self.assertEqual(["AGENTS.md"], [p.name for p in self.root.iterdir()])

    def test_explicit_replace_preserves_original_bytes(self):
        self.root.mkdir()
        original = b"original preferences\r\n"
        self.target.write_bytes(original)
        install_profile(self.root, apply=True, replace=True)
        backups = list(self.root.glob("AGENTS.md.backup-*"))
        self.assertEqual(1, len(backups))
        self.assertEqual(original, backups[0].read_bytes())
        self.assertEqual(PROFILE.read_bytes(), self.target.read_bytes())
        self.assertEqual([], list(self.root.glob(".AGENTS-*")))

    def test_symlink_does_not_modify_another_file(self):
        self.root.mkdir()
        other = self.root / "actual.md"
        other.write_text("keep this\n")
        try:
            self.target.symlink_to(other)
        except OSError as error:
            self.skipTest(f"Symlinks unavailable on this host: {error}")
        with self.assertRaises(ValueError):
            install_profile(self.root, apply=True, replace=True)
        self.assertEqual("keep this\n", other.read_text())

    def test_cli_uses_explicit_directory_without_touching_user_profile(self):
        self.assertEqual(0, main(["--codex-home", str(self.root), "--apply"]))
        self.assertEqual(PROFILE.read_bytes(), self.target.read_bytes())


if __name__ == "__main__":
    unittest.main()
