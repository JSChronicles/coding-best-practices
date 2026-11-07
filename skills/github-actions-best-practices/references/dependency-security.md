# Dependency Security and Updates

Use this reference when adding or updating actions, reusable workflows, or
workflow dependency policy.

## Resolve the Latest Stable Release First

For new workflows and newly added actions, using the latest stable compatible
release is a required authoring step, not optional cleanup. Resolve every
external `uses:` dependency immediately before writing or finalizing the
workflow.

Use the action's official repository as the source of truth. For repositories
that publish GitHub releases, a read-only query such as this returns GitHub's
latest non-draft, non-prerelease release:

```console
gh api repos/OWNER/REPOSITORY/releases/latest --jq .tag_name
```

Then confirm the action's official README or release notes support that release
for the target GitHub product, runner, inputs, and runtime. If the repository
does not publish releases, use its official documentation and tags to identify
the latest stable supported ref. Do not infer a version from search snippets,
third-party examples, or another repository's workflow.

Apply these rules:

- Prefer the latest stable release, excluding drafts, prereleases, and nightly
  channels unless the user explicitly requests a preview.
- Write the complete release tag, such as `vN.N.N`, rather than a major-only or
  major-minor ref.
- Re-resolve versions even when copying a workflow from the same organization.
- Review every existing `uses:` line during a workflow modernization. Flag
  stale releases unless a current compatibility constraint is documented.
- If the latest release is incompatible, select the newest compatible stable
  release and record the concrete reason. Compatibility is the exception; age
  or familiarity is not.
- If current release information cannot be reached, do not guess or silently
  reuse a remembered version. State what could not be verified.

Release currency and immutable resolution are separate controls: first choose
the latest stable release, then lock or pin its exact commit, and finally keep it
current with Dependabot.

## Prefer Workflow Dependency Lockfiles

When supported, `.github/workflows/actions.lock` is the preferred way to secure
action dependencies because it pins direct and transitive actions while keeping
readable release refs in workflow YAML. It also records repository identity so
a repository transfer or replacement is visible during validation.

Before onboarding a workflow:

1. Resolve every `uses:` reference from its official repository and verify it
   targets the latest stable compatible release.
2. Install the official extension with
   `gh extension install github/gh-actions-lock` if it is not already present.
3. Run `gh actions-lock` for all workflows or pass a workflow path for a
   focused migration.
4. Review the workflow and lockfile together, including changed commits,
   `owner_id`, and `repo_id` values.
5. Commit `.github/workflows/actions.lock` with the workflow change.

Never edit the lockfile by hand. Regenerate it whenever an onboarded workflow's
action dependencies change. Use `gh actions-lock --verify` for a read-only,
network-backed CI check, or `gh actions-lock --verify-local` for an offline
coverage check. Repository or organization policy can also reject incomplete or
stale lockfiles.

Local actions referenced with `./` are not locked. Prefer the lock tool's
same-repository migration when appropriate so repository-local action
dependencies can be resolved. Use an ignore option only after understanding the
resulting coverage gap.

Do not automate acceptance of moved immutable refs or rewritten history. Review
the source and diff before using an explicit acceptance option.

## Full-SHA Fallback

If a lockfile is unavailable, intentionally not adopted, or does not include the
workflow, full-SHA pinning is mandatory for every external action. Do not create
or finish an unlocked workflow that uses a branch, major tag, minor tag, or full
release tag directly.

After resolving the latest stable compatible release, resolve that tag to the
commit in the action's original repository:

```console
gh api repos/OWNER/REPOSITORY/commits/TAG --jq .sha
```

Use the resulting full 40-character SHA and preserve the release tag as a
comment:

```yaml
- uses: OWNER/REPOSITORY@0123456789abcdef0123456789abcdef01234567 # vN.N.N
```

Required rules:

- Pin external actions to the complete commit SHA from the action's original
  repository, not a fork.
- Add a version comment such as `# v4.2.0` beside the SHA.
- Do not treat a branch, major tag, or release tag as immutable. Tags can move.
- Reject abbreviated SHAs. They are not an acceptable dependency pin.
- Prefer maintained actions with transparent source, minimal permissions, and a
  clear release and security process.

## Reusable Workflows

Actions lockfiles do not pin calls made with `jobs.<job_id>.uses`. Pin external
reusable workflows to a full commit SHA. Dependencies inside that reusable
workflow are governed by the lockfile in the reusable workflow's source
repository, if it has one.

For same-repository reusable workflows, follow the syntax supported by the
repository's GitHub product and version. Do not convert syntax without checking
GitHub Enterprise Server compatibility when that matters.

## Keep Dependencies Current

Configure Dependabot in `.github/dependabot.yml`. Give each package ecosystem
its own entry so its schedule, cooldown, grouping, labels, and exceptions remain
independent.

Choose a cadence the maintainers can reliably review. Monthly is a useful
low-noise default for small or stable repositories. Use weekly or more frequent
updates when the repository changes quickly, the ecosystem has a high security
exposure, or maintainers have the capacity to review that volume.

Set an explicit time and timezone so updates arrive during normal review hours.
When several ecosystems share a repository, stagger their scheduled times to
reduce branch churn, merge conflicts, and immediately outdated pull requests.

Use a cooldown for routine version updates when the repository prefers
stability over immediate adoption. Seven days is a practical starting point;
fourteen days is more conservative. Adjust or omit it when rapid updates are a
deliberate requirement.

Group routine version updates within an ecosystem, not across unrelated
ecosystems. Stable group names, commit prefixes, and labels make updates easy to
filter, route, and roll back. For example:

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
      time: "08:30"
      timezone: "America/Chicago"
    cooldown:
      default-days: 7
    groups:
      github-actions:
        applies-to: version-updates
        patterns:
          - "*"
    commit-message:
      prefix: "chore(github-actions)"
    labels:
      - "dependencies"
      - "github-actions"
```

Treat the values as a policy example, not universal requirements. Preserve
repository conventions and ensure every referenced label exists.

When workflows are onboarded to the lockfile, Dependabot can update the action
reference and matching lock entry together. Review release notes and breaking
changes for major upgrades. If auto-approval is enabled, limit it to explicitly
approved low-risk ecosystems and patch or minor updates; keep major upgrades
visible for manual review by default.

Do not mechanically replace an action with the numerically newest major. Check
runner requirements, changed inputs or outputs, runtime deprecations, and
repository compatibility first.

## Rollout and Enforcement

For organizations adopting lockfiles:

1. Pilot on representative repositories.
2. Add lockfile validation and optionally CODEOWNERS review.
3. Keep existing full-SHA policy during migration if needed.
4. Enforce lockfiles only after repositories have a workable update path.

Lockfile enforcement and full-SHA enforcement are distinct policies. Use both
during transition when organizational risk requires it.
