#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

SKILL_NAME = "anki-language"
AGENTS = ("codex", "claude", "antigravity", "antigravity-cli", "generic")


def skill_destination(agent: str, scope: str, project: Path, custom_dest: Path | None) -> Path:
    if agent == "generic":
        if custom_dest is None:
            raise ValueError("generic installation requires --dest <skill-directory>.")
        return custom_dest.expanduser().resolve()
    if scope == "project":
        if agent in {"codex", "antigravity", "antigravity-cli"}:
            return project / ".agents" / "skills" / SKILL_NAME
        if agent == "claude":
            return project / ".claude" / "skills" / SKILL_NAME
    home = Path.home()
    if agent == "codex":
        return home / ".agents" / "skills" / SKILL_NAME
    if agent == "claude":
        return home / ".claude" / "skills" / SKILL_NAME
    if agent == "antigravity":
        return home / ".gemini" / "config" / "skills" / SKILL_NAME
    if agent == "antigravity-cli":
        return home / ".gemini" / "antigravity-cli" / "skills" / SKILL_NAME
    raise ValueError(f"Unsupported agent: {agent}")


def workflow_destination(agent: str, scope: str, project: Path) -> Path | None:
    if agent != "antigravity":
        return None
    if scope == "project":
        return project / ".agents" / "workflows" / f"{SKILL_NAME}.md"
    return Path.home() / ".gemini" / "config" / "global_workflows" / f"{SKILL_NAME}.md"


def ensure_replaceable(path: Path | None, force: bool, label: str) -> None:
    if path is not None and path.exists() and not force:
        raise FileExistsError(f"{label} already exists: {path}. Re-run with --force to replace it.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the portable anki-language skill.")
    parser.add_argument("agent", choices=AGENTS)
    parser.add_argument("--scope", choices=["project", "user"], default="project")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--dest", type=Path, help="Custom destination for generic Agent Skill installation.")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-workflow", action="store_true", help="Skip Antigravity slash-workflow installation.")
    args = parser.parse_args()

    source = Path(__file__).resolve().parents[1]
    project = args.project.resolve()
    try:
        target = skill_destination(args.agent, args.scope, project, args.dest)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2
    workflow = None if args.no_workflow else workflow_destination(args.agent, args.scope, project)

    if target.exists() and source == target.resolve():
        print(f"Skill is already installed at {target}")
        return 0

    try:
        ensure_replaceable(target, args.force, "Skill destination")
        ensure_replaceable(workflow, args.force, "Workflow destination")
    except FileExistsError as exc:
        print(f"ERROR: {exc}")
        return 1

    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc", "*.apkg", "*.report.json"),
    )

    if workflow is not None:
        template = source / "assets" / "antigravity-workflow.md"
        if workflow.exists():
            workflow.unlink()
        workflow.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(template, workflow)

    print(f"Installed {SKILL_NAME} for {args.agent} ({args.scope}) at: {target}")
    if workflow is not None:
        print(f"Installed Antigravity workflow at: {workflow}")
    if args.agent == "codex":
        print("Invoke explicitly with: $anki-language")
    elif args.agent in {"claude", "antigravity"}:
        print("Invoke explicitly with: /anki-language")
    elif args.agent == "generic":
        print("Point your AI to the installed SKILL.md or use its native Agent Skills discovery mechanism.")
    else:
        print("Use /skills to verify discovery, then ask the CLI to use anki-language.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())