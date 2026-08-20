---
name: nestjs-standards
description: Production NestJS standards for modules, dependency injection, controllers, DTO validation, request lifecycle, security, persistence, testing, and operations. Use when designing, implementing, refactoring, or reviewing non-trivial NestJS code, including Express and Fastify applications.
license: MIT
---

# NestJS standards

Build Nest applications around an explicit module graph, constructor-injected providers, and the lifecycle slot that owns each HTTP concern. Fit the repository before improving it: task requirements and local rules govern, compatible existing patterns follow, and these standards supply defaults where the codebase is silent.

For trivial or mechanical edits, match the surrounding code and stop. Do not turn focused work into an architecture, adapter, ORM, or transport migration.

## Establish the local model

Read the nearest repository instructions, package manifest, Nest CLI and TypeScript configuration, bootstrap file, root module, affected feature modules, and nearby tests. These defaults target Nest 11 on Node 20 or later. Inspect installed packages and the migration guide; the docs site chrome may still show "Version 10" around v11 content.

Identify:

- Nest and Node versions;
- Express or Fastify, plus HTTP, GraphQL, WebSocket, or microservice transports;
- global middleware and `APP_*` enhancers;
- validation and serialization options;
- configuration, authentication, persistence, logging, health, and test libraries;
- provider scopes and shutdown behavior.

Load `typescript-standards` when types, failures, async boundaries, external data, persistence contracts, or TypeScript tests change. Nest examples sometimes expose ORM or transport types directly. Follow a stronger compatible repository boundary when one exists, but do not present that choice as a Nest requirement.

**Complete when:** installed versions, adapter, transports, module ownership, global lifecycle behavior, and verification commands affecting the change are known.

## Trace the operation

Trace each changed operation from transport input through middleware, guards, interceptors, pipes, controller, providers, persistence or external calls, outbound interceptors, exception filters, and response. Map each provider to the module that declares and exports it. Account for startup, shutdown, and tests when the change touches resources.

Read every matching reference completely before designing:

- [`references/modules-and-di.md`](references/modules-and-di.md) when modules, exports, dynamic or global modules, provider tokens, scopes, circular dependencies, or `ModuleRef` change.
- [`references/controllers-and-lifecycle.md`](references/controllers-and-lifecycle.md) when routing, controllers, middleware, guards, interceptors, pipes, filters, responses, decorators, request context, timeouts, or cancellation change.
- [`references/validation-and-serialization.md`](references/validation-and-serialization.md) when DTOs, `ValidationPipe`, `class-validator`, transformation, mapped types, or response serialization change.
- [`references/security.md`](references/security.md) when authentication, authorization, secrets, Helmet, CORS, CSRF, or throttling change.
- [`references/persistence-and-async-work.md`](references/persistence-and-async-work.md) when ORM modules, repositories, transactions, queues, events, or scheduled work change.
- [`references/testing.md`](references/testing.md) whenever behavior or a public Nest contract changes.
- [`references/configuration-observability-and-operations.md`](references/configuration-observability-and-operations.md) when configuration, logging, tracing, health checks, startup, shutdown, containers, or the HTTP adapter changes.
- [`references/structure-and-transports.md`](references/structure-and-transports.md) when files, barrels, GraphQL, WebSockets, microservices, CQRS, OpenAPI, or API versioning change.

**Complete when:** every changed input, decision, dependency, effect, failure, response, and test maps to one owning module and the correct lifecycle slot.

## Design from module and transport contracts inward

Treat a feature module's exports as its public API. Controllers own transport binding and delegate work to providers. Providers own application work and declare dependencies through constructors. DTO classes and pipes own HTTP input validation. Guards own route-aware access decisions. Interceptors wrap execution. Filters translate uncaught exceptions.

Keep singleton scope unless instance identity must vary. Use explicit imports rather than broad globals. Reuse the repository's persistence style; Nest does not require an ORM abstraction. Add an abstraction only when removing it would spread meaningful policy or provider details into callers.

**Complete when:** module imports and exports are intentional, each dependency has one token and owner, each lifecycle concern is in its native slot, and no request scope, global module, `forwardRef()`, `ModuleRef`, or transport-specific response object lacks a concrete need.

## Implement complete framework behavior

Implement validation, authorization, expected failures, serialization, diagnostics, and cleanup for every traced path. Register DI-dependent global enhancers through `APP_PIPE`, `APP_GUARD`, `APP_INTERCEPTOR`, or `APP_FILTER`. Preserve standard handler return mode unless direct adapter access is required. Keep adapter-specific code at the HTTP boundary.

**Complete when:** Nest can construct the graph without duplicate providers or hidden cycles, incoming data reaches providers in the intended form, uncaught failures reach the owning filter, and resources close through lifecycle hooks.

## Verify through public behavior

Test through the constructor, `TestingModule`, or HTTP interface that callers use. Run the smallest repository checks covering compilation, lint, focused tests, and affected end-to-end behavior.

Before completion, confirm:

1. Shared providers are exported and their modules imported rather than re-provided.
2. DTOs and DI tokens exist at runtime where Nest metadata requires them.
3. Singleton scope remains the default and scoped providers do not bubble accidentally.
4. The selected lifecycle slots and their ordering match the intended behavior.
5. Standard responses, serialization, exceptions, and global enhancers still compose.
6. Security and configuration defaults match the active HTTP adapter and deployment.
7. Every booted Nest application closes in tests, and production resources have shutdown owners.
8. Focused checks pass, or each skipped or failing check is reported with its remaining risk.

**Complete when:** every applicable reference has been checked, public behavior is covered at the right test level, verification passes or has a concrete blocker, and the change stays within scope.
