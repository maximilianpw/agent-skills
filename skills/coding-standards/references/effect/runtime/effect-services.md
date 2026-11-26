# Effect services

Apply [ownership and adapter guidance](../modules-services-and-adapters.md) when deciding where a capability belongs. Use the pinned Effect documentation for service and Layer construction syntax; the rules here select ownership, lifetimes, and the local public surface.

## Service test

Treat a service as an **authority seam**, not merely an injectable value. It earns a contextual requirement by owning external I/O, persistence, credentials, configuration, time, randomness, resource lifecycle, cohesive application policy, or real runtime implementation variation.

Prefer an existing Effect service before adding one. Parsed inputs, per-call options, pure computations, and wrappers that only rename another API remain values or ordinary modules. A test-only desire to inject a value is not production evidence for a new service.

## Authority and requirements

The application capability owns its interface, tag, and expected errors. A concrete adapter owns its construction and Layers only when translation, mechanics, reuse, or implementation variation earns the separate module. A service provides only implementations it truthfully owns; the composition root selects the remaining concrete dependencies.

Yield stable dependencies during Layer construction and close over them. Yield request-, fiber-, or operation-scoped context inside the method that uses it. Request values, authorization evidence, scoped handles, and external constructor options remain explicit inputs when they are part of the operation's contract; do not turn them into services merely to avoid parameters.

## Module shape

For a new module-namespace API, use `Interface`, `Service`, `layerWithoutDependencies`, and `layer` as public role names. The namespace and tag identify the capability. Preserve an established capability-prefixed equivalent rather than renaming a compatible API.

- `layerWithoutDependencies` leaves requirements visible for composition; it does not mean the service has no dependencies.
- `layer` provides concrete dependency Layers selected by this module.
- Keep construction private. Inline it when one Layer uses it; use a file-local factory when several owning Layers share it. Export raw construction only for a concrete supported external caller, not test setup or composition convenience.
- Keep error and requirement channels precise through construction and extracted helpers.

## Module surface

Consumers import the owning leaf and yield its service tag. A module-namespace API may use `export * as UserStore from "./user-store.js"` when the toolchain supports self-exports; otherwise use ordinary named exports or the established public entrypoint. This is a local naming option, not a requirement to introduce a barrel or rewrite exports.

## Runtime wiring

Compose Layers before providing them. Choose `Layer.provide` when hiding an owned dependency and `Layer.provideMerge` only when downstream consumers should also receive it.

In current v4, nested `Effect.provide` calls can reuse Layers already built by an enclosing provide/runtime. Independent sibling calls do not share their newly built Layers. A Layer value is therefore not a process-wide singleton. Use `Layer.fresh` or `Effect.provide(layer, { local: true })` deliberately for isolated acquisition; verify the project's version before relying on memoization behavior.

Use `Layer.effectContext` when one acquisition supplies multiple tags backed by the same instance, such as a production service and its test controls. Reserve `Context.Reference` for ambient values with a safe, truthful default; a default must not conceal a missing required dependency.

Long-lived work needs both a lifetime owner and a failure observer. Read [stream supervision](effect-streams.md#long-lived-consumers) before starting a consumer from a Layer.

## Named operation boundaries

Use `Effect.fn("Capability.operation")` for public and non-trivial internal operations. Keep whole-operation concerns in its transforms, which receive `(effect, ...originalArgs)`. Use `Effect.fnUntraced` only when the missing stack/span metadata is intentional.

An error mapper is reusable only when its entire source error channel has one meaning and it preserves concrete error/requirement types. Otherwise use explicit tagged cases at the [translation boundary](../errors.md#boundary-translation). Name an earned helper for the error it creates; avoid a wrapper whose only job is forwarding another transform.

## Test Layers

Use `layerMemory` for a faithful in-memory contract and `layerTest` for an implementation with test controls or failure injection. Prefer a real local substitute when transactions, serialization, or protocol semantics matter. A one-off fake stays in its test rather than creating production exports.

When reusable test controls are needed, [Effect testing](../testing.md#reusable-test-implementations) defines how they share the production implementation without entering the production interface.

## Verification

Show the production reason for each new service, the owner that selects each implementation, and the scope that acquires/releases it. Test isolation and repeated calls must demonstrate the intended acquisition count and lifetime, not merely the expected return value.
