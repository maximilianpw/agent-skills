# Adapting pstack into this repository

**Research record.** These findings informed [`project-verification`](../skills/project-verification/SKILL.md). This file is not agent instructions.

**Updated 2026-09-01.** pstack version `0.14.5` on `cursor/plugins` main, commit [`b9ddc83c32972210b8a94d389130713e8eed346e`](https://github.com/cursor/plugins/commit/b9ddc83c32972210b8a94d389130713e8eed346e). First-party commentary is Lauren Tan's 2026-08-31 X post, [status/2094457600259842065](https://x.com/poteto/status/2094457600259842065).

## Recommendation

Do not vendor pstack. Do not copy `/poteto-mode`, the 21 principle skills, `/setup-pstack`, Graphite shipping, or Cursor cloud-agent fan-out.

The one mechanism this stack does not already have, and the one Tan treats as infrastructure rather than a nice extra, is **project-local verification skill generation plus a maintenance loop**. That is the first slice.

A later, smaller second slice can add a thin user-invoked router that names *this* stack's existing skills. That is the `/poteto-mode` idea after you strip Lauren's style, Cursor APIs, and the 22-playbook catalog. It is not the first PR.

Steal interrogate's multi-model consensus rule into the existing `code-review` plus `model-routing` pair if a third slice is ever worth it. Do not add a fourth review skill.

**Working tree at write time.** HEAD still has no verification generator. While this note was being researched, an uncommitted `skills/project-verification/` appeared, plus a one-line README list entry. Those files were not written by this research pass and were not edited here. They already aim at slice 1: one model-invoked skill with Create and Maintain branches, harness-agnostic placement, Lauren Tan MIT attribution at commit `b9ddc83`. Review that candidate against the slice below instead of starting a second generator. It is not in HEAD, so the gap analysis still describes the committed repo.

## Scope and sources

Question: which pstack mechanisms are worth adapting into `/Users/max-vev/Local/agent-skills`, given the skills already in this repo and the ones already loaded globally for pi.

Primary sources, in order:

1. pstack itself, cloned from [`cursor/plugins` `pstack/`](https://github.com/cursor/plugins/tree/main/pstack) on 2026-09-01. Plugin metadata is [`.cursor-plugin/plugin.json`](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json). License is [`pstack/LICENSE`](https://github.com/cursor/plugins/blob/main/pstack/LICENSE).
2. First-party guide under [`pstack/docs/guide/`](https://github.com/cursor/plugins/tree/main/pstack/docs/guide).
3. Tan's X post, [The Complete Guide to pstack Pt. 1](https://x.com/poteto/status/2094457600259842065), plus the example she links, [`poteto/verification-skill-example`](https://github.com/poteto/verification-skill-example).
4. This repo at HEAD: [`README.md`](../README.md), [`LICENSE`](../LICENSE), [`package.json`](../package.json), and the committed skills under [`skills/`](../skills/). The dirty `skills/project-verification/` tree is called out separately and was not used as a primary source for the gap analysis.
5. Global pi policy at [`/Users/max-vev/.pi/agent/AGENTS.md`](/Users/max-vev/.pi/agent/AGENTS.md) and the installed skill trees at `/Users/max-vev/.pi/agent/skills/` and `/Users/max-vev/.agents/skills/`.

This repo has no `AGENTS.md` of its own. The policy that actually binds a pi session is the global file above. Secondary write-ups of pstack were not used.

# What pstack is

pstack is Lauren Tan's Cursor plugin. Version `0.14.5`, MIT, author field `Lauren Tan`. The README states the goal as writing less, higher-quality code, and using multi-model workflows. Install is Cursor-only: `/add-plugin pstack`. ([`pstack/README.md`](https://github.com/cursor/plugins/blob/main/pstack/README.md), [plugin.json](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json))

The runtime shape is a sticky mode plus a pile of leaf skills:

- [`/poteto-mode`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) matches a prompt to a playbook, copies that playbook's steps into a todo list verbatim, and calls other skills as those steps fire. The first todo is always "read the Principles section". ([guide 02](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/02-poteto-mode.md))
- Twenty-two named playbooks live under [`skills/poteto-mode/playbooks/`](https://github.com/cursor/plugins/tree/main/pstack/skills/poteto-mode/playbooks). A twenty-third file, [`opening-a-pr.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/opening-a-pr.md), is the shared tail every other playbook calls.
- Twenty-one `principle-*` skills are indexed inline in poteto-mode. The agent is supposed to name each principle that changed a decision. ([guide 08](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/08-principles.md))
- A Cursor subagent type, [`poteto-agent`](https://github.com/cursor/plugins/blob/main/pstack/agents/poteto-agent.md), exists so spawned workers reread poteto-mode. Substituting `generalPurpose` is called out as drift.

The X post's actual claim, once you ignore the 2,000 PRs and 100-1000x lines, is narrower. Verification is the bottleneck. If an agent can drive the real app, capture evidence, and keep going until the check passes, the human stops being the loop. Everything else in pstack composes onto that. ([X post](https://x.com/poteto/status/2094457600259842065))

That is the part worth taking seriously. "Fearless parallelism" in the README is the marketing wrapper around the same idea. You parallelize after you trust the check, not before.

# Comparison by mechanism

## Router and playbooks

pstack's router is `/poteto-mode`. The mechanism is specific:

1. Open a todo list. First item is the principles index.
2. Match the task to one playbook file.
3. Copy that file's numbered steps in verbatim, before any task-specific todos, before reasoning about the task.
4. A skipped step stays in the list as `skip: <reason>`. Silent skips are forbidden.
5. Route to other skills as steps fire (`how`, `architect`, `arena`, `interrogate`, `tdd`, `unslop`, and so on).
6. Stay sticky across turns until the user opts out. "new task" forces a rematch.

Source: [`skills/poteto-mode/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) "Playbooks" section, plus [guide 02](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/02-poteto-mode.md).

The Feature playbook is the template for code work: `how` the subsystem, `architect` the shape, write a four-item throughput checkpoint, delegate implementation to a subagent, verify on the matching surface, then open a PR. Skipping `architect` has to stay visible. ([`playbooks/feature.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/feature.md))

The Bug fix playbook is scientific. Reproduce on the real surface, binary-search the cause with runtime evidence, plan, verify the original repro, stage failing-then-passing history. Belt-and-suspenders that "might help" does not ship. ([`playbooks/bug-fix.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md))

When nothing fits, or the work is a large migration the human will review later, [`figure-it-out`](https://github.com/cursor/plugins/blob/main/pstack/skills/figure-it-out/SKILL.md) designs a bespoke playbook with a falsifiable done predicate, a harness built before the work, and a decision trail.

**What this repo and the global pi skills already do.** There is no sticky mode and no playbook catalog. There is a much thinner stack:

- Global [`AGENTS.md`](/Users/max-vev/.pi/agent/AGENTS.md) is the always-on policy. Inspect and plan for substantial work. Implement routine changes directly. Run the smallest relevant check. Load `model-routing` before any subagent.
- [`implement`](/Users/max-vev/.agents/skills/implement/SKILL.md) is a four-line router: TDD at agreed seams, typecheck often, `/code-review` at the end, commit.
- [`diagnosing-bugs`](/Users/max-vev/.agents/skills/diagnosing-bugs/SKILL.md) owns hard bugs. Its real content is "build a tight pass/fail loop first."
- [`writing-for-agents`](/Users/max-vev/.pi/agent/skills/writing-for-agents/SKILL-MECHANICS.md) already defines a **router skill**: one user-invoked skill that names the others and when to reach for each, so the human remembers one name. It also says a router can only hint at other user-invoked skills, never fire them.

`implement` is a router that is too small. `poteto-mode` is a router that is too large and too personal. The useful idea sits between them: copy steps from a short named playbook, keep skips visible, do not invent a bespoke plan that drops the named gates.

Copying the 22-playbook set would fight this repo on purpose. Babysit, Shipping, Autopilot-full, Autopilot-stack, Orchestrate, Worktree cleanup, and Session pickup are Cursor-plus-Graphite operations. Visual parity, hillclimb, and the two forensics playbooks are real, but they are not the missing piece.

Tan also says she does not believe in planning, and that Cursor's plan mode is enough if you want it. ([README, "why are there no planning skills?"](https://github.com/cursor/plugins/blob/main/pstack/README.md)) This stack already plans. `grill-me`, `improve`, and the global AGENTS.md plan-before-substantial-work rule are the opposite bet. Do not import her anti-planning stance. Import the "verbatim steps, visible skips" discipline.

## Verification skill generation and maintenance

This is pstack's highest-value mechanism, and Tan says so in the first-party post. She calls a good verification skill "critical infrastructure." The generator is a meta-skill distilled from the verify skills used on Grok Bot and Cursor. ([X post](https://x.com/poteto/status/2094457600259842065), [guide 06](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/06-verify-and-ship.md))

[`create-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md) does this:

1. Interview the repo, not the user. Surface, run command, drive harness, evidence, isolation. Ask only what the code cannot answer.
2. Write a project-local skill with Launch, Doctor, Drive, Evidence, Cleanup, Helpers. No placeholders.
3. Seed a feature map. README index plus one file per user-facing feature. Required H2s: `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, `Gotchas`. Worked example: [`references/feature-map-example/`](https://github.com/cursor/plugins/tree/main/pstack/skills/create-verification-skill/references/feature-map-example).
4. Prove the generated skill once end to end on one mapped feature. Evidence must survive cleanup. An unrun skill is a draft.
5. Point at `/maintain-verification-skill`.

[`maintain-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md) is the upkeep loop. One read-only source reader per feature in parallel, then one live pass that drives every feature. Outcomes are exactly `clean`, `changed`, or `blocked`. It may only edit the verify skill's own directory. Product regressions get reported, not papered over in the map.

The X post adds two implementation details the SKILL.md implies but the post makes explicit:

- **Build a small CLI**, not just markdown. Tan's "Build the Lever" principle applied to verification. Agents run `control-app doctor` instead of writing a throwaway click script. She wants composable subcommands, `--dry-run` on destructive actions, descriptive errors, rich `--help`, JSON output.
- **Feature maps are materialized memory.** Compact, searchable, user-POV. The codebase is the source of truth. The map is the token-cheap projection. Maintain it daily, or it rots.

The public example is [`poteto/verification-skill-example`](https://github.com/poteto/verification-skill-example). Fictional Atlas app, ~30 feature files, driver scripts omitted on purpose. The shape is the point.

pstack writes the generated skill to `.cursor/skills/verify-<app>/`. That path is Cursor-specific and should not be copied. The *contents* of the skill are portable.

**What already exists here.** Nothing generates a durable, project-local verify skill.

Closest substitutes, and why they are not the same thing:

- Global AGENTS.md says "run the smallest relevant verification and report anything skipped." That is a per-task habit, not a repo artifact the next agent can load cold.
- [`diagnosing-bugs`](/Users/max-vev/.agents/skills/diagnosing-bugs/SKILL.md) builds a tight loop for one bug, then throws the loop away.
- [`tdd`](/Users/max-vev/.agents/skills/tdd/SKILL.md) (global) is a red-green discipline at agreed seams. [`pstack tdd`](https://github.com/cursor/plugins/blob/main/pstack/skills/tdd/SKILL.md) is narrower, a cheap failing regression test for a bug. Neither maps user-facing features or drives the running app.
- [`blast-radius`](/Users/max-vev/.pi/agent/skills/blast-radius/SKILL.md) proves one safety fact by running code. It is a review tool, not an app driver.
- [`principle-prove-it-works`](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-prove-it-works/SKILL.md) is the pstack rule "check the real artifact." This stack believes that. It has no generator that makes the artifact checkable.

The gap is exactly the durable pair: a generator that writes Launch/Doctor/Drive/Evidence/Cleanup plus a feature map, and a maintainer that keeps the map honest. That pair is missing from both this repo and the global pi skills.

## Principles

pstack ships 21 one-principle skills, grouped as core, architecture, verification, delegation, and meta. poteto-mode indexes them inline. Humans steer by saying the name. The agent has to name the principle and the decision it changed, or the citation is treated as name-dropping. ([README principles table](https://github.com/cursor/plugins/blob/main/pstack/README.md), [guide 08](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/08-principles.md), [poteto-mode Principles section](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md))

The unique mechanism is the **named steering vocabulary**, not the prose. "apply prove it works" is cheaper than restating the verification rule. That only works if the names are already in context, which is why poteto-mode inlines the index.

Most of the 21 already live here under other names.

| pstack principle | Already here |
| --- | --- |
| Laziness protocol, subtract before you add, minimize reader load | Global AGENTS.md "simplest complete design." `typescript-standards` "prefer the smallest complete design." `codebase-design` depth vs shallow. |
| Model the domain | [`domain-modeling`](/Users/max-vev/.pi/agent/skills/domain-modeling/SKILL.md) |
| Type system discipline, boundary discipline | [`typescript-standards`](../skills/typescript-standards/SKILL.md) and [`references/types.md`](../skills/typescript-standards/references/types.md), [`references/boundaries.md`](../skills/typescript-standards/references/boundaries.md). pstack's own [`typescript-best-practices`](https://github.com/cursor/plugins/blob/main/pstack/skills/typescript-best-practices/SKILL.md) is a syntax grounding of the same principle. Do not add it. |
| Fix root causes | [`diagnosing-bugs`](/Users/max-vev/.agents/skills/diagnosing-bugs/SKILL.md) |
| Prove it works | AGENTS.md completion rule. No named principle skill. |
| Sequence verifiable units | Global `tdd` "one slice at a time." `implement` "single test files regularly." |
| Never block on the human | AGENTS.md "implement routine changes directly. Wait for approval only for plan-only requests, risky changes, or genuine ambiguity." pstack is more aggressive. Irreversible actions still pause. ([`principle-never-block-on-the-human`](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-never-block-on-the-human/SKILL.md)) |
| Guard the context window | `writing-for-agents` context load vs cognitive load. `research` already backgrounds the work. |
| Encode lessons in structure | [`principle-encode-lessons-in-structure`](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md) is the one that is only half-present. `writing-for-agents` prunes text. It does not say "make it a lint." |
| Build the lever | Missing as a named rule. Closest is diagnosing-bugs "build a feedback loop" and the X post's verify CLI. |

Vendoring 21 `principle-*` skills would be a context-load disaster. `writing-for-agents` is explicit: always-loaded pointers earn their tokens. Twenty-one extra descriptions, or one giant inline index on every multi-step task, is the opposite of this repo's taste.

If any principle text is worth keeping, keep three names as a short reference, not as skills: **prove it works**, **build the lever**, **encode lessons in structure**. Those are the ones the verification slice actually needs. The rest are already enforced by standards skills.

## Reflection

[`reflect`](https://github.com/cursor/plugins/blob/main/pstack/skills/reflect/SKILL.md) mines the current Cursor transcript with three parallel reviewers (judgment, tooling, divergent), synthesizes Accepted / Rejected / Backlog, refuses to encode as text what should be a lint, then **waits for explicit approval** before editing skills. Substantive edits go through Cursor's built-in `create-skill`. Transcript lookup is hard-coded to the workspace `agent-transcripts/` JSONL layout. Globbing `~/.cursor/projects/*/` is forbidden because it leaks other chats.

The portable idea is: after a hard run, extract a durable skill edit, prefer structure over prose, do not auto-apply. The implementation is Cursor-only.

**What already exists.**

- [`writing-for-agents`](/Users/max-vev/.pi/agent/skills/writing-for-agents/SKILL.md) is the authoring standard. Reflect would be a consumer of it, not a replacement.
- [`plannotator-compound`](/Users/max-vev/.agents/skills/plannotator-compound/SKILL.md) mines *denied plans*, not successful recipes. Different loop.
- [`handoff`](/Users/max-vev/.pi/agent/skills/handoff/SKILL.md) compact a session for the next agent. It does not edit skills.
- [`improve`](/Users/max-vev/.agents/skills/improve/SKILL.md) writes plans for other agents. Read-only on source.

Do not port reflect in the first slice. Pi has no `agent-transcripts/` contract, and this repo's README already says third-party skills are not vendored. A later reflect-for-pi would need a harness-specific transcript adapter and should call `writing-for-agents`, not Cursor `create-skill`.

## Model routing

pstack splits models by role, then writes an always-applied Cursor rule.

[`setup-pstack`](https://github.com/cursor/plugins/blob/main/pstack/skills/setup-pstack/SKILL.md) detects Task-tool slugs, asks per role, writes `~/.cursor/rules/pstack-models.mdc` with `alwaysApply: true`. Defaults in poteto-mode: `grok-4.6-fast-xhigh` for code, `claude-fable-5-thinking-max` for prose and judgment, `gpt-5.6-sol-max` for precisely specified sequences. Panel roles (how critics, arena runners, interrogate reviewers, architect runners) are *lists*. List length is fan-out. `inherit-parent` / `auto` omit the `model` field so Auto users stay on Auto.

This repo already has a better-fitted version: [`skills/model-routing/SKILL.md`](../skills/model-routing/SKILL.md), also installed globally. It routes by responsibility with explicit primary and fallback models, and checks CLIProxyAPI quota before a batch. Grok owns the code loop. Sol owns technical architecture and cross-cutting risk. Opus owns product judgment and taste. Routine review stays on Grok; independent high-stakes review uses Opus.

The overlap is the role split (code vs judgment vs review panel). The implementations should not merge.

- pstack's config file is a Cursor rule. This stack's config is the skill itself plus a quota command.
- pstack names Fable, which pi does not route.
- pstack's default code model is `grok-4.6-fast-xhigh`. This stack's Grok route is Grok 4.6 through CLIProxyAPI with a reasoning-effort knob. Do not import the Cursor slug.
- pstack uses four-model review panels by default. This stack's independent review is usually one extra model, on purpose. The routing table encodes that cost choice directly.

The one pstack routing idea worth borrowing later is **panel-as-list**. Interrogate and how-critique spawn one reviewer per configured model, same prompt, consensus is the signal. That is compatible with this stack's explicit independent-review route. It is not an invitation to default to four.

Do not add `/setup-pstack`. Do not write `~/.cursor/rules/`.

## Parallel review

pstack has three related fan-out tools. They are easy to mash together and should not be.

**Interrogate** is multi-model adversarial review of a diff. Same prompt and rubric to N models. Agreement across models is high-confidence. Lone-model findings are lower. The parent is a lead, not an aggregator. Buckets: Act on / Consider / Noted / Dismissed. Does not auto-apply. Defaults four models: Fable, Sol, Grok, Opus. ([`interrogate/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/SKILL.md), [rubric](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/references/rubric.md))

**Arena** is N parallel *attempts at the same artifact*, pick a base, graft the losers' best parts, verify. Cross-judge on a different model family. ([`arena/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/arena/SKILL.md))

**Swarm** is N parallel *workers on slices or races*, then one report. Default spawn is `environment: "cloud"`. Local is the exception. ([`swarm/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/swarm/SKILL.md))

`how` critique mode already copies interrogate's lead-judgment buckets and four-model critic panel. The global pi `how` skill is a byte-for-byte copy of pstack `how`, including those Cursor `Task` fields and model slugs. (`diff -rq` on `/Users/max-vev/.pi/agent/skills/how` vs pstack `skills/how` is empty.)

**What this stack uses for review.**

- [`code-review`](/Users/max-vev/.agents/skills/code-review/SKILL.md) is two-axis, not multi-model. Standards vs Spec, parallel sub-agents, no reranking across axes. Different job.
- `model-routing` Independent review is one extra model, chosen by fitness.
- `how` critique is already the pstack panel, accidentally, because the global skill was copied.

The missing piece is interrogate's **same-prompt, diverse-model, consensus-weighted** review of a diff, with an opinionated lead. `code-review` does not do that. Do not replace `code-review`. If you want the pstack review, add an optional panel pass that `code-review` or `model-routing` can invoke, using this stack's model table, not Fable/Sol/Grok/Opus-xhigh.

Do not copy swarm's `environment: "cloud"`. Pi's parallel workers are whatever the current harness offers (`herdr` only when asked, remote-development via Fleet). Arena is interesting and expensive. It is not the first slice.

# Duplication map

Several global pi skills are pstack files with the serial numbers still on.

| Skill | Relationship | Keep / drop |
| --- | --- | --- |
| `how` | Identical to pstack `how`, including `subagent_type`, `readonly`, and Fable/Sol/Grok/Opus critic slugs | Already global. Do not add to this repo. The Cursor Task dialect inside a pi skill is existing debt, not a reason to copy more. |
| `unslop` | Identical to pstack `unslop` | Already global (`.agents/skills/unslop`). Always-on for this session. |
| `blast-radius` | Identical except pstack sets `disable-model-invocation: true` | Already global. |
| `bro` | Identical except the same frontmatter flag | Already global. |
| `tdd` | Different. Global tdd is red-green at agreed seams. pstack tdd is "cheap failing regression test for a bug, skip if expensive." | Keep the global one. pstack's skip-if-expensive rule is worth folding into it later, not as a second tdd. |
| `teach` | Different. pstack teach is how+why woven into a conversation. Global teach is a learning-record / mission system with format files | Different products. Do not overwrite. |
| `typescript-best-practices` (pstack) vs `typescript-standards` (this repo) | Same type-discipline, this repo is deeper and framework-agnostic | Do not add pstack's. |
| `model-routing` (this repo) vs `setup-pstack` | Same job, different harness | Keep `model-routing`. |
| `code-review` vs `interrogate` | Two-axis spec/standards vs multi-model adversarial | Complementary. Do not merge blindly. |
| `implement` vs Feature playbook | Four lines vs eight gated steps | Keep `implement`. A later router can point at it. |
| `diagnosing-bugs` vs Bug fix playbook | Loop-first diagnosis vs reproduce-then-fix with subagent delegation | Keep `diagnosing-bugs`. It is stronger on constructing the signal. |
| `handoff` vs Session pickup / Pause safely | Session compact vs Cursor transcript / cloud-agent URL resume | Keep `handoff`. |
| `writing-for-agents` vs Authoring-a-skill playbook plus Cursor `create-skill` | This stack's authoring standard | Keep it. Any adapted pstack skill has to pass it. |
| `domain-modeling` / `codebase-design` vs `architect` | Vocabulary and seams vs multi-model design arena | Keep the local pair. `architect` without arena is just "sketch types first," which `typescript-standards` already says. |

This repo's own skills (`effect-standards`, `nestjs-standards`, `react-standards`, `typescript-standards`, `model-routing`, `remote-development`, `write-discoverable-code`) have no pstack equivalent worth replacing. pstack is a workflow plugin. This repo is mostly language standards plus routing.

The README already states the vendoring policy: "Third-party skills are not vendored here. Install them from their upstream repositories with the Skills CLI so their source and update history remain intact. Adapted work retains its upstream license and attribution inside the skill directory." ([`README.md`](../README.md))

If someone wants raw pstack in Cursor, they `/add-plugin pstack`. This repo is not that plugin.

# Gaps

Ranked by how much they would change agent behavior in *this* stack.

1. **No project-local verify skill generator, no feature map, no maintain loop in HEAD.** Highest. Covered above. The dirty `project-verification` skill is a candidate for this gap, not a shipped close.
2. **No verbatim-step router.** `implement` is too thin. Humans currently are the index for `diagnosing-bugs`, `tdd`, `code-review`, `how`, `model-routing`. `writing-for-agents` already says that is what a router skill is for.
3. **No multi-model consensus review of a diff.** `code-review` is two-axis. `model-routing` independent review is usually one extra model. `how` critique has the panel, but only for architecture explanations.
4. **No "build the lever" default.** Agents still hand-apply edits a script could rerun. diagnosing-bugs almost has this for bugs. Feature work does not.
5. **No session-to-skill reflection loop.** Acceptable. writing-for-agents plus a human is enough until transcripts have a pi-stable path.
6. **No `why` skill.** pstack `why` fans out across git, issues, docs, chat, observability, errors, analytics. Global `how` even says "Use why for motivation," then there is no `why` in the pi tree. Real gap, lower priority than verification. A pi `why` would need Executor/MCP detection, which pstack does at runtime. Do not copy the seven-category sweep until a project actually has those MCPs.

# Cursor-specific assumptions not to copy

These are load-bearing in pstack and wrong here.

**Plugin and config.** `/add-plugin pstack`. `/setup-pstack` writing `~/.cursor/rules/pstack-models.mdc`. `alwaysApply: true`. `disable-model-invocation: true` as Cursor frontmatter. `mode: true` sticky modes. Opt+Enter pinning a Custom Mode. ([guide 01](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/01-setup.md), X post on Opt+Enter)

**Task API.** `subagent_type: "poteto-agent"` / `"generalPurpose"` / `"Comment Sicko"`. `Task` `model:` slugs. `run_in_background: true`. `readonly: true` stripping MCP. `environment: "cloud"`. `AskQuestion`. Cursor `/loop`. Cloud-agent URLs as session identity. [`poteto-agent.md`](https://github.com/cursor/plugins/blob/main/pstack/agents/poteto-agent.md) is a Cursor routing target.

**Sibling plugins.** `/deslop`, `control-cli`, and `control-ui` live in `cursor-team-kit`, not pstack. `/create-skill` is a Cursor built-in. poteto-mode's Opening a PR playbook and reflect skill call all of these by name. ([README "not shipped here"](https://github.com/cursor/plugins/blob/main/pstack/README.md), [`opening-a-pr.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/opening-a-pr.md), [`reflect/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/reflect/SKILL.md))

**Graphite.** Shipping arms `gt` merge-when-ready with `--always`, forbids GitHub auto-merge on stacks, watches `graphite-base/*` retargets. ([`playbooks/shipping.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/shipping.md)) This is a Cursor-at-work merge queue. It does not belong in a personal skills repo.

**Generated paths.** `.cursor/skills/verify-<app>/`. Cursor `agent-transcripts/` JSONL layouts. `~/.cursor/projects/*/`.

**Cloud agents over worktrees.** The X post tells you not to use worktrees and to run Cursor cloud agents instead, because local copies eat disk. The pstack guide still tells you to give parallel work its own worktree. ([X post](https://x.com/poteto/status/2094457600259842065), [guide 02](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/02-poteto-mode.md)) For this stack, neither Cursor cloud nor "never worktree" is the rule. `remote-development` already owns Fleet hosts. `herdr` owns a multiplexer, and only when asked.

**Product-shaped extras.** `make-bot-ui` (Grok Bot webhooks, Tailscale). Benny Slack automations. Dr Eggbot. iOS simulator cleanup. Worktree disk janitor. Grok Bot install links in the X post.

**Model slugs.** `claude-fable-5-thinking-max`, `gpt-5.6-sol-max`, `grok-4.6-fast-xhigh`, `claude-opus-5-thinking-xhigh`. Route through `model-routing` instead.

**Anti-planning.** Tan's "the best spec is code" is a Cursor-plan-mode opinion. This stack plans on purpose.

# Licensing and attribution

pstack is MIT, Copyright (c) 2026 Lauren Tan. ([`pstack/LICENSE`](https://github.com/cursor/plugins/blob/main/pstack/LICENSE))

This repo is MIT, Copyright (c) 2026 Maximilian Pinder-White. ([`LICENSE`](../LICENSE))

MIT on MIT is legally straightforward. The conditions that matter:

1. Keep the Lauren Tan copyright notice in every adapted skill directory.
2. Do not pretend the adaptation is original pstack, and do not pretend it is original to this repo without the upstream line.
3. Follow the existing convention used by [`write-discoverable-code`](../skills/write-discoverable-code/): a skill-local `LICENSE` with both copyright holders, plus [`ATTRIBUTION.md`](../skills/write-discoverable-code/ATTRIBUTION.md) naming the upstream path and commit.
4. Honor the README vendoring rule. A full pstack dump would violate "Third-party skills are not vendored here." An adapted generator that substantially revises paths, harness calls, and model routing is the `write-discoverable-code` pattern, not a dump.

`effect-standards` is the other attribution precedent. Upstream had no license declared, and ATTRIBUTION.md says so. pstack *does* declare MIT, so the write-discoverable-code pattern is the one to copy.

Do not relicense. Do not drop `disable-model-invocation` notes as if they were original. Do not keep "poteto" in skill names. A router, if added later, should not be called `poteto-mode`. Tan's README says fork it and make it yours. `/automate-me` exists specifically so you do not ship her style under your name. ([README "make it yours"](https://github.com/cursor/plugins/blob/main/pstack/README.md))

# Smallest coherent implementation slice

One generator in this repo, adapted under MIT attribution. pstack ships creation and maintenance as two slash skills. Combining them is the smaller fit here.

## Add a verification generator, preferably as one skill with two branches

Two separate skills is what pstack ships. One skill with Create and Maintain branches is smaller and matches how maintain already points back at create when no target exists. The implementation keeps the upstream wording at the user's request, retains MIT attribution, and changes only the combined entry point and harness-specific paths.

**Keep from pstack.**

- Interview the repo, not the user.
- Generated skill sections: Launch, Doctor, Drive, Evidence, Cleanup, Helpers.
- Feature map with the four H2s and a README index. Ship the Notes example as a reference, rewritten if needed, still attributed.
- Prove the generated skill once on one feature before handover. Evidence survives cleanup.
- Maintain loop: source wave in parallel, one live pass, outcomes `clean` / `changed` / `blocked`. Edit only the verify skill directory. Report product regressions instead of editing product code.
- Prefer an existing harness in the target repo. Only then pick browser/CDP, PTY, or HTTP.
- Prefer a small CLI over markdown-only driving, per Build the Lever and the X post. `--dry-run`, subcommands, JSON, errors that say what to do instead.

**Change.**

- Output path is harness-agnostic. Write `.agents/skills/verify-<app>/` (Agent Skills spec, works in Cursor, Claude Code, Codex, and pi) unless the target repo already has a skills directory the generator can see. Never hard-code `.cursor/skills/`.
- No `control-cli` / `control-ui` / `cursor-team-kit` dependency. The generated CLI is the target app's.
- Model choices go through `model-routing`, including the maintain-loop source readers.
- Frontmatter follows this repo and the Agent Skills spec. No Cursor `disable-model-invocation` unless a later pass decides the generator should be user-invoked only. `writing-for-agents` says: user-invoked if the human is the index, model-invoked if another skill must reach it. The Feature playbook in a later router would need to reach it, so model-invoked is the right default.
- Each skill directory gets `LICENSE` (Lauren Tan + Maximilian Pinder-White) and `ATTRIBUTION.md` pointing at `cursor/plugins` `pstack/skills/create-verification-skill` and `.../maintain-verification-skill` at the commit above.
- Run the result through `writing-for-agents`. pstack SKILL.md files are long, trigger-heavy, and full of Cursor tool names. The adaptation has to be the shortest document that still forces Launch/Doctor/Drive/Evidence/Cleanup and the live proof.

**Do not do in this slice.**

- No `/poteto-mode`. No playbook directory. No 21 principles. No `setup-pstack`. No `interrogate`. No `arena`. No `swarm`. No `reflect`. No `architect`. No `typescript-best-practices`. No `figure-it-out`. No Graphite. No `poteto-agent`.
- No README skill-list rewrite until the skill is ready to ship. The dirty tree already added a README bullet. Keep that bullet only if the skill ships.

**Dirty candidate vs this slice.** `skills/project-verification/` already matches the keep list, the MIT attribution pattern, harness-agnostic placement, and the Create/Maintain merge. Check these before calling it done:

- Maintain-loop source readers should load `model-routing` rather than spawning anonymous subagents.
- The implementation now preserves pstack's H2 names and bundles its Notes feature-map example under the upstream MIT attribution.
- Placement says "the active agent's standard project skill directory" instead of a single default. That avoids `.cursor/skills/`. It also lets two agents in one repo write two copies. The "one canonical copy" sentence has to win.
- The skill is model-invoked, which this note wants. Confirm the description does not also steal `tdd` or `diagnosing-bugs` triggers.

## Why this slice is coherent

The X post's composition story is: make verification a repo artifact, then every other workflow can say "drive the mapped feature and keep the evidence." Bug fix, feature work, blast-radius, and overnight runs all assume that artifact. Without it, pstack's playbooks degrade to "remember to run the app."

This stack already has diagnosis, TDD, standards, model routing, and two-axis review. Those skills would get better the moment a target repo has `verify-<app>`. They do not need a new router first. A router without a verify skill is ceremony. A verify skill without a router still closes the loop.

## Later slices, if the first one earns its place

**Slice 2. A thin user-invoked router.** One skill, in the `writing-for-agents` sense. Names existing skills, copies a short step list, forbids silent skips. Five playbooks at most:

- Investigation → `how` (and `research` when the question is not the current repo)
- Bug → `diagnosing-bugs`, then `tdd` if the loop is a cheap test
- Feature → `model-routing`, language standards, `implement`, then the generated `verify-*`
- Review → `code-review`, optional multi-model panel
- Verify-skill upkeep → the Maintain branch of `project-verification`

No sticky Cursor mode. No principles index. No Graphite tail.

**Slice 3. Multi-model panel on `code-review`.** Same prompt, N models from `model-routing`, consensus vs lone-model, lead buckets. Default N=2, not 4.

Anything past that is a different project. At that point installing pstack in Cursor is cheaper than rewriting it.

# What to refuse

A full pstack import would give this repo a second, conflicting workflow language. poteto-mode wants Fable, Graphite, cloud `Task`s, and "never block on the human." AGENTS.md wants a lightweight plan, `model-routing`, and the smallest check. Those cannot both be the default.

The global `how` copy is the warning. Someone already dropped a pstack skill into pi with Cursor `Task` fields intact. It works only because models ignore the parts they cannot call. That is not a standard to extend.

Verification is the piece pstack got right and HEAD does not have. Generate it, maintain it, attribute it, stop. If `skills/project-verification/` is that generator, review it against the keep/change list above and do not start a second one.
