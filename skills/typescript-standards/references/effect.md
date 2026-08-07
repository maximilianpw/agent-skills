# Effect branch

Apply this reference only after the gate in `../SKILL.md` passes. First inspect the installed Effect version, package imports, and nearby code: APIs and conventions differ across Effect versions, and established project patterns beat generic examples.

The framework-neutral references still govern domain meaning and technology ownership. This file changes how effects, failure, resources, and dependencies are represented.

## Effects and failures

- Keep expected failures in the Effect error channel with specific tagged error types.
- Keep defects out of the expected error channel. Convert a defect into a typed failure only at a boundary that can meaningfully recover or translate it.
- Preserve causes when translating low-level failures.
- Use `Option` for ordinary absence when the local Effect code does so; use a typed error when absence violates the operation's promise.
- Avoid executing effects with `runPromise`, `runSync`, or a custom runtime inside application modules. Run the graph at a runtime boundary.

## Schema and data

- Use the repository's Effect Schema conventions for untrusted input and serialized output.
- Keep wire and persistence schemas at their owning boundary; expose domain values inward.
- Use branded schemas when same-shaped values can realistically be confused.
- Model state variants with tagged unions or the project's established Effect data types.
- Distinguish an optional key from a key whose value may be `undefined` according to protocol semantics.

## Services and layers

- Define services around cohesive application capabilities, not around miscellaneous helpers.
- Let service requirements remain visible in the Effect type instead of hiding them in globals or service locators.
- Build Layers at composition roots and provide them near the runtime boundary.
- Separate service construction from service use. Reuse layers only when their resource lifetime and memoization semantics are correct.
- Keep provider SDKs, ORM clients, and runtime bindings behind application-owned service interfaces.

Follow the service-tag and layer APIs already used by the installed Effect version. Do not migrate between service-definition styles during unrelated work.

## Configuration and sensitive values

- Prefer Effect Config when the package already uses it; otherwise adapt the project's parsed configuration at the composition boundary.
- Use the installed version's redacted-value support for secrets and unwrap only at final I/O.
- Validate dependent configuration fields during layer construction so startup fails before serving work.

## Resources, concurrency, and streams

- Acquire resources with scoped constructors and keep their scope at least as long as every consumer.
- Prefer structured concurrency. Fork into a scope with an explicit owner; avoid untracked fibers.
- Bound parallelism and preserve ordering only when the contract requires it.
- Use Schedule-based retry and repetition so timing and limits are explicit and testable.
- Use Stream when work is incremental, backpressured, or resource-scoped; keep a collection when data is already bounded and materialized.
- Choose Queue, PubSub, or subscription primitives based on delivery semantics rather than as interchangeable channels.

## HTTP and external clients

- Wrap the Effect HTTP client or external SDK in an application-owned service.
- Translate transport status, decode failures, and provider errors at that boundary.
- Put timeout, rate limiting, retry, and fallback policy in the operation that understands idempotency and caller expectations.

## Testing

- Use the Effect-aware test utilities already configured by the repository.
- Supply test Layers implementing the real service contracts.
- Use deterministic clock and synchronization primitives for time and concurrency instead of sleeping.
- Test typed failures through the error channel and defects through the cause when the distinction matters.
- Verify acquisition and finalization for scoped resources.

## Completion check

- The Effect API choices match the installed version and nearby project style.
- Requirements, expected errors, and resource scopes remain visible in the effect graph.
- The runtime is executed only at an owning boundary.
- Retries, fibers, streams, and test layers preserve the operation's real semantics.
