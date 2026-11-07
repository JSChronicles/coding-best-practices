# Concurrency and Context

Use concurrency only when independent work, latency hiding, streaming, or
throughput justifies the additional lifecycle and synchronization complexity.

## Goroutine Ownership

Before starting a goroutine, identify:

- who starts it and who waits for it;
- how it terminates on success, error, cancellation, and shutdown;
- where its error or result goes;
- which resources it owns and releases;
- whether the number of goroutines is bounded.

Do not launch fire-and-forget goroutines inside request paths unless their
lifecycle is explicitly transferred to a longer-lived owner. Avoid goroutine
leaks caused by blocked sends, receives, I/O, timers, or missing cancellation.

## Context

- Pass `context.Context` as the first parameter, conventionally named `ctx`.
- Do not store context in a struct or pass `nil`; use `context.Background()` or
  `context.TODO()` only at appropriate roots or temporary integration points.
- Propagate caller cancellation and deadlines through blocking dependencies.
- Call the cancellation function returned by `WithCancel`, `WithTimeout`, or
  `WithDeadline`, normally with `defer` immediately after creation.
- Use context values only for request-scoped data that crosses API boundaries,
  not optional function parameters or mutable configuration.
- Check `ctx.Err()` or select on `ctx.Done()` in long-running loops when the
  blocking operation does not already honor context.

## Channels and Synchronization

Use channels to coordinate ownership or communicate values; use mutexes to
protect shared state. Choose the simpler model for the actual invariant.

- The sender owns closing a channel. Receivers should not close a channel they
  do not own.
- Closing is a broadcast that no more values will arrive, not a universal
  cleanup mechanism.
- Use buffered channels only with a reasoned capacity and backpressure model.
- Avoid using `time.Sleep` for synchronization in production code or tests.
- Keep critical sections small, but do not split an invariant across multiple
  lock operations.
- Do not copy values containing mutexes after first use.
- Use atomics only for simple well-documented state where their memory semantics
  are understood; otherwise prefer a mutex.

For groups of tasks that return errors, use a bounded worker pattern and shared
cancellation. A dependency such as `errgroup` is reasonable when its lifecycle
semantics fit and the external module is acceptable.

## Shutdown and Resources

Give servers and background workers a bounded graceful-shutdown path. Stop
accepting new work, cancel or signal workers, wait for owned goroutines, flush
buffers, and close resources in a deliberate order. Do not let shutdown wait
forever on an uncooperative dependency.

Reuse timers and tickers appropriately in loops and always stop tickers that are
no longer needed. Prefer APIs that accept context for network and subprocess
operations.

## Race Validation

Run `go test -race ./...` for changes involving goroutines, caches, maps,
callbacks, shared clients, or mutable global state when the platform supports
the race detector. A clean race run does not prove correctness; still review
ownership, ordering, cancellation, and leak paths.
