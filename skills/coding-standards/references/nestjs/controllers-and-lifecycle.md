# Controllers and request lifecycle

## Controller boundary

Controllers own transport details: route, method, status, headers, DTO binding, and route-level enhancers. Inject providers and delegate storage, orchestration, and domain decisions to them.

Prefer standard response mode. Return a value and let Nest serialize it. Nest returns 200 by default and 201 for `@Post()` handlers. Use `@HttpCode()` and `@Header()` to depart from the defaults. Injecting `@Res()` or `@Next()` switches that handler to library-specific mode, where the handler owns completion and interceptors or response decorators may stop working. Use `@Res({ passthrough: true })` when direct header or cookie access is required but Nest should still produce the body.

Keep Express and Fastify request or response types inside the controller or an HTTP adapter. A handler may return a `Promise` or `Observable`; Nest subscribes to an Observable and uses its last emission.

## Pick the native lifecycle slot

| Need | Owner | Mechanism |
| --- | --- | --- |
| Raw request mutation, Helmet, CORS, ALS setup, body parsing | Middleware | Runs first and has no handler metadata |
| Route-aware authentication or authorization | Guard | Has `ExecutionContext` and `Reflector` |
| Argument validation or conversion | Pipe | Runs before the handler and may replace the value |
| Timing, mapping, cache, timeout, execution wrapping | Interceptor | Wraps `next.handle()` as an RxJS stream |
| Uncaught exception translation | Exception filter | Receives only exceptions that escape inner code |

Keep domain decisions in providers. Enhancers should apply transport or cross-cutting policy. Nest's pipes documentation includes entity-loading pipes such as `UserByIdPipe`; follow the repository's boundary rather than treating lookup pipes as universally required or forbidden.

## HTTP order

For a successful HTTP request, Nest runs:

1. global middleware;
2. module middleware, root first and then import order;
3. global, controller, then route guards;
4. global, controller, then route interceptors on the inbound path;
5. global, controller, route, then parameter pipes, with parameters processed last to first;
6. controller and provider code;
7. route, controller, then global interceptors on the outbound path;
8. the response.

Interceptors unwind first-in, last-out because they wrap Observables. On an uncaught exception, Nest skips the remaining normal path and checks route, controller, then global filters. Unlike other enhancers, filters resolve from the most specific scope outward.

Nest 11 runs middleware from global modules before other module middleware. Express 5 path wildcards must be named, such as `{*splat}`. Fastify middleware wildcard syntax differs.

## Exceptions and filters

Throw built-in `HttpException` subclasses such as `BadRequestException`, `UnauthorizedException`, `ForbiddenException`, and `NotFoundException`. Extend `HttpException` when the application needs a distinct HTTP error. Pass `{ cause }` to preserve a diagnostic cause; Nest does not expose that cause in the response.

The default filter converts unrecognized exceptions to a generic 500 response. Built-in HTTP, WS, and RPC exceptions derive from `IntrinsicException` and the default filter does not log them.

Filters see only uncaught exceptions. Catch an exception only to recover, add information and rethrow, or translate it deliberately. A matching inner filter consumes the exception, so broader filters do not run afterward.

Use `HttpAdapterHost` in a platform-neutral catch-all filter. Express `response.json()` and Fastify `response.send()` are not interchangeable. Bind injectable global filters with `APP_FILTER` and let Nest construct enhancer classes so it can inject and reuse them.

## Metadata and request context

Create typed metadata with `Reflector.createDecorator<T>()` when practical. Read handler and class metadata with:

- `getAllAndOverride` when method metadata should override class metadata;
- `getAllAndMerge` when both should combine;
- `get` for one known target.

Nest 11 returns `T | undefined` from `getAllAndOverride` and changed object merging behavior in `getAllAndMerge`. Handle absence explicitly.

Use custom parameter decorators to expose a narrow request value such as the current user. Keep authorization policy in a guard or provider rather than burying it in the decorator factory.

For request context needed by many singleton providers, initialize Node's `AsyncLocalStorage` with `run()` in middleware. Middleware is the first Nest lifecycle slot. Nest has no built-in ALS service; `nestjs-cls` is third-party. Keep the store narrow so it does not become hidden dependency injection.

## Timeouts and cancellation

Nest's documented timeout pattern is an interceptor using RxJS `timeout()` and translating `TimeoutError` to `RequestTimeoutException`. This cancels the Observable subscription. It does not automatically cancel a database query or downstream client call.

Nest does not provide a documented handler-level `AbortSignal` for HTTP client disconnects. Propagate a signal only when the active adapter and downstream library supply a real owner for it.

## Other transports

Pipes, guards, interceptors, and filters also apply to GraphQL, WebSockets, and microservices, but request extraction and exception classes differ. `useGlobalPipes()` and similar bootstrap registrations do not automatically apply to every gateway or hybrid transport. Verify the active transport rather than assuming HTTP behavior.

## Sources

- NestJS, [Controllers](https://docs.nestjs.com/controllers)
- NestJS, [Request lifecycle](https://docs.nestjs.com/faq/request-lifecycle)
- NestJS, [Middleware](https://docs.nestjs.com/middleware)
- NestJS, [Guards](https://docs.nestjs.com/guards)
- NestJS, [Pipes](https://docs.nestjs.com/pipes)
- NestJS, [Interceptors](https://docs.nestjs.com/interceptors)
- NestJS, [Exception filters](https://docs.nestjs.com/exception-filters)
- NestJS, [Execution context](https://docs.nestjs.com/fundamentals/execution-context)
- NestJS, [Async local storage](https://docs.nestjs.com/recipes/async-local-storage)
