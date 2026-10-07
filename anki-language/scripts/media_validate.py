#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import wave
from pathlib import Path
from typing import Any

from mutagen import File as MutagenFile
from PIL import Image, UnidentifiedImageError


class MediaValidationError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_audio(path: Path) -> dict[str, Any]:
    path = path.resolve()
    if not path.is_file():
        raise MediaValidationError(f"Audio file does not exist: {path}")
    size = path.stat().st_size
    if size < 64:
        raise MediaValidationError(f"Audio file is too small to be functional: {path}")

    duration = None
    fmt = path.suffix.lower().lstrip(".") or "audio"

    if path.suffix.lower() == ".wav":
        try:
            with wave.open(str(path), "rb") as wav:
                frames = wav.getnframes()
                rate = wav.getframerate()
                channels = wav.getnchannels()
                width = wav.getsampwidth()
                if rate <= 0 or channels <= 0 or width <= 0 or frames <= 0:
                    raise MediaValidationError(f"Invalid WAV stream parameters: {path}")
                duration = frames / float(rate)
        except (wave.Error, EOFError) as exc:
            raise MediaValidationError(f"Invalid WAV file {path}: {exc}") from exc
    else:
        try:
            parsed = MutagenFile(str(path))
        except Exception as exc:
            raise MediaValidationError(f"Audio parser rejected {path}: {exc}") from exc
        if parsed is None or getattr(parsed, "info", None) is None:
            raise MediaValidationError(f"Unsupported or invalid audio file: {path}")
        duration = float(getattr(parsed.info, "length", 0.0) or 0.0)

    if duration is None or duration <= 0.05:
        raise MediaValidationError(f"Audio duration is not functional ({duration}): {path}")

    return {
        "status": "valid",
        "validator": "audio-decode",
        "format": fmt,
        "bytes": size,
        "duration_seconds": round(duration, 4),
        "sha256": sha256_file(path),
    }


def validate_image(path: Path) -> dict[str, Any]:
    path = path.resolve()
    if not path.is_file():
        raise MediaValidationError(f"Image file does not exist: {path}")
    size = path.stat().st_size
    if size < 64:
        raise MediaValidationError(f"Image file is too small to be functional: {path}")

    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            image.load()
            width, height = image.size
            fmt = (image.format or path.suffix.lstrip(".") or "image").lower()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise MediaValidationError(f"Invalid image file {path}: {exc}") from exc

    if width < 16 or height < 16:
        raise MediaValidationError(f"Image dimensions are too small ({width}x{height}): {path}")

    return {
        "status": "valid",
        "validator": "pillow-decode",
        "format": fmt,
        "bytes": size,
        "width": width,
        "height": height,
        "sha256": sha256_file(path),
    }


def validate_media_file(path: Path, kind: str) -> dict[str, Any]:
    if kind == "audio":
        return validate_audio(path)
    if kind == "image":
        return validate_image(path)
    raise MediaValidationError(f"Unknown media kind: {kind}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate that an audio/image file is actually decodable and functional.")
    parser.add_argument("kind", choices=["audio", "image"])
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        result = validate_media_file(args.path, args.kind)
    except MediaValidationError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
