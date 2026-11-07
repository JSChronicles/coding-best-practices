# Testing and Tooling

## Behavioral Tests

Test observable contracts rather than private implementation steps. Keep tests
deterministic, isolated, and readable.

- Use table-driven tests when cases share setup and assertions.
- Use subtests for meaningful case names, selective execution, or separate
  parallel lifecycles.
- Call `t.Helper()` in reusable test helpers so failures point to the caller.
- Use `t.Cleanup()` for resources tied to a test lifecycle.
- Use `t.TempDir()` for filesystem tests and avoid shared fixed paths.
- Compare errors with `errors.Is` or `errors.As` when identity matters.
- Avoid sleeping to wait for concurrency. Coordinate with channels, hooks, fake
  clocks, or bounded eventual assertions.
- Use `t.Parallel()` only when cases do not share mutable process state,
  environment, ports, files, or non-thread-safe fakes.

Prefer small fakes or consumer-defined interfaces over extensive mocks. An
integration test is often clearer when behavior depends on a real parser,
database protocol, filesystem, or subprocess boundary.

## Fuzzing and Benchmarks

Use fuzz tests for parsers, decoders, boundary validation, and functions with a
large or adversarial input space. Seed representative valid and invalid inputs,
assert stable invariants, and keep fuzz targets deterministic.

Write benchmarks only for a performance question. Prevent compiler elimination,
control setup separately from measured work, report allocations when useful,
and compare results with a tool such as `benchstat`. Do not optimize from one
noisy benchmark run.

## Standard Validation

Run repository-provided commands first. Otherwise use the relevant checks:

```console
gofmt -w <changed-go-files>
go vet ./...
go test ./...
```

Add these when applicable:

```console
go test -race ./...
go test -fuzz=<target> <package>
go test -bench=. -benchmem <package>
go mod tidy
go mod verify
govulncheck ./...
```

Review formatting changes, module changes, and generated output. Do not run a
destructive or broad modernization command outside the requested scope.

## Dependencies and Vulnerabilities

Keep module dependencies current through the repository's update policy and
review changelogs before major upgrades. Use the official Go vulnerability
tooling when available. Treat findings in reachable code as actionable; assess
unreachable findings and tool limitations explicitly rather than ignoring all
scanner output.

Do not blindly run `go get -u ./...` as routine cleanup. Select upgrades
deliberately, review direct and transitive changes, run tests and race checks,
and confirm the module's supported Go version.

## Static Analysis and CI

`go vet` is a baseline, not an exhaustive linter. Preserve established tools
such as Staticcheck or golangci-lint when the repository uses them, and pin CI
tool versions through the project's normal mechanism. Avoid adding a large
lint suite without agreement on enabled rules and maintenance.

CI should format-check, analyze, and test supported Go versions and platforms
in proportion to the compatibility contract. Run the race detector on a
supported platform when concurrency risk warrants its cost.
