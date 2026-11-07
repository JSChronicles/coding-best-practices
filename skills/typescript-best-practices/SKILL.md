---
name: typescript-best-practices
description: Creates, reviews, refactors, and tests maintainable TypeScript applications, libraries, packages, and CI workflows. Use for .ts and .tsx files, tsconfig files, package structure, type design, runtime validation, async behavior, dependency management, tests, builds, or TypeScript GitHub Actions.
metadata:
  author: JSChronicles
  version: "0.1.0"
---

# TypeScript Best Practices

Produce clear, type-safe TypeScript whose runtime behavior, public contracts,
module boundaries, and failure modes are easy to understand. Follow the
repository's existing runtime, framework, package manager, and build conventions
unless the task explicitly changes them.

## Start Here

1. Read repository instructions and inspect `package.json`, the selected
   lockfile, relevant `tsconfig` files, package exports, source layout, tests,
   and established scripts before editing.
2. Identify the runtime and module contract: Node.js, browser, edge, library,
   application, ESM, CommonJS, or a deliberate dual-package build.
3. Preserve supported Node.js, TypeScript, framework, and package-manager
   versions unless the request includes an upgrade. For new projects or explicit
   modernization, verify current supported releases from official sources.
4. Make the smallest coherent change, then format, lint, type-check, test, and
   build with the repository's own commands.

## Core Rules

- Enable TypeScript's strict mode for new projects. In an existing non-strict
  project, improve the touched boundary without forcing an unrelated migration.
- Prefer precise domain types, discriminated unions, and narrowing over casts,
  non-null assertions, broad index signatures, or `any`.
- Use `unknown` for untrusted or genuinely unknown values and narrow it before
  use. Validate external data at runtime; static types do not validate JSON,
  environment variables, network responses, or storage.
- Keep public APIs small and explicit. Avoid leaking framework, transport, or
  persistence types across domain boundaries unless they are part of the
  intended contract.
- Model invalid states out when practical, but do not build elaborate generic
  type machinery whose maintenance cost exceeds its safety benefit.
- Keep imports, file extensions, package `type`, compiler module settings,
  bundler behavior, and runtime resolution consistent. Do not mix ESM and
  CommonJS conventions accidentally.
- Use `import type` and `export type` when the distinction affects emitted code,
  module cycles, or repository style. Avoid barrel files that create cycles or
  obscure ownership.
- Treat rejected promises deliberately. Await, return, aggregate, or explicitly
  detach them with an owned error path; do not leave floating promises.
- Thread cancellation through supported APIs such as `AbortSignal`. Bound
  concurrency when work can scale with input size or external resources.
- Throw `Error` objects with useful context. Narrow caught values before reading
  them, preserve causal information where supported, and do not silently swallow
  failures.
- Keep side effects at clear boundaries. Prefer dependency injection or small
  adapters over hidden module globals when behavior must be tested or replaced.
- Use the package manager selected by the checked-in lockfile and keep installs
  frozen in CI. Do not rewrite or introduce a second lockfile accidentally.
- Write tests around observable behavior, boundary cases, and failure paths.
  Avoid tests that merely restate implementation details or TypeScript syntax.
- Do not edit generated JavaScript, declarations, clients, schemas, or bundles
  by hand. Change their source or generator and regenerate them.

## Reference Loading

- Read [project-structure.md](references/project-structure.md) for `src`, tests,
  applications, packages, entrypoints, exports, ESM/CommonJS, and monorepos.
- Read [type-system-and-api-design.md](references/type-system-and-api-design.md)
  for strictness, narrowing, generics, unions, public contracts, data modeling,
  and runtime validation.
- Read [runtime-and-async.md](references/runtime-and-async.md) for errors,
  promises, cancellation, concurrency, resources, logging, and side effects.
- Read [testing-and-tooling.md](references/testing-and-tooling.md) for tests,
  formatting, linting, type checks, builds, dependencies, and package managers.
- Read [github-actions-ci.md](references/github-actions-ci.md) when creating or
  reviewing TypeScript GitHub Actions, and also apply
  `github-actions-best-practices`.
- Use [review-checklist.md](references/review-checklist.md) for reviews and final
  quality passes.

## Validation

Run the repository's established scripts. When no stronger project command
exists, use the applicable package-manager equivalents of:

```console
<package-manager> run format:check
<package-manager> run lint
<package-manager> run typecheck
<package-manager> test
<package-manager> run build
```

Use a frozen install only when dependency installation is needed. Do not invent
missing scripts solely to make this command list uniform. Report commands that
could not run and any browser, integration, generated-code, or environment
behavior that remains unverified.

## Review Output

Lead with concrete findings ordered by severity. Prioritize runtime/type
mismatches, unsafe boundary assumptions, incorrect module resolution, unhandled
promises, races or leaks, API compatibility, dependency and lockfile drift, and
missing behavioral tests. Avoid style-only findings already enforced by the
project's formatter or linter.
