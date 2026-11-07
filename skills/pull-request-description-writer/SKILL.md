---
name: pull-request-description-writer
description: Writes concise, reviewer-focused pull request titles and descriptions from local branch changes. Use when asked to summarize a branch for a PR, draft or improve a PR description, explain changes to reviewers, or identify testing, risks, breaking changes, migrations, and follow-up work for code review.
metadata:
  author: JSChronicles
  version: "0.1.0"
---

# Pull Request Description Writer

Write accurate, descriptive pull request content that helps reviewers understand
the change quickly. Focus on behavior, intent, risk, and verification rather than
enumerating files or retelling the diff.

## Gather Evidence

1. Read repository instructions and any pull request template or contribution
   guidance.
2. Identify the intended base branch from the user's request, branch tracking
   information, or repository defaults. State the assumed base when it is not
   explicit and the distinction matters.
3. Inspect the local branch commits and diff against the merge base. Use status,
   diff statistics, and targeted file inspection to understand the change; do
   not infer behavior from filenames alone.
4. Distinguish committed branch changes from uncommitted working-tree changes.
   Include uncommitted work only when the user asks for it or clearly intends
   the current working state to be summarized.
5. Review available test results, validation output, migration files, dependency
   changes, configuration, workflows, and documentation before making claims.

This skill authorizes read-only inspection for drafting. It does not authorize
committing, pushing, opening a pull request, or changing repository content.

## Write for Reviewers

Return a concise bulleted summary that highlights:

- major code or behavior changes;
- new features or capabilities;
- important configuration, workflow, dependency, or documentation updates;
- subtle implementation or operational details reviewers should know;
- breaking changes, migrations, rollout requirements, follow-up actions, or
  compatibility concerns;
- tests and validation actually performed, plus meaningful gaps.

Group related changes into outcomes. Explain why a change matters when the diff
does not make that obvious. Use plain language and introduce technical terms only
when reviewers need them to evaluate correctness or risk.

Do not explain every small file change, list mechanical formatting updates, or
repeat the same point under multiple headings. Do not claim a test passed, a bug
was fixed, or compatibility was preserved unless the available evidence supports
it.

## Default Output

Follow the repository's pull request template when one exists. Otherwise use
only the sections that add value:

```markdown
## Summary

- <major reviewer-relevant change>
- <new behavior or capability>
- <important configuration, workflow, or documentation change>

## Reviewer notes

- <subtle behavior, risk, migration, or focused review area>

## Testing

- <command or validation performed>
- Not run: <important gap and reason>
```

Omit empty sections. Keep ordinary pull requests short; add detail only for
complex behavior, operational risk, breaking changes, or migrations.

When asked for a title, provide a short imperative or outcome-focused title that
describes the primary change. Do not combine several unrelated details into the
title.

## Review Before Returning

- Every bullet is supported by the inspected branch.
- The summary describes outcomes rather than a file inventory.
- Breaking changes, migrations, deployment considerations, and follow-ups are
  prominent rather than buried.
- Testing distinguishes completed checks from recommendations or missing checks.
- The description is concise enough to scan and detailed enough to guide review.
