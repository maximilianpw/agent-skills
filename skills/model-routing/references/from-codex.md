# Delegate from Codex to Claude

Use this adapter when Codex cannot select the routed Claude model natively.

- Run `claude -p --model opus` only for the architecture or design work routed to Opus.
- Request critique or structured recommendations by default. Request edits only for a tightly scoped patch or isolated worktree.
- Use `--output-format json` or `--json-schema` when the caller needs structured output.
