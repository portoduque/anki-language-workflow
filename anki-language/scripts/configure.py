#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or update anki-language workspace configuration.")
    parser.add_argument("--target-name", required=True)
    parser.add_argument("--target-code", required=True)
    parser.add_argument("--base-name", required=True)
    parser.add_argument("--base-code", required=True)
    parser.add_argument("--output", type=Path, default=Path("anki-language.config.json"))
    args = parser.parse_args()

    data = {
        "version": "1.0",
        "target_language": {"name": args.target_name.strip(), "code": args.target_code.strip()},
        "base_language": {"name": args.base_name.strip(), "code": args.base_code.strip()},
    }

    for key in ("target_language", "base_language"):
        if not data[key]["name"] or len(data[key]["code"]) < 2:
            print(f"ERROR: {key} requires a non-empty name and a language code with at least 2 characters.")
            return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved workspace language configuration: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())