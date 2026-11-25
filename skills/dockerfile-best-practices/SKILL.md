---
name: dockerfile-best-practices
description: Creates, reviews, and improves Dockerfiles, .dockerignore files, and OCI container-image builds. Use for image stage design, build context, layer caching, base-image integrity, non-root runtime behavior, secrets, metadata, multi-platform builds, image smoke tests, or container-focused CI commands. Do not use for Docker Compose or Kubernetes orchestration unless the request also changes how an image is built or validated.
metadata:
  author: JSChronicles
  version: "0.1.1"
---

# Dockerfile Best Practices

Build OCI images that are secure, reproducible, cache-efficient, minimal, and
testable. Preserve repository-local requirements and the application's real
runtime contract; a smaller image is not an improvement if it is harder to
operate, update, or debug safely.

## Start Here

1. Inspect the Dockerfile, `.dockerignore`, lockfiles, package manifests,
   runtime documentation, and existing build or release automation.
2. Read relevant history for non-obvious choices and past failures before
   removing pins, stages, cache boundaries, annotations, or smoke tests.
3. Identify the image's contract: command, arguments, ports, writable paths,
   user and group IDs, signals, configuration, credentials, supported
   platforms, and required metadata.
4. Separate build-only tools from the runtime filesystem with named stages.
5. Order copies and installs so dependency layers depend on manifests and
   lockfiles before frequently changing source.
6. Build the relevant target and exercise the resulting image as a user would.

## Core Rules

- Use a small, maintained base that still supplies the libc, certificates,
  timezone data, shells, or diagnostic support the application actually needs.
- Use meaningful tags for maintainability and an immutable digest when the
  build or deployment must be reproducible. Keep the tag beside the digest so
  humans and dependency tooling can identify and update the base.
- Verify current base-image tags and digests from the authoritative registry or
  publisher. Do not invent or preserve a stale digest from memory.
- Keep compilers, package managers, source trees, caches, and test tooling out
  of the runtime stage unless they are runtime dependencies.
- Copy dependency manifests and lockfiles before application source, install
  locked dependencies, then copy and install the application. Do not weaken
  lockfile enforcement merely to make a build pass.
- Use BuildKit cache mounts for regenerable package caches when they materially
  speed builds. Cache mounts improve performance; they must not be required for
  correctness or copied into the final image.
- Keep the build context intentionally narrow. Prefer a deny-by-default
  `.dockerignore` allowlist for focused application images when its maintenance
  cost is acceptable; otherwise exclude secrets, VCS data, local environments,
  build output, caches, and unrelated large files explicitly.
- Prefer `COPY` for ordinary build-context files. Use `ADD` only when its
  deliberate archive, remote-resource, or Git-source behavior is needed, and
  integrity-pin remote content.
- Make shell-form `RUN` commands fail when any required operation fails. Do not
  assume the default shell propagates failures from every pipeline component.
- Never put credentials or sensitive tokens in `ARG`, `ENV`, `COPY`, image
  labels, or command text. Use BuildKit secret or SSH mounts for build-time
  access and runtime secret injection for the running container.
- Run the final image as a dedicated non-root user. Give it ownership only of
  the paths it must write, and use stable numeric IDs when host-mounted volume
  permissions or platform policy depend on them.
- Use exec-form `ENTRYPOINT` and `CMD` when the application should receive
  signals directly. Choose their split from the intended override behavior,
  not from a blanket rule.
- Set `WORKDIR` explicitly and use absolute, intentional filesystem locations.
- Add standard OCI labels when publishing an image, including source, license,
  version, revision, and creation time when those values are available from the
  release process.
- Do not install unrelated operator tools into an application image for
  convenience. Create a separate tooling image when the use case is distinct.

## Package Installation

- Combine operating-system package index refresh, installation, and cleanup in
  one layer. Install only required packages and suppress recommended packages
  when the distribution and application permit it.
- Do not run a package index refresh or full distribution upgrade in an
  isolated layer. Refresh the pinned base regularly instead of hiding base
  maintenance inside an opaque upgrade step.
- Prefer verified package repositories and checksums or signatures for direct
  downloads. Avoid unverified `curl | sh` installation paths.
- Remove temporary archives, package lists, and installer output in the same
  layer that creates them when cache or mount semantics do not already exclude
  them.

## Decision References

Load only the detail needed for the task:

- Read [build-design-and-caching.md](references/build-design-and-caching.md) for
  stage boundaries, dependency layers, build context, cache mounts, and
  multi-platform concerns.
- Read [runtime-security-and-metadata.md](references/runtime-security-and-metadata.md)
  for users, permissions, secrets, signals, writable paths, labels, and runtime
  configuration.
- Read [validation-and-release.md](references/validation-and-release.md) for
  linting, smoke tests, architecture coverage, vulnerability checks, SBOMs,
  provenance, publication, or container CI.
- Read [review-checklist.md](references/review-checklist.md) for Dockerfile and
  image reviews.
- When editing GitHub Actions workflow mechanics, also apply
  `github-actions-best-practices`. This skill owns image-build and image-test
  semantics; the workflow skill owns triggers, permissions, action integrity,
  expressions, runners, caching, artifacts, and release orchestration.

## Validation

- Parse or lint the Dockerfile with the repository's configured tooling.
- Build the changed target from a clean-enough context using the same lockfiles
  and arguments expected in CI.
- Run focused smoke tests against the built image, including the default command
  or entrypoint, non-root identity, required imports or binaries, writable
  paths, read-only mounts, and signal or health behavior when relevant.
- Validate each supported platform natively or through the project's established
  cross-platform builder; do not infer multi-platform support from one build.
- Inspect the final image configuration, layers, size, labels, and accidental
  files. Run the repository's vulnerability, SBOM, or policy checks when they
  exist.
- Report the exact checks run, the image target or platform covered, and any
  registry, daemon, architecture, or credentials-dependent validation not run.

## Review Behavior

Lead with concrete security, correctness, reproducibility, runtime, and cache
risks. Distinguish defects in the final image from optional size or style
improvements. Explain the observable impact and the smallest practical fix.
If no issues are found, say so and identify any platforms or runtime behavior
that were not exercised.
