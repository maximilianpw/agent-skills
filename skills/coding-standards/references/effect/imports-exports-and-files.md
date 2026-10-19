# Effect imports and exports

Shared [file layout](../file-layout.md) and [TypeScript](../typescript.md) rules own placement, naming, public entrypoints, type-only edges, and dynamic loading.

For application modules, use named imports for self-describing operations, classes, and focused helpers. A domain module with an established canonical API may use a namespace when it preserves useful ownership at call sites.

Complete when application imports preserve searchable ownership and shared file/export rules are satisfied.
