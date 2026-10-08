#!/usr/bin/env python3
"""Generate short audio samples so the learner can choose a Piper voice by ear."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from media_enrich import synthesize_piper
from media_validate import validate_media_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare language-matched Piper voices.")
    parser.add_argument("--text", default="Bonjour ! Vous pouvez me suivre.")
    parser.add_argument("--language", default="fr")
    parser.add_argument("--voices", nargs="+", default=[
        "fr_FR-siwis-medium", "fr_FR-tom-medium", "fr_FR-upmc-medium",
    ])
    parser.add_argument("--length-scale", type=float, default=0.93)
    parser.add_argument("--out", type=Path, default=Path("voice-previews"))
    args = parser.parse_args()
    if not 0.75 <= args.length_scale <= 1.25:
        parser.error("--length-scale must be in [0.75, 1.25].")
    args.out.mkdir(parents=True, exist_ok=True)
    results = []
    for name in args.voices:
        output = args.out / f"{name}-{args.length_scale:.2f}.wav"
        try:
            synthesize_piper(args.text, args.language, output, name,
                             args.out / ".piper-voices",
                             length_scale=args.length_scale)
            info = validate_media_file(output, "audio")
            results.append({"voice": name, "file": str(output.resolve()),
                            "seconds": info["duration_seconds"], "status": "ok"})
        except Exception as exc:
            results.append({"voice": name, "status": "error", "error": str(exc)})
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if any(item["status"] == "ok" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
