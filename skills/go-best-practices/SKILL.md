---
name: go-best-practices
description: Creates, reviews, refactors, and tests idiomatic Go applications, packages, modules, and Go CI workflows. Use for .go files, go.mod, project structure, APIs, interfaces, errors, context, concurrency, logging, tests, fuzzing, benchmarks, dependencies, or GitHub Actions that format, vet, build, race-test, and scan Go.
metadata:
  author: JSChronicles
  version: "0.2.0"
---

# Go Best Practices

Produce simple, idiomatic, maintainable Go that makes ownership, failure, and
concurrency behavior easy to understand. Follow repository-local conventions
when they are stronger than general guidance.

## Start Here

1. Read repository instructions and inspect `go.mod`, the targeted packages,
   tests, generated-code boundaries, and existing tooling.
2. Preserve the module's declared Go compatibility unless the task includes a
   version upgrade. For a new module or explicit modernization, verify the
   current stable Go release from an official Go source instead of guessing.
3. Define package responsibilities and public behavior before adding types,
   interfaces, goroutines, or dependencies.
4. Implement the smallest clear solution, then format, analyze, test, and review
   ownership and cancellation paths.

## Core Rules

- Always run `gofmt` on changed Go files. Do not hand-format Go.
- Keep packages cohesive and named for what they provide. Avoid catch-all
  packages such as `common`, `helpers`, or `utils` without a focused domain.
- Choose the smallest directory structure that expresses real package,
  executable, visibility, and ownership boundaries. Start flat for small code;
  introduce `cmd/`, `internal/`, subpackages, fixtures, or deployment assets
  only when their semantics are needed.
- Keep exported APIs small. Prefer unexported identifiers until another package
  genuinely needs the behavior.
- Accept interfaces at the point of use and keep them minimal. Return concrete
  types unless abstraction is part of the package contract.
- Make useful zero values when practical. Add constructors when invariants,
  validation, dependencies, or resource acquisition require them.
- Return errors for expected failures. Do not use `panic` for routine input,
  configuration, I/O, or dependency errors.
- Wrap errors with context using `%w` when callers need the cause. Inspect error
  identity with `errors.Is` or `errors.As`, never string matching.
- Pass `context.Context` as the first parameter for request-scoped cancellation,
  deadlines, and values. Do not store contexts in structs or pass `nil`.
- Every goroutine must have a clear owner, termination condition, and error or
  result path. Prefer synchronous code until concurrency provides real value.
- Let senders own channel closure. Do not close channels merely to signal every
  cancellation case; use context or an explicit done mechanism where suitable.
- Protect shared mutable state deliberately and make copying or aliasing of
  slices, maps, and pointers clear at API boundaries.
- Prefer the standard library. Add dependencies only when they materially
  improve correctness or maintainability and their lifecycle is acceptable.
- Use structured logging appropriate to the project, normally `log/slog` for a
  new standard-library-based application. Libraries should not configure global
  logging or emit routine logs callers cannot control.
- Write tests around observable behavior. Use table-driven tests and subtests
  when they improve clarity, not as mandatory ceremony.
- Keep generated files generated. Change the source or generator and regenerate
  instead of editing generated output by hand.

## Reference Loading

- Read [project-layout-and-packages.md](references/project-layout-and-packages.md)
  for modules, commands, `internal`, package naming, dependencies, configuration,
  and repository structure.
- Read [api-errors-and-data.md](references/api-errors-and-data.md) for exported
  APIs, interfaces, errors, zero values, ownership, logging, and data modeling.
- Read [concurrency-and-context.md](references/concurrency-and-context.md) before
  adding or reviewing goroutines, channels, synchronization, worker pools,
  cancellation, or request-scoped work.
- Read [testing-and-tooling.md](references/testing-and-tooling.md) for unit and
  integration tests, fuzzing, benchmarks, race detection, formatting, static
  analysis, vulnerabilities, and module maintenance.
- Read [github-actions-ci.md](references/github-actions-ci.md) when creating or
  reviewing GitHub Actions for Go, and also apply
  `github-actions-best-practices`.
- Use [review-checklist.md](references/review-checklist.md) for reviews and final
  quality passes.

## Validation

Run the repository's established checks. When no stronger project command
exists, use the applicable subset of:

```console
gofmt -w <changed-go-files>
go vet ./...
go test ./...
go test -race ./...
govulncheck ./...
```

Use race detection when concurrency or shared state is involved and the target
platform supports it. Run benchmarks only when performance is part of the task.
Run `go mod tidy` when imports or module requirements change, then review both
`go.mod` and `go.sum` rather than treating tidy output as automatically correct.

Report commands that could not run, platform limitations, and any generated,
integration, or external behavior that still needs verification.

## Review Output

Lead with concrete findings ordered by severity. Prioritize correctness,
goroutine leaks, races, cancellation failures, error identity, resource leaks,
API compatibility, unsafe ownership, and missing behavioral tests. Avoid
style-only findings already handled by `gofmt` unless they reveal a design or
maintainability problem.
