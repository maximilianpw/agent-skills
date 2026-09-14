# Dillon Mulroy dotfiles: additional skills to adapt?

**Research record.** These findings compare [`dmmulroy/.dotfiles`](https://github.com/dmmulroy/.dotfiles) skills against this repository. This file is not agent instructions. It does not modify skills or manifests.

**Updated 2026-09-14.** Inspected public `main` at commit [`fcdf06013853c2e8e5718b620d3a2b481fbcedb9`](https://github.com/dmmulroy/.dotfiles/commit/fcdf06013853c2e8e5718b620d3a2b481fbcedb9) (`updates`, 2026-09-14 08:53:22 -0400). That commit only changed [`home/.agents/.skill-lock.json`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/.skill-lock.json). Skill bodies are the same as the current `main` tree.

## Recommendation

Do not pull any additional Mulroy skill into this repository now.

The two Mulroy skills this repo already tracks remain the right ones: [`coding-standards`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/coding-standards) as `effect-standards`, and [`write-discoverable-code`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/write-discoverable-code). Do not add a third copy of `coding-standards`.

The only first-party skill with substantive unique engineering guidance is [`cloudflare-composition-root`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/cloudflare-composition-root). Mine selected Hono/Workers leakage and exact-dependency rules into the existing TypeScript and Effect standards. Do not vendor it as a standalone skill: its examples are Promise/class composition, and this stack already owns Cloudflare composition through Effect/Alchemy.

Everything else is either a third-party copy that this repo refuses to vendor, already installed globally, already adapted from a better upstream, or out of this repository's reusable engineering scope.

**Working tree at write time.** HEAD is [`597573318a2fd045950ae47e5196b587e69ee096`](https://github.com/maximilianpw/agent-skills/commit/597573318a2fd045950ae47e5196b587e69ee096). Unrelated dirty work already present, and not edited here:

- modified `effect-standards` (including `ATTRIBUTION.md` pinned to this same Mulroy commit), `nestjs-standards/SKILL.md`, `project-verification/SKILL.md`, `update-upstream-skills/SKILL.md`, `upstream-skills.json`, `README.md`
- untracked `skills/code-review/`, `skills/grill-me/`, `skills/tdd/`, `skills/effect-standards/references/lint-and-policy.md`

Those files were not used as the source of truth for the gap analysis except to avoid colliding with an in-progress `effect-standards` sync.

## Scope and sources

Question: which skills in Dillon Mulroy's public dotfiles are worth adapting into `/Users/max-vev/Local/agent-skills`, beyond the two already inventoried in `upstream-skills.json`.

Primary sources, in order:

1. Public repo [`dmmulroy/.dotfiles`](https://github.com/dmmulroy/.dotfiles), default branch `main`, commit [`fcdf060`](https://github.com/dmmulroy/.dotfiles/commit/fcdf06013853c2e8e5718b620d3a2b481fbcedb9). GitHub license field is `null`. Sparse clone of that commit; skill tree listed from [`home/.agents/skills`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills).
2. Mulroy's [`AGENTS.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/AGENTS.md), [`README.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/README.md) (including the License section), and [`home/.agents/.skill-lock.json`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/.skill-lock.json).
3. This repo at HEAD: [`README.md`](../README.md), [`AGENTS.md`](../AGENTS.md), [`upstream-skills.json`](../upstream-skills.json), and committed skill entry points under [`skills/`](../skills/). Dirty uncommitted skill trees are called out, not treated as the comparison baseline.
4. The live consumer skill trees this machine already loads: `/Users/max-vev/.pi/agent/skills/` and `/Users/max-vev/.agents/skills/`. Those are installation state, not this repository, but they bound "is this missing from the stack."

Secondary write-ups were not used. GitHub's rendered README still omits `home/.agents/`; the skill tree is the authority.

Evaluation axes, applied to every candidate:

- **Unique guidance:** does the body teach a mechanism this stack does not already have?
- **Overlap:** local skills, plus global installs that already cover the same name.
- **Repository scope:** static, reusable engineering skills; no vendoring of third-party skill packages ([`AGENTS.md`](../AGENTS.md), [`README.md`](../README.md)).
- **Invocation reliability:** can a description fire on the intended branches without stealing Effect/TypeScript work or over-firing on "maybe use a subagent"?
- **Adaptation cost:** license, sibling-path rewrites, idiom clash with Effect, harness-specific CLIs.

# What the upstream tree is

Mulroy stows agent skills from `home/.agents/skills/` to `~/.agents/skills/`. [`AGENTS.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/AGENTS.md) forbids a second copy under `home/.pi/agent/skills/`. The tree is a personal mix of first-party skills and Skills-CLI installs recorded in `.skill-lock.json`.

At `fcdf060` there are **22 skill directories**. GitHub lists no root `LICENSE`. The only license file in the skill tree is [`cua-driver/LICENSE.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/cua-driver/LICENSE.md) (Cua AI, MIT). The README License section says the repository is for personal use and "Feel free to fork and adapt for your own needs." That is permission-shaped prose, not an SPDX license. This repo has already adapted two skills from that tree and recorded the missing license in `effect-standards` attribution.

## Inventory at `fcdf060`

First-party (absent from `.skill-lock.json`):

| Skill | Path | Tree SHA | Notes |
| --- | --- | --- | --- |
| `bro` | [`home/.agents/skills/bro`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/bro) | `53c3b2c5dc11fe0ee4156468da27505df9239dc6` | 267-byte user-invoked restatement |
| `cloudflare-composition-root` | [`home/.agents/skills/cloudflare-composition-root`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/cloudflare-composition-root) | `558bde8c2caf321816db660da0ab6673f7bd341f` | Hono/Workers composition root |
| `coding-standards` | [`home/.agents/skills/coding-standards`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/coding-standards) | `06c11e173bbc43f6b9ce9bc7f6fdd58ab7e53b6c` | Already tracked as `effect-standards` |
| `herdr` | [`home/.agents/skills/herdr`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/herdr) | `09f6f89e12d812ce2c596b0b148273d0522472f7` | Herdr CLI control |
| `plannotator-tui` | [`home/.agents/skills/plannotator-tui`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/plannotator-tui) | `1906b632a2ce1060294aaf6047256ba71ce1fdf1` | Herdr pane opener for Plannotator |
| `recipe-diagrams` | [`home/.agents/skills/recipe-diagrams`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/recipe-diagrams) | `54844697fae6c8967e523480ef42a9a2042e02cf` | Cooking-for-Engineers PNG renderer |
| `workday-training` | [`home/.agents/skills/workday-training`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/workday-training) | `2dbecb9dfb4655612d5d402a429c3d3442bbf238` | Workday/SCORM course driver |
| `worktrees` | [`home/.agents/skills/worktrees`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees) | `38d022ca8601fb1fb6c2c354bef9c08f4dd783a8` | Canonical `.bare` worktree layout |

Vendored via `.skill-lock.json` (do not treat Mulroy's copy as upstream):

| Skill | Declared source | Lock vs tree |
| --- | --- | --- |
| `code-review` | [`mattpocock/skills`](https://github.com/mattpocock/skills) `skills/engineering/code-review` | lock `d8e341ce…` ≠ tree `9f01557d…` |
| `diagnosing-bugs` | mattpocock `skills/engineering/diagnosing-bugs` | match |
| `domain-modeling` | mattpocock `skills/engineering/domain-modeling` | lock `388c9822…` ≠ tree `c3f8ecf2…` |
| `grill-me` | mattpocock `skills/productivity/grill-me` | match |
| `grill-with-docs` | mattpocock `skills/engineering/grill-with-docs` | lock `eedaf256…` ≠ tree `6ca01cac…` |
| `grilling` | mattpocock `skills/productivity/grilling` | match |
| `handoff` | mattpocock `skills/productivity/handoff` | match |
| `implement` | mattpocock `skills/engineering/implement` | **locked, missing from the tree** |
| `prototype` | mattpocock `skills/engineering/prototype` | match |
| `research` | mattpocock `skills/engineering/research` | lock `0a6796c5…` ≠ tree `b8dfd488…` |
| `tdd` | mattpocock `skills/engineering/tdd` | lock `79288be1…` ≠ tree `fee2c08e…` |
| `write-discoverable-code` | [`modem-dev/skills`](https://github.com/modem-dev/skills) `write-discoverable-code` | match |
| `writing-for-agents` | mattpocock `skills/productivity/writing-for-agents` | match |
| `show-me` | [`humanlayer/skills`](https://github.com/humanlayer/skills) `plugins/show-me/skills/show-me` | lock `0bdb821a…` ≠ tree `e86b7806…` |
| `cua-driver` | [`trycua/cua`](https://github.com/trycua/cua) `libs/cua-driver/rust/Skills/cua-driver`, ref `cua-driver-rs-v0.24.0` | lock `58e3cdf8…` ≠ tree `3b5cfe29…` |

Hash mismatches mean Mulroy's tree is not a clean vendor pin. Several of those skills are already in this repo from their *original* upstreams, or already installed globally.

# Already tracked here

## `coding-standards` → `effect-standards` — skip as a new skill

Manifest entry: `localSkill: effect-standards`, `pinnedCommit: fcdf06013853c2e8e5718b620d3a2b481fbcedb9`, `upstreamPaths: ["home/.agents/skills/coding-standards"]`. That pin **is** current `main`.

At this commit the upstream `SKILL.md` body matches local `effect-standards/SKILL.md` except the name, description, and title. Every upstream reference filename exists locally. Byte-for-byte identity holds for all references except dirty local edits to `effect-alchemy.md` and `effect-services.md`.

Do not import `coding-standards` as a third standards skill. TypeScript-only work already has `typescript-standards`. Effect/Alchemy work already has `effect-standards`. Continue the in-progress sync of the tracked skill; do not start a parallel adaptation.

No `coding-standards/LICENSE` exists at this commit, despite the local manifest still listing that path.

## `write-discoverable-code` — skip as a new skill

Manifest entry: `localSkill: write-discoverable-code`, `pinnedCommit: 0ccfc7d648148f78dfbe78f63ec536441589c99e`. Diff from that pin to `fcdf060` on `home/.agents/skills/write-discoverable-code` is empty. Content is unchanged; the pin is merely older than HEAD.

Mulroy's lockfile attributes the folder to [`modem-dev/skills`](https://github.com/modem-dev/skills), MIT in frontmatter. Local attribution correctly names the Mulroy tree copy at `0ccfc7d` and records a substantial rewrite. Leave updates to `update-upstream-skills`.

# Verdicts

## Pull / adapt now

**None.**

A new skill in this repo has to clear unique reusable engineering guidance, a description that will fire reliably, and an adaptation cost that does not fight Effect/TypeScript standards or this repo's "do not vendor third-party skills" rule. Nothing remaining in Mulroy's tree clears all four.

## Mine selected guidance

### `cloudflare-composition-root` — mine, do not vendor

- **Upstream:** [`home/.agents/skills/cloudflare-composition-root/SKILL.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/cloudflare-composition-root/SKILL.md) and [`EXAMPLES.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/cloudflare-composition-root/EXAMPLES.md). Introduced [`834914b15560a7806e8fc9fd6b04cfcf52f44332`](https://github.com/dmmulroy/.dotfiles/commit/834914b15560a7806e8fc9fd6b04cfcf52f44332); last edit [`dcfccdffccea86ef2e3730e2980a33ca5df20b7b`](https://github.com/dmmulroy/.dotfiles/commit/dcfccdffccea86ef2e3730e2980a33ca5df20b7b).
- **What it is.** A model-invoked composition-root recipe for Hono and Cloudflare: entrypoint adapter, binding adapter, application service, domain module, exact dependency objects. Inner code must not see `Env`, raw bindings, binding names, or `context.env`.
- **Unique mechanism, not already written here.** The leakage audit (`rg 'Env|KVNamespace|R2Bucket|D1Database|DurableObjectNamespace|ExecutionContext'` and classify every hit), "binding adapter takes the smallest capability not all of `Env`," Hono `createApp(dependencies)` / no `context.env` in routes, and "each WorkerEntrypoint, Durable Object, Workflow, queue, and scheduled handler is its own composition root."
- **Overlap.** Local [`typescript-standards/references/boundaries.md`](../skills/typescript-standards/references/boundaries.md) already says parse at the edge, narrow capabilities, construct at a composition root. Local [`effect-standards/references/modules-services-and-adapters.md`](../skills/effect-standards/references/modules-services-and-adapters.md) already names Domain / Application Service / Adapter / composition root. [`effect-alchemy.md`](../skills/effect-standards/references/effect-alchemy.md) already owns Alchemy two-phase Workers, Durable Objects, Workflows, and bindings. Mulroy's examples are `async`/`Promise` classes (`ResolveJurisdictionService`, `WorkersKvJurisdictionCache`), which would fight this repo's Effect/Layer default.
- **Invocation.** Description is usable: "Composition roots for Hono and Cloudflare. Use when adding a binding-backed service or refactoring raw runtime dependencies out of inner code." As a sibling skill it would compete with `effect-standards` on Alchemy work unless the description excluded Effect/Alchemy. That is a reliability bug, not a reason to copy it whole.
- **Adaptation cost.** Sibling pointer `../coding-standards/SKILL.md` must become `typescript-standards` plus `effect-standards`. No SPDX license. Effect-ifying the examples is a rewrite, not a copy.
- **What to mine, later, into existing references (not a new skill):**
  1. Binding adapters accept the smallest platform type, never the whole `Env`.
  2. Each service's dependency object is exact; renaming `Env` to `Dependencies` is a fail.
  3. Hono: close over exact dependencies; store only typed capabilities in Hono variables; routes and middleware do not read `context.env`.
  4. Treat every runtime surface as its own composition root; do not reuse one graph across Worker / DO / Workflow / queue / cron.
  5. Keep `ExecutionContext` out of inner code; detached work gets an explicit owner.
  6. After a change, search for raw runtime types and classify every match as composition root, binding adapter, unavoidable framework declaration, or violation.
- **What not to copy.** Promise/class services as the house style; a required `Tracer` constructor bag that bypasses Effect tracing; the relative `coding-standards` pointer.

If a future personal backend is raw Hono on Workers *without* Alchemy, revisit a standalone skill. That is not the current greenfield default.

### `worktrees` — mine only if this stack later wants a worktree skill

- **Upstream:** [`home/.agents/skills/worktrees`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees), added [`78de1da9336a375737e4cba50b6389ce561b86fb`](https://github.com/dmmulroy/.dotfiles/commit/78de1da9336a375737e4cba50b6389ce561b86fb). Helper: [`scripts/new-worktree.sh`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees/scripts/new-worktree.sh). Layout: [`references/canonical-root.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees/references/canonical-root.md).
- **Unique.** A complete `.bare` root layout (`<repo>/.bare`, `<repo>/main`, `<repo>/<topic>`), fetch/reuse/create decision order, and conversion invariants.
- **Overlap / scope.** This repo's machine skill is `remote-development` (Fleet), not Git layout. `model-routing` mentions isolated worktrees as a delegation mechanic, not a checkout convention. Mulroy's layout is a personal canonical-root policy.
- **Invocation.** Description is tight enough ("canonical `.bare` repository root") that it would not fire on ordinary `git worktree` chatter. Still the wrong package until this stack actually uses that layout.
- **If ever writing a local worktree skill:** steal the helper's branch decision order and the "account for dirty state before `worktree remove`" completion check. Do not require `.bare` unless that becomes the local convention.

## Skip

### First-party, out of scope or already present

**`herdr`** — [`home/.agents/skills/herdr/SKILL.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/herdr/SKILL.md), last body commit [`d0b81835146e03a42e374312de47ef9b303f6205`](https://github.com/dmmulroy/.dotfiles/commit/d0b81835146e03a42e374312de47ef9b303f6205). Already installed at `/Users/max-vev/.pi/agent/skills/herdr`. Bodies match except the description. The local description is stricter ("only when the user explicitly mentions Herdr") and is the one to keep. Mulroy's description ("Use for subagents when the user or another skill explicitly asks for or requires them") over-fires. Packaging Mulroy's version here would regress invocation. If this repo ever wants a Herdr skill as a sibling of `remote-development`, start from the local global copy, not from `dmmulroy`.

**`bro`** — [`home/.agents/skills/bro/SKILL.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/bro/SKILL.md), first seen [`cdba491f1f9c952979af37f15e4c3efb26f625df`](https://github.com/dmmulroy/.dotfiles/commit/cdba491f1f9c952979af37f15e4c3efb26f625df). Four instruction sentences, user-invoked. Already installed globally. Not reusable engineering guidance.

**`plannotator-tui`** — [`home/.agents/skills/plannotator-tui/SKILL.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/plannotator-tui/SKILL.md), present since [`fd84f529229f3ed41f7e72e784164da5fd1d6a41`](https://github.com/dmmulroy/.dotfiles/commit/fd84f529229f3ed41f7e72e784164da5fd1d6a41). Thin Herdr wrapper around `plannotator-tui herdr open`. This machine already loads `plannotator`, `plannotator-review`, `plannotator-annotate`, and related skills from `@plannotator/pi-extension`. Do not duplicate a TUI shim.

**`recipe-diagrams`** — [`home/.agents/skills/recipe-diagrams`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/recipe-diagrams), PNG renderer added [`4cb584aefa74bcb224cd918ca1051438ac1a7b54`](https://github.com/dmmulroy/.dotfiles/commit/4cb584aefa74bcb224cd918ca1051438ac1a7b54). Well-made, user-invoked, ImageMagick/Python, cooking diagrams. Outside this repository's engineering inventory. Visual explanation of *code* is already covered globally by `show-me` and `visual-explainer`.

**`workday-training`** — [`home/.agents/skills/workday-training`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/workday-training), recovered [`d61bbb260030c2e03e27f2c4a84816374ccb8352`](https://github.com/dmmulroy/.dotfiles/commit/d61bbb260030c2e03e27f2c4a84816374ccb8352), last edit [`374324a74a906a366c1ed3cfa1aca659a088d3c7`](https://github.com/dmmulroy/.dotfiles/commit/374324a74a906a366c1ed3cfa1aca659a088d3c7). Employer-specific CDP/SCORM driver for completing Workday courses by manipulating the LMS API. Not reusable public engineering guidance; out of scope.

### Third-party copies — skip; use original upstreams if wanted

This repository's rule is explicit: do not vendor third-party skills; install them from their source so history stays intact ([`README.md`](../README.md), [`AGENTS.md`](../AGENTS.md)). Mulroy's `.skill-lock.json` already names those sources. Several lock hashes do not match his tree, so his copies are a worse pin than the originals.

| Mulroy path | Why skip |
| --- | --- |
| [`code-review`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/code-review) | Already adapted here from [`mattpocock/skills`](https://github.com/mattpocock/skills) at `3cca18b`. Local is a smaller, harness-neutral rewrite. Mulroy's copy is larger and drifted from its lock hash. |
| [`grill-me`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/grill-me) / [`grilling`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/grilling) / [`grill-with-docs`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/grill-with-docs) | Already adapted here from mattpocock. Local inlined the interview loop and made the "grill me" trigger model-invoked. Mulroy's `grill-me` is a trampoline ("Call the Skill tool with grilling") with `disable-model-invocation: true`. `grill-with-docs` is two Skill-tool calls. Do not re-import the trampoline. |
| [`tdd`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/tdd) | This repo already chose pstack's `tdd` (`5bf2b154…`), not mattpocock's. Mulroy's copy is the mattpocock one, user-invoked, broader trigger ("wants integration tests"). Replacing local TDD would be a product reversal, not an update. |
| [`diagnosing-bugs`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/diagnosing-bugs), [`domain-modeling`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/domain-modeling), [`handoff`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/handoff), [`research`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/research), [`writing-for-agents`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/writing-for-agents) | mattpocock originals, already installed globally. Not missing from the stack. If this repo later packages one, pin mattpocock, not Mulroy's possibly drifted copy. |
| [`prototype`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/prototype) | Real unique workflow (throwaway logic HTML vs UI variant lab). Still mattpocock's skill. If wanted, install from [`mattpocock/skills/skills/engineering/prototype`](https://github.com/mattpocock/skills/tree/main/skills/engineering/prototype), do not launder it through dotfiles. |
| [`show-me`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/show-me) | humanlayer original, already installed globally. Mulroy tree hash drifted from lock. |
| [`cua-driver`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/cua-driver) | trycua computer-use driver, ~69KB `SKILL.md` plus platform manuals, MIT from Cua. Host-tooling, not this repo's reusable coding-standards surface. Install from [`trycua/cua`](https://github.com/trycua/cua) if a machine needs it. |
| `implement` | Listed in the lockfile, absent from the skill tree. Nothing to adapt. |

# License and packaging cost

| Fact | Source |
| --- | --- |
| GitHub `license` is `null` | [repo API](https://api.github.com/repos/dmmulroy/.dotfiles) at inspection time |
| No root `LICENSE` blob | tree of `fcdf060` |
| README: "This repository is for personal use. Feel free to fork and adapt for your own needs." | [README License](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/README.md) |
| `write-discoverable-code` declares MIT in frontmatter; lockfile names modem-dev | [SKILL.md](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/write-discoverable-code/SKILL.md), `.skill-lock.json` |
| mattpocock / humanlayer / cua copies carry their upstream licenses; cua is the only bundled license file | `cua-driver/LICENSE.md` |
| Existing local adaptations already proceeded on that basis | `skills/effect-standards/ATTRIBUTION.md`, `skills/write-discoverable-code/ATTRIBUTION.md` |

Any future Mulroy-first-party adaptation should keep ATTRIBUTION language that the upstream repo still has no SPDX license, and should not invent a `coding-standards/LICENSE` that is not in the tree.

Mulroy often sets `disable-model-invocation: true` on skills this repo prefers to keep model-invoked with a tight description (`grill-me`, `tdd`, `code-review`). Copying his frontmatter would silently drop discoverability.

# What not to do

- Do not add `cloudflare-composition-root` as a packaged skill next to `effect-standards`.
- Do not re-adapt `coding-standards` under a second name.
- Do not vendor mattpocock, humanlayer, modem-dev, or trycua skills from Mulroy's stow tree; his lock hashes already prove copies drift.
- Do not replace local pstack `tdd` with Mulroy's mattpocock `tdd`.
- Do not copy Mulroy's `herdr` description over the stricter local one.
- Do not package `workday-training` or `recipe-diagrams` into this engineering skills repo.
- Do not treat `.skill-lock.json`'s missing `implement` as a candidate.

# Checks

- Upstream commit and skill tree enumerated from Git, not from the GitHub README.
- Local comparison used HEAD plus `upstream-skills.json`; dirty `effect-standards` / untracked `code-review`, `grill-me`, and `tdd` were not overwritten and were not treated as committed inventory.
- No skill files, attribution files, or `upstream-skills.json` were modified.
- Structural repo check not required: documentation-only note under `research/`.
