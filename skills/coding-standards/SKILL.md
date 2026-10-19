---
name: coding-standards
description: Engineering standards for implementing, refactoring, or reviewing non-trivial code. Covers types, boundaries, errors, file layout, comments, and tests, with conditional TypeScript, Effect/Alchemy, React/TanStack/Vite, and NestJS guidance. Use before adding type escapes or moving code.
license: See ATTRIBUTION.md
---

# Coding standards

One entry point, with references selected by the changed behavior. Apply explicit task requirements and repository policy first, then compatible local conventions; these standards supply defaults. Framework references specialize the shared rules only for that framework. Keep unrelated code unchanged.

Working agreements, engineering judgment, permissions, stack defaults, and execution gates belong to the global and repository `AGENTS.md`, not a second policy here.

## Establish the change

Inspect the affected package, installed versions, compiler/lint configuration, nearby code, and tests. Trace the changed operation from input through state, failures, side effects, and caller-visible results. Identify which runtime and module own each concern before adding an abstraction.

Define the caller-facing input, output, failures, and dependencies first. Reuse an existing owner when it fits.

## Read only the matching references

Load each matching reference once. Follow its conditional links only when their trigger applies; do not read the whole tree.

### Shared concerns

- [File layout and naming](references/file-layout.md): writing or substantially changing code, naming files, or organizing test support.
- [Safe restructures](references/restructuring.md): moving, renaming, or merging files.
- [Comments and documentation](references/comments-and-docs.md): adding or changing comments, docstrings, or docs.
- [Boundaries and ownership](references/boundaries.md): external data, dependencies, package boundaries, configuration, persistence, security, or side effects.
- [Failures and async work](references/failures.md): errors, absence, concurrency, cancellation, retries, or resource cleanup.
- [Public errors](references/public-errors.md): failures reaching HTTP/RPC, CLI, or SDK callers.
- [API contracts](references/api-contracts.md): HTTP routes, schemas, or generated OpenAPI.
- [Testing](references/testing.md): behavior or public-contract changes.

Use the repository's language and decoder library. TypeScript examples in shared references illustrate the contract, not a requirement to adopt TypeScript.

### Language and framework branches

- [TypeScript](references/typescript.md): TypeScript types, signatures, narrowing, assertions, or compiler configuration. Read before adding `any`, casts, or non-null assertions.
- [Effect and Alchemy](references/effect.md): Effect Schema, services, Layers, error channels, resource ownership, streams, or Alchemy runtimes. Also read TypeScript when its trigger applies.
- [React](references/react.md): components, Hooks, UI state, forms, accessibility, routing, or React tests, including TanStack and Vite.
- [NestJS](references/nestjs.md): modules, DI, controllers, DTOs, lifecycle, transports, or Nest tests.

## Complete the behavior

Implement each traced path through its owner, including recovery, cleanup, authorization, and cancellation where applicable. Validate untrusted data at its boundary; a typed client is not runtime proof. Keep server-only capabilities out of client-reachable code and package-private code behind public entrypoints.

Update vendored code only through its documented upstream workflow; preserve explicit local-adaptation policies. Ship custom lint rules with colocated passing and failing tests.

## Review the result

Check the final diff against every applicable loaded rule. Confirm that public behavior, failure semantics, type inference, runtime boundaries, and side-effect order remain intentional. Remove comments that only restate names, types, errors, or adjacent code.

Use the verification gates in `AGENTS.md`; fix failures caused by the change and report unverified behavior with concrete evidence or a blocker. For UI changes, verify semantics, labels, keyboard behavior, and focus, plus automated accessibility checks where the project has them.
