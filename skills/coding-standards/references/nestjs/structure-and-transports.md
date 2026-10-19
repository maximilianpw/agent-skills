# Structure, metadata, and transports

## Files and names

Match the repository. For greenfield Nest code, follow CLI conventions:

- `cats.module.ts` and `CatsModule`
- `cats.controller.ts` and `CatsController`
- `cats.service.ts` and `CatsService`
- `create-cat.dto.ts` and `CreateCatDto`
- `http-exception.filter.ts` and `HttpExceptionFilter`
- colocated `*.spec.ts`, with `*.e2e-spec.ts` under `test/`

Organize by feature once a capability has its own controller, providers, DTOs, or tests. Nest's standard feature layout keeps those files together. Do not impose a domain-layer folder scheme on a repository that does not use one.

Avoid `index.ts` barrels for module, controller, and provider classes that participate in the same module graph. Same-folder barrels can create runtime circular imports even when TypeScript type checking succeeds. Import the concrete file.

## Decorators and metadata

Decorators attach runtime metadata used by Nest. Keep decorated classes and DTOs available as value imports. Use `@SetMetadata()` when interoperating with an established metadata key.

Decorator composition is useful when one application concept always applies the same metadata and enhancers. Keep the combined decorator small enough that a reader can find what it installs.

## GraphQL

GraphQL reuses modules, providers, pipes, guards, interceptors, and filters, but it has a different execution context.

- Import mapped types from `@nestjs/graphql` so GraphQL metadata is preserved.
- Convert `ExecutionContext` with `GqlExecutionContext` before reading GraphQL context or arguments.
- Use the GraphQL `CONTEXT` token rather than HTTP `REQUEST` for request-scoped context injection.
- Return GraphQL-appropriate errors and confirm how the selected driver formats them.
- HTTP bootstrap globals and Express response assumptions may not apply to subscriptions or other GraphQL paths.

Keep resolver methods transport-focused and delegate application work to providers, as with controllers.

## WebSockets

Gateways are singleton infrastructure and cannot use request scope. Use WebSocket-specific exception types and adapters. Confirm whether global pipes, guards, interceptors, and filters apply to the gateway; hybrid applications do not inherit every HTTP global automatically.

Connection state, authentication during handshake, and per-message authorization have different lifetimes. Do not carry an HTTP request assumption into a long-lived socket.

## Microservices

Nest microservices reuse enhancer concepts but use transport-specific request context, acknowledgements, serialization, retry, and `RpcException` behavior. A global HTTP `ValidationPipe` or filter does not automatically configure a connected microservice in a hybrid application.

For each message handler, define:

- delivery and acknowledgement semantics;
- duplicate and redelivery behavior;
- timeout and retry ownership;
- transport error mapping;
- correlation and tracing propagation.

Apply enhancers through the microservice or hybrid application's documented registration path.

## CQRS

`@nestjs/cqrs` is an optional recipe, not Nest's default architecture. Use it when separate command, query, event, or saga handlers solve demonstrated workflow or team-boundary complexity. Keep a straightforward provider method when buses and handler discovery would only rename a direct call.

Events published through an in-process CQRS bus are not automatically durable. Persistence, outbox, retry, and cross-process delivery remain separate design decisions.

## OpenAPI and versioning

When `@nestjs/swagger` owns API metadata, import mapped types from that package. Generate the document from the same application configuration that owns routes and global prefixes.

Nest supports URI, header, media-type, and custom versioning. URI versioning is the default mode when enabled. Use neutral routes deliberately. Version middleware behavior and wildcard syntax depend on the HTTP adapter and Nest version.

Treat the published schema and version behavior as caller-facing contracts. Add end-to-end coverage when a change affects route resolution, validation, or generated metadata.

## Sources

- NestJS, [Modules](https://docs.nestjs.com/modules)
- NestJS, [CLI usage](https://docs.nestjs.com/cli/usages)
- NestJS, [Circular dependency](https://docs.nestjs.com/fundamentals/circular-dependency)
- NestJS, [Custom decorators](https://docs.nestjs.com/custom-decorators)
- NestJS, [Execution context](https://docs.nestjs.com/fundamentals/execution-context)
- NestJS, [GraphQL](https://docs.nestjs.com/graphql/quick-start)
- NestJS, [WebSockets](https://docs.nestjs.com/websockets/gateways)
- NestJS, [Microservices](https://docs.nestjs.com/microservices/basics)
- NestJS, [CQRS](https://docs.nestjs.com/recipes/cqrs)
- NestJS, [OpenAPI](https://docs.nestjs.com/openapi/introduction)
- NestJS, [Versioning](https://docs.nestjs.com/techniques/versioning)
