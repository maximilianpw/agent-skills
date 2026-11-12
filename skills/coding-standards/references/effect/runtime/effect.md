# Effect

## Source rule

These references target Effect v4. Concrete API spellings were checked against Effect 4.1.4 ([source baseline](https://github.com/Effect-TS/effect/tree/3fcc7fa7373a42e29786970a340a06cb587fd7c7)); this is not an instruction to upgrade a project.

Resolve the installed version first. Use that package's agent documentation (`AGENTS.md`, `ai-docs`, or equivalent when present), declarations, and tests for API signatures and examples. If unavailable locally, use official source at the matching release, not unrelated vendored copies or current `main`. The official [agent-documentation source](https://github.com/Effect-TS/effect/tree/3fcc7fa7373a42e29786970a340a06cb587fd7c7/ai-docs/src) and [migration guide](https://github.com/Effect-TS/effect/blob/3fcc7fa7373a42e29786970a340a06cb587fd7c7/MIGRATION.md) are starting points, not substitutes for version matching.

Our preferences for generators, service-module layout, `Option`, and test seams are local conventions, not universal Effect requirements. Apply the repository's explicit policy first; preserve compatible public APIs.

## Branch chooser

Load only branches matching the changed behavior:

- Models, codecs, brands, variants, or optional fields: [Schema](effect-schema-and-data.md).
- Services, Layers, dependency lifetimes, or `Effect.fn`: [Services](effect-services.md).
- Alchemy Workers, Durable Objects, Workflows, or two-phase composition: [Alchemy](effect-alchemy.md).
- Runtime configuration and providers: [Configuration](effect-configuration.md).
- Retries, polling, pacing, or timeouts: [Scheduling](effect-scheduling-and-retry.md).
- Memoization, TTLs, deduplication, or batching: [Caching](effect-caching.md).
- Streams, subscriptions, buffers, or long-lived consumers: [Streams](effect-streams.md).
- Outgoing HTTP and rate limits: [HTTP clients](effect-http-clients.md).
- Test clocks, concurrent tests, or test Layers: [Testing](effect-testing.md).

## Local workflow style

Keep dependency retrieval, sequential effects, branching, and loops in `Effect.gen` or a generator-based `Effect.fn`. Apply cross-cutting error translation, retry, timeout, tracing, and provision outside that control flow. A single pure result transform can stay in `Effect.map`; several dependent transforms belong in a generator where intermediate values and order are visible.

A local `.pipe(...)` around one yielded effect is useful for its own translation or result transform. Whole-operation policy belongs around the whole operation. In particular, wrapping an entire generator in retry repeats every preceding effect, not only the failing step; establish the [retry safety guarantee](../workflows-transactions-and-idempotency.md) first.
