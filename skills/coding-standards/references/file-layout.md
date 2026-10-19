# File layout and naming

## Placement

Apply this precedence: framework conventions, then runtime boundaries (server, client, edge), then package ownership. Within those constraints, colocate a feature's private code, tests, styles, stories, and helpers.

- Place a file in the narrowest folder containing all its users. A component, hook, or helper used by one route or feature stays there; move it upward only when several places share it.
- Entry and aggregator files do not count as users: app shells, routers or route trees, registries, and server entries import broadly by design.
- Code used across packages or layers is organized by topic, not by its first caller.
- `common/`, `shared/`, and `components/` hold code actually used in several places, not anticipated reuse.
- In file-based routers, treat the route directory as a manifest. Put non-route files under the router's supported ignore prefix (such as `-components/` or `_private/`), or one level up in the feature folder; confirm which convention the installed router supports.
- When a folder grows past about fifteen files, group by feature or concern to keep it scannable. This is a review signal, not permission to reorganize unrelated files.
- Merge a small file into its only importer when it reads naturally as a section there. Keep a file separate when maintainers would search for its own name. Prefer a specific subject over `utils` or `helpers`, and one clear feature entry over an `index.ts` re-export barrel. Intentional package public entrypoints remain valid.

## Names

- Name files after their main export or behavior (`secret-masking.ts`, `UserMenu.tsx`), not their first caller. Preserve repository casing and framework names such as `route.tsx`, `page.tsx`, and `layout.tsx`.
- Qualify duplicate names when they actually confuse readers. When core and adapter share a concept, the core keeps the noun (`tenant-fan-out.ts`); the adapter takes a verb or qualifier (`run-all-tenants.ts`, `use-tenant-fan-out.ts`).
- Drop prefixes already supplied by a folder (`auth/login.test.ts`) unless the full name materially improves search.
- Name tests after behavior (`checkout-form.test.tsx`), not chronology (`review-fixes.test.tsx`).

## Order inside a file

Apply to files written or substantially changed. Earlier rules win when they conflict:

1. Framework directives (`"use client"`, `"use server"`), then imports.
2. A component's props type directly above that component, even when exported.
3. A schema directly before its inferred type (`type X = z.infer<typeof xSchema>` or the decoder library's equivalent).
4. Other exported types and interfaces after imports, before implementation.
5. Helper types beside the function using them.

## Test support

Colocate tests, fixtures, helpers, stories, and type tests when only the covered code uses them. End-to-end tests live in their own folder.

Code shared by several tests goes in a support folder for that package, not a global cross-package folder. Group it by concern: fakes (mock servers, MSW handlers, in-memory services), harness (render helpers, test servers, page objects), and fixtures (data and builders).
