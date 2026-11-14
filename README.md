# bugfix-skill

An [OpenCode](https://opencode.ai) skill that turns a bug report into a small, evidence-backed fix: reproduce the defect, pin it with a regression test, apply the minimal patch, then report what was and was not tested.

Status: this is a new, AI-assisted personal workflow sample. It has not been used on real projects and has not been validated in use. The examples are fictional fixtures built for evaluation.

## Compatibility

Written for the OpenCode v2 skills format, checked against OpenCode v2.2.5:

- Project skills live in `.opencode/skills/<skill-id>/` as a folder containing `SKILL.md` with `name` and `description` frontmatter. Matches the v2.2.5 docs.
- The skill ID comes from the directory name (`focused-bugfix`), not the frontmatter name. Documented v2 behavior.
- Supporting files next to `SKILL.md` are read on demand. Documented behavior.

Anything else, including other OpenCode versions and other agents' skill loaders, is unverified here.

Verified on the machine that produced this repository (OpenCode v2.2.5): with the skill folder copied into a test project's `.opencode/skills/`, the server API (`GET /api/skill`) listed the skill by ID `focused-bugfix` and returned its body with the frontmatter stripped. The same check passes inside this repository through the `opencode.json` source registered below. The full behavioral evaluation, where an agent follows the skill end to end on a fixture, is still pending; see Evaluation.

## Installation

Copy the skill folder into a project that uses OpenCode. Do not install globally, and do not modify other projects.

```sh
# from your project root
mkdir -p .opencode/skills
cp -r /path/to/bugfix-skill/skills/focused-bugfix .opencode/skills/
```

OpenCode discovers it automatically. No configuration, credentials, or network access needed.

Alternatively, if you open OpenCode inside a clone of this repository, the repo's `opencode.json` (`"skills": ["./skills"]`) makes the skill discoverable there directly, so you can try it without copying anything.

## Usage

In an OpenCode session inside a project, invoke the skill directly:

```text
@focused-bugfix The Export CSV button produces an empty file when the table has exactly one row. Fix it.
```

The agent should then reproduce the bug with a one-row table, add a failing test, make the smallest fix, rerun the one-row case plus a multi-row case and an empty-table case, and report actual results. Reports produced under this skill state the bug, the evidence for its cause, the changed files, the checks run with their real output, the checks skipped and why, and remaining risks. It never invents a pass.

## Limitations

- The skill is instructions, not enforcement. It guides the model but cannot guarantee compliance.
- It cannot run a browser. UI behavior is either checked manually or marked unverified.
- It does not override the host project's permissions, secrets handling, or deployment policy.
- Verified against OpenCode v2.2.5 only.

## Evaluation

Three scenarios live in `examples/`, each with a checklist:

- `pure-code-bug/`: a repeatable failing input, a regression test, and normal and edge cases, demonstrated on a disposable copy while the original fixture stays untouched.
- `ui-selection/`: expected behavior and repeated-switch manual checks for a fictional tab-switching bug. The UI behavior is explicitly marked untested.
- `blocked-dependency/`: a missing dependency scenario where the agent must report the blocker instead of faking a pass, and must leave an unrelated change untouched.

Run the structural and fixture checks (standard library only, no network):

```sh
python -m unittest discover -s tests -v
```

A behavioral evaluation in a fresh OpenCode session is pending. The prompt and pass criteria are in `examples/evaluation-prompt.md`; no credentials or paid services are required to run it.

Verified on OpenCode v2.2.5 (this machine): the installed CLI lists `focused-bugfix` for a disposable project with the skill copied into `.opencode/skills/`, and for this repository via its `opencode.json` source, using `GET /api/skill` with the location parameter. The loaded content is the `SKILL.md` body without frontmatter. That confirms discovery and loading, not model behavior; the behavioral evaluation above stays pending.

## What is in this repository

```text
bugfix-skill/
├── README.md
├── opencode.json                      registers ./skills for OpenCode opened here
├── skills/focused-bugfix/SKILL.md     the skill itself
├── examples/                          fictional fixtures and evaluation checklists
└── tests/                             structural checks and executable fixture tests
```

## License

None yet. One will be added only with the owner's approval.
