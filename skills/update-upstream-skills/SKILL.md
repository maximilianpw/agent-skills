---
name: update-upstream-skills
description: Audit upstream-skills.json in the maximilianpw/agent-skills repository, checking attributed pstack, dmmulroy, and other adaptations against upstream. Use when maintaining this repository and asked for a full refresh of its upstream-derived skills.
---

# Update upstream skills

Maintain adapted skills against their upstream sources without replacing local decisions blindly. `upstream-skills.json` is the inventory and owns each reviewed commit pin. `ATTRIBUTION.md` presents that pin to readers.

## Check

1. Confirm the current repository contains `upstream-skills.json`. This skill is repository-specific; stop if the manifest is absent.
2. Read `git status --short`. Preserve unrelated work and never clean the worktree.
3. Run:

   ```bash
   python3 skills/update-upstream-skills/scripts/check_upstreams.py
   ```

   Exit `0` means every tracked upstream path matches its reviewed pin and every exact-copy file matches upstream. Exit `1` means review is required. Exit `2` means the check itself failed.
4. Read the reported `summary.json` and each generated `upstream.diff`. The checker writes only under `.scratch/upstream-skills/`.

The Skills CLI updates installed, unmodified skills by replacing them from one upstream `skillPath`. It cannot merge this repository's combined or renamed adaptations. Do not run `npx skills update` as the update mechanism for files under `skills/`.

## Review

For every entry requiring review:

1. Read the upstream diff from the pinned commit to the reported latest commit.
2. Read the local skill and its `ATTRIBUTION.md` in full.
3. Classify every upstream change:
   - **Port.** The change still applies. Adapt it while preserving the local skill's name, invocation, scope, cross-agent paths, and repository conventions.
   - **Sync exact copy.** A file listed in `exactFiles` has no intentional local edits. Exact-file handling wins over the general upstream diff. Replace it with the `.latest` artifact emitted by the checker. If the local file should diverge, remove its `exactFiles` mapping before dismissing or adapting it.
   - **Dismiss.** The change is Cursor-specific, superseded locally, outside the adaptation's scope, or otherwise inapplicable. Record the concrete reason.
4. Read every emitted license artifact at the new commit. Preserve required notices and update the local `LICENSE` when its terms or copyright notice changed.
5. Update `pinnedCommit` in `upstream-skills.json` plus the commit and commit link in `ATTRIBUTION.md` only after every upstream change has a disposition. The manifest pin means "reviewed through here," not "copied verbatim."
6. If an upstream path is missing, inspect the repository for a rename. Update `upstreamPaths` only after proving the replacement path owns the same skill.

When adding another upstream-derived skill, add one complete manifest entry with its attribution file, repository, ref, reviewed pin, upstream paths, license paths, and byte-for-byte file mappings. The entry is complete when the checker recognizes it and a second run is current.

## Verify

1. Run the smallest checks owned by every changed skill.
2. Validate each changed skill:

   ```bash
   uvx --from skills-ref agentskills validate skills/<name>
   ```

3. Confirm package discovery:

   ```bash
   npx --yes skills add . --list
   ```

4. Re-run the checker. It must exit `0`. A remaining tree change, attribution mismatch, or exact-file mismatch means the update is incomplete.
5. Run `git diff --check` and inspect the complete diff. Keep `.scratch/` out of the commit.

## Report

For each tracked skill, report:

- previous pin and reviewed upstream commit;
- upstream changes ported, exact-copied, or dismissed;
- local files changed;
- license changes;
- verification commands and results;
- anything blocked.
