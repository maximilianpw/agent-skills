---
name: react-standards
description: Production React standards for components, hooks, rendering, forms, accessibility, async UI, and tests. Use when designing, implementing, refactoring, or reviewing non-trivial React code, including React applications built with TanStack or Vite.
license: MIT
---

# React Standards

Build React interfaces as pure, compositional renderers over explicit state and side-effect owners. Fit the repository before improving it: task requirements and local rules govern, established compatible patterns follow, and these standards supply defaults where the codebase is silent.

For trivial or mechanical edits, match the surrounding code and stop. Do not turn focused work into a component-system, state-library, or framework migration.

## Establish the local model

Read the nearest repository instructions, package manifest, framework and build configuration, affected components, and nearby tests. Identify:

- React and framework versions;
- client, server, SSR, hydration, and routing boundaries;
- server-state, form, styling, localization, and component libraries;
- accessibility, browser, visual, bundle, and production verification gates.

**Complete when:** the governing files and installed versions have been identified, the changed UI's local conventions have been inspected, and its server/browser execution paths are accounted for.

## Trace the user-visible behavior

Trace the changed experience from route or parent input through rendering, interaction, asynchronous work, and recovery. Account for:

- content and actions composed by the parent;
- URL, server, form-draft, workflow, and ephemeral presentation state;
- pending, empty, stale, success, missing, forbidden, and failed states;
- focus, keyboard, labels, announcements, responsive layout, and localization;
- external systems synchronized by Effects and cleanup;
- the component, hook, route, and browser tests that observe the behavior.

Load each matching reference completely before designing:

- [`references/components-and-composition.md`](references/components-and-composition.md) when a component interface, props/children split, compound pattern, list identity, or data-driven UI changes.
- [`references/state-and-effects.md`](references/state-and-effects.md) when Hooks, state ownership, reducers, Effects, context, refs, transitions, or external stores change.
- [`references/async-routing-and-builds.md`](references/async-routing-and-builds.md) when data fetching, routing, mutations, SSR/hydration, server/client code, TanStack Start/Router/Query integration, or a Vite build boundary changes.
- [`references/forms-and-accessibility.md`](references/forms-and-accessibility.md) when a form, field library, dialog, interactive control, focus behavior, responsive content, or localization behavior changes.
- [`references/testing-and-performance.md`](references/testing-and-performance.md) whenever caller-visible React behavior changes; apply its browser, visual, bundle, and field-performance branches only when those contracts are affected.

Also load `typescript-standards` when types, errors, async boundaries, external data, or TypeScript tests change. Its general signal-propagation rule still applies: propagate the cancellation signal supplied by the operation's actual owner, such as Query's `queryFn` signal for Query-owned work.

**Complete when:** each state, side effect, interaction, and recovery path has one owner and maps to the applicable references.

## Design from composition inward

Start with the parent-visible interface: what values and behavior are props, what structure is composed as children or named slots, and what state remains private.

- Use props for data, finite variants, and event callbacks.
- Use children or React-node slots for substantial caller-owned structure.
- Use typed data definitions for closed vocabularies such as navigation, statuses, filters, or columns.
- Keep workflows with branching behavior as explicit React and state logic rather than a page-building configuration language.
- Extract an abstraction when it hides repeated policy or creates a real seam. Prefer composition over boolean-prop growth, home-grown render callbacks used mainly as escape hatches, or wrappers that merely rename an existing library interface.
- Keep framework mechanics in route/controller adapters when a screen should remain renderable and testable from a plain model and actions.

Apply the deletion test: removing a useful abstraction should spread meaningful policy back into several callers. If deleting it only removes forwarding, keep the direct implementation.

**Complete when:** the proposed component and hook interfaces are smaller than the behavior they hide, state ownership is explicit, and no new configuration DSL or pass-through wrapper is required.

## Implement complete interaction states

Keep render pure. Derive display values during render, perform user-caused work in event handlers, and reserve Effects for synchronization with systems outside React. Preserve stable component identity intentionally; use keys when a changed identity should reset a subtree.

Implement every traced state, including cleanup, cancellation ownership, pending-close behavior, stale or conflicting data, focus restoration, and request recovery. Keep server authorization authoritative and keep secrets and server-only dependencies outside client-reachable modules.

**Complete when:** every user-visible path is implemented through its owner, render remains pure, and browser/server boundaries are respected.

## Verify through public behavior

Test through the component, hook, controller, or route interface that callers use. Assert rendered semantics and user-observable transitions rather than implementation details. Run the smallest repository checks covering types, lint, focused tests, accessibility, and build behavior; add browser, hydration, visual, and bundle checks when the change affects those contracts.

Before completion, confirm:

1. Each state has one owner and derived values are not synchronized through Effects.
2. Component APIs use composition without hiding ordinary React behind a local DSL.
3. Effects synchronize external systems, declare dependencies, and clean up completely.
4. Async data, cancellation, cache invalidation, and error reset follow their owning framework.
5. Interactive UI has native semantics where possible and intentional keyboard, focus, label, status, reflow, and localized-content behavior.
6. Tests cover the changed happy path and important pending, empty, failure, and recovery paths.
7. Production checks pass, or each skipped or failing gate is reported with its missing prerequisite and remaining risk.

**Complete when:** every applicable reference has been checked, focused verification passes or has a concrete reported blocker, and the change remains within requested scope.
