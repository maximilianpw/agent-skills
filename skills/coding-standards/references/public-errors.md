# Public errors

Use this when a failure crosses a public boundary: an HTTP or RPC response, a CLI message, or an SDK error. Internal error design stays in [`failures.md`](failures.md); this reference governs what callers see.

## Messages

A public message is a product interface. Each one:

- names the operation or outcome that failed and gives the most specific safe reason known;
- offers an actionable way forward when one is known: correct the identified input, retry safely, reconcile the named resource, or contact support with a correlation ID when available;
- offers reassurance ("the document was unchanged") only when the operation could not have committed that change. Across a non-atomic operation, state the uncertainty and direct the caller to read the resource;
- uses calm, direct domain vocabulary, describing the problem rather than blaming the caller or a provider;
- has a stable code or literal message phrase that leads a plain-text search back to its owner.

## Public contract

Preserve an established error protocol, envelope, and SDK compatibility. These defaults do not authorize a wire-format migration. For a new structured error contract, use a discriminated union with:

- `code`: a stable, machine-readable literal per public failure variant;
- `message`: the operation-specific message above;
- `details`: safe structured context, typed per variant;
- `requestId`: the existing correlation identifier when the operation has request context;
- `retryable`: true only when repeating the same logical operation is safe and may succeed.

The public `code` is a compatibility contract independent of an internal class name or Effect `_tag`. An internal refactor must not silently change it. Pair each code with its own details schema rather than an unrestricted record.

Map these meanings onto the existing protocol when field names differ. A local CLI failure does not need a fabricated request ID or JSON envelope; a remote SDK failure should preserve the server's correlation identifier.

Retry guidance follows the operation's real idempotency. When an outcome is unknown, say whether retrying with the same idempotency key is safe; when a retry could start a second logical operation, do not advertise it as retryable.

## Translation and redaction

The public adapter translates each known internal error explicitly into its public variant. Keep unhandled known variants visible to the typechecker or exhaustive tests until someone selects their public outcome. At the outermost boundary, unexpected defects may use a generic public message with the available correlation identifier, never the cause, stack trace, or defect message. That fallback is not a substitute for classifying known failures.

Expose only authorized, safe identifiers and details. Credentials, access assertions, token claims, and raw payloads must not leak into public errors or telemetry. SQL, stack traces, internal causes, schema issues that echo payloads, and vendor response bodies are excluded from public output. Keep richer internal diagnostics only under the repository's redaction policy; correlate safe internal causes with the public identifier where available.

For HTTP, choose status from caller-visible meaning and the established API contract, not from the component that failed. Declare it in the owning contract and verify the actual response, including error headers and serialization.

## Completion check

Exercise each changed public failure through its adapter. Verify contract compatibility, code/detail agreement, safe output, and correlation where applicable. Check retry and reassurance claims against commit/idempotency behavior, including uncertain outcomes. Known failures retain explicit translations; unexpected defects produce only the sanitized fallback.
