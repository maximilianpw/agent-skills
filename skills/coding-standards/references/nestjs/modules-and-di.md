# Modules and dependency injection

## Feature modules are ownership boundaries

Group a capability's controllers and providers in a feature module. Import that module from its consumer. A small application may have only `AppModule`; split once a capability has its own behavior or dependencies.

A provider is private to its declaring module unless exported. To share one instance:

1. Declare the provider in its owning module.
2. Export it from that module.
3. Import the owning module in each consumer.

Registering the same provider class in several modules creates several instances and can split caches or mutable state. Re-export an imported module when a facade module intentionally exposes its complete API.

Treat `exports` as the module public API. Export only what consumers use.

## Global and dynamic modules

Use `@Global()` or `global: true` only for infrastructure that belongs throughout the application, such as configuration registered once at the root. Explicit feature imports keep ownership visible. Nest's documentation warns against making every provider global.

Use a dynamic module when consumers supply registration options. Follow the repository's `forRoot` or `register` convention and provide an async variant for options that require DI. Prefer `ConfigurableModuleBuilder` over duplicating sync and async option plumbing.

A dynamic module must return `module: ThisModule`. In Nest 11, dynamic module identity uses object references rather than predictable option hashes. Assign a registration to a variable and reuse it when consumers must share the same dynamic module instance. The `deep-hash` module ID algorithm is a compatibility option, not the default.

## Provider tokens and constructors

Prefer constructor injection.

- Inject classes and abstract classes by type.
- Use `@Inject(TOKEN)` for symbol or string tokens.
- Prefer exported `Symbol` tokens for library-facing interfaces to avoid string collisions.
- Keep shared tokens in a plainly named constants or tokens file.
- Use `useValue` for constants and test doubles, `useClass` for an alternate implementation, `useFactory` for dependency-aware construction, and `useExisting` for aliases.

TypeScript interfaces cannot be DTOs or DI tokens because compilation erases them. An abstract class can be a token because it exists at runtime.

Property injection is a narrow escape hatch for inheritance that makes constructor forwarding impractical. Constructors keep dependencies visible and make isolated tests straightforward.

## Scope

`Scope.DEFAULT` is singleton scope and Nest's recommended default.

- Request scope creates an instance per request and bubbles upward. A singleton that injects a request-scoped provider becomes request-scoped.
- Transient scope creates an instance per consumer and does not bubble in the same way.
- Gateways, Passport strategies, cron controllers, and other process-owned components must remain singletons.
- Durable providers are for a deliberately shared DI subtree, such as a bounded tenant set. They are not a general replacement for singleton scope.

Before adding request scope, identify the value that must vary and every provider that will inherit the scope. Prefer an explicit method argument or AsyncLocalStorage for cross-cutting request context when either preserves singleton providers.

Lifecycle hooks do not run for request-scoped providers.

## Cycles and runtime lookup

Remove circular dependencies by correcting ownership, extracting shared behavior, or moving a shared type before reaching for framework escape hatches.

If a real bidirectional dependency remains, use `forwardRef(() => Other)` on both sides of the provider or module relationship. Construction order is indeterminate. Request-scoped circular graphs have known undefined-dependency failure modes.

Use `ModuleRef` for framework cases that constructor injection cannot express:

- `get()` retrieves static providers and cannot retrieve request- or transient-scoped providers.
- `resolve()` creates or joins a scoped DI subtree. Pass a `ContextId` when resolutions must share one subtree.
- `create()` instantiates a class that was not registered as a provider.

Nest documents `ModuleRef` for dynamic resolution and cases constructors cannot express, rather than as the application's default DI API. Constructor injection keeps routine collaborators explicit.

## Global enhancers with DI

Register DI-dependent global behavior from a module:

```typescript
providers: [
  AppAuthGuard,
  { provide: APP_GUARD, useExisting: AppAuthGuard },
]
```

The same pattern applies to `APP_PIPE`, `APP_INTERCEPTOR`, and `APP_FILTER`. `app.useGlobal*()` runs outside the module graph, so Nest cannot inject dependencies into instances created there. `useExisting` also makes the concrete enhancer token overrideable in tests.

## Sources

- NestJS, [Modules](https://docs.nestjs.com/modules)
- NestJS, [Custom providers](https://docs.nestjs.com/fundamentals/custom-providers)
- NestJS, [Dynamic modules](https://docs.nestjs.com/fundamentals/dynamic-modules)
- NestJS, [Injection scopes](https://docs.nestjs.com/fundamentals/injection-scopes)
- NestJS, [Circular dependency](https://docs.nestjs.com/fundamentals/circular-dependency)
- NestJS, [Module reference](https://docs.nestjs.com/fundamentals/module-ref)
- NestJS, [Migration guide](https://docs.nestjs.com/migration-guide)
