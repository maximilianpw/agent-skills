---
name: typescript-standards
description: Pragmatic TypeScript standards for production code. Use when designing, implementing, refactoring, or reviewing non-trivial TypeScript; apply Effect guidance only where the affected package already uses Effect or the user requests it.
license: MIT
---

# TypeScript Standards

Build TypeScript that makes invalid data, recoverable errors, and side-effect ownership visible. Fit the repository before improving it: explicit task requirements and repository rules govern, established local conventions follow, and this skill supplies defaults where the codebase is silent.

For trivial or mechanical edits, match the surrounding code and stop; that completes this workflow. Do not turn a focused task into a standards migration.

## Select the guidance branch

Inspect the nearest package manifest, TypeScript configuration, repository instructions, and affected imports before designing the change.

Use **standard TypeScript** by default. Load [`references/effect.md`](references/effect.md) only when:

- the affected package declares `effect` and the changed area already uses it; or
- the user explicitly asks to introduce or use Effect.

A dependency elsewhere in a monorepo is not enough. In a mixed repository, apply Effect conventions only inside the Effect-owned boundary. Do not introduce Effect into ordinary TypeScript merely because it is available or preferred in another project.

## Trace the changed behavior

Follow each caller-visible operation from input to result and side effect. Identify:

- trusted and untrusted inputs;
- outputs, ordinary absence, recoverable errors, and invariant violations;
- state transitions and persistence;
- external systems, configuration, time, randomness, and concurrency;
- the public interface and tests that observe the behavior.

Load the references that match the change:

- [`references/types.md`](references/types.md) for signatures, domain types, state models, assertions, exports, and compiler settings.
- [`references/failures.md`](references/failures.md) for absence, errors, promises, cancellation, retries, and resource cleanup.
- [`references/boundaries.md`](references/boundaries.md) for parsing, dependencies, services, adapters, persistence, configuration, security, and observability.
- [`references/testing.md`](references/testing.md) whenever behavior or a public contract changes.

## Design from the caller inward

Define or confirm the input, output, recoverable error, and dependency contract before implementation. Keep domain decisions independent of frameworks and providers. Put translation at the boundary that owns the external representation, and put sequencing policy in the module that owns the use case.

Prefer the smallest complete design. Reuse an existing owner when it fits; add an abstraction only when it removes meaningful complexity from callers or isolates a real boundary.

## Implement the complete behavior

Cover every traced path, including external translation, diagnostics, cleanup, and cancellation where applicable. Keep unrelated behavior unchanged. Preserve the repository's established approach unless the task explicitly includes migration.

## Verify

For non-trivial changes, before completion:

1. Confirm repository instructions, compiler options, lint rules, package versions, and nearby conventions were followed.
2. Confirm external data is parsed before domain use and provider/framework representations do not escape their owner.
3. Confirm every recoverable error and ordinary absence has an intentional caller-facing representation.
4. Confirm new assertions, abstractions, and dependency seams are necessary for the changed behavior.
5. Run the repository's smallest relevant typecheck, tests, and lint commands and report concrete failures rather than claiming unrun checks.
6. Name any deliberate deviation from these standards and why the repository or task requires it.
