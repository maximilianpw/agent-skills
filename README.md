# Agent Skills

Personal agent skills maintained by [Maximilian Pinder-White](https://github.com/maximilianpw).

## Install

Install every skill globally with the [Skills CLI](https://github.com/vercel-labs/skills):

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
  --skill grilling \
  --yes

npx skills add https://github.com/cursor/plugins/tree/main/pstack/skills/tdd \
  --global \
  --yes
```

Update installed skills:

```bash
npx skills update --global
```

## Skills

- `cloudflare-composition-root` — keep Cloudflare bindings, runtime lifetimes, and platform types at their owning boundaries.
- `cua-helium` — operate Helium on macOS or Linux through the local Cua Driver computer server.
- `effect-standards` — production Effect standards, including focused Alchemy runtime and infrastructure guidance.
- `model-routing` — select models for workflows, subagents, and independent reviews.
- `nestjs-standards` — production NestJS standards for modules, HTTP boundaries, security, testing, and operations.
- `project-verification` — create or maintain a project-local harness and feature map that prove behavior on the real user surface.
- `react-standards` — production React UI standards, including TanStack and Vite guidance.
- `remote-development` — operate remote development machines through the Fleet CLI.
- `typescript-standards` — pragmatic production TypeScript standards, independent of any framework.
- `write-discoverable-code` — make names, modules, errors, and events easy to find through search.

Pi can also load this repository directly as a package because `package.json` exposes `skills/` through `pi.skills`.

## Requirements

`cua-helium` expects Helium, the upstream `cua-driver` skill, and either the `computer` MCP server from `pi-config` or the `cua-driver` CLI. `model-routing` expects CLIProxyAPI and its documented `pi-config` fallback. `remote-development` expects the personal Fleet CLI and generated Fleet configuration. Matt Pocock's `code-review`, `domain-modeling`, and `grilling` skills are installed directly from [`mattpocock/skills`](https://github.com/mattpocock/skills), and pstack's `tdd` skill is installed directly from [`cursor/plugins`](https://github.com/cursor/plugins/tree/main/pstack/skills/tdd), rather than being republished here. These integrations are deliberate prerequisites, not bundled services.

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
