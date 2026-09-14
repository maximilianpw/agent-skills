---
name: code-review
description: Review changes since a fixed point against repository standards and the originating spec as separate axes. Use for branch, pull-request, work-in-progress, or 'review since X' requests.
---

# Code Review

Review one fixed diff twice:

- **Standards:** whether the change follows the repository's documented rules and established patterns.
- **Spec:** whether the change implements the requested behavior without omissions or scope creep.

Keep the axes separate so success on one cannot hide failure on the other.

## 1. Pin the review range

Use the user's commit, branch, tag, or merge-base when supplied. Otherwise infer the default branch and compare from its merge-base. Include uncommitted changes when the user asks to review work in progress.

Confirm the fixed point resolves and the resulting diff is non-empty. Record the exact diff command and changed-file list once so both reviews inspect the same change.

## 2. Find the spec

Look for intent in this order:

1. A path, issue, pull request, or acceptance criteria supplied by the user.
2. References in commit messages or branch metadata.
3. Matching files under `docs/`, `specs/`, `plans/`, `goals/`, or the repository's equivalent.
4. Existing tests that clearly encode the requested behavior.

Ask only when the missing spec prevents an honest review. If there is no spec, skip that axis and say so.

## 3. Find the standards

Read every applicable `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, coding standard, ADR, and language/framework skill. Treat repository-specific decisions as authoritative. Tool-enforced formatting is not a review finding.

## 4. Run independent reviews

When background subagents are available, consult `model-routing` and run the Standards and Spec reviews in parallel. Give both agents the exact fixed point, diff command, changed files, and repository context. Give each only the sources needed for its axis.

If subagents are unavailable, perform the two passes sequentially and keep their notes separate.

Each finding must include:

- impact and concrete failure mode;
- `file:line` evidence from the changed code;
- the violated standard or quoted spec requirement;
- confidence and whether the problem was introduced by the reviewed change.

Return findings only, not a rewritten diff.

## 5. Vet and report

Open every cited location yourself. Reject duplicates, wrong line references, tooling-only style notes, and behavior that repository docs explicitly chose. Do not repeat an unverified subagent claim.

Report:

```markdown
## Standards
- ...

## Spec
- ...

## Summary
- Standards: N findings; worst issue ...
- Spec: N findings; worst issue ...
```

If an axis has no findings, say it passed. If it could not be reviewed, state the missing evidence. The review is complete when both axes are either vetted or explicitly marked unavailable.
