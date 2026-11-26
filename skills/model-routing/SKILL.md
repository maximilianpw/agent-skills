---
name: model-routing
description: Route workflows, subagents, and independent reviews to the right model. Use before delegation or when rerouting failed or stalled work.
license: MIT
---

# Model routing

Choose the model here. The caller's policy decides whether work stays in the current thread or uses a subagent.

## Roster

| model | provider | role |
| --- | --- | --- |
| Opus 5.5 | Anthropic | Default for everything: the coordinating thread, judgment, architecture, product and UI decisions, prose, synthesis, and the hardest tasks. |
| Fable 5.2 | Anthropic | Delegated hands-on code loops with explicit scope and checks: implementation, refactoring, bug fixes, performance work, and repository exploration. |
| GPT-6 Astra | OpenAI | Independent review only: code, security, and design review of Claude-authored work, and the second `council` seat. |

Astra is a reviewer, not a worker. Give it a read-only, report-only brief with a fixed scope; it tends to ask, over-test, and produce long lists, so cap findings to evidence-backed problems.

## Check availability

Before each delegation batch, run:

```bash
cliproxyapi-util quota --json 2>/dev/null || bun "$HOME/pi-config/cli/cliproxyapi-util.ts" quota --json
```

The `claude` family covers Opus and Fable; `codex` covers Astra. Treat `unknown` as available until a call fails. If the check fails, route normally.

## Routes

| responsibility | primary | fallback |
| --- | --- | --- |
| coordinating thread, planning, architecture, product/UI/copy, subjective API design | Opus 5.5 | none; ask |
| delegated implementation, refactoring, migrations, tests, reproducible debugging, performance | Fable 5.2 | Opus 5.5 |
| delegated repository exploration or bounded analysis | Fable 5.2 | Opus 5.5 |
| independent code or security review | GPT-6 Astra | Opus 5.5 in a fresh context, labeled same-provider |
| independent architecture or design review | GPT-6 Astra for Opus work; Opus 5.5 for Fable work | the other of the two |

Keep the current model while failures are concrete and each iteration makes measurable progress. Move a stalled Fable loop to Opus when progress stops, evidence cannot bound the risk, or the task becomes an architecture or product judgment.

Editing delegates share the current worktree unless isolated. Give one editing agent ownership of a worktree; use isolated worktrees for parallel editors. Ask for a report when the delegate only analyzes or reviews.

## Council defaults

For the `council` skill, use **Opus 5.5 (Anthropic) and GPT-6 Astra (OpenAI)** at high reasoning effort where supported. These are model families/versions, not hardcoded API IDs; resolve them through the host's model catalog. Honor user-named members. If a seat is unavailable, report it and ask before substituting rather than silently running a smaller panel. The council skill owns review budgets and reconciliation; this section owns the default roster.

## Cross-harness delegation

Use native model selection when the harness supports it. In Pi, select Astra as `cliproxyapi/gpt-6-astra`. From Claude Code, load [`references/from-claude-code.md`](references/from-claude-code.md).
