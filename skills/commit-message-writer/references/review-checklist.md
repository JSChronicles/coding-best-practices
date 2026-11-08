# Commit Message Review Checklist

## Evidence

- Does the message describe only the staged or explicitly requested boundary?
- Was the staged diff inspected beyond filenames and statistics?
- Are behavior, motivation, testing, migrations, and issue references supported
  by evidence?
- Are unstaged and untracked changes excluded unless explicitly requested?

## Convention and Labels

- Does explicit user or repository policy take precedence over fallbacks?
- Was Commitlint, release tooling, contribution guidance, and labeler behavior
  inspected when present?
- Is the type truthful to the primary intent rather than selected only to obtain
  a label?
- Is the scope repository-defined or a useful stable domain?
- Are label descriptions and mappings stated as confirmed only when evidence
  supports them?

## Message Quality

- Is the title concise, imperative, specific, lowercase after the prefix, and
  free of a trailing period?
- Does the body explain why and meaningful behavior without repeating the title
  or listing files?
- Are breaking changes marked with `!` and a useful `BREAKING CHANGE:` footer?
- Are dependency changes classified as `build`, `chore`, `fix`, or `ci` from
  their actual role?
- Is a small change allowed to remain title-only?

## Atomicity and Authority

- Does the commit represent one coherent intent and Conventional Commit type?
- Should unrelated changes be proposed as separate commits?
- Does the grouping preserve buildability, tests, and dependency order?
- Were staging, committing, amending, rebasing, resetting, and pushing avoided
  unless explicitly authorized?
