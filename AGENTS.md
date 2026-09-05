# Agent skills repository guidance

## Purpose and ownership

This repository packages static, reusable agent skills. `skills/<name>/SKILL.md`
is each skill's progressively disclosed entry point; supporting detail belongs
in that skill's `references/`. Optional `agents/openai.yaml` supplies interface
metadata. `package.json` exposes `./skills` to Pi.

- Keep root guidance about repository maintenance, not the workflows taught by
  individual skills. Do not copy every skill's rules here or into `README.md`.
- Keep each skill self-contained: relative Markdown links must resolve within
  its directory. Do not vendor third-party skills; preserve license and
  attribution files for adapted material.
- Keep `README.md`'s concise skill inventory synchronized with directory names.
  Use the Agent Skills specification linked there for package semantics.

## Local workflow and checks

CI uses Node.js 22 and has no install step. Local editing and validation are safe
without asking.

- Validate repository structure and links:
  `node scripts/validate-skills.mjs`.
- When changing the validator:
  `node --test scripts/validate-skills.test.mjs`.
- Full repository check: `npm run check`.
- Documentation-only changes outside skill packaging: `git diff --check`.

The validator enforces discoverability and package integrity, not instruction
quality. For skill changes, also inspect the rendered Markdown, confirm the
description triggers only the intended workflow, and keep the entry point brief
by linking conditional detail. Completion means applicable checks pass after
fixes, the final diff is reviewed, and skipped checks are reported.

## Boundaries

- Do not install or update skills in user/global state as repository validation.
- Do not invoke external providers, CLIs, remote machines, or operational
  services described by a skill while maintaining its static content.
- Never add credentials, tokens, private machine details, captured responses, or
  generated installation output.
