# Skill Composition

Read this reference only when the requested work genuinely spans more than one
installed skill.

## Ownership

| Concern | Owning skill |
| --- | --- |
| Python syntax, packaging, runtime, CLIs, logging, typing, and Python tests | `python-best-practices` |
| PowerShell syntax, streams, functions, modules, remoting, and Pester tests | `powershell-best-practices` |
| Terraform configuration, providers, modules, state, plans, backends, and apply safety | `terraform-best-practices` |
| GitHub Actions triggers, jobs, permissions, dependencies, runners, expressions, and CI/CD workflow security | `github-actions-best-practices` |
| Go packages, modules, APIs, errors, ownership, context, concurrency, and tests | `go-best-practices` |
| TypeScript types, runtime boundaries, modules, packages, async behavior, builds, and tests | `typescript-best-practices` |
| Pull request titles, descriptions, reviewer summaries, risks, verification, migrations, and follow-ups | `pull-request-description-writer` |
| Agent skill scope, activation, architecture, references, assets, scripts, validation, evaluation, portability, and maintenance | `agent-skill-authoring-best-practices` |

Repository-local instructions and the user's requested outcome apply across all
selected skills. Within that scope, let each specialized skill own its artifact
instead of translating another language's conventions onto it.

## Common Compositions

### Python and Terraform

Use Python guidance for the application or automation code. Use Terraform
guidance for emitted or validated HCL, module contracts, provider constraints,
state implications, and plan/apply safety.

### PowerShell and Terraform

Use PowerShell guidance for parameters, pipeline behavior, errors, streams,
logging, `ShouldProcess`, and tests. Use Terraform guidance for command
semantics, configuration, state safety, plan review, and apply behavior.

### Python and PowerShell

Use each language skill for its own scripts, interfaces, tests, and runtime.
Define the boundary between them explicitly when one launches the other,
including arguments, exit codes, structured output, and error propagation.

### GitHub Actions and Language or Infrastructure Skills

Use GitHub Actions guidance for workflow triggers, permissions, dependency
integrity, expressions, runners, caching, concurrency, and orchestration. Add
the Go, Python, PowerShell, or TypeScript skill when the task changes a
substantive inline program or referenced source file. Add the Terraform skill when the workflow
changes Terraform command semantics, state handling, plan review, apply safety,
or configuration.

Do not load every language skill merely because a workflow invokes its normal
test command. Prefer moving substantial inline logic into a repository script,
then let each skill own its corresponding artifact.

When the task creates or reviews a language-specific CI workflow, load both
skills even if no source file changes. The GitHub Actions skill owns triggers,
permissions, action resolution, lockfiles or SHA pins, concurrency, caching,
artifacts, and timeouts. The Go, Python, PowerShell, Terraform, or TypeScript
skill owns the toolchain version, formatting, analysis, build, test, coverage,
and deployment safety semantics for that technology.

For TypeScript CI, GitHub Actions owns workflow mechanics, action currency and
locking, permissions, caching, and orchestration. TypeScript owns the Node.js
support contract, selected package manager and lockfile commands, formatting,
linting, type checking, tests, builds, and package-consumer behavior.

### Repository-Wide Work

Load all matching skills only when the requested review or change includes
artifacts owned by each of them. Organize findings by severity and file rather
than producing separate repetitive reports per skill.

### Pull Request Descriptions

Use the pull request description skill as the output owner. Add a language,
Terraform, or GitHub Actions skill only when the diff contains subtle behavior
that requires specialized interpretation to summarize accurately. The
specialized skill supplies technical meaning; the pull request skill keeps the
result concise, evidence-based, and reviewer-focused.

### Agent Skill Authoring

Use the agent skill authoring skill as the owner of skill structure, activation,
progressive disclosure, safety boundaries, validation, evaluation, and
portability. Add a domain skill when the new skill encodes specialized technical
practice that must be checked for correctness. Add GitHub Actions guidance only
when the skill package includes workflow files; ordinary skill Markdown does not
require it.

## Composition Rules

- Read all selected entrypoints before implementation or review.
- Load only the references needed for the concrete subtask in each skill.
- Resolve overlap by artifact ownership; do not let the broadest skill dominate.
- Avoid duplicate findings. Attribute a cross-boundary issue to the layer where
  its fix belongs and mention downstream effects once.
- Validate each changed artifact with its normal tools when practical, but keep
  validation proportional to the request and available environment.
- A skill selection does not authorize unrelated refactors, deployments,
  applies, or other external changes.

## Extending Composition

When a new skill is added, document composition only for real boundaries it
shares with existing skills. Do not create a full pairwise matrix or speculative
rules for combinations that have no demonstrated workflow.
