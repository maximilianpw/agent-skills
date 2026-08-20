# Validation and serialization

## DTOs must exist at runtime

Use classes for request bodies, query objects, and parameter objects when Nest needs runtime metadata. Import DTO classes as values. TypeScript interfaces, type-only imports, generic arrays, and erased unions do not give `ValidationPipe` a runtime constructor.

Decorate every validated field. Keep validation at the transport boundary so providers receive the intended input shape. Apply stronger domain parsing inside the owning application boundary when HTTP validation alone cannot establish the domain invariant.

## Global validation

Install `class-validator` and `class-transformer` when using Nest's standard `ValidationPipe`. Bind the pipe globally and enable `whitelist: true` so properties without validation metadata do not pass through.

```typescript
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
  }),
);
```

Use `forbidNonWhitelisted: true` when extra properties should fail with 400 rather than be stripped. Choose `disableErrorMessages` from the product's production error policy. Register the pipe with `APP_PIPE` when it needs injected dependencies.

A class with no validation decorators has no whitelist metadata. Decorate accepted fields rather than treating an empty DTO as validated.

## Transformation is an explicit choice

`transform: true` instantiates DTO classes and enables primitive conversion for decorated route inputs. That can hide string-to-number or string-to-boolean conversion across the whole application. Enable it when the application relies on that behavior.

Prefer local built-in pipes when conversion should be visible at the parameter:

- `ParseIntPipe`
- `ParseBoolPipe`
- `ParseUUIDPipe`
- `ParseArrayPipe`
- `ParseEnumPipe`

Parse pipes reject `undefined`. Put `DefaultValuePipe` before a parse pipe for an optional parameter with a default.

Nested object conversion follows `class-transformer` metadata and options. `enableImplicitConversion` is not automatic merely because a global `ValidationPipe` exists. Use `plainToInstance`; `plainToClass` is deprecated.

## The `forbidUnknownValues` mismatch

`class-validator` 0.14 and later defaults `forbidUnknownValues` to `true`, which rejects objects for which it finds no validation metadata. Nest 11's `ValidationPipe` explicitly defaults that option to `false` for compatibility.

Do not copy assumptions between raw `validate()` calls and `ValidationPipe`. Prefer decorated DTOs plus whitelisting. When unknown-value validation fails, find the missing or mismatched metadata before changing the flag.

## Mapped types

Import mapped-type helpers from the package that owns the active metadata system:

- plain HTTP: `@nestjs/mapped-types`;
- OpenAPI: `@nestjs/swagger`;
- GraphQL: `@nestjs/graphql`.

Mixing these packages can omit or duplicate metadata. Use `PartialType`, `PickType`, `OmitType`, and `IntersectionType` rather than manually copying decorated fields when the derived DTO has the same semantic relationship.

## Response serialization

`ClassSerializerInterceptor` uses `class-transformer`'s `instanceToPlain()`.

- Use `@Exclude()` and exposure groups or versions only on classes that represent the response policy.
- Return class instances when relying on class metadata.
- If providers return plain objects, use `@SerializeOptions({ type: ResponseDto })` where supported so Nest knows the target class.
- Do not wrap an instance in an arbitrary plain object and assume nested serialization will apply.
- `StreamableFile` bypasses class serialization.

Nest documentation sometimes puts serialization decorators on ORM entities. That is valid Nest behavior but couples persistence and HTTP policy. Use a response DTO when the repository keeps those boundaries separate.

Never rely on serialization alone to protect a secret that should not have reached the response model.

## Sources

- NestJS, [Validation](https://docs.nestjs.com/techniques/validation)
- NestJS, [Pipes](https://docs.nestjs.com/pipes)
- NestJS, [Serialization](https://docs.nestjs.com/techniques/serialization)
- NestJS, [OpenAPI mapped types](https://docs.nestjs.com/openapi/mapped-types)
- class-validator, [`forbidUnknownValues` change](https://github.com/typestack/class-validator/pull/1798)
- NestJS, [`ValidationPipe` source](https://github.com/nestjs/nest/blob/master/packages/common/pipes/validation.pipe.ts)
