# Review Checklist

## Dependency Integrity

- Every external action in new or substantially rewritten workflow code was
  resolved from its official repository during the current task.
- Actions use the latest stable compatible full release tag; no version came
  from memory, an old workflow, boilerplate, or an unverified example.
- Any action below the latest stable release has a documented product, runner,
  or interface compatibility constraint and uses the newest compatible release.
- An Actions lockfile is generated, reviewed, committed, and current where the
  repository has adopted one.
- Without a lockfile, or when the workflow is not onboarded to it, every
  external action uses a verified full 40-character commit SHA from the original
  repository with a release-tag comment. No mutable action ref remains.
- External reusable workflows use full commit SHAs.
- Dependabot covers the `github-actions` ecosystem.
- The update cadence matches review capacity and uses an explicit review-hours
  timezone when timing matters.
- Multiple ecosystems have separate entries and staggered schedules where
  simultaneous updates would create branch churn.
- Cooldowns, ecosystem-scoped groups, commit prefixes, and labels reflect the
  repository's dependency policy.
- Auto-approval is restricted to explicitly approved low-risk patch and minor
  updates; major upgrades remain subject to manual review by default.
- New third-party actions are necessary, maintained, and appropriately trusted.

## Security

- Events and checked-out refs do not cross an unintended trust boundary.
- `pull_request_target` never executes untrusted contribution code with secrets
  or write privileges.
- Workflow and job `permissions` are explicit and least-privileged.
- Untrusted context values are passed as data, not interpolated into scripts.
- Secrets are absent from logs, outputs, caches, artifacts, and untrusted jobs.
- Cloud authentication uses restricted OIDC trust where practical.
- Environments and approvals protect sensitive deployments.
- Self-hosted runners are not exposed to untrusted code without isolation.

## Correctness and Design

- Triggers, filters, conditions, and job dependencies match the intended graph.
- Shells, quoting, exit behavior, and working directories are explicit enough
  for the selected runners.
- Long logic lives in testable scripts; reuse uses the appropriate abstraction.
- Matrices contain equivalent variants and have intentional failure behavior.
- Caches are keyed from relevant lockfiles and contain no secrets.
- Artifacts have the right contents, retention, and trust assumptions.
- Deployments and replaceable runs use appropriate concurrency controls.
- Jobs and risky external operations have sensible timeouts.

## Validation

- YAML and Actions expressions pass the repository's linter or parser.
- Referenced scripts and reusable components exist and their tests pass.
- The lockfile check passes when lockfiles are used.
- The diff contains no accidental permission, trigger, runner, or secret changes.
- Any behavior requiring a live GitHub run is identified explicitly.
