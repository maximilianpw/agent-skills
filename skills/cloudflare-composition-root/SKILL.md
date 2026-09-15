---
name: cloudflare-composition-root
description: Compose Cloudflare Workers, Durable Objects, Queues, scheduled handlers, and binding-backed services without leaking raw runtime capabilities into application code. Use when adding or refactoring Cloudflare bindings, entrypoints, runtime lifetimes, or D1, R2, KV, Queue, Durable Object, Workflow, or service-binding integration.
---

# Cloudflare Composition Roots

Treat every Cloudflare runtime surface as a composition root: turn raw platform capabilities into application-owned dependencies, assemble the runtime, and invoke behavior through narrow interfaces.

```text
Cloudflare entrypoint
  -> configuration and invocation context
  -> binding adapters
  -> application services
  -> protocol result
```

For Effect or Alchemy code, also read and apply the `effect-standards` skill, especially its Alchemy, service, resource-lifetime, error, and testing references. This skill owns the Cloudflare-specific boundary audit; `effect-standards` owns the Effect implementation shape.

## 1. Classify the runtime surface

Identify every affected surface independently:

- fetch Worker or framework adapter;
- `WorkerEntrypoint` or service binding;
- Durable Object constructor and each invocation method;
- Queue producer or consumer;
- scheduled or alarm handler;
- Workflow entrypoint;
- Workers Assets or SSR host;
- local Wrangler, test runtime, and Alchemy composition.

Trace each surface from raw bindings through every effect to its externally visible result. Record configuration, parsing, errors, retries, tracing, detached work, serialization, and resource lifetime before moving a boundary.

**Complete when:** every affected entrypoint, binding, side effect, failure policy, and lifetime has an owner.

## 2. Keep raw Cloudflare capabilities at the edge

Raw `Env`, `ExecutionContext`, framework contexts, binding names, and generated Worker configuration types belong only in:

- runtime entrypoints and composition roots;
- binding adapters that directly perform Cloudflare I/O;
- unavoidable platform class declarations such as `DurableObject<Env>`.

An adapter accepts the smallest capability it needs—such as `D1Database`, `R2Bucket`, `KVNamespace`, `Queue`, or `DurableObjectNamespace`—not the complete `Env`. Application services receive domain-shaped interfaces, parsed configuration, and exact dependencies.

Do not rename `Env` to `Dependencies`. Each dependency object exposes only capabilities used by that consumer. Keep key formats, SQL, object metadata, pagination tokens, TTLs, and Cloudflare response parsing inside the owning adapter.

A Durable Object class may require `Env` at its platform boundary. Resolve its bindings there, then keep domain and application operations independent of the complete environment.

**Complete when:** inner modules expose no raw binding names or platform-wide environment objects, and each adapter owns one coherent external role.

## 3. Compose each surface separately

Do not assume one dependency graph or lifetime fits every Cloudflare surface. Compose Workers, Durable Objects, queue consumers, cron handlers, alarms, and Workflows independently.

At each composition root:

1. Parse configuration and boundary input.
2. Establish correlation, tracing, and safe diagnostic context.
3. Resolve raw bindings.
4. Construct binding adapters from the smallest capabilities.
5. Assemble exact application dependencies or provide the owning Effect Layers.
6. Invoke the operation.
7. translate typed results and expected failures into the external protocol.
8. Hand detached work to an explicit owner rather than leaking `ExecutionContext` inward.

Choose lifetimes from the actual platform contract:

- reuse immutable services only when their clients and state are safe across invocations;
- construct invocation-owned clients inside the invocation that performs their I/O;
- keep Durable Object storage-backed resources in the runtime phase, not Alchemy planning;
- never let a canonical key or cache extend a stub/client beyond its valid I/O context.

**Complete when:** every service, Layer, client, cache, and resource is acquired and released by the runtime context that owns it.

## 4. Preserve application ownership

Application services own sequencing, authorization, fallback, retry, idempotency, and best-effort policy. Binding adapters own Cloudflare mechanics and translate platform failures precisely enough for the application to choose policy.

Parse external and stored values before they enter inner code. Treat D1 rows, KV values, R2 metadata, Queue messages, Durable Object storage, service-binding responses, and Workflow state as boundary representations rather than trusted domain values.

Introduce a dynamic factory only when information required for construction appears after composition, such as an account selected after authentication. The factory accepts application values and capabilities, not `Env` or raw binding names.

For an existing codebase, move the seam outward incrementally:

1. Capture current behavior with tests at the existing public seam.
2. Define the narrow capability from operations the consumer already uses.
3. Put the raw binding behind an adapter without changing policy.
4. Replace the direct consumer's platform dependency with the capability.
5. Move adapter construction outward one caller at a time.
6. Remove the old `Env` or binding path after its final caller moves.

## 5. Verify the Cloudflare boundary

Run focused behavior, adapter, and runtime tests. Use the representative local Cloudflare runtime when serialization, storage, transactions, Durable Object behavior, or binding protocols matter. Keep production deployment and resource changes behind explicit user authorization.

Search the changed source for leakage, tailoring paths and symbols to the repository:

```bash
rg 'Env|ExecutionContext|KVNamespace|R2Bucket|D1Database|DurableObjectNamespace|Queue' src packages
rg 'context\.env|this\.env|env\.[A-Z][A-Z0-9_]+' src packages
rg 'cloudflare:workers|wrangler|Cloudflare\.(Worker|DurableObject|Queues|Workflow)' src packages
```

Classify every match as one of:

- composition root;
- binding adapter;
- unavoidable framework/platform declaration;
- violation to move outward.

**Complete when:** every raw platform reference is classified and permitted; each changed surface has behavior and failure-path evidence; binding adapters use the smallest capabilities; invocation lifetimes are correct; and no application or domain module receives the complete Cloudflare environment.
