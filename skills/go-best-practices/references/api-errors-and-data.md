# API, Errors, and Data Design

## Exported APIs

Export only what callers need. Choose names that read clearly with the package
name and preserve compatibility once published. Document exported behavior,
including concurrency safety, ownership, mutation, blocking, and error
conditions when they are not obvious from the type.

Prefer concrete types for returned values. Define small interfaces where they
are consumed so callers depend only on required behavior. Do not create an
interface merely to mirror every method of one implementation or to enable
mocking without a real abstraction boundary.

Use generics when one type-safe algorithm or data structure genuinely applies
across types. Prefer ordinary functions or interfaces when they communicate the
domain more clearly. Keep constraints minimal and avoid exposing type machinery
callers do not need.

## Construction and Zero Values

Design useful zero values when practical. Use a constructor when it must:

- enforce invariants or validate input;
- initialize required maps, channels, or internal state;
- acquire or inject resources;
- select an implementation while hiding details.

Do not add `NewType` ceremony for a struct callers can safely initialize or use
at its zero value. If a constructor is required, make bypassing it difficult by
keeping invariant-bearing fields unexported.

## Errors

- Return errors to the caller that can decide policy. Do not both log and return
  the same error unless the log adds information unavailable at the boundary.
- Add concise operation and subject context when crossing a meaningful boundary.
- Wrap with `%w` when callers should retain the underlying identity.
- Use `errors.Is` and `errors.As` for decisions. Never depend on error text.
- Use sentinel errors sparingly for stable identity and custom error types when
  callers need structured details.
- Avoid exposing implementation-specific errors accidentally as a permanent API
  contract.
- Keep error messages lower-case and free of terminal punctuation when they are
  intended to compose inside larger errors.
- Reserve `panic` for impossible internal states or unrecoverable programmer
  errors. Do not panic for normal external failures.

Ensure cleanup errors are not silently discarded when they can affect data
integrity. Preserve the primary failure while making consequential close,
flush, commit, or rollback failures observable.

## Ownership and Mutation

Slices and maps are reference-like. State whether a function retains, mutates,
or returns storage shared with its caller. Copy at boundaries when retaining
caller-owned mutable data would create surprising coupling or races.

Use pointer receivers when methods mutate the receiver, the value is large, or
method-set consistency requires them. Use value receivers for small immutable
value-like types. Avoid mixing receiver styles without a reason.

Protect invariants rather than exporting fields for convenience. Prefer typed
structures over `map[string]any` when the schema is known.

## Logging

Applications own logging configuration. For a new standard-library-based
application, prefer structured `log/slog` records with stable keys and useful
context. Avoid logging secrets, credentials, tokens, or unnecessarily sensitive
payloads.

Libraries should normally return errors rather than log routine failures. If a
library must emit operational events, accept a narrow logging dependency or
logger supplied by the caller and document the behavior. Do not mutate the
process-wide default logger from a library.
