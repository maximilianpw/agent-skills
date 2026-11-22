---
name: cua-helium
description: Operate the Helium browser on macOS or Linux through the `computer` MCP server (Cua Driver). Use when driving, automating, inspecting, or navigating Helium, especially when browser profiles or authenticated identity matter.
compatibility: Requires Helium and the `computer` MCP server.
---

# Cua Driver with Helium

The `computer` MCP server is Cua Driver. Its instructions, sent when it connects, are the general rules for driving any app: find the window, read narrowly, act by element token, batch with `run_steps`, and verify at checkpoints. Follow them. This skill adds only what is specific to Helium.

## Transport

Use the `computer` MCP server. It runs `fleet computer <host>`, which is `cua-driver mcp` on the desktop host itself and the same server over SSH from any other host, so the windows it sees belong to that desktop, not necessarily to the machine you run on.

Discover its tools before use, describe an unfamiliar tool once, then reuse its schema. For deeper guidance call `get_guide` with a topic (`browser`, `menus`, `batching`, `drag`, `permissions`) instead of guessing; it comes from the running driver, so it matches its tools.

If the server is disconnected, reconnect once and rediscover its tools. If it fails to start, the desktop host is probably asleep, locked, or offline: say so and stop rather than switching to another way of controlling the machine. A permission refusal is not a connection failure: stop and ask for the required OS permission or foreground authorization. Do not substitute AppleScript, shell input tools, or global-pointer tools after a Cua refusal.

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

Call `get_guide({topic: "browser"})` before using typed browser tools.

Do not assume Helium supports Cua's typed Chromium page route merely because it is Chromium-based. First bind the exact native Helium window with `get_browser_state`. If it refuses, follow its `next_call` only when that does not need any of the changes below; otherwise continue through the window's accessibility tree, and pixel actions where the tree cannot reach.

Never enable remote debugging, relaunch an authenticated profile, change browser policy, or widen existing-profile authorization solely to make automation easier without the user's approval. Keep browser-page identity separate from native-window identity: a page target does not authorize another Helium window or profile.

## Safety and verification

Prefer APIs, CLIs, and filesystem operations for non-GUI outcomes. Use Cua for authenticated UI, native application state, and visual verification.

Keep background delivery and the visible agent cursor by default. Foreground or desktop takeover, including temporarily activating Helium for a native menu operation, requires existing authorization or a new approval. After every action, verify the requested postcondition from fresh state; successful delivery is not task completion. Never retry text insertion before inspecting whether the first attempt landed.

Do not enable recording or history automatically. Do not persist screenshots, accessibility trees, URLs, account markers, or captured browser state in this public repository.

## Configuration ownership

- `~/nix-config` declares the `computer` MCP server for every agent harness, and installs Cua Driver on desktop hosts, Helium on Linux, and Helium's availability on macOS.
- This skill owns only the Helium workflow on top of that server.

When the driver is updated, trust the server's live instructions, guides, and schemas over anything in this file, and preserve their safety rules rather than copying stale tool names forward.
