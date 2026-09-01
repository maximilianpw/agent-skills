# Delegate to Grok

Use this adapter when the current harness cannot select Grok natively.

- In Pi, use `harness: "pi"`, `model: "cliproxyapi/grok-4.6"`, and the routed reasoning effort.
- Otherwise run `pi --provider cliproxyapi --model grok-4.6 --print` with a self-contained prompt.
- If CLIProxyAPI is unavailable, return to `model-routing` and use the fallback.
