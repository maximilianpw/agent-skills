# Delegate from Claude Code to OpenAI

Use this adapter when Claude Code cannot select the routed OpenAI model natively.

- Use `codex exec` for bounded work and `codex review` for independent review.
- Pass the selected model explicitly.
- Request a report for analysis or review. Request edits only with explicit scope.
- If a workflow accepts only Claude models, invoke Codex outside that workflow rather than spending Opus on a passthrough wrapper. Label the handoff `codex:<task>`.
- Give long runs a timeout or run them in the background and poll for their report.
