# Delegate from Codex to Claude

Use this adapter after `model-routing` selects a Claude model while the current harness is Codex.

- Invoke Claude non-interactively with `claude -p --model <model>`.
- Use `opus` or `sonnet` according to the model selected by the routing rules.
- Ask for critique or structured recommendations by default. Request edits only in an isolated worktree or for a tightly scoped patch.
- Use `--output-format json` or `--json-schema` when the caller needs structured output.
