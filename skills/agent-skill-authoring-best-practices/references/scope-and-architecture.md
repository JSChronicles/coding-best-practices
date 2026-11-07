# Scope and Architecture

Design the skill around repeatable work and decisions, not around a desired file
count. Depth should reduce ambiguity, risk, or repeated rediscovery.

## Define the Contract

Before writing instructions, identify:

- representative user requests that should activate the skill;
- adjacent requests that should use another skill or ordinary reasoning;
- inputs and repository evidence the agent needs;
- outputs and observable acceptance criteria;
- decisions that require domain guidance;
- irreversible, privileged, external, or production effects;
- failure modes demonstrated by prior use or inherent in the workflow;
- target agents and the portable subset of their skill formats.

Do not define scope only from a topic label such as "security" or "cloud." Tie
it to concrete artifacts, procedures, decisions, and deliverables.

## Complexity Levels

### Focused Skill

Use one `SKILL.md` when the task has one clear mode, a short workflow, few
conditional rules, and no reusable assets or deterministic mechanics. Examples
include a focused review method or a small writing standard.

### Structured Skill

Add references or assets when the skill has multiple substantial modes,
technology-specific decisions, long policies, schemas, templates, or distinct
review and creation workflows. Keep shared invariants in the entrypoint and load
only the relevant depth.

### Operational Skill

Add scripts, detailed validation, permission boundaries, state transitions, or
evaluation fixtures when the workflow is fragile, repeated, high-risk, or
mechanically complex. Examples include deployment, migrations, generated
artifacts, external systems, or procedures where ordering is a correctness
requirement.

An advanced skill may use any of these levels. "Advanced" means the skill
captures meaningful expertise and validates outcomes, not that it has many
files.

## Resource Decisions

Use `references/` for material the agent reads conditionally: modes, schemas,
policies, detailed review criteria, troubleshooting, or substantial examples.
Split by decision area, not arbitrary length.

Use `scripts/` when deterministic behavior materially improves reliability,
especially for repeated transformations, validators, parsing, or API mechanics.
Scripts need documented inputs, outputs, failure behavior, dependencies, and
tests or representative execution.

Use `assets/` for templates and files copied or adapted into deliverables. An
asset must be usable, internally consistent, and clearly routed from the skill.

Use agent-specific metadata directories only for UI, discovery, dependency, or
invocation configuration required by that host. Do not duplicate the portable
skill body there.

## Progressive Disclosure

The entrypoint should be sufficient to choose a correct path. It must contain:

- purpose and scope;
- essential invariants and safety boundaries;
- the main workflow or mode-selection logic;
- explicit routing to supporting resources;
- validation and result-reporting expectations.

References contain depth needed only after a mode or artifact is selected. Do
not require the agent to read every reference for every request, and do not
create a separate router when the entrypoint has only one meaningful path.

## Portability

Prefer portable terms such as agent, model, tool, repository instructions, and
skill. Isolate host-specific invocation syntax, metadata, permissions, and
packaging. When formats disagree, document adapters rather than claiming one
layout works unchanged everywhere.

Portable content does not mean lowest-common-denominator content. Keep strong
domain guidance in the shared skill while placing product capabilities in
clearly scoped integration metadata or references.
