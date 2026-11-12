# Effect testing

[Behavioral testing](../testing.md) owns test levels, public contracts, and faithful doubles. Use the installed `@effect/vitest` documentation for test helper signatures; keep its release compatible with the installed Effect version.

## Clock and synchronization

Use `it.effect` for the test-services environment, including TestClock. Use `it.live` only when real time or live runtime services are the behavior under test; it does not provide TestClock automatically.

Fork an effect that sleeps before advancing the test clock, and coordinate through readiness or observable state. Awaiting the sleep before advancing time deadlocks the test. Wall-clock sleeps are not evidence that another fiber reached a particular state.

Use a signal for one-shot readiness, a test-controlled queue for event sequences, and an observable state/control service for repeated interactions. Readiness must mean the required initialization completed, not merely that a fiber started. Test startup failure and post-readiness failure separately when a consumer can fail in either phase.

## Reusable test implementations

A reusable substitute must implement its advertised contract completely. Prefer the real local database/runtime when transactions, serialization, or protocol behavior matter. Tiny one-off partial doubles stay in their focused tests; `Layer.mock` can fail loudly for omitted operations but is not a faithful reusable implementation.

When reusable observation or failure injection is needed:

1. Keep production callers on the real `Service` tag.
2. Expose controls on a separate `TestService` tag, not production methods.
3. Acquire one backing object and provide it under both tags with `Layer.effectContext` so test controls affect the exact instance the caller uses.
4. Keep mutable state inside that Layer acquisition; test isolation must acquire fresh state rather than reuse a top-level object.

Use [test Layer names](effect-services.md#test-layers) that distinguish faithful in-memory behavior from a controlled test double. Members are function-valued, including zero-argument observations, so named operation boundaries apply consistently.

## Configuration

Provide a deterministic ConfigProvider when testing recipes. Supplying a decoded service bypasses decoding and cannot prove defaults, malformed-value failures, or provider precedence; see [provider tests](effect-configuration.md#providers).

## Verification

A concurrency test should fail if ordering, failure observation, interruption, or finalization is broken—not merely if the final return value changes. Check the public inference contract when types are behavior: input, success, expected errors, and requirements, including rejected call sites without rescue casts.
