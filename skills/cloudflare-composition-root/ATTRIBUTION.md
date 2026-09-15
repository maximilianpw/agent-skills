# Attribution

This skill is adapted from Dillon Mulroy's [`cloudflare-composition-root`](https://github.com/dmmulroy/.dotfiles/tree/main/home/.agents/skills/cloudflare-composition-root) skill at commit [`fcdf06013853c2e8e5718b620d3a2b481fbcedb9`](https://github.com/dmmulroy/.dotfiles/commit/fcdf06013853c2e8e5718b620d3a2b481fbcedb9).

The adaptation broadens the upstream Hono-focused workflow to the Cloudflare architectures used by this repository owner's projects: raw Workers, WorkerEntrypoints, Durable Objects, Queues, scheduled handlers, D1, R2, KV, service bindings, Effect, and Alchemy. It keeps the upstream composition-root, narrow-binding, lifetime, migration, and leakage-audit principles while delegating Effect implementation details to `effect-standards`.

The upstream repository does not declare an SPDX license.
