# Workflow Security

## Establish the Trust Boundary

For every privileged job, identify:

- which event starts it and who can influence the event payload;
- which commit or ref is checked out and executed;
- whether code comes from a fork or untrusted contributor;
- token permissions, secrets, environments, and cloud identities available;
- the runner type and what persistent resources it can reach.

Privilege the smallest job possible, and keep untrusted build or test work in a
separate job or workflow without secrets and with read-only permissions.

## Token Permissions

Declare `permissions` explicitly. Start from `contents: read` or `{}` and add
only required scopes. Put elevated permissions at job level when only one job
needs them. Remember that setting any explicit permission makes unspecified
permissions `none`.

Do not grant broad write access merely because a later command might need it.
Separate read-only validation from publishing, commenting, release, or deploy
jobs and protect privileged jobs with environments or other approvals.

## Pull Request Events

Use `pull_request` for building and testing untrusted contributions. It is
designed for reduced privileges and does not expose normal repository secrets
to forked pull requests.

`pull_request_target` runs in the base repository's privileged context. Use it
only for isolated tasks such as trusted labeling or triage. Never combine it
with checking out, building, or executing untrusted pull request code while a
write-capable token or secrets are available.

## Script Injection

Treat user-controlled contexts as data, including titles, bodies, branch names,
commit messages, issue text, and many event fields. Do not splice expressions
directly into an inline script:

```yaml
- env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: printf '%s\n' "$PR_TITLE"
```

Quote variables according to the target shell. Prefer a maintained action with
a narrow interface when it avoids handling untrusted text in a shell.

## Secrets and OIDC

- Prefer OIDC federation and short-lived credentials over stored cloud keys.
- Grant `id-token: write` only to the job that authenticates.
- Restrict the provider trust policy using claims for the intended repository,
  owner, ref, environment, or reusable workflow.
- Keep secrets out of command lines, logs, artifacts, caches, job outputs, and
  pull request workflows.
- Use protected environments for sensitive deployments and scope environment
  secrets to those jobs.
- Do not pass all inherited secrets to reusable workflows when explicit named
  secrets will do.

## Third-Party Actions and Runners

Review the action source, owner, release history, requested permissions, and
dependency chain. Prefer first-party or well-maintained actions and restrict
which actions may run through repository or organization policy where useful.

Treat self-hosted runners as sensitive infrastructure. Avoid running untrusted
fork code on persistent self-hosted runners. Use ephemeral, isolated runners
when possible, minimize reachable credentials and networks, and assume a job can
inspect anything left on the runner.

## Deployments

Use environments, approvals, branch or tag restrictions, and concurrency groups
for deployments. Separate build artifacts from deployment credentials so the
deploy job consumes a reviewed artifact instead of rebuilding mutable source in
a privileged context.
