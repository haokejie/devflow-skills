from pathlib import Path
from contextlib import redirect_stderr
import io
import os
import sys
import tempfile
import unittest
from unittest.mock import patch


PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "devflow-skills"
sys.path.insert(0, str(PLUGIN / "scripts"))

from install_profile import PROFILE, default_config_dir, install_profile, main


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

    def test_cli_preserves_legacy_directory_alias(self):
        self.assertEqual(0, main(["--codex-home", str(self.root), "--apply"]))
        self.assertEqual(PROFILE.read_bytes(), self.target.read_bytes())

    def test_default_preserves_codex_home(self):
        with patch.dict(os.environ, {"CODEX_HOME": str(self.root)}, clear=True):
            self.assertEqual(self.root, default_config_dir())
            self.assertEqual(0, main(["--apply"]))
        self.assertEqual(PROFILE.read_bytes(), self.target.read_bytes())

    def test_default_preserves_original_home_location(self):
        with patch("install_profile.Path.home", return_value=self.root):
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(self.root / ".codex", default_config_dir())
                self.assertEqual(0, main([]))
                self.assertFalse(self.root.exists())
                self.assertEqual(0, main(["--apply"]))
        self.assertEqual(PROFILE.read_bytes(), (self.root / ".codex/AGENTS.md").read_bytes())

    def test_explicit_directory_overrides_default_for_preview_and_apply(self):
        default = Path(self.temp.name) / "default-config"
        with patch.dict(os.environ, {"CODEX_HOME": str(default)}, clear=True):
            flags = ["--config-dir", str(self.root)]
            self.assertEqual(0, main(flags))
            self.assertFalse(self.root.exists())
            self.assertEqual(0, main(flags + ["--apply"]))
        self.assertEqual(PROFILE.read_bytes(), self.target.read_bytes())
        self.assertFalse(default.exists())

    def test_explicit_directory_keeps_existing_overwrite_boundary(self):
        flags = ["--config-dir", str(self.root)]
        main(flags + ["--apply"])
        self.target.write_text("existing rules\n")
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            main(flags + ["--apply"])
        self.assertEqual(1, error.exception.code)
        self.assertEqual("existing rules\n", self.target.read_text())
        main(flags + ["--apply", "--replace"])
        self.assertEqual(PROFILE.read_bytes(), self.target.read_bytes())
        backup = next(self.root.glob("AGENTS.md.backup-*"))
        self.assertEqual("existing rules\n", backup.read_text())

    def test_removed_agent_argument_is_rejected_before_writing(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            main(["--agent", "devin", "--config-dir", str(self.root), "--apply"])
        self.assertEqual(2, error.exception.code)
        self.assertFalse(self.root.exists())

    def test_conflicting_directory_arguments_are_rejected_before_writing(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            main(["--config-dir", str(self.root), "--codex-home", str(self.root / "other"), "--apply"])
        self.assertEqual(2, error.exception.code)
        self.assertFalse(self.root.exists())


if __name__ == "__main__":
    unittest.main()
