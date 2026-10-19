# Effect and Alchemy composition

Use this reference when changing an Alchemy Worker, Durable Object, Workflow, binding-backed service, or other two-phase Effectful Constructor.

Also apply [`effect-services.md`](effect-services.md) for service and Layer ownership, [`configuration-and-resources.md`](../configuration-and-resources.md) for lifetimes, and [`modules-services-and-adapters.md`](../modules-services-and-adapters.md) for composition-root boundaries.

## Verify the pinned Alchemy model

Read the pinned Alchemy documentation and source before choosing a composition shape. In particular, verify the Effectful Constructor, init/runtime phases, Layers, bindings, and the relevant runtime class. Use installed source as the API authority; vendored documentation is useful when its revision matches. A class/resource name, physical identity, and serialized-state contract are separate facts to verify.

## Compose through the outer Effect

Alchemy Effectful Constructors have two phases:

- the outer init Effect runs during planning and again at runtime cold start;
- the returned inner Effect or handlers run only in the deployed runtime.

Provide infrastructure-backed application Layers to the outer Effect, then yield their service tags during outer initialization. Close over those stable service values for the returned runtime handlers. Prefer this Layer composition:

```ts
Effect.gen(function* () {
  const dependency = yield* ApplicationDependency;

  return {
    fetch: requestHandler(dependency),
  };
}).pipe(Effect.provide(applicationDependencyLayer));
```

Provide an existing Layer from the composition root rather than exposing or yielding a raw `makeApplicationDependency` construction Effect. The Layer is the implementation choice and preserves dependency wiring, acquisition semantics, memoization, and substitution.

When an inner runtime Layer needs an outer-initialized service, bridge the captured value with `Layer.succeed`:

```ts
const dependency = yield* ApplicationDependency;
const handlersLayer = handlersLayerWithoutDependencies.pipe(
  Layer.provide(Layer.succeed(ApplicationDependency, dependency)),
);
```

This value bridge is distinct from providing the infrastructure-backed Layer to the inner runtime Layer. Providing that Layer only inside the returned runtime Effect may incorrectly defer deploy-time binding registration or require init-only Alchemy services where they are unavailable.

## Durable Object state

Alchemy evaluates a Durable Object's outer Effect during planning with mock state. The outer Effect may resolve bindings, service Layers, and the Durable Object state reference, but it must not acquire or use state-backed runtime resources against the mock storage.

Describe state-backed Layers outside when useful, then acquire them only inside the returned runtime Effect. Database migrations, SQL clients, and storage-backed services complete before handlers become available at runtime.

## Durable Object services over HTTP

Treat each application Durable Object as an independent service: it serves an Effect `HttpApi` through `fetch`, and the rest of the application reaches it only through an application-owned client service. The HTTP contract keeps the service boundary explicit, versioned, and typed even when Cloudflare runs both sides in one runtime; it is a logical boundary, not necessarily a network hop.

- Name the pair for the capability: `AccountServer` is the Alchemy Durable Object class; the `AccountClient` module exposes `Interface` and `Service` per [`effect-services.md`](effect-services.md), and callers yield `AccountClient.Service`.
- Key every instance by its canonical branded domain ID (`AccountId` selects an `AccountServer`), never a display name or caller-chosen label. Client operations accept the domain ID; namespace lookup stays inside the client implementation.
- The client constructor yields its Alchemy Durable Object service directly and closes over the namespace. Bindings, namespaces, stubs, and `Cloudflare.toHttpClient` stay inside the client and server modules.
- Version every route from `/v1`.
- Typed Durable Object RPC is a recorded exception: use it only when the HTTP contract's cost outweighs its value, such as a library-internal coordinator exchanging plain data, and record that decision beside the class.

## Invocation-owned clients

Resolve stable bindings during init while deferring runtime I/O to the invocation that owns it. A Durable Object namespace's canonical key selects the remote instance; it does not let a caller-side stub or generated HTTP client escape its Cloudflare I/O context.

Use the pinned Alchemy execution-memo facility to acquire suspended stub-backed clients in the current invocation. Add keyed caching only when multiple targets require it, with an intentional capacity and request-owned lifetime: an execution-memoized `Cache` keyed by canonical domain ID joins concurrent first lookups and reuses each generated client within that invocation, and its capacity can be unbounded because the invocation bounds its lifetime.

```ts
const accountHttpClients = yield* makeExecutionMemo(
  Cache.make<AccountId, AccountHttpClient>({
    capacity: Number.POSITIVE_INFINITY,
    lookup: (id) =>
      Effect.suspend(() =>
        HttpApiClient.makeWith(AccountHttpApi, {
          baseUrl: "http://account.internal",
          httpClient: Cloudflare.toHttpClient(namespace.getByName(id)),
        }),
      ),
  }),
);
```

Keep the keyed resolver private to the client implementation; service operations call it internally, and it never appears on the service interface. With exactly one target per invocation, memoize the single suspended client without a `Cache`. Suspension alone delays acquisition; an isolate-scoped Layer or cache still has the wrong lifetime. Ready application Layers leave implementation selection at its existing owner rather than exporting client resolvers to callers.

Verify planning without native storage access and repeated invocations without stale client reuse. Local runtime tests do not authorize production deployments, resource adoption, or namespace transfers.

## Completion check

Every changed Alchemy constructor follows the pinned two-phase model; infrastructure-backed application Layers are provided to the outer Effect; stable services are yielded by tag and closed over; no composition root bypasses an existing Layer through a raw construction Effect; inner runtime Layers receive captured services through value Layers when necessary; each application Durable Object serves a versioned `HttpApi` keyed by its canonical domain ID behind an application-owned client, or carries a recorded RPC exception; deploy-time bindings remain discoverable during planning; state-backed resources execute only in the runtime phase; invocation-bound clients remain within their actual I/O context; and identity, storage compatibility, runtime evidence, and production authorization are verified separately.
