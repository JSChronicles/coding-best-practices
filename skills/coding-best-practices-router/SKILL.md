---
name: coding-best-practices-router
description: Routes ambiguous, repository-wide, or mixed-technology coding requests to the smallest useful set of installed coding best-practices skills. Use when the target technology is unclear, work spans multiple supported technologies, or the user asks which catalog skill applies. Do not use when one specialized skill already clearly matches.
metadata:
  author: JSChronicles
  version: "0.3.0"
---

# Coding Best Practices Router

Dispatch coding work to the smallest useful set of specialized skills in this
plugin. Do not repeat their technical guidance in the router.

## Routing Workflow

1. Honor the user's explicit technology, files, and requested scope.
2. Read [technology-detection.md](references/technology-detection.md) only when
   the target is ambiguous, repository-wide, or potentially mixed.
3. Read [routing-table.md](references/routing-table.md) and select only skills
   that exist in the installed catalog.
4. For more than one selected skill, read
   [skill-composition.md](references/skill-composition.md) to assign ownership
   and avoid duplicated or conflicting guidance.
5. Read every selected skill's `SKILL.md` before acting. Load its references
   only when that skill says they are relevant.
6. Announce the selected skill or skill set and the evidence for the route.

When one specialized skill clearly matches, use it directly on later turns.
Re-route only when the task pivots, expands to another technology, or changes
to a different subproject.

## Boundaries

- Do not infer technologies from vendored dependencies, generated output,
  virtual environments, build artifacts, or fixtures unless the request
  specifically targets them.
- In a monorepo, route by the requested file or subproject instead of the
  repository's dominant language.
- Do not load multiple skills merely because their files coexist. The requested
  work must cross their ownership boundaries.
- Do not fabricate a route for an unsupported technology. Follow applicable
  project instructions and general engineering practices, and state the catalog
  gap only when useful.
- Ask one focused question only when competing routes would materially change
  the work and project evidence cannot resolve them.

## Maintaining the Router

When a specialized skill is added or removed, update the routing table in the
same change. Update detection or composition guidance only when the catalog
change creates a real new signal or ownership overlap. Never publish routes to
skills that are not included in the plugin.
