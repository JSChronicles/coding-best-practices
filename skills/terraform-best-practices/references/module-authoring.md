# Module Authoring

## Variables

Every module must have a `variables.tf` file. Treat it as the module input contract.

Each variable should include:

- Clear `description`
- Explicit `type`
- `default` only when appropriate
- `sensitive = true` when needed
- `validation` blocks for important assumptions

Example:

```hcl
variable "application_name" {
  description = "Name of the application."
  type        = string

  validation {
    condition     = length(var.application_name) > 0
    error_message = "application_name must not be empty."
  }
}

variable "environment" {
  description = "Deployment environment."
  type        = string

  validation {
    condition     = contains(["dev", "test", "stage", "prod"], var.environment)
    error_message = "environment must be one of: dev, test, stage, prod."
  }
}

variable "tags" {
  description = "Tags applied to supported resources."
  type        = map(string)
  default     = {}
}
```

Do not scatter variable declarations across unrelated files.

Avoid vague variables such as `config`, `data`, `items`, `list`, `map`, and `name`.

Prefer descriptive variables such as:

- `vpc_cidr_block`
- `private_subnet_cidr_blocks`
- `application_name`
- `environment`
- `permissions_boundary_arn`
- `cloudwatch_log_retention_days`

## Type Constraints

Use explicit types. Terraform type constraints are the equivalent of type hints.

Prefer:

```hcl
variable "subnets" {
  description = "Subnet definitions keyed by logical subnet name."

  type = map(object({
    cidr_block        = string
    availability_zone = string
    public            = bool
  }))
}
```

Avoid:

```hcl
variable "subnets" {
  type = any
}
```

Use `any` only when there is a clear reason.

## Locals

Do not centralize all local values in `locals.tf` by default.

Locals are implementation details. Keep them close to the resources, data sources, modules, or outputs that use them. Prefer placing locals near the top of the relevant file.

Example:

```hcl
locals {
  task_execution_role_name = "${var.application_name}-${var.environment}-task-execution"
}

resource "aws_iam_role" "task_execution" {
  name = local.task_execution_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}
```

A dedicated `locals.tf` is acceptable for values genuinely shared across the module, such as common tags and a name prefix.

Avoid putting every computed value in `locals.tf` when most values are used by only one resource or one file.

## Outputs

Use `outputs.tf` for module outputs. Outputs should expose useful values, not entire resources.

Prefer:

```hcl
output "bucket_name" {
  description = "Name of the created S3 bucket."
  value       = aws_s3_bucket.this.bucket
}

output "bucket_arn" {
  description = "ARN of the created S3 bucket."
  value       = aws_s3_bucket.this.arn
}
```

Avoid:

```hcl
output "bucket" {
  value = aws_s3_bucket.this
}
```

Mark sensitive outputs:

```hcl
output "database_password_secret_arn" {
  description = "ARN of the database password secret."
  value       = aws_secretsmanager_secret.database_password.arn
  sensitive   = true
}
```

## Naming

Use descriptive names for variables, locals, resources, data sources, modules, outputs, and files.

Resource names should describe logical purpose.

Avoid:

```hcl
resource "aws_s3_bucket" "bucket" {}
resource "aws_iam_role" "role" {}
resource "aws_security_group" "sg" {}
```

Prefer:

```hcl
resource "aws_s3_bucket" "access_logs" {}
resource "aws_iam_role" "lambda_execution" {}
resource "aws_security_group" "alb_ingress" {}
```

Module names should describe the capability, system, or boundary they represent.

Avoid implementation-mechanics names such as `create`, `creation`, `build`, `deploy`, `stuff`, `misc`, `common`, and `shared`. Use `shared` or `common` only when the contents are truly shared or common.

## Providers

Root modules should configure providers.

Child modules should normally declare provider requirements but should not usually configure providers themselves.

Root module example:

```hcl
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.common_tags
  }
}
```

Use provider aliases deliberately for multiple regions or accounts:

```hcl
provider "aws" {
  region = var.primary_region
}

provider "aws" {
  alias  = "secondary"
  region = var.secondary_region
}

module "replica_bucket" {
  source = "./modules/s3_bucket"

  providers = {
    aws = aws.secondary
  }

  bucket_name = var.replica_bucket_name
}
```

Do not hide provider behavior in child modules unless the design specifically requires it.

## Defensive Design

Terraform does not have normal try/catch error handling. Defensive Terraform means:

- Validate inputs.
- Use explicit type constraints.
- Use preconditions and postconditions when useful.
- Mark sensitive values.
- Protect critical resources from accidental destruction.
- Make bad plans fail early.
- Make error messages clear.

Use lifecycle protection for critical resources:

```hcl
resource "aws_s3_bucket" "state" {
  bucket = var.state_bucket_name

  lifecycle {
    prevent_destroy = true
  }
}
```

Use preconditions where resource-specific assumptions must be true:

```hcl
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name

  lifecycle {
    precondition {
      condition     = length(var.bucket_name) >= 3
      error_message = "bucket_name must be at least 3 characters."
    }
  }
}
```

## Module Design

Create modules when they provide real value:

- Reuse across projects
- Standardize a repeated pattern
- Encapsulate provider or resource complexity
- Enforce security or governance defaults
- Provide a clean interface for a larger capability
- Reduce repeated Terraform across environments
- Represent a meaningful infrastructure capability or system boundary

Bad reasons to create a module:

- A file is mildly long
- A resource type appeared once
- A value was computed once
- The code feels more abstract
- Every resource needs its own wrapper
- The pattern is not stable yet

Prefer a simple root module first. Extract a module when repetition, reuse, or clarity justifies it.
