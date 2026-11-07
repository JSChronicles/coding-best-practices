# TypeScript Project Structure

Choose structure from runtime, deployable units, package boundaries, and public
APIs. Do not copy a large application layout into a small library or script.

## Small Package or Application

A practical starting point is:

```text
project/
|-- src/
|   |-- index.ts
|   `-- feature.ts
|-- tests/                 optional when tests are not colocated
|-- package.json
|-- tsconfig.json
`-- <package-manager-lockfile>
```

Colocated `*.test.ts` or `*.spec.ts` files are appropriate when proximity helps
ownership. A separate `tests/` tree is useful for integration tests, fixtures,
or black-box package tests. Follow the existing runner's discovery rules.

Create directories such as `adapters/`, `domain/`, `routes/`, `services/`, or
`components/` only when they express real responsibility. Avoid generic
`utils/`, `helpers/`, or `common/` collections; name modules for the capability
they provide.

## Applications and Libraries

Keep one clear application composition root where configuration, concrete
adapters, and long-lived resources are assembled. Domain modules should not
reach through global state to discover infrastructure.

For a published library:

- define deliberate entrypoints and package exports;
- include only supported runtime and declaration artifacts;
- test the package as consumers import it, not only through source aliases;
- avoid exposing private build paths;
- treat changes to exports, declarations, and runtime module format as API
  changes.

Use `src/index.ts` only as a deliberate public entrypoint. Do not add deep
barrel-file chains that hide dependencies, cause circular imports, or make
tree-shaking and ownership harder to reason about.

## ESM, CommonJS, and Resolution

Determine the contract from `package.json`, `tsconfig`, the runtime, and the
build tool together. Keep these aligned:

- package `type` and `exports`;
- compiler `module` and `moduleResolution`;
- emitted file extensions and import specifiers;
- test runner and bundler resolution;
- declaration output and consumer expectations.

Prefer one module system. A dual ESM/CommonJS package needs separate verified
entrypoints, correct conditional exports, and consumer tests for both formats.
Do not solve module errors with broad aliases or copied output trees before
understanding runtime resolution.

## Configuration Layout

Keep a primary `tsconfig.json` readable. Extend a shared base only when multiple
configs genuinely share policy. Separate build and test configs when their
inputs, globals, module behavior, or emission requirements differ.

Use project references for real package or build boundaries that benefit from
independent checking and incremental builds. Do not split a small project into
references merely to imitate a monorepo.

Exclude build output, coverage, caches, and generated artifacts from source
inputs unless a tool explicitly consumes them. Keep `rootDir`, `outDir`, source
maps, declarations, and declaration maps aligned with how artifacts are
published and debugged.

## Monorepos

Use `apps/` and `packages/` only when the repository contains multiple
deployables or reusable packages with distinct ownership. Each package should
have an explicit dependency contract, scripts, and entrypoints. Centralize
tooling where it reduces drift, but let package-specific runtime and build
requirements remain visible.

Do not import another workspace package through its private `src/` path. Consume
its declared workspace package or supported export so builds and tests exercise
the real boundary.
