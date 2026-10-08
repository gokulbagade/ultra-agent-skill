#!/usr/bin/env python3
"""
Unit tests for install_skill.py
"""

import sys
import unittest
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from install_skill import install_ultra_skill, adapt_workspace_entrypoints


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
        gemini_md = self.target_path / "GEMINI.md"
        agents_md = self.target_path / "AGENTS.md"
        claude_md = self.target_path / "CLAUDE.md"
        self.assertTrue(gemini_md.exists())
        self.assertTrue(agents_md.exists())
        self.assertTrue(claude_md.exists())
        self.assertTrue((self.target_path / ".slopignore").exists())

        # Verify entrypoints point to .agents/skills/ultra-skill/SKILL.md
        gemini_text = gemini_md.read_text(encoding="utf-8")
        agents_text = agents_md.read_text(encoding="utf-8")
        claude_text = claude_md.read_text(encoding="utf-8")

        self.assertIn(".agents/skills/ultra-skill/SKILL.md", gemini_text)
        self.assertIn(".agents/skills/ultra-skill/SKILL.md", agents_text)
        self.assertIn(".agents/skills/ultra-skill/SKILL.md", claude_text)
        self.assertNotIn("file:///d:/Agent", gemini_text)
        self.assertNotIn("file:///d:/Agent", agents_text)

    def test_clean_root_removes_loose_folders(self):
        # Simulate an accidental clone or manual copy with loose root folders
        loose_skills = self.target_path / "skills"
        loose_skills.mkdir()
        (loose_skills / "dummy.txt").write_text("loose", encoding="utf-8")

        loose_agents = self.target_path / "agents"
        loose_agents.mkdir()
        (loose_agents / "dummy.txt").write_text("loose", encoding="utf-8")

        result = install_ultra_skill(self.target_path, clean_root=True)
        self.assertEqual(result["status"], "SUCCESS")

        # Loose folders should be gone
        self.assertFalse(loose_skills.exists())
        self.assertFalse(loose_agents.exists())

        # Proper .agents should be present
        self.assertTrue((self.target_path / ".agents" / "skills" / "ultra-skill").exists())
        self.assertTrue((self.target_path / ".agents" / "agents").exists())


if __name__ == "__main__":
    unittest.main()
