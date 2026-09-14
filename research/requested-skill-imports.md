# Requested skill imports: grilling, grill-with-docs, cua-driver

**Research record.** Implementation recommendations for replacing local `grill-me` with Matt Pocock's `grilling` plus `grill-with-docs`, and adding `cua-driver`. This file is not agent instructions. It does not modify skills or manifests.

**Updated 2026-09-14.** Primary trees inspected from Git, not from secondary write-ups.

## Recommendation

Do the import, but **from the original upstreams**, not from Dillon Mulroy's stow copies.

1. **Delete** `skills/grill-me/` (the inlined, one-question, `ask_user` adaptation).
2. **Add** `grilling` and `grill-with-docs` from [`mattpocock/skills`](https://github.com/mattpocock/skills) at commit [`3cca18b368ae95cdbdebbff572ccafa662551015`](https://github.com/mattpocock/skills/commit/3cca18b368ae95cdbdebbff572ccafa662551015) (current `main`).
3. **Also add** `domain-modeling` from the same commit. `grill-with-docs` is a trampoline onto `grilling` **and** `domain-modeling`; packaging the trampoline without the second skill leaves a broken skill for anyone who installs only this package.
4. **Add** `cua-driver` from [`trycua/cua`](https://github.com/trycua/cua) tag [`cua-driver-rs-v0.24.0`](https://github.com/trycua/cua/releases/tag/cua-driver-rs-v0.24.0) (commit [`4b3396d9fe4bd3cf723b0eb8db83c18a8764b520`](https://github.com/trycua/cua/commit/4b3396d9fe4bd3cf723b0eb8db83c18a8764b520)).
5. **Do not copy** Mulroy's trees as the source of truth. `grill-me` / `grilling` match upstream; `grill-with-docs` and `cua-driver` do not. His `cua-driver` extras (`LOCAL.md`, Helium, `computer` MCP, Stow) are machine-local and must stay out of this public package.

Pi has no Skill tool, this repository forbids packaged links that leave a skill directory, and `SKILL.md` must stay under 500 lines. Those three rules drive every adaptation below.

**Working tree at write time.** HEAD is [`597573318a2fd045950ae47e5196b587e69ee096`](https://github.com/maximilianpw/agent-skills/commit/597573318a2fd045950ae47e5196b587e69ee096). Unrelated dirty work already present, and not edited here: modified `effect-standards`, `nestjs-standards/SKILL.md`, `project-verification/SKILL.md`, `update-upstream-skills/SKILL.md`, `upstream-skills.json`, `README.md`; untracked `skills/code-review/`, `skills/grill-me/`, `skills/tdd/`, `research/dmmulroy-upstream-skills.md`. Treat the untracked `skills/grill-me/` as the local skill being replaced, not as committed inventory.

This request **overrides** the "pull none" verdict in [`research/dmmulroy-upstream-skills.md`](dmmulroy-upstream-skills.md) for these named skills only. That earlier note is still right that Mulroy's copies are the wrong pin.

## Scope and sources

Question: how to remove local `grill-me`, replace it with `grilling` plus `grill-with-docs`, and bring in `cua-driver`, in a way that satisfies this repository's packaging rules and Pi's skill loader.

Primary sources, in order:

1. [`mattpocock/skills`](https://github.com/mattpocock/skills) `main` at [`3cca18b`](https://github.com/mattpocock/skills/commit/3cca18b368ae95cdbdebbff572ccafa662551015). Sparse checkout of `skills/productivity/grill-me`, `skills/productivity/grilling`, `skills/engineering/grill-with-docs`, `skills/engineering/domain-modeling`, root `LICENSE`. GitHub license: MIT. ([repo API](https://api.github.com/repos/mattpocock/skills))
2. [`trycua/cua`](https://github.com/trycua/cua) tag `cua-driver-rs-v0.24.0` at [`4b3396d9f`](https://github.com/trycua/cua/commit/4b3396d9fe4bd3cf723b0eb8db83c18a8764b520) (`chore(main): release cua-driver-rs 0.24.0 (#3472)`). Sparse checkout of `libs/cua-driver/rust/Skills/cua-driver` and root `LICENSE.md`. GitHub license: MIT. ([repo API](https://api.github.com/repos/trycua/cua))
3. [`dmmulroy/.dotfiles`](https://github.com/dmmulroy/.dotfiles) commit [`fcdf06013853c2e8e5718b620d3a2b481fbcedb9`](https://github.com/dmmulroy/.dotfiles/commit/fcdf06013853c2e8e5718b620d3a2b481fbcedb9), plus [`home/.agents/.skill-lock.json`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/.skill-lock.json). GitHub license: `null`.
4. This repo: [`AGENTS.md`](../AGENTS.md), [`README.md`](../README.md), [`upstream-skills.json`](../upstream-skills.json), [`scripts/validate-skills.mjs`](../scripts/validate-skills.mjs), [`skills/update-upstream-skills/SKILL.md`](../skills/update-upstream-skills/SKILL.md), local untracked [`skills/grill-me/`](../skills/grill-me/).
5. Pi 0.85.1: [`docs/skills.md`](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md) (loaded from the installed `libexec/pi/docs/skills.md`), Pi README "No MCP" philosophy, Agent Skills [specification](https://agentskills.io/specification) and [integrate-skills](https://agentskills.io/integrate-skills).

Secondary write-ups were not used. Mulroy's tree is a comparison target, not an upstream.

# Provenance: Mulroy copies versus original upstreams

Mulroy's lockfile already names the original sources. Folder hashes prove which copies are clean and which drifted.

| Skill | Declared source in `.skill-lock.json` | Lock folder hash | Upstream tree at requested pin | Mulroy tree at `fcdf060` |
| --- | --- | --- | --- | --- |
| `grill-me` | `mattpocock/skills` `skills/productivity/grill-me/SKILL.md` | `3df14e2d3a89459bf300614be9247e3ce74798f8` | **same** at `3cca18b` | **same** |
| `grilling` | `mattpocock/skills` `skills/productivity/grilling/SKILL.md` | `f0732035b8b1b60ae39454e4191caef32fa91903` | **same** | **same** |
| `grill-with-docs` | `mattpocock/skills` `skills/engineering/grill-with-docs/SKILL.md` | `eedaf2562c83155115e9c649fa3ecaac2e10e81d` | **same as lock** at `3cca18b` | `6ca01cacea9e4f41b62a6362bddc139c357fc0ec` (**drifted**) |
| `domain-modeling` | `mattpocock/skills` `skills/engineering/domain-modeling/SKILL.md` | `388c9822641805ca2dcd5038e68a1d5282437ee5` | **same** at `3cca18b` | not compared here (not requested, but required companion) |
| `cua-driver` | `trycua/cua` ref `cua-driver-rs-v0.24.0` `libs/cua-driver/rust/Skills/cua-driver/SKILL.md` | `58e3cdf81557d0af108d69441f5bb31f703f9ad1` | **same as lock** at tag | `3b5cfe29d00b318d1ace2ae2e422933451bb6a60` (**drifted**) |

Byte comparison of individual files:

| File | mattpocock / trycua vs Mulroy |
| --- | --- |
| `grill-me/SKILL.md`, `grill-me/agents/openai.yaml` | identical |
| `grilling/SKILL.md`, `grilling/agents/openai.yaml` | identical |
| `grill-with-docs/agents/openai.yaml` | identical |
| `grill-with-docs/SKILL.md` | **description only.** Upstream: `which also creates docs (ADR's and glossary) as we go.` Mulroy: `which also creates docs as we go.` Body is the same trampoline. |
| `cua-driver/{BROWSER,EMBEDDING,LINUX,MACOS,README,RECORDING,WINDOWS}.md` | identical |
| `cua-driver/SKILL.md` | **not identical.** Mulroy prepends a "Dotfiles integration — read first" section pointing at `LOCAL.md`. |
| `cua-driver/LOCAL.md` | **Mulroy-only** (3012 bytes). Helium profiles, `computer` MCP, Stow, `vpx skills add`. |
| `cua-driver/LICENSE.md` | **Mulroy-only inside the skill dir.** Bytes match trycua root `LICENSE.md` (Cua AI, MIT, 2025). Upstream skill pack has no license file of its own. |

Conclusion: pin mattpocock `3cca18b` and trycua `4b3396d9f`. Use Mulroy only as a list of Pi-local overrides **not** to vendor.

# What the original skills are

## `grilling` (model-invoked primitive)

Upstream [`skills/productivity/grilling/SKILL.md`](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/grilling/SKILL.md) (1987 bytes, 4 files if you count `agents/openai.yaml`).

- Description: `Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.`
- No `disable-model-invocation`. Matt's README lists it under **Model-invoked** and calls it the reusable primitive behind `grill-me` and `grill-with-docs`. ([README](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/README.md))
- Mechanism: private **design tree**, work it in **rounds**, ask the whole **frontier** in one round (numbered questions + recommended answers), wait, recompute. Facts are the agent's job (dispatch a sub-agent; do not block the rest of the frontier). Done when the frontier is empty **and** the user confirms shared understanding. Do not act until then.
- No Skill-tool language. No `ask_user`. No supporting `references/`.

`agents/openai.yaml`:

```yaml
interface:
  display_name: "Grilling"
  short_description: "Stress-test thinking a round of questions at a time"
```

No `default_prompt`, so this repository's OpenAI-metadata check does not apply.

## `grill-me` (user-invoked trampoline, upstream)

Upstream [`skills/productivity/grill-me/SKILL.md`](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/grill-me/SKILL.md) (157 bytes):

```markdown
---
name: grill-me
description: A relentless interview to sharpen a plan or design.
disable-model-invocation: true
---

Call the Skill tool with "grilling".
```

`agents/openai.yaml` sets `policy.allow_implicit_invocation: false`.

**Do not re-add this trampoline** unless the user later wants `/skill:grill-me` muscle memory. `grilling`'s description already fires on "any 'grill' trigger phrases", which covers natural-language "grill me". Keeping both would restore the Skill-tool problem for no extra mechanism.

## Local `grill-me` being removed

Untracked [`skills/grill-me/SKILL.md`](../skills/grill-me/SKILL.md) is **not** the upstream trampoline. It is a self-contained, model-invoked rewrite:

- Description names the `"grill me"` trigger (no `disable-model-invocation`).
- One question at a time; `ask_user` when answers can be enumerated.
- Completion: stop when no unresolved product/design decision blocks a correct plan; continue into planning only if asked.

That is a different product from `grilling`. Replacing it **is** the round-based, whole-frontier interview. Do not smuggle one-at-a-time back into `grilling`.

Manifest already has a `grill-me` entry pinned to mattpocock `3cca18b` / `skills/productivity/grill-me`. Delete that entry with the directory.

## `grill-with-docs` (user-invoked trampoline)

Upstream [`skills/engineering/grill-with-docs/SKILL.md`](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/grill-with-docs/SKILL.md) (247 bytes):

```markdown
---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
disable-model-invocation: true
---

Call the Skill tool twice, for "grilling" and "domain-modeling".
```

Matt's engineering README: "Grilling session that also builds your project's domain model, sharpening terminology and updating `CONTEXT.md` and ADRs inline." Keep the longer description (ADRs + glossary). Mulroy's shortened description is worse for invocation: it drops the branches that distinguish this skill from plain `grilling`.

`agents/openai.yaml`: `display_name: "Grill with Docs"`, `allow_implicit_invocation: false`.

## `domain-modeling` (required companion)

Upstream tree at `3cca18b`:

```
skills/engineering/domain-modeling/
├── SKILL.md              3331 bytes
├── CONTEXT-FORMAT.md     2290 bytes
├── ADR-FORMAT.md         2733 bytes
└── agents/openai.yaml     101 bytes
```

[`SKILL.md`](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/domain-modeling/SKILL.md) is model-invoked. It already uses packaged relative links `[CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md)` and `[ADR-FORMAT.md](./ADR-FORMAT.md)`, which this repository's validator will accept. No Skill-tool language. Description: `Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording or editing an ADR.`

It is already installed globally on this machine (`~/.pi/agent/skills/domain-modeling`, `~/.agents/skills/domain-modeling`). That does **not** help `npx skills add maximilianpw/agent-skills` consumers. If `grill-with-docs` ships in this package, `domain-modeling` must ship too.

## `cua-driver`

Upstream pack at tag `cua-driver-rs-v0.24.0`:

```
libs/cua-driver/rust/Skills/cua-driver/
├── SKILL.md      1123 lines / 68469 bytes   ← over this repo's 500-line cap
├── README.md      113 lines /  4027 bytes
├── BROWSER.md     494 lines / 24203 bytes
├── EMBEDDING.md   578 lines / 28678 bytes
├── LINUX.md       364 lines / 21346 bytes
├── MACOS.md       509 lines / 30791 bytes
├── RECORDING.md   161 lines /  8074 bytes
└── WINDOWS.md     866 lines / 49830 bytes
```

No `agents/openai.yaml`. No `LICENSE` inside the skill directory. Root [`LICENSE.md`](https://github.com/trycua/cua/blob/cua-driver-rs-v0.24.0/LICENSE.md) is MIT, Copyright (c) 2025 Cua AI, Inc. The skill README says repository copies are MIT; ClawHub copies are MIT-0. This package copies from GitHub, so MIT.

Frontmatter (keep):

- `name: cua-driver`
- unquoted `description` (431 characters, under 1024)
- `version: 0.24.0 # x-release-please-version`
- nested `metadata.openclaw.requires` (bins, env vars, homepage `https://cua.ai/docs/cua-driver`)

This repository's frontmatter parser only extracts `name` and `description` from unindented keys, so the extra fields and nested `description:` env-var lines are ignored. Pi also ignores unknown frontmatter. ([`scripts/validate-skills.mjs`](../scripts/validate-skills.mjs), [Pi skills.md](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md))

Transport default in upstream `SKILL.md`:

> Default transport is the `cua-driver` CLI for one-off calls — `Bash` shelling out to `cua-driver <tool-name> '<JSON-args>'`. … Persistent MCP wins for an ordered action loop. … translate to MCP form only when MCP is requested.

That CLI default is the Pi-native path. Pi's README states **No MCP** in core; MCP is an optional extension. ([Pi README](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/README.md))

Companion files are referenced from `SKILL.md` with backtick filenames (`MACOS.md`, …), not markdown links. The validator only checks markdown links, so those references will not be link-checked unless the adapted entry point converts the pointers.

No Skill-tool, `ask_user`, or Herdr references anywhere in the pack.

# Pi and repository constraints that force adaptations

## 1. There is no Skill tool

Pi discovers skills, puts name/description (and path) in the system prompt, and expects the model to **`read` the `SKILL.md`** (or `/skill:name`). ([Pi docs/skills.md](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md); [integrate-skills](https://agentskills.io/integrate-skills) "file-read activation")

Codex/Claude Skill-tool phrasing (`Call the Skill tool with "grilling"`) is a no-op here. `grill-me` and `grill-with-docs` trampolines **must** be rewritten to "read and follow skill X". `grilling` itself has no such phrasing.

`disable-model-invocation: true` is a Pi (and Codex yaml-policy) extra, not an Agent Skills spec field. Pi hides those skills from the catalog; the user must `/skill:name`. Keep it on `grill-with-docs`. Keep it **off** `grilling`, `domain-modeling`, and `cua-driver`.

A user-invoked skill cannot use a packaged relative link to a sibling skill: [`AGENTS.md`](../AGENTS.md) and the validator require relative markdown links to resolve **inside** the skill directory. Name the other skills in prose. Pi's catalog still exposes `grilling` and `domain-modeling` because those are model-invoked.

Suggested `grill-with-docs` body (keep the upstream description and `disable-model-invocation`):

```markdown
Read and follow the `grilling` skill and the `domain-modeling` skill.
Use `read` on each skill's `SKILL.md` (or `/skill:grilling` then `/skill:domain-modeling`).
Run them together: the interview is `grilling`; glossary and ADR writes are `domain-modeling`.
```

Do not invent a packaged `../grilling/SKILL.md` link.

## 2. `ask_user` is not part of Pi's default tool set

Local `grill-me` says "Use `ask_user` when the likely answers can be enumerated." Some Pi sessions on this machine have had an `ask_user` tool (Codex/OpenAI-style); this repository's Pi 0.85.1 docs mention optional `ask_question` and `--exclude-tools ask_question`. Neither is guaranteed.

Upstream `grilling` already does the portable thing: print a numbered round and **wait for the user's message**. Keep that. Do **not** port `ask_user` into `grilling`. A whole-frontier round cannot be expressed as one `ask_user` call anyway.

Optional one-line harness note inside `grilling`, not a behavior change:

> Print the round in the conversation and wait for the user's replies. Do not require a special question tool.

The upstream "dispatch a sub-agent" sentence fights Pi core ("No sub-agents") but matches this stack's `model-routing` / background-agent convention. Adapt to: look the fact up with tools; if a background agent is available, dispatch one and **do not block** the rest of the frontier. That preserves the frontier rule.

## 3. `SKILL.md` must be under 500 physical lines

[`scripts/validate-skills.mjs`](../scripts/validate-skills.mjs) fails at 500 lines. The Agent Skills spec recommends the same cap. Upstream `cua-driver/SKILL.md` is **1123 lines**. Copying it unmodified will fail `npm run check`.

Pi itself is lenient and would still load it. The 500-line rule is this package's rule, and it is the right one: 1123 lines is also well above the spec's ~5000-token instruction budget.

**Split, do not raise the validator limit.**

Keep companion files at the skill root with upstream names so they can be `exactFiles`. Move the overflow of `SKILL.md` into `references/core.md`. Convert the entry-point pointers to markdown links so the validator actually checks them.

Recommended `SKILL.md` keep (the steps every run needs):

- Frontmatter (name, description, version, metadata, plus a `compatibility` line: `Requires the cua-driver CLI on PATH, or an MCP client connected to cua-driver mcp.`)
- Snapshot-before-action invariant
- CLI vs MCP transport default (CLI for one-off; persistent MCP only when requested / actually connected)
- Narrowest semantic route (the 0–5 ladder, short)
- No-foreground principle (short) with links to platform files
- Canonical loop
- "Read this next" links: current OS guide, `BROWSER.md` / `RECORDING.md` / `EMBEDDING.md` only when needed, and [the rest of the core](references/core.md)

Move into `references/core.md`: recent-history continuation, filesystem/clipboard outcome detail, Claude Code computer-use flag, shell/MCP session mechanics, agent cursor overlay, full behavior matrix, verify-then-escalate algorithm, tool dispatch table, parameter contract, pixel-click contract, web-rendered apps, recording, error patterns, things to avoid, e2e example.

Do not flatten platform manuals into `references/`; upstream and `cua-driver doctor` tell the agent to read `MACOS.md` beside `SKILL.md`.

## 4. MCP, Herdr, and local overrides

**MCP.** Upstream already prefers CLI and says to translate to MCP only when MCP is requested. Keep that. If this Pi has an MCP gateway, the agent should **discover** server and tool names (`mcp({ search, server })`), not assume Mulroy's `computer` server or `computer_` prefix. Those names live in *his* `home/.pi/agent/mcp.json`, not in a reusable skill.

Do not bake `mcp({ tool: "computer_get_window_state", args: "..." })` into this package.

**Herdr.** The cua pack never mentions Herdr. Herdr is a terminal multiplexer (`HERDR_ENV=1`). cua-driver drives native GUI apps. Do not add Herdr hooks, pane forwarding, or "run cua inside Herdr" instructions.

**Mulroy `LOCAL.md` — do not import.** It encodes:

- persistent `computer` MCP as the default (overrides upstream CLI default)
- Helium (`net.imput.helium`) work vs personal profiles
- Stow symlink layout; "do not install duplicate copies under `.pi/agent/skills`"
- `vpx skills add` from tag `cua-driver-rs-v0.24.0`
- telemetry disabled locally; standard permission mode

Those belong in the user's chezmoi/dotfiles (or a private overlay skill), not in `maximilianpw/agent-skills`. If a local override is needed later, add it outside this repository so updates of the packaged skill do not clobber Helium/MCP policy.

## 5. OpenAI metadata

Copy upstream `agents/openai.yaml` files as-is for `grilling`, `grill-with-docs`, and `domain-modeling`. They have no `interface.default_prompt`, which the validator allows. ([`scripts/validate-skills.test.mjs`](../scripts/validate-skills.test.mjs) "checks an exact skill token only when default_prompt is present")

Do **not** add a `default_prompt` unless you are willing to include the exact `$skill-name` token. Do not invent `agents/openai.yaml` for `cua-driver`; upstream has none.

Keep `policy.allow_implicit_invocation: false` on `grill-with-docs` next to Pi's `disable-model-invocation: true`. They are the Codex and Pi expressions of the same choice.

## 6. Consumer `AGENTS.md` is outside this repo

Global [`/Users/max-vev/.pi/agent/AGENTS.md`](/Users/max-vev/.pi/agent/AGENTS.md) currently says: "Use `grill-me` for explicitly requested planning or unresolved product/design decisions that need user input". After this change, that line should name `grilling` (and `grill-with-docs` when docs should be written). That edit is **not** part of this repository. Flag it as a follow-up on the implementing agent's report.

This repository's own [`AGENTS.md`](../AGENTS.md) must not grow a catalog of skill workflows.

# Licenses and attribution

| Skill | License | Copyright to retain | Local LICENSE pattern |
| --- | --- | --- | --- |
| `grilling`, `grill-with-docs`, `domain-modeling` | MIT ([mattpocock/skills/LICENSE](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/LICENSE)) | Copyright (c) 2026 Matt Pocock | Dual-copyright MIT file inside each skill, same as [`skills/code-review/LICENSE`](../skills/code-review/LICENSE): add `Copyright (c) 2026 Maximilian Pinder-White` **only if the body was adapted**. Exact-copy files still need the upstream notice. |
| `cua-driver` | MIT ([trycua/cua/LICENSE.md](https://github.com/trycua/cua/blob/cua-driver-rs-v0.24.0/LICENSE.md)) | Copyright (c) 2025 Cua AI, Inc. | Bundle as `skills/cua-driver/LICENSE` (this repo's filename convention, not `LICENSE.md`). Add adapter copyright because `SKILL.md` will be split. |

[`AGENTS.md`](../AGENTS.md): "Do not vendor third-party skills; preserve license and attribution files for adapted material." The existing house style is **adapt + ATTRIBUTION + bundled LICENSE**, not an unmodified vendor dump. `cua-driver` is large, but `remote-development` already established machine-tooling skills in this package. Still adapt the entry point; exact-copy the manuals.

Each new skill gets `ATTRIBUTION.md` that names repository, path, and the **40-character pin**, because `check_upstreams.py` requires the pin string to appear in that file.

# Manifest, README, and checker implications

`package.json` `pi.skills: ["./skills"]` does not change.

[`README.md`](../README.md) inventory is alphabetical and must equal `skills/*` directory names. After the change, drop `` `grill-me` `` and add:

- `` `cua-driver` — drive a native GUI app through the cua-driver CLI or MCP, with snapshot-before-action. ``
- `` `domain-modeling` — sharpen glossary and ADRs while the domain is being designed. ``
- `` `grill-with-docs` — user-invoked grilling session that also writes CONTEXT.md and ADRs. ``
- `` `grilling` — relentlessly interview the user a frontier-round at a time. ``

Requirements section: add that `cua-driver` expects the [cua-driver](https://cua.ai/docs/cua-driver) binary on PATH (optional MCP). Do not run the upstream install curl during repository validation ([`AGENTS.md`](../AGENTS.md) boundaries).

`upstream-skills.json`:

- **Remove** the `grill-me` object.
- **Add** four entries. `pinnedCommit` must be a 40-char SHA. `ref` is what `git clone --depth 1 --branch` uses in [`check_upstreams.py`](../skills/update-upstream-skills/scripts/check_upstreams.py).

Suggested entries (SHAs verified from the checkouts above):

```json
{
  "localSkill": "grilling",
  "attribution": "skills/grilling/ATTRIBUTION.md",
  "repository": "https://github.com/mattpocock/skills.git",
  "ref": "main",
  "pinnedCommit": "3cca18b368ae95cdbdebbff572ccafa662551015",
  "upstreamPaths": ["skills/productivity/grilling"],
  "licensePaths": ["LICENSE"],
  "exactFiles": [
    {
      "upstream": "skills/productivity/grilling/agents/openai.yaml",
      "local": "skills/grilling/agents/openai.yaml"
    }
  ]
}
```

If the implementing agent keeps `grilling/SKILL.md` byte-identical except a short harness note, **do not** list `SKILL.md` in `exactFiles`. Exact-file handling wins over adapted diffs; a harness note would then look like drift.

```json
{
  "localSkill": "grill-with-docs",
  "attribution": "skills/grill-with-docs/ATTRIBUTION.md",
  "repository": "https://github.com/mattpocock/skills.git",
  "ref": "main",
  "pinnedCommit": "3cca18b368ae95cdbdebbff572ccafa662551015",
  "upstreamPaths": ["skills/engineering/grill-with-docs"],
  "licensePaths": ["LICENSE"],
  "exactFiles": [
    {
      "upstream": "skills/engineering/grill-with-docs/agents/openai.yaml",
      "local": "skills/grill-with-docs/agents/openai.yaml"
    }
  ]
}
```

```json
{
  "localSkill": "domain-modeling",
  "attribution": "skills/domain-modeling/ATTRIBUTION.md",
  "repository": "https://github.com/mattpocock/skills.git",
  "ref": "main",
  "pinnedCommit": "3cca18b368ae95cdbdebbff572ccafa662551015",
  "upstreamPaths": ["skills/engineering/domain-modeling"],
  "licensePaths": ["LICENSE"],
  "exactFiles": [
    {
      "upstream": "skills/engineering/domain-modeling/CONTEXT-FORMAT.md",
      "local": "skills/domain-modeling/CONTEXT-FORMAT.md"
    },
    {
      "upstream": "skills/engineering/domain-modeling/ADR-FORMAT.md",
      "local": "skills/domain-modeling/ADR-FORMAT.md"
    },
    {
      "upstream": "skills/engineering/domain-modeling/agents/openai.yaml",
      "local": "skills/domain-modeling/agents/openai.yaml"
    }
  ]
}
```

Keep `domain-modeling/SKILL.md` out of `exactFiles` only if it is edited. Prefer leaving it byte-identical and listing it as an exact file too.

```json
{
  "localSkill": "cua-driver",
  "attribution": "skills/cua-driver/ATTRIBUTION.md",
  "repository": "https://github.com/trycua/cua.git",
  "ref": "cua-driver-rs-v0.24.0",
  "pinnedCommit": "4b3396d9fe4bd3cf723b0eb8db83c18a8764b520",
  "upstreamPaths": ["libs/cua-driver/rust/Skills/cua-driver"],
  "licensePaths": ["LICENSE.md"],
  "exactFiles": [
    {
      "upstream": "libs/cua-driver/rust/Skills/cua-driver/README.md",
      "local": "skills/cua-driver/README.md"
    },
    {
      "upstream": "libs/cua-driver/rust/Skills/cua-driver/BROWSER.md",
      "local": "skills/cua-driver/BROWSER.md"
    },
    {
      "upstream": "libs/cua-driver/rust/Skills/cua-driver/EMBEDDING.md",
      "local": "skills/cua-driver/EMBEDDING.md"
    },
    {
      "upstream": "libs/cua-driver/rust/Skills/cua-driver/LINUX.md",
      "local": "skills/cua-driver/LINUX.md"
    },
    {
      "upstream": "libs/cua-driver/rust/Skills/cua-driver/MACOS.md",
      "local": "skills/cua-driver/MACOS.md"
    },
    {
      "upstream": "libs/cua-driver/rust/Skills/cua-driver/RECORDING.md",
      "local": "skills/cua-driver/RECORDING.md"
    },
    {
      "upstream": "libs/cua-driver/rust/Skills/cua-driver/WINDOWS.md",
      "local": "skills/cua-driver/WINDOWS.md"
    }
  ]
}
```

Pinning `ref` to the **release tag** is deliberate: Mulroy's lock does the same, and `check_upstreams` cloning `--branch cua-driver-rs-v0.24.0` will stay current until someone moves the pin to a newer tag. Do not track `main` for this skill; the pack is versioned with the driver (`version: 0.24.0` in frontmatter).

`SKILL.md` and `references/core.md` are adaptations, not exact copies.

# Implementation sequence for the next agent

Do not install skills into `~/.agents` or `~/.pi` as "validation". Do not run `cua-driver` install scripts. Do not commit `.scratch/`.

1. Delete `skills/grill-me/` (`SKILL.md`, `ATTRIBUTION.md`, `LICENSE`, `agents/openai.yaml`).
2. Copy mattpocock trees for `grilling`, `grill-with-docs`, `domain-modeling` from commit `3cca18b`.
3. Rewrite only `grill-with-docs/SKILL.md` body (Skill-tool → Pi read). Keep `disable-model-invocation: true` and the ADR/glossary description.
4. Add the short harness note to `grilling/SKILL.md` (print the round and wait; facts via tools / optional background agent without blocking). Do not change the round format.
5. Leave `domain-modeling` byte-identical if the links already resolve; add `ATTRIBUTION.md` + `LICENSE`.
6. Copy the cua pack from tag `cua-driver-rs-v0.24.0`. Split `SKILL.md` as above. Add `LICENSE` from upstream `LICENSE.md`. Add `ATTRIBUTION.md` describing the split and the CLI-default (no Mulroy MCP/Helium overlay).
7. Update `README.md` inventory (alphabetical) and Requirements.
8. Replace the `grill-me` object in `upstream-skills.json` with the four entries above.
9. Checks:
   - `node scripts/validate-skills.mjs` (and `npm run check` if tests were not already run this session)
   - `uvx --from skills-ref agentskills validate skills/<name>` for each new/changed skill
   - `npx --yes skills add . --list`
   - `python3 skills/update-upstream-skills/scripts/check_upstreams.py` (must exit 0 once pins and exactFiles match)
   - `git diff --check`
10. Inspect rendered Markdown: `grilling` still fires on "grill me"; `grill-with-docs` does not steal ordinary grilling (user-invoked); `cua-driver` description still requires a real GUI/app-drive request; `domain-modeling` still fires on CONTEXT.md/ADR work.

# What not to do

- Do not treat `dmmulroy/.dotfiles` as upstream for these skills. His lock already names mattpocock and trycua; two of the four trees drifted.
- Do not re-import the inlined one-question `ask_user` loop into `grilling`.
- Do not keep a Skill-tool `grill-me` trampoline "for compatibility" unless the user later asks for `/skill:grill-me`.
- Do not package `grill-with-docs` without `domain-modeling`.
- Do not copy `LOCAL.md`, Helium rules, `computer_` MCP examples, or Stow layout into this repo.
- Do not add Herdr integration to `cua-driver`.
- Do not vendor the 1123-line `SKILL.md` unchanged (validator will fail).
- Do not raise the 500-line cap to sneak it through.
- Do not run `npx skills update` as the update mechanism for these adapted trees ([`update-upstream-skills`](../skills/update-upstream-skills/SKILL.md)).
- Do not mention `workday-training`, `recipe-diagrams`, or other Mulroy first-party skills here; they are out of scope.

# Checks performed in this research pass

- Original trees enumerated from Git at the requested pins, not from GitHub's rendered README.
- Mulroy `fcdf060` compared file-by-file (SHA-256 and `git ls-tree`) against those pins.
- `.skill-lock.json` folder hashes matched to `git rev-parse <commit>:<path>`.
- Licenses read from GitHub's `license` field plus the actual `LICENSE` / `LICENSE.md` blobs.
- Pi skill loader, `disable-model-invocation`, 500-line validator, and packaged-link rule read from first-party docs and this repo's checker.
- No skill files, attribution files, or `upstream-skills.json` were modified. This note is documentation under `research/`.
