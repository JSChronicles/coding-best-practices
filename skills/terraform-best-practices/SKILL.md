---
name: terraform-best-practices
description: Creates, edits, reviews, explains, and refactors Terraform .tf and .tfvars code, modules, providers, state, CI checks, and project layouts. Use when user asks to "write Terraform", "review Terraform", "fix tf files", "add a module", "configure providers", "validate Terraform", or "plan infrastructure".
metadata:
  author: JSChronicles
  version: "0.10"
---

# Terraform

Use this skill to produce Terraform that is readable, maintainable, safe to review, and aligned with practical Terraform best practices.

Prefer Terraform that is boring, explicit, and easy to review. Do not over-engineer layout, modules, or abstractions.

## Core Rules

- Put all Terraform source code under `terraform/`. Do not place `.tf` files at the repository root.
- Use predictable module interface files: `main.tf`, `variables.tf`, and `outputs.tf`.
- Use `providers.tf` and `versions.tf` in root modules when provider configuration and version constraints are needed.
- Keep implementation flexible. Add files only when they improve understanding.
- Organize files by purpose, capability, lifecycle, or ownership boundary, not by provider resource type by default.
- Keep locals close to the code that uses them. Use `locals.tf` only for values genuinely shared across the module.
- Create modules only when they provide clear value: reuse, standardization, governance, complexity hiding, or a meaningful system boundary.
- When Terraform creates generated or dynamic file content, prefer `templatefile`
  with a `.tftpl` template over large inline heredocs or repetitive string/list
  assembly. Keep Terraform responsible for resolving data and let the template
  carry the file shape.
- Use explicit input types, useful descriptions, validations where helpful, and `sensitive = true` where needed.
- Expose useful outputs, not entire provider resources.
- Configure providers in root modules. Child modules may declare provider requirements but should usually not configure providers.
- Use remote state for shared, team-managed, or production infrastructure.
- Never commit state files, `.terraform/`, secrets, or unprotected plan artifacts.

## Workflow

1. Inspect the existing repository layout and Terraform conventions before editing.
2. Confirm whether the task touches a root module, child module, reusable public module, or review-only workflow.
3. Keep the structure proportional to the amount of Terraform present.
4. Prefer small, explicit changes over broad refactors.
5. Use current stable Terraform and provider versions for new projects, but verify current versions before writing constraints.
6. Run `terraform fmt -recursive` after edits when Terraform is available.
7. Run `terraform init`, `terraform validate`, and a plan when practical and appropriate for the task.
8. Clearly state any validation that could not be run.

## Reference Loading

Load only the reference files needed for the current task:

- For project structure, root modules, child modules, nested modules, README expectations, and file splitting, read `references/layout.md`.
- For variables, type constraints, locals, outputs, naming, providers, and defensive Terraform patterns, read `references/module-authoring.md`.
- For Terraform and provider version constraints, lock files, upgrades, state, backends, secrets, and CI/CD, read `references/operations.md`.
- For Terraform code reviews, read `references/review-checklist.md`.

## Review Behavior

When reviewing Terraform, lead with concrete risks and line-specific findings. Prioritize state safety, destructive changes, secrets exposure, provider/version drift, missing validation, unsafe CI apply behavior, and unclear module interfaces.

If no issues are found, say so directly and mention any validation gaps.

## Final Rule

Keep Terraform boring, explicit, reviewable, and proportional to the problem.
