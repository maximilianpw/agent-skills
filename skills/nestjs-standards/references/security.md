# Security

## Authentication and authorization

Authentication establishes identity. Authorization decides whether that identity may run the selected handler.

For JWT bearer APIs, issue and verify tokens through an authentication provider, attach the verified principal to the request, and expose it through a typed parameter decorator or request type. Keep signing keys in validated configuration. Hash passwords with a current password-hashing library. Nest's tutorial constants and plaintext comparison are teaching placeholders, not production patterns.

Middleware or a global guard may authenticate requests and attach identity. Route-aware decisions belong in guards because guards receive `ExecutionContext` and handler metadata.

When most routes are private, register authentication as `APP_GUARD` and mark public routes with typed metadata. Read class and handler metadata with `Reflector.getAllAndOverride`.

Use custom metadata for roles or permissions. Return `false` when a known caller lacks permission and 403 is correct. Throw `UnauthorizedException` when no valid identity exists. Keep authorization checks that depend on loaded business data in the provider that owns that operation; route metadata alone cannot express every policy.

Passport through `@nestjs/passport` is optional. Nest's first-party JWT flow also works without Passport. Follow the repository's selected strategy.

## Secrets and configuration

Read secrets through `ConfigService` or the repository's vault integration. Validate required secrets at startup. Keep raw secrets out of source, logs, exception messages, health responses, and serialized DTOs.

Use separate token lifetimes and keys when the product's threat model distinguishes access, refresh, email verification, or password-reset tokens. This is application security policy, not a Nest default.

## HTTP hardening follows the adapter

Register Helmet before other `app.use()` middleware and routes so its headers apply to every response.

- Express: `app.use(helmet())`.
- Fastify: register `@fastify/helmet` as a plugin and await registration.

GraphQL playground or other embedded tools may need deliberate CSP exceptions. Scope those exceptions rather than disabling CSP application-wide.

Enable CORS with `app.enableCors()` or bootstrap options. Configure origins, credentials, headers, and methods from the deployment contract. Fastify 5 defaults to CORS-safelisted methods, so list `PUT`, `PATCH`, and `DELETE` when clients need them.

CSRF protection is for browser requests authenticated by ambient cookies or sessions. Register the adapter-specific package after its cookie or session storage:

- Express: `csrf-csrf` after session or `cookie-parser`.
- Fastify: `@fastify/csrf-protection` after a storage plugin.

A bearer token in an explicit authorization header has a different threat model. Do not add cookie-oriented CSRF middleware without confirming how the application authenticates.

## Rate limiting

Use `@nestjs/throttler` for Nest-managed limits. Its `ttl` is milliseconds in current releases. Verify the installed package version before copying older examples.

Behind a reverse proxy, configure trusted proxy handling so the tracker receives the real client address. Override `getTracker` when identity comes from another trusted field. In-memory storage applies only to one process; clustered or horizontally scaled deployments need a shared store. Redis stores linked by Nest are community packages and must be assessed as third-party dependencies.

Rate limits are one control, not authorization. Choose keys and limits per operation cost and abuse case.

## Error exposure

Return stable, non-sensitive client errors. Preserve diagnostic causes for logs without serializing stack traces, SQL errors, tokens, or provider responses. Record security-relevant failures once at an owning boundary rather than logging the same exception in every provider and filter.

## Sources

- NestJS, [Authentication](https://docs.nestjs.com/security/authentication)
- NestJS, [Authorization](https://docs.nestjs.com/security/authorization)
- NestJS, [Guards](https://docs.nestjs.com/guards)
- NestJS, [Helmet](https://docs.nestjs.com/security/helmet)
- NestJS, [CORS](https://docs.nestjs.com/security/cors)
- NestJS, [CSRF protection](https://docs.nestjs.com/security/csrf)
- NestJS, [Rate limiting](https://docs.nestjs.com/security/rate-limiting)
- NestJS, [Configuration](https://docs.nestjs.com/techniques/configuration)
