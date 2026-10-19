# Types and state

## Compiler posture

- New configurations should enable `strict`. Consider `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` when their migration cost is acceptable.
- Preserve established compiler settings during focused work; stricter flags require an explicit migration because they can create package-wide changes.

## Unknowns and assertions

- Use `unknown` for values whose shape has not been established. Narrow or parse before use.
- Avoid `any`. Keep unavoidable interop `any` at the smallest boundary, explain why it cannot be typed, and expose a safe type inward.
- Avoid non-null assertions and broad casts. Prefer control-flow narrowing, parsing, or a small assertion function.
- When an assertion represents an invariant the compiler cannot see, state that invariant beside the assertion.
- `as const` and `satisfies` are normal type-shaping tools, not suspicious casts.

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

- Keep public entrypoints intentional. Avoid exporting helpers solely to make tests reach private implementation.
- Put provider and framework types behind the module that owns that integration.
- Prefer a cohesive module over a collection of shallow helpers, but keep a helper local when only one implementation needs it.

## Completion check

- No unbounded `any`, unexplained non-null assertion, or broad cast was added.
- State variants and mixable values cannot be confused accidentally at the changed boundary.
- New exports are intentional, stable enough to support callers, and consistent with local conventions.
