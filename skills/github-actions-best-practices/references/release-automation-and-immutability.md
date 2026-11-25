# Release Automation and Immutability

Design releases as a controlled transition from reviewed source to a
versioned, verifiable artifact. Keep release credentials narrower than general
repository automation and make publication the final step, especially when
immutable releases are enabled.

## Establish the Release Contract

Before changing automation, inspect:

- the authoritative release branch and whether pull requests are squash,
  rebase, or merge committed;
- existing version files, tags, changelog configuration, package registries,
  artifacts, and release notes;
- the current release bot or token, its installation scope, and repository
  rules that affect bot pushes or tags;
- whether releases include attached assets, attestations, SBOMs, checksums, or
  provenance; and
- whether release immutability is disabled, enabled by the repository, or
  enforced by the organization.

Choose one release source, normally a reviewed commit on the default branch.
Pull-request workflows should validate untrusted changes without release
credentials. The privileged release workflow should run only after the chosen
branch contains the reviewed commit.

## Choose the Release Model

Use a direct release when approval of the source pull request is the release
gate. A typical sequence is:

1. Merge a Conventional Commit or a pull request with a release-significant
   squash title into the release branch.
2. Calculate the next semantic version from commits since the last release tag.
3. Update every authoritative version file and the changelog together.
4. Commit the generated release changes, create the matching tag on that
   commit, and publish the GitHub Release.
5. Ignore the generated release commit in the release trigger to prevent a
   loop.

Use a release pull request only when maintainers need a separate review gate for
the proposed version or changelog. That model necessarily needs permission to
create and update a branch and pull request. Do not add that complexity merely
because a release tool supports it.

With squash merging, the pull-request title commonly becomes the only commit
subject seen by semantic-release tooling. Require a Conventional Commit title
or configure another reliable version signal. A common policy is `feat:` for a
minor release, `fix:` or `perf:` for a patch, and `!` or a
`BREAKING CHANGE:` footer for a major release. Match the repository's actual
parser rather than assuming this mapping.

Before enabling tag-based calculation in a repository with existing versions,
create and verify a baseline tag such as `v0.6.0` on the commit that actually
published version 0.6.0. Never place a baseline tag on an unrelated current
commit merely to make the workflow pass.

## Use a Dedicated Release Bot

Prefer a GitHub App over a personal access token when the organization can
operate one. A dedicated App separates release authority from a maintainer's
account, produces short-lived installation tokens, and can be installed only on
repositories it releases.

Name the App for its narrow responsibility:

- use `<project>-release-bot` when it serves one project;
- use `<ecosystem>-release-bot`, such as `python-release-bot`, when a small set
  of repositories intentionally share the same release process; and
- avoid broad names such as `automation-bot` when the App also has unrelated
  administration, Actions, environment, or secrets access.

For a bot that commits versions, creates tags, and publishes GitHub Releases,
the minimum repository permissions are normally:

| Permission | Access | Purpose |
| --- | --- | --- |
| Metadata | Read | Granted automatically to GitHub Apps |
| Contents | Read and write | Push the version commit and tag, and create the GitHub Release |

Grant no organization permissions and no Actions, Administration, Dependabot,
Environments, Issues, Pull requests, Secrets, or Workflows permission by
default. Add a permission only when a verified API endpoint or chosen release
model requires it. For example, a release-pull-request model typically adds
Pull requests write access and may need Issues write access for labels. Keep
package-registry publication credentials separate; prefer registry trusted
publishing or OIDC instead of expanding the release App.

Install the App on selected repositories rather than every repository. Store
the private key as a secret, scope organization secrets to the intended
repositories, and rotate the key according to organization policy. A Client ID
is not secret and may be stored as a repository or organization variable unless
local policy requires secrets for all App configuration.

In the workflow, request only the token permissions needed for that job, such
as `permission-contents: write`. Keep the automatic `GITHUB_TOKEN` read-only or
disabled when the App token performs the write. If repository rules prevent the
generated release commit, either redesign the flow or grant the specific App a
narrow bypass; do not give it Administration permission as a shortcut.

Installing an App, expanding its permissions, changing branch-rule bypasses,
pushing a baseline tag, enabling release immutability, and publishing a release
are external mutations. Confirm the requested scope and exact repository before
performing them.

## Keep Versions and Tags Consistent

- Use one documented tag format, normally `vX.Y.Z`, and ensure release tooling
  reads the same format it writes.
- Update every distributed manifest, package version, marketplace entry, and
  generated version source in one release commit.
- Validate that all versions agree before creating the tag.
- Create the tag from the release commit, then verify its commit SHA before
  publication.
- Never force-move a published release tag. Correct a bad release with a new
  version.
- Serialize releases for the same branch so concurrent runs cannot calculate
  and publish competing versions.
- Test the no-release path and the generated-release-commit loop guard as well
  as feature, fix, and breaking-change calculations.

## Enable Release Immutability

Enable **Enable release immutability** in repository settings when GitHub
supports it and the publishing workflow can finalize the release in one pass.
Prefer an organization policy when the same standard should cover many
repositories. Immutability applies to future releases, so verify the setting
before the first release that depends on it.

Once an immutable release is published, its associated tag cannot be moved and
its attached assets cannot be modified or deleted. Release titles and notes may
still be edited, and GitHub creates a release attestation for the published tag,
commit, and assets. Treat these guarantees as a reason to verify inputs before
publication, not as a substitute for build and artifact validation.

When a release has attached assets:

1. Build and test the exact artifacts that will be published.
2. Create a draft release.
3. Attach every asset, checksum, SBOM, and required provenance item.
4. Verify asset names, digests, platform coverage, and the target tag.
5. Publish the draft only after the release is complete.

Do not design a workflow that publishes first and uploads or replaces assets
later. With immutability enabled, that sequence cannot complete. Repair a bad
published release with a new version rather than attempting to reuse its tag.

Enabling the repository setting is an administrative setup action, not an
ongoing release-bot responsibility. The release App does not need
Administration permission to publish immutable releases.

## Validate the Release Path

Before enabling or merging release automation:

- dry-run version calculation against representative `feat`, `fix`, no-release,
  and breaking commits;
- confirm the baseline tag and current version point to the same released
  commit;
- verify every version-bearing file changes to the same value;
- confirm the release commit and tag are created from the intended branch and
  SHA;
- inspect App installation scope, secret scope, requested token permissions,
  and branch-rule bypasses;
- verify release immutability is enabled at the intended repository or
  organization scope;
- exercise draft creation, complete asset upload, and final publication when
  assets exist; and
- confirm a generated release commit does not start another release.

Report dry-run evidence separately from a live publication. State any branch
rules, App installation approvals, registry credentials, organization policy,
or immutable-release behavior that can only be confirmed on GitHub.

## GitHub Source Authority

Review GitHub's current documentation before implementing this policy because
release and permission behavior can change:

- [Immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)
- [Preventing changes to releases](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/prevent-release-changes)
- [Managing releases in a repository](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [REST API endpoints for releases](https://docs.github.com/en/rest/releases/releases)
- [Permissions required for GitHub Apps](https://docs.github.com/en/rest/authentication/permissions-required-for-github-apps)

Last reviewed against GitHub documentation: 2026-11-24.
