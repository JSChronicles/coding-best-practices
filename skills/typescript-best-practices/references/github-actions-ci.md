# TypeScript GitHub Actions CI

Use this reference when creating or reviewing GitHub Actions that install,
format, lint, type-check, test, build, or package TypeScript. Also apply
`github-actions-best-practices` for current actions, action lockfiles or SHA
pins, permissions, concurrency, caching, and timeouts.

Start from the adaptable
[TypeScript workflow template](../assets/github-workflow.yaml). Resolve every
placeholder from the repository's package manager, lockfile, scripts, Node.js
support contract, and current action releases. Do not paste placeholder commands
into a real workflow.

## Baseline Workflow

Validate pull requests and pushes to the protected integration branch. Begin
with `contents: read`, cancel superseded CI runs, and set a timeout.

Preserve this order:

1. Check out without persisted credentials.
2. Install the supported Node.js version.
3. Enable or install the declared package-manager version when needed.
4. Install exactly from the checked-in lockfile.
5. Check formatting.
6. Lint.
7. Type-check without emission when that is a separate script.
8. Run tests.
9. Build production or publishable artifacts.
10. Run consumer, end-to-end, or package checks when the project requires them.

Use the repository's scripts instead of duplicating long commands in workflow
YAML. Keep failures fatal.

## Runtime and Package Manager

Read Node.js compatibility from the repository's version file, `engines`, test
matrix, or documented support policy. For a new project, verify the current
supported LTS release from the official Node.js source rather than guessing.

Match the lockfile:

| Lockfile | Cache value | Frozen install |
| --- | --- | --- |
| `package-lock.json` or `npm-shrinkwrap.json` | `npm` | `npm ci` |
| `pnpm-lock.yaml` | `pnpm` | `pnpm install --frozen-lockfile` |
| `yarn.lock` | `yarn` | `yarn install --immutable` |

Do not create a second lockfile in CI. For pnpm or Yarn, activate the version
declared by the project before setup or install, using the repository's existing
Corepack or setup-action convention.

## Caching

Prefer the supported Node setup action's package-manager cache when it fits the
project. Set its dependency path to the actual lockfile, including workspace
paths when needed. Cache only reproducible package-manager data, not
`node_modules`, secrets, arbitrary build output, or mutable credentials.

Add framework or build caches only when they save meaningful time and their keys
include every input needed for correctness. A cache miss must remain correct.

## Tests, Coverage, and Matrices

Run tests in non-watch mode. Ensure the runner terminates and reports unhandled
rejections and leaked handles according to project policy. Upload coverage or
test reports only when another check or reviewer consumes them.

Add a Node.js or operating-system matrix only when the package promises those
versions or platforms. Run expensive browser or end-to-end suites in a separate
bounded job with explicit service setup and artifact handling.

## Publishing and Security

Do not publish packages from pull-request jobs. Use a separately authorized
release workflow with protected environments, provenance where supported, and
short-lived identity rather than long-lived registry tokens when available.

Dependency review, security scanning, and automated updates complement tests;
they do not justify running lifecycle scripts from untrusted dependency changes
with elevated credentials. Keep pull-request permissions read-only and do not
expose deployment or publishing secrets.

## Workflow Review

- Node.js and package-manager versions come from an explicit support contract.
- The frozen install matches the one checked-in lockfile.
- Current action releases are lockfile-managed or full-SHA pinned.
- Formatting, lint, type-check, tests, and build are fatal when applicable.
- Cache keys and dependency paths match the package manager and workspace.
- Matrices cover supported environments rather than arbitrary versions.
- Pull-request jobs cannot publish, deploy, or access unnecessary secrets.
