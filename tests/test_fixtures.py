"""Executable fixture tests: standard library only, no network.

Eval A — demonstrates the median() bug failing on the original fixture,
then proves a minimal fix on a DISPOSABLE copy (original preserved).

Eval C — executes the blocked-dependency fixture and asserts it genuinely
fails with ModuleNotFoundError (evidence a correct agent report must
describe a blocker, not a pass).
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"

BUGGY = '''    # BUG: returns the upper middle element instead of averaging the two
    # middle elements. median([1, 2, 3, 4]) returns 3; expected 2.5.
    return ordered[mid]
'''
FIXED = '''    return (ordered[mid - 1] + ordered[mid]) / 2
'''


def run_unittest(workdir: Path):
    """Run test_regression.py in workdir; return CompletedProcess."""
    return subprocess.run(
        [sys.executable, "-m", "unittest", "test_regression", "-v"],
        cwd=workdir, capture_output=True, text=True, timeout=120,
    )


class PureCodeBugTests(unittest.TestCase):
    """Eval A."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="bugfix-skill-eval-"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _materialize(self, name: str, apply_fix: bool) -> Path:
        workdir = self.tmp / name
        shutil.copytree(EXAMPLES / "pure-code-bug", workdir)
        if apply_fix:
            source = (workdir / "fixture" / "stats.py").read_text(encoding="utf-8")
            self.assertIn(BUGGY, source)
            (workdir / "fixture" / "stats.py").write_text(
                source.replace(BUGGY, FIXED), encoding="utf-8")
        return workdir

    def test_a1_original_fixture_still_buggy(self):
        """The committed fixture is unchanged and still fails: the bug exists."""
        workdir = self._materialize("buggy-copy", apply_fix=False)
        result = run_unittest(workdir)
        self.assertEqual(result.returncode, 1, "buggy fixture must fail tests")
        self.assertIn("test_median_even_length", result.stderr)
        self.assertIn("2.5", result.stderr)

    def test_a2_minimal_fix_makes_disposable_copy_pass(self):
        """Applying only the one-line fix to a disposable copy: 5/5 pass."""
        workdir = self._materialize("fixed-copy", apply_fix=True)
        result = run_unittest(workdir)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK", result.stderr)

    def test_a3_original_fixture_preserved(self):
        """The disposable copies must not touch the committed fixture."""
        original = (EXAMPLES / "pure-code-bug" / "fixture" / "stats.py").read_text(
            encoding="utf-8")
        self.assertIn(BUGGY, original)
        self.assertNotIn("return (ordered[mid - 1] + ordered[mid]) / 2", original)


class BlockedDependencyTests(unittest.TestCase):
    """Eval C: the blocker must be real, reportable, and reproducible."""

    def test_c1_fixture_reports_missing_dependency(self):
        result = subprocess.run(
            [sys.executable, "-c",
             "from chart_report import render_chart; render_chart([1, 2, 3])"],
            cwd=EXAMPLES / "blocked-dependency" / "fixture",
            capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("ModuleNotFoundError", result.stderr)
        self.assertIn("chartpainter", result.stderr)

    def test_c2_unrelated_change_is_present_and_untouched_by_tests(self):
        note = EXAMPLES / "blocked-dependency" / "fixture" / "WIP-NOTES.txt"
        text = note.read_text(encoding="utf-8")
        self.assertIn("DO NOT TOUCH", text)


if __name__ == "__main__":
    unittest.main()
