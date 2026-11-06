# Terraform Review Checklist

When reviewing Terraform, check the highest-risk items first.

## Directory Structure

- Is all Terraform code under `terraform/`?
- Are there `.tf` files at the repository root that should move under `terraform/`?

## Project Layout

- Is the file structure proportional to the module size?
- Are unnecessary files avoided?
- Are private child-module READMEs used only when they add value?

## File Structure

- Are files organized by purpose rather than provider resource type?
- Are small supporting resources kept near the feature they support?
- Are resource-type files used only when they genuinely improve readability?

## Versioning

- Is the minimum Terraform version the version actually tested?
- Is the minimum provider version the version actually tested?
- Is the upper bound set before the next untested major version?
- Is `.terraform.lock.hcl` committed for deployed stacks?
- Does CI use `terraform init -lockfile=readonly` when a committed lock file should not change?
- Are Terraform CLI versions pinned in CI and aligned with `required_version`?

## Variables

- Are all inputs in `variables.tf`?
- Do variables have descriptions?
- Do variables have explicit types?
- Are validations present where useful?
- Are sensitive values marked?

## Locals

- Are locals close to where they are used?
- Is `locals.tf` used only for genuinely shared values?

## Naming

- Are variables, resources, modules, and outputs descriptive?
- Are vague names avoided?
- Are lowercase underscore names used consistently?

## Providers

- Are provider versions constrained?
- Are provider configs kept in the root module?
- Are aliases used deliberately?
- Are provider, backend, account, and region assumptions explicit?

## State

- Is remote state used for shared infrastructure?
- Is state protected and encrypted?
- Are state files excluded from git?
- Is state locking enabled for apply?
- Are deploy workflows serialized by target environment or state?
- Do deploy workflows avoid canceling in-progress applies by default?

## Safety

- Are destructive resources protected where appropriate?
- Are secrets kept out of code and outputs?
- Are secrets kept out of committed tfvars and plan artifacts?
- Are plans reviewed before apply?
- Are apply workflows restricted to trusted branches or protected environments?
- Are speculative pull request plans prevented from becoming privileged apply artifacts without explicit mitigation?

## CI/CD And GitHub Actions

- Are pull request workflows limited to format, validation, lint, security scanning, and speculative plans?
- Are apply workflows separated from pull request validation workflows?
- Are GitHub Actions `permissions` minimal and job-scoped?
- Is GitHub OIDC or equivalent workload identity used instead of long-lived cloud keys where practical?
- Are role ARNs, regions, account IDs, and environment names stored as non-secret configuration?
- Are credentials, private values, tokens, and sensitive Terraform variables stored as secrets?
- Are GitHub environments used for deployment approval gates or environment-scoped roles where appropriate?
- Are workflow artifacts, plan files, and required environment values checked before use?
- Do workflows fail clearly when required validation, artifacts, variables, or secrets are missing?

## Quality

- Does `terraform fmt` pass?
- Does `terraform validate` pass?
- Is linting or security scanning used where appropriate?
- Is `.terraform.lock.hcl` committed where appropriate?

## Review Response Shape

For a code review, lead with findings ordered by severity. Use exact file and line references where possible.

Focus especially on:

- Destructive changes that could be applied accidentally
- State exposure or weak backend configuration
- Secrets in code, outputs, tfvars, plans, artifacts, or workflow logs
- Unreviewed apply paths in CI
- Unsafe GitHub Actions permissions or credential handling
- Pull request plan artifacts crossing into privileged apply workflows
- Missing input validation for important assumptions
- Provider aliases or configurations that change deployment account or region
- Broad version constraints not matching tested versions
- Missing lock files or CI that mutates lock files unexpectedly
- Apply workflows that disable locking, run concurrently against one state, or cancel in-progress applies

If no findings are present, say that clearly and list any commands that were not run.
