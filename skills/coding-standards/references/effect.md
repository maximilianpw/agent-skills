# Effect and Alchemy

Inspect the pinned package versions and local service, schema, error, and test conventions. The references below specialize the shared standards for Effect; they do not require a new framework or migration of unrelated code. Preserve precise success, expected-error, and dependency types.

## Load by concern

- [Effect APIs and workflow style](effect/runtime/effect.md): whenever Effect code changes; its branch pointers select services, Schema, resources, retries, caching, HTTP, streams, and tests. Verify API choices against pinned source.
- [Alchemy](effect/runtime/effect-alchemy.md): Workers, Durable Objects, Workflows, bindings, or two-phase composition.
- [Errors](effect/errors.md): expected failures, defects, absence, or public error translation.
- [Sensitive data and observability](effect/sensitive-data-and-observability.md): secrets, personal data, logs, traces, metrics, or rendered errors.
- [Parsing and schemas](effect/parsing-and-schemas.md): external/serialized data, parser changes, or new invariants.
- [Domain types and state](effect/domain-types-and-state.md): IDs, units, optionality, lifecycle state, or operation options.
- [Services and adapters](effect/modules-services-and-adapters.md): ownership, dependency interfaces, extraction, or effect ordering.
- [Persistence](effect/persistence.md): databases, caches, ORM records, or durable storage.
- [Workflow safety](effect/workflows-transactions-and-idempotency.md): transactions, retries, replay, compensation, and uncertain outcomes.
- [Configuration and resources](effect/configuration-and-resources.md): startup configuration, resource lifetimes, time, randomness, or global state.
- [Testing](effect/testing.md): changed behavior, parser contracts, public inference, or test implementations.
- [TypeScript additions](effect/typescript-safety.md): compiler settings, mutable state, public signatures, or type escapes.
- [Lint policy](effect/lint-and-policy.md): lint configuration, custom rules, or prevention tooling.
- [Imports and exports](effect/imports-exports-and-files.md): Effect imports or public entrypoints.

- [Comments and JSDoc](effect/comments-and-jsdoc.md): exported symbols, comments, and rendered errors.

## Effect-specific decisions

Expected failures are values; defects remain distinct. Parse external representations at their owner, preserve established evidence inward, and establish newly computed invariants through constructors or refinements. Keep meaningful service interfaces explicit, with Layers owning implementation and resources. Test through real services and faithful implementations, not module mocks.

For cleanup, distinguish runtime work removed from type-only changes. Compare public behavior, failure/recovery semantics, and inference; fewer parsers or branches do not prove a safer implementation.
