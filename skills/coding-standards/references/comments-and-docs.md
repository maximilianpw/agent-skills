# Comments and documentation

## Comments must earn their place

Default to code without commentary. Add a comment only when a competent reader would otherwise misread the code or change it into a bug: a workaround, browser/framework/server quirk, security invariant, reason the code cannot express, or mirrored upstream behavior (`// Upstream: …`).

Interfaces and helpers do not need docstrings merely because they exist or are exported. Keep documentation required by public API tooling and describe contracts the types cannot express, including component constraints. Prefer a name, type, or error message when it can carry the meaning instead.

Attach required API documentation to the original declaration; re-exports rely on it rather than duplicating it. Use tags only when they add caller-relevant information.

Reread each added comment before completion. Remove what names, types, errors, or the next line already say.

## Document what the code cannot tell you

Keep setup, environment and secret handling, safety rules, and contracts with other systems. Avoid changelogs, component catalogues, module maps, file trees, or diagrams that merely restate code, types, generated API documentation, or the running app. Preserve documentation required by the repository or an explicit user request.

Plans, run evidence, and scratch output belong outside the repository or in a git-ignored folder. A maintained verification recipe is a contract for driving the system, not captured run evidence; keep the recipe with its owner and the evidence in its named ignored or external location.
