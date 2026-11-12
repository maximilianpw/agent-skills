# Caching and batching

Use Effect's keyed cache when its TTL, capacity, eviction, and lifecycle semantics fit rather than maintaining a second in-flight map or LRU implementation. Check the pinned Cache, ScopedCache, and RequestResolver documentation for construction syntax.

## Choose by request shape

- Repeated or concurrent requests for the same key: `Cache` shares the pending lookup and can retain its result.
- Many distinct keys accepted by one backend batch operation: `Effect.request` with a `RequestResolver`; bound batch size and group distinct targets deliberately.
- Distinct keys with only per-item backend operations: bounded concurrency, optionally a cache for repeated keys. A resolver does not turn per-item calls into a batch endpoint.
- Cached resources requiring finalization: `ScopedCache`, with a lifetime compatible with its handles.

## Exit-aware TTL

A lookup failure or degraded fallback can be cached too. `Cache.makeWith` chooses TTL from the lookup's `Exit` and key. Use zero TTL for a transient failure or non-cacheable fallback so the current caller receives it and the next lookup can retry. Use a deliberate short negative TTL for stable misses when it protects the upstream.

A cache needs an intentional capacity, staleness policy, and owner. Construct it once per intended lifetime; a fresh cache on every call loses deduplication, while a global cache can retain resources beyond their valid scope.

## Acquire expensive clients once

Acquire stable clients once per owning Layer or scope. A canonical cache key identifies the remote resource; it does not extend the caller's I/O context. Request-bound clients stay request-bound even if their keys are stable. For Alchemy clients, apply [invocation-owned clients](effect-alchemy.md#invocation-owned-clients).

## Verification

Check concurrent same-key lookup, transient failure followed by recovery, TTL expiry, and invalidation where applicable. For resource caches, verify finalization and that reuse never crosses the handle's owning invocation or scope.
