import assert from "node:assert/strict";
import { mkdtemp, mkdir, rm, symlink, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { validateRepository } from "./validate-skills.mjs";

async function fixture(options = {}) {
  const root = await mkdtemp(path.join(os.tmpdir(), "agent-skills-validation-"));
  const skillName = options.directory ?? "testing-things";
  const skillDirectory = path.join(root, "skills", skillName);
  await mkdir(path.join(skillDirectory, "references"), { recursive: true });
  const metadataName = options.name ?? skillName;
  const description = options.description ?? "Tests repository skills. Use when validating a fixture.";
  const metadata = options.metadata ?? `name: ${metadataName}\ndescription: ${description}\nlicense: MIT (see ATTRIBUTION.md)`;
  const body = options.body ?? "# Testing things\n\nRead [the reference](references/example.md).";
  const skillText = options.skillText ?? `---\n${metadata}\n---\n\n${body}\n`;
  await writeFile(path.join(skillDirectory, "SKILL.md"), skillText);
  await writeFile(path.join(skillDirectory, "references", "example.md"), "# Example\n");
  await writeFile(path.join(root, "README.md"), options.readme ?? `- \`${skillName}\` — fixture.\n`);
  await writeFile(
    path.join(root, "package.json"),
    JSON.stringify({ pi: { skills: options.piSkills ?? ["./skills"] } }),
  );
  if (options.prompt !== null) {
    await mkdir(path.join(skillDirectory, "agents"));
    await writeFile(
      path.join(skillDirectory, "agents", "openai.yaml"),
      options.agentText ?? `interface:\n  default_prompt: "${options.prompt ?? `Use $${skillName} for this task.`}"\n`,
    );
  }
  return root;
}

async function validateFixture(options) {
  const root = await fixture(options);
  try {
    return await validateRepository(root);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
}

test("accepts the current metadata subset and optional absent agent metadata", async () => {
  assert.deepEqual((await validateFixture({ prompt: null })).failures, []);
});

test("accepts exact name and description length boundaries", async () => {
  const name = `a${"b".repeat(63)}`;
  assert.deepEqual((await validateFixture({ directory: name, description: "d".repeat(1024) })).failures, []);
  assert.match((await validateFixture({ directory: `${name}c` })).failures.join("\n"), /name must be 1–64/);
});

test("rejects duplicate, missing, and mismatched metadata", async () => {
  assert.match((await validateFixture({ metadata: "name: testing-things\nname: testing-things" })).failures.join("\n"), /duplicate name.*missing description/s);
  assert.match((await validateFixture({ metadata: "name: testing-things\ndescription: Valid\ndescription:" })).failures.join("\n"), /duplicate description/);
  assert.match((await validateFixture({ metadata: "description: Valid description" })).failures.join("\n"), /missing name/);
  assert.match((await validateFixture({ name: "testing-others" })).failures.join("\n"), /name must match directory/);
});

test("rejects unsupported metadata scalars", async () => {
  for (const description of ['""', "null", "|\n  Multiline description."]) {
    const result = await validateFixture({ metadata: `name: testing-things\ndescription: ${description}` });
    assert.match(result.failures.join("\n"), /description must use a non-empty unquoted single-line scalar/);
  }
});

test("rejects metadata overflow and counts physical entrypoint lines", async () => {
  assert.match((await validateFixture({ description: "d".repeat(1025) })).failures.join("\n"), /description must be/);
  const entrypoint = ["---", "name: testing-things", "description: Valid description", "---"];
  while (entrypoint.length < 499) entrypoint.push(`line ${entrypoint.length + 1}`);
  assert.deepEqual((await validateFixture({ skillText: `${entrypoint.join("\n")}\n` })).failures, []);
  assert.deepEqual((await validateFixture({ skillText: entrypoint.join("\n") })).failures, []);
  entrypoint.push("line 500");
  assert.match((await validateFixture({ skillText: `${entrypoint.join("\n")}\n` })).failures.join("\n"), /under 500 lines/);
});

test("rejects broken packaged links", async () => {
  const result = await validateFixture({ body: "Read [missing](references/missing.md)." });
  assert.match(result.failures.join("\n"), /missing packaged relative link/);
  const malformed = await validateFixture({ body: "Read [invalid](references/%GG.md)." });
  assert.match(malformed.failures.join("\n"), /invalid encoded relative link/);
});

test("rejects relative links whose symlink target leaves the skill package", async () => {
  const root = await fixture({ body: "Read [outside](references/outside.md)." });
  try {
    await writeFile(path.join(root, "outside.md"), "# Outside\n");
    await symlink(path.join(root, "outside.md"), path.join(root, "skills", "testing-things", "references", "outside.md"));
    assert.match((await validateRepository(root)).failures.join("\n"), /missing packaged relative link/);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("ignores links inside variable-length fenced code blocks", async () => {
  const body = "# Fences\n\n````markdown\n[missing](references/missing.md)\n````";
  assert.deepEqual((await validateFixture({ body })).failures, []);
});

test("rejects a stale or duplicate README inventory", async () => {
  assert.match((await validateFixture({ readme: "- `other-skill` — stale.\n" })).failures.join("\n"), /inventory must equal/);
  const duplicate = "- `testing-things` — first.\n- `testing-things` — duplicate.\n";
  assert.match((await validateFixture({ readme: duplicate })).failures.join("\n"), /inventory must equal/);
});

test("rejects a missing Pi discovery path", async () => {
  assert.match((await validateFixture({ piSkills: ["./missing"] })).failures.join("\n"), /pi\.skills must include/);
});

test("checks an exact skill token only when default_prompt is present", async () => {
  const wrong = await validateFixture({ prompt: "Use $testing-things-extra for this task." });
  assert.match(wrong.failures.join("\n"), /exact \$testing-things token/);
  const unrelated = await validateFixture({
    agentText: 'interface:\n  short_description: "$testing-things"\n  default_prompt: "Use another skill."\n',
  });
  assert.match(unrelated.failures.join("\n"), /exact \$testing-things token/);
  assert.deepEqual((await validateFixture({ agentText: "interface:\n  display_name: Testing Things\n" })).failures, []);
  assert.deepEqual((await validateFixture({ prompt: "Use $testing-things for this task." })).failures, []);
});

test("scopes default_prompt to interface and rejects unsupported values", async () => {
  const masked = await validateFixture({
    agentText: 'other:\n  default_prompt: "Use $testing-things."\ninterface:\n  default_prompt: "Use another skill."\n',
  });
  assert.match(masked.failures.join("\n"), /exact \$testing-things token/);
  assert.deepEqual(
    (await validateFixture({ agentText: 'other:\n  default_prompt: "Use another skill."\ninterface:\n  display_name: Testing Things\n' })).failures,
    [],
  );
  const empty = await validateFixture({
    agentText: 'interface:\n  default_prompt:\n  short_description: "Use $testing-things."\n',
  });
  assert.match(empty.failures.join("\n"), /default_prompt must use a non-empty single-line scalar/);
  const quotedEmpty = await validateFixture({ agentText: 'interface:\n  default_prompt: ""\n' });
  assert.match(quotedEmpty.failures.join("\n"), /default_prompt must use a non-empty single-line scalar/);
  const multiline = await validateFixture({ agentText: "interface:\n  default_prompt: |\n    Use $testing-things.\n" });
  assert.match(multiline.failures.join("\n"), /default_prompt must use a non-empty single-line scalar/);
  const flow = await validateFixture({ agentText: "interface:\n  default_prompt: [Use $testing-things]\n" });
  assert.match(flow.failures.join("\n"), /default_prompt must use a non-empty single-line scalar/);
});
