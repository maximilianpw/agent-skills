---
name: write-discoverable-code
description: Improve code findability through plain-text search. Use when naming or renaming exported symbols or files, shaping a module's public surface, moving or splitting code, defining errors or events, or reviewing a diff for discoverability.
license: MIT (see ATTRIBUTION.md)
---

# Write Discoverable Code

Plain-text search is the cheapest lookup tool and works across languages, tools, and partially indexed repositories. Shape code so a reader can search for the concept they know and reach its owner in one or two hops.

## Respect the codebase

Repository conventions, linters, language idioms, and framework-mandated names win. Apply these rules to code being created or intentionally refactored, not as permission for unrelated repository-wide cleanup.

Do not rename a published API, wire field, database column, telemetry identifier, feature flag, or localization key as a side effect. Use the compatibility or deprecation mechanism appropriate to that boundary.

## Make names useful search queries

- Reuse the domain vocabulary already present in code and documentation. One concept should keep one spelling unless a migration explicitly changes it.
- Give generic operations enough object and domain context to be distinguishable: `sanitizeEmailHtml` carries more signal than `sanitize` in a flat TypeScript module.
- Stop when the name plus its visible module or package context is unambiguous. Flat-import ecosystems often need context in the symbol; path-qualified ecosystems should avoid stuttering.
- Keep one authoritative definition for a behavior. Move and delete rather than copying implementations between homes.
- Rename when a private behavior's meaning or audience changes. For stable external contracts, preserve compatibility and point to the replacement.
- Avoid bare role names such as `utils.ts`, `helpers.ts`, or `types.ts` when several domains could produce the same search hit. Name files you are free to name after the concept they own. Framework names such as `page.tsx`, `route.ts`, `mod.rs`, or `conftest.py` are not violations.

## Put context where search lands

- Document a public symbol when its type cannot express a critical constraint such as units, timezone, ordering, ownership, mutation, or side effects.
- Include the natural-language phrase people are likely to search when the identifier's casing or terminology would hide it.
- Skip comments that merely restate a self-explanatory signature. A stale comment is worse than no comment.
- Keep stable event names, error codes, flags, and protocol identifiers as complete literals in a searchable definition. Construction may be dynamic, but the supported vocabulary should be findable verbatim when practical.
- Begin operational error messages with a stable, specific phrase so a log excerpt leads back to its origin. Keep variable context in structured fields or after that prefix.

## Let types carry meaning

Use the language and repository's existing type mechanisms when they make a public distinction easier to find and understand. Type design belongs to the project's language standards; this skill only checks that a reader landing on the definition can see the distinction without reconstructing distant context.

## Give each concept a home

- A module should answer a coherent question and expose an interface that points callers toward the implementation.
- Keep orchestrators focused on sequencing. Move substantial domain behavior into the module that names and owns it.
- Split new or intentionally refactored code when unrelated concepts make searches land on the same large file.
- Keep a helper local when it only supports one concept; a file per tiny function makes navigation worse.
- Follow the repository's test layout, and name tests after the behavior or unit they protect so searches connect specification and implementation.

## Review the diff

Before completion, check:

1. Can each new public concept be found using the words a maintainer is likely to know?
2. Does each concept use the repository's established spelling everywhere changed?
3. Do types or nearby documentation carry the important constraint instead of relying on distant context?
4. Can emitted error, event, flag, and protocol identifiers be searched verbatim in source?
5. Did moved behavior leave one owner, with old paths removed or explicitly deprecated?
6. Did file splitting improve a real navigation problem without broadening the requested change?
