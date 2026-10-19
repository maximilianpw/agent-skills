# Safe file restructures

A restructure contains moves, renames, and whole-file merges only. Keep behavior changes and logic deduplication in separate changes.

## Move from known ownership

1. Apply [file layout](file-layout.md) to choose the new owner. Preserve server/client/edge and package boundaries.
2. Before merging, inspect value-level import cycles, module side effects, lazy loading, and the destination bundle. Preserve side-effect order.
3. Rewrite imports with a script or IDE refactor that resolves each import from its old location and retains path aliases (`@/`) as aliases. Plain text replacement cannot resolve relative imports correctly. `git mv` is optional; Git detects renames.
4. Move or rename snapshots and visual baselines with their tests.

## Verify more than compilation

Run the affected packages' type checks, builds, and tests. Run moved tests as CI does, using CI mode or the flag that fails for missing snapshots instead of writing new ones.

Inspect paths the compiler may miss, including excluded files and string-held paths:

- test and script path strings, dynamic imports, assets and public paths;
- `tsconfig` paths, lint/bundler/Tailwind/Storybook globs;
- generated route trees (regenerate; never hand-edit);
- `package.json` `exports` and `bin`;
- deployment configuration such as `wrangler.toml`, and CI workflow paths;
- documentation and agent-skill links.

Complete when old references are removed or intentionally retained for compatibility, runtime boundaries and loading order are preserved, and all affected checks pass or have a concrete reported blocker. If commits are authorized, commit moves separately from behavior changes and merges; inspect `git show -M --stat` for readable rename history.
