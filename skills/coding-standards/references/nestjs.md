# NestJS

Inspect installed Nest/Node versions, Express or Fastify, transport types, bootstrap globals, provider scopes, and shutdown behavior. Examples target Nest 11 on Node 20 or later; check installed APIs rather than relying on the docs site version label.

Trace the operation through middleware, guards, interceptors, pipes, controller, providers, outbound interceptors, exception filters, and the response. Map each provider to its declaring/exporting module.

## Load by concern

- [Modules and DI](nestjs/modules-and-di.md): module exports, provider tokens, scopes, circular dependencies, dynamic modules, or `ModuleRef`.
- [Controllers and lifecycle](nestjs/controllers-and-lifecycle.md): routing, middleware, guards, pipes, interceptors, filters, decorators, context, and cancellation.
- [Validation and serialization](nestjs/validation-and-serialization.md): DTOs, validation pipes, transformations, mapped types, and responses.
- [Security](nestjs/security.md): authentication, authorization, secrets, CORS, CSRF, Helmet, or throttling.
- [Persistence and async work](nestjs/persistence-and-async-work.md): ORM modules, transactions, queues, events, and scheduled work.
- [Testing](nestjs/testing.md): caller-visible Nest behavior or contracts.
- [Configuration and operations](nestjs/configuration-observability-and-operations.md): startup, shutdown, logging, health checks, containers, or adapter changes.
- [Structure and transports](nestjs/structure-and-transports.md): files, metadata, GraphQL, WebSockets, microservices, CQRS, OpenAPI, or versioning.

## Nest-specific decisions

- Controllers bind transport input and delegate application work to providers. DTO classes and pipes own input validation; guards own route-aware access decisions; interceptors wrap execution; filters translate uncaught exceptions.
- Use constructor injection and explicit module imports/exports. Shared providers are imported, not re-provided. Keep singleton scope unless instance identity requires otherwise.
- Register DI-dependent global enhancers through `APP_PIPE`, `APP_GUARD`, `APP_INTERCEPTOR`, or `APP_FILTER`. Preserve standard response handling unless direct adapter access is needed.
- Keep DTOs and DI tokens available at runtime where decorator metadata requires them. A passing typecheck does not prove Nest can construct the module graph.
- Test through constructors, `TestingModule`, or real HTTP as appropriate; close every booted test application.
