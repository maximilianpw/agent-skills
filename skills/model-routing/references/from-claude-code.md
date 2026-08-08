# Delegate from Claude Code to OpenAI

Use this adapter after `model-routing` selects an OpenAI model while the current harness is Claude Code.

- Invoke bounded work with `codex exec` and independent reviews with `codex review`.
- Request a report by default. Request edits only when the scope is explicit.
- Pass the selected model explicitly when supported instead of relying on the Codex CLI default.
- If a Claude workflow accepts only Claude models, use a thin `sonnet`/`low` wrapper that writes a self-contained Codex prompt, runs the selected OpenAI model, and returns its report. Prefix wrapper labels with `codex:`.
- Give long runs an explicit timeout or run them in the background and poll for a report file.
- Run parallel implementation agents in isolated worktrees.
