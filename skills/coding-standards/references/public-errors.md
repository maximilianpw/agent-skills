# Public errors

Use this when a failure crosses a public boundary: an HTTP or RPC response, a CLI message, an SDK error, or any error another team or agent reads. Internal error design stays in [`failures.md`](failures.md); this reference governs what callers see.

## Messages

A public message is a product interface. Each one:

- names the operation or outcome that failed and gives the most specific safe reason known;
- ends with a way forward: correct the identified input, retry the same operation, read back or reconcile the named resource, or contact support with the request ID;
- offers reassurance ("the Account name was unchanged") only when the operation could not have committed that change. Across a non-atomic operation, state the uncertainty and direct the caller to read the resource;
- uses calm, direct domain vocabulary, describing the problem rather than blaming the caller or a provider;
- begins with a stable literal phrase, so a reported message searches straight back to its source.

```text
Pool checkout has no run wfp-missing. Check the run ID; it comes from the dispatch response.
```

## Envelope

Serve every public failure in one envelope:

- `code`: a stable, machine-readable literal per failure variant;
- `message`: the operation-specific message above;
- `details`: safe structured context, typed per variant;
- `requestId`: correlates the response with traces and logs;
- `retryable`: true only when repeating the same request is safe and may succeed.

Model the envelope as a discriminated union on `code`, each variant with its own `details` schema. An unrestricted details record lets a code and its details disagree; the union makes them agree by construction.

`retryable` follows the operation's real idempotency. When an outcome is unknown, say whether retrying with the same idempotency key is safe; when a retry could start a second logical operation, the error is not retryable.

## Translation

The public adapter translates each known internal error explicitly into its public variant. Exhaustive translation turns a newly introduced failure into a compile error until someone chooses its code, status, message, details, and retry guidance; a catch-all fallback hides that decision.

Public output carries the operation, the requested domain IDs, and the classified reason. Credentials, access assertions, token claims, raw request bodies, SQL, stack traces, internal causes, schema issues that echo payloads, and vendor response bodies stay in internal telemetry, correlated by `requestId`.

## HTTP status

Choose status from the caller-visible meaning, not from the component that failed:

| Status | Meaning |
| --- | --- |
| `400` | The caller can correct malformed or invalid request data. |
| `401` | The request could not be authenticated. |
| `403` | The authenticated caller may not perform the operation. |
| `404` | A syntactically valid resource identity is unknown. |
| `409` | Current resource state conflicts with the operation. |
| `415` | The request uses an unsupported media type. |
| `500` | An internal invariant failed or a non-transient internal failure occurred. |
| `503` | A required capability is temporarily unavailable. |

## Completion check

Every changed public failure:

1. names what failed and the most specific safe reason;
2. carries typed `details` that agree with its `code`;
3. tells the caller how to correct, retry, reconcile, or escalate;
4. makes only provably true reassurance and retry claims;
5. reads calmly in domain vocabulary;
6. has a message or code searchable in the source;
7. carries a `requestId` that matches traces and logs;
8. excludes secrets, internal causes, and raw external data;
9. is translated explicitly at its boundary, never by a catch-all.
