# Runtime Security and Metadata

Model the container as a constrained process with an explicit filesystem and
identity contract. Image construction should make the safe runtime path the
default.

## Identity and Filesystem

- Create a dedicated user and group in the runtime stage and switch with
  `USER` before the default command.
- Prefer stable non-system numeric IDs when bind mounts or policy engines need a
  predictable identity. Document the IDs for operators.
- Create writable directories deliberately and grant the narrowest ownership
  needed. Application code, interpreters, and configuration should not become
  writable merely to satisfy one output path.
- Set `HOME` to the runtime user's real home when libraries resolve caches or
  configuration from it.
- Test with a read-only root filesystem when the target platform expects one,
  supplying explicit temporary or persistent mounts for required writes.

## Secrets and Configuration

- Build arguments and environment variables persist in image metadata or build
  history and are not secret channels.
- Use `RUN --mount=type=secret` or `RUN --mount=type=ssh` for authenticated
  build access. Ensure the command does not copy the mounted material, echo it,
  or leave it in tool configuration or caches.
- Supply runtime credentials through the platform's secret mechanism,
  workload identity, environment injection when policy permits it, or read-only
  mounts. Never bake a local credential directory into an image.
- Keep environment-specific endpoints and behavior outside the image unless
  they are part of the immutable application release.

## Process Contract

- Use exec-form commands so the application is PID 1 and receives termination
  signals directly. If a wrapper is required, it must forward signals and
  preserve the child's exit status, normally by ending with `exec`.
- Put the stable executable in `ENTRYPOINT` and default overridable arguments in
  `CMD` when that matches the intended CLI. Use only `CMD` when operators should
  replace the entire command naturally.
- Add an init process only when the application cannot reap children or handle
  PID 1 behavior itself and the deployment platform does not already provide
  one.
- Treat `EXPOSE` as documentation, not firewall or publication configuration.
- Add `HEALTHCHECK` only when the image can perform a cheap, meaningful local
  check and the deployment environment will use it. Avoid checks that require
  shells or network clients added solely for health probing.

## OCI Metadata

For published images, prefer standard `org.opencontainers.image.*` labels:

- `title` and `description` for human identification;
- `source`, `url`, and `documentation` for provenance and support;
- `licenses` for the declared distribution license;
- `version`, `revision`, and `created` from the release build.

Pass release-specific values as non-secret build arguments and verify the final
config. For a multi-platform image, add required annotations to the image index
as well as child manifests when registry consumers inspect the index.

## Avoid Accidental Privilege

- Do not add `sudo`, a daemon, SSH server, or an interactive shell unless it is
  an explicit runtime requirement.
- Avoid Linux capabilities and privileged execution by default. If the program
  requires a capability, document and test the narrow runtime grant rather than
  embedding broad privilege assumptions.
- Do not make the container run as root merely to support arbitrary host volume
  ownership. Document the identity contract or provide a deliberate entrypoint
  strategy with clear tradeoffs.
