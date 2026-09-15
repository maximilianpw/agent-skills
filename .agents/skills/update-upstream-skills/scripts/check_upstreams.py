#!/usr/bin/env python3
"""Check adapted skills against the upstream commits recorded in attribution files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GIT_AUTH_ENV_KEYS = {"GIT_ASKPASS", "GIT_SSH", "GIT_SSH_COMMAND", "GIT_TERMINAL_PROMPT"}


class CheckError(RuntimeError):
    pass


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    text: bool = True,
) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    for key in list(environment):
        if key.startswith("GIT_") and key not in GIT_AUTH_ENV_KEYS:
            environment.pop(key)
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=text,
        env=environment,
    )
    if check and result.returncode != 0:
        stderr = result.stderr.strip() if text else result.stderr.decode(errors="replace").strip()
        raise CheckError(f"{' '.join(command)} failed: {stderr}")
    return result


def git_text(repo: Path, *args: str, check: bool = True) -> str:
    result = run(["git", *args], cwd=repo, check=check)
    assert isinstance(result.stdout, str)
    return result.stdout.strip()


def git_bytes(repo: Path, *args: str) -> bytes:
    result = run(["git", *args], cwd=repo, text=False)
    assert isinstance(result.stdout, bytes)
    return result.stdout


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise CheckError(f"cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise CheckError(f"{path} must contain a JSON object")
    return value


def require_string(value: Any, field: str, owner: str) -> str:
    if not isinstance(value, str) or not value:
        raise CheckError(f"{owner}.{field} must be a non-empty string")
    return value


def require_string_list(value: Any, field: str, owner: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        raise CheckError(f"{owner}.{field} must be a non-empty string array")
    return value


def load_manifest(path: Path) -> list[dict[str, Any]]:
    manifest = read_json(path)
    if manifest.get("version") != 1:
        raise CheckError(f"{path} has unsupported version {manifest.get('version')!r}")
    skills = manifest.get("skills")
    if not isinstance(skills, list) or not skills:
        raise CheckError(f"{path}.skills must be a non-empty array")

    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for index, raw in enumerate(skills):
        owner = f"skills[{index}]"
        if not isinstance(raw, dict):
            raise CheckError(f"{owner} must be an object")
        local_skill = require_string(raw.get("localSkill"), "localSkill", owner)
        if local_skill in seen:
            raise CheckError(f"duplicate localSkill {local_skill!r}")
        seen.add(local_skill)
        exact_files = raw.get("exactFiles", [])
        if not isinstance(exact_files, list):
            raise CheckError(f"{owner}.exactFiles must be an array")
        normalized_exact: list[dict[str, str]] = []
        for exact_index, exact in enumerate(exact_files):
            exact_owner = f"{owner}.exactFiles[{exact_index}]"
            if not isinstance(exact, dict):
                raise CheckError(f"{exact_owner} must be an object")
            normalized_exact.append(
                {
                    "upstream": require_string(exact.get("upstream"), "upstream", exact_owner),
                    "local": require_string(exact.get("local"), "local", exact_owner),
                }
            )
        normalized.append(
            {
                "localSkill": local_skill,
                "attribution": require_string(raw.get("attribution"), "attribution", owner),
                "repository": require_string(raw.get("repository"), "repository", owner),
                "ref": require_string(raw.get("ref"), "ref", owner),
                "pinnedCommit": require_string(raw.get("pinnedCommit"), "pinnedCommit", owner),
                "upstreamPaths": require_string_list(raw.get("upstreamPaths"), "upstreamPaths", owner),
                "licensePaths": raw.get("licensePaths", []),
                "exactFiles": normalized_exact,
            }
        )
        if not re.fullmatch(r"[0-9a-fA-F]{40}", normalized[-1]["pinnedCommit"]):
            raise CheckError(f"{owner}.pinnedCommit must be a 40-character commit SHA")
        normalized[-1]["pinnedCommit"] = normalized[-1]["pinnedCommit"].lower()
        license_paths = normalized[-1]["licensePaths"]
        if not isinstance(license_paths, list) or not all(
            isinstance(item, str) and item for item in license_paths
        ):
            raise CheckError(f"{owner}.licensePaths must be a string array")
    return normalized


def attribution_contains_pin(repo_root: Path, attribution_path: str, pin: str) -> bool:
    path = repo_root / attribution_path
    try:
        return pin.lower() in path.read_text().lower()
    except OSError as error:
        raise CheckError(f"cannot read attribution file {path}: {error}") from error


def clone_repository(repository: str, ref: str, destination: Path) -> str:
    run(
        [
            "git",
            "clone",
            "--filter=blob:none",
            "--no-checkout",
            "--depth",
            "1",
            "--branch",
            ref,
            repository,
            str(destination),
        ]
    )
    return git_text(destination, "rev-parse", "HEAD")


def ensure_commit(repo: Path, repository: str, commit: str) -> None:
    present = run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=repo, check=False)
    if present.returncode == 0:
        return
    result = run(["git", "fetch", "--depth", "1", "origin", commit], cwd=repo, check=False)
    if result.returncode != 0:
        raise CheckError(f"cannot fetch pinned commit {commit} from {repository}")


def object_id(repo: Path, revision: str, path: str) -> str | None:
    result = run(["git", "rev-parse", f"{revision}:{path}"], cwd=repo, check=False)
    if result.returncode != 0:
        return None
    assert isinstance(result.stdout, str)
    return result.stdout.strip()


def changed_files(repo: Path, pinned: str, latest: str, paths: list[str]) -> list[str]:
    result = run(
        ["git", "diff", "--no-ext-diff", "--name-only", pinned, latest, "--", *paths],
        cwd=repo,
        check=False,
    )
    if result.returncode != 0:
        assert isinstance(result.stderr, str)
        raise CheckError(f"git diff --name-only failed: {result.stderr.strip()}")
    assert isinstance(result.stdout, str)
    return [line for line in result.stdout.splitlines() if line]


def upstream_diff(
    repo: Path,
    pinned: str,
    latest: str,
    include_paths: list[str],
    excluded_files: set[str],
) -> str:
    command = [
        "git",
        "diff",
        "--no-ext-diff",
        "--find-renames",
        pinned,
        latest,
        "--",
        *include_paths,
        *(f":(exclude){path}" for path in sorted(excluded_files)),
    ]
    result = run(command, cwd=repo, check=False)
    if result.returncode != 0:
        assert isinstance(result.stderr, str)
        raise CheckError(f"git diff failed: {result.stderr.strip()}")
    assert isinstance(result.stdout, str)
    return result.stdout


def safe_artifact_name(value: str) -> str:
    digest = hashlib.sha256(value.encode()).hexdigest()[:10]
    readable = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-")[-80:]
    return f"{readable}-{digest}" if readable else digest


def write_text_diff(local_path: Path, upstream_bytes: bytes, output_path: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="upstream-exact-diff-") as temp:
        latest_path = Path(temp) / "latest"
        latest_path.write_bytes(upstream_bytes)
        result = run(
            [
                "git",
                "diff",
                "--no-ext-diff",
                "--no-index",
                "--",
                str(local_path),
                str(latest_path),
            ],
            check=False,
        )
        if result.returncode not in (0, 1):
            assert isinstance(result.stderr, str)
            raise CheckError(f"git diff --no-index failed: {result.stderr.strip()}")
        assert isinstance(result.stdout, str)
        output_path.write_text(result.stdout)


def check_skill(
    repo_root: Path,
    clone: Path,
    latest_commit: str,
    entry: dict[str, Any],
    run_directory: Path,
) -> dict[str, Any]:
    local_skill = entry["localSkill"]
    pinned_commit = entry["pinnedCommit"]
    if not attribution_contains_pin(repo_root, entry["attribution"], pinned_commit):
        raise CheckError(
            f"{entry['attribution']} does not contain manifest pin {pinned_commit}"
        )
    ensure_commit(clone, entry["repository"], pinned_commit)

    skill_output = run_directory / local_skill
    skill_output.mkdir(parents=True, exist_ok=True)

    path_results: list[dict[str, Any]] = []
    for upstream_path in entry["upstreamPaths"]:
        pinned_object = object_id(clone, pinned_commit, upstream_path)
        latest_object = object_id(clone, latest_commit, upstream_path)
        state = "current"
        if pinned_object is None:
            state = "missing-at-pin"
        elif latest_object is None:
            state = "missing-upstream"
        elif pinned_object != latest_object:
            state = "changed"
        path_results.append(
            {
                "path": upstream_path,
                "state": state,
                "pinnedObject": pinned_object,
                "latestObject": latest_object,
            }
        )

    all_changed_files = changed_files(
        clone, pinned_commit, latest_commit, entry["upstreamPaths"]
    )
    exact_upstream_paths = {exact["upstream"] for exact in entry["exactFiles"]}
    adapted_changed_files = [
        path for path in all_changed_files if path not in exact_upstream_paths
    ]

    diff_path: str | None = None
    if adapted_changed_files:
        diff = upstream_diff(
            clone,
            pinned_commit,
            latest_commit,
            entry["upstreamPaths"],
            exact_upstream_paths,
        )
        if not diff.strip():
            raise CheckError(
                f"adapted upstream files changed for {local_skill}, but git produced an empty diff"
            )
        artifact = skill_output / "upstream.diff"
        artifact.write_text(diff + ("\n" if not diff.endswith("\n") else ""))
        diff_path = str(artifact.relative_to(repo_root))

    exact_results: list[dict[str, Any]] = []
    for exact in entry["exactFiles"]:
        local_path = repo_root / exact["local"]
        latest_object = object_id(clone, latest_commit, exact["upstream"])
        state = "match"
        latest_artifact: str | None = None
        exact_diff: str | None = None
        if latest_object is None:
            state = "missing-upstream"
        else:
            latest_bytes = git_bytes(clone, "show", f"{latest_commit}:{exact['upstream']}")
            latest_file = skill_output / f"{safe_artifact_name(exact['local'])}.latest"
            latest_file.write_bytes(latest_bytes)
            latest_artifact = str(latest_file.relative_to(repo_root))
            if not local_path.exists():
                state = "missing-local"
            elif local_path.read_bytes() != latest_bytes:
                state = "different"
                diff_file = skill_output / f"{safe_artifact_name(exact['local'])}.diff"
                write_text_diff(local_path, latest_bytes, diff_file)
                exact_diff = str(diff_file.relative_to(repo_root))
        exact_results.append(
            {
                "upstream": exact["upstream"],
                "local": exact["local"],
                "state": state,
                "latestArtifact": latest_artifact,
                "diff": exact_diff,
            }
        )

    license_results: list[dict[str, Any]] = []
    for license_path in entry["licensePaths"]:
        pinned_object = object_id(clone, pinned_commit, license_path)
        latest_object = object_id(clone, latest_commit, license_path)
        state = "current"
        latest_artifact: str | None = None
        if pinned_object is None and latest_object is None:
            state = "absent"
        elif pinned_object is None:
            state = "added"
        elif latest_object is None:
            state = "removed"
        elif pinned_object != latest_object:
            state = "changed"
        if latest_object is not None:
            license_bytes = git_bytes(clone, "show", f"{latest_commit}:{license_path}")
            license_file = skill_output / f"license-{safe_artifact_name(license_path)}.latest"
            license_file.write_bytes(license_bytes)
            latest_artifact = str(license_file.relative_to(repo_root))
        license_results.append(
            {
                "path": license_path,
                "state": state,
                "pinnedObject": pinned_object,
                "latestObject": latest_object,
                "latestArtifact": latest_artifact,
            }
        )

    needs_review = (
        any(result["state"] != "current" for result in path_results)
        or any(result["state"] != "match" for result in exact_results)
        or any(result["state"] not in ("current", "absent") for result in license_results)
    )
    return {
        "localSkill": local_skill,
        "repository": entry["repository"],
        "ref": entry["ref"],
        "attribution": entry["attribution"],
        "pinnedCommit": pinned_commit,
        "latestCommit": latest_commit,
        "status": "review" if needs_review else "current",
        "paths": path_results,
        "changedFiles": all_changed_files,
        "adaptedChangedFiles": adapted_changed_files,
        "exactFiles": exact_results,
        "licenses": license_results,
        "diff": diff_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check upstream-derived skills without overwriting local adaptations."
    )
    parser.add_argument("--manifest", default="upstream-skills.json")
    parser.add_argument("--output", default=".scratch/upstream-skills")
    parser.add_argument("--skill", action="append", dest="skills")
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd().resolve()
    manifest_path = (repo_root / args.manifest).resolve()
    output_root = (repo_root / args.output).resolve()
    try:
        scratch_root = (repo_root / ".scratch").resolve()
        if output_root != scratch_root and not output_root.is_relative_to(scratch_root):
            raise CheckError("--output must stay inside this repository's .scratch directory")
        entries = load_manifest(manifest_path)
        if args.skills:
            requested = set(args.skills)
            entries = [entry for entry in entries if entry["localSkill"] in requested]
            missing = sorted(requested - {entry["localSkill"] for entry in entries})
            if missing:
                raise CheckError(f"unknown skills requested: {', '.join(missing)}")
        if not entries:
            raise CheckError("no upstream skills selected")
        if shutil.which("git") is None:
            raise CheckError("git is required")

        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + f"-{os.getpid()}"
        run_directory = output_root / run_id
        run_directory.mkdir(parents=True, exist_ok=False)

        groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for entry in entries:
            groups.setdefault((entry["repository"], entry["ref"]), []).append(entry)

        results: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []
        with tempfile.TemporaryDirectory(prefix="upstream-skills-") as temp:
            temp_root = Path(temp)
            for group_index, ((repository, ref), grouped_entries) in enumerate(groups.items()):
                clone = temp_root / f"repo-{group_index}"
                try:
                    latest_commit = clone_repository(repository, ref, clone)
                    for entry in grouped_entries:
                        try:
                            results.append(
                                check_skill(repo_root, clone, latest_commit, entry, run_directory)
                            )
                        except CheckError as error:
                            errors.append({"localSkill": entry["localSkill"], "error": str(error)})
                except CheckError as error:
                    for entry in grouped_entries:
                        errors.append({"localSkill": entry["localSkill"], "error": str(error)})

        summary = {
            "version": 1,
            "checkedAt": datetime.now(timezone.utc).isoformat(),
            "manifest": str(manifest_path.relative_to(repo_root)),
            "runDirectory": str(run_directory.relative_to(repo_root)),
            "results": results,
            "errors": errors,
        }
        summary_path = run_directory / "summary.json"
        summary_path.write_text(json.dumps(summary, indent=2) + "\n")

        if args.json_output:
            print(json.dumps(summary, indent=2))
        else:
            for result in results:
                if result["status"] == "review":
                    print(
                        f"REVIEW  {result['localSkill']}: "
                        f"{result['pinnedCommit'][:12]} -> {result['latestCommit'][:12]}"
                    )
                elif result["pinnedCommit"] != result["latestCommit"]:
                    print(
                        f"CURRENT {result['localSkill']}: tracked paths unchanged at "
                        f"{result['pinnedCommit'][:12]}; upstream HEAD is "
                        f"{result['latestCommit'][:12]}"
                    )
                else:
                    print(f"CURRENT {result['localSkill']}: {result['pinnedCommit'][:12]}")
                if result["diff"]:
                    print(f"        adapted upstream diff: {result['diff']}")
                for exact in result["exactFiles"]:
                    if exact["state"] != "match":
                        print(f"        exact file {exact['state']}: {exact['local']}")
                        if exact["diff"]:
                            print(f"        exact diff: {exact['diff']}")
                for license_result in result["licenses"]:
                    if license_result["state"] not in ("current", "absent"):
                        print(
                            f"        license {license_result['state']}: "
                            f"{license_result['path']}"
                        )
            for error in errors:
                print(f"ERROR   {error['localSkill']}: {error['error']}", file=sys.stderr)
            print(f"Artifacts: {summary['runDirectory']}")

        if errors:
            return 2
        if any(result["status"] == "review" for result in results):
            return 1
        return 0
    except CheckError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
