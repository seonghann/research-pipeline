"""Regression tests for Codex workflow generation and installation."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "codex_setup", ROOT / "scripts/codex_setup.py"
)
assert SPEC is not None and SPEC.loader is not None
CODEX_SETUP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CODEX_SETUP)


class CodexSetupTest(unittest.TestCase):
    """Validate generated assets and non-destructive installation behavior."""

    def test_generated_assets_are_complete_and_parseable(self) -> None:
        CODEX_SETUP.generate()
        skills = sorted((ROOT / "codex/skills").glob("*/SKILL.md"))
        agents = sorted((ROOT / "codex/agents").glob("*.toml"))
        self.assertEqual(len(skills), 10)
        self.assertEqual(len(agents), 8)
        self.assertTrue((ROOT / "codex/skills/source-command-go/SKILL.md").exists())
        for agent in agents:
            data = tomllib.loads(agent.read_text())
            self.assertEqual(data["name"], agent.stem)
            self.assertIn("developer_instructions", data)
        for skill in skills:
            text = skill.read_text()
            self.assertTrue(text.startswith("---\nname: source-command-"))
            self.assertNotIn("Task(\"", text)
            self.assertNotIn("git checkout .", text)

    def test_install_preserves_config_and_is_repeatable(self) -> None:
        CODEX_SETUP.generate()
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            codex_home = base / ".codex"
            skills_home = base / ".agents/skills"
            codex_home.mkdir(parents=True)
            stale = skills_home / "source-command-go/references/agents/stale.md"
            stale.parent.mkdir(parents=True)
            stale.write_text("old imported role")
            original = (
                'notify = ["agent-turn-complete"]\n\n'
                '[mcp_servers.existing]\ncommand = "existing-tool"\n'
            )
            (codex_home / "config.toml").write_text(original)

            first = CODEX_SETUP.Installer(codex_home, skills_home)
            first.install()
            installed = (codex_home / "config.toml").read_text()
            parsed = tomllib.loads(installed)
            self.assertEqual(parsed["notify"], ["agent-turn-complete"])
            self.assertIn("existing", parsed["mcp_servers"])
            self.assertIn("arxiv", parsed["mcp_servers"])
            self.assertEqual(parsed["project_doc_max_bytes"], 65536)
            self.assertNotIn("${WANDB_API_KEY}", installed)
            self.assertTrue(first.backup.exists())
            self.assertFalse(stale.exists())
            self.assertTrue(
                (
                    first.backup
                    / str(stale.absolute()).lstrip("/")
                ).exists()
            )

            second = CODEX_SETUP.Installer(codex_home, skills_home)
            second.install()
            self.assertEqual(second.changes, [])
            self.assertFalse(second.backup.exists())

    def test_adopt_preserves_project_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            project.mkdir()
            original = "# Project\n\nScientific claim stays.\n"
            (project / "AGENTS.md").write_text(original)
            installer = CODEX_SETUP.Installer(
                Path(temp) / ".codex", Path(temp) / ".agents/skills"
            )
            installer.adopt(project)
            self.assertEqual((project / "AGENTS.md").read_text(), original)
            self.assertEqual(installer.changes, [])


if __name__ == "__main__":
    unittest.main()
