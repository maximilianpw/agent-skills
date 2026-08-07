# Testing TypeScript behavior

## Test through meaningful interfaces

- Exercise caller-visible behavior through the real public interface whenever practical.
- Assert outputs, state transitions, persisted effects, and externally visible errors rather than private call sequences.
- A call count is appropriate when the interaction itself is the contract, such as deduplication or retry limits.
- Keep test placement, naming, and runner usage consistent with the repository.

## Choose test doubles deliberately

Prefer a real in-memory or local implementation when it preserves production semantics at reasonable cost. Use a small fake that implements the real application-owned interface when infrastructure is unsuitable.

Use module mocks when the repository convention or boundary makes them the clearest option. Do not rewrite an established mocked suite as a side effect. Avoid mocks that permit impossible behavior or duplicate implementation details.

## Cover risky shapes

- Table-test state transitions and error classification.
- Use property-based tests for parsers, encoders, round trips, and invariant-heavy calculations when examples leave a large input space uncovered.
- Control time and randomness rather than sleeping or relying on wall-clock timing.
- Test cancellation, timeout, retry exhaustion, and partial side effects when the changed operation owns those policies.
- For a bug fix, demonstrate that the test fails on the original behavior and passes with the fix when doing so is practical.

## Keep types honest

Test data should satisfy the same public contracts as production data. Prefer builders or `satisfies` over broad casts. A deliberate invalid fixture should cross the same untrusted boundary that receives invalid data in production.

Do not export private helpers solely for direct tests. If behavior cannot be tested without reaching through the public surface, reconsider whether the module boundary is hiding too much or the test is asserting implementation detail.

## Completion check

- Every changed caller-visible path has proportionate evidence.
- Tests can fail for the behavior they claim to protect.
- Test doubles preserve the contract relevant to the assertion.
- The repository's focused test and typecheck commands were run and their output inspected.
