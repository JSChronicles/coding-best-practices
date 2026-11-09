# Agent Instructions

This repository is the canonical source for the Coding Best Practices plugin.

## Skill Routing

Use
[skills/coding-best-practices-router/SKILL.md](skills/coding-best-practices-router/SKILL.md)
when:

- the applicable skill or technology is unclear;
- work spans multiple installed skills;
- performing a repository-wide review; or
- adding, removing, or changing catalog routing.

When one specialized skill clearly matches, use that skill directly instead of
loading the router.

## Skill Authoring

Use
[skills/agent-skill-authoring-best-practices/SKILL.md](skills/agent-skill-authoring-best-practices/SKILL.md)
when creating, substantially editing, reviewing, or validating a skill.

When changing a domain-specific skill, apply both:

- `agent-skill-authoring-best-practices` for activation, structure, references,
  assets, validation, versioning, and maintainability;
- the domain skill for technical correctness.

Read only the supporting references needed for the requested change.

## GitHub Actions

Use
[skills/github-actions-best-practices/SKILL.md](skills/github-actions-best-practices/SKILL.md)
when creating, editing, or reviewing:

- files under `.github/workflows/`;
- action versions or dependency lockfiles;
- Dependabot configuration;
- workflow permissions, OIDC, caching, concurrency, or artifacts.

Resolve current action releases before writing new references. Use the Actions
lockfile when supported and never edit it manually.

## Repository Rules

- Keep each canonical skill under `skills/<skill-name>/`.
- Do not duplicate skill content under product-specific plugin directories.
- Product manifests must expose the canonical `skills/` directory.
- Keep portable skill instructions provider-neutral.
- Preserve automatic skill discovery unless explicitly requested otherwise.
- Update the router when adding, removing, or renaming a skill.
- Increment a skill's version when its behavior or resources change.
- Keep root plugin, Claude plugin, and marketplace metadata synchronized when
  the package version or description changes.
- Do not add references, scripts, assets, or directories without a concrete use.

## Validation

After changing skills or plugin metadata, run:

```console
uv run scripts/validate_skills.py
git diff --check
```

After changing a workflow or action dependency, also run:

```console
gh actions-lock
gh actions-lock --verify-local
```

Review generated lockfile changes instead of editing the lockfile by hand.

Report any validation that could not be run.
