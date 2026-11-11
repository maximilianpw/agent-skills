---
name: sol-loop
description: Run a bounded, evidence-led Sol review loop. Use when the user explicitly requests a sol loop.
license: MIT (see LICENSE and ATTRIBUTION.md)
---

# Sol loop

Use one read-only Sol reviewer; the coordinating agent owns decisions, implementation, checks, and user interaction. Load the installed `model-routing` skill for model availability and cross-harness routing. Resolve the configured Sol model through the available model catalog rather than guessing an API ID. Honor an explicitly requested version; if it cannot run, report the blocker instead of substituting.

## Scope and budget

Inspect status and preserve unrelated edits. Record a fixed base SHA against the actual PR base (or the user's local comparison point), one diff command, scoped paths, untracked files, intent, exclusions, and covering check results. A local review includes staged and unstaged changes, not just committed HEAD. If unrelated edits cannot be separated, ask before reviewing them.

Default to **three rounds total**. Extend to five only when the user requests it or evidence-backed security, permission, data-loss, or concurrency findings remain. Stop early for nits only. A budget ending or a reviewer timing out is not approval.

## Review

Honor the global session-host orchestration policy; use a bounded native subagent outside a verified orchestrator. Give the reviewer the repository path, fixed base, exact diff command, intent, scope, checks, and instructions:

> Review only; do not edit, commit, push, post comments, or spawn agents. Read surrounding code and untracked scoped files. Find concrete bugs and intent mismatches, not speculative expansions. Return APPROVE or CHANGES, followed by stable finding IDs, severity, file:line evidence, and the smallest proposed fix.

Use **blocker** for broken intended behavior or a serious safety issue, **should** for another evidenced defect in scope, and **nit** for optional improvements. Rare but material security or data-loss issues are not automatically nits.

Keep scoped files unchanged while the reviewer runs. Wait through the harness's result delivery; avoid duplicate reviewers. On failure, confirm the old task stopped before a bounded retry.

## Reconcile and repeat

Check each claim yourself. Record ID, severity, fixed/disputed/declined status, and evidence. Make the smallest justified fixes; decline scope creep explicitly. Re-run checks. Give later rounds the same base, ledger, complete scope, and delta, asking them to review changed code and open findings only.

Start another round only for an open substantive finding or behavior changes not covered by approval. Formatting-only changes and declined nits need no new round. A dispute surviving two replies goes to the user with evidence from both sides rather than another automatic round.

Finish when the current behavior diff is approved and no substantive finding remains, or report blocked/disputed/budget-exhausted. Summarize model, rounds, fixed and declined findings, checks, and remaining risk; report usage only when exposed. Publication is a separate explicit authorization, never a consequence of reviewer approval.
