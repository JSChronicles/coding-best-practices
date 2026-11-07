# Technology Detection

Use project evidence only when the user has not already identified the target,
or when the request may span multiple technologies.

## Evidence Precedence

Use the first level that resolves the route:

1. Explicit technology, skill, file, directory, or subproject named by the user.
2. Files directly attached, referenced, selected, or changed for the task.
3. Technology-specific manifests, imports, commands, and test configuration.
4. Repository-wide file distribution and documentation.
5. A focused clarification when competing routes would materially change the
   work.

Stop inspecting once the evidence is sufficient. Do not scan an entire
repository to confirm a route that is already explicit.

## Current Fingerprints

| Technology | High-confidence signals | Supporting signals |
| --- | --- | --- |
| Python | Targeted `*.py`; `pyproject.toml` defining Python packages or tools | Python imports, pytest files, dependency and lock files, console entry points |
| PowerShell | Targeted `*.ps1`, `*.psm1`, or `*.psd1` | Pester tests, PSScriptAnalyzer settings, PowerShell commands in CI or documentation |
| Terraform | Targeted `*.tf` or `*.tfvars`; Terraform-specific blocks | `.terraform.lock.hcl`, `terraform` commands, provider/module/backend configuration |
| GitHub Actions | Targeted files under `.github/workflows/`; `action.yml` or `action.yaml`; `.github/workflows/actions.lock` | `uses:`, `runs-on:`, `workflow_call`, GitHub contexts and expressions, a `github-actions` Dependabot entry |
| Go | Targeted `*.go`; `go.mod` defining a module | `go.sum`, `go.work`, `_test.go`, `go:generate`, `go test`, `go vet`, Go imports and package declarations |
| TypeScript | Targeted `*.ts` or `*.tsx`; `tsconfig.json` or another targeted `tsconfig` | TypeScript compiler or test configuration, `typescript` in `package.json`, package-manager lockfiles, TypeScript imports and scripts |

## Disambiguation

- **Monorepos:** choose the requested package or file. Multiple technologies at
  the repository root do not make every task mixed.
- **Generators and wrappers:** when Python or PowerShell generates, validates,
  or orchestrates Terraform, route to both only if the requested work changes
  both the host-language behavior and Terraform semantics or operations.
- **Generic HCL:** require Terraform-specific syntax, files, or commands. Do not
  route Packer, Nomad, or other HCL configurations to Terraform by extension
  alone.
- **Configuration files:** YAML, JSON, TOML, Markdown, and CI files are evidence
  only when their requested content controls a supported technology. YAML routes
  to GitHub Actions only when its path or schema identifies a workflow or action.
- **Workflows containing language commands:** route to GitHub Actions for
  triggers, permissions, jobs, runners, expressions, dependencies, caching, or
  orchestration. Also route to a language skill only when the requested work
  changes substantive embedded code or a referenced script owned by that skill.
- **Language CI workflows:** when creating or reviewing formatting, linting,
  validation, build, test, coverage, or security jobs for an installed language
  or Terraform, route to both GitHub Actions and that technology skill even if
  the requested artifact is only workflow YAML. GitHub Actions owns workflow
  mechanics; the technology skill owns commands, matrices, and test semantics.
- **Go templates and generated files:** route generated `.go` output to Go only
  when the requested work intentionally changes generated behavior. Prefer the
  owning generator or template when generated-file markers identify one.
- **JavaScript versus TypeScript:** route JavaScript-only work to TypeScript only
  when the request also changes a TypeScript-owned contract, declaration, build,
  or configuration. A `package.json` or lockfile alone does not prove that the
  requested source work is TypeScript.
- **TSX frameworks:** route `*.tsx` syntax, types, runtime boundaries, and tests
  to TypeScript. Apply framework-specific project guidance when available; do
  not invent React, JSX runtime, or browser assumptions from the extension alone.
- **Embedded snippets:** a Terraform example inside Python or PowerShell
  documentation does not require the Terraform skill unless its correctness is
  part of the task.
- **Generated and third-party trees:** ignore `.venv`, `.terraform`, dependency
  caches, vendored code, generated reports, compiled output, and copied examples
  unless the user explicitly targets them.
- **Tests and fixtures:** route tests with the technology they exercise. Do not
  let an incidental fixture extension override the test's actual runtime.

## Unsupported Technologies

If the evidence points to a technology without an installed skill, do not map it
to the closest language. Use project-local instructions and ordinary engineering
judgment. A future catalog skill becomes routable only after its directory and
valid `SKILL.md` are included in the plugin and the routing table is updated.

## Cross-Technology Requests

A request to draft a pull request title, description, branch summary, testing
summary, migration note, or reviewer guidance routes to
`pull-request-description-writer` regardless of the implementation language.
Add a technology skill only when accurate interpretation of the change requires
its specialized semantics; do not load every language represented in the diff
for an ordinary summary.

A request to create, improve, review, validate, evaluate, or package a reusable
agent skill routes to `agent-skill-authoring-best-practices`. Product-specific
skill metadata or installation may require host guidance too, but the authoring
skill owns the portable scope, instructions, resources, and quality model.
