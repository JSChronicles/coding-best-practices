# Type System and API Design

Use TypeScript to make contracts and state transitions clearer, not to move
runtime uncertainty behind assertions.

## Strictness and Narrowing

Enable `strict` for new projects. Consider stronger checks such as
`noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, and
`useUnknownInCatchVariables` when their semantics fit the repository and its
dependencies. Introduce them as reviewed migrations rather than hiding errors
with casts.

Prefer control-flow narrowing, type predicates with real runtime checks, and
discriminated unions. Use assertions only when a nearby invariant proves the
claim and TypeScript cannot express it. Avoid double assertions such as
`value as unknown as Target`.

Use `unknown` at untrusted boundaries. Reserve `any` for narrow compatibility
edges where typing is impossible, document why it is needed, and prevent it
from spreading into the domain API.

## Data Modeling

Represent meaningful alternatives with literal unions or discriminated unions.
Use exhaustive checks for closed state machines when a missing case would be a
bug. Distinguish absence, `null`, empty values, and default values according to
the actual domain rather than treating them interchangeably.

Prefer readonly views for inputs the callee must not mutate. Remember that
TypeScript readonly types do not provide deep runtime immutability. Copy data at
ownership boundaries when mutation or aliasing would be unsafe.

Use `type` and `interface` according to the shape and repository convention.
Interfaces are useful for extendable object contracts; type aliases naturally
express unions, intersections, primitives, and mapped types. Do not create a
style-only migration between them.

## Functions and Generics

Let local implementation details infer naturally, but annotate exported
functions and important boundaries when doing so stabilizes the contract.
Prefer small parameter objects when several same-typed positional arguments are
easy to confuse or when options evolve independently.

Add a generic only when callers preserve or relate type information. Constrain
it to the operations the implementation actually uses. Avoid generic parameters
that occur only once, excessive conditional types, and public types that are
more difficult to understand than the values they describe.

Use overloads only when distinct call shapes provide a meaningfully better
public contract. Keep the implementation compatible with every overload and
test the runtime dispatch.

## Public APIs

Expose domain-focused inputs and outputs. Do not return internal ORM records,
framework request objects, or mutable caches unless they intentionally form the
public contract. Prefer named result types for complex outcomes.

Use `satisfies` when a value should be checked against a contract without losing
its useful inferred type. Use `as const` only when literal preservation and
readonly behavior are intended; do not scatter it as a substitute for modeling.

Treat exported types as compatibility surface. Removing union members,
narrowing accepted input, changing optionality, or altering generic defaults can
break consumers even when emitted JavaScript appears unchanged.

## Runtime Validation

Validate values from JSON, HTTP, environment variables, command-line input,
databases, queues, storage, and third-party libraries before treating them as
domain values. Use focused manual guards for small schemas or the repository's
existing schema library for complex data. Infer types from schemas when that is
the established single source of truth.

Validation errors should identify the boundary and useful field context without
exposing secrets or entire sensitive payloads. Convert validated transport data
into domain types once, then keep the interior strongly typed.
