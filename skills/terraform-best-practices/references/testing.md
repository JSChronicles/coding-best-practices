# Terraform Testing

Use Terraform tests to prove module behavior without making normal development slow, expensive, or risky.

Prefer a layered test strategy:

1. Static checks for formatting, validation, linting, and security scanning.
2. Mocked Terraform tests for fast module logic validation.
3. Real infrastructure tests only when provider or cloud behavior must be proven.

Terraform tests should improve confidence without polluting production module code. Keep test behavior in `.tftest.hcl` files.

## Testing Philosophy

Use mocked tests to validate module logic, input behavior, generated expressions, conditions, outputs, and resource shape.

Use real infrastructure tests to validate provider behavior, AWS-side constraints, dependencies, lifecycle behavior, and anything mocks cannot prove.

A mocked test can prove that Terraform would shape a plan a certain way. It cannot prove that AWS will accept, create, update, or operate the infrastructure correctly.

Do not treat testing as a reason to add unnecessary abstraction. Test the module interface and important behavior directly.

## Test Types

Use three broad test categories.

### Static Checks

Static checks should usually run before Terraform tests:

- `terraform fmt -check -recursive`
- `terraform init -backend=false`
- `terraform validate`
- `tflint`
- Security scanners such as `checkov`, `tfsec`, or `trivy` where appropriate

### Mocked Terraform Tests

Mocked Terraform tests are fast tests using `terraform test`.

They should usually:

- Use `.tftest.hcl` files.
- Use `command = plan` unless the test specifically needs apply behavior.
- Use `mock_provider`, `override_resource`, `override_data`, or `override_module` when useful.
- Avoid requiring cloud credentials where practical.
- Avoid creating real infrastructure.
- Validate module logic, rendered resource arguments, outputs, validations, and failure behavior.

### Real Infrastructure Tests

Real infrastructure tests use real providers and real credentials.

They may:

- Use `command = apply`.
- Create actual cloud resources.
- Validate provider behavior, AWS-side validation, lifecycle behavior, and resource interactions.

Real infrastructure tests should be isolated, tagged, disposable, and restricted to trusted workflows.

## Test File Layout

For a reusable module, prefer a simple `tests/` directory under the Terraform module being tested:

```text
terraform/
├── README.md
├── main.tf
├── variables.tf
├── outputs.tf
├── providers.tf
├── versions.tf
└── tests/
    ├── unit.tftest.hcl
    ├── integration.tftest.hcl
    └── fixtures/
        ├── basic/
        └── complete/
```

Keep test structure proportional. A small module can start with one file:

```text
terraform/
└── tests/
    └── unit.tftest.hcl
```

Do not create a large test hierarchy for a small module.

Use clear names such as:

- `unit.tftest.hcl`
- `validation.tftest.hcl`
- `waf_rules.tftest.hcl`
- `integration.tftest.hcl`
- `real_infra.tftest.hcl`

## Unit-Style Tests With Mocks

Use unit-style Terraform tests for behavior that can be proven from the plan, generated expressions, validations, and outputs.

Good candidates:

- Input validation behavior
- Conditional resource creation
- Dynamic blocks
- `for_each` and `count` behavior
- Locals and derived names
- Tag merging
- IAM policy document generation
- Rule generation
- Output shape
- Module wiring
- Preconditions and postconditions
- Expected failure cases

Prefer several focused tests over one large test that tries to cover every option.

## When To Mock

Use mocks when the test is validating Terraform logic rather than real provider behavior.

Mock when testing:

- Whether resources would be planned with expected arguments
- Whether inputs produce the expected resource shape
- Whether outputs are computed as expected
- Whether optional objects, maps, lists, or dynamic blocks are expanded correctly
- Whether module wiring passes expected values to child modules
- Failure paths that should happen before infrastructure is created
- Cases that would be slow, expensive, risky, or flaky with real infrastructure

Mock or override resources when creating them would make the test slow, expensive, flaky, quota-sensitive, or unsafe.

## What To Mock

Mock provider interactions that are not the point of the test.

Good mock targets:

- Provider data sources used only to look up existing infrastructure
- Caller identity lookups
- Region or partition lookups
- Existing VPC, subnet, KMS key, Route 53 zone, ACM certificate, or IAM role lookups
- Expensive resources unrelated to the assertion
- Slow dependencies that only provide IDs, ARNs, or names
- External modules that are not under test

Common AWS values to mock:

- Account ID
- Partition
- Region
- ARNs
- VPC IDs
- Subnet IDs
- Security group IDs
- KMS key ARNs
- ACM certificate ARNs
- Route 53 zone IDs
- IAM role ARNs

Mock dependencies. Do not mock the behavior the test is supposed to prove.

## Overrides For Slow, Expensive, Or Risky Infrastructure

Use Terraform test overrides for resources that should not be created during normal test runs because they are slow, expensive, risky, quota-sensitive, global, or unnecessary for the behavior being tested.

Common examples:

- RDS databases and clusters
- OpenSearch domains
- ElastiCache clusters
- NAT gateways
- Load balancers when the load balancer itself is not under test
- AWS Shield Advanced protections
- AWS WAF configurations where the test is not specifically validating real WAF behavior
- CloudFront distributions
- Resources with long creation or deletion times
- Resources with meaningful hourly cost
- Resources with account-level, regional, or global side effects

Prefer `override_resource`, `override_data`, or `override_module` in Terraform test files instead of adding test-only switches, fake variables, conditional resource branches, or testing hooks to the module itself.

Production module code should not be changed to support mocks. Test overrides belong in `.tftest.hcl` files.

Do not add module variables such as:

- `create_rds = false`
- `enable_test_mode = true`
- `mock_waf = true`
- `skip_expensive_resources = true`
- `use_fake_ids = true`

Those flags pollute the module interface and can create production ambiguity.

If a module genuinely needs feature flags for production use, they must be justified by real consumer behavior, not only by tests.

## When Not To Mock

Do not rely only on mocks when validating behavior that depends on real provider or cloud behavior.

Use real infrastructure tests when validating:

- Whether AWS accepts the final resource configuration
- Provider-side defaults
- Provider-side validation
- API constraints
- Resource lifecycle behavior
- Resource replacement behavior
- Cross-resource dependencies
- IAM permission behavior
- AWS service quotas or naming constraints
- Eventual consistency behavior
- Service-specific behavior that Terraform schema alone cannot prove

Even when a resource should eventually be tested with real infrastructure, it can still be overridden in routine tests if creating it is too slow, too expensive, or too risky. In that case, keep a smaller number of explicitly approved integration tests for real infrastructure behavior.

## Integration Tests With Real Infrastructure

Create real infrastructure when correctness depends on AWS behavior, not just Terraform configuration shape.

Use real infrastructure tests for:

- Reusable public modules
- Security-sensitive modules
- Modules with complex provider behavior
- Modules with multiple resources that must work together
- Modules using service features with strict AWS-side validation
- Modules where provider mocks would hide the real risk

Real infrastructure tests should be narrower than mocked tests. They should prove the critical path, not every input permutation.

## Real Infrastructure Test Safety

Real infrastructure tests must be isolated, tagged, and disposable.

Rules:

- Use a dedicated test AWS account or sandbox where practical.
- Use short-lived credentials such as GitHub OIDC.
- Use unique names with a random or CI run suffix.
- Apply common tags that identify owner, repository, test suite, and expiration.
- Avoid production accounts.
- Avoid shared state unless the test is specifically validating shared state behavior.
- Keep test resources small and low-cost.
- Prefer regional resources over global resources when possible.
- Explicitly document any resources that may incur cost.
- Ensure test-created resources are destroyed after apply tests.
- Do not run destructive integration tests automatically against protected environments.
- Do not run expensive or long-running apply tests on every pull request.

## Assertions

Assertions should validate meaningful behavior.

Good assertions check:

- Resource count or presence
- Important arguments
- Derived names
- Tags
- Rule priorities
- Rule actions
- Provider alias wiring
- Output values
- Validation failures
- Preconditions and postconditions

Avoid assertions that only restate the input value without proving module behavior.

Prefer direct, readable assertions over clever expressions.

## AWS-Specific Testing Guidance

For AWS modules, use mocked tests for routine validation and selective real infrastructure tests for behavior AWS must prove.

Mock or override:

- Account identity and partition data sources
- Region lookups
- Existing network lookups
- Existing KMS, ACM, IAM, and Route 53 dependencies
- Long-running infrastructure such as RDS, OpenSearch, ElastiCache, CloudFront, and load balancers when they are not the behavior under test
- Expensive or sensitive controls such as AWS Shield Advanced

Use real infrastructure tests when validating:

- Whether AWS accepts service-specific resource combinations
- Whether provider aliases deploy resources to the intended region or account
- Whether dependencies work together after apply
- Whether lifecycle or replacement behavior matters
- Whether IAM permissions actually allow the desired operation

## AWS WAF Module Testing Guidance

For an AWS WAF module, mocked tests are useful for checking that Terraform renders the expected Web ACL shape.

Mocked tests can validate:

- Single Web ACL creation
- Multiple Web ACL creation
- Single IP set behavior
- Multiple IP set behavior when applicable
- One IP set per scope and region when the module owns IP set creation
- IP set references from Web ACL rules
- Rate-based rule rendering
- Managed rule group rendering
- Managed rule action mode, such as count or block
- Rule priority ordering
- Visibility config behavior
- CloudWatch metric names
- Regional versus CloudFront scope wiring

Use overrides when WAF resources are not the specific behavior under test or when creating them would make the test slow, expensive, quota-sensitive, or risky.

Use real infrastructure tests only for the smaller set of behavior that AWS must prove, such as:

- AWS accepting the final Web ACL configuration
- IP set and Web ACL compatibility by scope and region
- Managed rule group names and vendor names being valid
- Rule action overrides behaving as expected in the provider schema
- Provider alias behavior for regional or CloudFront-scoped resources

Do not modify the WAF module code to support test overrides. Keep overrides in `.tftest.hcl` files.

## CI/CD Testing Flow

For pull requests:

1. Run static checks:
   - `terraform fmt -check -recursive`
   - `terraform init -backend=false`
   - `terraform validate`
   - `tflint`
   - Security scanner where appropriate

2. Run mocked tests:
   - `terraform test`
   - No cloud credentials required where practical
   - No real infrastructure by default

3. Optionally run speculative plans:
   - Use read-only or restricted credentials
   - Do not apply from pull request code

For trusted branches, protected environments, or manually approved workflows:

1. Run integration tests with real infrastructure.
2. Use protected environments where appropriate.
3. Use short-lived credentials.
4. Keep apply permissions separate from pull request validation.
5. Keep expensive tests opt-in or scheduled unless they are essential.

Do not design workflows that apply unreviewed Terraform changes from pull requests.

## Review Checklist Additions

When reviewing Terraform tests, check:

- Are Terraform tests present for reusable or complex modules?
- Are mocked tests used for fast validation of module logic?
- Are mocks limited to dependencies and provider-returned values rather than hiding the behavior under test?
- Are slow, expensive, risky, or quota-sensitive resources overridden in test files instead of created by default?
- Are test overrides kept in `.tftest.hcl` files instead of production module code?
- Are real infrastructure tests used where provider or AWS behavior must be proven?
- Are integration tests isolated from production?
- Are test resources uniquely named, tagged, and disposable?
- Are costly or global resources avoided unless necessary?
- Are PR workflows limited to safe validation and mocked or speculative tests?
- Are real apply-style tests restricted to trusted branches, protected environments, scheduled runs, or manual approval?
- Does CI clearly separate static checks, mocked tests, plans, and real infrastructure tests?
