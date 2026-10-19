# React

Inspect the installed React/framework versions, server/browser and hydration boundaries, and the project's routing, query, forms, styling, and localization libraries. Keep server authorization authoritative.

Trace each changed interaction through pending, empty, stale, success, missing, forbidden, and failed states. Account for keyboard/focus behavior, cleanup, cancellation, and recovery.

## Load by concern

- [Components and composition](react/components-and-composition.md): props, children, compound components, lists, identity, and abstraction boundaries.
- [State and Effects](react/state-and-effects.md): Hooks, state ownership, reducers, Effects, context, refs, transitions, or external stores.
- [Async, routing, and builds](react/async-routing-and-builds.md): fetching, mutations, SSR/hydration, TanStack Start/Router/Query, and Vite boundaries.
- [Forms and accessibility](react/forms-and-accessibility.md): forms, controls, dialogs, focus, responsive content, and localization.
- [Testing and performance](react/testing-and-performance.md): caller-visible UI changes; read browser, visual, bundle, and performance branches only when affected.

## React-specific decisions

- Start from the parent-visible component interface. Use props for values and callbacks, children or named slots for caller-owned structure, and typed data for closed vocabularies. Keep workflows in React logic rather than a page-building DSL.
- Give each state value one owner. Derive values during render, handle user-caused work in event handlers, and reserve Effects for synchronization with external systems.
- Keep render pure and component identity stable. Use intentional keys to reset state, not incidental remounting.
- Follow the async owner's cancellation and recovery model: for example, propagate Query's `queryFn` signal for Query-owned work rather than creating a competing lifecycle.
- Verify through rendered semantics and public interactions, not private state or Hook internals. Component tests do not prove CSS, hydration, or production chunk loading.
