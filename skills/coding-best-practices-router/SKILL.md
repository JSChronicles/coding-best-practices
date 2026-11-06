---
name: coding-best-practices-router
description: Routes ambiguous, repository-wide, or mixed-technology coding requests to the smallest useful set of included best-practices skills. Use when deciding among Python, PowerShell, and Terraform guidance, when a request spans more than one of them, or when the user asks which coding-best-practices skill applies.
---

# Coding Best Practices Router

Select and load the smallest useful set of skills from this plugin. Route the
request; do not repeat the specialized skills' guidance here.

## When to Route

Use this router when the request:

- does not clearly identify one supported technology;
- asks for a repository-wide or cross-language review;
- spans Python, PowerShell, and/or Terraform; or
- explicitly asks which coding-best-practices skill to use.

When the request already identifies exactly one supported technology and its
specialized skill is available, use that skill directly. Re-route only when the
task pivots or expands to another technology.

## Routing Process

1. Prefer the user's explicit target, named technology, and referenced files.
2. If the target is ambiguous, inspect only enough project evidence to identify
   the relevant technology or technologies.
3. Select the minimal matching skill set from the table below.
4. Read every selected `SKILL.md` before acting. Load its references only when
   the selected skill says they are relevant.
5. Apply each skill only to the files and concerns it owns.

| Evidence or request | Load |
| --- | --- |
| Python, `.py`, `pyproject.toml`, Python packaging, pytest, type hints | `../python-best-practices/SKILL.md` |
| PowerShell, `.ps1`, `.psm1`, `.psd1`, Pester, PSScriptAnalyzer | `../powershell-best-practices/SKILL.md` |
| Terraform, `.tf`, `.tfvars`, HCL, providers, modules, state, plans | `../terraform-best-practices/SKILL.md` |

Do not infer a technology from vendored dependencies, virtual environments,
generated output, build artifacts, or fixtures unless the request targets those
files. In a monorepo, route by the requested file or subproject rather than the
repository's dominant language.

## Mixed-Technology Requests

Load multiple skills only when the requested work crosses their ownership
boundaries. Examples:

- A Python tool that generates or validates Terraform: load Python for the
  application code and Terraform for the generated HCL and infrastructure
  contract.
- A PowerShell deployment wrapper around Terraform: load PowerShell for the
  wrapper and Terraform for commands, state safety, plan/apply behavior, and
  module changes.
- A repository-wide review containing all three technologies: load all three,
  then report findings against the file type each skill owns.

When multiple skills apply, follow stronger repository-local instructions and
resolve overlap by artifact: the language skill owns its language and runtime;
the Terraform skill owns Terraform configuration, state, and infrastructure
operations.

## Unsupported or Unclear Technologies

If no included skill matches, do not fabricate one or force the request into the
closest language. Follow the repository's local instructions and general
engineering practices. State the catalog gap only when it helps the user.

If two routes remain equally plausible and the choice would materially change
the work, ask one focused question about the target file or technology.

## Router Maintenance

When a new specialized skill is added to this plugin, add one discriminating
row to the routing table and update mixed-technology ownership only if the new
skill creates a real overlap.
