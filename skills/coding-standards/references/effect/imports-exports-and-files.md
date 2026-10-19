# Effect imports and exports

Shared [file layout](../file-layout.md) and [TypeScript](../typescript.md) rules own placement, naming, public entrypoints, type-only edges, and dynamic loading.

Import stable Effect modules as named namespaces from the package root, combined in one declaration. Import unstable modules from their narrow public entrypoint. Use the same form in source and tests:

```ts
import { Config, Effect, Layer } from "effect";
import { HttpServerResponse } from "effect/unstable/http";
```

Leaf namespace imports such as `import * as Effect from "effect/Effect"` split one module across two spellings; use the root form.

For application modules, use named imports for self-describing operations, classes, and focused helpers. A domain module with an established canonical API may use a namespace when it preserves useful ownership at call sites.

Complete when every changed Effect import uses the root or its narrow unstable public entrypoint, application imports preserve searchable ownership, and shared file/export rules are satisfied.
