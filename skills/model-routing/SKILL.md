---
name: model-routing
description: Select models for workflows and delegated work. Use before choosing a model for any workflow or subagent, reallocating work after delegation fails, or assigning an independent review.
license: MIT
---

# Model Routing

Choose models by fitness for the task. Cost breaks ties; it does not justify work below the required quality bar.

## Ranking

Higher intelligence and taste are better. Cost is the user's relative cost, where lower is cheaper.

| model | cost | intelligence | taste |
| --- | ---: | ---: | ---: |
| GPT-5.6 Sol | 9 | 8 | 5 |
| Sonnet 5 | 5 | 5 | 7 |
| Opus 5 | 4 | 7.5 | 8 |

For work that ships, prioritize intelligence, then taste, then cost. User-facing UI, copy, and API design require taste of at least 7.

## Route the work

### GPT-5.6 family

- **Sol:** open-ended discovery, architecture, ambiguous debugging, cross-cutting or high-risk changes, and final synthesis.
- **Terra:** bounded analysis and routine implementation with explicit scope and acceptance checks.
- **Luna:** narrow mechanical work with objectively checkable output. Never use it as the sole planner or reviewer.

Start unfamiliar task classes with Sol, then delegate bounded work to cheaper models. Escalate when scope expands, evidence is missing, agents disagree, or verification fails.

### Claude family

- **Opus 5:** reviews, architecture, difficult implementation, and user-facing work where judgment and taste matter.
- **Sonnet 5:** fallback for bounded user-facing work when Opus is unavailable or constrained; Opus otherwise dominates it under the ranking above.
- **Haiku:** never use.

### Review specialist

**Fable 5** is an unscored specialist for independent plan and implementation reviews. Use Opus 5 when the review also needs editing, architectural judgment, or final synthesis. Add GPT-5.6 Sol only when another independent perspective is worth the cost.

## Invoke across harnesses

After selecting a model, load the adapter for the current harness when delegation crosses model families:

- From Claude Code to an OpenAI model: [`references/from-claude-code.md`](references/from-claude-code.md).
- From Codex to a Claude model: [`references/from-codex.md`](references/from-codex.md).

Use native workflow or subagent model selection when the current harness supports the selected model directly.

## Recover from weak output

If a cheaper model misses the bar, rerun or redo the work with a stronger model without asking. If a named model is unavailable, choose the closest available model that satisfies the role; do not silently route user-facing work to a low-taste model.
