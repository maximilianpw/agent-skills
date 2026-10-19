# TypeScript additions for Effect

Apply [shared TypeScript rules](../typescript.md) for type provenance, assertions, and the documented, test-backed library-internal exception. This reference adds only the Effect codebase conventions below.

## Compiler posture

New or changed TypeScript configurations enable `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, and `noFallthroughCasesInSwitch`. A legacy configuration that cannot adopt a flag within the changed behavior records the blocking diagnostics and migration boundary rather than silently weakening the rule.

## Values and signatures

- Prefer immutable values. Localize mutation in imperative shells, performance-sensitive internals, builders, or adapters, behind precise interfaces.
- Exported interface methods and public class methods have explicit return types. Exported functions returning objects, unions, or collections also state their return types. Local callbacks and unexported helpers use inference when it preserves the complete contract.
- Use concise inline return types; introduce a named result contract only when its domain meaning or reuse earns the name. Derive it from its owning schema rather than duplicating types.
- Preserve exact success, error, and Effect requirement types through extraction.
- Resolve optionality by branching, parsing, or refining before use; do not add non-null assertions in Effect code.

## Completion check

Compiler exceptions have diagnostics and a migration boundary; mutation is contained; exported signatures follow the rules above; and every cast or unavoidable `any` meets the shared safety and test-evidence requirements.
