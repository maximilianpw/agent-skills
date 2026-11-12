# Schema and data modeling

Apply [parsing provenance](../parsing-and-schemas.md#provenance) before choosing an API. The pinned Schema documentation owns constructor and combinator syntax; this reference owns the selection rules and local modeling defaults.

## Records

Our local default for new records is `Schema.Struct` plus a same-name derived interface (`interface User extends Schema.Schema.Type<typeof User> {}`). Use structural tagged structs/unions for variants as well; Schema tagged errors are the class exception. Preserve compatible existing public APIs.

Reuse fields when contracts share meaning, not merely shape. Key-renaming combinators fit naming-only differences; joins, normalization, and domain translation remain explicit. Add schema identifiers only when diagnostics, code generation, or API tooling consumes them. To establish a new constraint, use `schema.makeEffect` when failure belongs in the Effect channel; `schema.make` throws on failure.

## Decoder selection and public parsers

- `decodeUnknownEffect` accepts genuinely unknown boundary input. `decodeEffect` accepts the codec's exact encoded type while still validating its contents. A known `string` does not satisfy an encoded literal union; casting it does not establish that evidence.
- JSON codecs fit actual JSON boundaries. Encoding an established domain value merely to decode it again is an unnecessary round trip, not provenance preservation.
- Effect decoders retain typed failures in workflows. Pure Result decoders are valid for explicit pure success/failure; this is different from redundantly wrapping a Result inside an Effect success channel. Option decoders deliberately discard failure details. Sync decoders fit only where throwing is the intended boundary behavior.
- Instantiate codecs privately at their owner. Directly exporting a decoder factory also exports library parse options; use a narrow wrapper unless a low-level codec API is intentionally public.

For a known encoded string, retain its type without exposing library options:

```ts
import { Effect, Schema } from "effect"

const DeploymentStage = Schema.String.check(
  Schema.isPattern(/^(local|preview|production)$/),
).pipe(Schema.brand("DeploymentStage"))

type DeploymentStage = typeof DeploymentStage.Type
const decodeDeploymentStage = Schema.decodeEffect(DeploymentStage)

export const parseDeploymentStage = (
  input: string,
): Effect.Effect<DeploymentStage, Schema.SchemaError> => decodeDeploymentStage(input)
```

Preserve existing public compatibility when narrowing an established parser. Translated fields and `satisfies` do not establish cross-field or transition invariants; retain the owning runtime refinement after translation or computation.

## Optionality and defaults

`Schema.optionalKey` permits an absent key; `Schema.optional` also admits explicit `undefined`. Nullability is a separate encoded-contract choice. Model exactly what the protocol permits, then apply the local [Option policy](../domain-types-and-state.md#operation-inputs-and-optionality) on the decoded application side. Defaults produce required normalized values rather than leaving downstream code to rediscover them.

Use the pinned Schema's Option transformations rather than copying an optional wire shape into the domain. A plain `optionalKey` field alone does not decode into `Option`.

## Brands and variants

[Domain modeling](../domain-types-and-state.md) decides where brands and variants earn their place. Apply scalar constraints before branding. Use `Data.TaggedEnum` for internal control flow and Schema variants when decoding, persistence, encoding, or generated contracts are required. External discriminators and omitted tags are wire-format decisions, not reasons to impose `_tag` on a foreign protocol.

## Errors

Use the tagged-error constructor exported by the pinned release; the checked baseline uses `Schema.TaggedError`. Follow [error ownership and translation](../errors.md), keeping public error schemas distinct from richer internal diagnostics.

`Schema.Defect()` describes a defect-like payload; it does not redact it. Keep raw causes internal under the [sensitive-data policy](../sensitive-data-and-observability.md).

## Verification

Exercise parser input types and public arity as well as runtime failures. Test application-owned transformations, refinements, compatibility, and public error behavior—not the schema library's basic struct or union mechanics. Invalid fixtures must challenge the invariant independently rather than deriving their validity from the schema being tested.
