---
name: commit-message-writer
description: Drafts, reviews, and plans clear Conventional Commit titles and descriptions from repository evidence. Use when asked to write or improve a commit message, choose feat/fix/chore or another type, map commit prefixes to repository labels, summarize staged changes, or split mixed changes into logical commits.
metadata:
  author: JSChronicles
  version: "0.1.0"
---

# Commit Message Writer

Write accurate commit titles and bodies that explain one coherent change and
work with the repository's release, changelog, and labeling automation.

Use Conventional Commit types by default. Repository-enforced conventions and
documented label semantics take precedence over the fallback rules in this
skill.

## Modes

Choose the mode from the request:

- **Draft one commit:** describe the staged diff as one commit.
- **Plan commits:** divide explicitly requested working-tree changes into
  coherent commit groups and draft a message for each group.
- **Review a message:** compare an existing title and body with the actual
  change and repository convention, then propose a corrected version.

Do not treat a pull request description as a commit message. A commit describes
one atomic historical change; a pull request may summarize many commits and
their combined review context.

## Evidence and Boundaries

1. Read repository instructions and contribution guidance.
2. Inspect commit-message, release, changelog, and labeler configuration using
   [conventions-and-labels.md](references/conventions-and-labels.md).
3. For a single message, treat `git diff --cached` as the default boundary.
   Inspect the staged name/status and statistics, then read enough of the staged
   diff and surrounding code to understand intent.
4. Do not include unstaged or untracked changes unless the user explicitly asks
   for working-tree or commit-planning mode.
5. Inspect recent commit subjects only to learn repository convention; do not
   copy vague or inconsistent historical messages.
6. Use test output and validation evidence only when available. Never claim a
   check passed merely because a related file or script exists.

If nothing is staged in single-commit mode, say so rather than silently
summarizing the entire working tree. The user may then request working-tree mode
or stage the intended boundary.

This skill authorizes read-only inspection and message drafting. It does not
authorize staging, committing, amending, rebasing, resetting, or pushing. Perform
those actions only when the user explicitly requests them.

## Convention Selection

Use this precedence:

1. An explicit type, scope, or format requested by the user.
2. Enforced repository configuration such as Commitlint or release tooling.
3. Documented labeler rules and repository label descriptions.
4. Contribution guidance and consistent recent commit history.
5. The fallback Conventional Commit mapping in
   [conventions-and-labels.md](references/conventions-and-labels.md).

Inspect how a labeler actually works. Some labelers parse commit or pull request
titles, while others use changed paths, branches, or manually applied labels.
Do not claim a prefix controls labeling unless the configuration demonstrates
that relationship.

When local configuration does not explain repository labels and authenticated
GitHub CLI access is already available, a read-only `gh label list` query may be
used to inspect label names and descriptions. If remote label information is not
available, fall back to the documented mapping and state material uncertainty.

## Message Rules

- Use `type(scope): imperative summary`; omit the scope when it adds no useful
  ownership or domain context.
- Keep the title concise, specific, lowercase after the prefix, and free of a
  trailing period. Follow a repository title-length rule when one exists;
  otherwise aim for no more than 72 characters.
- Select the type from the primary intent and observable behavior, not merely
  the files changed or the label someone hopes to obtain.
- Use the body for why the change was needed, important behavioral effects,
  design decisions, migrations, compatibility, or follow-up requirements.
- Do not repeat the title, narrate every file, or include mechanical details
  that do not help future maintainers.
- Use `!` and a `BREAKING CHANGE:` footer when the change breaks a supported
  contract. Do not hide a breaking change behind `refactor` or `chore`.
- Add issue, ticket, co-author, or release footers only when supported by
  evidence or explicitly provided by the user.
- If staged changes contain multiple independent intents or Conventional Commit
  types, recommend a split instead of producing a vague combined message.

Read [message-design-and-grouping.md](references/message-design-and-grouping.md)
for type selection, dependency changes, scopes, bodies, footers, examples, and
commit planning.

## Default Output

Return the message in a copyable block:

```text
type(scope): concise imperative summary

Explain why the change is needed and any important behavioral effect.

BREAKING CHANGE: describe required migration when applicable.
```

Omit the body and footers when the title fully explains a small change. When
planning multiple commits, return ordered groups with their included files or
hunks, dependency order, and proposed message. Do not stage the groups.

Mention the detected convention or label mapping only when it influenced a
non-obvious choice. Use [review-checklist.md](references/review-checklist.md)
before returning a complex message or commit plan.
