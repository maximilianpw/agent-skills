# Effect configuration

Apply [configuration ownership](../configuration-and-resources.md). Use the pinned Config/ConfigProvider documentation for provider construction and path-mapping APIs; install providers at the composition root rather than reading ambient environment variables inside services.

## Missing is not malformed

In the checked Effect 4.1.4 baseline, constructors are `Config.String`, `Config.Boolean`, and `Config.Redacted` (capitalized). Verify exports before adapting older prerelease examples.

```ts
import { Config, Effect } from "effect"

export const configuration = Effect.gen(function* () {
  const apiKey = yield* Config.Redacted("API_KEY")
  const optionalModel = yield* Config.option(Config.String("MODEL"))
  const enabled = yield* Config.Boolean("FEATURE_ENABLED").pipe(
    Config.withDefault(false),
  )
  return { apiKey, optionalModel, enabled }
})
```

`Config.withDefault` and `Config.option` handle missing data; malformed supplied values still fail. `Config.orElse` handles any config parse failure, so it can conceal a typo or invalid secret as well as absence. Use it only when every such failure genuinely selects the fallback.

## Providers

Replacing a provider and adding a fallback have different precedence. With `ConfigProvider.layerAdd`, `{ asPrimary: true }` makes the added provider override the current one. Test both a conflicting key and a missing key when precedence changes.

A configuration test must provide its own data source; the developer's shell must not silently supply missing test values. Test absence, malformed values, redaction, and precedence through the actual recipes. Supplying an already-decoded service tests its consumers, not Config decoding.

## Layer config helpers

A `layerConfig(options: Config.Wrap<Options>)` helper earns its place only when callers need to compose Config recipes. Keep the concrete `layer(options)` form for callers that already have decoded options, and expose only forms with real consumers. Do not manufacture an environment round trip to reuse a constructor.
