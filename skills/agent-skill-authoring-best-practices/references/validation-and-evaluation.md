# Validation and Evaluation

Structural validation proves the package can load. Behavioral evaluation tests
whether it activates appropriately and improves work.

## Structural Validation

Use the target repository's validator and verify:

- required frontmatter and supported metadata;
- directory and skill names;
- YAML, JSON, schemas, and local links;
- referenced files and resource routing;
- absence of unfinished scaffold placeholders;
- manifest, catalog, router, and package-version synchronization;
- executable permissions and dependencies for scripts where applicable.

Parse template formats and exercise deterministic scripts with representative
inputs. A valid Markdown file alone does not prove an asset or helper works.

## Behavioral Cases

Create a small evaluation set based on realistic requests:

1. **Direct use:** an explicit request that should activate the skill.
2. **Natural use:** a request phrased as a user normally asks it without naming
   the skill.
3. **Boundary:** a request that needs one conditional reference or mode.
4. **Non-trigger:** an adjacent request the skill should not capture.
5. **Failure or missing input:** a case where the agent must stop, report a gap,
   or request authority rather than inventing data.
6. **High-risk path:** when relevant, a case that tests approval, exact targeting,
   ordering, or fail-closed behavior.

Evaluate the resulting decisions and artifacts, not whether the agent repeated
preferred phrases. Inspect whether it loaded the right resources, preserved
scope, used repository evidence, respected authority, validated meaningful
outcomes, and reported limitations.

## Forward Testing

For a complex or risky skill, test it through a fresh context or independent
reviewer using only the skill, a realistic request, and necessary raw artifacts.
Do not tell the evaluator the expected conclusion or suspected bug. Keep the
test isolated from production systems and uncommitted repository work.

Review the produced files, commands, and decisions. Improve the skill only from
observed gaps or strong domain evidence; do not accumulate universal rules for
every stylistic variation.

## Regression and Maintenance

Retain compact evaluation cases for failures likely to recur: misrouting,
incorrect ordering, missing validation, unsafe permission inference, broken
templates, or stale tool assumptions. Re-run them when the skill or host format
changes.

Version the skill when instructions or resources change behavior. Update plugin
or catalog versions according to repository policy when the distributed package
changes. Record source authority and review dates for volatile facts; prefer
instructions to verify current versions rather than freezing rapidly changing
values in prose.

Remove obsolete examples, duplicate rules, unused resources, and compatibility
paths that are no longer supported. A skill is maintained software, not an
append-only prompt.

## Completion Evidence

Report:

- validators and behavioral cases run;
- scripts, templates, and links exercised;
- target agents or formats checked;
- anything not run and why;
- remaining assumptions, permissions, or environment dependencies.
