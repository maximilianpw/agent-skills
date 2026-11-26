# Review with Astra from Claude Code

Claude Code cannot select GPT-6 Astra natively; run it through the Codex CLI as a read-only reviewer.

- Use `codex review -c model="gpt-6-astra"` with `--uncommitted`, `--base <BRANCH>`, or `--commit <SHA>` for diff review.
- Use `codex exec -m gpt-6-astra --sandbox read-only` for design documents or reviews that need a custom brief.
- Request a report only. Astra never edits in this role.
- If a workflow accepts only Claude models, invoke Codex outside that workflow rather than spending Opus on a passthrough wrapper. Label the handoff `codex:<task>`.
- Give long runs a timeout or run them in the background and wait for their report.
