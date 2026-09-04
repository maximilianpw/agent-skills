import { lstat, readFile, readdir, realpath } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath, pathToFileURL } from "node:url";

const skillNamePattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const markdownLinkPattern = /\[[^\]\r\n]+\]\(([^)\r\n]+)\)/g;

async function isPresent(file) {
  try {
    await lstat(file);
    return true;
  } catch (error) {
    if (error.code === "ENOENT") return false;
    throw error;
  }
}

async function listMarkdownFiles(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...(await listMarkdownFiles(file)));
    else if (entry.isFile() && entry.name.endsWith(".md")) files.push(file);
  }
  return files;
}

function withoutFencedCode(text) {
  let fence;
  return text
    .split(/\r?\n/)
    .map((line) => {
      const marker = line.match(/^ {0,3}(`{3,}|~{3,})/u)?.[1];
      if (!fence && marker) {
        fence = { character: marker[0], length: marker.length };
        return "";
      }
      if (fence) {
        const closing = line.match(/^ {0,3}(`+|~+)[ \t]*$/u)?.[1];
        if (closing?.[0] === fence.character && closing.length >= fence.length) fence = undefined;
        return "";
      }
      return line;
    })
    .join("\n");
}

function parseMetadata(file, text, failures) {
  const frontmatter = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1];
  if (frontmatter === undefined) {
    failures.push(`${file}: missing frontmatter`);
    return {};
  }

  const values = {};
  const counts = { name: 0, description: 0 };
  for (const line of frontmatter.split(/\r?\n/)) {
    const match = line.match(/^(name|description):[ \t]*(.*)$/u);
    if (!match) continue;
    const [, key, rawValue] = match;
    counts[key] += 1;
    if (counts[key] > 1) {
      failures.push(`${file}: duplicate ${key} metadata`);
      continue;
    }
    const value = rawValue.trim();
    if (!value || /^["'|>{[]/u.test(value) || /^(?:null|~)$/iu.test(value)) {
      failures.push(`${file}: ${key} must use a non-empty unquoted single-line scalar`);
      continue;
    }
    values[key] = value;
  }
  for (const key of ["name", "description"]) {
    if (counts[key] === 0) failures.push(`${file}: missing ${key} metadata`);
  }
  return values;
}

function parseInterfacePrompt(file, text, failures) {
  let inInterface = false;
  let prompt;
  let promptCount = 0;
  for (const line of text.split(/\r?\n/)) {
    if (/^[^ \t]/u.test(line)) inInterface = line === "interface:";
    if (!inInterface) continue;
    const match = line.match(/^ {2}default_prompt:[ \t]*(.*)$/u);
    if (!match) continue;
    promptCount += 1;
    if (promptCount > 1) {
      failures.push(`${file}: duplicate interface.default_prompt`);
      continue;
    }
    const value = match[1].trim();
    const quoted = value.match(/^(["'])(.*)\1$/u)?.[2];
    if (!value || quoted === "" || /^[|>[{]/u.test(value) || /^(?:null|~)$/iu.test(value) || (/^["']/u.test(value) && quoted === undefined)) {
      failures.push(`${file}: interface.default_prompt must use a non-empty single-line scalar`);
      continue;
    }
    prompt = quoted ?? value;
  }
  return prompt;
}

function countPhysicalLines(text) {
  if (!text) return 0;
  const trailingTerminator = /(?:\r\n|\n|\r)$/u.test(text) ? 1 : 0;
  return text.split(/\r\n|\n|\r/u).length - trailingTerminator;
}

export async function validateRepository(root) {
  const failures = [];
  const relative = (file) => path.relative(root, file) || ".";
  const skillsDirectory = path.join(root, "skills");
  const skillDirectories = (await readdir(skillsDirectory, { withFileTypes: true }))
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();

  for (const skillName of skillDirectories) {
    const skillDirectory = path.join(skillsDirectory, skillName);
    const realSkillDirectory = await realpath(skillDirectory);
    const skillFile = path.join(skillDirectory, "SKILL.md");
    if (!(await isPresent(skillFile))) {
      failures.push(`${relative(skillFile)}: missing skill entrypoint`);
      continue;
    }

    const skillText = await readFile(skillFile, "utf8");
    const metadataFailures = [];
    const metadata = parseMetadata(relative(skillFile), skillText, metadataFailures);
    failures.push(...metadataFailures);
    if (metadata.name !== undefined) {
      if (metadata.name !== skillName) failures.push(`${relative(skillFile)}: name must match directory ${skillName}`);
      if (!skillNamePattern.test(metadata.name) || metadata.name.length > 64) {
        failures.push(`${relative(skillFile)}: name must be 1–64 lowercase letters, numbers, or single hyphens`);
      }
    }
    if (metadata.description !== undefined && (metadata.description.length === 0 || metadata.description.length > 1024)) {
      failures.push(`${relative(skillFile)}: description must be 1–1024 characters`);
    }
    if (countPhysicalLines(skillText) >= 500) failures.push(`${relative(skillFile)}: SKILL.md must be under 500 lines`);

    const agentFile = path.join(skillDirectory, "agents", "openai.yaml");
    if (await isPresent(agentFile)) {
      const agentText = await readFile(agentFile, "utf8");
      const promptFailures = [];
      const prompt = parseInterfacePrompt(relative(agentFile), agentText, promptFailures);
      failures.push(...promptFailures);
      if (prompt !== undefined) {
        const escapedName = skillName.replaceAll("-", "\\-");
        if (!new RegExp(`\\$${escapedName}(?![a-z0-9-])`).test(prompt)) {
          failures.push(`${relative(agentFile)}: default_prompt must contain the exact $${skillName} token`);
        }
      }
    }

    for (const markdownFile of await listMarkdownFiles(skillDirectory)) {
      const markdown = withoutFencedCode(await readFile(markdownFile, "utf8"));
      for (const match of markdown.matchAll(markdownLinkPattern)) {
        const target = match[1].trim();
        if (target.startsWith("#") || /^[a-z][a-z0-9+.-]*:/i.test(target)) continue;
        let decodedTarget;
        try {
          decodedTarget = decodeURIComponent(target.split("#", 1)[0]);
        } catch (error) {
          failures.push(`${relative(markdownFile)}: invalid encoded relative link ${target} (${error.message})`);
          continue;
        }
        const linkedPath = path.resolve(path.dirname(markdownFile), decodedTarget);
        const packagedPath = path.relative(skillDirectory, linkedPath);
        let realLinkedPath;
        try {
          realLinkedPath = await realpath(linkedPath);
        } catch (error) {
          if (error.code !== "ENOENT") throw error;
        }
        const realPackagedPath = realLinkedPath && path.relative(realSkillDirectory, realLinkedPath);
        const leavesPackage = (candidate) => candidate === ".." || candidate.startsWith(`..${path.sep}`) || path.isAbsolute(candidate);
        if (leavesPackage(packagedPath) || !realLinkedPath || leavesPackage(realPackagedPath)) {
          failures.push(`${relative(markdownFile)}: missing packaged relative link ${target}`);
        }
      }
    }
  }

  const readme = await readFile(path.join(root, "README.md"), "utf8");
  const inventory = [...readme.matchAll(/^- `([^`]+)` —/gm)].map((match) => match[1]);
  if (new Set(inventory).size !== inventory.length || JSON.stringify(inventory) !== JSON.stringify(skillDirectories)) {
    failures.push(`README.md: skill inventory must equal ${skillDirectories.join(", ")}`);
  }

  const manifest = JSON.parse(await readFile(path.join(root, "package.json"), "utf8"));
  if (!Array.isArray(manifest.pi?.skills) || !manifest.pi.skills.includes("./skills") || !(await isPresent(skillsDirectory))) {
    failures.push("package.json: pi.skills must include the existing ./skills directory");
  }

  return { failures, skillCount: skillDirectories.length };
}

const invokedFile = process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href;
if (invokedFile === import.meta.url) {
  const root = path.resolve(process.argv[2] ?? path.join(path.dirname(fileURLToPath(import.meta.url)), ".."));
  const result = await validateRepository(root);
  if (result.failures.length > 0) {
    console.error(`Skill validation failed (${result.failures.length}):`);
    for (const failure of result.failures) console.error(`- ${failure}`);
    process.exitCode = 1;
  } else {
    console.log(`Validated ${result.skillCount} skills.`);
  }
}
