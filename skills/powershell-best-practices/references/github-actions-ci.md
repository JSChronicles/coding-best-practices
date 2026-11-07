# PowerShell GitHub Actions CI

Use this reference when creating or reviewing GitHub Actions that format,
analyze, document, or test PowerShell. Also apply
`github-actions-best-practices` for current action releases, lockfiles or SHA
pins, permissions, concurrency, and timeouts.

Start from the adaptable
[PowerShell workflow template](../assets/github-workflow.yaml) when a new
workflow is requested. Resolve every placeholder and tailor module paths,
versions, warning policy, runner matrix, and documentation checks.

Reference implementations:

- `JSChronicles/foundry-powershell-template/.github/workflows/psscriptanalyzer.yaml`
- `JSChronicles/foundry-powershell-template/.github/workflows/pester.yaml`
- `JSChronicles/foundry-powershell-template/.github/workflows/powershell-docs.yaml`

Use their quality stages as examples, but resolve current dependencies and
adapt module paths, versions, and documentation policy to the target repository.

## Baseline Workflow Shape

Validate pull requests and pushes to the protected integration branch, with
manual dispatch when useful. Use `pwsh` explicitly, start with
`contents: read`, cancel stale validation runs, and set job timeouts.

Separate analysis and tests when independent required checks are valuable. Run
documentation validation only for modules that generate or enforce external
help.

### Formatting and PSScriptAnalyzer

Install an explicitly selected current compatible PSScriptAnalyzer release with
`Install-PSResource`. Do not silently install an unbounded latest module in a
reproducibility-sensitive workflow.

Formatting validation should enumerate owned `.ps1`, `.psm1`, and `.psd1`
files, exclude generated or vendored paths, compare each file with
`Invoke-Formatter`, and fail without rewriting the checkout.

Run `Invoke-ScriptAnalyzer` recursively with the repository's settings file
when present. Treat errors as failures. Decide whether warnings fail CI through
repository policy rather than accidentally ignoring all findings.

### Pester

Install a selected compatible Pester version, import the module explicitly, and
run tests against the same manifest or module boundary users import. A typical
command is:

```powershell
Invoke-Pester -Path './tests' -CI
```

Use a Pester configuration object when the repository configures coverage,
test-result output, tags, exclusions, or strict discovery. Ensure the process
exits unsuccessfully when tests fail; do not add `if: always()` to a validation
job in a way that masks failure semantics.

Test on Linux for cross-platform modules. Add Windows or macOS runners only
when the support contract or platform-specific behavior requires them. Never
claim cross-platform support from one operating-system run.

### Documentation

For modules using PlatyPS or generated external help, run generation in a clean
checkout and fail when the generated diff is nonempty. Ordinary pull-request CI
should verify documentation rather than commit or push changes with a write
token. Keep source help and generated output ownership documented.

## Dependencies and Caching

Pin development module versions through repository configuration or workflow
variables and update them deliberately. Use `PSResourceGet` rather than legacy
PowerShellGet commands for new workflows. Cache installed modules only when the
cache key includes OS, PowerShell version, module names, and versions and the
time saved justifies the added invalidation logic.

## Workflow Review

- Actions and PowerShell modules use current compatible releases and immutable
  dependency controls.
- Formatting checks but does not mutate the branch.
- PSScriptAnalyzer settings and warning policy are explicit.
- Pester imports the module like a consumer and reliably fails the job.
- The runner matrix matches the supported operating systems.
- Documentation generation is a check, not an unreviewed pull-request push.
- Pull-request jobs have no unnecessary secrets or write permissions.
