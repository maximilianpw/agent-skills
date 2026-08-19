# State, events, and Effects

## Hook discipline

- Call ordinary Hooks only at the top level of function components or custom Hooks, before conditional returns.
- Keep Hooks out of loops, conditions, event handlers, class components, and ordinary functions.
- Name a custom Hook with `use` and give it one reusable state or synchronization contract; a forwarding wrapper around one library Hook is not automatically useful.
- Do not pass Hooks around as values or dynamically choose which Hook to call.
- React's `use` API is a documented exception that may run in loops or conditions, but it still runs during a component or Hook and not inside `try`/`catch`. Pass it a cached Promise supplied by a Suspense-aware framework, cache, or server component; creating a new Promise during every client render causes repeated suspension.

## Minimal state

State is the minimal changing information required to reproduce the UI.

- Derive values from props and state during render rather than storing synchronized copies.
- Avoid contradictory booleans; use one discriminated state when variants carry different valid data.
- Store an entity ID instead of duplicating the entity when the entity already exists in owned data.
- Group values that always transition together and flatten deeply nested update structures when practical.
- Keep URL state, server state, form drafts, workflow state, and ephemeral presentation state in their respective owners.

A typical ownership model is:

| State | Owner |
| --- | --- |
| Shareable filters, pagination, selection, and route identity | Router / URL |
| Reusable remote data and freshness | Server-state cache |
| Input drafts, touched fields, and client validation | Form or local form owner |
| Multi-step legal transitions | Feature reducer or explicit workflow model |
| Open menus, hover, temporary disclosure | Local component state |

## Render purity

Render is a calculation from current props, state, and context.

- Produce the same output for the same inputs.
- Do not perform network requests, subscriptions, DOM mutations, timers, logging side effects, or non-local mutation during render.
- Local mutation of a value created within the current render is fine.
- Treat props and state as immutable snapshots.
- Keep components safe under Strict Mode's development re-render and Effect setup/cleanup probes.

## Events versus Effects

Choose by why the work runs:

- A user interaction caused it: run it in that event handler.
- Rendering must synchronize with an external system: run it in an Effect.
- It is a display transformation: derive it during render.
- It is remote data coordinated by the framework: use the framework's loader/cache interface.

Effects are appropriate for subscriptions, browser APIs, non-React widgets, and external resources. They are not a general sequencing mechanism for application state.

For every Effect:

1. Name the external system being synchronized.
2. Include every reactive value read by setup and cleanup.
3. Make cleanup fully undo setup.
4. Handle stale asynchronous results or use the owning framework's cancellation primitive.
5. Keep user-event-specific work in the initiating handler.
6. Extract a purpose-built custom hook when several components own the same synchronization contract.

Do not suppress Hook dependency lint to force a lifecycle shape. Restructure ownership or make a non-reactive Effect event explicit when the current React version supports it.

## Resetting and adjusting state

When a changed identity should reset a whole subtree, give the subtree that identity as a `key`. This avoids rendering stale state and resetting it in an Effect.

Use an event to reset because the user requested reset. Derive a valid selection from current data when possible. Adjust state during render only for the narrow React-documented case where a key or derivation cannot express the requirement; keep the guarded comparison local.

## Reducers and workflow state

Use `useReducer` when many events transition related state or when incorrect combinations are recurring defects.

- Actions describe what happened.
- Reducers are pure and calculate the next state.
- Dispatch one meaningful action for one user interaction, even if several fields change.
- Use exhaustive action handling.
- Keep I/O, timers, navigation, and notifications outside the reducer.
- Prefer `useState` when transitions remain simple and independent.

A finite-state-machine library is justified by demonstrated concurrency, cancellation, persistence, visualization, or transition complexity—not merely by component size.

## Context

Try explicit props and composition before context. Context is appropriate for stable cross-cutting values or a cohesive screen provider, including locale, theme, current authority, routing, and reducer state/actions.

- Put the provider at the narrowest common owner.
- Expose domain- or application-facing values rather than third-party implementation details.
- Split contexts when read and action consumers have materially different update needs.
- Keep provider values stable where rerender breadth is significant, then measure before optimizing.
- Avoid a universal application context that hides dependencies and rerenders unrelated subtrees.

## Refs and imperative work

Use refs for values that must persist without affecting rendering and for narrow DOM operations such as focus, scroll, and measurement.

- Do not read or write `ref.current` during render except deterministic one-time initialization.
- Do not use refs as hidden render state.
- Avoid mutating DOM nodes React owns beyond operations React does not express.
- Expose a narrow imperative handle rather than a DOM or command surface when a parent genuinely needs imperative control.

## Transitions and deferred values

Use transitions for non-urgent updates that may be interrupted and for retaining already revealed content during navigation or expensive rerendering. Keep controlled input updates synchronous. Use a deferred value when a slow region may lag behind an input; it is not a fixed debounce.

Memoization is a performance tool, not a correctness mechanism. Preserve purity, measure a real rerender or calculation cost, then add `memo`, `useMemo`, or `useCallback` where the measurement and component interface justify it. When React Compiler is enabled and supported by the repository, let its automatic memoization remove the need for routine manual memoization; measure explicit exceptions.

## External stores

Use `useSyncExternalStore` for mutable stores or browser APIs outside React. Its snapshot must be immutable and referentially stable while unchanged, its subscription function should be stable, and SSR must provide a matching server snapshot when hydration requires one.

## Sources

- React, [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks)
- React, [`use`](https://react.dev/reference/react/use)
- React, [React Compiler](https://react.dev/learn/react-compiler)
- React, [Choosing the State Structure](https://react.dev/learn/choosing-the-state-structure)
- React, [Sharing State Between Components](https://react.dev/learn/sharing-state-between-components)
- React, [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
- React, [Separating Events from Effects](https://react.dev/learn/separating-events-from-effects)
- React, [Lifecycle of Reactive Effects](https://react.dev/learn/lifecycle-of-reactive-effects)
- React, [Preserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state)
- React, [Extracting State Logic into a Reducer](https://react.dev/learn/extracting-state-logic-into-a-reducer)
- React, [Passing Data Deeply with Context](https://react.dev/learn/passing-data-deeply-with-context)
- React, [Scaling Up with Reducer and Context](https://react.dev/learn/scaling-up-with-reducer-and-context)
- React, [Referencing Values with Refs](https://react.dev/learn/referencing-values-with-refs)
- React, [`useTransition`](https://react.dev/reference/react/useTransition)
- React, [`useDeferredValue`](https://react.dev/reference/react/useDeferredValue)
- React, [`useSyncExternalStore`](https://react.dev/reference/react/useSyncExternalStore)
- React, [Components and Hooks must be pure](https://react.dev/reference/rules/components-and-hooks-must-be-pure)
