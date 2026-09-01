#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_upstreams.py")


def run(
    command: list[str],
    cwd: Path,
    *,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, env=env)
    if check and result.returncode != 0:
        raise AssertionError(f"{' '.join(command)} failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    return result


def git(repo: Path, *args: str) -> str:
    return run(["git", *args], repo).stdout.strip()


class CheckUpstreamsTest(unittest.TestCase):
    def test_detects_and_clears_upstream_and_exact_file_drift(self) -> None:
        with tempfile.TemporaryDirectory(prefix="check-upstreams-test-") as temp:
            root = Path(temp)
            upstream = root / "upstream"
            project = root / "project"
            upstream.mkdir()
            project.mkdir()

            git(upstream, "init", "-b", "main")
            git(upstream, "config", "user.name", "Test")
            git(upstream, "config", "user.email", "test@example.com")
            skill = upstream / "skills" / "source-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("version one\n")
            (skill / "example.md").write_text("example one\n")
            stable_skill = upstream / "skills" / "stable-skill"
            stable_skill.mkdir(parents=True)
            (stable_skill / "SKILL.md").write_text("stable\n")
            git(upstream, "add", ".")
            git(upstream, "commit", "-m", "initial")
            pinned = git(upstream, "rev-parse", "HEAD")

            local_skill = project / "skills" / "adapted-skill"
            local_skill.mkdir(parents=True)
            attribution = local_skill / "ATTRIBUTION.md"
            attribution.write_text(f"Reviewed at {pinned}.\n")
            exact = local_skill / "example.md"
            exact.write_text("example one\n")
            stable_local = project / "skills" / "stable-adaptation"
            stable_local.mkdir(parents=True)
            stable_attribution = stable_local / "ATTRIBUTION.md"
            stable_attribution.write_text(f"Reviewed at {pinned}.\n")
            manifest = {
                "version": 1,
                "skills": [
                    {
                        "localSkill": "adapted-skill",
                        "attribution": "skills/adapted-skill/ATTRIBUTION.md",
                        "repository": str(upstream),
                        "ref": "main",
                        "pinnedCommit": pinned,
                        "upstreamPaths": ["skills/source-skill"],
                        "licensePaths": ["LICENSE"],
                        "exactFiles": [
                            {
                                "upstream": "skills/source-skill/example.md",
                                "local": "skills/adapted-skill/example.md",
                            }
                        ],
                    },
                    {
                        "localSkill": "stable-adaptation",
                        "attribution": "skills/stable-adaptation/ATTRIBUTION.md",
                        "repository": str(upstream),
                        "ref": "main",
                        "pinnedCommit": pinned,
                        "upstreamPaths": ["skills/stable-skill"],
                        "licensePaths": ["LICENSE"],
                        "exactFiles": [],
                    },
                ],
            }
            (project / "upstream-skills.json").write_text(json.dumps(manifest))

            hostile_git_environment = os.environ.copy()
            hostile_git_environment["GIT_OBJECT_DIRECTORY"] = str(root / "missing-objects")
            hostile_git_environment["GIT_COMMON_DIR"] = str(root / "missing-common")
            hostile_git_environment["GIT_EXTERNAL_DIFF"] = "false"
            current = run(
                ["python3", str(SCRIPT), "--output", ".scratch/artifacts/current"],
                project,
                check=False,
                env=hostile_git_environment,
            )
            self.assertEqual(current.returncode, 0, current.stdout + current.stderr)
            self.assertIn("CURRENT adapted-skill", current.stdout)

            unsafe_output = run(
                ["python3", str(SCRIPT), "--output", "skills/adapted-skill"],
                project,
                check=False,
            )
            self.assertEqual(unsafe_output.returncode, 2)
            self.assertIn("--output must stay inside", unsafe_output.stderr)

            (skill / "SKILL.md").write_text("version two\n")
            (skill / "example.md").write_text("example two\n")
            git(upstream, "add", ".")
            git(upstream, "commit", "-m", "change skill")
            latest = git(upstream, "rev-parse", "HEAD")

            drift = run(
                ["python3", str(SCRIPT), "--output", ".scratch/artifacts/drift"],
                project,
                check=False,
            )
            self.assertEqual(drift.returncode, 1, drift.stdout + drift.stderr)
            self.assertIn("REVIEW  adapted-skill", drift.stdout)
            self.assertIn("CURRENT stable-adaptation: tracked paths unchanged", drift.stdout)
            summary_path = next(
                (project / ".scratch" / "artifacts" / "drift").glob("*/summary.json")
            )
            summary = json.loads(summary_path.read_text())
            result = next(
                item for item in summary["results"] if item["localSkill"] == "adapted-skill"
            )
            self.assertEqual(result["paths"][0]["state"], "changed")
            self.assertEqual(result["exactFiles"][0]["state"], "different")
            self.assertEqual(result["adaptedChangedFiles"], ["skills/source-skill/SKILL.md"])
            upstream_diff = project / result["diff"]
            upstream_diff_text = upstream_diff.read_text()
            self.assertIn("version one", upstream_diff_text)
            self.assertIn("version two", upstream_diff_text)
            self.assertNotIn("example.md", upstream_diff_text)
            self.assertNotIn("example two", upstream_diff_text)
            latest_artifact = project / result["exactFiles"][0]["latestArtifact"]
            self.assertEqual(latest_artifact.read_text(), "example two\n")

            attribution.write_text(f"Reviewed at {latest}. Previously {pinned}.\n")
            stable_attribution.write_text(f"Reviewed at {latest}. Previously {pinned}.\n")
            manifest["skills"][0]["pinnedCommit"] = latest
            manifest["skills"][1]["pinnedCommit"] = latest
            (project / "upstream-skills.json").write_text(json.dumps(manifest))
            exact.write_text("example two\n")
            refreshed = run(
                ["python3", str(SCRIPT), "--output", ".scratch/artifacts/refreshed"],
                project,
                check=False,
            )
            self.assertEqual(refreshed.returncode, 0, refreshed.stdout + refreshed.stderr)
            self.assertIn("CURRENT adapted-skill", refreshed.stdout)


if __name__ == "__main__":
    unittest.main()
