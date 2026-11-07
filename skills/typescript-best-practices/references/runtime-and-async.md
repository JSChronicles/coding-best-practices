# Runtime and Async Behavior

TypeScript erases at runtime. Design errors, resources, cancellation, logging,
and concurrency as JavaScript behavior first, then describe them accurately in
types.

## Errors

Throw `Error` instances or deliberate subclasses, not strings or arbitrary
objects. Add context at the layer that understands the failed operation. Use an
error cause when supported and useful, while preserving stable public error
classification separately from incidental message text.

Caught values may not be errors. Narrow with `instanceof Error` or a focused
guard before reading properties. Do not use message substring matching when a
stable code, class, or discriminated result is available.

Use result-style return values for expected alternatives when callers routinely
branch on the outcome. Use exceptions for failures that interrupt the normal
operation. Apply one coherent contract at each boundary rather than mixing
`undefined`, rejected promises, and thrown errors for the same failure.

## Promises and Cancellation

Every promise must be awaited, returned, aggregated, or deliberately detached.
A detached operation needs an owner and an error path. Avoid async promise
constructors and unnecessary `async` wrappers.

Use `Promise.all` when all operations must succeed and concurrency is bounded.
Use `Promise.allSettled` only when partial outcomes are meaningful and every
rejection is inspected. Do not launch unbounded work by mapping a large input
directly into `Promise.all`; use batching, a queue, or a concurrency limiter.

Accept and propagate `AbortSignal` through supported I/O APIs for request-scoped
work. Check cancellation around expensive work that does not natively observe
the signal. Cancellation is not automatically a failure worth retrying or
logging as an error.

## Resources and Lifecycle

Make ownership of servers, streams, timers, subscriptions, database clients,
workers, and temporary files explicit. Pair acquisition with cleanup in a
`finally` block or a lifecycle abstraction the project already uses. Tests must
not pass while open handles keep the process alive.

Avoid module-import side effects that start work, read mutable environment, or
connect to services. Keep initialization in an application entrypoint so tests
and consumers control lifecycle.

## State and Concurrency

JavaScript's event loop does not prevent logical races. Protect read-modify-write
sequences that cross awaits, make idempotency explicit for retried operations,
and avoid shared mutable module state when requests or tests can overlap.

Use workers only for appropriate CPU-bound or isolated work. Define message
schemas, error propagation, termination, and resource limits rather than hiding
worker behavior behind an untyped channel.

## Logging and Configuration

Use the repository's structured logger and stable event fields. Libraries
should normally return errors or accept an injected logger instead of
configuring global logging. Never log secrets, authorization material, or full
untrusted payloads by default.

Read configuration at the application boundary, validate it once, and pass a
typed configuration object inward. Do not scatter direct `process.env` access
through domain modules or rely on truthiness for booleans and numbers.
