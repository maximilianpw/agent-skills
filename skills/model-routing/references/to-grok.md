# Delegate to Grok

Use this adapter after `model-routing` selects Grok and the current harness cannot select an xAI model directly.

- Prefer native delegation when available. In pi, select `harness: "pi"` with `model: "cursor/grok-4.6"`.
- Select `cursor/grok-4.6:slow` for unattended, long-running work where lower cost matters more than latency. Set reasoning effort separately according to task difficulty.
- Otherwise invoke pi non-interactively with `pi --provider cursor --model grok-4.6 --print` and a self-contained prompt; add the `:slow` suffix for the asynchronous cost-saving lane.
- Include the settled plan, exact file scope, invariants, acceptance checks, and verification command. Grok owns implementation, not unresolved product or architecture decisions.
- Run editing agents only in the intended trusted worktree. Ask for a report instead when the caller only needs analysis.
- Preserve the implementation report and verification output for the Claude or Sol review pass.
