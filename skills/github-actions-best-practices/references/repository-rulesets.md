# Repository Rulesets

Use rulesets to make the repository's review, merge, tag, and automation policy
explicit. Start with the smallest enforceable policy that protects the default
branch, then add required checks and release-tag controls backed by workflows
that actually exist.

## Inspect Effective Policy First

Before creating or changing a ruleset, inspect:

- repository- and organization-level rulesets targeting the repository;
- legacy branch protection that may overlap with rulesets;
- the default branch, merge methods, merge queue, CODEOWNERS file, and actual
  status-check names;
- GitHub Apps, roles, teams, users, and deploy keys on every bypass list; and
- release automation that must create a version commit or `v*` tag.

Organization and repository rulesets aggregate. A repository ruleset can add
restrictions but cannot weaken an applicable organization rule. Review the
effective rules through the repository's rules view rather than evaluating one
JSON export in isolation.

Ruleset changes, bypass grants, and imports are external administrative
mutations. Confirm the exact repository or organization scope before applying
them. Prefer evaluate mode and inspect rule insights before activating a broad
organization policy when the GitHub plan supports evaluation.

## Minimum Default-Branch Ruleset

Target `~DEFAULT_BRANCH` so the policy follows an intentional default-branch
rename. For a repository developed through pull requests, a practical minimum
active ruleset includes:

- block deletion;
- block non-fast-forward updates;
- require a pull request before merging;
- require at least one approving review;
- dismiss stale approvals when new commits are pushed;
- require approval of the most recent reviewable push by someone other than the
  pusher;
- require all review threads to be resolved; and
- require named status checks that cover the repository's actual validation.

Require CODEOWNERS review only when the repository has an accurate, maintained
CODEOWNERS file and the affected paths should have designated ownership. An
empty required-reviewer list is not a substitute for CODEOWNERS or a review
count.

The required-status-check rule must contain at least one real check. Selecting
"require branches to be up to date" while leaving `required_status_checks`
empty does not create a CI gate; GitHub requires a defined check for that option
to take effect. Record exact, stable check names after a successful workflow
run. Rename workflow jobs deliberately because required checks depend on the
reported check identity.

Choose allowed merge methods to match the versioning and audit model. If squash
titles drive semantic versioning, validate pull-request titles and avoid
presenting merge and rebase as equivalent paths unless their commit histories
produce the same release decision.

## Recommended Policy Variants

Use one of these named variants as the starting policy. The names describe the
security behavior rather than copying a repository-specific ruleset name such
as `main`.

### `reviewed-default-branch`

This is the default for repositories developed entirely through pull requests:

- target `~DEFAULT_BRANCH`;
- use active enforcement after evaluation or focused testing;
- block deletion and non-fast-forward updates;
- require the review behavior in the minimum ruleset above;
- require the repository's actual status checks; and
- configure no bypass actors.

If the repository does not have stable CI checks yet, omit the required-status-
checks rule temporarily. Do not add the rule with an empty array and describe
the branch as CI-protected. Add the rule when at least one successful check name
is known.

### `reviewed-default-branch-with-release-bot`

Use this variant only when direct release automation must push a generated
version commit to the default branch:

- start with every rule from `reviewed-default-branch`;
- add exactly the dedicated `<project>-release-bot` or
  `<ecosystem>-release-bot` GitHub App as an Integration bypass actor;
- use `always` only because this release model deliberately pushes without a
  pull request; and
- keep unrelated Apps, repository roles, teams, and users off the bypass list.

Add the App through GitHub's bypass picker and confirm its displayed name before
activation. Do not publish a portable JSON example containing the App's numeric
Integration ID. The number identifies one specific GitHub App and is unsafe to
guess or copy as a generic placeholder.

If another narrowly scoped App must push directly for a separate workflow,
document it as its own policy extension rather than silently folding it into
the release-bot example. Prefer separate purpose-specific Apps over one
overprivileged automation bot.

## Bypass Actors

Treat bypass as privileged production access:

- prefer no human bypass for routine development;
- use `pull_request` bypass for a human role or team when emergency merges must
  retain a pull-request and audit trail;
- use `always` only for an automation identity that must push directly, such as
  a narrowly scoped release App creating a generated version commit; and
- never grant broad repository administration to a bot merely to bypass rules.

Verify every actor by name and purpose in the GitHub UI before activation.
Exported rulesets encode repository roles and GitHub Apps as numeric actor IDs;
those IDs are not self-describing and may not be portable to another account or
repository. Do not infer that an `Integration` actor is the intended release bot
from its number, and do not import a `RepositoryRole` actor without confirming
which role GitHub displays.

Review rule insights and audit entries for bypass use. An `always` bypass means
the actor can bypass every rule in that ruleset, not only the pull-request rule
that motivated the exception.

## Release Tag Ruleset

Create a separate active tag ruleset for release tags, normally matching
`refs/tags/v*` or the repository's documented tag format. A useful baseline is:

- restrict creation to bypass actors;
- block deletion;
- block non-fast-forward updates; and
- allow the dedicated release GitHub App to bypass so it can create the tag.

Do not add general administrator, maintainer, or workflow bypass merely for
convenience. Verify the release App's installation scope and keep its repository
permission at Contents read/write for direct version commits, tags, and GitHub
Releases.

Tag rulesets and immutable releases cover different states. The tag ruleset
controls who may create or change a matching tag before and during publication.
Release immutability locks the associated tag and assets after the GitHub
Release is published. Use both when supported.

## Required Checks and Merge Queues

- Cover every owned language or infrastructure domain present in the change.
  The baseline categories are formatting in check mode, lint or static
  analysis, automated tests, and schema validation when schemas or
  schema-governed documents exist. Add type checking, compilation, security
  scanning, documentation generation, or artifact smoke tests when they are
  maintained parts of that domain's quality contract.
- Formatting checks must fail on a diff without rewriting the pull-request
  branch. Lint and test jobs must propagate a nonzero exit status instead of
  reporting findings while succeeding.
- Use the matching domain skill to select exact tools, versions, matrices, and
  commands. GitHub Actions owns orchestration and required-check identity; the
  language or infrastructure skill owns validation semantics.
- For Python, normally require the configured formatter in check mode, the
  configured linter, tests, and a configured type checker when the project uses
  one.
- For PowerShell, normally require formatter comparison, PSScriptAnalyzer, and
  Pester. Add generated-help or documentation validation when the module owns
  those artifacts.
- For Terraform, normally require `terraform fmt -check -diff -recursive`,
  initialization suitable for validation, and `terraform validate`. Add
  `terraform test`, TFLint, security scanning, documentation validation, and a
  review plan when the repository maintains those policies.
- Validate JSON, YAML, OpenAPI, JSON Schema, plugin manifests, workflow files,
  or other structured documents with their authoritative parser or schema.
  Validate representative documents against a changed schema as well as
  validating the schema itself.
- Require checks that exercise the merge result users will receive, including
  skill validation, tests, linting, security policy, or artifact builds that are
  genuine merge gates.
- Do not require optional, path-filtered, or event-specific checks that can
  remain permanently pending when a pull request does not match their trigger.
- In a mixed-language repository, either make each required workflow report a
  deliberate success when its domain is unchanged or require one stable
  aggregate check that depends on every applicable domain job. Do not mark a
  skipped language check as required unless GitHub will still receive a
  conclusive result.
- Keep required check names unique across workflows and apps so GitHub cannot
  accept an unintended producer with the same name.
- Treat names such as `ruff` and `pytest` as project-specific examples, not
  portable defaults. They are appropriate only when those exact checks are
  emitted by the target repository's trusted workflow.
- When strict status checks are enabled, verify the repository's update burden
  is acceptable. Use a merge queue when available and appropriate for a busy
  branch rather than repeatedly asking contributors to update manually.
- Ensure required workflows support the merge-group event before enabling a
  merge queue; otherwise queued changes may never receive their checks.

## Repository Hygiene Defaults

Rulesets protect refs and merge policy, but several repository-level settings
reduce routine cleanup and keep pull requests moving. For an active repository
developed through pull requests, enable these defaults under repository
**Settings**:

- **Automatically delete head branches** removes a merged pull request's head
  branch after the merge, reducing stale branches and accidental reuse. A
  branch protection rule or ruleset can prevent deletion. For pull requests
  from forks, GitHub uses the setting on the fork and also requires the person
  merging to have write access to that fork.
- **Auto-close issues with merged linked pull requests** closes an issue when a
  pull request explicitly linked to it is merged. Do not link a broad tracking
  issue as the closing issue for one partial pull request; use sub-issues or a
  narrower implementation issue instead.
- **Always suggest updating pull request branches** makes the update-branch
  control available to people with write access whenever a head branch is
  behind its base branch. This offers an update; it does not update branches
  automatically and does not replace strict required checks or a merge queue.

Treat these as defaults rather than unconditional requirements. Retain merged
branches only when a documented audit, deployment, or support workflow needs
them. If one merged pull request does not complete a linked issue, model the
relationship without making that issue the pull request's closing issue.

These settings are separate from ruleset JSON exports. Review them when
onboarding, templating, or auditing a repository instead of assuming a ruleset
import configured them.

## Export and Import Safely

JSON exports are useful as reviewed templates, not universal drop-in policy:

1. Remove or review repository-specific identifiers, source metadata, check
   names, and bypass actor IDs.
2. Confirm the target repository has the referenced default branch,
   CODEOWNERS coverage, workflows, Apps, teams, and merge methods.
3. Import in disabled or evaluate mode when available.
4. Exercise ordinary contributor, administrator, Dependabot, and release-bot
   paths.
5. Inspect rule insights, then activate the ruleset deliberately.

Do not copy an empty `required_status_checks` array and describe the result as
CI enforcement. Do not copy an Integration ID and assume it identifies the same
App in another organization.

## Validation Checklist

- Confirm deletion and force-push attempts are blocked on the default branch.
- Open a representative pull request and verify approvals, stale-review
  dismissal, last-push approval, CODEOWNERS, and thread resolution behavior.
- Confirm every required check reports on pull requests and, when applicable,
  merge-group commits.
- Verify a failing or missing required check blocks merging.
- Confirm ordinary users cannot create, move, or delete protected release tags.
- Confirm only the intended release App can create the next valid tag.
- Inspect rule insights for pass, fail, and bypass events.
- Re-read the effective repository rules after organization and repository
  policies are combined.

Report controls verified from configuration separately from actions exercised
against GitHub. State any behavior that still depends on an App installation,
organization policy, plan feature, or future live release.

## GitHub Source Authority

Review GitHub's current documentation before implementing rulesets because
available rules, plan support, and bypass behavior can change:

- [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [Creating rulesets for a repository](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Managing rulesets for a repository](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository)
- [REST API endpoints for repository rules](https://docs.github.com/en/rest/repos/rules)
- [Managing the automatic deletion of branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches)
- [Managing the automatic closing of issues](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-auto-closing-issues)
- [Managing suggestions to update pull request branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-suggestions-to-update-pull-request-branches)

Last reviewed against GitHub documentation: 2026-11-24.
