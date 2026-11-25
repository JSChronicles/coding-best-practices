# Validation and Release

Validate the artifact that will run, not only the Dockerfile text. Publication
should promote an already tested image by immutable digest whenever the build
system permits it.

## Local and CI Validation

Use the project's tools and risk profile to select checks:

1. Parse and lint the Dockerfile and `.dockerignore` policy.
2. Build the intended target with lockfile enforcement and expected build
   arguments.
3. Run the default entrypoint or command and one meaningful application
   operation such as `--version`, a validation command, or a local request.
4. Confirm the effective user is non-root and required writable paths work.
5. Confirm expected binaries, modules, certificates, and package data exist;
   also inspect for build tools, credentials, source, or caches that should not.
6. Exercise bind mounts and read-only inputs that appear in documented usage.
7. Stop a running container and verify timely signal handling when graceful
   shutdown matters.
8. Inspect image config, history, labels, architectures, and size.

Do not make linting a substitute for a build or make a successful build a
substitute for starting the image.

## Security Evidence

- Scan the final runtime image, not only the builder. Apply repository policy to
  severity, fix availability, allowlists, and expiration of exceptions.
- Generate an SBOM for distributed images when the publishing system supports
  it. Ensure attestations are associated with the immutable digest.
- Emit build provenance for released images when supported, without exposing
  secrets or private build arguments.
- Review base-image and tool-image updates continuously with dependency tooling.
  A digest pin provides immutability, not automatic freshness.
- Treat vulnerability results as triage input. Confirm whether a vulnerable
  component is present and reachable, and update the base or dependency rather
  than hiding findings without a recorded rationale.

## Multi-Platform Publication

- Build each platform image and smoke-test that exact image before assembling
  the multi-platform index.
- Prefer digest-based handoff between build, test, and publication jobs. Do not
  rebuild separately for release after testing a different artifact.
- Attach semantic tags only after all required platform builds pass.
- Verify the published index contains every advertised platform and the
  expected OCI annotations.
- When public access is part of the product contract, log out and verify the
  digest can be inspected or pulled anonymously.
- Report the published digest in release output so downstream deployments can
  pin it.

## GitHub Actions Boundary

When the implementation uses GitHub Actions, apply
`github-actions-best-practices` for workflow triggers, minimal permissions,
external action versions and locking, untrusted input, artifacts, concurrency,
and timeouts. Container-specific expectations remain:

- isolate per-platform cache scopes when outputs differ;
- avoid publishing on untrusted pull-request events;
- grant registry write permission only to the publishing job;
- smoke-test before manifest creation or tag promotion;
- publish SBOM and provenance according to release policy; and
- pass digests, not mutable tags, between jobs and downstream consumers.

## Validation Gaps to Report

State when checks could not cover a required CPU architecture, need a registry
login, depend on unavailable secrets or hardware, require a running daemon, or
can only be confirmed after publication. Do not describe an unbuilt or unrun
image as validated.
