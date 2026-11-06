# Terraform Operations

## Terraform And Provider Versions

For new projects, use the latest stable Terraform 1.x version unless the user specifies otherwise. Do not target beta, release candidate, or experimental versions unless explicitly requested.

Use the latest stable provider major version appropriate for the project, but verify current versions before writing constraints.

Use explicit version constraints:

- Minimum version: the version actually tested.
- Upper bound: usually before the next untested major version.

Do not use a low minimum version just because the code might work with it. Do not claim broad compatibility unless the project is tested across that range.

Pattern:

```hcl
terraform {
  required_version = ">= X.Y.Z, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= A.B.C, < NEXT_MAJOR.0.0"
    }
  }
}
```

For a new project, `X.Y.Z` and `A.B.C` should normally be the current tested stable versions.

Commit `.terraform.lock.hcl` for deployed stacks. In CI, use `terraform init -lockfile=readonly` when a lock file is committed so provider changes are reviewed intentionally.

## Upgrades

When upgrading Terraform or providers:

1. Update the minimum version to the new tested version.
2. Run `terraform init -upgrade`.
3. Run `terraform validate`.
4. Run a Terraform plan.
5. Review provider release notes for breaking changes or behavior changes.
6. Commit the updated `.terraform.lock.hcl`.

## State And Backends

Use remote state for shared infrastructure. Do not use local state for team-managed, production, or shared environments.

Backend standards:

- Encrypt state.
- Enable locking where supported.
- Restrict access to state.
- Treat state as sensitive.
- Do not store secrets in state intentionally.
- Do not commit state files.
- Do not commit `.terraform/`.
- Do not commit plan files unless they are protected CI artifacts.

Common backend-related files:

- `backend.tf`
- `providers.tf`
- `versions.tf`

Keep backend configuration simple and explicit.

Do not disable state locking for apply. Use `-lock=false` only for speculative plans when concurrent pull request plans are an intentional and documented tradeoff.

## Secrets And Sensitive Data

Do not commit secrets to Terraform files or tfvars files.

Avoid putting secrets in:

- `.tf` files
- committed `.tfvars` files
- locals
- outputs
- plan artifacts
- backend configuration

Use secret managers or CI/CD secret injection.

Mark sensitive variables and outputs:

```hcl
variable "database_password" {
  description = "Database password."
  type        = string
  sensitive   = true
}
```

Remember that `sensitive = true` hides values in CLI output but does not remove them from Terraform state.

For CI cloud authentication, prefer short-lived credentials such as GitHub OIDC or equivalent workload identity. Store non-secret configuration such as role ARNs, regions, account IDs, and environment names in variables or environment-scoped configuration. Store credentials, tokens, and sensitive Terraform variables in secrets.

## Code Quality

Use these checks locally and in CI where practical:

- `terraform fmt -recursive`
- `terraform init`
- `terraform validate`
- `terraform plan`

Recommended CI checks:

- `terraform fmt -check -recursive`
- `terraform init -backend=false`
- `terraform init -lockfile=readonly` when validating a deployed stack with a committed lock file
- `terraform validate`
- `tflint`
- `terraform-docs`
- `checkov`

Security scanners may include `checkov`, `tfsec`, or `trivy`. Use whichever scanner is appropriate for the project.

General standards:

- Run `terraform fmt`.
- Run `terraform validate`.
- Use `tflint` where practical.
- Generate documentation with `terraform-docs` where useful.
- Require reviewed plans before apply.
- Separate plan and apply permissions for shared environments.
- Prefer short-lived cloud credentials such as OIDC in CI.
- Keep plans and artifacts protected.

## CI/CD Standards

For pull requests:

- Run format checks.
- Run validation.
- Run linting.
- Run security scanning where appropriate.
- Generate a speculative Terraform plan.
- Make the plan available for review.
- Canceling in-progress validation runs is usually acceptable when a newer commit supersedes the old run.

For apply:

- Apply only from trusted branches or approved environments.
- Use environment protection for production.
- Use remote state.
- Use short-lived credentials.
- Avoid local manual applies for shared infrastructure.
- Keep state locking enabled.
- Serialize deploys by target environment or state.
- Do not cancel in-progress applies by default.

Do not design workflows that apply unreviewed Terraform changes from pull requests.

## GitHub Actions Standards

Use explicit GitHub Actions behavior for Terraform repositories:

- Pin the Terraform CLI version in CI and keep it aligned with `required_version`.
- Use job-scoped `permissions` and grant only what the job needs.
- Prefer pinned action SHAs with version comments when that is the repository convention.
- Use `vars` for role ARNs, regions, environment names, and other non-secret configuration.
- Use `secrets` for credentials, tokens beyond `GITHUB_TOKEN`, private values, and sensitive Terraform variables.
- Use GitHub environments for deploy jobs that need approval gates or environment-scoped cloud roles.
- For deploy concurrency, key the group to the target environment or state, such as `terraform-deploy-production`, and set `cancel-in-progress: false`.
- For pull request validation concurrency, canceling in-progress runs is usually acceptable.
- Fail clearly when a required artifact, validation run, variable, secret, or environment value is missing.

Keep plan and apply trust boundaries clear. A plan generated from untrusted pull request code should not become the apply artifact for a privileged deploy unless the workflow has explicitly mitigated that trust boundary.

## Documentation

The repository should have a root `README.md`.

The `terraform/` directory should usually have a `README.md` explaining:

- Purpose
- Usage
- Requirements
- Providers
- Inputs
- Outputs
- State/backend behavior
- Important safety behavior
- Destructive behavior or lifecycle protection
- CI/CD workflow behavior
- Required variables, secrets, and environment approvals
- Examples, when useful

Reusable public modules should have a README. Private child modules should have a README only when it adds value.

Use `terraform-docs` when appropriate to generate input and output documentation. Do not manually maintain large input/output tables if they can be generated.
