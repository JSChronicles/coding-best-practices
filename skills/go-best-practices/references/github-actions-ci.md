# Go GitHub Actions CI

Use this reference when creating or reviewing GitHub Actions that format,
analyze, build, test, race-test, or vulnerability-scan Go. Also apply
`github-actions-best-practices` for current actions, lockfiles or SHA pins,
permissions, concurrency, caching, and timeouts.

Start from the adaptable [Go workflow template](../assets/github-workflow.yaml)
when a new workflow is requested. Resolve every action placeholder and tailor
race, vulnerability, integration, matrix, and artifact behavior to the module's
actual support contract.

## Baseline Workflow Shape

Validate pull requests and pushes to the protected integration branch, with
manual dispatch when useful. Start with `contents: read`, cancel stale runs, and
bound every job with a timeout.

Use the Go version from `go.mod` and any `toolchain` directive. For a new module,
verify the current stable Go release from an official source. Add a matrix only
when the project promises compatibility with multiple Go versions or operating
systems.

### Formatting and Static Analysis

Check formatting without modifying the branch:

```console
test -z "$(gofmt -l .)"
go vet ./...
```

On a non-POSIX runner, use a small checked-in script or equivalent shell-native
check that prints unformatted files and exits unsuccessfully. Add Staticcheck or
golangci-lint only when the repository configures and maintains it; pin the tool
through the project's chosen mechanism.

### Modules, Tests, and Build

Use the checked-in module graph and fail if module metadata is untidy:

```console
go mod download
go mod verify
go test ./...
go build ./...
```

To enforce tidy module files, run `go mod tidy` in CI and fail if `go.mod` or
`go.sum` changes. Do not commit the generated diff from CI.

Run the race detector when the code contains concurrency or the repository's
quality policy requires it:

```console
go test -race ./...
```

Race testing normally runs on one supported platform rather than every matrix
entry. Add integration tests with explicit services, credentials, and timeouts;
do not hide network-dependent tests inside the ordinary unit suite.

### Vulnerability Scanning

Install or invoke an explicitly selected current compatible `govulncheck`
version and run:

```console
govulncheck ./...
```

Keep vulnerability scanning visible as its own check when ownership and response
policy differ from unit tests. Do not ignore all findings because some are not
reachable; report tool context and assess reachable findings.

## Caching and Artifacts

Use the supported Go setup action's module and build cache behavior when it
matches repository policy. Keys must account for the runner, Go version, and
`go.sum`. Cache only regenerable module and build data and never credentials.

Upload binaries, coverage, or test reports only when another job or reviewer
uses them. For releases, rebuild or promote through a separately authorized
workflow with provenance and artifact verification rather than publishing from
an untrusted pull-request job.

## Workflow Review

- The Go version comes from the module compatibility contract.
- Current action releases are locked or full-SHA pinned.
- `gofmt`, `go vet`, tests, and build failures fail the job.
- `go mod tidy` cannot silently rewrite the branch.
- Race detection and vulnerability scanning match the project's risk and policy.
- The matrix tests only versions and platforms the project supports.
- Pull-request jobs have read-only permissions and no unnecessary secrets.
