# Failures and asynchronous work

## Classify outcomes

Separate three cases before choosing a representation:

- **Ordinary absence:** a normal outcome such as an optional lookup miss.
- **Recoverable error:** a caller may recover, retry, translate, or present it.
- **Programmer error:** an invariant is broken or the program reached an impossible state.

Use the repository's established mechanism for recoverable errors. That may be typed error classes routed through middleware, a `Result` type, a discriminated union, or another explicit convention. Do not impose a new result library on an exception-based codebase during unrelated work.

Throw when an invariant is broken. Recoverable errors may also throw when the surrounding framework makes the thrown type part of the documented contract.

## Error design

- Give programmatically handled errors a stable discriminant and structured fields.
- Classify errors by type or tag, never by parsing their human message.
- Write messages for operators and users, while keeping secrets and sensitive values out.
- Translate SDK, database, and protocol failures inside the adapter that owns that dependency.
- Preserve a useful cause when translation would otherwise destroy diagnostic context.
- Catch only when adding policy, translation, cleanup, or context. Do not catch merely to log and rethrow the same error.

## Absence

- Return an optional value when missing is routine and the caller can continue.
- Return or throw a typed not-found failure when the operation promises that the value exists.
- Do not use empty strings, sentinel numbers, or unrelated exceptions to encode absence.

## Promises and cancellation

- Await or intentionally retain every promise. Mark deliberate background work and give its failures an owner.
- Accept or propagate `AbortSignal` across cancellable I/O boundaries when the surrounding stack supports it.
- Use `Promise.all` only when operations are independent and concurrent failure semantics are acceptable. Use sequential execution when order or partial effects matter.
- Bound concurrency for large or untrusted collections.
- Release resources with the runtime or repository's established disposal mechanism, or with `finally` when no stronger abstraction exists.

## Retry and timeout

- Add retries only for classified transient failures.
- Check that the operation is idempotent or protected by an idempotency key before retrying a side effect.
- Bound attempts and elapsed time; include backoff and jitter for shared services.
- Keep timeout, retry, and fallback policy in the use-case owner rather than hiding it inside a generic client.

## Completion check

- Every new error path has an intentional representation and owner.
- No promise, cancellation path, detached task, or resource lifetime is orphaned.
- Retry and concurrency choices preserve side-effect correctness.
