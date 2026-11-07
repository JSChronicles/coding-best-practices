---
name: agent-skill-authoring-best-practices
description: Designs, creates, reviews, and improves reusable AI agent skills with proportional depth, precise activation, progressive disclosure, supporting references, assets or scripts, safety boundaries, validation, and realistic evaluation. Use when asked to build a skill, strengthen a shallow skill, design a reusable agent workflow, or review skill quality and portability.
metadata:
  author: JSChronicles
  version: "0.1.0"
---

# Agent Skill Authoring Best Practices

Create reusable agent skills that improve real decisions and outcomes. A strong
skill is not merely longer: it has the depth, resources, guardrails, and testing
needed for its actual complexity while staying easy to discover and load.

Keep core instructions provider-neutral unless the requested capability depends
on one agent product. Put product-specific UI or packaging metadata outside the
portable skill instructions when the target format supports that separation.

## Authoring Workflow

1. Read the target repository instructions, skill format, validators, existing
   catalog conventions, and packaging rules before creating files.
2. Define realistic requests the skill should handle, nearby requests it should
   not capture, expected outputs, and important failure modes.
3. Select a complexity level from
   [scope-and-architecture.md](references/scope-and-architecture.md). Do not
   force a one-file skill onto a complex workflow or inflate a narrow skill into
   a documentation bundle.
4. Design the entrypoint, conditional references, deterministic scripts, and
   output assets around actual decision boundaries.
5. Write precise activation metadata, essential instructions, safety and
   authorization boundaries, the workflow, validation, and output expectations.
6. Validate structure and links, exercise scripts and assets, and run realistic
   behavioral evaluations using
   [validation-and-evaluation.md](references/validation-and-evaluation.md).
7. Review the finished package for trigger quality, depth, portability,
   contradictions, maintenance cost, and demonstrated usefulness.

## Core Rules

- Preserve the user's requested outcome, technology, workflow, and authority.
  A skill guides work; it does not silently broaden permission or replace user
  choices with the author's preferred stack.
- Write a discriminating name and description. The description must identify
  both what the skill does and when it should activate without becoming a
  catchall for adjacent work.
- Put essential purpose, invariants, safety rules, workflow, reference routing,
  and result expectations in the entrypoint. Do not hide critical behavior in a
  reference that may never load.
- Put conditional depth in references organized by decision area or operating
  mode. State exactly when each reference should be read.
- Use scripts when deterministic, repeated mechanics are safer or more reliable
  than regenerating commands. Use assets for templates or files that belong in
  generated output. Do not add empty resource directories.
- Include non-obvious, task-changing guidance. Remove generic advice an agent
  already follows, duplicated material, ornamental examples, and arbitrary
  rules that do not protect correctness or maintainability.
- Distinguish requirements, defaults, options, and examples. Avoid turning one
  past failure or one repository convention into a universal mandate.
- Define destructive, privileged, external, or production actions precisely.
  State what requires confirmation, how targets are resolved, and what evidence
  or stopping condition applies.
- Specify observable output quality and validation. Do not prescribe a rigid
  response template when several valid outputs exist, but do make critical
  deliverables and reporting obligations explicit.
- Add author and version metadata using the repository's convention. Increment
  the skill version when its behavior or resources change.
- Keep the package maintainable. Prefer one authoritative location for each
  rule, schema, template, or procedure and avoid copied product-specific forks.

## Depth Standard

For a complex or high-risk skill, do not stop after a short list of principles.
Provide the decision support the agent would otherwise have to rediscover:

- operating modes and selection criteria;
- artifact or project structure where it affects correctness;
- real invariants and ordering constraints;
- integration and permission boundaries;
- failure handling and stopping conditions;
- relevant templates, schemas, or deterministic helpers;
- validation commands and behavioral acceptance criteria;
- realistic positive, boundary, and non-trigger evaluations;
- maintenance ownership and versioning expectations.

For a narrow, low-risk skill, include only the subset that materially improves
performance. Complexity must be earned by the task.

## Reference Loading

- Read [scope-and-architecture.md](references/scope-and-architecture.md) when
  deciding skill scope, complexity, file layout, resources, or portability.
- Read [instruction-design.md](references/instruction-design.md) when writing or
  reviewing activation metadata, workflows, guardrails, examples, and output
  contracts.
- Read
  [validation-and-evaluation.md](references/validation-and-evaluation.md) when
  validating, testing, versioning, or diagnosing a skill that activates poorly
  or produces weak results.
- Use [review-checklist.md](references/review-checklist.md) for a final quality
  review or an assessment of an existing skill.
- Adapt [SKILL.template.md](assets/SKILL.template.md) when a new portable
  Markdown skill needs a starting structure; remove sections the skill does not
  need.

## Review Output

When reviewing a skill, lead with concrete findings ordered by impact. Identify
activation problems, missing decision logic, unsafe authority, contradictions,
unusable resources, weak validation, and maintenance risks before wording or
formatting preferences. If a simple skill is already sufficient, say so instead
of recommending complexity for its own sake.
