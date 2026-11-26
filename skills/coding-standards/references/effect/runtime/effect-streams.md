# Streams

Use streams for many-valued sources whose demand, ordering, buffering, or subscription lifecycle matters. A repeated effect with no useful emitted values usually belongs in [scheduling](effect-scheduling-and-retry.md). Consult the pinned Stream documentation for source, transformation, and consumption APIs rather than recreating them.

## Delivery and ownership

Choose delivery semantics before choosing the primitive: a Queue hands an item to one consumer, a PubSub broadcasts to subscribers, and a SubscriptionRef supplies current state plus changes. Expose a Stream from the service; keep producer queues, mutable refs, and test controls private to their owners.

Backpressure is effective only where the producer cooperates. At a callback or externally pushed boundary, define what happens when the buffer fills: suspend where possible, drop newest, drop oldest, or fail. An unbounded buffer needs an independent bound on growth.

Preserve per-key ordering while allowing concurrency across independent keys. Choose queueing, replacement, or coalescing from application policy; contain keyed fiber bookkeeping in one owner. Use unordered processing only when the observable contract permits it.

## Long-lived consumers

A Layer-owned consumer needs **both scoped lifetime and explicit failure observation**: the scope stops it, and a supervision policy handles failure.

- Fork into the Layer's scope so acquisition can complete. If later service methods start work in that lifetime, capture the scope at acquisition and use it privately.
- `Effect.forkScoped` returns a Fiber immediately. A later failure does not become an error from the already-completed Layer acquisition. Dropping the Fiber handle is not a supervision policy.
- Before forking, attach the chosen typed-failure handling, or retain the Fiber for a supervisor to observe through `Fiber.await`/`Fiber.join`. Decide whether failure changes health/readiness, restarts with a bound, or stops the owning runtime. Logging alone is insufficient when callers would otherwise keep using a dead consumer.
- Keep defects and interruption distinct. Intentional shutdown must not trigger a restart loop; cause-level recovery belongs only to the explicit supervisor.

If startup requires the consumer to become ready, use an explicit readiness signal and observe failure before readiness. Successful fiber creation does not prove the subscription or listener initialized.

## Verification

Use finite fixtures only for finite sources. An open subscription fixture must remain open until the test deliberately closes or bounds it; collect only a stream known to terminate. Use test-controlled events and [clock/synchronization guidance](../testing.md#clock-and-synchronization) rather than sleeps.

Exercise readiness, post-acquisition consumer failure, and owner shutdown separately. Assert that failure is observed, health/restart behavior follows policy, and scope closure interrupts the consumer and releases its resources.
