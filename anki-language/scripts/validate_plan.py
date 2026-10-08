#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import collections
import re
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator

from card_contract import AUDIO_REQUIRED_PRONUNCIATION_MODES, SUPPORTED_MODES_BY_SKILL, normalize_mode, writing_parts
from media_validate import MediaValidationError, validate_media_file

CONFIG_FILENAME = "anki-language.config.json"


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{label} root must be a JSON object.")
    return data


def load_plan(path: Path) -> dict[str, Any]:
    return load_json_object(path, "Plan")


def schema_errors(data: dict[str, Any], schema_name: str, label: str) -> list[str]:
    schema_path = Path(__file__).resolve().parents[1] / "schemas" / schema_name
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        path = "$"
        for part in error.absolute_path:
            path += f"[{part}]" if isinstance(part, int) else f".{part}"
        errors.append(f"{label} {path}: {error.message}")
    return errors


def discover_config(plan_path: Path, explicit: Path | None = None) -> Path | None:
    if explicit is not None:
        return explicit.resolve()
    candidates = [Path.cwd() / CONFIG_FILENAME, plan_path.resolve().parent / CONFIG_FILENAME]
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.is_file():
            return resolved
    return None


def validate_language_config(plan: dict[str, Any], config_path: Path) -> list[str]:
    try:
        config = load_json_object(config_path, "Configuration")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"Invalid workspace configuration: {exc}"]
    errors = schema_errors(config, "config.schema.json", "Config")
    if errors:
        return errors
    for key in ("target_language", "base_language"):
        plan_lang = plan[key]
        config_lang = config[key]
        if str(plan_lang["code"]).casefold() != str(config_lang["code"]).casefold() or str(plan_lang["name"]).casefold() != str(config_lang["name"]).casefold():
            errors.append(
                f"Plan {key} ({plan_lang['name']} / {plan_lang['code']}) does not match "
                f"workspace configuration ({config_lang['name']} / {config_lang['code']})."
            )
    return errors


def normalized_utterance(value: str) -> str:
    """Compare target/transcript tokens, retaining meaningful contractions."""
    folded = unicodedata.normalize("NFKC", value).casefold().replace("’", "'")
    # "can" and "can't" must never be matched as the same spoken word.
    return " ".join(re.findall(r"[^\W_]+(?:'[^\W_]+)*", folded, flags=re.UNICODE))


def retrieval_signature(card: dict[str, Any]) -> tuple[str, ...]:
    """Catch identical review tasks regardless of ids, tags, notes, or source.

    Intentionally do not compare across skills: recognition, listening, and
    production can be independent retrieval operations. This is not an AI
    similarity score and must not discard legitimate semantic variations.
    """
    skill = str(card["skill"])
    mode = normalize_mode(card)
    def norm(key: str) -> str:
        return " ".join(unicodedata.normalize("NFKC", str(card.get(key, ""))).casefold().split())

    signature = [skill, mode, norm("target_text"), norm("prompt")]
    if skill == "writing":
        signature.append(norm("writing_answer"))
    elif skill == "production":
        signature.extend([norm("hint"), norm("image")])
    elif skill in {"listening", "pronunciation"}:
        clip = card.get("audio_clip")
        signature.extend([
            norm("audio"),
            json.dumps(clip, sort_keys=True, ensure_ascii=False) if clip else "",
            json.dumps(card.get("audio_request"), sort_keys=True, ensure_ascii=False)
            if card.get("audio_request") else "",
        ])
    return tuple(signature)



AUDIO_SOURCE_SUFFIXES = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".opus", ".aac"}


def validate_source_inventory(plan: dict[str, Any], plan_path: Path) -> list[str]:
    """Make every supplied source audio auditable without forcing cards per file."""
    inventory = plan.get("source_inventory")
    if inventory is None:
        if any(card.get("source_item_id") for card in plan["cards"]):
            return ["Cards reference source_item_id but no source_inventory is declared."]
        return []

    errors: list[str] = []
    root = Path(str(inventory["audio_root"]))
    source_root = root if root.is_absolute() else plan_path.resolve().parent / root
    source_root = source_root.resolve()
    try:
        if source_root.is_dir():
            actual = {
                file.relative_to(source_root).as_posix()
                for file in source_root.rglob("*")
                if file.is_file() and file.suffix.lower() in AUDIO_SOURCE_SUFFIXES
            }
        elif source_root.is_file() and source_root.suffix.lower() == ".zip":
            with zipfile.ZipFile(source_root) as archive:
                actual = {
                    name for name in archive.namelist()
                    if not name.endswith("/") and
                    PurePosixPath(name).suffix.lower() in AUDIO_SOURCE_SUFFIXES
                }
        else:
            return [f"source_inventory.audio_root must be a directory or ZIP: {source_root}"]
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"Cannot read source_inventory.audio_root: {exc}"]

    if not actual:
        errors.append("source_inventory.audio_root contains no recognized audio files.")
    declared: set[str] = set()
    item_ids: set[str] = set()
    card_by_id = {str(card["id"]): card for card in plan["cards"]}
    linked: set[str] = set()
    for index, item in enumerate(inventory["items"]):
        path = str(item["file"]).replace("\\", "/")
        prefix = f"source_inventory.items[{index}]"
        normalized = PurePosixPath(path)
        if normalized.is_absolute() or ".." in normalized.parts or path != normalized.as_posix():
            errors.append(f"{prefix}.file must be a normalized relative path in audio_root.")
            continue
        if path in declared:
            errors.append(f"{prefix}.file is listed more than once: {path}")
        declared.add(path)
        item_id = str(item["id"])
        if item_id in item_ids:
            errors.append(f"{prefix}.id is duplicated: {item_id}")
        item_ids.add(item_id)
        status = item["status"]
        ids = item.get("card_ids") or []
        if status == "skipped":
            if ids or not str(item.get("reason", "")).strip():
                errors.append(f"{prefix}: skipped audio needs a reason and no card_ids.")
        elif status == "selected" and not ids:
            errors.append(f"{prefix}: selected audio needs at least one linked card_id.")
        for cid in ids:
            if cid in linked:
                errors.append(f"{prefix}: card_id {cid} appears under multiple source audios.")
            linked.add(cid)
            card = card_by_id.get(cid)
            if card is None:
                errors.append(f"{prefix}: card_id {cid} does not exist.")
            elif card.get("source_item_id") != item_id:
                errors.append(f"{prefix}: card {cid} must set source_item_id={item_id!r}.")

    for card in plan["cards"]:
        source_id = card.get("source_item_id")
        if not source_id or source_id not in item_ids:
            errors.append(f"Card {card['id']} must reference a declared source_item_id.")
        elif str(card["id"]) not in linked:
            errors.append(f"Card {card['id']} is absent from the inventory card_ids.")

    missing = sorted(actual - declared)
    extra = sorted(declared - actual)
    if missing:
        errors.append("Source audio files omitted from inventory: " + ", ".join(missing))
    if extra:
        errors.append("Inventory references missing source audio: " + ", ".join(extra))
    return errors


def validate_source_units(plan: dict[str, Any], plan_path: Path, check_media: bool = True) -> list[str]:
    """Require all author-supplied learning units to be visibly represented."""
    if plan["version"] not in {"2.2", "2.3", "2.4", "2.5", "2.6"}:
        return []
    units = plan.get("source_units")
    if not units:
        return ["v2.2 requires nonempty source_units: include every supplied phrase/word."]
    errors: list[str] = []
    cards = {str(card["id"]): card for card in plan["cards"]}
    ids: set[str] = set()
    card_links: set[str] = set()
    for n, unit in enumerate(units):
        uid = unit["id"]
        if uid in ids:
            errors.append(f"source_units[{n}].id is duplicated: {uid}")
        ids.add(uid)
        for card_id in unit["card_ids"]:
            if card_id not in cards:
                errors.append(f"source_units[{n}]: card_id {card_id!r} does not exist.")
            card_links.add(card_id)
    if (plan["version"] == "2.3" or (plan["version"] in {"2.4", "2.5", "2.6"} and plan.get("audio_settings", {}).get("include_source_audio", False))) and check_media:
        for n, unit in enumerate(units):
            raw = unit.get("audio")
            if not raw:
                errors.append(f"source_units[{n}].audio must be resolved for v2.3; run media enrichment.")
                continue
            path = Path(str(raw))
            resolved = path if path.is_absolute() else plan_path.resolve().parent / path
            try:
                current = validate_media_file(resolved.resolve(), "audio")
            except (MediaValidationError, OSError) as exc:
                errors.append(f"Invalid source_units[{n}].audio: {exc}")
                continue
            recorded = (unit.get("media_validation") or {}).get("audio") or {}
            if recorded.get("sha256") and recorded["sha256"] != current["sha256"]:
                errors.append(f"source_units[{n}].audio changed after validation.")
    for card_id in cards:
        if card_id not in card_links:
            errors.append(f"Card {card_id!r} is not linked to any supplied phrase/word.")
    if plan.get("source_text_file"):
        path = Path(str(plan["source_text_file"]))
        file_path = path if path.is_absolute() else plan_path.resolve().parent / path
        try:
            if file_path.suffix.lower() == ".txt":
                originals = [line.strip() for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            elif file_path.suffix.lower() == ".json":
                data = json.loads(file_path.read_text(encoding="utf-8"))
                originals = [str(x if isinstance(x, str) else x["text"]).strip() for x in data]
            else:
                return errors + ["source_text_file must be .txt (one phrase/word per line) or .json (array of strings or {text} objects)."]
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            return errors + [f"Cannot read source_text_file: {exc}"]
        expected = collections.Counter(normalized_utterance(x) for x in originals)
        observed = collections.Counter(normalized_utterance(x["text"]) for x in units)
        if expected != observed:
            missing = list((expected - observed).elements())
            surplus = list((observed - expected).elements())
            errors.append(f"source_units differ from original source_text_file: missing={missing[:12]}, extra={surplus[:12]}")
    inventory = plan.get("source_inventory")
    if inventory:
        for i, item in enumerate(inventory["items"]):
            linked = item.get("source_unit_ids") or []
            if not linked:
                errors.append(f"source_inventory.items[{i}] needs source_unit_ids: every supplied audio's phrase must appear on at least one card.")
            for uid in linked:
                if uid not in ids:
                    errors.append(f"source_inventory.items[{i}] references unknown source_unit_id {uid!r}.")
            if item["status"] == "selected":
                unit_cards = {cid for unit in units if unit["id"] in linked for cid in unit["card_ids"]}
                if not set(item.get("card_ids") or []) & unit_cards:
                    errors.append(f"source_inventory.items[{i}]: selected audio does not link a card that displays its phrase.")
            # Duplicate original audio may be omitted as a separate sound card,
            # but its phrase still needs a source unit displayed on a card.
    return errors



def vocabulary_match(text: str, term: str) -> bool:
    """Match word/phrase boundaries while allowing French clitics.

    'université' matches "l'université"; 'can' must not match "can't".
    Only orthographic boundaries are checked, not word meanings.
    """
    haystack = normalized_utterance(text)
    needle = normalized_utterance(term)
    if not needle:
        return False
    return re.search(r"(?<!\w)" + re.escape(needle) + r"(?![\w'])", haystack) is not None


def vocabulary_coverage(plan: dict[str, Any]) -> dict[str, Any]:
    """Lexical form coverage: excludes verbatim original-source footers."""
    source_words = {
        word for unit in plan.get("source_units", [])
        for word in normalized_utterance(str(unit["text"])).split()
        if not word.isdecimal()
    }
    used_words = {
        word for card in plan["cards"]
        for raw in ([str(card["target_text"])] +
                    [str(e["text"]) for e in card.get("teaching_examples", [])])
        for word in normalized_utterance(raw).split()
    }
    missing = sorted(source_words - used_words)
    result = {"source_words": len(source_words),
              "covered_words": len(source_words) - len(missing),
              "missing_words": missing}
    if plan.get("version") == "2.6":
        priority = [normalized_utterance(str(item))
                    for item in plan.get("teacher_analysis", {}).get("priority_vocabulary", [])]
        active = [normalized_utterance(str(card["target_text"])) for card in plan["cards"]]
        active += [normalized_utterance(str(ex["text"]))
                   for card in plan["cards"] for ex in card.get("teaching_examples", [])]
        result.update({
            "context_only_words": missing,
            "priority_vocabulary": len(priority),
            "priority_covered": sum(any(vocabulary_match(content, term) for content in active) for term in priority),
        })
    return result


def validate_teacher_cards(plan: dict[str, Any]) -> list[str]:
    """Ensure provenance and that all source words are used in learning content."""
    if plan["version"] not in {"2.5", "2.6"}:
        return []
    errors: list[str] = []
    source_units = plan.get("source_units", [])
    for i, card in enumerate(plan["cards"]):
        prefix = f"cards[{i}]"
        origin = card.get("origin")
        if origin not in {"source", "teacher"}:
            errors.append(f"{prefix}.origin is required in v2.5 (source or teacher).")
            continue
        linked_units = [unit for unit in source_units
                        if str(card["id"]) in unit["card_ids"]]
        target = normalized_utterance(str(card["target_text"]))
        if origin == "source":
            if not any(
                f" {target} " in f" {normalized_utterance(str(unit['text']))} "
                for unit in linked_units
            ):
                errors.append(
                    f"{prefix}.origin=source: target_text must occur in a linked "
                    "verbatim source unit. Adapted phrases use origin=teacher."
                )
        else:
            if card.get("source_excerpt"):
                errors.append(
                    f"{prefix}.origin=teacher cannot claim an exact source_excerpt."
                )
            if not str(card.get("base_text", "")).strip():
                errors.append(
                    f"{prefix}.base_text required for teacher-created target."
                )
        for j, example in enumerate(card.get("teaching_examples") or []):
            if (not str(example.get("text", "")).strip() or
                    normalized_utterance(str(example["text"])) == target):
                errors.append(
                    f"{prefix}.teaching_examples[{j}] must differ from the target."
                )
    missing = vocabulary_coverage(plan)["missing_words"]
    if missing and plan["version"] == "2.5":
        errors.append(
            "v2.5 vocabulary coverage incomplete: source words missing from "
            "card targets and teacher_examples (Source footers do not count): "
            + ", ".join(missing[:35])
            + (" ..." if len(missing) > 35 else "")
        )
    return errors



def validate_professor_selection(plan: dict[str, Any]) -> list[str]:
    """Enforce deliberate chunk selection, not one copied turn per card."""
    if plan["version"] != "2.6":
        return []
    errors: list[str] = []
    analysis = plan.get("teacher_analysis")
    if not analysis:
        return ["v2.6 requires teacher_analysis with goals, priority vocabulary, and rejected candidates."]
    if len(plan.get("source_units", [])) >= 3 and not analysis["discarded_candidates"]:
        errors.append("teacher_analysis.discarded_candidates must justify at least one rejected candidate for multi-unit material.")
    original = [normalized_utterance(str(unit["text"]))
                for unit in plan.get("source_units", [])]
    used = [normalized_utterance(str(card["target_text"])) for card in plan["cards"]]
    used += [normalized_utterance(str(e["text"]))
             for card in plan["cards"] for e in card.get("teaching_examples", [])]
    goals: set[str] = set()
    entire_long_turns = 0
    for index, card in enumerate(plan["cards"]):
        prefix = f"cards[{index}]"
        goal = str(card.get("learning_goal", "")).strip()
        reason = str(card.get("selection_reason", "")).strip()
        if not goal or not reason:
            errors.append(f"{prefix} requires learning_goal and selection_reason (one distinct teachable objective and its review value).")
        normalized_goal = normalized_utterance(goal)
        if normalized_goal and normalized_goal in goals:
            errors.append(f"{prefix}.learning_goal duplicates another card's goal; check semantic redundancy.")
        goals.add(normalized_goal)
        target = normalized_utterance(str(card["target_text"]))
        words = target.split()
        if card["skill"] == "reading" and len(words) > 17:
            errors.append(f"{prefix}.target_text is too long for a fast Reading task ({len(words)} words); mine a shorter natural chunk.")
        if len(words) >= 9 and target in original:
            entire_long_turns += 1
    if len(original) >= 3 and len(plan["cards"]) >= 3:
        if entire_long_turns >= max(3, (len(plan["cards"]) + 2) // 3):
            errors.append(
                "v2.6 source-copy shortcut detected: many cards repeat whole original "
                "turns. Mine useful short chunks and teacher examples instead; preserve "
                "the original complete sentence on the Back."
            )
    original_joined = " ".join(original)
    for term in analysis["priority_vocabulary"]:
        normalized = normalized_utterance(str(term))
        if not normalized or not vocabulary_match(original_joined, normalized):
            errors.append(f"Priority vocabulary {term!r} is not present in source units.")
        elif not any(vocabulary_match(txt, normalized) for txt in used):
            errors.append(f"Priority vocabulary {term!r} is missing from targets and examples; Source footers are not active use.")
    for i, candidate in enumerate(analysis["discarded_candidates"]):
        if normalized_utterance(str(candidate["text"])) in used:
            errors.append(f"teacher_analysis.discarded_candidates[{i}] must not equal an accepted card or example.")
    return errors


def validate_plan(
    plan: dict[str, Any],
    plan_path: Path,
    check_media: bool = True,
    config_path: Path | None = None,
) -> list[str]:
    errors = schema_errors(plan, "card-plan.schema.json", "Plan")
    if errors:
        return errors

    if plan["version"] in {"2.1", "2.2", "2.3", "2.4", "2.5", "2.6"} and "source_inventory" not in plan:
        source_audio = any(
            card.get("audio_clip")
            or (card.get("audio_provenance") or {}).get("kind") in {"user-supplied", "native-source"}
            or (plan["version"] in {"2.2", "2.3", "2.4", "2.5", "2.6"} and card.get("audio")
                and (card.get("audio_provenance") or {}).get("kind") != "tts")
            for card in plan["cards"]
        )
        if source_audio:
            errors.append(
                "source_inventory is required whenever original source audio "
                "is clipped or attached. Enumerate all original recordings and justify skips."
            )
    if plan["version"] in {"2.4", "2.5", "2.6"}:
        voice = (plan.get("audio_settings") or {}).get("voice")
        if voice:
            code = str(plan["target_language"]["code"]).replace("-", "_")
            if not (voice.startswith(code + "-") or (
                len(code) == 2 and voice.startswith(code + "_")
            )):
                errors.append("audio_settings.voice must match target_language.code.")
    errors.extend(validate_source_inventory(plan, plan_path))
    errors.extend(validate_source_units(plan, plan_path, check_media=check_media))
    errors.extend(validate_teacher_cards(plan))
    errors.extend(validate_professor_selection(plan))
    resolved_config = discover_config(plan_path, config_path)
    if resolved_config is not None:
        errors.extend(validate_language_config(plan, resolved_config))

    seen_ids: set[str] = set()
    seen_retrievals: dict[tuple[str, ...], tuple[int, str]] = {}
    media_by_basename: dict[str, Path] = {}
    audio_uses: dict[Path, list[tuple[int, str, str]]] = {}
    audio_hash_uses: dict[str, list[tuple[int, str, str, str]]] = {}
    plan_dir = plan_path.resolve().parent

    for index, card in enumerate(plan["cards"]):
        prefix = f"cards[{index}]"
        if plan["version"] in {"2.3", "2.4", "2.5", "2.6"} and check_media and not card.get("audio"):
            errors.append(f"{prefix}.audio must be resolved for v2.3; run media enrichment.")
        card_id = str(card["id"]).strip()
        if card_id in seen_ids:
            errors.append(f"Duplicate card id: {card_id}")
        else:
            seen_ids.add(card_id)

        signature = retrieval_signature(card)
        previous = seen_retrievals.get(signature)
        if previous is not None:
            previous_index, previous_id = previous
            errors.append(
                f"{prefix}: duplicate retrieval task of cards[{previous_index}] "
                f"(id={previous_id!r}); differing ids, tags, notes, or sources "
                "do not make a new learning target."
            )
        else:
            seen_retrievals[signature] = (index, card_id)

        skill = card["skill"]
        if plan["version"] in {"2.1", "2.2", "2.3", "2.4", "2.5", "2.6"} and skill == "production":
            errors.append(
                f"{prefix}.skill: Production is retired for new plans (v2.1–v2.6). "
                "Use Reading/Listening/Pronunciation/Writing only; v2.0 stays readable for legacy archives."
            )
        mode = normalize_mode(card)
        allowed_modes = SUPPORTED_MODES_BY_SKILL[skill]
        if mode not in allowed_modes:
            errors.append(
                f"{prefix}.mode '{mode}' is not supported for skill '{skill}'. "
                f"Allowed: {sorted(allowed_modes)}"
            )
        if plan["version"] in {"2.2", "2.3", "2.4", "2.5", "2.6"} and skill == "reading":
            target = str(card["target_text"])
            if any(separator in target.casefold() for separator in (" / ", " × ", " vs ", " versus ")) and not str(card.get("prompt", "")).strip():
                errors.append(
                    f"{prefix}.prompt: Reading comparison/contrast fronts require a "
                    "specific instruction (e.g. which grammatical distinction to notice)."
                )
        if skill == "production" and not str(card.get("prompt", "")).strip():
            errors.append(f"{prefix}.prompt is required for production cards.")
        if skill == "writing":
            if not str(card.get("prompt", "")).strip():
                errors.append(f"{prefix}.prompt is required for Writing to constrain the typed answer.")
            try:
                writing_parts(card)
            except ValueError as exc:
                errors.append(f"{prefix}.writing_answer: {exc}")
        elif card.get("writing_answer") is not None:
            errors.append(f"{prefix}.writing_answer is only supported for Writing cards.")
        request = card.get("audio_request")
        if request and (mode == "standard" or (skill == "pronunciation" and mode == "spelling-sound")):
            requested_text = normalized_utterance(str(request["text"]))
            target_text = normalized_utterance(str(card["target_text"]))
            if requested_text != target_text:
                errors.append(
                    f"{prefix}.audio_request.text must match target_text for this mode; "
                    "TTS must not teach different spoken words than the card answer."
                )
        clip = card.get("audio_clip")
        audio_sources = [key for key in ("audio", "audio_clip", "audio_request") if card.get(key)]
        if len(audio_sources) > 1:
            errors.append(
                f"{prefix}: choose only one audio source: audio, audio_clip, or audio_request."
            )
        if card.get("image") and card.get("image_request"):
            errors.append(f"{prefix}: choose only one image source: image or image_request.")
        if clip and check_media:
            errors.append(f"{prefix}.audio_clip must be resolved before delivery.")
        if skill == "listening" and not str(card.get("audio", "")).strip():
            if check_media or (
                plan["version"] not in {"2.3", "2.4", "2.5", "2.6"} and not (card.get("audio_request") or clip)
            ):
                errors.append(f"{prefix}.audio is required for listening cards after media enrichment.")
        if skill == "pronunciation" and not str(card.get("prompt", "")).strip():
            errors.append(f"{prefix}.prompt is required for pronunciation cards so the builder never invents a base-language instruction.")
        if skill == "pronunciation" and mode in AUDIO_REQUIRED_PRONUNCIATION_MODES and not str(card.get("audio", "")).strip():
            if check_media or (
                plan["version"] != "2.3" and not (card.get("audio_request") or clip)
            ):
                errors.append(f"{prefix}.audio is required for pronunciation mode '{mode}' after media enrichment.")

        # A source excerpt is a verbatim quotation, not a generated paraphrase.
        # Verify even small chunks against the supplied source wording.
        source_excerpt = normalized_utterance(str(card.get("source_excerpt", "")))
        target_text = normalized_utterance(str(card["target_text"]))
        if source_excerpt and f" {target_text} " not in f" {source_excerpt} ":
            errors.append(
                f"{prefix}.source_excerpt does not contain the target wording; "
                "check the original material and do not silently rewrite quotations."
            )

        raw_audio = card.get("audio")
        if raw_audio:
            path = Path(str(raw_audio))
            resolved_audio = (path if path.is_absolute() else plan_dir / path).resolve()
            target = normalized_utterance(str(card.get("target_text", "")))
            transcript = normalized_utterance(str(card.get("audio_transcript", "")))
            audio_uses.setdefault(resolved_audio, []).append((index, target, transcript))
            # Full-sentence listening and answer-feedback audio must say exactly
            # the card's target, not a longer dialogue that happens to contain it.
            # Recognition-only Reading may intentionally retain broader context.
            exact_audio = skill in {"listening", "production", "writing"} or (
                skill == "pronunciation" and mode in {"standard", "spelling-sound"}
            )
            if transcript and target:
                if exact_audio and transcript != target:
                    errors.append(
                        f"{prefix}.audio_transcript must match target_text exactly "
                        "for this skill; clip the original recording, use matching "
                        "TTS, or omit optional answer audio."
                    )
                elif not exact_audio and f" {target} " not in f" {transcript} ":
                    errors.append(
                        f"{prefix}.audio_transcript does not contain the target wording; "
                        "use a matching clip, adjust the target, or omit the audio."
                    )
            provenance = card.get("audio_provenance") or {}
            if exact_audio and provenance.get("kind") in {"user-supplied", "native-source"} and not transcript:
                errors.append(
                    f"{prefix}.audio_transcript is required for original source audio "
                    "used as this skill's retrieval/answer audio. Verify the actual "
                    "spoken words; file decoding alone does not establish alignment."
                )

        for media_key in ("audio", "image"):
            raw = card.get(media_key)
            if not raw:
                continue
            media_path = Path(str(raw))
            if not media_path.is_absolute():
                media_path = (plan_dir / media_path).resolve()
            basename = media_path.name
            previous = media_by_basename.get(basename)
            if previous is not None and previous != media_path:
                errors.append(f"Media basename collision for '{basename}': '{previous}' and '{media_path}'.")
            else:
                media_by_basename[basename] = media_path
            if check_media:
                if not media_path.is_file():
                    errors.append(f"Missing {media_key} file for {prefix}: {media_path}")
                    continue
                try:
                    current = validate_media_file(media_path, media_key)
                except MediaValidationError as exc:
                    errors.append(f"Invalid {media_key} for {prefix}: {exc}")
                    continue
                if media_key == "audio":
                    fingerprint = str(current.get("sha256", ""))
                    audio_hash_uses.setdefault(fingerprint, []).append((
                        index, normalized_utterance(str(card["target_text"])),
                        skill, mode,
                    ))
                recorded = (card.get("media_validation") or {}).get(media_key)
                if recorded and recorded.get("sha256") and recorded["sha256"] != current["sha256"]:
                    errors.append(
                        f"{prefix}.{media_key} changed after validation: "
                        f"recorded sha256={recorded['sha256']} current sha256={current['sha256']}"
                    )

    for path, uses in audio_uses.items():
        if len({target for _, target, _ in uses}) <= 1:
            continue
        transcripts = {transcript for _, _, transcript in uses if transcript}
        for index, _, transcript in uses:
            if not transcript:
                errors.append(
                    f"cards[{index}].audio_transcript is required because audio "
                    f"'{path.name}' is reused for different target texts. "
                    "Verify the recording transcript before reusing it."
                )
        if len(transcripts) > 1:
            errors.append(
                f"Audio '{path.name}' has inconsistent transcripts across reused cards."
            )

    # Distinct filenames may hide byte-identical recordings assigned to
    # different spoken targets. Reading and sound-identification can use a
    # broader context, so only compare exact-audio skills here.
    for fingerprint, uses in audio_hash_uses.items():
        exact_uses = [
            (index, target) for index, target, used_skill, used_mode in uses
            if used_skill in {"listening", "production", "writing"} or (
                used_skill == "pronunciation" and used_mode in {"standard", "spelling-sound"}
            )
        ]
        if len({target for _, target in exact_uses}) > 1:
            errors.append(
                "Identical audio bytes are assigned to different exact-audio "
                "targets in cards "
                + ", ".join(f"{index} ({target})" for index, target in exact_uses)
                + "; verify the source and clip per target."
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an anki-language card plan.")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--config", type=Path, help="Explicit workspace language configuration. Auto-discovered when omitted.")
    parser.add_argument("--allow-missing-media", action="store_true", help="Validate structure without requiring referenced media files to exist.")
    args = parser.parse_args()
    try:
        plan = load_plan(args.plan)
        errors = validate_plan(plan, args.plan, check_media=not args.allow_missing_media, config_path=args.config)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2
    if errors:
        print("Plan validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Plan valid: {len(plan['cards'])} card(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())