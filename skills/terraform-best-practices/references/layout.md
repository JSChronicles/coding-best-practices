# Terraform Layout

## Directory Rule

All Terraform source code belongs under `terraform/`.

Preferred:

```text
repository/
├── README.md
├── terraform/
│   ├── README.md
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── providers.tf
│   └── versions.tf
└── ...
```

Avoid:

```text
repository/
├── README.md
├── main.tf
├── variables.tf
├── outputs.tf
└── ...
```

The repository root may contain project-level files such as `.github/`, `docs/`, `scripts/`, `policy/`, `Makefile`, and `.pre-commit-config.yaml`.

## Module Definitions

- Root module: deployable entry point for an environment, stack, or project.
- Child module: reusable module called by a root module or another module.
- Nested module: private implementation detail inside another module's `modules/` directory.

Nested modules should exist only when they improve the parent module implementation. Do not create nested modules to hide a small number of obvious resources.

## Baseline Files

Every root module and child module should generally have:

- `main.tf`: resources, data sources, and module calls.
- `variables.tf`: all input variables and the input contract.
- `outputs.tf`: useful output values and the output contract.

Root modules usually also have:

- `README.md`: structure, usage, requirements, workflows, state, environments, modules, and safety notes.
- `providers.tf`: provider configuration.
- `versions.tf`: Terraform and provider constraints.

For child modules, `providers.tf` and `versions.tf` are optional but useful when they improve clarity. Child modules should declare provider requirements when appropriate, but provider configuration should usually stay in the root module.

Private child modules do not automatically need a README. Add one only when it improves usability, documents non-obvious behavior, or explains an interface consumers need to understand.

## Reusable Modules

Use `terraform/modules/` for reusable modules:

```text
repository/
├── README.md
├── terraform/
│   ├── README.md
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── providers.tf
│   ├── versions.tf
│   └── modules/
│       └── example_module/
│           ├── main.tf
│           ├── variables.tf
│           └── outputs.tf
└── ...
```

For reusable public modules, add a module README and examples when they improve usability:

```text
terraform/
  modules/
    example_module/
      main.tf
      variables.tf
      outputs.tf
      examples/
        basic/
          main.tf
        complete/
          main.tf
```

Examples should be realistic and runnable where practical. Avoid examples that show every option at once without explaining why.

## File Splitting

Use proportional structure. Do not over-split small modules.

Organize Terraform by purpose, not provider resource type. A useful file usually contains the variables, locals, data sources, resources, module calls, and outputs needed for one related concern.

Good file names describe reader intent or infrastructure purpose:

- `application_service.tf`
- `load_balancer.tf`
- `github_oidc.tf`
- `centralized_logging.tf`
- `network_boundary.tf`
- `state_backend.tf`
- `dns_records.tf`

For example, `load_balancer.tf` may contain `aws_lb`, target groups, listeners, security groups, rules, alarms, and related locals. That is acceptable because the file is organized around the load balancer capability.

Avoid resource-type files by default:

- `s3.tf`
- `iam.tf`
- `security_groups.tf`
- `policies.tf`
- `cloudwatch.tf`

These are reasonable only when that resource type is itself the concern or the amount of related code is large enough to make the split easier to read. For example, `iam.tf` can be reasonable in a module that manages several roles, policies, permission boundaries, trust policies, and attachments.

Keep small supporting resources near the feature they support.

Preferred:

```text
application_service.tf
  ECS service, task definition, service role, log group, security group, alarms, and related locals
```

Usually avoid:

```text
ecs.tf
iam.tf
logs.tf
security_groups.tf
```

when those files only exist to support the same application service.

Split files only when the split improves readability, reviewability, or ownership.
