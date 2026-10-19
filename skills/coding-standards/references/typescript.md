# Types and state

## Compiler posture

- New configurations should enable `strict`. Consider `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` when their migration cost is acceptable.
- Preserve established compiler settings during focused work; stricter flags require an explicit migration because they can create package-wide changes.

## Preserve established types

A type is evidence of where a value came from and which invariants already hold. Carry the strongest owner-provided type (domain, library, or platform) through parameters, returns, and transformations:

```ts
// Discards the library's contract.
const transformOperation = (value: Record<string, unknown>): Record<string, unknown> => { /* … */ };

// Preserves it.
const transformOperation = (operation: OpenApiOperation): OpenApiOperation => { /* … */ };
```

- Use `unknown` for decoder inputs, generic infrastructure that walks arbitrary data, and caught errors (named `cause`). Parse untrusted boundary values into the strongest meaningful type. Keep ordinary static types for props, callbacks, React nodes, internal state, and values passed between your own functions.
- Values created by your code or already validated are known. Keep their type even when a receiving API is inconvenient. A typed API alone does not prove runtime validation; inspect its trust boundary before treating a response as validated.
- Before writing a local structural type, search the owning module or library for its exported type, schema, or generic parameter.
- When a value gains a new invariant, establish the stronger type with its owning constructor or schema, starting from the known source type rather than re-parsing from `unknown` or round-tripping through JSON.
- When a library is typed more broadly than the value it supplies, prefer a first-class API, an upgrade or upstream fix, a parsed boundary adapter, or dropping the unsupported behavior.

## Unknowns and assertions

- Use `unknown` for values whose shape has not been established. Narrow or parse before use. Prefer plain discriminant checks; write a named type guard when the narrowing repeats or is not obvious.
- Avoid `any`. Keep unavoidable interop `any` at the smallest boundary, explain why it cannot be typed, and expose a safe type inward.
- Avoid non-null assertions and broad casts. Prefer control-flow narrowing, parsing, or a small assertion function.
- A widen-then-assert chain (`as unknown as T`, `as any as T`, or the same thing across statements) fabricates evidence it threw away; redesign the boundary instead.
- `as const` and `satisfies` are normal type-shaping tools, not suspicious casts.

Fix type and lint findings with the real type, a simpler signature, control-flow narrowing, or boundary validation first. Keep unavoidable casts, `any`, and non-null assertions at the smallest untyped-input boundary, with a local reason and a safe type exposed inward. If a module needs broader lint accommodation, use a scoped override with its reason, not project-wide permission. An assertion requires a runtime invariant that already holds and that TypeScript cannot express. As a last resort inside a library's internals (never its public signatures or an application), an assertion may also preserve a better public API, such as inference callers would otherwise lose; that case may chain through `unknown` when TypeScript reports the types do not overlap. Either way, write directly above the assertion:

```ts
// SAFETY: every registry member is a pool class whose `.make()` returns a Layer for that same
// pool, so the mapped type holds at runtime; TypeScript cannot relate the two mapped types.
// Verified by: registry.test.ts "the registry Layer requires every pool body"
// oxlint-disable-next-line typescript/consistent-type-assertions
const bodies = layers as unknown as RegistryBodies<Pools>;
```

- `SAFETY:` proves the runtime type: where the value comes from, which invariant guarantees it, and why the compiler cannot see it.
- `Verified by:` names the tests that fail if the invariant breaks.
- The narrowest lint suppression for exactly the rules that fire, when the repository's lint flags the assertion.

Keep each assertion to one expression, as close to the value's origin as possible.

## Public contracts

- Make exported inputs, outputs, and failure-bearing results understandable without reading the implementation.
- Add explicit return types where they stabilize a public boundary; preserve useful inference for local implementation details.
- Use `readonly` where callers should not mutate a value. Do not spread `readonly` mechanically through private code.
- Prefer an options object when positional arguments are easy to transpose or when boolean flags obscure intent.

## Domain meaning

- Reuse the repository's domain vocabulary.
- Introduce branded IDs or unit types when same-shaped primitives can realistically be mixed up across a boundary. Do not brand every string by default.
- Represent lifecycle variants with a discriminated union when each state carries different valid data.
- Handle closed unions exhaustively. An unreachable branch should fail close to the missing case.
- Distinguish missing, empty, pending, and failed states when they produce different behavior.

## Files and exports

- Keep public entrypoints intentional. Avoid exporting helpers solely to make tests reach private implementation. Before changing exports, inspect package entrypoints, re-exports, type-only/dynamic uses, and external published consumers; no local hit does not prove an SDK API is unused. Apply compatibility/versioning policy to public changes.
- Use `import type` and `export type` for type-only edges. Use static imports for ordinary dependencies; dynamic imports belong to lazy-loading, optional-runtime, plugin, or code-splitting boundaries.
- Use ES modules for application grouping; reserve TypeScript `namespace` for required interop.
- Put provider and framework types behind the module that owns that integration.
- Prefer a cohesive module over a collection of shallow helpers, but keep a helper local when only one implementation needs it.

## Completion check

- Known values keep their owner-provided types through every changed signature; `unknown` is limited to decoder inputs, genuinely arbitrary-data infrastructure, and caught `cause` values.
- No unbounded `any`, unexplained non-null assertion, or broad cast was added; every assertion carries `SAFETY:` and `Verified by:` lines, and every widen-then-assert chain is a library-internal one that meets the rule above.
- State variants and mixable values cannot be confused accidentally at the changed boundary.
- New exports are intentional, stable enough to support callers, and consistent with local conventions.
