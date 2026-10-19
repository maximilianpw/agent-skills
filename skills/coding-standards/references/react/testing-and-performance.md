# Testing and performance

## Test the public UI interface

Test through the same component, hook, controller, route, or browser entrypoint a caller uses.

- Render components in the providers and routing context required by production.
- Interact through roles, names, labels, text, and pointer/keyboard behavior.
- Assert visible content, focus, URL state, cache consequences, announcements, and durable outcomes.
- Prefer Testing Library over renderer internals. Import `act` from React only when the test tool does not already wrap the interaction.
- Keep test data valid under production types and schemas. Deliberately invalid values should cross the same untrusted boundary as production input.
- Avoid mocking React Hooks or testing state variables directly. Replace owned dependencies through explicit interfaces, providers, request interception, or faithful fakes.

## Required behavior shapes

For changed UI, assess and cover the applicable states:

- initial render and hydrated render;
- pending without flicker or destructive layout replacement;
- empty successful result;
- stale data during refresh;
- missing resource;
- forbidden or read-only authority;
- recoverable and unrecoverable errors;
- retry and Query/Router error reset;
- successful mutation and invalidation;
- conflict, stale record, duplicate submission, and cancellation;
- unmount and Effect cleanup;
- back/forward navigation and shareable URL state;
- keyboard operation, focus placement/restoration, and announcements;
- narrow viewport and translated or unusually long content.

A bug fix should demonstrate failure on the original behavior when practical. A regression test should fail for the behavior it claims to protect, not only because an implementation detail changed.

## Test layers

Use the smallest layer that proves the contract, then add higher layers for integration risks:

1. Pure tests for reducers, validators, search projections, and workflow decisions.
2. Component tests for composition, semantics, state transitions, forms, and focus.
3. Controller/route tests for URL state, loaders, cache keys, capability gates, hydration, invalidation, and recovery.
4. Browser journeys for real routing, overlays, CSS, keyboard, accessibility scans, responsive behavior, assets, and server/client integration.
5. Production startup and deployment-path checks for SSR, headers, chunk loading, and runtime environment behavior.

Do not make E2E the only evidence for pure state or validation logic. Do not assume unit/component tests verify CSS, hydration, or production chunks.

## Accessibility and visual evidence

Automated accessibility scans catch only part of WCAG. Scan important initial and interacted states, then maintain a focused manual matrix for keyboard, screen reader, zoom/reflow, forced colors, reduced motion, and touch targets.

Use visual regression for stable, high-risk surfaces:

- design-system foundations and semantic states;
- open dialogs, menus, sheets, selects, and tooltips;
- shared layout and navigation patterns;
- narrow reflow;
- dark/light themes and one long localized-content case.

Keep screenshot environments deterministic. Screenshots verify appearance; semantic and interaction assertions remain authoritative for behavior.

## Rendering performance

Correct ownership and purity come before memoization.

- Derive inexpensive values during render.
- Move state down when unrelated parent updates are the real rerender cause.
- Keep context scopes and values proportionate to their consumers.
- Use stable semantic query keys and avoid request waterfalls.
- Virtualize only collections whose measured rendering cost requires it.
- Add `memo`, `useMemo`, or `useCallback` after identifying a material repeated render/calculation or when a documented library interface requires stable identity.
- Re-measure after optimization and remove optimizations that do not improve the target path.

## Loading and bundles

Measure both cold routes and later interactions.

- Split genuinely deferred render code, not critical route matching or data-start code.
- Inspect the production module graph; source-level dynamic imports do not prove an entry is small when an eager runtime imports the same dependency.
- Budget bytes and requests. Request-count-only gates allow a fixed number of chunks to grow without limit.
- Include CSS, fonts, images, locale catalogs, hydration data, and third-party scripts in page-load analysis.
- Verify loading, error, and recovery behavior for failed dynamic chunks across deployments.

## Core Web Vitals

Use field data when available and assess the 75th percentile separately for mobile and desktop. Current “good” thresholds are:

- LCP at or below 2.5 seconds;
- INP at or below 200 milliseconds;
- CLS at or below 0.1.

Use lab tests for reproducible regression and diagnostics; they do not replace field evidence. Reserve dimensions for images and embeds, avoid late content injection that shifts the page, keep event handlers short, and avoid large client bundles or waterfalls that delay rendering and interaction.

## Verification discipline

Run the repository's smallest relevant commands while developing and its declared review/release gates before claiming those states. Vite build success does not include TypeScript type checking. A dev server does not prove production SSR, asset, or startup behavior.

Report every skipped check with:

- the exact command;
- its missing service, browser, credential, or toolchain prerequisite;
- the remaining CI or operator gate that must provide the evidence.

## Sources

- React, [`act`](https://react.dev/reference/react/act)
- React, [React DOM Test Utils warning](https://react.dev/warnings/react-dom-test-utils)
- React, [React 19 Upgrade Guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide)
- Testing Library, [Guiding Principles](https://testing-library.com/docs/guiding-principles/)
- Playwright, [Accessibility Testing](https://playwright.dev/docs/accessibility-testing)
- Playwright, [Visual Comparisons](https://playwright.dev/docs/test-snapshots)
- web.dev, [Web Vitals](https://web.dev/articles/vitals)
- web.dev, [Optimize Interaction to Next Paint](https://web.dev/articles/optimize-inp)
- web.dev, [Optimize Largest Contentful Paint](https://web.dev/articles/optimize-lcp)
- web.dev, [Cumulative Layout Shift](https://web.dev/articles/cls)
- Vite, [Features — TypeScript](https://vite.dev/guide/features.html#typescript)
- Vite, [Building for Production](https://vite.dev/guide/build.html)
