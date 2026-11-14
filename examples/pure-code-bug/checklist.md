# Evaluation checklist — Eval A: pure-code bug

Fictional, self-contained fixture (`fixture/stats.py`). No real project code.

## Scenario

> `median([1, 2, 3, 4])` returns `3`. Expected `2.5`.

## Steps an agent following the `focused-bugfix` skill should produce

- [ ] **Observed vs expected** stated up front (returns 3 vs returns 2.5).
- [ ] **Smallest reproduction** recorded, from `fixture/`:
      `python -c "from stats import median; print(median([1,2,3,4]))"` → `3`.
- [ ] **Working tree checked**; unrelated changes untouched.
- [ ] **Reproduction before editing**; regression test `test_median_even_length` added and shown failing.
- [ ] Failure classified as a **real bug failure** (not missing tools or broken setup).
- [ ] **Minimal fix** only in the even branch of `median()` — no refactoring of the
      odd branch, no reformatting, no API change, no dependency added.
- [ ] **Original failing case** re-run → passes.
- [ ] **Normal case** (odd length) and **edge cases** (single element, two
      elements, empty input) actually run with results recorded.
- [ ] Report names changed files, actual outputs, and anything not run.

## Demonstrated result (fixture tests, disposable copy)

- Buggy fixture: 1 failure / 4 pass (`test_median_even_length` fails: 3 != 2.5).
- Disposable copy with minimal fix: 5/5 pass. Original fixture unchanged.

## Honesty requirements

- If the environment cannot run Python, the agent must report the blocker,
  not a fake pass.
- Any part not executed must be reported as not executed.
