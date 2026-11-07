# TypeScript Review Checklist

Review the highest-risk behavior first. Report concrete findings with file and
line references, impact, and a focused remediation.

## Correctness and Boundaries

- Are external values validated before entering typed domain code?
- Do types match runtime behavior for absence, nullability, errors, and async
  results?
- Are casts, non-null assertions, and `any` hiding an unproven invariant?
- Are discriminated unions handled exhaustively where missing a case is unsafe?
- Are configuration and secrets parsed once without truthiness mistakes or
  accidental logging?

## APIs and Modules

- Are exported contracts small, intentional, and compatible with existing
  consumers?
- Do `package.json`, `tsconfig`, imports, emitted extensions, and runtime module
  resolution agree?
- Are package exports and declaration files verified from the consumer view?
- Do barrel files, path aliases, or workspace imports create cycles or bypass
  public package boundaries?
- Are generated files changed through their source or generator?

## Async and Resources

- Is every promise awaited, returned, aggregated, or deliberately detached with
  error ownership?
- Is concurrency bounded and cancellation propagated where workload or I/O can
  outlive the request?
- Are timers, streams, subscriptions, servers, workers, and clients cleaned up
  on success, failure, and cancellation?
- Can shared mutable state race across awaits, requests, retries, or tests?
- Are thrown and caught values handled without relying on unstable message text?

## Tests and Tooling

- Do tests cover observable success, failure, boundary, cancellation, and
  cleanup behavior?
- Are mocks, globals, environment values, interceptors, and fake timers restored?
- Does a production build or consumer test verify behavior beyond `tsc`?
- Does the package manager match the existing lockfile and declared version?
- Were manifest and lockfile changes reviewed together without unrelated
  upgrades?

## GitHub Actions

- Does CI preserve frozen install, format, lint, type-check, test, then build
  order using repository-owned scripts?
- Are Node.js and package-manager versions explicit and supported?
- Are current actions lockfile-managed or full-SHA pinned?
- Are permissions minimal, caches reproducible, timeouts bounded, and stale CI
  runs cancelable?
- Are publish and deploy credentials excluded from pull-request workflows?
- Does the workflow follow
  [github-actions-ci.md](github-actions-ci.md) and
  `github-actions-best-practices`?

## Final Validation

Run the applicable repository commands for formatting, linting, type checking,
tests, and build. State anything not run and any runtime, browser, integration,
or generated-artifact behavior not verified.
