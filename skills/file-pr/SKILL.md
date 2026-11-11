---
name: file-pr
description: Prepare or publish a concise, problem-first pull request. Use when asked to file, open, or create a PR.
license: MIT (see LICENSE and ATTRIBUTION.md)
---

# File PR

1. Inspect status and the complete diff against the actual target base. Preserve unrelated work and check for an existing PR for this branch before creating another.
2. Follow repository title conventions and PR templates. Lead with the user's problem and the benefit of the change, then briefly explain the solution. Keep required template sections; avoid an implementation inventory or unsupported performance claims.
3. Include verification actually performed and concrete limitations. Distinguish observed results from expectations.
4. End with the verified model and harness that made the change, including contributing implementation subagents when applicable. If identity is unavailable, name the harness without guessing.
5. Check the entire title, body, quotes, and attachments for secrets and private details.
6. Publish only within explicit authorization to push/create/update a PR. A request to draft text is not publication permission. Honor requests for a draft and repository draft policy; otherwise use a non-draft PR so review bots run.
7. Verify the returned PR URL, head, base, and draft state. If the user requested monitoring, continue with the installed `babysit-pr` skill. Otherwise hand off the link and verification summary.

Use authenticated `gh`. If GraphQL rate limits block creation, the REST endpoint `repos/<owner>/<repo>/pulls` is an alternative with the same authorization requirements; preserve the intended draft state. Do not retry creation blindly after an uncertain response—check whether the PR exists first.

Additional public comments require an actual purpose and authorization; use the installed `leaving-pr-comments` skill for their format.
