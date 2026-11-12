# Effect imports and exports

Shared [file layout](../file-layout.md) and [TypeScript](../typescript.md) rules own placement, naming, public entrypoints, type-only edges, and dynamic loading.

Our convention is named namespace imports from the package root for stable modules, and the narrow public entrypoint for other modules. Verify exports using the [pinned-source rule](runtime/effect.md#source-rule). For the checked 4.1.4 baseline:

```ts
import { Config, Effect, Layer } from "effect";
import { HttpServerResponse } from "effect/http";
```

Leaf namespace imports such as `import * as Effect from "effect/Effect"` split one module across two spellings; use the root form.

For application modules, use named imports for self-describing operations, classes, and focused helpers. A domain module with an established canonical API may use a namespace when it preserves useful ownership at call sites.

An API can remain unstable without `unstable` appearing in its import path. Current v4 removed that segment; preserve older spellings only when the installed package actually exports them.
