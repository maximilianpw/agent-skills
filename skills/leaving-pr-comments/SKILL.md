---
name: leaving-pr-comments
description: Attribute and verify agent-authored GitHub comments. Use when preparing an authorized PR comment, inline review, or reply.
license: MIT (see LICENSE and ATTRIBUTION.md)
---

# Leaving PR comments

Posting or resolving review feedback requires authorization under the consuming repository's policy. Formatting a draft grants neither.

Prefix agent-authored comments posted on the user's behalf with:

```markdown
> [!NOTE]
> 🤖 **<model> responding on behalf of <user>**

Actual comment starts here.
```

Use the verified public model name and user's name or GitHub login. Use the harness name when the model is not exposed; avoid guessed identities.

Keep attribution inside the note and the reply outside it. Lead with the conclusion, cite relevant code or observed checks, and distinguish evidence from judgment. Avoid filler and status-only comments.

Apply this to top-level comments, inline reviews, replies, and explanations preceding thread resolution. Exclude PR descriptions, commit messages, and text explicitly requested verbatim without attribution.

Before posting, preview the Markdown and inspect quotes and attachments for secrets or private details. After posting, verify GitHub returned the comment/review URL. Resolve a thread only when authorized and after the response was successfully posted.
