---
name: github-actions-best-practices
description: Creates, reviews, refactors, and secures GitHub Actions workflows, reusable workflows, and custom or composite actions. Use for files under .github/workflows, action.yml or action.yaml, action versioning, workflow dependency lockfiles, SHA pinning, permissions, OIDC, Dependabot, caching, matrices, concurrency, artifacts, and CI/CD workflow design.
metadata:
  author: JSChronicles
  version: "0.2.1"
---

# GitHub Actions Best Practices

Build workflows that are secure, reproducible, understandable, and economical
to operate. Preserve repository-local policy and make the smallest change that
achieves the requested outcome.

## Start Here

1. Read repository instructions and inspect the targeted workflows, action
   metadata, dependency policy, and existing conventions.
2. Identify the trust boundary: event, actor, checked-out ref, token
   permissions, secrets, environments, and external dependencies.
3. Choose the smallest suitable abstraction: a workflow step, repository
   script, composite action, reusable workflow, or published action.
4. Secure dependencies and privileges before optimizing performance.
5. Validate syntax and behavior with the project's existing tools and a
   proportionate set of workflow checks.

## Core Rules

- For every new or substantially rewritten workflow, resolve each external
  action's latest stable release from its official repository at implementation
  time and use the full release tag. Never copy an action version from memory,
  an old workflow, generated boilerplate, or a documentation example without
  verifying it first.
- Treat an action that is behind its latest stable compatible release as a
  defect in newly authored workflow code. If the newest stable release is
  incompatible with the target GitHub product, runner, or required interface,
  use the newest compatible release and document the exact constraint.
- Do not silently fall back to a remembered major when release verification is
  unavailable. Report the verification limitation instead of presenting a
  potentially stale workflow as complete.
- Use current supported runner images. Verify runner and action compatibility
  from official documentation; do not guess.
- Prefer GitHub Actions workflow dependency lockfiles when the repository and
  GitHub plan support them. Generate, review, and commit
  `.github/workflows/actions.lock`; never edit it manually.
- When an Actions lockfile is absent, unsupported, or has not onboarded the
  workflow, pin every external action to a verified full 40-character commit
  SHA from the action's original repository. This is the mandatory default for
  unlocked workflows, not an optional hardening step. Keep the release tag in a
  comment beside the SHA so humans and update tooling can identify the version.
- Pin external reusable workflows to a full commit SHA even when an Actions
  lockfile exists; reusable workflow calls are not covered by that lockfile.
- Configure Dependabot for the `github-actions` ecosystem so action references
  and matching lock entries stay current. Review updates rather than silently
  accepting moved or rewritten refs.
- Declare `permissions` explicitly and grant the minimum access needed. Prefer
  job-level permissions when jobs need different privileges.
- Prefer OIDC and short-lived cloud credentials to stored long-lived keys.
  Grant `id-token: write` only to jobs that request an identity token, and
  restrict the cloud trust policy to the intended repository, ref, workflow,
  and environment.
- Treat pull request content, branch names, issue text, and other event context
  as untrusted input. Pass values through environment variables instead of
  interpolating expressions directly into shell scripts.
- Do not use `pull_request_target` to check out and execute untrusted pull
  request code with secrets or a write-capable token. Use `pull_request` for
  untrusted CI unless a carefully isolated privileged workflow is required.
- Prefer repository scripts for substantial or testable logic. Avoid adding a
  marketplace action when a short, clear command or existing tool is enough.
- Use caches for regenerable dependencies and build intermediates; use
  artifacts for outputs that must be retained or passed between jobs. Never put
  secrets in either, and treat restored cache content as untrusted.
- Add concurrency controls to deployments and replaceable runs, and add
  sensible timeouts to jobs or steps that could hang or consume costly runners.
- Keep workflows focused. Use matrices for genuinely equivalent variants, not
  as a substitute for clear job boundaries or materially different procedures.

## Dependency Decision

Use this order:

1. **Actions lockfile available and adopted:** use readable release refs in
   workflows, generate the lockfile with `gh actions-lock`, review identity and
   commit changes, and commit both workflow and lockfile updates.
2. **No lockfile or workflow not onboarded:** use a verified full 40-character
   commit SHA for every external action, plus a release comment, and enable
   Dependabot. Do not leave mutable branch or tag refs in an unlocked workflow.
3. **External reusable workflow:** always use a full commit SHA. The caller's
   Actions lockfile does not pin reusable workflow calls.

Read [dependency-security.md](references/dependency-security.md) before adding,
updating, pinning, locking, or reviewing actions and reusable workflows.

## Design Decisions

Read [workflow-design.md](references/workflow-design.md) when choosing between
inline commands, scripts, composite actions, reusable workflows, matrices,
caches, artifacts, or concurrency behavior.

Read [workflow-security.md](references/workflow-security.md) when a workflow
handles pull requests, secrets, deployments, cloud access, elevated token
permissions, self-hosted runners, or untrusted input.

For a review or final quality pass, use
[review-checklist.md](references/review-checklist.md).

## Validation

- Parse and lint changed YAML with repository-standard tools such as
  `actionlint`, plus any local schema or policy checks.
- Run scripts and tests outside the workflow when practical.
- If a lockfile is present, regenerate it after dependency changes and run
  `gh actions-lock --verify` for a frozen network-backed check, or
  `gh actions-lock --verify-local` for an offline coverage check.
- Inspect the diff for permissions, triggers, expression interpolation,
  dependency identity, secret exposure, and unintended changes in runner or
  deployment behavior.
- Report checks that could not be run and any assumptions that require a live
  GitHub run to confirm.

## Review Output

Lead with concrete findings ordered by severity. Include the workflow and job or
step, explain the security or operational impact, and suggest the smallest
practical correction. Avoid style-only findings unless they materially improve
maintainability or prevent mistakes.
