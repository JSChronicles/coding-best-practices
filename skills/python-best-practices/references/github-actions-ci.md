# Python GitHub Actions CI

Use this reference when creating or reviewing GitHub Actions that format, lint,
type-check, build, or test Python. Also apply `github-actions-best-practices` so
the workflow uses current action releases, an Actions lockfile or full SHA pins,
least-privilege permissions, concurrency, and timeouts.

Start from the adaptable [Python workflow template](../assets/github-workflow.yaml)
when a new workflow is requested. Replace every placeholder, remove inapplicable
steps, and never deliver the template with unresolved dependency refs.

Reference implementations:

- `JSChronicles/foundry-python-template/.github/workflows/ruff.yaml`
- `JSChronicles/foundry-python-template/.github/workflows/pytest.yaml`

Inspect their current versions when useful, but copy the testing intent rather
than action refs or repository-specific paths.

## Baseline Workflow Shape

Use pull-request validation, pushes to the protected integration branch, and
manual dispatch when maintainers need it. Start with `contents: read`, cancel
stale validation runs for the same pull request or branch, and give each job a
reasonable timeout.

Prefer separate lint and test jobs when independent status checks or parallel
feedback are useful. A small repository may use one job when setup cost exceeds
the value of separation.

### Quality Job

1. Check out without persisted credentials.
2. Install the repository's package manager and declared Python version.
3. Synchronize the locked development environment.
4. Run the configured formatter in check mode.
5. Run the configured linter and type checker.

For a uv and Ruff project, the command sequence is normally:

```console
uv sync --locked --all-extras --all-groups
uv run ruff format --check .
uv run ruff check --output-format=github .
```

Add the repository's type checker, such as `uv run ty check` or
`uv run mypy`, only when it is configured. Do not invent a second lint or type
configuration in workflow YAML.

### Test and Build Job

1. Install the project from its lockfile.
2. Run the full automated test suite with the repository's coverage policy.
3. Build distributions for installable projects.
4. Smoke-test the built artifact rather than only the source checkout.

Typical commands are:

```console
uv sync --locked --all-extras --all-groups
uv run pytest --cov
uv build
```

For a command-line package, install the built wheel into an isolated environment
and run `--version`, `--help`, or a safe representative command. Avoid setting
`PYTHONPATH` merely to make an incorrectly packaged project importable.

## Python Versions and Runners

Read the supported Python range from `pyproject.toml`. Test the declared primary
version. Add a matrix for the minimum and latest supported versions when the
project promises multi-version compatibility; do not create a matrix for
versions the package does not claim to support.

Use a current supported runner image. If a container is used, pin its image by
digest and keep the readable tag in a comment or dependency update policy. Do
not assume a mutable `python:latest` or `python:X.Y-slim` tag is reproducible.

## Caching and Artifacts

Use the package manager's supported cache integration and key it from the lock
file and relevant interpreter/platform data. Caches must contain only
regenerable data and no credentials. Upload coverage, test, or build artifacts
only when another job or reviewer consumes them, with intentional retention.

## Workflow Review

- Action releases were resolved during the current task and are locked or
  full-SHA pinned.
- Python and dependency versions come from project metadata and lockfiles.
- Formatting uses check mode and never rewrites the branch in ordinary CI.
- Tests fail the job on failures and do not depend on machine-specific state.
- Build and smoke tests exercise the distributable artifact when applicable.
- Secrets and write permissions are absent from untrusted pull-request jobs.
