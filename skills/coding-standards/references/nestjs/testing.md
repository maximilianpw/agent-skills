# Testing Nest applications

## Choose the smallest truthful level

Nest supports three useful levels:

- Construct a controller or provider directly when a plain constructor and explicit test doubles cover the contract.
- Use `Test.createTestingModule(...).compile()` when provider tokens, module exports, factories, scopes, or enhancers are part of the behavior.
- Create and initialize a Nest application when routing, validation, serialization, guards, filters, middleware, or adapter behavior must be proven.

Test through the interface callers use. A controller unit test cannot prove global `ValidationPipe` options. A provider test does not need an HTTP server.

Keep unit specs next to their class as `*.spec.ts` when the repository follows Nest's scaffold. Keep end-to-end tests under `test/` as `*.e2e-spec.ts`. Nest is test-runner agnostic. Nest 11 scaffolds Jest by default; follow the installed runner rather than future Nest 12 plans.

## TestingModule

Register realistic module ownership where that ownership matters. Retrieve singleton providers with `moduleRef.get(Token)`. Retrieve request- or transient-scoped providers with `moduleRef.resolve(Token)`.

Override a dependency before `compile()`:

```typescript
const moduleRef = await Test.createTestingModule({
  imports: [CatsModule],
})
  .overrideProvider(CatsStore)
  .useValue(catsStore)
  .compile();
```

The override API also supports guards, interceptors, filters, and pipes. `useMocker()` is a convenience for large graphs, not a reason to stop checking caller-visible behavior.

## Global enhancer override trap

An `APP_GUARD` provider registered with `useClass` is a multi-provider under the framework token. Overriding the guard class token will not replace that hidden instance.

Register an alias instead:

```typescript
providers: [
  JwtAuthGuard,
  { provide: APP_GUARD, useExisting: JwtAuthGuard },
]
```

Tests can then call `.overrideProvider(JwtAuthGuard)`. Use the same pattern for DI-dependent global pipes, interceptors, and filters that tests need to replace.

## End-to-end lifecycle

For Express-backed tests:

1. Build the `TestingModule`.
2. Call `moduleRef.createNestApplication()`.
3. Apply the same bootstrap configuration that production behavior depends on.
4. `await app.init()`.
5. Exercise `app.getHttpServer()` with the repository's HTTP test client.
6. `await app.close()` in `afterAll` or `finally`.

Avoid duplicating bootstrap logic between `main.ts` and tests. Extract an idempotent function that configures an application when global pipes, filters, versioning, or middleware must match.

Fastify requires its adapter and readiness behavior. Await `app.getHttpAdapter().getInstance().ready()` when the test path needs it, and consider Fastify's `app.inject()` for adapter-native HTTP testing.

Every test that creates a Nest application must close it. Otherwise open listeners, pools, workers, and timers leak into later tests.

## Shutdown hooks in tests

`enableShutdownHooks()` installs process listeners. Tests that boot many applications in one process can hit listener-count warnings. Enable it in tests only when shutdown-signal behavior is under test. `app.close()` still invokes the normal close lifecycle for the test application.

## Scoped providers

`resolve()` creates a new scoped subtree unless calls share a `ContextId`. When several request-scoped resolutions must represent one request, create or obtain one context ID and pass it to each resolution. Do not compare instances from separate `resolve()` calls and assume they share request state.

## Coverage expectations

For changed public behavior, cover the happy path plus the important validation, authorization, missing-data, provider-failure, and recovery paths. Assert status, response contract, and externally visible effects. Use real or faithful infrastructure at the test level where transaction, serialization, module registration, or adapter behavior is the subject.

## Sources

- NestJS, [Testing](https://docs.nestjs.com/fundamentals/testing)
- NestJS, [Injection scopes](https://docs.nestjs.com/fundamentals/injection-scopes)
- NestJS, [Lifecycle events](https://docs.nestjs.com/fundamentals/lifecycle-events)
- NestJS, [Performance with Fastify](https://docs.nestjs.com/techniques/performance)
