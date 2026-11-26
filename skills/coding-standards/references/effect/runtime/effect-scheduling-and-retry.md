# Scheduling and retry

Use the pinned Schedule documentation for combinator signatures. [Workflow safety](../workflows-transactions-and-idempotency.md) owns idempotency and retry placement; this reference covers failure-channel and timing traps.

## Retry and repeat are different policies

`Effect.retry` retries typed failures, not defects or interruption. `Effect.repeat` repeats successes; an unhandled failure ends the loop. The initial run happens before the schedule is stepped, so `Schedule.recurs(3)` permits three additional attempts, not three total attempts.

Choose completion-relative spacing for polling that should rest after work, or cadence-based scheduling when wall-clock alignment matters. Backoff with jitter prevents synchronized retries, but is not a termination policy: choose an attempt bound, deadline, or explicitly unbounded worker lifetime.

Wrapping a multi-step operation in retry repeats its earlier successful mutations too. Put retries at the owner with a proven repeated-execution guarantee; preserve exhaustion as a typed failure unless that owner has a truthful fallback.

## Polling and per-item isolation

A polling pass or batch item may recover an expected failure only when product policy permits continuing, retrying later, or skipping it. Recover around that pass/item, not around the entire worker by accident.

`Effect.ignore` discards typed failures but not defects; combining it with logging deliberately changes failure into success and therefore allows repetition. Do not use it to make a worker appear healthy while required work has stopped.

A supervisor that recovers causes must preserve interruption. An intentional shutdown should end the worker, not be logged and retried as an operational failure.

## Provider limits and deadlines

When a provider gives a retry delay, use at least that delay rather than replacing it with a shorter backoff. State whether the deadline covers each attempt or the whole logical operation, including delays.

For HTTP-level 429 handling, use [HTTP client guidance](effect-http-clients.md#retry-and-rate-limits); its helper has an unbounded retry default that must be chosen deliberately.

## Verification

Use [TestClock and explicit synchronization](../testing.md#clock-and-synchronization) to check initial versus additional attempts, delays, exhaustion, interruption, and partial side effects. Every retry path states the guarantee making a repeated mutation safe; every loop has an owner and a termination policy.
