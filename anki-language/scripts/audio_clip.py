"""Conservative source-audio clipping for language cards.

Uses exact word alignment from optional faster-whisper, or source-verified
timestamps. Fail closed: never guess which repeated phrase to attach.
"""
from __future__ import annotations

import math
import re
import array
import wave
import shutil
import subprocess
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any

from media_validate import MediaValidationError, validate_media_file

LEAD_SECONDS = 0.22
TAIL_SECONDS = 0.35
MAX_CLIP_SECONDS = 30.0


def tokenize(text: str) -> list[str]:
    folded = unicodedata.normalize("NFKC", text).casefold().replace("’", "'")
    # Keep contractions intact: "I can" must not match "I can't".
    return re.findall(r"[^\W_]+(?:'[^\W_]+)*", folded, flags=re.UNICODE)


@lru_cache(maxsize=1)
def _whisper_model() -> Any:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError(
            "Automatic source-audio alignment needs optional faster-whisper. "
            "Install: python -m pip install -r requirements-alignment.txt; "
            "alternatively provide verified start_seconds/end_seconds."
        ) from exc
    return WhisperModel("small", device="cpu", compute_type="int8")


def transcribe_words(source: Path, language: str) -> list[tuple[str, float, float]]:
    """Return original-audio word times. No forced text or guessed matches."""
    model = _whisper_model()
    segments, _ = model.transcribe(
        str(source),
        language=language.split("-", 1)[0].lower(),
        word_timestamps=True,
        beam_size=5,
    )
    result: list[tuple[str, float, float]] = []
    for segment in segments:
        for word in segment.words or []:
            if word.start is not None and word.end is not None:
                result.append((str(word.word), float(word.start), float(word.end)))
    if not result:
        raise ValueError(f"No word-level transcript found in '{source.name}'.")
    return result


def locate_exact_phrase(
    target: str,
    timed_words: list[tuple[str, float, float]],
) -> tuple[float, float]:
    """Match a contiguous phrase exactly, once, without silently choosing repeats."""
    wanted = tokenize(target)
    if len(wanted) < 2:
        raise ValueError(
            "Auto-alignment of a single word is unreliable. Provide verified "
            "start_seconds/end_seconds or use focused audio."
        )
    flat: list[tuple[str, float, float]] = []
    join_next = False
    for text, start, end in timed_words:
        if not math.isfinite(start) or not math.isfinite(end) or not 0 <= start < end:
            raise ValueError("Invalid word timestamps in transcription.")
        raw = str(text).strip().replace("’", "'")
        if not raw:
            continue
        # ASR may time "J'" + "habite" or "can" + "'t" separately.
        # Reconstruct the contraction before matching lexical targets.
        if (join_next or raw.startswith("'")) and flat:
            previous, first, _ = flat.pop()
            raw = previous + ("'" if join_next else "") + raw
            start = first
        elif raw.startswith("'"):
            raise ValueError("Unanchored apostrophe fragment in word timestamps.")
        flat.extend((word, start, end) for word in tokenize(raw))
        join_next = raw.endswith("'")

    matches = [
        i for i in range(len(flat) - len(wanted) + 1)
        if [word for word, _, _ in flat[i:i + len(wanted)]] == wanted
    ]
    if not matches:
        raise ValueError(
            "Target words were not found exactly in the source recording. "
            "Check the transcription, use verified timestamps, or use matching TTS."
        )
    if len(matches) != 1:
        raise ValueError(
            "Target phrase occurs multiple times in the source recording. "
            "Provide verified start_seconds/end_seconds to select the right occurrence."
        )
    index = matches[0]
    return flat[index][1], flat[index + len(wanted) - 1][2]



def inspect_clip_edges(path: Path) -> list[str]:
    """Flag very loud non-quiet PCM edges; does not certify spoken phonemes."""
    try:
        with wave.open(str(path), "rb") as audio:
            if audio.getnchannels() != 1 or audio.getsampwidth() != 2:
                raise ValueError("Audio clip quality check requires 16-bit mono WAV.")
            frames = audio.getnframes()
            rate = audio.getframerate()
            samples = array.array("h", audio.readframes(frames))
    except (wave.Error, OSError, EOFError) as exc:
        raise ValueError(f"Cannot inspect clip boundary audio: {exc}") from exc
    if not frames or not samples or rate <= 0:
        raise ValueError("Clip boundary signal is empty.")
    edge_len = min(int(rate * 0.04), len(samples) // 5)
    if edge_len < 1:
        return ["Clip is too short for reliable audio-edge inspection."]
    def rms(seq: array.array) -> float:
        return (sum(v * v for v in seq) / len(seq)) ** 0.5 / 32768.0
    beginning = rms(samples[:edge_len])
    end = rms(samples[-edge_len:])
    interior = rms(samples[edge_len:-edge_len]) if len(samples) > edge_len * 2 else 0.0
    # Conservative: strong audio at cut edges can indicate a truncated sound.
    # Do not flag low-level continuous background noise as missing speech.
    return [
        label for label, value in (("start", beginning), ("end", end))
        if value > 0.075 and value >= interior * 0.60
    ]

def clip_audio(
    source: Path,
    destination: Path,
    *,
    target_text: str,
    language: str,
    start_seconds: float | None,
    end_seconds: float | None,
    word_cache: dict[tuple[Path, str], list[tuple[str, float, float]]],
    strict_boundaries: bool = False,
) -> dict[str, Any]:
    """Cut a focused WAV, return verified original times and match method."""
    original = validate_media_file(source, "audio")
    length = float(original["duration_seconds"])
    if (start_seconds is None) != (end_seconds is None):
        raise ValueError("Audio clip requires both start_seconds and end_seconds.")

    if start_seconds is None:
        key = (source.resolve(), language.split("-", 1)[0].lower())
        if key not in word_cache:
            word_cache[key] = transcribe_words(source, language)
        first, last = locate_exact_phrase(target_text, word_cache[key])
        method = "asr-exact"
    else:
        first, last = float(start_seconds), float(end_seconds)
        method = "verified-timestamps"

    if not all(math.isfinite(v) for v in (first, last)):
        raise ValueError("Clip timestamps must be finite.")
    if not (0 <= first < last <= length + 0.02):
        raise ValueError(
            f"Clip bounds {first:.3f}–{last:.3f}s are outside "
            f"'{source.name}' ({length:.3f}s)."
        )
    start = max(0.0, first - LEAD_SECONDS)
    end = min(length, last + TAIL_SECONDS)
    if end - start > MAX_CLIP_SECONDS:
        raise ValueError(
            f"Clip is longer than {MAX_CLIP_SECONDS:g}s; choose a shorter "
            "utterance or provide more precise boundaries."
        )
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "Audio clipping requires FFmpeg on PATH. Install FFmpeg "
            "or provide an already-trimmed audio file."
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(source), "-ss", f"{start:.3f}", "-t", f"{end - start:.3f}",
        "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "24000",
        "-c:a", "pcm_s16le", str(destination),
    ]
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=90, check=False)
        if completed.returncode:
            raise RuntimeError(completed.stderr.strip() or "FFmpeg exited unsuccessfully.")
        output = validate_media_file(destination, "audio")
        if abs(float(output["duration_seconds"]) - (end - start)) > 0.3:
            raise ValueError("FFmpeg produced a clip with an unexpected duration.")
        if strict_boundaries:
            risky = inspect_clip_edges(destination)
            if risky:
                raise ValueError("Potentially abrupt/truncated clip at " + ", ".join(risky) + " edge(s). Verify source timestamps and allow more speech padding before delivery.")
    except (RuntimeError, ValueError, OSError, subprocess.TimeoutExpired, MediaValidationError):
        destination.unlink(missing_ok=True)
        raise

    return {
        "source": str(source),
        "start_seconds": round(start, 3),
        "end_seconds": round(end, 3),
        "alignment": method,
        "validation": output,
    }
