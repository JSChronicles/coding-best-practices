---
name: powershell-best-practices
description: Creates, edits, reviews, explains, and refactors PowerShell 7.6+ scripts, modules, advanced functions, classes, pipeline behavior, error handling, ShouldProcess support, dynamic parameters, and concurrency. Use when the user asks to write PowerShell, review PowerShell, improve a script, explain PowerShell behavior, build a module, or learn PowerShell best practices.
metadata:
  author: JSChronicles
  version: "0.10"
---

# PowerShell Best Practices

Use this skill to produce professional PowerShell 7.6+ code that is clear, typed, documented, pipeline-friendly, safe to execute, testable, and proportional to the problem.

Prefer idiomatic PowerShell over patterns copied from other languages. Use advanced functions, object output, structured error handling, comment-based help, standard streams, and PSScriptAnalyzer-friendly style.

Do not over-engineer. Avoid unnecessary classes, wrappers, dynamic parameters, custom concurrency, global state, or abstractions unless they clearly improve readability, safety, reuse, performance, or correctness.

## Core Rules

- Target PowerShell 7.6 or higher.
- Use `[CmdletBinding()]` for reusable functions and scripts with cmdlet behavior.
- Use `begin`, `process`, and `end` blocks for advanced functions.
- Use `clean` only when there is meaningful cleanup work.
- Strongly type public parameters.
- Use validation attributes when they make invalid input fail early.
- Add comment-based help for public functions and scripts.
- Use `SupportsShouldProcess` for commands that create, update, delete, modify, send, start, stop, restart, enable, disable, or change state.
- Wrap operations that can fail in explicit `try`/`catch` blocks when handling adds value.
- Use `-ErrorAction Stop` when non-terminating cmdlet errors need to be caught.
- End every `try`/`catch` chain with a generic catch that calls `$PSCmdlet.ThrowTerminatingError($PSItem)`.
- Use `Write-Verbose`, `Write-Debug`, `Write-Warning`, and `Write-Error` for their intended streams.
- Do not use `Write-Host` for logging. If console mirroring is explicitly needed, make it optional and keep file or structured logging as the source of truth.
- Output objects, not formatted strings, unless the command is specifically for display.
- Prefer `[pscustomobject]@{}` over `New-Object PSObject -Property`, and prefer `[Type]::new()` over `New-Object` when available.
- Use splatting for long command calls; avoid backtick line continuations.
- Filter as close to the data source as possible before using right-side pipeline filters.
- Never use `+=` to build arrays in loops; output from the loop into a variable or use a generic list.
- Avoid aliases in scripts and reusable functions. Write full command names and prefer `$PSItem` over `$_`.
- Avoid external modules unless the user or repository explicitly allows them.
- Write code that should pass PSScriptAnalyzer.

## Reference Navigation

Read only the reference files needed for the current task:

- [advanced-functions.md](references/advanced-functions.md): function skeletons, `begin`/`process`/`end`, pipeline input, and default function shapes.
- [parameters-and-help.md](references/parameters-and-help.md): parameter attributes, validation, parameter sets, and comment-based help.
- [credentials-and-remoting.md](references/credentials-and-remoting.md): `PSCredential` parameters, `[Credential()]`, conditional credential splatting, and remote session cleanup.
- [errors-and-streams.md](references/errors-and-streams.md): `try`/`catch`, terminating errors, `-ErrorAction Stop`, and stream usage.
- [logging.md](references/logging.md): preferred file logging patterns, simple log writer/parser functions, `PsLogger`, and optional console mirroring.
- [shouldprocess.md](references/shouldprocess.md): `SupportsShouldProcess`, `ShouldProcess()`, `-WhatIf`, `-Confirm`, and mutating command patterns.
- [module-design.md](references/module-design.md): module setup, folder layout, module naming, function naming, approved verbs, and exports.
- [objects-and-modeling.md](references/objects-and-modeling.md): object output, `[pscustomobject]`, classes, naming, and formatting boundaries.
- [performance.md](references/performance.md): array-building performance, avoiding `+=` in loops, and collection choices.
- [concurrency-and-caching.md](references/concurrency-and-caching.md): parallel execution, jobs, runspaces, throttling, cleanup, and caching.
- [pester-testing.md](references/pester-testing.md): Pester test structure, module import patterns, assertions, mocking, and CI usage.
- [project-quality.md](references/project-quality.md): module/script quality, dependencies, PSScriptAnalyzer expectations, and tests.
- [review-checklist.md](references/review-checklist.md): PowerShell review priorities and response shape.

## Default Workflow

1. Inspect the surrounding code before choosing patterns.
2. Follow existing repository conventions when they are reasonable.
3. Choose the smallest professional PowerShell design that meets the requirement.
4. Load relevant references for detailed patterns and examples.
5. Implement code that preserves pipeline behavior, error semantics, and output contracts.
6. Run targeted validation when possible, such as PSScriptAnalyzer or existing tests.
7. When reviewing, lead with concrete risks and exact file/line references.

## Final Rule

Keep PowerShell clear, typed, documented, pipeline-friendly, safe to execute, and proportional to the problem. Add validation, parameter sets, dynamic parameters, classes, caching, or concurrency only when they improve correctness, safety, maintainability, or usability.
