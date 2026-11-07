# Terraform GitHub Actions CI

Use this reference when creating or reviewing GitHub Actions for Terraform
formatting, initialization, validation, linting, security scanning, documentation,
or plans. Also apply `github-actions-best-practices` for action currency,
lockfiles or SHA pins, permissions, OIDC, concurrency, and timeouts.

Start from the
[Terraform validation template](../assets/github-workflow.yaml) when a new
workflow is requested. Resolve every placeholder and add lint, security, plan,
documentation, or deployment jobs only when the repository owns their policy.

When deployment automation is requested, create a second workflow from the
[Terraform deploy template](../assets/github-deploy-workflow.yaml). Never add an
apply job to the pull-request validation workflow.

Reference implementations:

- `JSChronicles/foundry-terraform-template/.github/workflows/terraform-validation.yaml`
- `JSChronicles/foundry-terraform-template/.github/workflows/tflint.yaml`
- `JSChronicles/foundry-terraform-template/.github/workflows/checkov.yaml`
- `JSChronicles/foundry-terraform-template/.github/workflows/terraform-docs.yaml`

Use these as behavioral examples, not as permission or action-version defaults.

## Required Two-Workflow Model

Terraform validation and deployment are separate trust boundaries and must use
separate workflow files.

### 1. Pull-Request Validation Workflow

The validation workflow runs first and must not apply infrastructure. Preserve
this order, skipping only stages the repository does not use:

1. Check out the pull-request commit without persisted credentials.
2. Install the exact Terraform CLI version.
3. Authenticate with the approved planning identity when the plan requires
   provider or backend access.
4. Run `terraform fmt -check -diff -recursive`.
5. Initialize for validation, using `-backend=false` when backend access is not
   required or the repository's read-only planning backend when it is.
6. Run `terraform validate`.
7. Run `terraform test` when test files exist.
8. Create the saved plan artifact consumed by deploy.
9. Upload the plan only after successful plan creation, with short retention
    and plan metadata that identifies the source commit and target.
10. Publish a bounded, sanitized plan summary for review.
11. Fail the workflow if any required stage failed.

Keep maintained lint and security workflows such as TFLint and Checkov as
required checks in their established positions. Do not move plan creation into
deploy to compensate for a missing check.

Formatting and plan steps may capture outcomes for reporting, but the final job
must still fail. When a deploy workflow exists, the validation/plan workflow is
responsible for producing its plan artifact; no other workflow may substitute a
new plan.

### 2. Trusted Deploy Workflow

The deploy workflow runs only from a trusted integration branch or explicit
manual dispatch. Preserve this order:

1. Confirm the trusted ref, actor policy, target environment, configured
   environment approval, and required validation status.
2. Enter a deploy concurrency group keyed to environment or state, with
   `cancel-in-progress: false`.
3. Check out the exact commit being deployed.
4. Install the same approved Terraform CLI version used for validation.
5. Authenticate with OIDC using the apply role.
6. Find the successful validation/plan workflow run associated with the change.
7. Fail if that successful run or its required plan artifact does not exist.
8. Download the saved plan and verify its source change, workflow, toolchain,
   lockfile, target environment, and artifact identity.
9. Initialize the real remote backend with state locking enabled.
10. Apply the downloaded saved plan exactly as produced. Do not run
    `terraform plan`, refresh the plan, or substitute a newly generated plan.
11. Record the deployed commit, plan identity, result, and relevant outputs
    without exposing secrets.

Branch protection should require the validation workflow before merge. The
deploy workflow must not infer that an arbitrary successful run or similarly
named artifact belongs to the change being deployed.

## Plan Artifact Identity

The Foundry template demonstrates locating a successful validation run and
downloading its saved plan. Preserve that promotion concept only when the plan
is safe to apply and identity checks prove all of the following:

- the plan came from the successful validation run associated with the change;
- the workflow and Terraform/provider lockfiles match;
- the target backend, workspace, account, region, and environment match;
- the plan came from a trusted workflow and was not replaceable by an untrusted
  actor;
- the artifact is protected, unexpired, and approved for deployment.

If the saved plan is missing, failed, expired, or does not satisfy the required
identity checks, deploy must stop. The plan workflow must be rerun through the
approved process to produce a replacement; deploy must not generate one.

## Baseline Validation

Run non-mutating checks for pull requests and the protected integration branch.
Start with `contents: read`, cancel stale runs, set job timeouts, and use the
repository's Terraform directory as the working directory.

A baseline validation job normally runs:

```console
terraform fmt -check -diff -recursive
terraform init -backend=false -input=false -no-color
terraform validate -no-color
```

Use an exact Terraform version selected from the repository's `required_version`,
version file, or documented toolchain policy. Do not silently run whichever
Terraform release the setup action happens to install.

Keep formatting failures fatal. Do not use `continue-on-error` unless a later
step deliberately records the failure and the job still exits unsuccessfully.

## Linting and Security

Run TFLint when the repository maintains a TFLint configuration. Initialize
plugins from the checked-in config and keep plugin versions constrained.

Run Checkov or the repository's selected security scanner as a separate,
visible check. Use SARIF only when the repository or organization consumes it,
and grant `security-events: write` only to the job that uploads SARIF. Keep
scanner exceptions narrow, justified, and versioned.

Do not require every Terraform repository to use every scanner. The workflow
should reflect maintained policy rather than duplicate overlapping tools with
unowned findings.

## Plans

When deployment automation is enabled, the validation/plan workflow must create
the saved plan that deploy consumes. Backend access, provider credentials, cost,
and untrusted-code risk must be understood. Prefer OIDC and a narrowly scoped
planning identity. Never expose production credentials to untrusted fork code.

Use `-input=false`, preserve state locking unless an isolated validation backend
justifies otherwise, and ensure a failed plan fails the job. A saved plan can
contain sensitive values; do not upload it by default. If another trusted job
must consume it, use restricted artifacts, short retention, and an explicit
trust boundary.

If posting a plan summary to a pull request, sanitize and bound the output,
avoid secrets, use the minimum `pull-requests: write` permission in that job,
and update one stable bot comment instead of creating unlimited comments.

## Documentation and Deployment

Validate generated Terraform documentation in pull requests by regenerating and
failing on a diff. Do not push documentation changes from untrusted
pull-request workflows.

Keep apply or deployment workflows separate from validation. Require a reviewed
plan or equivalent approval, protected environments, OIDC, concurrency that
serializes the target environment, and explicit authorization. Validation
workflow creation never implies permission to apply infrastructure.

## Workflow Review

- Current action releases are locked or full-SHA pinned.
- Terraform and provider versions are explicit and compatible with lockfiles.
- Formatting, initialization, and validation failures are fatal.
- Elevated permissions exist only in jobs that need them.
- Plans do not expose secrets or bypass appropriate state locking.
- Documentation checks do not write to pull-request branches.
- Apply behavior is isolated, approved, serialized, and outside untrusted CI.
- Validation and deploy workflows preserve the required order, and any promoted
  plan is operationally tied to the validated change and target environment.
- Deploy contains no plan-generation step and fails closed when the successful
  plan workflow run or required artifact cannot be verified.
