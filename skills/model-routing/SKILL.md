---
name: model-routing
description: Select models for workflows and delegated work. Use before choosing a model for any workflow or subagent, reallocating work after delegation fails, or assigning an independent review.
license: MIT
---

# Model Routing

Choose models by fitness for the task. Route code-centric work to the strongest cost-effective coder; reserve expensive judgment models for decisions that code verification cannot settle.

## Ranking

Higher intelligence, code quality, and taste are better. Cost is the user's relative effective cost, where lower is cheaper.

| model | cost | intelligence | code quality | taste |
| --- | ---: | ---: | ---: | ---: |
| GPT-5.6 Sol | 9 | 8 | 8 | 5 |
| Opus 5 | 4 | 7.5 | 7.5 | 8 |
| Grok 4.6 | 1 | 7.5 | 8 | 5.5 |
| Sonnet 5 | 5 | 5 | 5 | 7 |

Scores are routing priors, not benchmark measurements. Grok's strong coding evaluations support giving it ownership of code quality, not merely bulk generation.

For work that ships, prioritize the dimension the task exercises. User-facing UI, copy, and API design require taste of at least 7; implementation correctness favors code quality and objective verification.

## Route by responsibility

| responsibility | route |
| --- | --- |
| narrow mechanical edit | Terra or Luna |
| repository exploration and code-centric planning | Grok 4.6 |
| implementation, refactoring, migration, and test writing | Grok 4.6 |
| reproducible debugging and performance work | Grok 4.6 |
| code-quality review and verification | Grok 4.6 |
| product architecture or ambiguous high-risk decisions | Opus 5 or Sol |
| user-facing design, copy, and subjective API taste | Opus 5 |

Grok owns the full code loop: investigate, plan, implement, test, inspect the diff, and repair failures. Add Opus or Sol when the unresolved question is architectural, subjective, or too high-risk for tests and static checks to establish confidence. Code volume strengthens the Grok route but is no longer a prerequisite.

### GPT-5.6 family

- **Sol:** open-ended discovery, architecture, ambiguous debugging, cross-cutting or high-risk changes, and final synthesis.
- **Terra:** bounded analysis and routine implementation with explicit scope and acceptance checks.
- **Luna:** narrow mechanical work with objectively checkable output. Use a stronger model for planning and review.

Start unfamiliar code task classes with Grok. Start unfamiliar product, domain, or architecture decisions with Sol, then delegate the engineering loop to Grok. Escalate when evidence is missing, agents disagree, or verification cannot bound the risk.

### Claude family

- **Opus 5:** product and architecture decisions, ambiguous non-reproducible debugging, high-risk audits, and user-facing work where judgment and taste matter.
- **Sonnet 5:** fallback for bounded user-facing work when Opus is unavailable or constrained; Opus otherwise dominates it under the ranking above.
- **Haiku:** never use.

### Grok family

- **Grok 4.6 through CLIProxyAPI:** default owner for code-centric planning, implementation, refactoring, reproducible debugging, tests, code review, and verification. Give it the goal, constraints, invariants, and acceptance checks, then let it complete the engineering loop.
- Use Pi's reasoning-effort setting to match the task difficulty; CLIProxyAPI exposes Grok 4.6 reasoning levels from `low` through `xhigh`.

### Independent review

Use Grok 4.6 as the default code reviewer, including for Claude implementations. Review Grok work with Opus when architecture, security impact, or user-facing taste raises the stakes; add Sol only when another independent perspective is worth the cost.

## Invoke across harnesses

After selecting a model, load the adapter for the current harness when delegation crosses model families:

- From any harness to Grok: [`references/to-grok.md`](references/to-grok.md).
- From Claude Code to an OpenAI model: [`references/from-claude-code.md`](references/from-claude-code.md).
- From Codex to a Claude model: [`references/from-codex.md`](references/from-codex.md).

Use native workflow or subagent model selection when the current harness supports the selected model directly.

## Recover from weak output

Let Grok continue repairing while failures are concrete and each iteration makes measurable progress. Escalate to Opus or Sol when progress stalls, the problem resolves into an architectural decision, or verification cannot bound the risk. If a named model is unavailable, choose the closest available model that satisfies the role; keep user-facing work on a model with sufficient taste.
