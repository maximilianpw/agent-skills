---
name: auditing-code
description: Comprehensive code audit of a diff or entire repo. Use for /audit, audit the repo, audit this diff, run audit, security audit, or code audit.
---

# Code Audit Skill

Perform a deep, structured audit of either the current diff (uncommitted/staged changes) or the full repository.

## Invocation

The user triggers this skill with `/audit` or phrases like "audit the repo", "audit this diff", "run an audit".

## Step 1 — Determine Scope

Ask the user (or infer from their message) which mode to run:

| Mode | What it covers |
|------|---------------|
| **diff** (default) | Uncommitted + staged changes (`git diff HEAD`) |
| **branch** | Changes between current branch and `main`/`master` (`git diff main...HEAD`) |
| **repo** | Full repository scan (heavier — warn the user it may take a moment) |

If the user just says "/audit" with no qualifier, default to **diff** mode. If the diff is empty, fall back to **repo** mode automatically.

## Step 2 — Run the Audit

### 2a. Gather context

1. Read `AGENTS.md` / `CLAUDE.md` at the repo root (if they exist) to learn project-specific rules.
2. Read `package.json`, `tsconfig.json`, or equivalent config files to understand the stack.
3. For **diff/branch** mode: generate the diff with `git diff` (use `--stat` first to see scope, then full diff for changed files).
4. For **repo** mode: use `find` / `glob` to enumerate source files, then sample key files (entry points, configs, routers, services).

### 2b. Audit checklist

Run each category below. For **diff/branch** mode, focus only on changed code and its immediate context. For **repo** mode, scan broadly.

#### 🔒 Security
- Hardcoded secrets, API keys, tokens, passwords
- SQL injection, XSS, command injection vectors
- Missing input validation / sanitization at boundaries
- Insecure dependencies (check for known patterns)
- PII logging (tokens, passwords, payment data in logs)
- Missing authentication / authorization checks
- Insecure crypto or hashing usage
- CORS misconfiguration

#### 🐛 Bugs & Correctness
- Null/undefined dereferences, unhandled promise rejections
- Off-by-one errors, race conditions
- Swallowed exceptions (empty catch blocks)
- Incorrect type assertions / unsafe casts (`as any`)
- Dead code that may indicate incomplete refactors
- Missing error handling on I/O operations (DB, HTTP, file)

#### 🏗️ Architecture & Design
- SOLID violations (god classes, tight coupling)
- Circular dependencies
- Business logic in wrong layer (e.g., controllers doing DB queries)
- Missing abstractions or over-abstractions
- Inconsistent patterns across similar modules

#### ⚡ Performance
- N+1 query patterns
- Missing pagination on list endpoints
- Unbounded loops or memory allocations
- Missing indexes (if schema files are present)
- Synchronous blocking in async contexts
- Unnecessary re-renders (frontend)

#### 📝 Code Quality
- Missing or outdated JSDoc on public APIs
- `console.log` in production code (should use structured logging)
- Inconsistent naming conventions
- Overly complex functions (high cyclomatic complexity)
- Missing tests for new/changed behavior
- Import order violations (per project conventions)

#### 🔧 Configuration & DevOps
- Secrets in config files or environment defaults
- Missing environment variable validation
- Dockerfile issues (running as root, missing health checks)
- Missing or misconfigured CI checks

### 2c. Use the `code_review` tool

For **diff** and **branch** modes, also invoke the built-in `code_review` tool to get a complementary automated review:
- For diff mode: `diff_description` = "uncommitted and staged changes (git diff HEAD)"
- For branch mode: `diff_description` = "changes between main and current branch (git diff main...HEAD)"

Pass `instructions` summarizing any project-specific rules from AGENTS.md.

## Step 3 — Report

Present findings as a structured markdown report:

```
# 🔍 Audit Report — [mode] mode

**Scope**: [description of what was audited]
**Files scanned**: [count]
**Severity summary**: 🔴 Critical: N | 🟠 High: N | 🟡 Medium: N | 🔵 Low: N | ✅ Info: N

---

## 🔴 Critical Issues
1. **[category]** — [file:line]: one-sentence summary
   > Brief explanation and recommended fix

## 🟠 High Issues
...

## 🟡 Medium Issues
...

## 🔵 Low Issues
...

## ✅ What Looks Good
- Brief list of things done well (positive reinforcement)

---

## Recommendations
1. Prioritized list of next steps
```

### Severity definitions

| Severity | Meaning |
|----------|---------|
| 🔴 Critical | Security vulnerabilities, data loss risks, production-breaking bugs |
| 🟠 High | Bugs likely to surface, significant design issues |
| 🟡 Medium | Code quality issues, minor bugs, missing tests |
| 🔵 Low | Style issues, minor improvements, nitpicks |
| ✅ Info | Observations, things done well |

## Rules

- Be **specific**: always cite file paths and line numbers.
- Be **actionable**: every issue must include a concrete fix suggestion.
- Be **honest**: if nothing is wrong, say so. Don't invent issues.
- **Respect project conventions**: check AGENTS.md / CLAUDE.md and apply those rules.
- When in **repo** mode, prioritize breadth over depth — flag patterns, don't read every line.
- Keep the report scannable — one line per issue in the summary, details in expandable sections if needed.

## After the Report

Ask: "Would you like me to fix any of these issues? (e.g., 'fix #1' or 'fix all critical')"
