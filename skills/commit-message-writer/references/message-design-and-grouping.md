# Message Design and Commit Grouping

Make each message describe one coherent historical change. Optimize for future
maintainers, release automation, and accurate review rather than maximum detail.

## Conventional Commit Shape

```text
type(scope)!: imperative summary

Optional body explaining motivation and important behavior.

Optional-Key: value
BREAKING CHANGE: required migration or compatibility impact
```

The type is mandatory under the fallback convention. The scope is optional.
Use `!` only for a breaking supported contract and include the breaking-change
footer when migration detail is useful.

## Type Selection

- `feat`: adds a capability users or consumers can use.
- `fix`: corrects behavior that was wrong, broken, unsafe, or incompatible.
- `docs`: changes only documentation or examples.
- `refactor`: changes internal structure without intended behavior change.
- `test`: changes test coverage or test infrastructure without product behavior.
- `perf`: improves measured or clearly intended performance.
- `build`: changes compilation, packaging, artifact production, or build tools.
- `ci`: changes continuous integration, workflows, runners, or CI automation.
- `chore`: performs maintenance not accurately covered by another type.
- `style`: changes formatting only, without semantics.
- `revert`: reverses an earlier commit and identifies it in the body.

Prefer the most specific truthful type. Do not use `chore` to avoid deciding
whether a change is a feature, fix, build change, or CI change.

## Scopes

Use a scope when it helps identify the affected product area, package, service,
plugin, skill, workflow, or subsystem. Prefer repository-defined scopes. When no
scope policy exists, derive a stable domain name rather than a filename.

Good scopes include `terraform`, `router`, `api`, `cli`, `auth`, `deps`, or a
workspace package name. Avoid scopes such as `misc`, `files`, or a ticket number.
Omit the scope if the entire repository is the natural boundary.

## Titles

Use an imperative summary that completes the thought "This commit will..." after
the prefix:

```text
feat(skills): add TypeScript best practices
fix(terraform): disable locking for validation plans
ci(validation): validate plugin metadata on pull requests
docs(readme): explain marketplace installation
```

Name the outcome, not the editing activity. Prefer `add validation workflow`
over `update yaml files`. Avoid a trailing period, issue-only titles, vague
verbs such as `change` or `improve`, and title bodies pasted into the subject.

## Bodies and Footers

Use a body when the title cannot capture motivation, non-obvious behavior,
compatibility, operational ordering, migration, or important validation. Explain
why and what changed at the behavioral level. Do not inventory files or repeat
the title in a full sentence.

Reference tests only from evidence:

```text
Tests: uv run pytest
```

Use repository-required issue and release footers. For a breaking change:

```text
feat(config)!: replace legacy provider variables

BREAKING CHANGE: rename aws_role to deployment_role before upgrading.
```

## Planning Multiple Commits

Use commit-planning mode only for changes the user explicitly places in scope.
Inspect staged, unstaged, and untracked changes separately and preserve
dependencies between groups.

Group by coherent intent and reversibility:

- foundational capability before consumers;
- implementation with its directly supporting tests;
- generated artifacts with their source change when required;
- documentation with the behavior it documents when tightly coupled;
- release metadata and catalog integration after the underlying capability;
- unrelated refactors, fixes, formatting, or dependency updates separately.

A single commit may touch many files when they implement one atomic outcome. A
single file may contain hunks that belong to different commits. Recommend hunk
staging when necessary, but do not perform it without explicit authorization.

For each proposed group, return:

1. intent and dependency order;
2. included files or specific hunks;
3. proposed title and body;
4. validation evidence or a clearly labeled gap.

If splitting would make intermediate commits invalid or misleading, keep the
dependent changes together and explain why.
