# Attribution

This skill is adapted from Dillon Mulroy's [`cloudflare-composition-root`](https://github.com/dmmulroy/.dotfiles/tree/main/home/.agents/skills/cloudflare-composition-root) skill at commit [`4035e4211d962ced3164c95270b0d82826608ae9`](https://github.com/dmmulroy/.dotfiles/commit/4035e4211d962ced3164c95270b0d82826608ae9).

The adaptation broadens the upstream Hono-focused workflow to the Cloudflare architectures used by this repository owner's projects: raw Workers, WorkerEntrypoints, Durable Objects, Queues, scheduled handlers, D1, R2, KV, service bindings, Effect, and Alchemy. It keeps the upstream composition-root, narrow-binding, lifetime, migration, and leakage-audit principles while delegating Effect implementation details to `effect-standards`. It omits the upstream `disable-model-invocation` metadata so agents can select the skill for work covered by its description.

The upstream repository does not declare an SPDX license.
