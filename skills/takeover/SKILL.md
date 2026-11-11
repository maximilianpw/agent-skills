---
name: takeover
description: Continue an existing PR, branch, or agent handoff while preserving intent and contributor credit. Use when asked to take over existing work.
license: MIT (see LICENSE and ATTRIBUTION.md)
---

# Takeover

1. Read the original goal, source PR/branch/thread, review findings, and subsequent user corrections. Resolve the handoff to the actual repository and head; inspect uncommitted work. Inherited summaries are context, not proof.
2. Confirm the requested finish and permissions. Continuing local work does not authorize pushing, public comments, merging, closing, or modifying the original PR. Follow global orchestration policy when reading another agent thread; a handoff is not permission to spawn separate working agents.
3. Preserve unrelated changes. For a requested replacement PR, import original commits onto a new branch and add fixes separately. Honor explicitly requested in-place or stacked continuation.
4. Preserve authorship and co-author trailers. Credit original contributors and link the source PR in the eventual PR description. For squash merges, preserve human credit using verified identities, not guessed emails.
5. Use the installed `modernize` skill to reassess the goal against its actual base and current architecture. Rework only within the authorized scope; recheck whether the source PR advanced while you worked.
6. Independently reproduce the original failure and verify realistic workflows under repository rules. State what remains unverified instead of relying on inherited green tests.
7. If publication is explicitly requested, use `file-pr`. If monitoring is included, continue with `babysit-pr`. Authorized public replies use `leaving-pr-comments`. Keep the source PR open unless closure or merge was separately authorized.

Report what you inherited, what you changed, verification, how credit was preserved, publication status, and the remaining decision.
