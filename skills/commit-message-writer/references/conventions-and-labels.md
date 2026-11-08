# Repository Conventions and Labels

Discover repository policy before applying the fallback Conventional Commit
mapping. Label names are not universal, and not every labeler reads commits.

## Evidence Precedence

Use the strongest available evidence:

1. Explicit user instruction.
2. Enforced configuration.
3. Labeler rules and label descriptions.
4. Contribution or release documentation.
5. Consistent recent commit history.
6. Fallback mapping from this reference.

Conflicting automated configuration is more important than a few inconsistent
historical titles. Report a material conflict instead of guessing which system
will win.

## Local Discovery

Inspect relevant files when present:

- `commitlint.config.*` and `.commitlintrc*`;
- Commitlint entries in `package.json`;
- Semantic Release, Release Please, Changesets, or equivalent release config;
- `.github/labeler.yml`, `.github/labeler.yaml`, and label-related workflows;
- `.github/labels.yml` or `.github/labels.yaml`;
- `.github/release-drafter.yml` or `.github/release-drafter.yaml`;
- pull request templates and contribution guidance;
- scripts that parse commit subjects, scopes, or footers.

Inspect workflow implementation rather than inferring behavior from a filename.
Determine whether automation matches commit titles, pull request titles, paths,
branches, authors, or manually assigned labels.

Use a bounded sample of recent commit subjects to identify style:

```console
git log -n 50 --pretty=format:%s
```

Do not use history as permission to repeat weak messages or violate current
enforced configuration.

## Remote Label Discovery

When local files do not define the available labels and authenticated GitHub CLI
access is already available, use a read-only query such as:

```console
gh label list --limit 100 --json name,description,color
```

Treat a non-empty label description as stronger evidence than an inferred name.
If descriptions are missing, compare label names with labeler and release
configuration. Do not mutate labels or repository settings while drafting a
message.

## Fallback Type and Label Mapping

Use this mapping only when the repository provides no stronger policy:

| Commit type | Primary intent | Likely labels |
| --- | --- | --- |
| `feat` | Add a user-visible capability | `enhancement`, `feature` |
| `fix` | Correct incorrect behavior | `bug`, `bugfix` |
| `docs` | Change documentation only | `documentation`, `docs` |
| `test` | Add or correct tests | `tests`, `testing` |
| `ci` | Change CI, workflows, or automation | `ci`, `github-actions`, `automation` |
| `build` | Change builds, packaging, or build tooling | `build`, `packaging` |
| `chore` | Perform repository maintenance not covered elsewhere | `maintenance`, `chore` |
| `refactor` | Restructure code without intended behavior change | `refactor`, `technical-debt` |
| `perf` | Improve performance | `performance` |
| `style` | Make formatting-only changes | `style`, `formatting` |
| `revert` | Revert an earlier commit | `revert` |
| `fix(security)` | Correct a security weakness | `security` |
| `type!` | Break a supported contract | `breaking-change` |

The mapping describes likely semantics, not guaranteed automation. A path-based
labeler may assign `documentation` from changed files regardless of a `docs:`
prefix. Keep the commit type truthful even when labeling uses another signal.

## Dependency Changes

Choose dependency types from intent:

- `build(deps)` for build tooling or dependencies that directly define the
  build and packaging system;
- `chore(deps)` for routine dependency maintenance;
- `fix(deps)` when the dependency change directly corrects broken or vulnerable
  behavior;
- `ci(deps)` for GitHub Actions and CI-only dependencies.

Follow a repository's automated dependency-update convention when it defines
one. Do not label all dependency changes `chore` without inspecting their role.
