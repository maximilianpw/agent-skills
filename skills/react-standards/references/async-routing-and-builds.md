# Async data, routing, SSR, and builds

Apply the framework's documented ownership model. This reference gives TanStack and Vite rules when those tools are present; use the repository's equivalent owners for other frameworks.

## Async ownership

Keep each asynchronous concern with one owner:

- Router coordinates matching, navigation, URL state, route readiness, and route-level recovery.
- A server-state cache owns reusable remote data, freshness, deduplication, refetching, and invalidation.
- A form owner owns input drafts and validation lifecycle.
- A feature controller coordinates domain actions, cache consequences, navigation, focus, and presentation feedback.
- Server endpoints remain the authorization boundary.

Avoid generic hooks that merely rename `useQuery`, `useMutation`, or route hooks. Extract feature-specific query or mutation definitions when they centralize keys, decoding, invalidation, authority refresh, or recovery policy.

## TanStack Router and Query

### Query definitions

Own semantic query keys and `queryOptions` in the feature that understands the data. Use the exact same options in the route loader and observer:

```tsx
const options = productCollectionQueryOptions(feature, search)

// route loader
await queryClient.ensureQueryData(options)

// route controller
const result = useSuspenseQuery(options)
```

- Await critical data before rendering the route.
- Start non-critical data without blocking only when the screen has an intentional streamed or client-pending state.
- Set Router `defaultPreloadStaleTime: 0` when Query owns freshness.
- Use a non-zero Query `staleTime` for SSR-hydrated data when immediate client refetch is not desired.
- Keep route loader return values and Query cache data from becoming competing sources of truth.

### Search and loader dependencies

Validate search before guards and loaders. Treat shareable filters, pagination, selection, and workflow identity as typed URL state.

- `loaderDeps` is deterministic and serializable.
- Include every search value used by the loader and no unrelated presentation values.
- Project route search into one canonical feature query input used by both loader and controller.
- Normalize messy optional URL input when recovery is more useful than an error page.

### Eager route configuration

Keep path parsing, search validation, `beforeLoad`, loader dependencies, loaders, context, and static route data eager. Split render code: component, pending component, error component, and not-found component. Splitting a loader adds a chunk round trip before its data work can start and requires explicit evidence to justify.

### Pending, error, and absence

Classify each route's critical, deferred, stale-refresh, empty, missing, forbidden, and recoverable-error states deliberately.

- Throw `notFound()` from a loader for a missing route resource; use a route-specific `notFoundComponent` when recovery differs.
- Keep empty collections and optional selected panels as successful feature states.
- For suspense Query errors, call `useQueryErrorResetBoundary().reset()` when the route error boundary mounts, then reset/invalidate Router state on retry.
- Keep already-rendered layout chrome mounted when only child content is pending or failed, unless the whole layout truly depends on the operation.

A React Error Boundary or framework `errorComponent` catches errors thrown while rendering its descendant tree. It does not catch failures from event handlers, later asynchronous callbacks, server rendering, or the boundary itself. Handle user-caused async failures in the owning event/mutation flow. Put route loading and rendering failures in the framework's route boundary, and pair suspense Query failures with Query's reset boundary. Suspense owns pending presentation, not error recovery.

### Cancellation

Propagate Query's own `queryFn` signal through the underlying cancellable I/O. Do not substitute a Router loader signal: one obsolete loader consumer does not imply every observer of that shared Query key is obsolete.

Pass Router's signal through Router-owned fetches. Use explicit `queryClient.cancelQueries` only when the application intends to cancel the shared Query operation and accepts its state-reversion semantics. TanStack Query documents that cancellation is not available through its suspense hooks; do not make correctness depend on observer-driven cancellation in that mode.

### Mutations

Use feature-specific `mutationOptions` or controller logic when it owns meaningful cache and authority policy.

- The command owner defines the mutation input and expected failures.
- The feature/cache owner defines invalidation or direct cache updates.
- The authority owner refreshes session/capability state after privilege changes.
- The screen owns localized success feedback, dialog closure, and focus restoration.
- Prevent a destructive or durable command dialog from appearing cancellable while the command continues in the background.

## TanStack Start and SSR

Create a fresh Router and Query client per server request. Keep one browser Query client for the SPA lifetime. Put Query on typed Router context and wrap rendering in its provider; use the official SSR Query integration or a tested manual dehydrate/hydrate seam.

Start code is isomorphic unless protected:

- A loader may run on the server for initial SSR and in the browser on navigation.
- Keep secrets, private environment access, database clients, and trusted headers in server-only modules or server functions.
- Authorize every private server function, server route, or API endpoint independently of `beforeLoad`.
- Treat route guards as navigation UX, not security.
- Render stable server and first-client output. Gate browser-only values behind hydration-aware interfaces with an SSR fallback.
- Keep personalized HTML and data private or no-store; do not publicly cache identity-dependent responses.

Use React Server Components only when the selected framework version supports them as a deliberate architectural foundation. Do not introduce them through an unrelated component refactor.

## Vite

Vite transpiles TypeScript but does not type-check it. Run the repository's separate `tsc --noEmit` or equivalent type gate alongside `vite build`.

### Imports and chunks

- Use static imports for code required to start the route or application.
- Use dynamic imports for genuinely deferred screens, dialogs, editors, or workflows; measure the resulting initial and interaction paths.
- Keep `import.meta.glob` patterns literal. It is Vite-specific and should represent an intentional module registry, not hide ordinary imports.
- Let the framework's route splitting policy lead before overriding Vite/Rolldown chunking.
- Verify production chunks and requests rather than inferring bundle behavior from source imports.
- Handle stale deployed chunks deliberately when the product can keep old HTML or sessions open across releases; Vite emits `vite:preloadError` for failed dynamic preload.

### Environment and assets

- Values exposed through `VITE_*` are public client bundle data, always strings before parsing, and never secrets.
- Use imported asset URLs or Vite's documented public directory behavior so the configured base path is respected.
- Treat dev-server success, production build success, SSR startup, and browser behavior as distinct gates.

## Sources

### TanStack

- Router, [External Data Loading](https://tanstack.com/router/latest/docs/framework/react/guide/external-data-loading)
- Router, [Data Loading](https://tanstack.com/router/latest/docs/framework/react/guide/data-loading)
- Router, [Search Params](https://tanstack.com/router/latest/docs/framework/react/guide/search-params)
- Router, [Code Splitting](https://tanstack.com/router/latest/docs/framework/react/guide/code-splitting)
- Router, [Not Found Errors](https://tanstack.com/router/latest/docs/framework/react/guide/not-found-errors)
- Router, [Authenticated Routes](https://tanstack.com/router/latest/docs/framework/react/guide/authenticated-routes)
- Router, [Query Integration](https://tanstack.com/router/latest/docs/integrations/query)
- Query, [Important Defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)
- Query, [Query Cancellation](https://tanstack.com/query/latest/docs/framework/react/guides/query-cancellation)
- React, [Catching rendering errors with an Error Boundary](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)
- React, [`Suspense`](https://react.dev/reference/react/Suspense)
- Query, [SSR](https://tanstack.com/query/latest/docs/framework/react/guides/ssr)
- Query, [`useQueryErrorResetBoundary`](https://tanstack.com/query/latest/docs/framework/react/reference/useQueryErrorResetBoundary)
- Start, [Execution Model](https://tanstack.com/start/latest/docs/framework/react/guide/execution-model)
- Start, [Server Functions](https://tanstack.com/start/latest/docs/framework/react/guide/server-functions)
- Start, [Authentication Server Primitives](https://tanstack.com/start/latest/docs/framework/react/guide/authentication-server-primitives)

### Vite

- Vite, [Features](https://vite.dev/guide/features.html)
- Vite, [Building for Production](https://vite.dev/guide/build.html)
- Vite, [Env Variables and Modes](https://vite.dev/guide/env-and-mode.html)
- Vite, [Server-Side Rendering](https://vite.dev/guide/ssr.html)
