# Build Design and Caching

Design stages and layers around invalidation boundaries and artifact ownership.
The final stage should contain the runnable application, not the history of how
it was compiled.

## Stage Boundaries

- When BuildKit-only features depend on a Dockerfile frontend version, declare
  a supported syntax directive deliberately and keep it updateable. Do not copy
  a parser version from an unrelated example without checking the project's
  builder compatibility.
- Give stages descriptive names such as `builder`, `test`, and `runtime`; copy
  from names rather than numeric stage positions.
- Centralize a shared pinned base only when stages truly need the same operating
  system and runtime. Independent tools can come from their own pinned stage and
  be copied as individual binaries or artifacts.
- Build and test in an earlier stage, then copy the smallest complete runtime
  artifact set. Verify shared libraries and data files rather than assuming one
  executable is self-contained.
- Use `--target` for development or test images when useful, but keep the
  default final stage suitable for the primary production artifact.

## Cache-Friendly Ordering

Use change frequency to order layers without breaking correctness:

1. Select and pin base and tool images.
2. Install rarely changing operating-system build dependencies.
3. Copy package manifests and lockfiles.
4. Restore locked third-party dependencies without installing the project when
   the ecosystem supports that split.
5. Copy the minimum project metadata and source required for installation.
6. Build or install the project.
7. Copy only runtime artifacts into the final stage.

This pattern prevents an ordinary source edit from invalidating dependency
resolution. Do not split dependency and project installation when the package
manager cannot preserve an equivalent locked result.

Use BuildKit cache mounts for package-manager download and compilation caches.
Choose cache IDs or scopes that avoid unsafe sharing across incompatible
platforms, toolchain versions, or mutually untrusted builds. Set cache mount
ownership and modes for the user that writes them. A build must still succeed
with an empty cache.

Choose cache sharing from the tool's concurrency behavior:

- Use the default `sharing=shared` for caches that safely support concurrent
  readers and writers, such as content-addressed download caches.
- Use `sharing=locked` when the tool requires exclusive access to a mutable
  database or cache directory. This prevents concurrent corruption but
  serializes access, so do not apply it indiscriminately.
- Use `sharing=private` when each concurrent build needs an isolated cache and
  reuse between those builds is less important than separation.

When one package operation spans multiple state directories, apply compatible
sharing rules to every directory involved. Scope architecture-dependent caches
by target platform, and do not share writable caches across mutually untrusted
builds merely for speed.

## Build Context and Copy Semantics

- Treat the context as input to the build and as a possible disclosure
  boundary. Inspect it before adding a broad `COPY . .`.
- A deny-by-default `.dockerignore` can make a narrow context explicit:
  ignore everything, then allow the Dockerfile, lockfiles, manifests, licenses,
  documentation required by packaging, and selected source directories.
- Keep allowlists synchronized with real build inputs. Missing migrations,
  generated schemas, package data, or nested ignore exceptions can produce an
  image that builds but fails at runtime.
- Prefer specific `COPY` instructions so each layer expresses its inputs.
- Use `COPY --chown` when it avoids a separate ownership layer and matches the
  target stage's available user and group.
- Never assume `.gitignore` protects the Docker build context; `.dockerignore`
  is separate.

## `COPY` and `ADD`

- Use `COPY` for normal files and directories from the build context or another
  stage. Its narrower behavior makes the inputs easier to review.
- Use `ADD` when automatic extraction of a trusted local archive is intentional,
  or when Docker's remote URL or Git-source handling provides a concrete
  benefit. Do not use it as a shorter spelling of `COPY`.
- Local tar archives supplied to `ADD` may be extracted automatically; remote
  archives fetched by URL are not automatically unpacked. Make that difference
  explicit rather than relying on a filename extension.
- For a public HTTP or HTTPS source, require immutable content and use
  `ADD --checksum=sha256:<digest>` when the supported Dockerfile frontend
  provides it. A checksum proves content identity; it does not establish that
  the publisher is trustworthy.
- Pin remote Git sources to an immutable commit. Retain `.git` data only when
  the build genuinely consumes it, and never pass repository credentials in
  the source URL.
- Prefer a `RUN` download with signature or checksum verification when access
  requires a secret mount, redirects or headers need control, or the artifact
  must be transformed explicitly. Remove the download in the same layer after
  producing the required artifact.

## Shell-Form `RUN`

- The shell form normally runs through the base image's default shell. A
  pipeline can report only its last command's status, hiding an earlier
  download, verification, or transformation failure.
- Avoid a pipeline when separate commands or a temporary file make error
  handling clearer. Otherwise select a shell that supports `pipefail` and
  enable it for that command. Do not assume `/bin/sh` implements
  `set -o pipefail`.
- Chain operations that must all succeed with `&&`, while recognizing that
  `set -e` and `&&` do not replace deliberate handling of pipelines,
  conditionals, subshells, or expected nonzero statuses.
- Use exec-form `RUN` when direct process execution is useful, but remember it
  does not provide shell expansion, pipes, redirection, or command chaining.
- Use a `SHELL` instruction only when subsequent shell-form instructions share
  a real shell requirement. Confirm that shell exists in the stage and avoid
  adding it to a minimal runtime image solely for build convenience.
- Avoid tracing commands that may expose tokens or sensitive URLs in build
  logs. Secret mounts protect the mounted file, not commands that print its
  contents.

## Multi-Platform Builds

- Distinguish build-platform tools from target-platform artifacts. Use
  BuildKit's platform arguments when compiling or downloading architecture-
  specific content.
- Do not run a target binary during a cross-build unless emulation is explicitly
  configured and tested.
- Scope caches by platform where outputs are architecture-dependent.
- Build and smoke-test every advertised platform. Publishing a manifest list is
  not evidence that every child image starts successfully.

## Patterns to Avoid

- Copying the entire repository before dependency installation.
- Keeping compilers and headers in the runtime image because cleanup appears
  inconvenient.
- Using mutable convenience tags where an immutable input is required.
- Forcing cache hits with stale or incomplete copied inputs.
- Copying package-manager caches or BuildKit secret mounts into the image.
- Using `ADD` for ordinary local files or fetching mutable remote content
  without an integrity check.
- Assuming a multi-command pipeline fails when any component fails.
- Optimizing layer count at the cost of reviewability; layer semantics and final
  contents matter more than minimizing the instruction count.
