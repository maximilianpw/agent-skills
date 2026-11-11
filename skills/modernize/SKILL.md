---
name: modernize
description: Reassess and rebase an old PR against its current base and architecture. Use when asked to modernize or rebase a PR.
license: MIT (see LICENSE and ATTRIBUTION.md)
---

# Modernize

Modernize the idea, not just the branch. A clean rebase does not prove the PR still belongs.

## Establish intent

1. Record the PR URL, state, actual base, head repository/branch/SHA, author, checks, and review state. Read its body, linked issues, commits, feedback, and complete diff. Use the harness's PR-comment reader when available.
2. Inspect local status. Preserve unrelated edits; use a disposable worktree when the active tree is dirty or occupied. Fetch the actual remote base and head, then record the merge base and original head.
3. State the smallest coherent goal. Inspect base changes since divergence and competing open or merged PRs. Look for replaced APIs, deleted code, changed invariants, duplicate ownership, and an already-solved problem.

## Choose before rebasing

- **MODERNIZE:** the goal and implementation still fit. Rebase and verify locally.
- **REWORK:** the goal matters but a mechanical rebase preserves the wrong design. Explain the smallest rewrite; obtain authorization if it changes the requested scope.
- **CLOSE:** the work is superseded or no longer worthwhile. Cite evidence and stop without closing the PR.

A modernization request alone does not authorize publication, force-pushing, merging, closing, or changing the PR base. Follow the consuming repository's approval policy; request missing authorization before those actions.

## Preserve intent

1. Rebase a safe local branch at the recorded head onto the fetched base.
2. Resolve conflicts using current invariants and the original goal. Reconsider the disposition when a conflict reveals a product decision.
3. Compare the original and rebased commit series with `git range-diff`; inspect the final diff for lost behavior or reintroduced changes.
4. Run repository checks for the touched behavior and exercise its real surface where applicable. Separate introduced failures from existing failures and infrastructure blockers.
5. If explicitly authorized to update the PR, push only its branch with an explicit lease tied to the remote head recorded before rebasing. A failed lease means fetch and reassess, not overwrite.

Report the disposition first, then meaningful base changes, conceptual conflicts, verification, publication status, PR link, and remaining decisions. Posting a requested public reply uses the installed `leaving-pr-comments` skill; otherwise report in the conversation.
