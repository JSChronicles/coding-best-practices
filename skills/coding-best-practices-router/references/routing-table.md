# Routing Table

This is the authoritative catalog of specialized skills available to the
router. Select the smallest set that owns the requested artifacts and concerns.

| Skill | Route when the request targets | Strong project or file signals | Primary ownership |
| --- | --- | --- | --- |
| [`python-best-practices`](../../python-best-practices/SKILL.md) | Python code, packages, CLIs, tests, typing, logging, concurrency, caching, or Python project structure | `*.py`, `pyproject.toml`, Python dependency or lock files, pytest configuration | Python syntax, runtime behavior, packaging, application structure, and tests |
| [`powershell-best-practices`](../../powershell-best-practices/SKILL.md) | PowerShell scripts, modules, advanced functions, pipeline behavior, remoting, Pester, or PSScriptAnalyzer | `*.ps1`, `*.psm1`, `*.psd1`, Pester tests, PowerShell module manifests | PowerShell syntax, streams, functions, modules, runtime behavior, and tests |
| [`terraform-best-practices`](../../terraform-best-practices/SKILL.md) | Terraform configuration, modules, providers, plans, state, backends, or Terraform automation safety | `*.tf`, `*.tfvars`, `.terraform.lock.hcl`, Terraform blocks and commands | Terraform configuration, module interfaces, provider constraints, state, plans, and apply behavior |
| [`github-actions-best-practices`](../../github-actions-best-practices/SKILL.md) | GitHub Actions workflows, reusable workflows, action metadata, dependency locking, permissions, OIDC, caching, or CI/CD workflow design | `.github/workflows/*.yml`, `.github/workflows/*.yaml`, `action.yml`, `action.yaml`, `.github/workflows/actions.lock`, GitHub Actions entries in `.github/dependabot.yml` | Workflow triggers, jobs, permissions, action dependencies, GitHub expression behavior, runners, and workflow security |
| [`go-best-practices`](../../go-best-practices/SKILL.md) | Go applications, libraries, commands, packages, modules, APIs, errors, context, concurrency, logging, or tests | `*.go`, `go.mod`, `go.sum`, `go.work`, Go tool commands and test files | Go syntax, package and API design, module behavior, ownership, errors, concurrency, and tests |
| [`typescript-best-practices`](../../typescript-best-practices/SKILL.md) | TypeScript applications, libraries, packages, types, runtime validation, async behavior, builds, dependencies, or tests | `*.ts`, `*.tsx`, `tsconfig*.json`, TypeScript scripts and test files, TypeScript dependencies in `package.json` | TypeScript syntax and types, runtime boundaries, module behavior, package structure, async behavior, builds, and tests |
| [`pull-request-description-writer`](../../pull-request-description-writer/SKILL.md) | Pull request titles, descriptions, branch summaries, reviewer notes, testing summaries, migration notes, or review guidance | An explicit PR-description request, local branch commits and diffs, pull request templates, contribution guidance | Reviewer-focused synthesis of change intent, behavior, risk, verification, migrations, and follow-up work |
| [`agent-skill-authoring-best-practices`](../../agent-skill-authoring-best-practices/SKILL.md) | Creating, reviewing, strengthening, validating, evaluating, or packaging reusable AI agent skills | An explicit skill-authoring request, `SKILL.md`, skill metadata, references, assets, helper scripts, skill catalogs or routers | Skill scope, activation, instruction architecture, progressive disclosure, safety boundaries, validation, evaluation, portability, and maintenance |

## Selection Rules

- An explicit user request or referenced file is stronger than repository-wide
  signals.
- A supported file type is enough when that file is the requested target.
- Manifests and tool configuration support a route but do not expand a focused
  request to unrelated files.
- Select multiple skills only when the requested change or review crosses the
  primary ownership columns above.
- Generic YAML, JSON, shell, HCL, or Markdown alone does not establish one of
  these routes. For example, HCL used by Packer or Nomad is not Terraform.

## Request Kinds

Writing, editing, reviewing, refactoring, explaining, and testing all route by
the technology that owns the artifact. The request kind changes which references
the selected skill loads; it does not require a separate router entry.

## Catalog Maintenance

Add a row only after the corresponding skill exists in the plugin. Keep signals
discriminating, state what the skill owns, and avoid copying its detailed rules
into this table.
