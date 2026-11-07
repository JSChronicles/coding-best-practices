# Testing and Tooling

Use the repository's selected formatter, linter, compiler, test runner, build
tool, and package manager. Do not replace working tools merely because another
tool is newer or personally preferred.

## Test Strategy

Test observable behavior through public or intentionally testable boundaries.
Cover normal behavior, invalid inputs, async rejection, cancellation, cleanup,
and meaningful edge cases. Keep tests deterministic and independent.

Unit tests should isolate logic, not mock every internal function. Integration
tests should exercise real module boundaries such as a database adapter, HTTP
handler, package export, or generated client with explicit setup and cleanup.
Use end-to-end tests for a small number of critical user or system paths.

Prefer fakes for stable domain collaborators and focused mocks or spies for
interaction contracts. Restore timers, globals, environment values, network
interceptors, and mocks after each test. Fake timers require deliberate control
of both timers and pending promises.

Test runtime validation with malformed and adversarial values. Add compile-time
type tests only for important public type contracts; they do not replace runtime
tests.

Coverage is a diagnostic, not proof. Enforce thresholds only when the repository
owns them and focus review on untested risk rather than maximizing a percentage.

## Compiler and Build

Run type checking with emission disabled when build and checking are separate:

```console
tsc --noEmit
```

Use the project's build command to verify real transforms, declarations,
assets, aliases, package exports, and runtime module resolution. A successful
type check does not prove the emitted package can be imported or executed.

For libraries, test packed or built artifacts as a consumer where practical.
For applications, exercise the production build mode without assuming a dev
server validates the same paths.

## Formatting and Linting

Let the configured formatter own layout. Keep lint rules focused on defects,
unsafe types, promise handling, imports, and maintainability signals that the
team will act on. Do not disable broad rule families to silence one local case;
use the narrowest justified suppression with an explanation when needed.

Keep formatter and linter responsibilities distinct to avoid conflicting
rewrites. Type-aware linting needs the correct project configuration and may be
too expensive to run identically in every editor and CI job.

## Package Managers and Lockfiles

Select the package manager from the existing lockfile and `packageManager`
field. Use exactly one lockfile family:

- npm: `npm ci`
- pnpm: `pnpm install --frozen-lockfile`
- Yarn: `yarn install --immutable`

Use the repository's declared package-manager version when present. Review
manifest and lockfile changes together. Classify dependencies correctly as
runtime, development, optional, or peer dependencies, especially for published
packages.

Do not run broad dependency upgrades as a side effect of an unrelated code
change. When upgrading, verify release notes, runtime and type compatibility,
peer constraints, build output, tests, and security impact. Remove unused
dependencies and imports rather than leaving accidental supply-chain surface.

## Validation Order

Use the project's scripts, usually in this order:

1. Frozen dependency install when needed.
2. Formatting check.
3. Lint.
4. Type check.
5. Unit and integration tests.
6. Production build.
7. Consumer, end-to-end, or package checks when applicable.

Do not hide failures with `continue-on-error`. Keep generated files and build
output out of commits unless the repository intentionally versions them.
