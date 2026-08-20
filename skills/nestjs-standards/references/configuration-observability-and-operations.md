# Configuration, observability, and operations

## Configuration

Load environment configuration through `ConfigModule.forRoot()` at the root. Use `isGlobal: true` only when configuration is genuinely application-wide. Validate at startup with a Joi schema or a `validate` function. Services should inject typed configuration rather than reading `process.env` throughout the graph.

Runtime environment values override `.env` values. In `@nestjs/config` 4, `ConfigService#get` checks internal custom configuration, validated environment, then `process.env`. Verify installed behavior before relying on precedence. `ignoreEnvVars` is deprecated in favor of `validatePredefined`.

`validationSchema` does not validate values returned by custom configuration factories. Validate those inside the factory or parse them into a typed configuration provider.

After `NestFactory.create()`, bootstrap code can read configuration with `app.get(ConfigService)`. Keep non-entrypoint imports inert. Do not open connections or read process state at module import time.

## Logging

Use `new Logger(ClassName.name)` for contextual application logs. A transient custom logger may call `setContext` per consumer. A singleton custom logger that mutates one shared context will mislabel concurrent consumers.

To replace Nest's own logger through DI, create the application with `bufferLogs: true`, resolve the logger from the application, then call `app.useLogger(logger)`. Implement `LoggerService` for Pino, Winston, or another backend.

Nest 11's `ConsoleLogger` supports `{ json: true }`, which is suitable for container log collectors. Keep one event per record and preserve stable fields for request ID, operation, status, and duration. Redact secrets and personal data at the logger boundary.

Built-in HTTP exceptions are not logged by the default exception filter. Add reporting in an owning filter or extend `BaseExceptionFilter` when those events need recording. Avoid logging the same failure in each service and again in the filter.

## Correlation and tracing

Nest does not ship a first-party request-ID module. Establish correlation IDs in early middleware and carry them through AsyncLocalStorage or explicit parameters. Return the ID in a response header when clients need it for support.

OpenTelemetry support comes from upstream JS contrib, not a Nest package or official Nest module. Load the SDK before `NestFactory.create()` so Nest, HTTP, Express, or Fastify instrumentation can patch modules in time. Check the instrumentation package's Nest version range.

## Health checks

Use `@nestjs/terminus` for readiness and liveness endpoints. `@HealthCheck()` plus `HealthCheckService` composes packaged indicators for supported databases, HTTP dependencies, memory, and disk.

In Terminus 11, implement custom indicators with `HealthIndicatorService`. `HealthIndicator` and `HealthCheckError` are deprecated. Health responses should expose operational state without secrets, raw provider errors, or sensitive topology.

A dependency being reachable does not always mean the application is ready. Keep liveness cheap and independent enough to avoid restart loops; use readiness for dependencies required to serve traffic.

## Shutdown

Graceful shutdown is opt-in for operating-system signals. Call `app.enableShutdownHooks()` in production processes that must react to them.

Use `OnModuleDestroy`, `BeforeApplicationShutdown`, or `OnApplicationShutdown` to stop consumers and close database, cache, and telemetry resources. Nest 11 runs destroy hooks in reverse initialization order. Request-scoped providers do not receive lifecycle hooks. With shutdown hooks enabled, Terminus can report `shutting_down`; `gracefulShutdownTimeoutMs` can leave a bounded readiness-propagation window before shutdown continues.

`app.close()` starts Nest shutdown but does not force the Node process to exit while timers or handles remain. Find and close their owner. Signal behavior is platform-specific; Windows Task Manager does not provide Unix `SIGTERM` semantics.

## Express and Fastify

Express is Nest's default adapter. Stay with the repository's adapter unless migration is in scope.

Fastify has different plugins, request objects, middleware behavior, and tests. It listens on `127.0.0.1` by default. Containers that must accept external traffic should use:

```typescript
await app.listen(port, '0.0.0.0');
```

Express 5 and Fastify 5 also differ in wildcard routes, Helmet, CSRF, multipart handling, and CORS defaults. Read adapter-specific package documentation for every raw request or plugin integration.

## Deployment

Nest 11 requires Node 20 or later. Run built production output with production dependencies and `NODE_ENV=production`. Use the repository's package manager and lockfile. Keep build tooling and source files out of the runtime image when using a multi-stage container.

Expose health endpoints expected by the orchestrator, stop accepting new work during shutdown, and give in-flight requests or workers a bounded drain period. Mau is Nest's official deployment product, not a requirement.

## Sources

- NestJS, [Configuration](https://docs.nestjs.com/techniques/configuration)
- NestJS, [Logger](https://docs.nestjs.com/techniques/logger)
- NestJS, [Exception filters](https://docs.nestjs.com/exception-filters)
- NestJS, [Health checks](https://docs.nestjs.com/recipes/terminus)
- NestJS, [Lifecycle events](https://docs.nestjs.com/fundamentals/lifecycle-events)
- NestJS, [Performance with Fastify](https://docs.nestjs.com/techniques/performance)
- NestJS, [Deployment](https://docs.nestjs.com/deployment)
- NestJS, [Migration guide](https://docs.nestjs.com/migration-guide)
- OpenTelemetry JS contrib, [Nest instrumentation](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-nestjs-core)
