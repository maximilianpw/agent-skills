---
name: model-routing
description: Route workflows, subagents, and independent reviews to the right model. Use before delegation or when rerouting failed or stalled work.
license: MIT
---

# Model routing

Choose the model here. The caller's policy decides whether work stays in the current thread, uses a subagent, or runs in Herdr.

Choose by responsibility. Objective verification lowers the need for expensive judgment.

## Grading

These are personal routing priors, not benchmark claims. Personal cost uses `1` for cheapest and `10` for most expensive. Higher judgment, code, taste, and efficiency scores are better. Efficiency combines cost, speed, and token economy.

| model | personal cost | judgment | code | taste | efficiency |
| --- | ---: | ---: | ---: | ---: | ---: |
| GPT-6 Luna | 1 | 5 | 4.7 | 4 | 10 |
| Grok 4.6 | 3 | 6.5 | 6.5 | 8 | 9 |
| GPT-6 Sol | 4 | 7.5 | 7.8 | 6 | 9 |
| GPT-6 Astra | 9 | 9 | 9 | 7 | 6 |
| Opus 5.5 | 7 | 10 | 9 | 10 | 7 |

## Check availability

Before each delegation batch, run:

```bash
cliproxyapi-util quota --json 2>/dev/null || bun "$HOME/pi-config/cli/cliproxyapi-util.ts" quota --json
```

The quota families map as follows: `codex` is Astra, Sol, and Luna; `claude` is Opus; `grok` is Grok 4.6. Remove unavailable families for CLIProxyAPI routes. Astra consumes Codex allowance several times faster than Sol, so reserve it for work that benefits from peak judgment. A known-working native harness remains available. Treat `unknown` as available until a call fails. If the check fails, route normally.

## Routes

| responsibility | primary | fallback |
| --- | --- | --- |
| trivial mechanical edit with an obvious check | GPT-6 Luna | Grok 4.6 |
| bounded analysis or routine edit with explicit scope and checks | GPT-6 Luna | Grok 4.6 |
| repository exploration, code planning, implementation, refactoring, migrations, tests, reproducible debugging, performance | Grok 4.6 | GPT-6 Sol |
| routine code review and verification | Grok 4.6 | GPT-6 Sol |
| cross-cutting high-risk implementation or non-reproducible technical debugging | GPT-6 Sol | Grok 4.6; escalate to GPT-6 Astra after progress stalls |
| long-horizon cross-system analysis, computer-use work, or a stalled frontier task | GPT-6 Astra | GPT-6 Sol |
| technical architecture | GPT-6 Sol | GPT-6 Astra |
| product architecture, UI, copy, and subjective API design | Opus 5.5 | GPT-6 Sol |
| independent code or security review | GPT-6 Astra for Grok or Sol work; Grok 4.6 for Astra, Luna, or Opus work | the other of Grok 4.6 or GPT-6 Sol |
| independent architecture or design review | Opus 5.5 for Sol or Astra work; GPT-6 Astra for Opus work | the other of Opus 5.5 or GPT-6 Sol |

If both routes are unavailable, choose the closest listed model that preserves the task's main requirement. Use Opus for high-judgment architecture, design, review, or stalled work rather than routine loops.

Reserve Astra for ambitious multi-step work, computer use, cross-file review, or stalled tasks. It is coherent and token-efficient but quota-heavy and may ask, over-test, or stop; grant authority to finish and cap questions and verification.

Keep the current model while failures are concrete and each iteration makes measurable progress. Escalate when progress stalls, evidence cannot bound the risk, or the task becomes an architecture or product judgment.

Editing delegates share the current worktree unless isolated. Give one editing agent ownership of a worktree; use isolated worktrees for parallel editors. Ask for a report when the delegate only analyzes or reviews.

## Cross-harness delegation

Use native model selection when the harness supports it. Otherwise load the matching adapter:

- Grok from any harness: [`references/to-grok.md`](references/to-grok.md).
- OpenAI from Claude Code: [`references/from-claude-code.md`](references/from-claude-code.md).
- Claude from Codex: [`references/from-codex.md`](references/from-codex.md).
