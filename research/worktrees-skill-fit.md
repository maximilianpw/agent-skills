# Would Dillon Mulroy's `worktrees` skill complement the copied Pi extension?

**Research record.** These findings compare the local Pi worktree extension with [`dmmulroy/.dotfiles`](https://github.com/dmmulroy/.dotfiles) `home/.agents/skills/worktrees` and with actual checkouts on this machine. This file is not agent instructions. It does not modify skills, extensions, or manifests.

**Updated 2026-09-14.** Inspected public `main` at commit [`fcdf06013853c2e8e5718b620d3a2b481fbcedb9`](https://github.com/dmmulroy/.dotfiles/commit/fcdf06013853c2e8e5718b620d3a2b481fbcedb9). Local Pi config is `/Users/max-vev/pi-config`, Home Manager-linked into `/Users/max-vev/.pi/agent`.

## Recommendation

**Skip** adding [`home/.agents/skills/worktrees`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees) to this repository.

The copied Pi extension and Mulroy's skill are a matched pair for one layout: a canonical repository root with `<repo>/.bare` as the shared Git directory and linked checkouts as direct children (`main`, `<topic>`). The extension already bundles the skill's create helper. The skill's remaining unique content is setup, conversion, prune, and repair of that layout.

This machine does not use that layout. Sampled personal and work clones are ordinary `.git` directories. Live linked checkouts are standard `git worktree add` directories whose `gitdir` files point at `<clone>/.git/worktrees/<name>`, including Herdr's default `~/.herdr/worktrees/<repo>/<branch-slug>`. On those trees, `/worktrees` fails before it can list, create, or remove anything. Installing the skill would not change that. It would teach conversion to a policy the user has not adopted, and its description would compete with Herdr's existing worktree commands.

**Adapt later only if a defined set of personal repos is converted to `.bare`.** Until that layout exists on disk, the complementary work is an extension/layout decision in `pi-config`, not a new skill here.

This tightens the earlier verdict in [`dmmulroy-upstream-skills.md`](dmmulroy-upstream-skills.md): that note said to mine the skill only if this stack later wanted a worktree skill. The extension has now been copied; the layout still has not.

## Scope and sources

Question: identify the worktree extension copied from Dillon Mulroy, document its files, commands, and assumptions, and decide whether `dmmulroy/.dotfiles` `home/.agents/skills/worktrees` at `fcdf060` would usefully complement it, given actual local repository layouts.

Primary sources, in order:

1. Local extension: [`/Users/max-vev/pi-config/extensions/pi-worktrees`](/Users/max-vev/pi-config/extensions/pi-worktrees), also resolved from [`/Users/max-vev/.pi/agent/extensions/pi-worktrees`](/Users/max-vev/.pi/agent/extensions/pi-worktrees). Documented in [`pi-config/README.md`](/Users/max-vev/pi-config/README.md).
2. Upstream extension and skill at [`dmmulroy/.dotfiles@fcdf060`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9):
   - [`home/.pi/agent/extensions/pi-worktrees`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.pi/agent/extensions/pi-worktrees)
   - [`home/.agents/skills/worktrees`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees)
3. Byte identity via `git hash-object` against GitHub blob SHAs at that commit.
4. Live checkouts under `/Users/max-vev`, `/Users/max-vev/Local`, and `/Users/max-vev/.herdr/worktrees`, inspected by reading `gitdir` pointer files and directory listings. `git` itself was not run against those working copies.
5. Herdr's default config (`herdr --default-config`) and [CLI reference, Worktrees](https://herdr.dev/docs/cli-reference/#worktrees). Local bindings in [`~/.config/herdr/config.toml`](/Users/max-vev/.config/herdr/config.toml).
6. This repo at HEAD: [`README.md`](../README.md), [`AGENTS.md`](../AGENTS.md), [`upstream-skills.json`](../upstream-skills.json). No `skills/worktrees/` exists. Global installs at `/Users/max-vev/.pi/agent/skills/` and `/Users/max-vev/.agents/skills/` also have no `worktrees` skill.

Secondary write-ups were not used except the earlier local note [`dmmulroy-upstream-skills.md`](dmmulroy-upstream-skills.md), which is a previous research record, not upstream.

# What was copied

The worktree extension the user referred to is **not** in `agent-skills`. It lives in Pi config:

| Path | Role |
| --- | --- |
| `/Users/max-vev/pi-config/extensions/pi-worktrees` | Editable source |
| `/Users/max-vev/.pi/agent/extensions/pi-worktrees` | Same tree; Home Manager link |

[`pi-config/README.md`](/Users/max-vev/pi-config/README.md) states that Home Manager links this tree into `~/.pi/agent`, that `/worktrees` is a notable local command, and that the manager "targets repositories using the canonical `.bare` plus linked-checkout layout. Its creation helper is bundled under `extensions/pi-worktrees/scripts/`." Root `package.json` includes `bun run --filter pi-worktrees-extension check`.

Copy origin: [`home/.pi/agent/extensions/pi-worktrees`](https://github.com/dmmulroy/.dotfiles/tree/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.pi/agent/extensions/pi-worktrees) at `fcdf060`. The create script was taken from the sibling skill, not from that extension package. Mulroy's extension originally resolved the helper as `join(homedir(), ".agents/skills/worktrees/scripts/new-worktree.sh")` ([`src/index.ts`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.pi/agent/extensions/pi-worktrees/src/index.ts)). The local copy inverted that dependency: the script is bundled next to the extension, so the skill is not required for create.

## Exact local files

| Local path | Git blob SHA | Match to `fcdf060` |
| --- | --- | --- |
| `src/worktree-command.ts` | `61caf0351af9134b79a4dec064cab63aa3d97e97` | identical to upstream extension |
| `src/worktree-command-runner.ts` | `243d300262190651cdab5b456e963bef1743c67c` | identical |
| `src/worktree-domain.ts` | `9ee1578a9334f0195f4722e7a8bb5f6d50703f99` | identical, including the `/skill:worktrees` error text |
| `src/worktree-manager-overlay.ts` | `4e1b9f506c4738a44cb469a053216ac46339086d` | identical |
| `src/worktree-service.ts` | `e3c7d287a661ad29ffd526caf3677d485f4ddf11` | identical |
| `src/git-worktree-output.test.ts` | `477b3b10323eba39921a52569581dcafb6d24448` | identical |
| `tsconfig.json` | `21a133b4607f2d795b08c3965c31386e86d9094c` | identical |
| `scripts/new-worktree.sh` | `c3b9004938efd39cd615915b3d93e0283202159d` | identical to **skill** helper, not present in upstream extension package |
| `src/index.ts` | `1e8fba31af1cc77adaeeb3b3ecb0a0276be99d7a` | **diverged** (bundled script URL) |
| `src/worktree-service.test.ts` | `6fd96c007b5a138d1f882a43309cefe778c84e65` | **diverged** (bundled script path) |
| `src/git-worktree-output.ts` | `5ef9bf4132f956774c30406009f89e411ce13a24` | **diverged** (omit empty optionals) |
| `package.json` | `76e3ee69935a600c6c841b63a78130e74616684a` | **diverged** (`bun run` check vs upstream `npm run`) |
| `index.ts` | local-only | root re-export: `export { default } from "./src/index.ts"` |

Upstream skill files at the same commit, **not** installed locally:

| Upstream path | Blob SHA | Size |
| --- | --- | --- |
| [`SKILL.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees/SKILL.md) | `e2a2d1fe25bef6ad213901d2c5132719ed6cbbd1` | 2099 |
| [`references/canonical-root.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees/references/canonical-root.md) | `6c9b0da52df3179eddd4c00339672df9c8ac3cff` | 1913 |
| [`scripts/new-worktree.sh`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees/scripts/new-worktree.sh) | `c3b9004938efd39cd615915b3d93e0283202159d` | 3738 |

Skill directory tree SHA: `38d022ca8601fb1fb6c2c354bef9c08f4dd783a8`. Introduced in [`78de1da9336a375737e4cba50b6389ce561b86fb`](https://github.com/dmmulroy/.dotfiles/commit/78de1da9336a375737e4cba50b6389ce561b86fb). No `LICENSE` in that skill. The upstream repo still has GitHub `license: null` and no root SPDX file.

Local porcelain-parser change: upstream `completeDraft` wrote `branch` / `lockedReason` / `prunableReason` as `draft.* ?? ""`. Local omits absent fields. That matches the already-identical test, which expects those keys missing on bare and detached records, and satisfies `exactOptionalPropertyTypes` in the shared `tsconfig.json`.

# Extension behavior

Entry: `pi.registerCommand("worktrees", …)` in [`src/index.ts`](/Users/max-vev/pi-config/extensions/pi-worktrees/src/index.ts). Description: "List, create, fetch, and safely remove linked Git worktrees".

## Commands and keys

`/worktrees` is TUI-only. In any other mode it notifies `"/worktrees requires Pi's interactive TUI mode"` and returns ([`worktree-command.ts`](/Users/max-vev/pi-config/extensions/pi-worktrees/src/worktree-command.ts)).

Overlay ([`worktree-manager-overlay.ts`](/Users/max-vev/pi-config/extensions/pi-worktrees/src/worktree-manager-overlay.ts)):

| Key | Action |
| --- | --- |
| `↑` / `↓` | Move selection |
| `a` | Create |
| `d` | Remove selected |
| `f` | Fetch |
| `r` | Refresh list |
| `esc` / `ctrl+c` | Close |

Create dialog prompts: branch (placeholder `dillon/topic`), local directory (last `/`-segment of the branch, sanitized), optional base (blank = remote default). It confirms, then calls the helper. Success notifies that the new path exists and that **the current Pi session stays in `ctx.cwd`**. There is no cd, no Herdr workspace, no editor switch.

Remove dialog blocks current, dirty, and locked worktrees. Choices are "Remove worktree only", optional "Remove worktree and merged local branch", or cancel. Branch delete uses `git branch -d` (merged-only). Failure to delete retains the branch and warns.

## Git operations

Implemented in [`GitWorktreeService`](/Users/max-vev/pi-config/extensions/pi-worktrees/src/worktree-service.ts), executed argument-safe through `pi.exec` ([`PiWorktreeCommandRunner`](/Users/max-vev/pi-config/extensions/pi-worktrees/src/worktree-command-runner.ts)):

| Operation | Command |
| --- | --- |
| Discover root | `git -C <cwd> rev-parse --path-format=absolute --git-common-dir`, then `git -C <root> rev-parse --is-bare-repository` |
| List | `git -C <root> worktree list --porcelain -z` |
| Status per linked tree | `git -C <path> status --porcelain=v1 --untracked-files=normal` |
| Fetch | `git -C <root> fetch --prune origin` (hardcoded `origin`, unlike the helper) |
| Create | bundled `new-worktree.sh <localDirectory> <branch> [base]` |
| Remove | `git -C <root> worktree remove <localDirectory>` |
| Optional branch cleanup | `git -C <root> branch -d <branch>` |

`localDirectory` must be one direct child of the root: non-empty, not `.` / `..`, no `/` or `\`. Branch must be non-empty and must not start with `-`. The helper additionally runs `git check-ref-format --branch`.

## Helper decision order

[`scripts/new-worktree.sh`](/Users/max-vev/pi-config/extensions/pi-worktrees/scripts/new-worktree.sh), byte-identical to the skill helper:

1. Reuse local `refs/heads/<branch>` if present: `git worktree add -- <dir> <branch>`.
2. Else if `WORKTREE_REMOTE` (default `origin`) has `refs/remotes/<remote>/<branch>`: `git worktree add --track -b <branch> -- <dir> <remote>/<branch>`.
3. Else create `--no-track -b <branch>` from `[base]`, or from `<remote>/HEAD`, else local `main`, else local `master`.

It fetches and prunes the remote first when that remote exists. `WORKTREE_ROOT` overrides discovery. Destination `$root/$local_dir` must not already exist.

Tests ([`worktree-service.test.ts`](/Users/max-vev/pi-config/extensions/pi-worktrees/src/worktree-service.test.ts)) build a fixture that follows the skill's setup recipe (`clone --bare .bare`, `gitdir: ./.bare`, fetch refspec, reflogs, relative worktree paths, `worktree add main`). A second test asserts a standard `git init` clone is rejected as `CanonicalWorktreeRootNotFound`.

## Assumptions the extension will not relax

From [`discoverWorktreeRoot`](/Users/max-vev/pi-config/extensions/pi-worktrees/src/worktree-service.ts) and [`CanonicalWorktreeRootNotFound`](/Users/max-vev/pi-config/extensions/pi-worktrees/src/worktree-domain.ts):

1. `git rev-parse --git-common-dir` from `cwd` succeeds.
2. That directory's basename is exactly `.bare`.
3. The parent of `.bare` is a bare repository (`rev-parse --is-bare-repository` prints `true`).
4. Linked checkouts live under that parent; create/remove names are single path segments.
5. Fetch talks to `origin`.
6. The user is in Pi TUI mode.
7. Setup guidance lives at `/skill:worktrees`.

Failure message, unchanged from upstream:

```text
Canonical worktree root not found from <cwd>; run /skill:worktrees for setup guidance.
```

That pointer is currently dangling: no `worktrees` skill is installed globally, and this repository does not package one. Pi skills in this stack are model-invoked from `~/Local/agent-skills`, not a `/skill:worktrees` command.

The extension does **not** convert clones, write `gitdir: ./.bare`, set `remote.origin.fetch` / `core.logAllRefUpdates` / `worktree.useRelativePaths`, prune stale registrations, or run `git worktree repair`. Those steps exist only in the skill's [`canonical-root.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees/references/canonical-root.md).

# What the upstream skill adds

[`SKILL.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees/SKILL.md) description:

> Manage Git worktrees in a canonical `.bare` repository root. Use when creating, reusing, listing, removing, or repairing worktrees, or when setting up a repository to keep all branch checkouts under one root.

Body:

- Layout diagram: `<repo>/.git` → `gitdir: ./.bare`; `<repo>/.bare`; `<repo>/main`; `<repo>/<topic>`.
- Create by running `scripts/new-worktree.sh` from a linked worktree or the root; complete when `git worktree list` contains the path and `git status` is clean unless the branch already carried changes.
- Remove only after accounting for staged, unstaged, and untracked changes; then `git -C <repo> worktree remove <local-dir>`; delete the branch only when commits are integrated or intentionally discarded.
- Setup/recovery: read `references/canonical-root.md`.

[`canonical-root.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees/references/canonical-root.md) is the unique document:

- New root: `git clone --bare <url> .bare`, `printf 'gitdir: ./.bare' >.git`, `remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*`, `core.logAllRefUpdates=true`, `worktree.useRelativePaths=true`, fetch, `remote set-head origin --auto`, `worktree add main main`, set upstream.
- Invariants to re-check with those same git-config getters plus `worktree list --verbose`.
- Stale registrations: `git worktree prune --dry-run --verbose` before prune.
- Moved roots: `git worktree repair`, then verify list and status.
- Existing clones: do not rearrange live metadata in place; prefer a fresh canonical root and move commits through Git.

Create/remove overlap with the extension is high. Conversion/repair overlap is zero. The skill is the setup half of Mulroy's original pair; the local copy kept the runtime half and the helper, and dropped the skill.

# Canonical `.bare` vs actual local repositories

No sampled tree is a canonical root. Evidence is directory shape plus `gitdir` pointer files, not `git worktree list` (sandbox blocks git against `.git`).

## Ordinary clones (`.git` is a directory)

These fail discovery immediately: common-dir basename is `.git`, not `.bare`.

| Path | `.git` |
| --- | --- |
| `/Users/max-vev/pi-config` | directory |
| `/Users/max-vev/Local/agent-skills` | directory |
| `/Users/max-vev/nix-config` | directory |
| `/Users/max-vev/Local/vev-cli` | directory |
| `/Users/max-vev/Local/stocket` | directory |
| `/Users/max-vev/Local/vev/ai-core` | directory |
| `/Users/max-vev/Local/vev/vev-docker-compose` | directory |

`/Users/max-vev/nix-config-worktrees` exists and is empty (created 2026-07-04). It is not a `.bare` root.

Depth-4 searches under `Local`, `pi-config`, `nix-config`, and `.herdr` found no `.bare` directories and no `gitdir: ./.bare` files.

## Standard linked worktrees (Herdr and sibling folders)

Herdr default config:

```toml
# [worktrees]
# directory = "~/.herdr/worktrees"
```

[CLI reference](https://herdr.dev/docs/cli-reference/#worktrees): without `--path`, `herdr worktree create` places the checkout at `<worktrees.directory>/<repo>/<branch-slug>`, runs ordinary `git worktree` against the parent clone, opens a Herdr workspace, and groups it with the parent. `worktree remove` runs `git worktree remove` and never deletes the branch.

Local Herdr bindings ([`config.toml`](/Users/max-vev/.config/herdr/config.toml)): `new_worktree = "prefix+shift+t"`, `open_worktree = "prefix+t"`, `remove_worktree = "prefix+alt+t"`.

Observed `gitdir` pointers:

| Checkout | `gitdir` target |
| --- | --- |
| `~/.herdr/worktrees/stocket/worktree-clear-field-3f12` | `/Users/max-vev/Local/stocketfr/stocket/.git/worktrees/worktree-clear-field-3f12` (target clone missing) |
| `~/.herdr/worktrees/stocket/worktree-green-stone-03f3` | `/Users/max-vev/Local/stocketfr/stocket/.git/worktrees/worktree-green-stone-03f3` (same, stale) |
| `~/.herdr/worktrees/vev-docker-compose/scan-pay` | `/Users/max-vev/Local/vev/vev-docker-compose/.git/worktrees/scan-pay` |
| `~/.herdr/worktrees/vev-dashboard/pdf-integration` | `/Users/max-vev/Local/vev/vev-docker-compose/.git/modules/submodules/vev-dashboard/worktrees/pdf-integration` (submodule worktree) |
| `Local/stocket-herdr/01-prepared-dialog` | `/Users/max-vev/Local/stocket/.git/worktrees/01-prepared-dialog` |
| `Local/stocket-herdr/05-invitation-screen` | `/Users/max-vev/Local/stocket/.git/worktrees/05-invitation-screen` |
| `Local/stocket-herdr/prs-191-tenant-lifecycle-support-access` | `/Users/max-vev/Local/stocket/.git/worktrees/prs-191-tenant-lifecycle-support-access` |
| `Local/stocket-herdr/verify-stocket-skill` | `/Users/max-vev/Local/stocket/.git/worktrees/verify-stocket-skill` |

`~/.herdr/worktrees/ai-core` and `vev-server` are empty placeholders. `Local/vev-workspaces/*` look like dashboard trees but have no `.git` file at the workspace root (copies or another VCS, not canonical `.bare`).

For every live linked checkout above, Git's common dir is the **parent clone's `.git` (or a submodule `.git`)**, basename `.git`. The extension's `.bare` check rejects them. The helper's same check rejects them unless `WORKTREE_ROOT` is forced at a bare repo that does not exist.

Consequence: `/worktrees` cannot list Herdr worktrees, cannot create beside them, and cannot remove them. Herdr already owns that loop, including dirty-tree `--force` and "never delete the branch."

# Would the skill complement the extension?

## What would actually complement

Only [`canonical-root.md`](https://github.com/dmmulroy/.dotfiles/blob/fcdf06013853c2e8e5718b620d3a2b481fbcedb9/home/.agents/skills/worktrees/references/canonical-root.md) plus the skill's completion checks. That is the missing setup/recovery half, and it is the only text that makes the dangling `/skill:worktrees` error honest.

The create helper is already local. Create/remove policy is already in the extension, and is stricter than the skill on current/locked/dirty trees.

## Why that complement is not useful on this machine today

1. **No consumer layout.** Complement is conversion guidance. Conversion is a destructive personal-repo migration. Sampled repos, including the Pi config and this skills repo, are still standard clones. Employer trees (`Local/vev/*`, `Local/stocket`) are even worse candidates: submodule worktrees, Herdr grouping, stale `stocketfr` pointers.
2. **Herdr already covers the real workflow.** Default directory, CLI, and keybindings create/open/remove ordinary linked worktrees and wrap them as workspaces. The local `herdr` skill is already installed and is stricter about invocation. Mulroy's skill description ("creating, reusing, listing, removing, or repairing worktrees") would fire on that work.
3. **Installing the skill does not make `/worktrees` work.** Discovery still requires `.bare`. The skill would instruct agents to convert; the extension would still fail until conversion finished.
4. **Script duplication.** Mulroy's pair had one helper, owned by the skill. Local already owns that helper in `pi-config`. Copying `scripts/new-worktree.sh` into `skills/worktrees/` would fork it.
5. **Repository scope.** This repo already carries personal host tooling (`remote-development` / Fleet), so a worktree skill is not automatically out of inventory. The block is layout mismatch and invocation theft, not "host tooling is forbidden."
6. **License.** Same as other Mulroy first-party adaptations: no SPDX on the source repo; README says fork and adapt. Any later adaptation needs ATTRIBUTION language that records that, not an invented LICENSE file.

# Verdicts

## Skip (now)

Do not add `skills/worktrees/` to this repository. Do not copy `SKILL.md`, `references/canonical-root.md`, or a second `new-worktree.sh`. Do not add an `upstream-skills.json` entry for this path. That matches, and is now stronger than, [`dmmulroy-upstream-skills.md`](dmmulroy-upstream-skills.md).

Do not treat the dangling `/skill:worktrees` string as a reason to package the skill. If that message should change, it belongs in `pi-config` (`worktree-domain.ts`), pointing at real local policy (Herdr, or an explicit conversion runbook), not at a skill that would teach the wrong default.

## Adapt (only after a layout decision)

Gate: at least one personal repo that Pi actually opens (`pi-config`, `nix-config`, or `agent-skills`) is converted to the canonical root and `/worktrees` lists it. Do not convert VEV or Stocket trees as a side effect of wanting a skill.

If that gate passes, adapt — do not vendor verbatim. Concrete scope:

1. `skills/worktrees/SKILL.md` + `references/canonical-root.md` only. No `scripts/`.
2. Description must name **canonical `.bare` conversion, invariant repair, prune, and `git worktree repair`**. It must not trigger on ordinary `git worktree`, Herdr `worktree create/open/remove`, or "give the delegate a worktree" in `model-routing`.
3. Create/remove steps should point at the bundled helper (`~/pi-config/extensions/pi-worktrees/scripts/new-worktree.sh` or `/worktrees` in TUI), not duplicate decision order.
4. Keep the conversion warning: preserve unpublished state; prefer a fresh root over rewriting a live `.git`.
5. ATTRIBUTION to `dmmulroy/.dotfiles` at `fcdf060`, recording the missing SPDX license.
6. `upstream-skills.json` entry with `upstreamPaths: ["home/.agents/skills/worktrees"]` and no `exactFiles` for the helper (local copy lives in `pi-config`).
7. Follow-up in `pi-config`, not here: retarget `CanonicalWorktreeRootNotFound` away from `/skill:worktrees`; consider making extension fetch honor `WORKTREE_REMOTE` the way the helper already does.

## Do not do

- Do not add the skill so that `/worktrees` "has docs" while every real cwd still errors.
- Do not rewrite the extension from this repository. Layout support for standard clones or `~/.herdr/worktrees` is a `pi-config` change.
- Do not replace Herdr worktrees with `.bare` children for VEV/Stocket.
- Do not restore Mulroy's `homedir()/.agents/skills/worktrees/scripts/...` path; the local bundle is the better seam.

# Checks

- Upstream skill and extension files hashed against GitHub blobs at `fcdf060`.
- Local layout claims come from directory listings and `gitdir` pointer files, not from running `git worktree list` (blocked in this environment). Absence of `.bare` is therefore "not observed under the sampled trees," not a proof that none exists elsewhere on disk.
- No skill files, attribution files, `upstream-skills.json`, or Pi extension sources were modified.
- Structural repo check not required: documentation-only note under `research/`.
