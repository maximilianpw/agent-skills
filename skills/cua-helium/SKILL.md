---
name: cua-helium
description: Use Cua Driver, through the computer MCP server or the cua-driver CLI, to operate Helium on macOS or Linux. Use when driving, automating, inspecting, or navigating the Helium browser, especially when browser profiles or authenticated identity matter.
compatibility: Requires the upstream cua-driver skill, Helium, and either the configured computer MCP server or the cua-driver CLI.
---

# Cua Driver with Helium

Use this skill together with the upstream `cua-driver` skill. Read that skill's `SKILL.md` and applicable platform/browser references completely before acting; its snapshot-before-action and verification rules remain authoritative.

Leave the upstream skill unmodified: whichever tool installs it (Nix, the Skills CLI, or a manual copy) owns its files and updates. This skill adds only the Helium workflow, so read both.

## Transport

When the harness has the persistent `computer` MCP server, prefer it for multi-step GUI workflows. `~/pi-config/mcp.json` defines it for Pi as:

```text
computer -> cua-driver mcp
```

The server starts lazily, keeps the connection alive, does not inherit Pi's full environment, and requires approval for every MCP tool call.

Discover the live tools from the `computer` server before use. Describe an unfamiliar tool once, then reuse its installed schema. Keep one transport for an ordered workflow: do not mix one-shot CLI actions into an active MCP sequence.

If `computer` is configured but disconnected, reconnect it once and rediscover its tools. Harnesses without that server use the `cua-driver` CLI as the upstream skill describes. A permission refusal is not a connection failure: stop and ask for the required OS permission or foreground authorization. Do not substitute AppleScript or global-pointer tools after a Cua refusal.

## Cross-platform Helium identity

Helium is the preferred Chromium browser on both supported desktop platforms:

| Platform | Application target | Installation |
| --- | --- | --- |
| macOS | bundle ID `net.imput.helium` | Homebrew cask `helium-browser` |
| Linux | application/executable `helium` | Nix package `helium` |

Use live application and window discovery rather than assuming a PID, process name, or window title. Select an exact Helium window before taking state or acting.

A Helium window may belong to a different browser profile or signed-in identity. Before navigating or changing authenticated state:

1. Prefer an already-open window whose visible profile or account marker matches the task.
2. Inspect the profile control or signed-in account marker when identity matters.
3. Ask the user when the intended profile is ambiguous or multiple identities could satisfy the request.
4. Never infer the profile from a window title alone.

Do not encode profile names, account names, email addresses, or profile-directory paths in this public skill.

## Browser route

Read the upstream `cua-driver` skill's `BROWSER.md` before using typed browser tools or preparing Chromium debugging.

Do not assume Helium supports Cua's typed Chromium page route merely because it is Chromium-based. First bind the exact native Helium window using the installed browser tools. If the browser route is unavailable or refuses the existing profile, continue through native window accessibility and pixel actions.

Never enable remote debugging, relaunch an authenticated profile, change browser policy, or widen existing-profile authorization solely to make automation easier without the user's approval. Keep browser-page identity separate from native-window identity: a page target does not authorize another Helium window or profile.

## Safety and verification

Prefer APIs, CLIs, and filesystem operations for non-GUI outcomes. Use Cua for authenticated UI, native application state, and visual verification.

Keep background delivery and the visible agent cursor by default. Foreground or desktop takeover, including temporarily activating Helium for a native menu operation, requires existing authorization or a new approval. After every action, verify the requested postcondition from fresh state; successful delivery is not task completion. Never retry text insertion before inspecting whether the first attempt landed.

Do not enable recording or history automatically. Do not persist screenshots, accessibility trees, URLs, account markers, or captured browser state in this public repository.

## Configuration ownership

- `~/pi-config/mcp.json` owns the `computer` MCP server definition.
- `~/nix-config` owns the Cua Driver binary and upstream `cua-driver` skill on desktop hosts, Helium on Linux, and Helium availability on macOS.
- This skill owns only the agent workflow connecting those capabilities.

When configuration changes, verify this integration against the installed `cua-driver` version and live MCP schemas. Preserve upstream safety invariants rather than copying stale tool names forward.
