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

## Release Automation

- Releases originate from one documented, reviewed branch and concurrent runs
  cannot publish competing versions.
- Semantic-version inputs match the repository's merge strategy, including
  squash-merge titles when they become the released commit subject.
- Existing version history has a verified baseline tag, and every distributed
  version source, release commit, tag, and GitHub Release agrees.
- A dedicated release GitHub App is preferred when practical, named for its
  narrow purpose, installed only on intended repositories, and granted no more
  than the permissions required by the chosen release model.
- A direct tag-and-release bot normally has only Metadata read and Contents
  read/write; broader permissions have concrete endpoint or workflow evidence.
- Package publication uses separate, preferably short-lived credentials rather
  than expanding the GitHub release bot.
- Release immutability is enabled when supported, and workflows with assets
  create a draft, attach and verify everything, then publish once.
- Published tags are never force-moved or reused; corrections receive a new
  version.
- Generated release commits cannot recursively start another release.

## Repository Rulesets

- Effective organization, repository, and legacy branch-protection rules were
  inspected together.
- The default branch blocks deletion and non-fast-forward updates and requires
  the intended pull-request reviews and thread resolution.
- Required status checks contain real, stable check identities; strict
  up-to-date enforcement is not paired with an empty check list.
- Every owned language or infrastructure domain has non-mutating formatting,
  lint or static analysis, and test gates, plus schema validation for schemas
  and schema-governed documents.
- Required checks always report a conclusive result for their triggering pull
  requests; path filters and skipped jobs cannot leave required checks pending.
- Allowed merge methods preserve the repository's commit-history and semantic
  versioning assumptions.
- Every bypass actor is identified by name and purpose, uses the narrowest
  bypass mode, and appears in rule insights when used.
- Exported numeric role and Integration IDs were verified in the target
  repository instead of copied by assumption.
- A separate `v*` tag ruleset restricts creation, deletion, and movement, with
  only the dedicated release App allowed to create releases.
- Tag rulesets protect release tags before publication and immutable releases
  protect the published tag and assets afterward.
- Required workflows support merge-group events before a merge queue is
  enabled.

## Repository Hygiene

- Merged head branches are deleted automatically unless a documented retention
  or deployment workflow requires them.
- Issues linked as closing issues are closed when their pull requests merge,
  and broad tracking issues are not linked as though one pull request completes
  all tracked work.
- Contributors with write access are always offered the update-branch control
  when a pull request falls behind its base branch.
- The team understands that update suggestions are not automatic updates, fork
  branch deletion depends on the fork's settings and access, and rulesets can
  prevent branch deletion.

## Validation

- YAML and Actions expressions pass the repository's linter or parser.
- Referenced scripts and reusable components exist and their tests pass.
- The lockfile check passes when lockfiles are used.
- The diff contains no accidental permission, trigger, runner, or secret changes.
- Any behavior requiring a live GitHub run is identified explicitly.
