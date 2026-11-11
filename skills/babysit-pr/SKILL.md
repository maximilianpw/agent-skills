---
name: babysit-pr
description: Monitor a GitHub PR through CI and review, triage findings, and report readiness. Use when asked to watch, monitor, or babysit a PR.
license: MIT (see LICENSE and ATTRIBUTION.md)
compatibility: Authenticated GitHub CLI and Python 3 on macOS or Linux for the bundled watcher.
---

# Babysit PR

Monitoring authorizes read-only observation, not public comments, resolving threads, pushing, rebasing a shared branch, merging, or changing auto-merge/queue state. Obtain explicit authorization for required mutations; local fixes follow the task's scope. Delegated reviewers remain read-only.

## Inspect before waiting

Read the current PR head/base, CI, human reviews, and unresolved feedback using the harness's PR-comment reader when available. The watcher's first run records a baseline rather than replaying existing comments. Revalidate unresolved older findings against the current head; an old timestamp alone does not dismiss them.

Use one watcher per PR. Honor the global session-host policy: in a verified T3 session, use its PR watcher if available and owned by this coordinating thread. Otherwise run the bundled helper. Never run both. Local locks do not coordinate Fleet hosts, so check known existing watchers first; leave unrelated processes alone.

## Bundled watcher

Resolve `scripts/pr-wait` relative to this skill's installed directory and invoke its absolute path:

```bash
/absolute/path/to/babysit-pr/scripts/pr-wait <pr> --repo owner/name --until green
```

Use `green` for repositories without Greptile/Macroscope. Use `ready` only when one of those bots is expected; it also checks unresolved threads. `any-change` returns on a new event. The script defaults to `ready`, so always specify the intended mode.

The helper reads GitHub and writes resumable state/locks under `~/.local/state/pr-wait/`. It polls every 20 seconds and has no built-in total timeout. Run it in a cancellable harness command with a 30-minute deadline unless the user specifies another budget. On timeout, stop the owned process and report pending work; do not silently restart forever. With no bounded command facility, inspect once and report that continuous monitoring is unavailable.

- Exit 0: the selected condition was met **or the PR merged**. Inspect the actual result.
- Exit 1: intervention needed, including failed checks, conflicts, closure, or API failure.
- Exit 2: invalid target/arguments or another local watcher holds the lock.

Restart only after handling the event, an authorized push, or a resume, within the remaining budget. Report meaningful changes rather than “still waiting.” If using T3's event delivery, end the turn only after the wake subscription is confirmed; unwatch before handing off or asking a question.

## Triage and handoff

Verify bot claims against source and the intended behavior. Fix real in-scope bugs; decline unsupported findings with evidence rather than growing the PR to satisfy reviewers. Run appropriate checks after fixes. Use the installed `leaving-pr-comments` skill for authorized replies; leave unapproved replies as drafts in the conversation.

Treat watcher output as news, not merge approval. It has bounded comment/thread queries, bot-specific heuristics, and some API-discovery failures are only warnings. Independently inspect the latest head, actual required checks, outstanding human change requests, required approvals, unresolved threads, and live mergeability before calling the PR ready. Unknown data means blocked, not approved.

Check base changes too: overlapping changes since the last green run or a BEHIND/DIRTY branch require reassessment and verification. Stop and recommend a disposition if another PR supersedes this work. Never bypass branch protection.

Report PR link, final head, ready/pending/blocked/merged state, verification, unresolved findings, and any required authorization. Merge only if separately authorized and all live gates pass. Read-only monitoring never changes auto-merge or queue membership.
