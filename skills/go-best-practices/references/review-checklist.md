# Go Review Checklist

## Correctness and API Design

- The directory layout is proportional to the project and expresses real
  executable, package, visibility, test, asset, and release boundaries.
- `cmd/`, `internal/`, subpackages, `testdata/`, and operational directories are
  present only where their semantics are useful; no template-only structure or
  unnecessary `src/`/`pkg/` hierarchy was introduced.
- Executable entrypoints are thin, and reusable or domain behavior is not copied
  between command directories.
- Package responsibilities and names are cohesive and clear at call sites.
- Exported identifiers are necessary, documented appropriately, and compatible
  with the intended public contract.
- Interfaces are small, consumer-owned where practical, and represent real
  substitution boundaries.
- Zero values and constructors preserve invariants without unnecessary ceremony.
- Slice, map, pointer, and resource ownership is explicit enough to avoid
  surprising mutation or races.
- Generated files were regenerated from their sources rather than hand-edited.

## Errors and Resources

- Expected failures return errors instead of panicking.
- Wrapped errors preserve identity with `%w`; decisions use `errors.Is` or
  `errors.As`, not text matching.
- Errors include useful operation and subject context without duplicating noise.
- Files, response bodies, transactions, timers, processes, and other resources
  are closed or finalized on every path.
- Cleanup failures that affect correctness are not silently discarded.
- Logging occurs at an appropriate boundary and exposes no secrets.

## Context and Concurrency

- Context is the first parameter, propagated, never stored, and never `nil`.
- Derived contexts are canceled and blocking operations honor cancellation.
- Every goroutine has an owner, bounded lifecycle, termination path, and result
  or error path.
- Channels have clear ownership and are closed by senders when closure is
  meaningful.
- Shared state is synchronized across the complete invariant; mutex-containing
  values are not copied after use.
- Worker counts, queues, retries, and shutdown waits are bounded.
- Race-sensitive changes were exercised with `go test -race` when supported.

## Tests, Modules, and Tooling

- Tests cover behavior, error paths, boundaries, and cancellation without
  relying on arbitrary sleeps.
- Parallel tests do not share unsafe process or filesystem state.
- Fuzzing or benchmarks are present when the task and risk justify them.
- `gofmt`, `go vet`, and `go test` pass for the affected scope.
- `go.mod` and `go.sum` changes are intentional and reviewed.
- New dependencies are justified, maintained, licensed appropriately, and
  proportionate to the problem.
- Vulnerability checks were run or their absence and limitations are reported.
- Go GitHub Actions use the module's Go contract and enforce formatting, vet,
  tests, build, tidy module files, race detection, and vulnerability policy as
  applicable; workflow security follows `github-actions-best-practices`.

## Review Output

Lead with defects and risks, ordered by severity and tied to exact files and
symbols. Explain the observable impact and smallest practical correction. If no
findings remain, state that clearly and identify validation that could not run.
