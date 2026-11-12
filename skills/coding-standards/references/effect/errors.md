# Errors

## Expected failures are values

Every known failure mode appears in the return type as a custom tagged error, even when the immediate caller cannot recover. A caller handles the error or returns it upward. The outermost boundary translates it into a valid outcome such as an HTTP response, CLI exit code, retry decision, dead letter, or startup error message.

Known failures include domain, parsing, authorization, integration, I/O, persistence, configuration, and workflow failures.

Represent workflow failures in the `E` channel of `Effect.Effect<A, E, R>`, rather than nesting a Result in its success channel or rejecting a Promise. A pure Result-returning decoder remains valid outside that workflow channel. At an unavoidable Promise boundary, the owning Adapter or private service implementation uses the pinned Effect interop API to classify rejection before it crosses the service interface. Preserve interruption and defects rather than translating every cause into an expected failure.

## Defects

Throw or panic only when a defect makes correct execution impossible, rather than because the current caller lacks a recovery strategy. Defects include:

- violated internal invariants;
- impossible branches;
- temporary `notYetImplemented` paths;
- catastrophic runtime conditions.

Known configuration failures are values; the composition root reports them safely and terminates startup.

Use the repository's established defect mechanism; otherwise use the runtime's native throw or panic. Reuse shared defect helpers when they carry stable semantics or serve multiple callers:

```ts
export function casesHandled(unexpectedCase: never): never;
export function shouldNeverHappen(msg?: string): never;
export function notYetImplemented(msg?: string): never;
```

Use `casesHandled` for exhaustive union handling. Keep a defect helper local until stable semantics or reuse earns shared ownership.

## Custom errors

Use the pinned Effect Schema tagged-error constructor; see [Effect schema errors](runtime/effect-schema-and-data.md#errors) for version-aware selection and payload handling.

A custom error includes:

- a stable tag supplied by the tagged-error constructor;
- a useful message explaining what failed, why when known, and how to recover when actionable;
- structured contextual fields with the relevant operation and safe domain/provider data;
- safe telemetry fields;
- an optional `cause: unknown`.

Keep distinct failure modes as granular error types and union them at the operation boundary. Combine failures only when callers handle them the same way, they need the same observability, and structured fields preserve the useful context.

The error that owns a failure constructs its stable message. Begin the message with a stable literal phrase that leads a plain-text search back to the owning error definition, then append dynamic context. Callers may add safe context or translate the error at an outer boundary. Error classification uses tags and fields rather than matching message text.

Model absence according to the operation's meaning. Return an optional value when missing data is an ordinary result for the caller to interpret. Return a typed not-found error when the operation requires the value or absence violates its local invariant or precondition.

Keep error unions precise at module boundaries:

```ts
Effect.Effect<User, UserNotFound | UserStoreUnavailable>
```

Broad `AppError`-style types belong near entrypoints, orchestration, logging, and rendering layers.

## Boundary translation

Translate only at the owner that knows the protocol or recovery policy. For a tagged Effect error union, prefer explicit `Effect.catchTag` / `Effect.catchTags` cases: pass already-correct application errors through unchanged and map each boundary failure by its known meaning. Leaving a new tag in the inferred error channel makes an unchosen policy visible to the compiler.

Use `Effect.mapError` or a shared error mapper when the complete input error channel intentionally has one meaning. A generic helper must preserve safe context and concrete error/requirement types, rather than collapsing distinct failures for convenience. Defects and interruption remain distinct from expected failures; cause-level recovery belongs to an explicit supervision boundary. A lost mutation response carries uncertainty, not proof of failure; apply [workflow safety](workflows-transactions-and-idempotency.md#uncertain-outcomes-and-compensation).

For documentation of expected typed failures, describe outcomes rather than using `@throws`. Reserve `@throws` for defects, framework-required throwing, or temporary `notYetImplemented` paths. Shared [comment rules](../comments-and-docs.md) still apply.

## Public error schemas

When a failure reaches an external caller, apply [public errors](../public-errors.md) for contract compatibility, messages, retryability, and redaction. For an Effect `HttpApi` boundary:

- Declare schema-backed public variants matching the established wire contract, or the newly defined public contract when no API exists yet. Use the pinned `HttpApi` annotations for HTTP status and list each variant in the endpoint's error schemas so generated OpenAPI agrees.
- Translate known internal errors explicitly with `Effect.catchTags`. Leave unhandled tags visible in the inferred error channel until the boundary selects their policy; verify the final handler satisfies the declared API error contract.
- Reuse the existing correlation context for the public identifier and trace span. CLI and SDK adapters follow their own public contract rather than acquiring an artificial HTTP envelope.

## Completion check

For each changed failure path, verify its inferred error union and observable boundary outcome, including redaction and recovery guidance. Adding a known failure must require an explicit boundary decision. Check that interruption, defects, ordinary absence, and uncertain mutation outcomes remain distinguishable rather than becoming a generic error.