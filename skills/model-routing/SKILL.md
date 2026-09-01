---
name: model-routing
description: Route workflows, subagents, and independent reviews to the right model. Use before delegation or when rerouting failed or stalled work.
license: MIT
---

# Model routing

Choose by responsibility. Objective verification lowers the need for expensive judgment.

## Grading

These are personal routing priors, not benchmark claims. Personal cost uses `1` for cheapest and `10` for most expensive. Higher judgment, code, and taste scores are better.

| model | personal cost | judgment | code | taste |
| --- | ---: | ---: | ---: | ---: |
| Luna | 1 | 5 | 6 | 4 |
| Grok 4.6 | 2 | 8 | 9 | 7 |
| GPT-5.6 Sol | 7 | 9 | 9 | 6 |
| Opus 5 | 10 | 8 | 7 | 9 |

Terra remains an ungraded utility route for bounded work.

## Check availability

Before each delegation batch, run:

```bash
cliproxyapi-util quota --json 2>/dev/null || bun "$HOME/pi-config/cli/cliproxyapi-util.ts" quota --json
```

The quota families map as follows: `codex` is Sol, Terra, and Luna; `claude` is Opus; `grok` is Grok 4.6. Remove unavailable families for CLIProxyAPI routes. A known-working native harness remains available. Treat `unknown` as available until a call fails. If the check fails, route normally.

## Routes

| responsibility | primary | fallback |
| --- | --- | --- |
| trivial mechanical edit with an obvious check | Luna | Grok 4.6 |
| bounded analysis or routine edit with explicit scope and checks | Terra | Grok 4.6 |
| repository exploration, code planning, implementation, refactoring, migrations, tests, reproducible debugging, performance | Grok 4.6 | GPT-5.6 Sol |
| routine code review and verification | Grok 4.6 | GPT-5.6 Sol |
| cross-cutting high-risk implementation or non-reproducible technical debugging | GPT-5.6 Sol | Grok 4.6 |
| technical architecture | GPT-5.6 Sol | Opus 5 |
| product architecture, UI, copy, and subjective API design | Opus 5 | GPT-5.6 Sol |
| independent code or security review | GPT-5.6 Sol for Grok work; Grok 4.6 for Sol, Terra, Luna, or Opus work | the other of Grok 4.6 or GPT-5.6 Sol |
| independent architecture or design review | Opus 5 for Sol work; GPT-5.6 Sol for Opus work | the other of Opus 5 or GPT-5.6 Sol |

If both routes are unavailable, choose the closest listed model that preserves the task's main requirement. Use Opus only for architecture or subjective design.

Grok owns the complete code loop. Give it the goal, exact file scope, constraints, invariants, acceptance checks, and verification command. Route Grok only through CLIProxyAPI, match reasoning effort to task difficulty from `low` through `xhigh`, and preserve its report plus verification output for review.

Keep the current model while failures are concrete and each iteration makes measurable progress. Escalate when progress stalls, evidence cannot bound the risk, or the task becomes an architecture or product judgment.

Editing delegates share the current worktree unless isolated. Give one editing agent ownership of a worktree; use isolated worktrees for parallel editors. Ask for a report when the delegate only analyzes or reviews.

## Cross-harness delegation

Use native model selection when the harness supports it. Otherwise load the matching adapter:

- Grok from any harness: [`references/to-grok.md`](references/to-grok.md).
- OpenAI from Claude Code: [`references/from-claude-code.md`](references/from-claude-code.md).
- Claude from Codex: [`references/from-codex.md`](references/from-codex.md).
