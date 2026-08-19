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
- `react-standards` — production React UI standards, including TanStack and Vite guidance.
- `remote-development` — operate remote development machines through the Fleet CLI.
- `typescript-standards` — pragmatic production TypeScript standards, independent of any framework.
- `write-discoverable-code` — make names, modules, errors, and events easy to find through search.

Pi can also load this repository directly as a package because `package.json` exposes `skills/` through `pi.skills`.

## Layout

Each first-party skill lives under `skills/<name>/` and follows the [Agent Skills specification](https://agentskills.io/specification).

Third-party skills are not vendored here. Install them from their upstream repositories with the Skills CLI so their source and update history remain intact. Adapted work retains its upstream license and attribution inside the skill directory.
