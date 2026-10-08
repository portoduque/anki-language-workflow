from __future__ import annotations

import json
import subprocess
import sys
import wave
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"
SCRIPTS = SKILL / "scripts"

sys.path.insert(0, str(SCRIPTS))

from build_apkg import CSS, MODEL_VERSION, make_model  # noqa: E402
from deliver_live import ensure_models  # noqa: E402


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def make_wav(path: Path) -> None:
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(b"\x00\x00" * 3200)


def make_png(path: Path) -> None:
    Image.new("RGB", (48, 32), (230, 230, 230)).save(path, format="PNG")


def test_every_v5_skill_has_safe_front_and_clear_answer_hierarchy() -> None:
    assert MODEL_VERSION == 5

    models = {skill: make_model(skill) for skill in ("reading", "listening", "production", "pronunciation")}
    fronts = {skill: model.templates[0]["qfmt"] for skill, model in models.items()}
    backs = {skill: model.templates[0]["afmt"] for skill, model in models.items()}

    # Reading tests written recognition without leaking the base-language answer.
    assert "{{Target}}" in fronts["reading"]
    assert "{{Base}}" not in fronts["reading"]
    assert "{{Source}}" not in fronts["reading"]

    # Listening tests audio first; transcript/meaning stay off the front.
    assert "{{FrontAudio}}" in fronts["listening"]
    assert "{{Target}}" not in fronts["listening"]
    assert "{{Base}}" not in fronts["listening"]
    assert "{{Source}}" not in fronts["listening"]

    # Production tests the learner-facing cue, never the target answer.
    assert "{{Prompt}}" in fronts["production"]
    assert "{{Target}}" not in fronts["production"]
    assert "{{Base}}" not in fronts["production"]
    assert "{{Source}}" not in fronts["production"]

    # The written target itself remains off the template front. The deterministic
    # FrontCue is populated only for read-aloud/spelling-to-sound tasks.
    assert "{{Prompt}}" in fronts["pronunciation"]
    assert "{{Target}}" not in fronts["pronunciation"]
    assert "{{Base}}" not in fronts["pronunciation"]
    assert "{{Source}}" not in fronts["pronunciation"]

    for skill, back in backs.items():
        assert "{{FrontSide}}" in back
        assert '<hr id="answer">' in back
        assert "{{TargetLanguage}}" in back
        assert "{{Source}}" in back
        assert 'class="answer-chip">Answer</div>' in back

    # Reading promotes meaning first; the other skills promote the target answer first.
    assert backs["reading"].index("{{Base}}") < backs["reading"].index("{{Target}}")
    for skill in ("listening", "production", "pronunciation"):
        assert backs[skill].index("{{Target}}") < backs[skill].index("{{Base}}")


def test_v5_optional_support_is_conditional_and_does_not_create_empty_sections() -> None:
    optional = ("Focus", "IPA", "Reading", "Variant", "Grammar", "Notes", "Source")

    for skill in ("reading", "listening", "production", "pronunciation"):
        back = make_model(skill).templates[0]["afmt"]
        for field in optional:
            assert f"{{{{#{field}}}}}" in back
            assert f"{{{{/{field}}}}}" in back

    # Production already shows Image on the front through FrontSide, so the answer
    # deliberately avoids rendering a second copy.
    production = make_model("production").templates[0]
    assert "{{#Image}}" in production["qfmt"]
    assert "{{#Image}}" not in production["afmt"]

    for skill in ("reading", "listening", "pronunciation"):
        assert "{{#Image}}" in make_model(skill).templates[0]["afmt"]


def test_v5_css_keeps_mobile_night_mode_rtl_and_dependency_free_guarantees() -> None:
    css = CSS.lower()
    assert ".card.nightmode" in css
    assert "@media (max-width: 480px)" in css
    assert "text-align: start" in css
    assert "unicode-bidi: plaintext" in css
    assert "overflow-wrap: anywhere" in css
    assert "prefers-reduced-motion" in css
    assert "http://" not in css
    assert "https://" not in css
    assert "@import" not in css

    for skill in ("reading", "listening", "production", "pronunciation"):
        model = make_model(skill)
        rendered = (model.templates[0]["qfmt"] + model.templates[0]["afmt"]).lower()
        assert 'dir="auto"' in rendered
        assert "<script" not in rendered
        assert "<iframe" not in rendered
        assert "javascript:" not in rendered


def test_full_four_skill_v5_plan_builds_and_deep_validates_with_media(tmp_path: Path) -> None:
    listening_audio = tmp_path / "listening.wav"
    pronunciation_audio = tmp_path / "pronunciation.wav"
    image = tmp_path / "scene.png"
    make_wav(listening_audio)
    make_wav(pronunciation_audio)
    make_png(image)

    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "Portuguese", "code": "pt-BR"},
        "deck_name": "French UX Functional",
        "cards": [
            {
                "id": "ui-reading",
                "skill": "reading",
                "target_text": "Même s'il pleut, je vais courir.",
                "base_text": "Mesmo que esteja chovendo, vou correr.",
                "prompt": "Entenda a ideia principal.",
                "reading": "Même s'il pleut...",
                "grammar": "concessive clause",
                "source": "functional-test",
                "tags": ["ui-test"],
            },
            {
                "id": "ui-listening",
                "skill": "listening",
                "target_text": "Je suis prêt.",
                "base_text": "Estou pronto.",
                "prompt": "Ouça antes de revelar a resposta.",
                "audio": listening_audio.name,
                "audio_transcript": "Je suis prêt.",
                "audio_provenance": {"kind": "user-supplied"},
                "source": "functional-test",
                "tags": ["ui-test"],
            },
            {
                "id": "ui-production",
                "skill": "production",
                "target_text": "J'ai déjà fini.",
                "base_text": "Eu já terminei.",
                "prompt": "Diga em francês: Eu já terminei.",
                "hint": "Use déjà.",
                "image": image.name,
                "image_provenance": {"kind": "user-supplied"},
                "source": "functional-test",
                "tags": ["ui-test"],
            },
            {
                "id": "ui-pronunciation",
                "skill": "pronunciation",
                "mode": "sound-discrimination",
                "target_text": "rue",
                "base_text": "rua",
                "prompt": "Identifique e repita o som.",
                "focus": "/ʁy/",
                "ipa": "/ʁy/",
                "audio": pronunciation_audio.name,
                "audio_provenance": {"kind": "user-supplied"},
                "source": "functional-test",
                "tags": ["ui-test"],
            },
        ],
    }

    plan_path = tmp_path / "plan.json"
    output = tmp_path / "French-UX-Functional.apkg"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")

    build = run(str(SCRIPTS / "build.py"), str(plan_path), "--output", str(output))
    assert build.returncode == 0, build.stdout + build.stderr
    assert output.is_file()

    validate = run(str(SCRIPTS / "validate_apkg.py"), str(output), "--plan", str(plan_path))
    assert validate.returncode == 0, validate.stdout + validate.stderr
    summary = json.loads(validate.stdout)

    assert summary["note_count"] == 4
    assert summary["card_count"] == 4
    assert summary["media_total"] == 3
    assert {
        "French UX Functional::01 Reading",
        "French UX Functional::02 Listening",
        "French UX Functional::03 Production",
        "French UX Functional::04 Pronunciation & Sounds",
    }.issubset(set(summary["deck_names"]))


class ModelContractFakeClient:
    def __init__(self) -> None:
        self.models: dict[str, dict[str, Any]] = {}

    def invoke(self, action: str, params: dict[str, Any] | None = None) -> Any:
        params = params or {}
        if action == "modelNames":
            return list(self.models)
        if action == "createModel":
            self.models[params["modelName"]] = {
                "fields": list(params["inOrderFields"]),
                "templates": {
                    item["Name"]: {"Front": item["Front"], "Back": item["Back"]}
                    for item in params["cardTemplates"]
                },
                "css": params["css"],
            }
            return {"id": len(self.models)}
        if action == "modelFieldNames":
            return self.models[params["modelName"]]["fields"]
        if action == "modelTemplates":
            return self.models[params["modelName"]]["templates"]
        if action == "modelStyling":
            return {"css": self.models[params["modelName"]]["css"]}
        raise AssertionError(f"Unexpected AnkiConnect action: {action}")


def test_live_model_contract_accepts_all_four_v5_models() -> None:
    client = ModelContractFakeClient()
    ensure_models(client, {"reading", "listening", "production", "pronunciation"})

    assert set(client.models) == {
        "Anki Language v5 — Reading",
        "Anki Language v5 — Listening",
        "Anki Language v5 — Production",
        "Anki Language v6 — Pronunciation & Sounds",
    }

    # A second pass proves the stored templates/CSS match the deterministic
    # model contract rather than relying only on successful creation.
    ensure_models(client, {"reading", "listening", "production", "pronunciation"})
