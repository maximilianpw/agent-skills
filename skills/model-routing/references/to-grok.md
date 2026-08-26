# Delegate to Grok

Use this adapter after `model-routing` selects Grok and the current harness cannot select an xAI model directly.

- Prefer native delegation when available. In pi, select `harness: "pi"` with `model: "cliproxyapi/grok-4.6"` and set reasoning effort according to task difficulty.
- Otherwise invoke pi non-interactively with `pi --provider cliproxyapi --model grok-4.6 --print` and a self-contained prompt.
- CLIProxyAPI is the sole Grok provider. Return to `model-routing` and choose another model if it is unavailable.
- Include the settled plan, exact file scope, invariants, acceptance checks, and verification command. Grok owns implementation, not unresolved product or architecture decisions.
- Run editing agents only in the intended trusted worktree. Ask for a report instead when the caller only needs analysis.
- Preserve the implementation report and verification output for the Claude or Sol review pass.
