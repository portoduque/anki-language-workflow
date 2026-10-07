#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

SKILL_NAME = "anki-language"


def destination(agent: str, scope: str, project: Path) -> Path:
    if scope == "project":
        if agent in {"codex", "antigravity"}:
            return project / ".agents" / "skills" / SKILL_NAME
        if agent == "claude":
            return project / ".claude" / "skills" / SKILL_NAME

    home = Path.home()
    if agent == "codex":
        codex_home = Path(os.environ.get("CODEX_HOME", str(home / ".codex"))).expanduser()
        return codex_home / "skills" / SKILL_NAME
    if agent == "claude":
        return home / ".claude" / "skills" / SKILL_NAME
    if agent == "antigravity":
        return home / ".gemini" / "config" / "skills" / SKILL_NAME

    raise ValueError(f"Unsupported agent: {agent}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the anki-language skill.")
    parser.add_argument("agent", choices=["codex", "claude", "antigravity"])
    parser.add_argument("--scope", choices=["project", "user"], default="project")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    source = Path(__file__).resolve().parents[1]
    target = destination(args.agent, args.scope, args.project.resolve())

    if source == target.resolve() if target.exists() else False:
        print(f"Skill is already installed at {target}")
        return 0

    if target.exists():
        if not args.force:
            print(f"ERROR: destination already exists: {target}")
            print("Re-run with --force to replace it.")
            return 1
        shutil.rmtree(target)

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns(
            "__pycache__",
            ".pytest_cache",
            "*.pyc",
            "*.apkg",
            "*.report.json",
        ),
    )

    print(f"Installed {SKILL_NAME} for {args.agent} ({args.scope}) at:")
    print(target)
    print()
    print("Install runtime dependency when needed:")
    print(f"python -m pip install -r {target / 'requirements.txt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
