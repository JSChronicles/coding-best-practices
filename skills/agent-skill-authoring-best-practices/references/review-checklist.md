# Agent Skill Review Checklist

Lead with concrete issues that can cause wrong activation, weak decisions,
unsafe behavior, invalid output, or maintenance drift.

## Scope and Discovery

- Does the description clearly state capability and activation conditions?
- Are adjacent requests excluded when misrouting is likely?
- Is the skill focused on repeatable work rather than a one-off prompt?
- Does it preserve user choices and repository-local instructions?

## Depth and Architecture

- Is complexity proportional to the workflow and risk?
- Does the entrypoint contain essential invariants, workflow, safety, routing,
  validation, and output expectations?
- Are references split by real decision area and loaded conditionally?
- Do scripts provide deterministic value with documented failure behavior?
- Are assets valid, adaptable, and intended for generated output?
- Are there unused, duplicated, or unreachable resources?

## Instruction Quality

- Do rules change decisions rather than repeat generic agent behavior?
- Are requirements, defaults, options, and examples distinguishable?
- Is fixed order used only where correctness depends on it?
- Are safety and authorization boundaries explicit and fail-closed where needed?
- Are output requirements precise without forcing unnecessary ceremony?
- Is core content provider-neutral, with host-specific metadata isolated?

## Validation and Evaluation

- Does the package pass the target structural validator?
- Were YAML, JSON, schemas, links, scripts, and templates actually exercised?
- Do realistic direct, natural, boundary, non-trigger, and failure cases exist?
- For risky work, was approval, exact targeting, ordering, or stopping behavior
  tested independently?
- Do evaluations inspect observable outcomes instead of matching wording?

## Packaging and Maintenance

- Are author and version metadata present and consistent with repository policy?
- Are routers, catalogs, manifests, descriptions, and package versions updated?
- Are volatile versions verified from authoritative sources when used?
- Is there one authoritative copy of each rule or resource?
- Can future maintainers identify what to update when tools or formats change?

If the skill is intentionally simple and meets its contract, do not require
extra references, scripts, assets, or evaluations merely to make it appear more
advanced.
