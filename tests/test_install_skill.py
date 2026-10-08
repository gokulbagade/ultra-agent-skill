#!/usr/bin/env python3
"""
Unit tests for install_skill.py
"""

import sys
import unittest
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from install_skill import install_ultra_skill


class TestInstallSkill(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.target_path = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_installs_proper_agents_folder_structure(self):
        result = install_ultra_skill(self.target_path)
        self.assertEqual(result["status"], "SUCCESS")

        agents_dir = self.target_path / ".agents"
        self.assertTrue(agents_dir.exists())

        # Check .agents/skills/ultra-skill/
        skill_dir = agents_dir / "skills" / "ultra-skill"
        self.assertTrue(skill_dir.exists())
        self.assertTrue((skill_dir / "SKILL.md").exists())
        self.assertTrue((skill_dir / "agents").exists())
        self.assertTrue((skill_dir / "workflows").exists())
        self.assertTrue((skill_dir / "scripts").exists())
        self.assertTrue((skill_dir / "references").exists())

        # Check .agents/agents/
        top_agents = agents_dir / "agents"
        self.assertTrue(top_agents.exists())
        self.assertTrue((top_agents / "planner.md").exists())
        self.assertTrue((top_agents / "architect.md").exists())
        self.assertTrue((top_agents / "engineer.md").exists())

        # Check .agents/rules/
        rules_dir = agents_dir / "rules"
        self.assertTrue(rules_dir.exists())
        self.assertTrue((rules_dir / "AGENTS.md").exists())

        # Check project root entrypoints
        self.assertTrue((self.target_path / "AGENTS.md").exists())
        self.assertTrue((self.target_path / "CLAUDE.md").exists())
        self.assertTrue((self.target_path / "GEMINI.md").exists())
        self.assertTrue((self.target_path / ".slopignore").exists())


if __name__ == "__main__":
    unittest.main()
