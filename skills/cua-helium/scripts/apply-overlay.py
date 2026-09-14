#!/usr/bin/env python3
"""Apply the local Pi and Helium overlay to a Skills CLI Cua installation."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

START = "<!-- cua-helium-overlay:start -->"
END = "<!-- cua-helium-overlay:end -->"
POINTER = f"""{START}
## Local integration — read first

Read [LOCAL.md](LOCAL.md) before the upstream guidance below. It defines this setup's `computer` MCP transport, cross-platform Helium identity, profile checks, and permission boundaries. Installed tool schemas remain authoritative.
{END}
"""


def find_install(explicit: Path | None) -> Path:
    candidates = (
        [explicit]
        if explicit is not None
        else [
            Path.home() / ".agents/skills/cua-driver",
            Path.home() / ".pi/agent/skills/cua-driver",
        ]
    )
    for candidate in candidates:
        if candidate is not None and (candidate / "SKILL.md").is_file():
            return candidate
    checked = ", ".join(str(path) for path in candidates if path is not None)
    raise FileNotFoundError(f"Cua Driver skill not found; checked: {checked}")


def patched_skill(text: str) -> str:
    if START in text or END in text:
        if text.count(START) != 1 or text.count(END) != 1:
            raise ValueError("Cua SKILL.md contains an incomplete or duplicate local overlay")
        before, remainder = text.split(START, 1)
        _, after = remainder.split(END, 1)
        return before.rstrip() + "\n\n" + POINTER + "\n" + after.lstrip("\n")

    heading = "# cua-driver\n\n"
    if heading not in text:
        raise ValueError("Cua SKILL.md is missing its expected '# cua-driver' heading")
    return text.replace(heading, heading + POINTER + "\n", 1)


def unpatched_skill(text: str) -> str:
    if START not in text and END not in text:
        return text
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError("Cua SKILL.md contains an incomplete or duplicate local overlay")
    before, remainder = text.split(START, 1)
    _, after = remainder.split(END, 1)
    return before.rstrip() + "\n\n" + after.lstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, help="Installed cua-driver skill directory")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Verify without writing")
    mode.add_argument("--remove", action="store_true", help="Remove the overlay before an upstream update")
    args = parser.parse_args()

    try:
        target = find_install(args.target)
        skill_path = target / "SKILL.md"
        local_path = target / "LOCAL.md"
        source_path = Path(__file__).resolve().parent.parent / "assets/LOCAL.md"
        source = source_path.read_text()
        current_skill = skill_path.read_text()

        if args.remove:
            skill_path.write_text(unpatched_skill(current_skill))
            if local_path.is_file():
                local_path.unlink()
            print(f"Removed Cua Helium overlay: {target}")
            return 0

        expected_skill = patched_skill(current_skill)
        if args.check:
            if not local_path.is_file() or local_path.read_text() != source:
                print(f"Local overlay differs or is missing: {local_path}", file=sys.stderr)
                return 1
            if current_skill != expected_skill:
                print(f"Local overlay pointer differs or is missing: {skill_path}", file=sys.stderr)
                return 1
            print(f"Cua Helium overlay is current: {target}")
            return 0

        local_path.write_text(source)
        skill_path.write_text(expected_skill)
        print(f"Applied Cua Helium overlay: {target}")
        return 0
    except (FileNotFoundError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
