"""Fictional self-contained fixture: a tiny stats helper with one bug.

Bug: median() returns the wrong value for even-length inputs because it
returns the upper middle element instead of the average of the two middles.
"""

import statistics  # noqa: F401  (kept so the fixture is a realistic module)


def median(values):
    """Return the median of a non-empty list of numbers.

    Raises ValueError on an empty list.
    """
    if not values:
        raise ValueError("median() arg is an empty sequence")
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2:
        return ordered[mid]
    # BUG: returns the upper middle element instead of averaging the two
    # middle elements. median([1, 2, 3, 4]) returns 3; expected 2.5.
    return ordered[mid]
