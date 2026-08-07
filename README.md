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

- `add-fleet-host` — add a trusted machine to the declarative nix-config fleet.
- `remote-development` — operate remote development machines through the Fleet CLI.
- `typescript-standards` — pragmatic TypeScript standards with Effect guidance gated per package or explicit request.
- `write-discoverable-code` — make names, modules, errors, and events easy to find through search.

## Layout

Each first-party skill lives under `skills/<name>/` and follows the [Agent Skills specification](https://agentskills.io/specification).

Third-party skills are not vendored here. Install them from their upstream repositories with the Skills CLI so their source and update history remain intact. Adapted work retains its upstream license and attribution inside the skill directory.
