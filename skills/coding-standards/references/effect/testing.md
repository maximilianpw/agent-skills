# Effect testing

Shared [testing](../testing.md) owns assertions on observable outcomes and the choice of test doubles; this file specializes it for Effect-owned behavior. Use the installed `@effect/vitest` documentation for test helper signatures; keep its release compatible with the installed Effect version.

## Test through real interfaces

Every caller-visible feature has an end-to-end happy-path test through its real public entrypoint when the normal test environment can run it reliably.

Add end-to-end coverage for expected error paths that the public entrypoint can exercise reliably. Cover remaining important failures at the closest real interface. Report why end-to-end coverage is impractical when unreliable third parties or unreasonable setup, runtime, or cost prevent it.

Prefer tests by confidence:

1. end-to-end tests through real public entrypoints;
2. integration tests through real interfaces;
3. focused/property tests for pure Domain Modules;
4. unit tests for meaningful behavior rather than implementation details.

Replace Effect-owned behavior through services and Layers, local database substitutes such as SQLite, faithful in-memory implementations, or fake external implementations, never through `vi.mock` or `jest.mock`. Prefer a recording implementation and inspect its public records over spying on implementation methods.

## Clock and synchronization

Use `it.effect` for the test-services environment, including TestClock. Use `it.live` only when real time or live runtime services are the behavior under test; it does not provide TestClock automatically.

Fork an effect that sleeps before advancing the test clock, and coordinate through readiness or observable state. Awaiting the sleep before advancing time deadlocks the test. Wall-clock sleeps are not evidence that another fiber reached a particular state.

Use a signal for one-shot readiness, a test-controlled queue for event sequences, and an observable state/control service for repeated interactions. Readiness must mean the required initialization completed, not merely that a fiber started. Test startup failure and post-readiness failure separately when a consumer can fail in either phase.

A concurrency test should fail if ordering, failure observation, interruption, or finalization is broken, not merely if the final return value changes.

## Property tests and arbitraries

Assess property-based testing for every changed invariant, transition, normalization, equivalence, ordering, idempotence, or roundtrip. Add property tests when generated inputs cover meaningful cases beyond a short example list. Apply this assessment especially to parsers, smart constructors, branded/refined types, state machines, serialization, and lawful combinators.

Use `fast-check` in normal TypeScript projects. In Effect projects, prefer Effect's FastCheck integration and derive arbitraries from owning Schemas when available.

Keep reusable arbitraries beside the domain module they support. Add a shared test-data entrypoint only when multiple consumers need one:

```txt
src/billing/
  invoice-number.ts
  invoice-number.test.ts
  invoice-number.arbitrary.ts
```

Valid generated domain data passes through production parsers or constructors. Corruption and rejection tests instead construct invalid external representations independently of the schema under test, then enter through its real boundary; otherwise removing the very refinement being tested can also weaken the fixture.

## Parsing and recovery regressions

Test application-owned transformations, cross-field filters, representation selection, and public failure behavior rather than restating a schema library's ordinary struct/brand mechanics. For a changed boundary, include positive current/legacy cases and negative malformed or hybrid evidence where applicable. Assert that rejected persisted authority remains intact and migration/state writes do not partially commit.

When removing a read, parse, or checkpoint, verify its distinct invariant and observable work through the owning interface. A focused deliberate-regression probe can show that a test fails when a refinement or source-precedence check is removed. Keep runtime recovery claims bounded: real SQLite reconstruction, a native runtime restart, and deployed recovery establish different evidence.

## Test implementations

A dependency interface represents real ownership or variability, not a test-only desire to mock.

- Keep a narrow one-off fake local to its test.
- Export a reusable static or recording implementation when its complete behavior is useful across tests.
- Use an established conventional name when it communicates expected behavior, such as `TestClock`.
- Otherwise use the shortest truthful behavior/implementation qualifier, such as `InMemoryCache`, `RecordingEmailSender`, `NoopEmailSender`, or `FailingEmailSender`.
- Use SQLite or another real local substitute when queries, schema, serialization, transactions, or protocol behavior matter.
- Use and name an implementation as in-memory only when it faithfully preserves the complete observable contract under test.

Keep production branches, exports, flags, and behavior determined by production needs. Test through an existing public interface or a faithful inert harness when no real dependency interface exists.

### Reusable test implementations

A reusable substitute must implement its advertised contract completely. Prefer the real local database/runtime when transactions, serialization, or protocol behavior matter. Tiny one-off partial doubles stay in their focused tests; `Layer.mock` can fail loudly for omitted operations but is not a faithful reusable implementation.

When reusable observation or failure injection is needed:

1. Keep production callers on the real `Service` tag.
2. Expose controls on a separate `TestService` tag, not production methods.
3. Acquire one backing object and provide it under both tags with `Layer.effectContext` so test controls affect the exact instance the caller uses.
4. Keep mutable state inside that Layer acquisition; test isolation must acquire fresh state rather than reuse a top-level object.

Use [test Layer names](runtime/effect-services.md#test-layers) that distinguish faithful in-memory behavior from a controlled test double. Members are function-valued, including zero-argument observations, so named operation boundaries apply consistently.

## Configuration

Provide a deterministic ConfigProvider when testing recipes. Supplying a decoded service bypasses decoding and cannot prove defaults, malformed-value failures, or provider precedence; see [provider tests](runtime/effect-configuration.md#providers).

## Compile-time behavior

When inference is public behavior, add compile-time tests using ordinary call sites without rescue annotations or casts. For parser/service API changes, assert the complete function contract: input, arity/options, success, expected errors, and Effect requirements where applicable. Include rejected calls as well as inferred results; parameter-only assertions can miss an error or requirement channel widened by extraction.

## Completion check

Every changed caller-visible behavior has an end-to-end happy path or a reported concrete blocker; each expected error path is covered at the highest reliable real interface or has a reported concrete blocker; every changed property named above has been assessed and applicable property tests are present; changed public inference has complete signature and accepted/rejected-call tests; tests cross real interfaces without module mocks; valid generated domain data preserves production invariants while invalid boundary fixtures independently challenge them; changed parsing/recovery behavior satisfies the regression guidance above; production surfaces remain determined by production needs; and every reusable test implementation truthfully matches its name and complete observable contract.
