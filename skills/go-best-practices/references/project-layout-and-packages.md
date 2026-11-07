# Project Layout and Packages

## Go Version and Module Policy

Treat `go.mod` as the module's compatibility contract. Preserve its `go`
directive unless the task includes modernization. Respect an existing
`toolchain` directive and the project's CI matrix.

For a new module or explicit upgrade, verify the current stable Go release from
an official source such as `https://go.dev/VERSION?m=text`. Do not choose a Go
version from memory, a stale template, or an unrelated repository. Review the
release notes before adopting language, standard-library, or toolchain behavior
that changes compatibility.

Use one module for a cohesive repository unless independent release cycles or
dependency boundaries justify multiple modules. Do not introduce a workspace or
nested modules solely to organize directories.

## Directory Structure Decision

Go does not require one universal repository tree. Choose the smallest layout
that makes executable boundaries, package ownership, import visibility, tests,
and release units obvious. Preserve a clear existing structure unless the task
includes reorganizing it.

| Repository shape | Prefer |
| --- | --- |
| Small library | Package files and tests at the module root |
| One small executable with no reusable packages | A root `main.go` can be sufficient |
| Executable with reusable or private application code | `cmd/<binary>/` plus focused packages, usually under `internal/` |
| Multiple executables | One thin entrypoint under each `cmd/<binary>/` |
| Public library with subpackages | Public package directories named for their domain; use `internal/` only for private implementation |
| Service with migrations, schemas, or deployment files | Keep Go under `cmd/` and domain packages; add non-Go directories only for assets the project actually owns |

Avoid adding empty directories or copying a large template before the code has a
boundary that needs them. Do not add `src/` around a normal Go module merely to
imitate another language's layout. The optional `pkg/` convention has no special
meaning to the Go toolchain; use it only when the repository intentionally uses
that convention and it improves navigation.

## Concrete Layouts

### Small Library

Keep a small cohesive library flat:

```text
repository/
├── go.mod
├── go.sum
├── client.go
├── client_test.go
├── options.go
└── README.md
```

Add subpackages only when they expose a distinct responsibility that callers
can understand. Do not split files into directories solely to reduce file size.

### Single Command with Private Packages

Keep the entrypoint thin and put reusable application behavior in focused
private packages:

```text
repository/
├── go.mod
├── go.sum
├── cmd/
│   └── foundryctl/
│       └── main.go
├── internal/
│   ├── config/
│   │   ├── config.go
│   │   └── config_test.go
│   └── command/
│       ├── run.go
│       └── run_test.go
└── README.md
```

`main.go` should normally parse process-level input, construct dependencies,
invoke application behavior, and map the result to logs and an exit status. It
should not contain the entire application.

### Multiple Commands

Give each produced binary its own entrypoint while sharing domain packages:

```text
repository/
├── go.mod
├── go.sum
├── cmd/
│   ├── api/
│   │   └── main.go
│   └── worker/
│       └── main.go
├── internal/
│   ├── app/
│   ├── queue/
│   └── store/
└── README.md
```

Do not copy business logic between command directories. Keep entrypoints thin
and share behavior through packages with real domain ownership.

### Service with Operational Assets

Keep non-Go assets beside, not mixed into, Go package directories:

```text
repository/
├── go.mod
├── go.sum
├── cmd/
│   └── service/
│       └── main.go
├── internal/
│   ├── httpapi/
│   ├── service/
│   └── store/
├── migrations/
├── docs/
├── deploy/
└── README.md
```

Add `migrations/`, `deploy/`, `api/`, `web/`, or similar directories only when
the repository owns those artifacts. Name them for their actual purpose and
document how they are generated, validated, or deployed.

## Directory Semantics

- **`cmd/<binary>/`:** executable entrypoints. Keep each `package main` thin.
- **`internal/`:** packages whose imports must be restricted to the owning
  parent tree. Use it for real privacy boundaries, not every implementation
  file by default.
- **Domain package directories:** cohesive public or private packages named for
  the capability they provide, not architectural filler such as `utils`.
- **`testdata/`:** package-local fixtures. The Go tool ignores these directories
  when discovering packages. Keep fixtures small and explain non-obvious origin
  or regeneration.
- **`examples/` or example tests:** runnable consumer examples when they improve
  the public API. Prefer `Example...` tests when documentation and verification
  should stay together.
- **`scripts/`:** operational scripts that are not Go packages. Do not place Go
  source here merely to avoid defining a package boundary.
- **`docs/`:** substantial design or operator documentation. Keep package API
  documentation close to the package.
- **`vendor/`:** generated vendored modules only when project policy requires
  them; never hand-edit vendored dependencies.

Keep ordinary unit tests beside the code they test. Use external test packages
when testing the public consumer surface is valuable. Put cross-package or
environment-dependent integration tests in a clearly named location only when
co-location would obscure their lifecycle or requirements.

## Feature versus Layer Organization

Prefer packages with domain or capability ownership over automatic horizontal
layers. `handler`, `service`, `repository`, and `model` packages are useful only
when each is a coherent package with a stable responsibility. Avoid a design
where every feature must cross generic layer packages and unrelated features
become coupled through shared types.

Split a package when it has distinct ownership, dependencies, reuse, or
visibility—not merely because it has many files. Multiple files in one package
are inexpensive and often clearer than premature package boundaries.

## Package Boundaries

- Give each package one understandable responsibility.
- Use short, lower-case package names that read naturally at call sites.
- Avoid package-name stutter such as `http.HTTPClient` when `http.Client` is
  clear.
- Keep implementation details unexported. Use `internal/` when the repository
  needs compiler-enforced import boundaries.
- Avoid import cycles by repairing responsibilities rather than adding a vague
  shared package.
- Put commands under `cmd/<name>` when a repository ships multiple executables.
  A single small command may remain at the module root when that is clearer.
- Keep reusable behavior outside `package main` when it needs direct testing or
  use by multiple commands.

Do not impose a universal directory tree. Add `cmd`, `internal`, `pkg`, or other
directories only when their semantics help the actual repository. In
particular, `pkg/` has no special meaning to the Go toolchain.

## Initialization and Configuration

Keep `init` functions rare and deterministic. Do not hide network access,
filesystem mutation, registration order dependencies, or expensive work at
import time. Prefer explicit construction and dependency wiring.

Parse configuration at the application boundary, validate it once, and pass
typed values inward. Keep environment-variable and flag handling out of domain
packages. Never store secrets in source, defaults, logs, or generated examples.

For a command, prefer the standard `flag` package when it meets the interface.
Adopt a CLI framework only when subcommands, completion, shared flags, or other
requirements justify the dependency.

## Dependencies and Modules

- Prefer the standard library when it is clear and sufficient.
- Evaluate maintenance, license, security history, transitive dependencies, and
  API stability before adding a module.
- Use the narrowest dependency that solves the problem; avoid frameworks for a
  small isolated feature.
- Run `go mod tidy` after import changes and review removals, additions, and
  version movement in both `go.mod` and `go.sum`.
- Commit `go.sum`. Commit `vendor/` only when repository policy or offline and
  reproducible build requirements call for vendoring.
- Use `go mod verify` when diagnosing module-cache integrity. Use vulnerability
  scanning as described in the testing and tooling reference.

## Generated Code and Embedding

Mark generated Go with the standard generated-code convention and keep the
generator command reproducible. Regenerate from source and review the output.

Use `go:embed` for versioned, build-time assets that belong in the binary. Do
not embed secrets, mutable runtime configuration, or large data without
considering binary size and update behavior.
