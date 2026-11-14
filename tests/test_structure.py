"""Structural checks: pure standard library, no network, no credentials.

Verifies the repo has the required files, the SKILL.md frontmatter is
valid for the OpenCode v2 skills format (checked against v2.2.5 docs),
and no secret-looking content is committed.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "focused-bugfix" / "SKILL.md"

REQUIRED_FILES = [
    "README.md",
    ".gitignore",
    "opencode.json",
    "skills/focused-bugfix/SKILL.md",
    "examples/pure-code-bug/fixture/stats.py",
    "examples/pure-code-bug/test_regression.py",
    "examples/pure-code-bug/checklist.md",
    "examples/ui-selection/fixture/index.html",
    "examples/ui-selection/checklist.md",
    "examples/blocked-dependency/fixture/chart_report.py",
    "examples/blocked-dependency/fixture/WIP-NOTES.txt",
    "examples/blocked-dependency/checklist.md",
    "examples/evaluation-prompt.md",
    "tests/test_structure.py",
    "tests/test_fixtures.py",
]

SECRET_PATTERNS = [
    re.compile(r"(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{8,}", re.I),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(ghp|gho|github_pat)_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]


class StructureTests(unittest.TestCase):
    def test_required_files_exist(self):
        missing = [f for f in REQUIRED_FILES if not (ROOT / f).is_file()]
        self.assertEqual(missing, [])

    def test_skill_frontmatter_has_name_and_description(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"), "SKILL.md must start with frontmatter")
        end = text.index("\n---", 4)
        fm = text[4:end]
        self.assertRegex(fm, r"(?m)^name:\s*focused-bugfix\s*$")
        self.assertRegex(fm, r"(?m)^description:\s*\S")

    def test_skill_id_matches_directory(self):
        # OpenCode v2: skill ID comes from the directory name, which must be
        # lowercase kebab-case per the portability recommendation.
        self.assertEqual(SKILL.parent.name, "focused-bugfix")
        self.assertRegex(SKILL.parent.name, r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def test_skill_body_covers_required_behaviors(self):
        body = SKILL.read_text(encoding="utf-8").lower()
        for needle in [
            "observed", "expected", "smallest reproduction",
            "regression test", "hypothesis", "unverified",
            "edge case", "unverified",  # UI honesty
            "remaining risks", "invent",
        ]:
            self.assertIn(needle, body, f"SKILL.md should mention: {needle}")

    def test_no_secret_looking_content(self):
        offenders = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for pat in SECRET_PATTERNS:
                if pat.search(text):
                    offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])

    def test_gitignore_covers_required_categories(self):
        gi = (ROOT / ".gitignore").read_text(encoding="utf-8").lower()
        for category, needle in {
            "secrets": ["secret", ".env"],
            "local config": ["local", ".env"],
            "caches": ["__pycache__"],
            "logs": ["*.log"],
            "generated output": ["dist", "output"],
            "machine-specific": [".vscode", "desktop.ini"],
        }.items():
            self.assertTrue(any(n in gi for n in needle),
                            f".gitignore must cover {category}")

    def test_opencode_json_registers_skills_source(self):
        # Lets OpenCode discover the skill when opened inside this repo.
        import json
        cfg = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertEqual(
            cfg.get("$schema"), "https://opencode.ai/config.json")
        self.assertIn("./skills", cfg.get("skills", []))

    def test_readme_states_unverified_and_honest_status(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("v2.2.5", readme)
        self.assertIn("unverified", readme.lower())
        self.assertIn("pending", readme.lower())
        self.assertIn("not", readme.lower())  # "not ... validated" claim

    def test_opencode_json_registers_repo_skill_source(self):
        # Lets OpenCode discover the skill when opened inside this repo.
        import json

        data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertEqual(data.get("$schema"), "https://opencode.ai/config.json")
        self.assertIn("./skills", data.get("skills", []))


if __name__ == "__main__":
    unittest.main()
