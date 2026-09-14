# Local Cloudflare project survey

**Research record.** Evidence for whether a standalone Cloudflare composition-root skill is justified. This file is not agent instructions.

**Updated 2026-09-14.** Survey of `/Users/max-vev/Local` source trees. Primary sources are package manifests, Wrangler/Alchemy configs, and application source. Secondary write-ups were not used except the already-local [`dmmulroy-upstream-skills.md`](dmmulroy-upstream-skills.md), cited only for the prior skill-placement verdict.

## Recommendation

Do **not** add a standalone `cloudflare-composition-root` skill.

The local Cloudflare backends that actually compose bindings are Effect + Alchemy (`rbi`, `rivierabox`, `repoship`). That work already belongs in `effect-standards`, especially [`effect-alchemy.md`](../skills/effect-standards/references/effect-alchemy.md). The remaining Workers are either tiny `fetch` adapters (`plannotator`), static/SSR hosting (`portfolio`, `diffy`), or a raw Wrangler Durable Object product (`cloudflare-os`) whose house style is `DurableObject<Env>`, not Hono.

**Hono is not used as a Cloudflare Worker framework in any local project.** The only real Hono app is `superlocal` on Bun/Node with SQLite. A Hono-centric composition-root skill would not fire on the current backends and would compete with `effect-standards` on Alchemy work.

Mine later, into existing references, not a new skill:

1. Binding adapters take the smallest platform type (`D1Database`, `R2Bucket`, `KVNamespace`), never the whole `Env`.
2. Each Worker, Durable Object, queue consumer, and cron is its own composition root.
3. After a change, search for raw runtime types and classify every hit.

Those bullets already sit in [`typescript-standards/references/boundaries.md`](../skills/typescript-standards/references/boundaries.md) (narrow capabilities, composition root) and [`effect-standards`](../skills/effect-standards/SKILL.md) (Alchemy two-phase Workers, DOs, Workflows, bindings). The prior Mulroy survey reached the same placement verdict.

## Scope and method

Question: which local projects use Cloudflare technologies, how they compose, whether Hono is real, and whether guidance belongs in a new skill or in `effect-standards` / `typescript-standards`.

Walked every top-level directory under `/Users/max-vev/Local`. Evidence classes:

- Config: `wrangler.toml`, `wrangler.jsonc`, `alchemy*.run.ts`
- Manifests: `wrangler`, `alchemy`, `@cloudflare/*`, `@effect/sql-d1`, `hono`
- Source: `cloudflare:workers`, `extends DurableObject`, `Cloudflare.Worker`, D1/R2/KV/Queue/Workflow types, `from 'hono'`, `c.env`

Excluded from deep source: `node_modules`, `.git`, `dist`, `build`, `.next`, `.turbo`, `.cache`, `.wrangler`, `.alchemy`, `coverage`, `rivierabox/.delta` worktrees, `repoship/.repos` (vendored Effect), dated `rbi-*` checkouts (same app as `rbi`), `overnight/repoship-slice05-20260823` (dated `repoship` copy). Those copies are listed only as snapshots.

No Cloudflare Pages project was found (`pages_build_output_dir`, `wrangler pages`, `@cloudflare/pages` all empty in the Worker repos). Static hosting uses Workers Assets.

No Cloudflare Workflows source (`extends WorkflowEntrypoint`, `cloudflare:workflows`) exists outside generated `worker-configuration.d.ts`.

## Hono

| Project | Hono in source? | On Cloudflare? |
| --- | --- | --- |
| `rbi` | No | — |
| `rivierabox` / `rivierabox-rba` | No (lockfile only, via Prisma) | — |
| `repoship` | No | — |
| `cloudflare-os` | Sample string in `packages/workshop-frontend/src/data/chat.ts` only | No |
| `plannotator` | No | — |
| `diffy` | No | — |
| `portfolio` | No | — |
| `stocket` family | No (`hono` is a root `overrides` pin, no imports) | — |
| `superlocal` | Yes: `packages/inbox-sdk/src/http.ts`, `server/index.ts` | No: Bun + `bun:sqlite` |
| `vev` | Transitive lockfile only | No |

There is no `c.env` / Hono `context.env` usage in real Worker code. The gadgets chat sample is the only `c.env` hit, and it is example file content, not a running Worker.

# Projects that use Cloudflare

Canonical trees first. Snapshots are named at the end of each section.

## 1. `rbi` — Effect + Alchemy Website Worker (D1 + R2)

**Path:** `/Users/max-vev/Local/rbi`
**Remote:** `git@github.com:maximilianpw/rbi-landing.git` @ `c119988`

**Architecture.** TanStack Start SSR Worker deployed as `Cloudflare.Website.Vite`. Request-scoped Effect CMS runtime. Not an Alchemy Effect-native `Cloudflare.Worker` constructor. Local `wrangler.jsonc` is Vite-dev only; production bindings are Alchemy.

**Evidence.**

- `/Users/max-vev/Local/rbi/package.json` — `@effect/sql-d1`, `alchemy@2.0.0-beta.72`, `@cloudflare/vite-plugin`, `wrangler`, `vitest.cloudflare.config.ts`
- `/Users/max-vev/Local/rbi/wrangler.jsonc` — Worker `src/server.ts`, `CMS_DB` D1, `CMS_ASSETS` R2, `nodejs_compat`
- `/Users/max-vev/Local/rbi/alchemy.run.ts` — `Cloudflare.D1.Database('CmsDatabase')`, `Cloudflare.R2.Bucket('CmsAssets')`, `Cloudflare.Website.Vite('Website', { env: { CMS_DB, CMS_ASSETS, ... } })`
- Also: `alchemy.data.run.ts`, `alchemy.website.run.ts`, `alchemy.qa.run.ts`, `alchemy.rehearsal.run.ts`
- `/Users/max-vev/Local/rbi/src/cloudflare/env.ts` — deferred getters over `cloudflare:workers` (TanStack-dev-safe)
- `/Users/max-vev/Local/rbi/src/server/cms-runtime.ts` — `D1Client.layer({ db })` plus D1/R2 adapters; native types stay in the request composition root
- `/Users/max-vev/Local/rbi/src/cms/adapters/r2/asset-object-store-r2.ts` — R2 adapter

**Used:** Workers, Wrangler (local), Alchemy, D1, R2, `cloudflare:workers` env, Effect.
**Not used:** Hono, Durable Objects, Queues, Workflows, KV, Pages, service bindings.

**Skill.** `effect-standards`. Already matches the Alchemy Website + request-scoped Layer pattern. A standalone composition-root skill would duplicate `cms-runtime.ts`.

**Snapshots (do not treat as separate products):** `rbi-sync-20260912-112459`, `rbi-qa-20260905`, `rbi-qa-auth-20260905`, `rbi-production-review-20260905`, `rbi-production-release-eb79017`. Same `alchemy.run.ts` / `wrangler.jsonc` / `src/cloudflare/env.ts` shape.

## 2. `rivierabox` — Effect + Alchemy Website Worker (D1 + R2)

**Path:** `/Users/max-vev/Local/rivierabox`
**Remote:** `https://github.com/maximilianpw/rivierabox.git` @ `d55f6cb`

**Architecture.** Same family as RBI: TanStack Start + `Cloudflare.Website.Vite`, deferred `cloudflare:workers` env, Effect Layers that accept `{ database: D1Database; bucket: R2Bucket }`. Data stack is separate from the website stack.

**Evidence.**

- `/Users/max-vev/Local/rivierabox/package.json` — `@effect/sql-d1@4.0.0-rc.112`, `alchemy@2.0.0-beta.74`, `@cloudflare/vite-plugin`, `@cloudflare/vitest-pool-workers`, `wrangler@4.127.1`
- `/Users/max-vev/Local/rivierabox/wrangler.jsonc` — local Worker `apps/web/src/server.ts`, D1 `DB`, R2 `FILES`
- `/Users/max-vev/Local/rivierabox/alchemy.data.run.ts` — `Cloudflare.D1.Database('Database')`, `Cloudflare.R2.Bucket('Files')`
- `/Users/max-vev/Local/rivierabox/alchemy.app.run.ts` — `Cloudflare.Website.Vite` with `DB`/`FILES` refs plus Clerk/Zoho env
- Also: `alchemy.private-pilot.app.run.ts`, `alchemy.private-pilot.data.run.ts`, `alchemy.inspect.run.ts`
- `/Users/max-vev/Local/rivierabox/packages/backend/src/platform/cloudflare/env.ts` — deferred `cloudflare.env.DB` / `FILES`
- `/Users/max-vev/Local/rivierabox/packages/backend/src/brochures/brochure-runtime.ts` — `brochureLayer(bindings: { database: D1Database; bucket: R2Bucket })`
- Integration tests import `env` from `cloudflare:workers` (for example `test/root-ssr.integ.test.ts`)

**Used:** Workers, Wrangler (local), Alchemy, D1, R2, Effect, `cloudflare:workers`.
**Not used:** Hono (Prisma lockfile only), Durable Objects, Queues, Workflows, KV, Pages.

**Skill.** `effect-standards`. Same composition as RBI; adapters already take the smallest binding types.

**Sibling checkout:** `/Users/max-vev/Local/rivierabox-rba` is the same GitHub repo at `1fdf45e`, same `wrangler.jsonc` / Alchemy files. Not a second architecture.

## 3. `repoship` — Alchemy Effect Workers, Durable Objects, Queues, R2, D1, service bindings

**Path:** `/Users/max-vev/Local/repoship`

**Architecture.** Greenfield Cloudflare backend: private Alchemy Workers, SQLite Durable Objects as authority, queue consumers, R2 object stores, D1 for fleet locator, service bindings / `Cloudflare.Workers.Fetch`, `@cloudflare/sandbox`, plus a TanStack landing Worker in root `wrangler.jsonc` (deploy-disabled default; staging/production envs bind `WORKSPACE_USER_COMMANDS`).

**Evidence.**

- Root `/Users/max-vev/Local/repoship/wrangler.jsonc` — landing Worker, `services` binding `WORKSPACE_USER_COMMANDS`
- `/Users/max-vev/Local/repoship/package.json` — `@cloudflare/vite-plugin`, `wrangler`, `build:cloudflare`
- Worker packages with `alchemy.run.ts` and `alchemy@2.0.0-beta.72`:
  - `packages/application-state-worker`
  - `packages/workspace-state-worker`
  - `packages/build-coordinator-worker`
  - `packages/build-control-worker`
  - `packages/build-output-broker-worker`
  - `packages/release-publisher-worker`
  - `packages/release-control-worker`
  - `packages/fleet-operations-worker`
  - `experiments/platform-tour`
- `/Users/max-vev/Local/repoship/packages/application-state-worker/src/application-do/index.ts` — `ApplicationDO extends Cloudflare.DurableObject`
- `/Users/max-vev/Local/repoship/packages/application-state-worker/src/recovery-fence-do/index.ts` — `RecoveryFenceDO`
- `/Users/max-vev/Local/repoship/packages/application-state-worker/src/application-state-worker.ts` — `Cloudflare.Worker` hosting those DOs, `Cloudflare.Queues.WriteQueueBinding`
- `/Users/max-vev/Local/repoship/packages/build-coordinator-worker/src/build-coordinator-worker.ts` — `Cloudflare.Queues.consumeQueueMessages`
- `/Users/max-vev/Local/repoship/packages/release-publisher-worker/src/release-publisher-worker.ts` — queue consume + sandbox
- `/Users/max-vev/Local/repoship/packages/build-output-broker-worker/src/resources.ts` — `Cloudflare.R2.Bucket('BuildOutputBucket')`
- `/Users/max-vev/Local/repoship/packages/fleet-operations-worker/src/resources.ts` — `Cloudflare.D1.Database` (`FleetLocatorDatabase`), R2 backup bucket, cron workers

**Used:** Workers, Wrangler, Alchemy, Durable Objects, Queues, R2, D1, service bindings, Sandbox, crons, Effect.
**Not used:** Hono, KV, Workflows, Pages.

**Skill.** `effect-standards` / `effect-alchemy.md`. This is the strongest local match for Alchemy two-phase Workers and Durable Objects. A Hono composition-root skill would fight the `Cloudflare.Worker` / Layer style.

**Snapshot:** `/Users/max-vev/Local/overnight/repoship-slice05-20260823`.

## 4. `cloudflare-os` — raw Wrangler Workers + Durable Objects (Gadgets)

**Path:** `/Users/max-vev/Local/cloudflare-os`
**Package name:** `gadgets`

**Architecture.** Multi-Worker product. Public `router` Worker fans out by `GATEKEEPER_*` service bindings. Workshop backend owns SQLite Durable Objects, KV, R2, Browser Rendering, worker loaders. Each gatekeeper is its own Wrangler Worker with SQLite DO classes. No Alchemy. No Effect. No Hono in running code. `Env` is the Durable Object generic.

**Evidence.**

- `/Users/max-vev/Local/cloudflare-os/wrangler.jsonc` — dev router `packages/router/src/index.ts`, service binding `WORKSHOP_BACKEND`
- `/Users/max-vev/Local/cloudflare-os/packages/router/src/index.ts` — `ExportedHandler<Env>`, scans `GATEKEEPER_*`, `env.ASSETS` / `env.WORKSHOP_BACKEND.fetch`
- `/Users/max-vev/Local/cloudflare-os/packages/workshop-backend/wrangler.jsonc` — KV `BLUEPRINTS`/`AVATARS`, R2 `BLUEPRINT_CONTENT`, Browser binding, SQLite DO migrations (`UserDurableObject`, `OverseerDurableObject`, `AdminSettings`, `PendingLogin`)
- DO classes: `packages/workshop-backend/src/user.ts`, `src/overseer.ts`, `src/admin-settings.ts`, `src/auth/login-flow.ts`, `src/agent.ts`
- Gatekeeper Wrangler configs, for example `/Users/max-vev/Local/cloudflare-os/packages/gatekeeper-github/wrangler.jsonc` (`UserAccount`, `GitHubGatekeeperImpl`)
- Many `export class X extends DurableObject<Env>` under `packages/gatekeeper-*`
- `/Users/max-vev/Local/cloudflare-os/packages/gatekeeper-context/wrangler.jsonc` — KV `CONTEXT_COLLECTIONS`
- `/Users/max-vev/Local/cloudflare-os/packages/workshop-frontend/src/data/chat.ts` — Hono sample **string**, not an import

**Used:** Workers, Wrangler, Durable Objects, KV, R2, service bindings, Browser Rendering, Workers Assets (router SPA).
**Not used:** Alchemy, Effect, Hono (runtime), D1, Queues, Workflows, Pages.

**Skill.** Not a standalone composition-root skill. The codebase intentionally threads `Env` into Durable Objects. Forcing Mulroy's "inner code never sees `Env`" rule would fight this product. If this tree is ever edited under personal standards, use `typescript-standards` boundaries (parse at the edge, keep vendor types in adapters) and do not pretend it is an Effect/Alchemy app.

## 5. `plannotator` — tiny dual-target Workers (KV + D1)

**Path:** `/Users/max-vev/Local/plannotator`

Two small services. Core handlers take a store interface. Cloudflare is one target among others (paste also has `targets/bun.ts` with `FsPasteStore`).

**Paste (KV).**

- `/Users/max-vev/Local/plannotator/apps/paste-service/wrangler.toml` — Worker `targets/cloudflare.ts`, KV `PASTE_KV`
- `/Users/max-vev/Local/plannotator/apps/paste-service/targets/cloudflare.ts` — `fetch(request, env)`, constructs `KvPasteStore(env.PASTE_KV)`, calls `handleRequest`
- `/Users/max-vev/Local/plannotator/apps/paste-service/stores/kv.ts` — `KVNamespace` stays in the store

**Waitlist (D1).**

- `/Users/max-vev/Local/plannotator/apps/waitlist-service/wrangler.toml` — Worker `targets/cloudflare.ts`, D1 `WAITLIST_DB`
- `/Users/max-vev/Local/plannotator/apps/waitlist-service/targets/cloudflare.ts` — `D1WaitlistStore(env.WAITLIST_DB)` plus CORS/Turnstile from `env`
- `/Users/max-vev/Local/plannotator/apps/waitlist-service/stores/d1.ts` — D1 adapter
- `package.json` scripts: `wrangler d1 create/execute`

**Used:** Workers, Wrangler, KV, D1.
**Not used:** Hono, Alchemy, Effect, Durable Objects, Queues, Workflows, R2, Pages.

**Skill.** `typescript-standards`. This already *is* a composition root: `fetch` builds a store from one binding and inner `core/handler.ts` never sees `Env`. Too small to justify a Cloudflare skill.

## 6. `diffy` — TanStack Start hosted on Workers; Convex is the backend

**Path:** `/Users/max-vev/Local/diffy/apps/web`

**Evidence.**

- `/Users/max-vev/Local/diffy/apps/web/wrangler.jsonc` — Worker name `diffy`, `main: "@tanstack/react-start/server-entry"`, `nodejs_compat`
- `/Users/max-vev/Local/diffy/apps/web/vite.config.ts` — `cloudflare({ viteEnvironment: { name: "ssr" } })`
- `/Users/max-vev/Local/diffy/apps/web/package.json` — `@cloudflare/vite-plugin`, `wrangler`, `deploy: pnpm run build && wrangler deploy`; app deps include `convex`

**Used:** Workers as SSR host.
**Not used:** Bindings, D1/R2/KV/DO/Queues, Hono, Alchemy, Effect.

**Skill.** `react-standards` / `typescript-standards` for the UI. Cloudflare is a deploy target, not a composition problem.

## 7. `portfolio` — static Workers Assets

**Path:** `/Users/max-vev/Local/portfolio`

**Evidence.**

- `/Users/max-vev/Local/portfolio/wrangler.jsonc` — `assets.directory: "./dist"`, `not_found_handling: "404-page"`, no `main`
- `/Users/max-vev/Local/portfolio/package.json` — Astro build, `wrangler deploy`

**Used:** Wrangler + Workers Assets.
**Not used:** Bindings, Hono, Alchemy, Effect.

**Skill.** None. Hosting only.

## 8. `stocket` family — R2 + DNS/CDN, not Workers

**Path:** `/Users/max-vev/Local/stocket` (same Terraform/R2 pattern in `stocket-license` and herdr/meta copies)

**Evidence.**

- `/Users/max-vev/Local/stocket/ops/recovery/object-storage.tf` — `cloudflare_r2_bucket` resources (`primary_photos`, `database_recovery`, …)
- `/Users/max-vev/Local/stocket/apps/api/src/recovery/reconcile-photos.ts` — S3-compatible endpoint `*.r2.cloudflarestorage.com`
- `/Users/max-vev/Local/stocket/ops/infrastructure/dns.tf`, origin certs, Cloudflare zone constraints in `compute.tf`
- Root `package.json` pins `"hono": "4.13.2"` under `overrides` only; no `from 'hono'` in source
- No `wrangler` / `alchemy` / Worker entry

**Used:** R2 via S3 API, Cloudflare DNS/TLS/firewall.
**Not used:** Workers, Wrangler, Hono, Alchemy, D1, KV, Durable Objects.

**Skill.** Not a Cloudflare Worker skill. Object-store adapters belong with the existing Effect/TypeScript persistence rules if those files change.

## 9. `vev` — Cloudflare DNS only

**Evidence.** `/Users/max-vev/Local/vev/infrastructure/dns.tf` (`cloudflare_record`), `variables.tf` (`cloudflare_api_token`, `cloudflare_zone_id`). Lockfiles mention `@cloudflare/workers-types` as a transitive optional peer. No Workers app.

**Skill.** None.

# Non-Cloudflare (checked)

No Wrangler/Alchemy/Workers/`cloudflare:workers` app in: `loggle`, `fleet`, `leerr`, `facom`, `discord-inventory`, `reported`, `rmus`, `maxcel`, `vev-cli`, `workshops`, `homebrew-tap`, `bitchcsharp`, `nixbench`, `license-prs`, `jj`, `fast-check`, `t3code` (icon manifest only: `wrangler.toml` / `alchemy.run.ts` file icons), `ynov` (`.gitignore` lists `.wrangler`), `agent-skills` (skill text only).

`superlocal` uses Hono and mentions Cloudflare Email Service as **planned** in `README.md`. Runtime is Bun + SQLite, not Workers.

# Skill placement

| If the work is… | Load |
| --- | --- |
| Alchemy Worker, DO, queue, cron, binding Layer, two-phase constructor (`rbi`, `rivierabox`, `repoship`) | `effect-standards` → `effect-alchemy.md` |
| Tiny `fetch` + store adapter (`plannotator`) or future non-Effect Worker | `typescript-standards` → `boundaries.md` |
| TanStack/Vite UI on a Worker host (`diffy`, RBI/Riviera Box UI) | `react-standards` |
| Raw `DurableObject<Env>` product (`cloudflare-os`) | local repo conventions; do not overlay a Hono/Alchemy skill |
| R2-as-S3 / DNS (`stocket`, `vev`) | not a Worker composition problem |

**Standalone Cloudflare composition-root skill: no.** It would only become useful if a future personal backend is raw Hono on Workers *without* Alchemy. That is not the greenfield default in global `AGENTS.md` (Effect + Drizzle / Alchemy) and it is not present in this survey.
