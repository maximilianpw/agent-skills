---
name: grill-with-docs
description: Run a grilling interview while updating the project's domain glossary and ADRs. Use when the user asks to be grilled and wants CONTEXT.md, glossary, or architecture decisions captured during the interview.
---

# Grill with Docs

Read and follow the `grilling` and `domain-modeling` skills before starting. Use `read` on each skill's `SKILL.md`, or have the user invoke `/skill:grilling` and `/skill:domain-modeling` when direct skill loading is required by the harness.

Run the workflows together:

- `grilling` owns the design tree, frontier rounds, recommendations, and user decisions.
- `domain-modeling` challenges terminology, checks the code and existing context, updates the glossary as terms settle, and records qualifying ADRs as decisions crystallize.

Do not postpone documentation until the interview ends. Keep `CONTEXT.md` and any warranted ADRs synchronized with each settled round.
