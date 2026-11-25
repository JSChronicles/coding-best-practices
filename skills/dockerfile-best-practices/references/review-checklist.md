# Dockerfile Review Checklist

Prioritize issues that change the built artifact or its operational safety.

## Build Inputs and Reproducibility

- Are base and tool images maintained, identifiable by tag, and pinned by
  digest where reproducibility is required?
- Are dependency versions locked and enforced during the build?
- Does `.dockerignore` exclude secrets, local environments, VCS data, caches,
  generated output, and unrelated context?
- Do `COPY` instructions include every required input without invalidating
  expensive layers unnecessarily?
- Is `ADD` reserved for intentional archive or remote-source behavior, with
  immutable checksums or commits for remote content?
- Can dependency updates still be discovered and reviewed after digest pinning?

## Stages and Layers

- Are build-only tools and caches absent from the runtime stage?
- Do dependency layers precede frequently changing source where the ecosystem
  supports a correct split install?
- Are package installation, index refresh, and cleanup performed safely?
- Are cache and secret mounts used only as ephemeral build inputs?
- Do cache mounts use `shared`, `locked`, or `private` according to the tool's
  real concurrent-write behavior and platform boundaries?
- Can every required shell-form `RUN` operation and pipeline surface an earlier
  command failure without leaking secrets through tracing?
- Are multi-platform downloads, builds, and caches architecture-correct?

## Runtime Contract

- Does the final image run as a dedicated non-root user?
- Are writable directories explicit, narrowly owned, and documented for volume
  users?
- Do `ENTRYPOINT` and `CMD` provide the intended override and signal behavior?
- Are credentials injected at runtime instead of stored in layers, metadata,
  history, or labels?
- Are required certificates, shared libraries, package data, and configuration
  defaults present?
- Are ports, health checks, and filesystem expectations meaningful rather than
  decorative?

## Distribution and Evidence

- Are source, license, version, revision, and creation metadata correct where
  the image is published?
- Is the exact built image smoke-tested on every supported platform?
- Are final-image vulnerability, SBOM, and provenance requirements satisfied?
- Is a multi-platform index created only from tested child digests and then
  inspected after publication?
- Can users obtain and pin the published digest?

## Review Output

For each finding, identify the affected stage or instruction, the resulting
image or runtime impact, and the smallest correction. Separate required fixes
from optional size, speed, or readability improvements. Mention daemon,
registry, platform, and runtime tests that were not available.
