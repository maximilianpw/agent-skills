# NestJS best practices research

**Research only.** This file is source material for a future `nestjs-standards` skill. It is not the skill.

**Updated 2026-08-20.** Baseline is NestJS 11, latest published core tag `v11.2.1` on 2026-08-14. Nest 12 is in progress and is not the documented production baseline.

## Executive summary for the future skill author

Nest is an Angular-inspired TypeScript application framework over Express or Fastify. The docs sell architecture more than a domain model. The pieces that actually constrain code are the module graph, constructor injection, and the HTTP request lifecycle.

A v1 skill should enforce Nest mechanics that official docs state as recommended or warned-against, then lean on `typescript-standards` for parse-at-the-edge, owned errors, and keeping ORM or transport types inside adapters. Do not smuggle hexagonal-architecture folklore into Nest rules unless a source says so. Nest's own examples inject `Repository<User>` into services. That is idiomatic Nest, not a violation of Nest. It can still violate this repo's TypeScript boundary rules. Keep those layers distinct.

The strongest official rules, in order of how often an agent will get them wrong:

1. Feature modules encapsulate providers. Export is the public API. Do not re-register the same provider in every consumer.
2. Controllers handle HTTP and delegate work to providers.
3. Singleton scope is the default and the recommended default. Request scope bubbles up the graph and has a documented performance cost.
4. Validate at the pipe boundary with DTO classes, not TypeScript interfaces. Enable `whitelist`. Treat `transform` as opt-in with real consequences.
5. Use the standard return-value response style. `@Res()` disables interceptors and `@HttpCode()` unless `passthrough: true`.
6. Throw `HttpException` subclasses. Filters only see uncaught exceptions. Prefer enhancer *classes* over `new` so Nest can reuse and inject them.
7. Use the right lifecycle slot. Middleware is path-dumb. Guards see `ExecutionContext`. Pipes transform or reject arguments. Interceptors wrap the RxJS stream. Filters map uncaught exceptions.
8. Register global pipes, guards, interceptors, and filters with `APP_*` tokens when they need DI. `app.useGlobal*()` cannot inject.
9. Tests that boot Nest must `app.close()`. Globally registered `APP_GUARD` providers need `useExisting` before `overrideProvider` works.
10. Do not make everything `@Global()`. Do not use barrel files for module and provider classes. Treat `forwardRef()` as a last resort.

GraphQL, WebSockets, microservices, and CQRS share enhancers and should stay optional references. A general HTTP skill should not require them.

v12 will change the default toolchain for new ESM apps, Vitest instead of Jest, oxlint, rspack, and ESM packages. Do not write those as current rules. Flag them as upcoming.

## Scope and source methodology

This research covers Nest HTTP applications written in TypeScript. It does not pick an ORM. Persistence findings stop at the Nest module and provider boundary, then point at TypeORM, Prisma, and Sequelize docs where Nest delegates.

Primary sources, in order:

1. Official docs from `nestjs/docs.nestjs.com` as published at [docs.nestjs.com](https://docs.nestjs.com/), read from the GitHub markdown sources on 2026-08-20.
2. Official GitHub: `nestjs/nest` releases, `ValidationPipe` source, migration notes.
3. Upstream libraries Nest names: `class-validator`, `class-transformer`, Express, Fastify, Helmet, OpenTelemetry JS contrib.
4. Official sample apps under `nestjs/nest/sample`.
5. Maintainer blogs, mostly Trilon and Kamil Mysliwiec. These are secondary. Each blog-derived claim is either traced to official docs or marked as practitioner opinion.

SEO listicles were not used as authority. Community Stack Overflow answers appear only where they restated an official GitHub comment.

When official docs show a pattern and this repo's TypeScript standards would reject it, the finding says so instead of inventing Nest consensus.

## Version baseline

| Fact | Value | Source |
| --- | --- | --- |
| Current documented major | NestJS 11 | [Migration guide](https://docs.nestjs.com/migration-guide), [v11.0.0 release](https://github.com/nestjs/nest/releases/tag/v11.0.0) |
| Latest published core tag on 2026-08-20 | `v11.2.1` (2026-08-14) | [Releases](https://github.com/nestjs/nest/releases/tag/v11.2.1) |
| v11 announcement | 2025-01-22, Kamil Mysliwiec, Trilon | [Announcing NestJS 11](https://trilon.io/blog/announcing-nestjs-11-whats-new) |
| Node requirement in v11 | Node.js 20 or higher. v16 and v18 dropped. | [Migration guide](https://docs.nestjs.com/migration-guide) |
| Default HTTP adapter | Express v5 | Same |
| Optional HTTP adapter | Fastify v5 via `@nestjs/platform-fastify` | Same |
| Docs site chrome | Homepage fetch still showed a "Version 10" selector label while the migration guide and latest release are v11. Treat docs.nestjs.com as the v11 docs, and do not trust the chrome label. | [docs.nestjs.com](https://docs.nestjs.com/) fetched 2026-08-20 |
| Next major | v12 in progress, approximate Q3 2026. ESM packages, CLI prompt for ESM vs CJS, Vitest and oxlint for new ESM apps, webpack deprecated, rspack default for monorepos. Published under `next` as `12.0.0-alpha.*`. | [nest#16391](https://github.com/nestjs/nest/pull/16391), [nest-cli#3280](https://github.com/nestjs/nest-cli/pull/3280) |

Version-sensitive facts are called out in each finding. Fastify vs Express changes Helmet, CSRF, CORS methods, middleware path syntax, listen host, and e2e setup. `class-validator` 0.14+ and Nest's `ValidationPipe` disagree on `forbidUnknownValues`. `@nestjs/config@4`, `@nestjs/cache-manager@3`, and `@nestjs/terminus@11` have their own breaking changes.

# Themed findings

Each finding uses this shape:

- **Rule candidate:** what a future skill should tell an agent to do.
- **Why:** the mechanism, not a slogan.
- **Idiomatic / not:** TypeScript sketches.
- **Sources, confidence, caveats.**

## 1. Modules and composition

### 1.1 Feature modules own a capability

**Rule candidate.** Group a closely related controller, providers, and DTOs in one feature module. Register that module from the root `AppModule` through `imports`. Do not dump every controller into `AppModule` once the app has more than a toy surface.

**Why.** `@Module()` is how Nest builds the application graph. Providers are encapsulated unless exported. The cats example in the docs is the canonical layout: `cats.module.ts`, `cats.controller.ts`, `cats.service.ts`, `dto/`, `interfaces/`.

```typescript
import { Module } from '@nestjs/common';
import { CatsController } from './cats.controller';
import { CatsService } from './cats.service';

@Module({
  controllers: [CatsController],
  providers: [CatsService],
})
export class CatsModule {}
```

```typescript
import { Module } from '@nestjs/common';
import { CatsModule } from './cats/cats.module';

@Module({
  imports: [CatsModule],
})
export class AppModule {}
```

Non-idiomatic: registering `CatsController` and `CatsService` only in `AppModule` after the feature has grown, or copying `CatsService` into several `providers` arrays.

**Sources.** [Modules](https://docs.nestjs.com/modules). **Confidence:** high. **Caveats:** the docs say small apps may have only a root module. Do not force a feature module for a one-file script.

### 1.2 Export is the module public API

**Rule candidate.** To share a provider, export it from the host module and import that module. Do not re-provide the class in the consumer. Re-export an imported module when a facade module should expose it.

**Why.** Modules are singletons. Importing a module that exports `CatsService` shares one instance. Registering `CatsService` in two modules creates two instances, extra memory, and split in-memory state.

```typescript
@Module({
  controllers: [CatsController],
  providers: [CatsService],
  exports: [CatsService],
})
export class CatsModule {}
```

```typescript
@Module({
  imports: [CommonModule],
  exports: [CommonModule],
})
export class CoreModule {}
```

**Sources.** [Shared modules](https://docs.nestjs.com/modules#shared-modules), [Module re-exporting](https://docs.nestjs.com/modules#module-re-exporting). **Confidence:** high.

### 1.3 Global modules are an exception

**Rule candidate.** Use `@Global()` or `global: true` on a dynamic module only for things that truly belong everywhere, such as config or a database connection module registered once from the root. Keep feature APIs explicit in `imports`.

**Why.** Nest encapsulates providers on purpose. Angular registers providers globally. Nest does not. The docs warn twice that making everything global is not a good design decision.

```typescript
@Global()
@Module({
  providers: [ConfigService],
  exports: [ConfigService],
})
export class ConfigModule {}
```

Prefer `ConfigModule.forRoot({ isGlobal: true })` when using `@nestjs/config`, which is the documented way to avoid importing `ConfigModule` in every feature.

**Sources.** [Global modules](https://docs.nestjs.com/modules#global-modules), [ConfigModule isGlobal](https://docs.nestjs.com/techniques/configuration#use-module-globally). **Confidence:** high.

### 1.4 Dynamic modules take consumer configuration

**Rule candidate.** If a module's providers depend on runtime options, expose `forRoot` / `register` and `forRootAsync` / `registerAsync`. Return a `DynamicModule` with `module: ThisModule`. Use `ConfigurableModuleBuilder` instead of hand-rolling async options. In Nest 11, share a dynamic module instance by assigning it to a variable. Do not assume hash-based deduplication.

**Why.** Static `imports: [ConfigModule]` cannot take a folder path. `register({ folder: './config' })` can. Nest 11 stopped generating predictable hashes for dynamic modules and compares object references instead.

```typescript
@Module({
  imports: [DatabaseModule.forRoot([User])],
})
export class AppModule {}
```

```typescript
export const usersOrm = TypeOrmModule.forFeature([User]);

@Module({
  imports: [usersOrm],
  exports: [usersOrm],
})
export class UsersModule {}
```

**Sources.** [Dynamic modules](https://docs.nestjs.com/fundamentals/dynamic-modules), [ConfigurableModuleBuilder](https://docs.nestjs.com/fundamentals/dynamic-modules), [v11 module resolution](https://docs.nestjs.com/migration-guide). **Confidence:** high. **Caveats:** `forRoot` vs `register` is convention, not a compiler rule. Integration tests that imported `TypeOrmModule.forFeature([User])` twice may now get two instances unless they reuse the same object or pass `moduleIdGeneratorAlgorithm: 'deep-hash'`.

### 1.5 Configuration is a dynamic module with validation at startup

**Rule candidate.** Load env through `ConfigModule.forRoot()`. Validate with Joi `validationSchema` or a `validate` function that uses `plainToInstance` and `validateSync`. Do not scatter `process.env` reads through services. Access `ConfigService` in `main.ts` via `app.get(ConfigService)` after create. Custom YAML/JS config factories are not covered by `validationSchema`. Validate inside the factory.

**Why.** Docs cite 12-factor config. Runtime env wins over `.env` when both define a key. `@nestjs/config@4` changed `ConfigService#get` precedence to internal config, then validated env, then `process.env`. `ignoreEnvVars` is deprecated in favor of `validatePredefined`.

**Sources.** [Configuration](https://docs.nestjs.com/techniques/configuration), [config 4.0.0 notes in the migration guide](https://docs.nestjs.com/migration-guide). **Confidence:** high for the Nest wrapper. dotenv and Joi behavior belongs to those libraries.

## 2. Controllers, providers, and injection

### 2.1 Controllers route. Providers do the work.

**Rule candidate.** Keep HTTP concerns in the controller: method, path, status, DTO binding, guards. Put storage, orchestration, and domain decisions in `@Injectable()` providers. Inject those providers through the constructor.

```typescript
@Controller('cats')
export class CatsController {
  constructor(private readonly catsService: CatsService) {}

  @Post()
  create(@Body() createCatDto: CreateCatDto) {
    return this.catsService.create(createCatDto);
  }

  @Get()
  findAll() {
    return this.catsService.findAll();
  }
}
```

**Sources.** [Controllers](https://docs.nestjs.com/controllers), [Providers](https://docs.nestjs.com/providers). The providers chapter says controllers should handle HTTP and delegate complex tasks. **Confidence:** high. This is the closest official statement to "no fat controllers."

### 2.2 Prefer constructor injection. Use `@Inject()` for non-class tokens.

**Rule candidate.** Inject by class type when the token is a class or abstract class. Use `@Inject(TOKEN)` for string or symbol tokens. Put tokens in a `constants.ts` file. Prefer `Symbol` tokens in libraries to avoid string collisions. Do not use property injection unless a subclass makes `super()` painful. Do not use TypeScript interfaces as DI tokens. They are erased.

```typescript
export const LOGGER_SERVICE = Symbol('LOGGER_SERVICE');

@Module({
  providers: [{ provide: LOGGER_SERVICE, useClass: PinoLoggerService }],
  exports: [LOGGER_SERVICE],
})
export class LoggerModule {}

@Injectable()
export class CatsService {
  constructor(@Inject(LOGGER_SERVICE) private readonly logger: LoggerService) {}
}
```

Abstract class tokens can skip `@Inject()` because they exist at runtime. That is official, not folklore.

**Sources.** [Providers](https://docs.nestjs.com/providers), [Custom providers](https://docs.nestjs.com/fundamentals/custom-providers). **Confidence:** high.

### 2.3 Custom providers: `useClass`, `useValue`, `useFactory`, `useExisting`

**Rule candidate.** Use `useValue` for mocks and constant config. Use `useClass` when the token should resolve to a different class. Use `useFactory` when construction needs other providers or async work. Use `useExisting` for aliases and for making `APP_GUARD` overrideable in tests. Export custom providers by token or by the full provider object.

**Sources.** [Custom providers](https://docs.nestjs.com/fundamentals/custom-providers), [Testing globally registered enhancers](https://docs.nestjs.com/fundamentals/testing#overriding-globally-registered-enhancers). **Confidence:** high.

### 2.4 Default singleton. Request scope is a special case.

**Rule candidate.** Leave providers on `Scope.DEFAULT` unless the instance must differ per request or per consumer. Request scope bubbles up. A singleton that injects a request-scoped provider becomes request-scoped. Transient does not bubble. Gateways, Passport strategies, and cron controllers must stay singletons. Durable providers exist for multi-tenant DI subtrees, not as a default.

```typescript
@Injectable({ scope: Scope.REQUEST })
export class TenantContext {
  constructor(@Inject(REQUEST) private readonly request: Request) {}
}
```

Do not write that for a normal `UsersService`.

The docs say a well-designed request-scoped app should not slow down by more than about 5% latency. Treat that as a Nest-authored estimate, not a benchmark you can quote as law. The stronger statement is the one they repeat: unless the provider must be request-scoped, use singleton.

**Sources.** [Injection scopes](https://docs.nestjs.com/fundamentals/injection-scopes). **Confidence:** high on the mechanism. Medium on the 5% figure.

**Caveats.** Injecting `REQUEST` forces request scope up the chain. Async local storage is the documented alternative when you want request data without that cost. See finding 6.3.

### 2.5 Circular dependencies: refactor first, then `forwardRef`, then `ModuleRef`

**Rule candidate.** Break the cycle with a shared module or by moving the shared type. If both providers or modules still depend on each other, wrap both sides in `forwardRef(() => Other)`. Do not depend on constructor order. Do not combine circular graphs with `Scope.REQUEST` without reading the known failure mode. `ModuleRef.get` is an official alternative, not the default style.

```typescript
@Injectable()
export class CatsService {
  constructor(
    @Inject(forwardRef(() => CommonService))
    private readonly commonService: CommonService,
  ) {}
}
```

**Sources.** [Circular dependency](https://docs.nestjs.com/fundamentals/circular-dependency), [nest#5778](https://github.com/nestjs/nest/issues/5778) for request-scoped undefined deps. Trilon's runtime article calls `forwardRef` a last resort. That last-resort wording is maintainer-adjacent opinion. The docs only say avoid cycles where possible. **Confidence:** high on the API. Medium on "last resort" as a hard rule.

### 2.6 `ModuleRef` is for scoped resolution and late instantiation, not a service locator

**Rule candidate.** Inject constructors. Use `ModuleRef.get` for tokens that cannot be declared, `resolve` for request or transient providers, and `create` for classes not registered as providers. `get()` cannot retrieve scoped providers. `resolve()` returns a unique subtree unless you pass a `ContextId`.

Using `ModuleRef` in every service to look up collaborators is not described as a best practice. It is described as an escape hatch for circular graphs and dynamic instantiation.

**Sources.** [Module reference](https://docs.nestjs.com/fundamentals/module-ref). **Confidence:** high on the API. The "do not service-locate" rule is inferred from the DI chapters, not a verbatim warning. Mark it as such in the skill.

## 3. DTOs, validation, transformation, serialization

### 3.1 DTO classes, not interfaces, at the HTTP boundary

**Rule candidate.** Declare request bodies, query objects, and param objects as classes. Import the class as a value, not `import type`. Do not type `@Body()` as an interface or a generic array and expect `ValidationPipe` to work. TypeScript erases those.

```typescript
import { IsEmail, IsNotEmpty } from 'class-validator';

export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsNotEmpty()
  password: string;
}
```

```typescript
@Post()
create(@Body() createUserDto: CreateUserDto) {
  return this.usersService.create(createUserDto);
}
```

**Sources.** [Controllers, request payloads](https://docs.nestjs.com/controllers#request-payloads), [Validation](https://docs.nestjs.com/techniques/validation). **Confidence:** high.

### 3.2 Validate in pipes at the boundary. Bind `ValidationPipe` globally.

**Rule candidate.** Install `class-validator` and `class-transformer`. Bind `ValidationPipe` with `app.useGlobalPipes` or `APP_PIPE`. Enable `whitelist: true`. Enable `forbidNonWhitelisted: true` when extra properties should 400 rather than be stripped. Keep detailed errors off in production with `disableErrorMessages` if that is the product policy.

Pipes run inside the exceptions zone. A thrown `BadRequestException` prevents the controller method from running. That is the documented reason pipes exist: validate external data at the system boundary, not inside every handler.

```typescript
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
  }),
);
```

**Sources.** [Pipes](https://docs.nestjs.com/pipes), [Validation](https://docs.nestjs.com/techniques/validation). **Confidence:** high.

### 3.3 `transform` is not a free lunch

**Rule candidate.** Set `transform: true` only when you want payloads instantiated as DTO classes and primitive query or path params converted from strings. Prefer explicit `ParseIntPipe`, `ParseBoolPipe`, `ParseUUIDPipe`, and `ParseArrayPipe` when conversion should be local and obvious. `Parse*` pipes throw on `undefined`. Put `DefaultValuePipe` first for optional query params.

```typescript
@Get()
findAll(
  @Query('activeOnly', new DefaultValuePipe(false), ParseBoolPipe)
  activeOnly: boolean,
  @Query('ids', new ParseArrayPipe({ items: Number, separator: ',' }))
  ids: number[],
) {}
```

**Sources.** [Validation, transform](https://docs.nestjs.com/techniques/validation#transform-payload-objects), [ParseArrayPipe](https://docs.nestjs.com/techniques/validation#parsing-and-validating-arrays), [DefaultValuePipe](https://docs.nestjs.com/pipes#providing-defaults). **Confidence:** high.

**Caveat.** Implicit conversion of query params requires `transform: true`. Implicit conversion of nested object types is `class-transformer` behavior, not Nest magic. `enableImplicitConversion` is a class-transformer option. Nest's config `validate` example sets it. A global `ValidationPipe` does not unless you pass `transformOptions`.

### 3.4 Nest's `ValidationPipe` defaults `forbidUnknownValues` to false

**Rule candidate.** Know the split. `class-validator` 0.14+ defaults `forbidUnknownValues` to true so objects with no metadata fail closed. Nest's `ValidationPipe` constructor still forces `forbidUnknownValues: false` unless the caller overrides it, because the 0.14 change broke undecorated DTO classes. For a standards skill, prefer decorated DTOs plus `whitelist`. Do not "fix" unknown-value errors by turning the flag off without understanding the metadata gap.

**Why.** class-validator enabled the flag to stop objects with no validators from passing. Nest restored the old default in the pipe to avoid a framework-wide regression. A DTO with zero decorators will pass Nest's pipe and fail a raw `validate()` call from 0.14.

**Sources.** [class-validator PR 1798](https://github.com/typestack/class-validator/pull/1798), [nest#10683](https://github.com/nestjs/nest/issues/10683), [validation.pipe.ts](https://github.com/nestjs/nest/blob/master/packages/common/pipes/validation.pipe.ts) line that sets `{ forbidUnknownValues: false, ...validatorOptions }`. **Confidence:** high. **Version-sensitive:** this is Nest current source as of the v11 line. Re-check on v12.

### 3.5 Mapped types must come from the right package

**Rule candidate.** HTTP apps without Swagger or GraphQL import `PartialType`, `PickType`, `OmitType`, and `IntersectionType` from `@nestjs/mapped-types`. OpenAPI apps import them from `@nestjs/swagger`. GraphQL apps import them from `@nestjs/graphql`. Mixing packages is a documented source of "undocumented side-effects."

```typescript
import { PartialType } from '@nestjs/mapped-types';

export class UpdateCatDto extends PartialType(CreateCatDto) {}
```

**Sources.** [Validation, mapped types](https://docs.nestjs.com/techniques/validation#mapped-types), [OpenAPI mapped types](https://docs.nestjs.com/openapi/mapped-types). **Confidence:** high.

### 3.6 Serialize with `ClassSerializerInterceptor` on class instances

**Rule candidate.** Exclude secrets with `@Exclude()`. Return class instances, or set `@SerializeOptions({ type: UserEntity })` when returning plain objects. Do not wrap an entity in a plain object and expect nested serialization. The interceptor uses `instanceToPlain()`. It does not apply to `StreamableFile`.

```typescript
@UseInterceptors(ClassSerializerInterceptor)
@Get()
findOne(): UserEntity {
  return new UserEntity({
    id: 1,
    firstName: 'John',
    lastName: 'Doe',
    password: 'password',
  });
}
```

**Sources.** [Serialization](https://docs.nestjs.com/techniques/serialization). **Confidence:** high.

**Caveat.** Nest docs put `@Exclude()` on `UserEntity`. That couples persistence and HTTP serialization if the same class is your ORM entity. Official Nest does this. `typescript-standards` would keep a response DTO. Do not call the Nest example wrong. Call the coupling out as a skill fork.

### 3.7 `class-transformer` `plainToClass` is deprecated

**Rule candidate.** Use `plainToInstance`. Nest's own docs and v11 changelog already switched.

**Sources.** [Pipes custom ValidationPipe sample](https://docs.nestjs.com/pipes), [v11.0.0 changelog](https://github.com/nestjs/nest/releases/tag/v11.0.0). **Confidence:** high.

## 4. Errors and the request lifecycle

### 4.1 Throw `HttpException` subclasses. Use `cause` for logs, not clients.

**Rule candidate.** Throw `NotFoundException`, `UnauthorizedException`, `ForbiddenException`, `BadRequestException`, and the rest from `@nestjs/common`. Extend `HttpException` for app-specific types. Pass `{ cause }` for logging. Built-in HTTP, WS, and RPC exceptions extend `IntrinsicException` and are not logged by the default filter. Unrecognized throws become `{ statusCode: 500, message: "Internal server error" }`. Objects with `statusCode` and `message` are treated like `http-errors`.

```typescript
throw new NotFoundException(`Cat ${id} was not found`);
```

```typescript
throw new BadRequestException('Invalid payload', {
  cause: error,
  description: 'CreateCatDto failed validation',
});
```

**Sources.** [Exception filters](https://docs.nestjs.com/exception-filters). **Confidence:** high.

### 4.2 Filters see only uncaught exceptions

**Rule candidate.** Do not wrap a service call in `try/catch` that swallows the error if a filter should format it. Caught exceptions skip filters. Route filters run before controller filters before global filters. A matching inner filter consumes the exception. Global `useGlobalFilters()` does not apply to gateways or hybrid apps. Register `APP_FILTER` from a module when the filter needs DI. Prefer passing the filter class, not `new HttpExceptionFilter()`, so Nest reuses the instance.

Platform-agnostic catch-all filters should reply through `HttpAdapterHost`, not Express `response.json()`. Fastify uses `response.send()`.

**Sources.** [Exception filters](https://docs.nestjs.com/exception-filters), [Request lifecycle](https://docs.nestjs.com/faq/request-lifecycle). **Confidence:** high.

### 4.3 Standard response mode, not library-specific `@Res()`

**Rule candidate.** Return values from handlers. Nest serializes objects to JSON. Default status is 200, 201 for POST. Use `@HttpCode()` and `@Header()` to change that. If you inject `@Res()` or `@Next()`, you own the response and you lose interceptors and those decorators unless `{ passthrough: true }`.

```typescript
@Get()
findAll(@Res({ passthrough: true }) res: Response) {
  res.setHeader('X-Request-Id', '…');
  return this.catsService.findAll();
}
```

**Sources.** [Controllers](https://docs.nestjs.com/controllers). **Confidence:** high.

## 5. Security

### 5.1 Authentication is a guard that assigns `request.user`

**Rule candidate.** For JWT bearer APIs, issue tokens from an `AuthService`, verify in an `AuthGuard`, assign `request.user`, and protect routes with `@UseGuards`. For "most routes are private," register `APP_GUARD` and mark public routes with `@Public()` metadata that `getAllAndOverride` reads. Never commit JWT secrets. The docs' sample `jwtConstants.secret` is explicitly a warning. Hash passwords. The sample compares plaintext and says not to.

Passport remains optional via `@nestjs/passport`. The newer first-class chapter uses `@nestjs/jwt` without Passport.

**Sources.** [Authentication](https://docs.nestjs.com/security/authentication), [Passport recipe](https://docs.nestjs.com/recipes/passport). **Confidence:** high for the JWT sample. Auth strategy choice is application-specific.

**Tension.** The Guards chapter says middleware is a fine choice for authentication because token validation is not route-specific. The Authentication chapter implements a guard. Both are official. A skill should say: middleware or a global guard may authenticate and attach `request.user`. Authorization that depends on route metadata belongs in a guard.

### 5.2 Authorization reads metadata through `Reflector`

**Rule candidate.** Put required roles or permissions on handlers with a custom decorator. Read them with `Reflector.getAllAndOverride` so class and method metadata compose. Return `false` only if a 403 is correct. Throw `UnauthorizedException` when the caller is anonymous. Docs call the built-in RBAC sample "basic" and warn that multi-operation handlers may need checks inside business logic. CASL is shown as one library, not the Nest standard.

**Sources.** [Guards](https://docs.nestjs.com/guards), [Authorization](https://docs.nestjs.com/security/authorization). **Confidence:** high on Reflector. Medium on CASL as a default.

### 5.3 Helmet, CORS, CSRF, rate limits, and secrets

**Rule candidate.**

- Apply Helmet before other `app.use()` calls and before routes. Express: `app.use(helmet())`. Fastify: `await app.register(helmet)` as a plugin, not middleware. GraphQL playground needs CSP exceptions.
- Enable CORS with `app.enableCors()` or `{ cors: true }`. Fastify v5 allows only CORS-safelisted methods by default. Name `PUT`, `PATCH`, and `DELETE` if you need them.
- CSRF is for cookie-session browser apps. Express uses `csrf-csrf` after session or cookie-parser. Fastify uses `@fastify/csrf-protection` after a storage plugin. A bearer-token API does not get a free CSRF story from these packages.
- Rate limit with `@nestjs/throttler`. `ttl` is milliseconds since v5. Behind a proxy, set `trust proxy` and override `getTracker`. In-memory storage is not a cluster source of truth. Redis storage is community, `jmcdo29/nest-lab`.
- Read secrets from env or a vault through `ConfigService`. Deployment docs: do not hardcode keys.

**Sources.** [Helmet](https://docs.nestjs.com/security/helmet), [CORS](https://docs.nestjs.com/security/cors), [CSRF](https://docs.nestjs.com/security/csrf), [Rate limiting](https://docs.nestjs.com/security/rate-limiting), [Deployment](https://docs.nestjs.com/deployment), [v11 Fastify CORS](https://docs.nestjs.com/migration-guide). **Confidence:** high.

## 6. Async work, RxJS, queues, cancellation

### 6.1 Handlers may return `Promise` or `Observable`. Nest subscribes.

**Rule candidate.** `async` methods are first-class. Returning `Observable` is also first-class. Nest subscribes and uses the last emission. Prefer Promises in application code unless you already have a stream. Do not mix `@Res()` with interceptor-based timeout or mapping.

**Sources.** [Controllers, asynchronicity](https://docs.nestjs.com/controllers#asynchronicity). **Confidence:** high.

### 6.2 Timeouts are an interceptor. They are not AbortSignal.

**Rule candidate.** The official timeout sample uses RxJS `timeout(5000)` in an interceptor and maps `TimeoutError` to `RequestTimeoutException`. Nest does not document a standard `AbortSignal` on `REQUEST` for handler cancellation. Do not claim framework-level request cancellation unless you implement it. Interceptor timeout cancels the Observable subscription. It does not automatically cancel a hanging database driver.

```typescript
return next.handle().pipe(
  timeout(5000),
  catchError((err) => {
    if (err instanceof TimeoutError) {
      return throwError(() => new RequestTimeoutException());
    }
    return throwError(() => err);
  }),
);
```

**Sources.** [Interceptors, more operators](https://docs.nestjs.com/interceptors#more-operators). **Confidence:** high that this is the official pattern. High that AbortSignal is absent from these docs.

### 6.3 Request context without request-scoped DI: AsyncLocalStorage

**Rule candidate.** When many providers need request-scoped values, wrap the request in `AsyncLocalStorage.run` from middleware, which is the first lifecycle slot. Nest has no built-in ALS abstraction. `nestjs-cls` is documented as a third-party package, not core. The docs warn that ALS hides data flow and can become a God object.

This is the official alternative to bubbling `Scope.REQUEST`.

**Sources.** [Async local storage](https://docs.nestjs.com/recipes/async-local-storage). **Confidence:** high.

### 6.4 Queues, events, and cron are optional infrastructure

**Rule candidate for a general skill.** Do not put CPU-heavy or retryable work on the request thread when a queue exists. `@nestjs/bullmq` is the actively developed wrapper. `@nestjs/bull` is maintenance mode. `@nestjs/event-emitter` is in-process `eventemitter2`. Listeners register on `onApplicationBootstrap`. `@nestjs/schedule` cron controllers must be singletons. In-process events are not a durable outbox.

These belong in a conditional reference, not v1 core, unless the repo already uses them.

**Sources.** [Queues](https://docs.nestjs.com/techniques/queues), [Events](https://docs.nestjs.com/techniques/events), [Task scheduling](https://docs.nestjs.com/techniques/task-scheduling), [Injection scopes notice on cron](https://docs.nestjs.com/fundamentals/injection-scopes). **Confidence:** high.

## 7. Persistence at the Nest boundary

### 7.1 Nest is database-agnostic. Official integrations still have a shape.

**Rule candidate.** Pick the repository's ORM. At the Nest boundary: register `forRoot` once, `forFeature` in the feature module, inject with the integration decorator, re-export `TypeOrmModule` if another module needs the same repository. Keep entities next to the feature, which is the Nest recommendation, not a DDD layered folder.

```typescript
@Module({
  imports: [TypeOrmModule.forFeature([User])],
  providers: [UsersService],
  controllers: [UsersController],
  exports: [TypeOrmModule],
})
export class UsersModule {}
```

```typescript
@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private readonly usersRepository: Repository<User>,
  ) {}
}
```

**Sources.** [Database](https://docs.nestjs.com/techniques/sql). **Confidence:** high for TypeORM integration shape. Prisma and Sequelize have parallel recipes.

**Skill fork.** Injecting `Repository<User>` into `UsersService` is idiomatic Nest. `typescript-standards` would hide the ORM behind an application-owned store. The Nest skill should not forbid `@InjectRepository` unless the local repo already has that seam.

### 7.2 `synchronize: true` is not production

**Rule candidate.** Never enable TypeORM `synchronize` in production. The docs warn you can lose data.

**Sources.** [Database](https://docs.nestjs.com/techniques/sql). **Confidence:** high.

### 7.3 Transactions: Nest recommends `QueryRunner` plus a narrow factory for tests

**Rule candidate.** For TypeORM, Nest recommends `QueryRunner` for control, and also shows `dataSource.transaction(async manager => …)`. Release the runner in `finally`. To test without mocking all of `DataSource`, wrap runner creation in a small factory. Transaction scope belongs in the operation that needs atomicity. Nest does not invent a Unit of Work beyond what the ORM provides.

Do not hold a transaction open across unrelated HTTP calls. That is `typescript-standards`, not a Nest sentence.

**Sources.** [TypeORM Transactions](https://docs.nestjs.com/techniques/sql). **Confidence:** high for TypeORM. Other ORMs: follow their recipe.

### 7.4 Request-scoped repositories are usually the wrong fix for tenancy

**Rule candidate.** A request-scoped DataSource that most of the graph depends on will request-scope the graph. Durable providers exist for a small tenant set. ALS can carry `tenantId` into a singleton repository. Choose with the scopes chapter in hand, not by making every repository request-scoped.

**Sources.** [Injection scopes, durable providers](https://docs.nestjs.com/fundamentals/injection-scopes). **Confidence:** high on the cost. Medium on which tenancy design to pick. Nest shows durable providers as the multi-tenant DI answer and warns they are not ideal for a large tenant count.

## 8. Testing

### 8.1 Three official levels: isolated, TestingModule, e2e

**Rule candidate.**

- Isolated: `new CatsController(catsService)` when the class is a plain constructor.
- Unit with Nest DI: `Test.createTestingModule({…}).compile()`, then `moduleRef.get(Token)`.
- Scoped: `moduleRef.resolve(Token)`.
- e2e: `createNestApplication()`, `init()`, `request(app.getHttpServer())`, `app.close()` in `afterAll`. Fastify also needs `getHttpAdapter().getInstance().ready()` and may use `app.inject()`.

Keep unit specs next to the class as `*.spec.ts`. Keep e2e under `test/` as `*.e2e-spec.ts`. Nest is test-runner agnostic. Jest is the v11 default scaffold. v12 ESM apps are planned to default to Vitest.

```typescript
const moduleRef = await Test.createTestingModule({
  imports: [CatsModule],
})
  .overrideProvider(CatsService)
  .useValue({ findAll: () => ['test'] })
  .compile();

app = moduleRef.createNestApplication();
await app.init();
```

**Sources.** [Testing](https://docs.nestjs.com/fundamentals/testing). **Confidence:** high.

### 8.2 Override global enhancers through `useExisting`

**Rule candidate.** `APP_GUARD` with `useClass: JwtAuthGuard` is a multi-provider. `overrideProvider(JwtAuthGuard)` will not replace it. Register `useExisting: JwtAuthGuard` plus `JwtAuthGuard` in `providers`, then override `JwtAuthGuard`.

**Sources.** [Testing](https://docs.nestjs.com/fundamentals/testing#overriding-globally-registered-enhancers). **Confidence:** high. Easy to miss. v1 should include it.

### 8.3 Auto-mocking is an official convenience, not a quality bar

**Rule candidate.** `useMocker` exists for large constructor graphs. Official e2e examples still replace one collaborator and hit HTTP. Jackie McDoniel's `testing-nestjs` repo is a useful catalog and says it is not canonical. Prefer tests through the module or HTTP surface the caller uses. That last sentence is this repo's testing standard, compatible with Nest's e2e chapter, not a Nest prohibition on `jest.spyOn`.

**Sources.** [Testing](https://docs.nestjs.com/fundamentals/testing), [jmcdo29/testing-nestjs](https://github.com/jmcdo29/testing-nestjs/). **Confidence:** high on the APIs. Medium on mock policy, because Nest's own unit sample spies on `catsService.findAll`.

### 8.4 Lifecycle cleanup

**Rule candidate.** Always `await app.close()` after `createNestApplication`. `enableShutdownHooks()` starts extra listeners. Do not enable it in tests that boot many apps in one Jest process unless you need those hooks. The docs warn Node will complain about listener counts.

**Sources.** [Testing](https://docs.nestjs.com/fundamentals/testing), [Lifecycle events](https://docs.nestjs.com/fundamentals/lifecycle-events). **Confidence:** high.

## 9. Observability

### 9.1 Use `Logger` with context. JSON in containers.

**Rule candidate.** `new Logger(CatsService.name)` or a transient custom logger with `setContext`. Do not use a singleton custom logger if `setContext` would overwrite the name for every consumer. For a DI logger that Nest itself should use, `bufferLogs: true` then `app.useLogger(app.get(MyLogger))`. v11 `ConsoleLogger` supports `{ json: true }` for container log aggregators. Implement `LoggerService` to swap in Pino or Winston. The built-in logger is for Nest system logs and simple app logs.

**Sources.** [Logger](https://docs.nestjs.com/techniques/logger), [v11.0.0 JSON logger](https://github.com/nestjs/nest/releases/tag/v11.0.0), [Deployment logging](https://docs.nestjs.com/deployment). **Confidence:** high.

### 9.2 Correlation IDs

**Rule candidate.** Deployment docs tell you to put correlation IDs in logs in distributed systems. They do not ship a first-party request-id module. Implement with middleware plus ALS, or with `nestjs-cls`, which can generate a request id. Interceptors can also set a header, but middleware runs first and is the ALS recipe's wrap point.

**Sources.** [Deployment logging](https://docs.nestjs.com/deployment), [Async local storage](https://docs.nestjs.com/recipes/async-local-storage). **Confidence:** high that you must build this. There is no official correlation interceptor.

### 9.3 OpenTelemetry is not first-party Nest

**Rule candidate.** Do not look for `@nestjs/opentelemetry` in official docs. There isn't a Nest chapter. OpenTelemetry JS contrib publishes `@opentelemetry/instrumentation-nestjs-core`, compatible with `@nestjs/core` `>=4 <12`. Load the SDK before `NestFactory.create`. Pair it with HTTP and Express or Fastify instrumentations. Nest's Sentry recipe is a separate error-reporting path.

**Sources.** [OpenTelemetry instrumentation-nestjs-core](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-nestjs-core), [Sentry recipe](https://docs.nestjs.com/recipes/sentry). **Confidence:** high that Nest docs do not cover OTel. High that the contrib package is the upstream instrumentation.

### 9.4 Exception reporting

**Rule candidate.** Built-in `HttpException`s are not logged. If you need them in a reporter, write a filter or extend `BaseExceptionFilter`. Do not log from every service and the filter. Record once at the boundary that has status code and path.

**Sources.** [Exception filters, exceptions logging](https://docs.nestjs.com/exception-filters). The "once at the boundary" part is `typescript-standards`, aligned with the filter chapter. **Confidence:** high on the Nest logging skip. Medium on single-boundary as a Nest rule.

## 10. Performance and operations

### 10.1 Fastify is faster and less compatible

**Rule candidate.** Stay on Express unless you need the benchmark win or Fastify plugins. Fastify listens on `127.0.0.1` by default. Production containers must `listen(port, '0.0.0.0')`. Middleware sees raw Node `req`/`res`, not Fastify wrappers. Helmet, CSRF, multipart, and e2e setup all change. Express recipes will not silently work.

**Sources.** [Performance](https://docs.nestjs.com/techniques/performance). **Confidence:** high.

### 10.2 Graceful shutdown is opt-in

**Rule candidate.** Call `app.enableShutdownHooks()` in production HTTP processes. Implement `OnModuleDestroy` / `BeforeApplicationShutdown` / `OnApplicationShutdown` to close DB pools and Redis. Request-scoped classes do not get these hooks. `app.close()` does not kill the Node process if timers remain. Windows does not deliver `SIGTERM` from Task Manager. v11 runs destroy hooks in reverse init order. Terminus `gracefulShutdownTimeoutMs` can delay shutdown for Kubernetes readiness.

```typescript
app.enableShutdownHooks();
```

**Sources.** [Lifecycle events](https://docs.nestjs.com/fundamentals/lifecycle-events), [Terminus graceful shutdown](https://docs.nestjs.com/recipes/terminus). **Confidence:** high.

### 10.3 Health checks through Terminus

**Rule candidate.** Expose `/health` with `@HealthCheck()` and `HealthCheckService`. Use the packaged indicators for TypeORM, Prisma, Mongoose, memory, disk, HTTP. Enable shutdown hooks so Terminus can report `shutting_down`. Custom indicators should use `HealthIndicatorService` in v11. `HealthIndicator` and `HealthCheckError` are deprecated.

**Sources.** [Healthchecks](https://docs.nestjs.com/recipes/terminus), [Migration guide](https://docs.nestjs.com/migration-guide). **Confidence:** high.

### 10.4 Versioning, OpenAPI, Docker

**Rule candidate.** URI versioning is the default of four types. Neutral routes opt out. Middleware versioning exists. OpenAPI lives in `@nestjs/swagger`. Mapped types must be imported from that package when Swagger is on. Production: `NODE_ENV=production`, `node dist/main.js`, Node 20+ image. The sample Dockerfile runs `npm install` then `npm run build`. A skill may recommend `npm ci --omit=dev` for a multi-stage image. That tightening is operations judgment, not a Nest sentence. Mau is the official Nest deploy product. Mention it. Do not require it.

**Sources.** [Versioning](https://docs.nestjs.com/techniques/versioning), [OpenAPI](https://docs.nestjs.com/openapi/introduction), [Deployment](https://docs.nestjs.com/deployment). **Confidence:** high on the APIs.

## 11. GraphQL, WebSockets, microservices, CQRS

**Rule candidate for core vs optional.** These stacks reuse pipes, guards, interceptors, and filters. They change how you get the request: `CONTEXT` instead of `REQUEST` in GraphQL, different exception types for RPC and WS, hybrid `useGlobalPipes()` not applying to gateways. Keep a short cross-cutting note in core. Put full rules in optional references.

CQRS is a recipe, not a default architecture. Do not require `@nestjs/cqrs` in v1.

**Sources.** [Microservices overview](https://docs.nestjs.com/microservices/basics), [CQRS recipe](https://docs.nestjs.com/recipes/cqrs), GraphQL and WebSockets sections of the docs index. **Confidence:** high.

## 12. Naming, structure, decorators, metadata

### 12.1 Follow the CLI file pattern unless the repo already differs

**Rule candidate.** Default idiomatic names are kebab-dot-role: `cats.controller.ts`, `cats.service.ts`, `cats.module.ts`, `create-cat.dto.ts`, `http-exception.filter.ts`. Classes are PascalCase with the role suffix: `CatsController`. The CLI generates this. Kamil said changing it was not supported in 2018. A later schematics `caseType` effort exists. Match the repo. When greenfield, use the CLI pattern.

Unit tests: `cats.controller.spec.ts` next to the class. e2e: `test/cats.e2e-spec.ts`.

**Sources.** [Modules directory tree](https://docs.nestjs.com/modules), [CLI generate](https://docs.nestjs.com/cli/usages), [nest-cli#183](https://github.com/nestjs/nest-cli/issues/183). **Confidence:** high as convention. Not a compiler rule.

### 12.2 Decorators attach metadata. `Reflector` reads it.

**Rule candidate.** Use `Reflector.createDecorator<T>()` or `@SetMetadata()`. Read with `get`, `getAllAndOverride`, or `getAllAndMerge`. v11 changed `getAllAndMerge` object-vs-array behavior and `getAllAndOverride` to `T | undefined`. Custom param decorators exist for wrapping `@Req()` access. Keep authorization policy in guards that read metadata. Do not hide business rules only in decorator factories.

**Sources.** [Guards](https://docs.nestjs.com/guards), [Custom decorators](https://docs.nestjs.com/custom-decorators), [Migration guide, Reflector](https://docs.nestjs.com/migration-guide). **Confidence:** high.

### 12.3 Do not import feature classes through same-folder barrels

**Rule candidate.** Skip `index.ts` barrels for files that participate in the module graph. `cats.controller` must not import `./` to reach `cats.service` in the same folder. This is an official warning with a linked issue, not folklore.

**Sources.** [Circular dependency](https://docs.nestjs.com/fundamentals/circular-dependency), [nest#1181](https://github.com/nestjs/nest/issues/1181#issuecomment-430197191). **Confidence:** high.

## 13. Anti-patterns, only where sources support them

| Pattern | What official sources actually say | Skill strength |
| --- | --- | --- |
| Re-providing instead of exporting | Creates extra instances and split state | Strong |
| `@Global()` on everything | "Not recommended as a design practice" | Strong |
| Barrel-induced cycles | Explicit warning | Strong |
| `forwardRef` as the first design | Avoid cycles where possible. Blogs say last resort. | Strong to avoid cycles. Medium on wording. |
| Fat controllers | Controllers handle HTTP, providers handle complex tasks | Strong |
| Business logic in pipes | Pipes are for transform/validate at the boundary. Docs also show `UserByIdPipe` loading an entity. | Strong for validation. Weak as a ban on lookup pipes. Official example contradicts a hard ban. |
| Business logic in interceptors | Interceptors are AOP: log, cache, map, timeout. Cache interceptor that skips `handle()` is official. | Do not dump domain rules here. Caching is allowed. |
| Request-scoped by default | "Strongly recommended" singleton | Strong |
| Swallowing exceptions | Filters ignore caught errors | Strong |
| `@Res()` without passthrough | Disables standard response features | Strong |
| `ModuleRef` as the app's DI API | Documented escape hatch | Medium. Infer, do not overclaim. |
| Leaking ORM types from HTTP | Nest examples return whatever the service returns, often entities | Not a Nest rule. Apply `typescript-standards` if the repo wants it. |
| Interfaces as DTOs or DI tokens | Erased at runtime | Strong |
| `synchronize: true` in production | Warning, data loss | Strong |
| JWT secret in source | Warning in the auth chapter | Strong |
| Helmet after routes | Order matters, will not apply | Strong |

# Lifecycle mechanism table

From [Request lifecycle](https://docs.nestjs.com/faq/request-lifecycle), plus the dedicated chapters.

Order for a successful HTTP request:

1. Incoming request
2. Globally bound middleware (`app.use`)
3. Module-bound middleware, root module first, then `imports` order. v11: global-module middleware runs first.
4. Global guards, controller guards, route guards
5. Global interceptors, controller interceptors, route interceptors, inbound
6. Global pipes, controller pipes, route pipes, then parameter pipes last-to-first
7. Controller method
8. Provider methods
9. Interceptors outbound, route then controller then global, FILO because Observables
10. Response

On uncaught exception, remaining steps skip to filters: route, then controller, then global.

| Need | Use | Why | Do not use |
| --- | --- | --- | --- |
| Mutate raw `req`/`res`, CORS, Helmet, ALS wrap, body parser | Middleware | First, path-based, Express-shaped. No `ExecutionContext`. | Guards, if you need handler metadata |
| Allow or deny using route metadata, roles, JWT | Guard | Runs after middleware, has `ExecutionContext` and `Reflector` | Middleware, if the decision depends on the handler |
| Validate or convert arguments | Pipe | Runs just before the method, can throw into the exception layer | Controller `if (!dto.email)` |
| Log timing, map the body, cache, timeout | Interceptor | Wraps `next.handle()` Observable | `@Res()` mapping, which they cannot see |
| Format uncaught errors | Exception filter | Only uncaught. Innermost wins. | `try/catch` that swallows |
| DI-capable global enhancer | `APP_PIPE` / `APP_GUARD` / `APP_INTERCEPTOR` / `APP_FILTER` | `app.useGlobal*()` is outside the module graph | `new` in `main.ts` when the class needs `ConfigService` |

Hybrid apps: `useGlobalPipes()` and `useGlobalGuards()` do not apply to gateways and microservices unless you change hybrid settings. Middleware path wildcards are version-sensitive: Express v5 wants `{*splat}`; Fastify middleware no longer wants `(.*)`.

# Proposed future skill information architecture

Match `react-standards` and `effect-standards`: a short `SKILL.md` that is a workflow, plus referenced files loaded by branch.

## `SKILL.md`

Always-loaded workflow:

1. Establish local Nest version, HTTP adapter, validation pipe options, ORM, test runner.
2. Trace the changed operation from HTTP or other transport through module exports, guards, pipes, provider, persistence, and tests.
3. Load every matching reference completely.
4. Design from the module public API and the controller's caller-visible contract inward.
5. Implement through constructors and Nest lifecycle slots.
6. Verify with the smallest typecheck and the tests those references require.

Decision priority should defer to the repo, then these defaults, and should name `typescript-standards` for types, errors, cancellation, and external-data parsing.

Pointers, one branch each:

- `references/modules-and-di.md` when modules, exports, global/dynamic modules, scopes, tokens, circular deps, or `ModuleRef` change.
- `references/http-controllers.md` when controllers, routing, `@Res()`, status codes, or versioning change.
- `references/validation-and-serialization.md` when DTOs, pipes, `class-validator`, mapped types, or `ClassSerializerInterceptor` change.
- `references/errors-and-enhancers.md` when exceptions, filters, guards, interceptors, middleware, or lifecycle order change.
- `references/security.md` when authn, authz, CORS, Helmet, CSRF, throttling, or secrets change.
- `references/persistence.md` when Nest ORM modules, repositories, or transactions at the Nest boundary change.
- `references/testing.md` whenever behavior or a public Nest contract changes.
- `references/observability-and-ops.md` when logging, health, shutdown, Fastify adapter, Docker, or config-in-`main.ts` change.
- `references/naming-and-structure.md` when files, barrels, CLI generate, or decorators or metadata change.

Also load `typescript-standards` when types, failures, or external data change.

## Conditional references

Create only when the skill description's extra branches fire:

- `references/graphql.md`
- `references/websockets.md`
- `references/microservices.md`
- `references/cqrs.md`
- `references/queues-events-schedule.md`

Do not put Fastify-only Helmet or listen-host rules only in a Fastify file. Put the adapter fork in `observability-and-ops.md` and `security.md`, because missing `0.0.0.0` is a production footgun.

## What not to duplicate

Leave Effect, React, and generic TypeScript in their skills. Nest-standards should not retell "parse at the edge" except to say: in Nest, that edge is a pipe plus a DTO class.

# Contradictions, weak claims, open questions

1. **Lookup pipes vs skinny handlers.** Pipes docs show `UserByIdPipe` returning a `UserEntity`. Many senior Nest codebases treat that as mixing persistence into the HTTP layer. Official docs allow it. Do not forbid it in v1 without a local rule.
2. **Authn in middleware vs guards.** Both are official. Resolve as: attach identity early, authorize with metadata in a guard.
3. **Returning ORM entities.** Serialization chapter uses `UserEntity` as the response type. Clean-architecture blogs from Trilon show repository interfaces. Official samples do not. Trace DIP-from-Trilon as practitioner opinion unless the repo already uses tokens for stores.
4. **Request-scope performance "about 5%".** Nest-authored, not independently measured here. Keep the qualitative rule. Drop the number from an enforceable skill, or quote it as Nest's own estimate.
5. **`forbidUnknownValues`.** class-validator and Nest `ValidationPipe` disagree. A skill that says "follow class-validator defaults" will fight Nest. Spell the Nest default out.
6. **Docs chrome still saying Version 10.** Content is v11. Agents that branch on the label will pick the wrong major.
7. **OpenTelemetry.** No Nest docs chapter. Contrib instrumentation exists and claims `<12`. Revisit at v12.
8. **AbortSignal / request cancellation.** Not a documented first-class HTTP feature. Timeout interceptor is. Client disconnect behavior depends on Express/Fastify and is not specified in the Nest lifecycle page.
9. **v12 test runner.** Do not rewrite testing rules around Vitest until v12 is the documented current. Scaffolded v11 apps still get Jest.
10. **Dynamic module identity in v11.** Tests that assumed `forFeature([User])` dedupes by content can fail. Official workaround list is in the migration guide.
11. **Global middleware order in v11.** Global-module middleware now runs first. Old topological-distance mental model is wrong.
12. **`nestjs-cls` and Redis throttler storage.** Documented by Nest, not owned by Nest. Third-party breakage is not a Nest bug.

# Prioritized shortlist for v1

Include these. They are source-backed and agents violate them constantly.

1. Feature modules, export as API, import to share a singleton, do not re-provide.
2. `@Global()` only for true app-wide infrastructure.
3. Constructor injection. Class or symbol tokens. No interface tokens. No same-folder barrels.
4. Singleton default. Request scope only when required, knowing it bubbles.
5. Controllers delegate to providers. Standard return values, not `@Res()` unless passthrough.
6. DTO classes with `class-validator`. Global `ValidationPipe` with `whitelist`. Right mapped-types package.
7. Throw HTTP exceptions. Do not swallow if a filter should run. `APP_*` tokens for DI globals. Pass enhancer classes, not always `new`.
8. Lifecycle table: middleware, guard, interceptor, pipe, filter.
9. Secrets from config. Helmet before routes. Adapter-specific CORS and Helmet. Throttler `ttl` in ms.
10. Tests: `TestingModule`, `overrideProvider`, `useExisting` for `APP_GUARD`, `app.close()`.
11. `enableShutdownHooks()` in production. Terminus for health. JSON logger in containers.
12. Fastify listen on `0.0.0.0` in containers. Named wildcards for Express v5 paths.

Defer to optional references: GraphQL resolvers, microservice transporters, WebSocket adapters, CQRS, BullMQ job design, durable multi-tenant trees, OTel SDK wiring.

# Source inventory

Access date for all entries: 2026-08-20, unless a publication date is listed.

## Primary: official Nest docs

| Title | URL |
| --- | --- |
| Documentation home | https://docs.nestjs.com/ |
| First steps / introduction | https://docs.nestjs.com/ |
| Modules | https://docs.nestjs.com/modules |
| Controllers | https://docs.nestjs.com/controllers |
| Providers | https://docs.nestjs.com/providers |
| Middleware | https://docs.nestjs.com/middleware |
| Exception filters | https://docs.nestjs.com/exception-filters |
| Pipes | https://docs.nestjs.com/pipes |
| Guards | https://docs.nestjs.com/guards |
| Interceptors | https://docs.nestjs.com/interceptors |
| Custom decorators | https://docs.nestjs.com/custom-decorators |
| Custom providers | https://docs.nestjs.com/fundamentals/custom-providers |
| Dynamic modules | https://docs.nestjs.com/fundamentals/dynamic-modules |
| Injection scopes | https://docs.nestjs.com/fundamentals/injection-scopes |
| Circular dependency | https://docs.nestjs.com/fundamentals/circular-dependency |
| Module reference | https://docs.nestjs.com/fundamentals/module-ref |
| Execution context | https://docs.nestjs.com/fundamentals/execution-context |
| Lifecycle events | https://docs.nestjs.com/fundamentals/lifecycle-events |
| Testing | https://docs.nestjs.com/fundamentals/testing |
| Configuration | https://docs.nestjs.com/techniques/configuration |
| Database / SQL | https://docs.nestjs.com/techniques/sql |
| Validation | https://docs.nestjs.com/techniques/validation |
| Serialization | https://docs.nestjs.com/techniques/serialization |
| Versioning | https://docs.nestjs.com/techniques/versioning |
| Logger | https://docs.nestjs.com/techniques/logger |
| Performance (Fastify) | https://docs.nestjs.com/techniques/performance |
| Queues | https://docs.nestjs.com/techniques/queues |
| Events | https://docs.nestjs.com/techniques/events |
| Task scheduling | https://docs.nestjs.com/techniques/task-scheduling |
| Authentication | https://docs.nestjs.com/security/authentication |
| Authorization | https://docs.nestjs.com/security/authorization |
| Helmet | https://docs.nestjs.com/security/helmet |
| CORS | https://docs.nestjs.com/security/cors |
| CSRF | https://docs.nestjs.com/security/csrf |
| Rate limiting | https://docs.nestjs.com/security/rate-limiting |
| Request lifecycle | https://docs.nestjs.com/faq/request-lifecycle |
| Migration guide, 10 to 11 | https://docs.nestjs.com/migration-guide |
| Deployment | https://docs.nestjs.com/deployment |
| Standalone applications | https://docs.nestjs.com/standalone-applications |
| OpenAPI mapped types | https://docs.nestjs.com/openapi/mapped-types |
| Healthchecks (Terminus) | https://docs.nestjs.com/recipes/terminus |
| Async local storage | https://docs.nestjs.com/recipes/async-local-storage |
| Passport | https://docs.nestjs.com/recipes/passport |
| CQRS | https://docs.nestjs.com/recipes/cqrs |
| Sentry | https://docs.nestjs.com/recipes/sentry |
| CLI usages | https://docs.nestjs.com/cli/usages |
| Microservices overview | https://docs.nestjs.com/microservices/basics |
| Docs markdown sources | https://github.com/nestjs/docs.nestjs.com |

## Primary: official Nest source and releases

| Title | Publisher | URL |
| --- | --- | --- |
| nestjs/nest README | NestJS | https://github.com/nestjs/nest |
| v11.0.0 release notes | Kamil Mysliwiec | https://github.com/nestjs/nest/releases/tag/v11.0.0 |
| v11.2.1 release | Kamil Mysliwiec, 2026-08-14 | https://github.com/nestjs/nest/releases/tag/v11.2.1 |
| ValidationPipe source, `forbidUnknownValues: false` | NestJS | https://github.com/nestjs/nest/blob/master/packages/common/pipes/validation.pipe.ts |
| nest#10683, class-validator 0.14 regression | NestJS issue tracker | https://github.com/nestjs/nest/issues/10683 |
| nest#1181, barrel files | NestJS issue tracker | https://github.com/nestjs/nest/issues/1181 |
| nest#5778, circular plus REQUEST scope | NestJS issue tracker | https://github.com/nestjs/nest/issues/5778 |
| v12.0.0 preparation PR | NestJS | https://github.com/nestjs/nest/pull/16391 |
| nest-cli v12 PR | NestJS | https://github.com/nestjs/nest-cli/pull/3280 |
| nest-cli#183, generated file names | Kamil Mysliwiec | https://github.com/nestjs/nest-cli/issues/183 |
| Official samples | NestJS | https://github.com/nestjs/nest/tree/master/sample |

## Primary: upstream libraries Nest delegates to

| Title | Publisher | URL |
| --- | --- | --- |
| class-validator usage | typestack | https://github.com/typestack/class-validator |
| class-validator PR 1798, `forbidUnknownValues` default | typestack | https://github.com/typestack/class-validator/pull/1798 |
| class-validator changelog | typestack | https://github.com/typestack/class-validator/blob/master/CHANGELOG.md |
| class-transformer | typestack | https://github.com/typestack/class-transformer |
| Express CORS | expressjs | https://github.com/expressjs/cors |
| Express v5 migration | Express | https://expressjs.com/en/guide/migrating-5.html |
| Fastify v5 migration | Fastify | https://fastify.dev/docs/v5.1.x/Guides/Migration-Guide-V5/ |
| Helmet | helmetjs | https://github.com/helmetjs/helmet |
| csrf-csrf | Psifi-Solutions | https://github.com/Psifi-Solutions/csrf-csrf |
| OpenTelemetry Nest instrumentation | OpenTelemetry JS contrib | https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-nestjs-core |
| Node.js AsyncLocalStorage | Node.js | https://nodejs.org/api/async_context.html |
| 12-factor config | 12factor.net | https://12factor.net/config |
| TypeORM transactions | TypeORM | https://typeorm.io/docs/advanced-topics/transactions/ |
| BullMQ | BullMQ | https://docs.bullmq.io/ |

## Secondary: maintainer and practitioner writing

Treat as opinion unless the same claim appears in official docs.

| Title | Author / publisher | Date | Notes |
| --- | --- | --- | --- |
| [Announcing NestJS 11: What's New](https://trilon.io/blog/announcing-nestjs-11-whats-new) | Kamil Mysliwiec, Trilon | 2025-01-22 | First-party announcement. Use for v11 feature list. Linked from the GitHub release. |
| [What is the NestJS Runtime](https://trilon.io/blog/what-is-the-nestjs-runtime) | Manuel Herrera, Trilon | 2022-06-23 | Restates singleton vs request scope. Adds "forwardRef as last resort" and SOLID framing. Last-resort wording is stronger than the docs. |
| [Dependency Inversion Principle](https://trilon.io/blog/dependency-inversion-principle) | Maciej Sikorski, Trilon | 2022-08-01 | Shows abstract-class or interface tokens with `useExisting`. The author says the principle need not apply to every dependency. Practitioner pattern, compatible with the custom providers docs. |
| [Implementing data source agnostic services with NestJS](https://trilon.io/blog/implementing-data-source-agnostic-services-with-nestjs) | Manuel Carballido, Trilon | 2023-04-14 | Factory that swaps TypeORM vs other stores from env. Opinionated architecture, not a framework rule. |
| [Introducing CLI Resource Generators](https://trilon.io/blog/introducing-cli-generators-crud-api-in-1-minute) | Kamil Mysliwiec, Trilon | 2020-09-22 | Matches CLI `nest g resource`. Traces to official CRUD generator docs. |
| [testing-nestjs](https://github.com/jmcdo29/testing-nestjs/) | Jackie McDoniel, Nest core team | accessed 2026-08-20 | Explicitly not canonical. Useful e2e and override examples. McDoniel says e2e should usually hit a real test database, issue comment 2020-12-03. Practitioner. |
| nest-lab Redis throttler storage | Jackie McDoniel | linked from official throttler docs | Community storage, Nest-documented as community. |

The four Trilon articles above were read in full. Keep their architectural advice labeled as practitioner opinion unless an official Nest source states the same rule.

## Intentionally unused

Generic "Top 20 NestJS best practices" listicles, Medium remixes of the cats tutorial, and vendor APM tutorials that are not OpenTelemetry contrib or Nest recipes.
