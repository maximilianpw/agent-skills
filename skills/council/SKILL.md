---
name: council
description: Gather independent reviews from two model providers with a bounded reconciliation loop. Use when the user explicitly requests a council review.
license: MIT (see LICENSE and ATTRIBUTION.md)
---

# Council

Run two independent, read-only reviewers from different model providers. The coordinating agent owns synthesis, any authorized implementation, verification, and user interaction. A council request alone is review permission, not permission to edit or publish.

## Select the panel

Load the installed `model-routing` skill and use its **Council defaults**, unless the user names members. Check availability before the batch and resolve actual model IDs through the host/harness model catalog. “Different providers” means model creators, even if all requests travel through the same proxy. Use high reasoning effort where supported; report the actual setting rather than inventing one.

Honor global session-host orchestration policy: verified T3 orchestration takes precedence; otherwise use the supported backend for bounded read-only delegates. Use explicit repository/workspace binding. If either selected member cannot run, report the missing seat and ask before changing the panel. Failed or missing reviews never count as approval.

## Review independently

Pin the intent, exclusions, base SHA and diff command (or exact design documents), scoped paths, untracked files, and available check results. Preserve unrelated work. Give every reviewer the same brief and independent access to the source, without the other reviewers' opinions.

Each brief must specify:

- Read-only work; no edits, commits, pushes, PR comments, or recursive delegates.
- Find evidence-backed correctness, safety, or intent problems; keep recommendations within scope.
- Return APPROVE or CHANGES, stable finding IDs, severity, file:line/source evidence, and minimal remedies. For code review, include a score out of 10 with a short rationale.

Run both reviewers in parallel. Keep scoped files unchanged until they finish. Wait through the host's result delivery, not polling or duplicate launches.

## Reconcile within budget

Default to **three rounds maximum**, including the first pass. Additional rounds require the user's request. Maintain a ledger of findings, severity, evidence, and fixed/disputed/declined outcomes. Check claims yourself; votes and scores are not proof. Preserve substantive minority concerns and report disagreements explicitly.

If implementation is already authorized, apply only justified in-scope fixes in the main thread and run the relevant checks. Otherwise present recommendations and stop without editing. Later rounds review deltas and unresolved findings against the same base, without reopening settled nits. Stop early if only optional nits remain.

Finish with agreement on the current reviewed diff, or a clearly labeled unresolved/budget-exhausted result. A changed behavior diff needs fresh coverage; expiry is not consensus. A repeatedly disputed material finding goes to the user rather than forcing agreement.

## Report

Summarize verified model identities, rounds, strongest findings, disagreements, check results, and remaining risks. For code review, show a model-by-round score table; write `no score` when absent. Scores summarize opinions, not an approval gate.

Put the report in the conversation. Updating a PR description requires explicit publication authorization; when authorized, put the council section before the model/harness attribution and verify the update. Council review never authorizes merging, pushing, public comments, or changing merge-queue state.
