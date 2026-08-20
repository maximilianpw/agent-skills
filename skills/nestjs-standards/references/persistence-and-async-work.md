# Persistence and asynchronous work

## Nest owns integration, not the database architecture

Nest is database-agnostic. Use the ORM, query builder, or client already chosen by the repository. Official Nest integrations usually follow this graph:

1. Register the connection once with `forRoot` or `forRootAsync`.
2. Register feature models or repositories in the owning feature module with `forFeature`.
3. Inject through the integration's token or decorator.
4. Re-export the integration module only when another module needs those same registered providers.

Injecting `Repository<User>` directly into a service is idiomatic Nest. An application-owned repository interface can improve provider isolation, but it is a repository architecture choice, not a Nest requirement. Follow the local boundary.

Keep entities near their feature when the repository follows Nest's feature layout. Do not create a new layered folder scheme during a focused persistence change.

Never enable TypeORM `synchronize: true` in production. Use reviewed migrations.

## Transactions

Put transaction scope around the application operation that requires atomicity. Use the active ORM's transaction API.

For TypeORM, Nest documents both `DataSource.transaction()` and `QueryRunner`. A manually created runner must connect, begin, commit or roll back, and release in `finally`. A narrow factory around runner creation can make transaction behavior testable without replacing the full `DataSource` graph.

Do not make repositories request-scoped merely to carry a transaction or tenant. Request scope bubbles. Prefer the ORM's transaction context, an explicit operation dependency, or a deliberately bounded ALS context according to local architecture.

## Queues

Move work off the request path when it is long-running, CPU-heavy, retryable, scheduled for later, or must survive a process restart. The request-facing operation should define enqueue failure, duplicate delivery, status lookup, and caller-visible completion semantics.

`@nestjs/bullmq` is Nest's actively developed BullMQ integration. `@nestjs/bull` is in maintenance mode. Jobs may run more than once, so handlers must account for idempotency, retry, partial progress, and poison jobs. Queue persistence is not a substitute for a database outbox when publishing must be atomic with a database write.

## Events

`@nestjs/event-emitter` uses in-process `eventemitter2`. Listeners register during `onApplicationBootstrap`. Events emitted before that point can be lost.

Use in-process events for decoupling within one running process when loss on crash is acceptable. They are not a durable integration bus and do not cross replicas.

## Scheduled work

`@nestjs/schedule` runs work in the application process. Cron controllers must remain singleton-scoped. In a multi-replica deployment, every replica may run the same schedule unless the deployment or job implementation elects one owner. Make scheduled operations safe for overlap and retry, or use an external scheduler with explicit delivery semantics.

## Resource ownership

Connections, workers, consumers, and timers need one startup owner and one shutdown owner. Close them through Nest lifecycle hooks. Request-scoped providers do not receive lifecycle hooks, another reason process resources belong to singleton infrastructure providers.

## Sources

- NestJS, [Database](https://docs.nestjs.com/techniques/sql)
- NestJS, [Injection scopes](https://docs.nestjs.com/fundamentals/injection-scopes)
- NestJS, [Interceptors](https://docs.nestjs.com/interceptors)
- NestJS, [Queues](https://docs.nestjs.com/techniques/queues)
- NestJS, [Events](https://docs.nestjs.com/techniques/events)
- NestJS, [Task scheduling](https://docs.nestjs.com/techniques/task-scheduling)
- NestJS, [Lifecycle events](https://docs.nestjs.com/fundamentals/lifecycle-events)
