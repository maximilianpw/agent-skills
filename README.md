# Agent Skills

Personal agent skills maintained by [Maximilian Pinder-White](https://github.com/maximilianpw).

## Install

The maintainer's machines install these skills from sources pinned in nix-config. Everyone else can install every skill globally with the [Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add maximilianpw/agent-skills --global --skill '*' --yes
```

List the available skills without installing them:

```bash
npx skills add maximilianpw/agent-skills --list
```

Install the upstream Matt Pocock skills used alongside this collection:

```bash
npx skills add mattpocock/skills --global \
  --skill code-review \
  --skill domain-modeling \
  --skill grill-me \
  --skill tdd \
  --yes
```

Update installed skills:

```bash
npx skills update --global
```

## Skills

- `babysit-pr` — monitor CI and review feedback with a bounded, resumable PR watcher.
- `cloudflare-composition-root` — keep Cloudflare bindings, runtime lifetimes, and platform types at their owning boundaries.
- `coding-standards` — shared engineering rules with conditional TypeScript, Effect/Alchemy, React, and NestJS references.
- `council` — gather independent reviews from two model providers within a fixed round budget.
- `cua-helium` — operate Helium on macOS or Linux through the `computer` MCP server (Cua Driver).
- `file-pr` — prepare or publish concise, problem-first PRs under explicit authorization.
- `leaving-pr-comments` — attribute agent-authored GitHub replies and verify their publication.
- `model-routing` — select models for workflows, subagents, and independent reviews.
- `modernize` — reassess an old PR's intent and relevance before rebasing it.
- `project-verification` — create or maintain a project-local harness and feature map that prove behavior on the real user surface.
- `remote-development` — operate remote development machines through the Fleet CLI.
- `takeover` — continue inherited work while preserving intent and contributor credit.
- `write-discoverable-code` — make names, modules, errors, and events easy to find through search.

Pi can also load this repository directly as a package because `package.json` exposes `skills/` through `pi.skills`.

## Requirements

`cua-helium` expects Helium and the `computer` MCP server, which nix-config declares for every agent harness. `model-routing` expects CLIProxyAPI and its documented `pi-config` fallback. `remote-development` expects the personal Fleet CLI and generated Fleet configuration. Matt Pocock's `code-review`, `domain-modeling`, `grill-me`, and `tdd` skills are installed directly from [`mattpocock/skills`](https://github.com/mattpocock/skills) rather than being republished here. `cloudflare-composition-root` and `write-discoverable-code` use `coding-standards` for shared coding rules; install it alongside either skill. Working agreements and execution permissions belong to the consuming agent's global/repository policy, not this package. These integrations are deliberate prerequisites, not bundled services.

The adapted tstack PR skills use authenticated `gh`; `babysit-pr` also needs Python 3 on macOS/Linux and a cancellable command runner. Install `leaving-pr-comments` alongside `file-pr`, `modernize`, or `babysit-pr`; `takeover` uses all four. `council` depends on `model-routing` and a harness capable of read-only delegates on the selected models. The council roster is maintained in `model-routing`, not hardcoded in the workflow. Upstream `full-send`, `full-stop`, and `sol-loop` are intentionally excluded.

## Development

Run the structural checks with the repository's supported Node.js version:

```bash
npm run check
```

The check validates the repository's current, single-line skill frontmatter format, packaged relative Markdown links, the README inventory, Pi discovery path, and optional OpenAI metadata. It does not grade instruction quality, parse general YAML or every Markdown construct, or fetch external links.

This repository contains static skill files and has no runtime service or deployment target. Consumer execution is a separate integration check: use a reviewed Skills CLI in an isolated environment rather than installing into user or shared state during repository validation.

## Layout

Each public skill lives under `skills/<name>/` and follows the [Agent Skills specification](https://agentskills.io/specification).

Third-party skills are not vendored here. Install them from their upstream repositories with the Skills CLI so their source and update history remain intact. Adapted work retains its upstream license and attribution inside the skill directory.

`upstream-skills.json` inventories adapted skills and their source paths. Run `npm run check:upstreams` or use the repository-local `update-upstream-skills` skill to check every attribution pin and exact-copy file for drift. The maintenance skill lives under `.agents/skills/`, is marked internal for the Skills CLI, and is not part of this package's public skill inventory.
