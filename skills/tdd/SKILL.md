---
name: tdd
description: Test-driven development for an explicitly requested red-green loop or a bug with an obvious cheap regression-test target. Skip when the test path is unclear, expensive, integration-heavy, or not requested.
---

# Test-Driven Development

Make the broken behavior executable before changing production code. The goal is a focused test worth keeping, not compliance with a ritual.

## Loop

1. Identify the intended behavior, current behavior, affected path, and smallest observable reproduction.
2. Choose the narrowest public seam already used by the codebase. Inspect the repository before asking; ask only when choosing the seam requires product or architecture judgment.
3. Write one focused test that would have caught the behavior. Use an independent expected value rather than recomputing the implementation.
4. Run the test before the fix. It must fail for the intended reason. Correct a passing or unrelated failure before touching production code.
5. Make the smallest production change that satisfies the behavior.
6. Rerun the focused test until it passes.
7. Refactor only while the test remains green, then run nearby tests and the smallest relevant type, lint, build, or scenario checks.
8. Repeat one vertical slice at a time when the requested behavior contains several independently observable cases.

## Practical escape hatch

Do not force a new test through brittle mocks, broad harness setup, production-only state, slow unrelated infrastructure, or large fixture churn. Before fixing, state why red-before-green is impractical and choose the closest faithful executable check: a disposable script, browser action, integration command, snapshot comparison, or log assertion.

Prefer no new test over one coupled to private implementation details. Keep existing assertions unless the expected behavior genuinely changed.

## Completion

Report:

- the failing-before test or executable check and its relevant failure;
- the passing-after run;
- nearby verification performed;
- any case where red-before-green could not be demonstrated and why.

The loop is complete only when the changed behavior has executable before/after evidence or an explicit, justified substitute.
