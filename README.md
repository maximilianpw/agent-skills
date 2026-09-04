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

Update installed skills:

```bash
npx skills update --global
```

## Skills

- `effect-standards` — production Effect standards, including focused Alchemy runtime and infrastructure guidance.
- `model-routing` — select models for workflows, subagents, and independent reviews.
- `nestjs-standards` — production NestJS standards for modules, HTTP boundaries, security, testing, and operations.
- `react-standards` — production React UI standards, including TanStack and Vite guidance.
- `remote-development` — operate remote development machines through the Fleet CLI.
- `typescript-standards` — pragmatic production TypeScript standards, independent of any framework.
- `write-discoverable-code` — make names, modules, errors, and events easy to find through search.

Pi can also load this repository directly as a package because `package.json` exposes `skills/` through `pi.skills`.

## Requirements

`model-routing` expects CLIProxyAPI and its documented `pi-config` fallback. `remote-development` expects the personal Fleet CLI and generated Fleet configuration. These integrations are deliberate prerequisites, not bundled services.

## Development

Run the structural checks with the repository's supported Node.js version:

```bash
npm run check
```

The check validates the repository's current, single-line skill frontmatter format, packaged relative Markdown links, the README inventory, Pi discovery path, and optional OpenAI metadata. It does not grade instruction quality, parse general YAML or every Markdown construct, or fetch external links.

This repository contains static skill files and has no runtime service or deployment target. Consumer execution is a separate integration check: use a reviewed Skills CLI in an isolated environment rather than installing into user or shared state during repository validation.

## Layout

Each first-party skill lives under `skills/<name>/` and follows the [Agent Skills specification](https://agentskills.io/specification).

Third-party skills are not vendored here. Install them from their upstream repositories with the Skills CLI so their source and update history remain intact. Adapted work retains its upstream license and attribution inside the skill directory.
