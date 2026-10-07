#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from deliver_live import deliver_live
from validate_plan import load_plan


def default_apkg(plan: dict, plan_path: Path) -> Path:
    raw = str(plan.get("deck_name") or "language").strip()
    safe = "".join(ch if ch.isalnum() or ch in "._-" else "-" for ch in raw).strip("-") or "language"
    return plan_path.resolve().parent / f"{safe}.apkg"


def build_apkg(plan_path: Path, output: Path) -> dict:
    script = Path(__file__).resolve().parent / "build.py"
    completed = subprocess.run(
        [sys.executable, str(script), str(plan_path), "--output", str(output)],
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stdout + completed.stderr)
    return json.loads(completed.stdout)


def deliver(plan_path: Path, mode: str | None = None, output: Path | None = None, endpoint: str | None = None, api_key: str | None = None) -> dict:
    plan = load_plan(plan_path)
    selected = mode or (plan.get("delivery") or {}).get("mode") or "apkg"
    if selected not in {"apkg", "live", "both"}:
        raise ValueError(f"Unsupported delivery mode: {selected}")

    report: dict = {"status": "ok", "mode": selected}
    if selected in {"apkg", "both"}:
        apkg = output or default_apkg(plan, plan_path)
        report["apkg"] = build_apkg(plan_path, apkg)
    if selected in {"live", "both"}:
        report["live"] = deliver_live(
            plan_path,
            endpoint or os.getenv("ANKICONNECT_URL", "http://127.0.0.1:8765"),
            api_key or os.getenv("ANKICONNECT_API_KEY") or None,
        )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Deliver a resolved plan as APKG, live Anki notes, or both.")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--mode", choices=["apkg", "live", "both"])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--endpoint")
    args = parser.parse_args()
    try:
        report = deliver(args.plan, args.mode, args.output, args.endpoint)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
