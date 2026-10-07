#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "anki-language"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="One-command installer for Codex, Claude Code, Antigravity, or any Agent-Skills-compatible AI."
    )
    parser.add_argument("agent", choices=["codex", "claude", "antigravity", "antigravity-cli", "generic"])
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--dest", type=Path, help="Required for generic installation.")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--skip-deps", action="store_true", help="Do not install Python runtime dependencies.")
    args = parser.parse_args()

    if args.agent == "generic" and args.dest is None:
        parser.error("generic installation requires --dest <skill-directory>")

    try:
        if not args.skip_deps:
            run([sys.executable, "-m", "pip", "install", "-r", str(SKILL / "requirements.txt")])

        cmd = [
            sys.executable,
            str(SKILL / "scripts" / "install_skill.py"),
            args.agent,
            "--scope",
            args.scope,
            "--project",
            str(args.project.resolve()),
        ]
        if args.dest is not None:
            cmd.extend(["--dest", str(args.dest.expanduser())])
        if args.force:
            cmd.append("--force")
        run(cmd)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: installation command failed with exit code {exc.returncode}")
        return exc.returncode or 1

    print()
    print("Installation complete. On first use in each workspace, the AI must ask for target language and base language.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())