# HTTP clients

Default to Effect HttpClient for outgoing application/provider HTTP. Current v4 exports these modules from `effect/http`; older prereleases used `effect/unstable/http`, which has no compatibility export in the checked 4.1.4 baseline. Import-path stability and API stability are separate: these APIs can still be marked unstable. Follow the [version-matched source rule](effect.md#source-rule).

## Boundary ownership

The outbound adapter or private concrete client owns request construction, authentication, cancellation, status classification, decoding, typed failure translation, and safe diagnostics. Application code receives domain values and failures rather than transport responses.

Classify status before decoding a success body; executing a request does not by itself establish a successful application response. Keep transport failures, rejected statuses, and invalid success payloads distinct enough for the caller to select policy. Use the pinned client/response documentation for combinator signatures.

## Retry and rate limits

Use client-level transient retry for transport/status failures only when repeating that request is safe. Use operation-level retry when the decision needs domain errors, payloads, or a logical idempotency key. Avoid stacking both policies without accounting for the multiplied attempts and deadline.

`HttpClient.withRateLimiter` retries HTTP 429 responses **without limit by default** in the checked baseline. Choose `times`, an overall deadline, or an explicitly unbounded worker policy. `times: 0` disables automatic retries; disabling response inspection does not. Pacing and honoring `Retry-After` do not establish mutation idempotency.

Apply [scheduling](effect-scheduling-and-retry.md) when the provider's delay, retry budget, or operation deadline needs custom policy.

## Raw fetch exception

Raw `fetch` is appropriate for a platform transport or a library/runtime boundary that cannot depend on Effect's HTTP modules. This exception does not remove the boundary's responsibilities:

- Pass the `AbortSignal` supplied by `Effect.tryPromise` to `fetch`; wrapping a Promise without wiring cancellation does not cancel the request.
- Classify status before success decoding, and classify body-read/decoding failures separately.
- Parse unknown response data into the owning application contract.
- Retain only safe diagnostic context, never credentials or raw sensitive payloads.

A boundary that can depend on Effect HttpClient should use it when shared transforms, retry, or rate limiting would otherwise be reimplemented. An interrupted or timed-out mutation may already have committed remotely; apply [uncertain-outcome handling](../workflows-transactions-and-idempotency.md#uncertain-outcomes-and-compensation).

## Verification

Test rejected status, malformed success body, interruption, retry exhaustion, and safe diagnostics through the owning boundary. For a mutation, prove that both automatic and operation-level retries preserve its idempotency contract.
