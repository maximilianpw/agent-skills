# Attribution

This skill is adapted from Lauren Tan's pstack [`create-verification-skill`](https://github.com/cursor/plugins/tree/main/pstack/skills/create-verification-skill) and [`maintain-verification-skill`](https://github.com/cursor/plugins/tree/main/pstack/skills/maintain-verification-skill) at commit [`d457567332aa6989e753ea289f30ea2bfbc80bc0`](https://github.com/cursor/plugins/commit/d457567332aa6989e753ea289f30ea2bfbc80bc0).

The adaptation combines creation and maintenance behind one model-invoked, cross-agent skill. It preserves the upstream wording and feature-map example, while replacing Cursor-specific skill paths and slash-command references with harness-aware project paths and one combined entry point. Local safety rules require explicit authorization for publication and shared-state changes, isolated verification data, and ignored or external evidence storage. The reviewed upstream changes for usable empty-data startup, missing seed prerequisites, and stand-in verification gaps are retained.

The pstack source is MIT licensed. The bundled [`LICENSE`](LICENSE) retains its permission notice and records the upstream and adaptation copyright holders.
