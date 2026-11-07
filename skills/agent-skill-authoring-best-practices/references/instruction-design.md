# Instruction Design

Write instructions that change decisions, preserve intent, and remain usable by
an agent that did not participate in the original design discussion.

## Activation Metadata

The name should be short, stable, and distinguishable. The description should
state the capability and recognizable activation conditions: target artifacts,
request types, or operating context. Include exclusions only when they prevent a
likely misroute.

Avoid descriptions that claim every task in a broad domain. A skill that creates
Terraform modules is different from one that operates production infrastructure
even if both concern Terraform.

## Entrypoint Content

Open with the outcome and the perspective the skill brings. Then define:

1. evidence to inspect before acting;
2. mode or scope selection when multiple paths exist;
3. essential domain rules and invariants;
4. implementation or review workflow;
5. safety, authorization, and stopping boundaries;
6. conditional reference and resource loading;
7. validation and final reporting.

Use fixed ordering only where order affects correctness. For exploratory or
creative work, state selection criteria and output quality rather than forcing a
ceremonial sequence.

## Rules and Guardrails

Write a rule when it protects correctness, safety, compatibility,
maintainability, or a deliberate project standard. Explain the condition or
reason when the rule would otherwise look arbitrary.

Separate:

- **must:** a correctness, safety, format, or user requirement;
- **default:** the preferred choice absent contrary repository evidence;
- **option:** a valid choice under stated conditions;
- **example:** one illustration, not an implicit mandate.

Keep authorization explicit. Inspection permission does not imply permission to
edit; editing does not imply permission to publish, deploy, message, or mutate an
external system.

## Examples and Templates

Use examples to resolve genuine ambiguity, demonstrate a fragile structure, or
show expected depth. Do not include many near-duplicate examples or allow sample
names and versions to become accidental requirements.

Templates should mark required substitutions, omit fake secrets, and remain
valid after placeholders are resolved. Explain what may be removed or extended.
Store reusable output templates as assets instead of burying large copies in the
entrypoint.

## Expected Outputs

Specify what the user needs to receive: changed artifacts, a findings-first
review, a plan, a validation report, or a concise summary. Include evidence and
remaining gaps where correctness depends on actions that may not run.

Avoid rigid headings when they add no value. Require exact schemas or sections
when another tool consumes the output or a review process depends on them.

## Common Weak Patterns

- A broad topic description with no activation boundary.
- Generic advice without a workflow or decision criteria.
- A large entrypoint that loads every edge case every time.
- Critical safety rules hidden only in a reference.
- References that are never linked or have no load condition.
- Scripts or templates added without validation or ownership.
- Absolute rules derived from one example or one tool preference.
- Permission expansion disguised as workflow convenience.
- Validation that checks wording instead of observable behavior.
- Product-specific terminology throughout a supposedly portable skill.
