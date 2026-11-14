"""Regression tests for the median() bug.

Original state: test_median_even_length FAILS against the buggy fixture.
After the minimal fix: all tests pass.
Run:  python -m unittest test_regression -v   (from this directory)
"""

import sys
import unittest
from pathlib import Path

# The fixture lives in fixture/ next to this test file.
sys.path.insert(0, str(Path(__file__).resolve().parent / "fixture"))

from stats import median  # noqa: E402


class MedianTests(unittest.TestCase):
    def test_median_even_length(self):
        # The reported bug: even-length input returns the upper middle element.
        self.assertEqual(median([1, 2, 3, 4]), 2.5)

    def test_median_odd_length_normal_case(self):
        self.assertEqual(median([3, 1, 2]), 2)

    def test_median_single_element_edge_case(self):
        self.assertEqual(median([7]), 7)

    def test_median_two_elements_edge_case(self):
        self.assertEqual(median([5, 10]), 7.5)

    def test_median_empty_input_edge_case(self):
        with self.assertRaises(ValueError):
            median([])


if __name__ == "__main__":
    unittest.main()
