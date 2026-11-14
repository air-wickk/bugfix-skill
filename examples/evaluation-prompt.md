# Pending behavioral evaluation — fresh OpenCode session

**Status: PENDING (not yet executed).** This file is the prompt for the
behavioral evaluation described in the README. It requires no new
credentials, paid services, or settings changes.

## Setup (disposable, local)

```sh
# 1. Copy the example into a disposable sandbox (NOT the original fixture)
mkdir -p _sandbox/.opencode/skills
cp -r skills/focused-bugfix   _sandbox/.opencode/skills/
cp -r examples/pure-code-bug  _sandbox/fixture-copy
cd _sandbox

# 2. Start a fresh OpenCode session here, then paste the prompt below.
```

## Prompt

```text
@focused-bugfix In fixture-copy/fixture/stats.py, calling
median([1, 2, 3, 4]) returns 3 but the docstring's contract implies 2.5.
Reproduce the bug, fix it minimally, and report what you ran and what you
did not run. Do not touch anything outside fixture-copy/.
```

## Pass criteria (compare against examples/pure-code-bug/checklist.md)

1. Reproduces before editing (shows the actual failing output `3`).
2. Adds/uses a regression test and shows it fail, then pass after the fix.
3. Classifies the failure as a real bug, not a broken environment.
4. Fix limited to the even-length branch; diff contains nothing else.
5. Reports normal + edge-case runs with real outputs, and any skipped check.
6. Original `examples/pure-code-bug/fixture/stats.py` remains byte-identical.

## Evidence to save if run

Save a sanitized transcript (no user paths beyond the sandbox, no secrets)
as `examples/evaluation-evidence.md`, with the session's diff and final
report. Until that file exists, the behavioral evaluation stays **pending**.
