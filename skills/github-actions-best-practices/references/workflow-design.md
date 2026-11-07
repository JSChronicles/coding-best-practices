# Workflow Design

## Choose the Right Reuse Boundary

- **Inline `run` step:** a short, readable command closely tied to one job.
- **Repository script:** substantial, testable, or locally reusable logic. This
  is usually better than a long YAML shell block.
- **Composite action:** a reusable sequence of steps that runs as part of one
  caller job and should behave like an action.
- **Reusable workflow:** one or more reusable jobs with their own runners,
  permissions, environments, inputs, outputs, and controlled secrets.
- **Published action:** stable behavior intended for reuse across repositories
  with versioning, documentation, tests, and a maintenance commitment.

Do not publish an action just to avoid a few clear commands. Do not hide complex
business logic inside workflow YAML when a normal script can be tested more
directly.

## Workflow Structure

- Give workflows, jobs, and important steps descriptive names.
- Keep triggers narrow and use path or branch filters only when their skipped
  behavior is understood.
- Use job dependencies to express the actual execution graph.
- Pass small values through outputs and files or build products through
  artifacts.
- Define defaults once when they are genuinely shared, but keep security-
  sensitive permissions and environments visible near the privileged job.
- Use explicit shell settings and fail on errors. Avoid shell-specific syntax
  without declaring or accounting for the runner shell.

## Matrices

Use a matrix when each variant performs the same procedure over supported
versions, operating systems, or configurations. Keep matrix dimensions bounded
and intentional. Use `include` for a small number of exceptions; split jobs when
variants have meaningfully different steps, permissions, or failure policy.

Choose `fail-fast` deliberately. Disable it when complete compatibility results
matter; keep it when a failure makes the remaining expensive variants useless.
Use `continue-on-error` only for explicitly experimental variants and make their
status visible.

## Caches and Artifacts

Use a cache for dependencies and intermediates that can be regenerated. Build
keys from the operating system, relevant toolchain, and lockfile or dependency
hash. Provide restore prefixes only when stale partial matches are safe.

Use artifacts for test reports, logs, packages, provenance, or outputs passed to
another job. Set retention intentionally for sensitive or large artifacts.

Never store secrets in either. Cache content may originate from less-trusted
runs, so never execute restored content as trusted merely because it came from
the cache.

## Concurrency, Timeouts, and Retries

Use concurrency groups to prevent overlapping deployments and to cancel stale,
replaceable validation runs. Include the environment, branch, or pull request in
the key when those executions must remain independent.

Set job or step timeouts based on expected duration and runner cost. Avoid blind
retries that hide deterministic failures. Retry only operations known to be
transient, with a bounded count and clear failure output.

## Maintainability and Portability

Use repository variables for non-secret values that legitimately vary by
environment. Avoid duplicating constants across many workflows. Pin tool
versions through the ecosystem's normal manifest or lockfile where possible.

Consider GitHub Enterprise Server compatibility before adopting recently added
syntax, hosted runner labels, or Actions features. Document any requirement on a
specific GitHub product or version.
