from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, check=False, text=True, capture_output=True)


def test_portable_skill_validates() -> None:
    result = run(str(SKILL / "scripts" / "validate_skill.py"), str(SKILL))
    assert result.returncode == 0, result.stdout + result.stderr


def test_skill_requires_first_run_target_and_base_languages() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "Mandatory first-run language setup" in text
    assert "Target language" in text
    assert "Base language" in text
    assert "do not use a default" in text.lower()
    assert "anki-language.config.json" in text


def test_openai_metadata_mentions_skill_and_first_run() -> None:
    data = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    assert "$anki-language" in data["interface"]["default_prompt"]
    assert "target language" in data["interface"]["default_prompt"].lower()
    assert "base language" in data["interface"]["default_prompt"].lower()
    assert data["policy"]["allow_implicit_invocation"] is True


def test_antigravity_workflow_delegates_and_has_first_run_handshake() -> None:
    workflow = (SKILL / "assets" / "antigravity-workflow.md").read_text(encoding="utf-8")
    assert "use the installed `anki-language` skill as the source of truth" in workflow
    assert "target language" in workflow.lower()
    assert "base language" in workflow.lower()


def test_readme_documents_all_install_surfaces() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for command in ("python install.py codex", "python install.py claude", "python install.py antigravity", "python install.py generic"):
        assert command in readme
    assert "README maintenance rule" in readme

def test_skill_exposes_non_negotiable_card_rules() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    required = (
        "minimum useful number of cards",
        "one primary retrieval target",
        "self-orienting",
        "blind/ambiguous cloze is forbidden",
        "do not create automatic reverse cards",
        "do not generate every card type",
        "sentence mining is selective",
        "audio and images are optional",
        "keep answers concise",
        "ask the user instead of guessing",
    )
    for phrase in required:
        assert phrase in text


def test_readme_contains_official_card_creation_rules() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Official card-creation rules" in readme
    assert "useful, distinct, clear, atomic, fast" in readme


def test_skill_allows_selective_multi_card_reuse_without_volume_inflation() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    assert "same sentence, word, expression, audio, image, or passage may produce multiple cards" in text
    assert "incremental learning value" in text
    assert "future review cost" in text
    assert "optimize memory efficiency, not volume" in text


def test_readme_documents_anki_reference_library() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Complete Anki technical reference library" in readme
    assert "find_anki_reference.py" in readme
    assert "https://docs.ankiweb.net/llms.txt" in readme


def test_readme_documents_ankiconnect_reference_library() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Complete AnkiConnect reference library" in readme
    assert "find_ankiconnect_reference.py" in readme
    assert "114 baseline/common documented actions" in readme.lower()
    assert "118 cataloged entries total" in readme.lower()
    assert "version" in readme and "apiReflect" in readme


def test_skill_requires_validated_automatic_media_pipeline() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "## Automatic media and delivery" in skill
    assert "audio_request" in skill
    assert "image_request" in skill
    assert "run_pipeline.py" in skill
    assert "Never bypass this gate" in skill
    assert "retrieveMediaFile" in skill
    assert "SHA-256" in skill


def test_readme_documents_media_generation_and_delivery_modes() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Automatic audio, images, and delivery" in readme
    assert "Piper" in readme
    assert "Openverse" in readme
    assert "Wikimedia Commons" in readme
    assert "--delivery live" in readme
    assert "--delivery both" in readme
    assert "retrieveMediaFile" in readme
    assert "--skip-media-deps" in readme


def test_antigravity_workflow_never_bypasses_media_validation() -> None:
    workflow = (SKILL / "assets" / "antigravity-workflow.md").read_text(encoding="utf-8")
    assert "every audio/image is decoded and hashed before packaging/upload" in workflow
    assert "Never bypass media validation" in workflow


def test_fluent_forever_refinements_are_explicit_and_selective() -> None:
    card_rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()

    assert "same speaker/voice" in card_rules
    assert "fade out spelling/sound scaffolding" in card_rules
    assert "semantic success over exact example reproduction" in card_rules
    assert "target-language definition" in card_rules
    assert "same speaker/voice" in skill
    assert "spelling/spelling-sound cards are scaffolding" in skill
    assert "semantically correct alternative examples" in skill
    assert "monolinguality is not a goal by itself" in pedagogy


def test_fluent_forever_research_note_records_rejections() -> None:
    note = (SKILL / "references" / "research" / "fluent-forever-gallery.md").read_text(encoding="utf-8").lower()
    assert "rigid “no translation on cards”" in note
    assert "an image for almost every sentence" in note
    assert "fixed phase progression" in note
    assert "old anki scheduling settings" in note
    assert "100–300" in note


def test_readme_documents_research_derived_refinements() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Research-derived refinements" in readme
    assert "fluent-forever-gallery.md" in readme
    assert "Minimal-pair isolation" in readme
    assert "Spelling fade-out" in readme
    assert "Semantic success over verbatim recall" in readme


def test_corinna_tutorial_refinements_are_explicit() -> None:
    card_rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()

    assert "capture candidates first; commit to cards second" in card_rules
    assert "creation effort must also earn its keep" in card_rules
    assert "brief back-side explanation" in card_rules
    assert "candidate" in skill and "batch selection" in skill
    assert "card-creation/customization time also counts" in skill
    assert "grammar/morphology explanations" in skill
    assert "card-creation time is part of the cost function" in pedagogy


def test_corinna_research_note_records_adopted_and_rejected_ideas() -> None:
    note = (SKILL / "references" / "research" / "corinna-anki-tutorial.md").read_text(encoding="utf-8").lower()
    assert "complete transcript was reviewed" in note
    assert "separate capture from card commitment" in note
    assert "creation/customization time is a real cost" in note
    assert "concise grammar explanation" in note
    assert "universal 20 new / 200 review rule" in note
    assert "forvo add-on as the core audio pipeline" in note


def test_readme_documents_corinna_research_refinements() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "corinna-anki-tutorial.md" in readme
    assert "Candidate before card" in readme
    assert "Creation time counts" in readme
    assert "Grammar notes stay concise" in readme


def test_meredith_guide_adaptation_is_selective_and_complete() -> None:
    note = (SKILL / "references" / "research" / "meredith-anki-setup-guide.md").read_text(encoding="utf-8").lower()
    assert "complete spoken transcript was reviewed" in note
    assert "bootstrap candidate source" in note
    assert "maximum reviews/day = 9999" in note
    assert "learning step = 10m" in note
    assert "descending retrievability" in note
    assert "ascending retrievability" in note
    assert "sibling burying" in note


def test_fsrs_reference_uses_current_semantics_not_copied_presets() -> None:
    ref = (SKILL / "references" / "anki" / "07-scheduling-fsrs-study-options.md").read_text(encoding="utf-8")
    assert "current official Anki documentation" in ref
    assert "Do not hard-code `9999`" in ref
    assert "Do not prescribe a universal `10m`" in ref
    assert "Ascending retrievability" in ref
    assert "Descending retrievability" in ref
    assert "one Anki note per planned card" in ref
    assert "will **not automatically space those cross-skill cards**" in ref
    assert "Easy Days" in ref and "redistributes" in ref


def test_beginner_shared_deck_is_candidate_source_not_blind_import() -> None:
    rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8")
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "### Beginner bootstrap exception" in rules
    assert "Do not blindly import the whole shared deck" in rules
    assert "absolute beginner" in skill
    assert "candidate source" in skill


def test_readme_documents_meredith_settings_corrections() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "meredith-anki-setup-guide.md" in readme
    assert "Scheduling settings are not copied from research videos" in readme
    assert "Ascending retrievability" in readme
    assert "same note" in readme
    assert "Beginner bootstrap is allowed, not blind import" in readme


def test_evildea_tutorial_refinements_are_explicit_and_selective() -> None:
    rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()

    assert "prefer near-i+1 sentence mining" in rules
    assert "inspect polysemy before deciding the card" in rules
    assert "production targets need a higher naturalness bar" in rules
    assert "one primary unknown/focus item" in skill
    assert "polysemous words/expressions" in skill
    assert "unverified ai-generated sentence" in skill
    assert "near-i+1 mined sentences" in pedagogy


def test_evildea_research_note_records_adopted_and_rejected_ideas() -> None:
    note = (SKILL / "references" / "research" / "evildea-anki-language-tutorial.md").read_text(encoding="utf-8").lower()
    assert "complete spoken transcript was reviewed" in note
    assert "strong near-i+1 sentence-mining default" in note
    assert "production sentences need stronger authenticity" in note
    assert "six sentences on one reading front" in note
    assert "post-answer shadowing / chorusing" in note
    assert "fixed new-card range" in note
    assert "no schema, deck architecture, builder, media provider, or ankiconnect change" in note


def test_readme_documents_evildea_refinements() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "evildea-anki-language-tutorial.md" in readme
    assert "Near-i+1 mining is the default" in readme
    assert "Explore polysemy before encoding it" in readme
    assert "Production authenticity is stricter" in readme


def test_hodos_refinements_are_explicit_and_selective() -> None:
    rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()

    assert "one primary sense/usage per card" in rules
    assert "mnemonics are optional scaffolding" in rules
    assert "verify it from a trustworthy source" in rules
    assert "invented sound-alike/keyword" in rules
    assert "one primary sense/usage per card" in skill
    assert "ai must not fabricate linguistic ancestry" in skill
    assert "mnemonics are optional scaffolding" in pedagogy


def test_hodos_research_note_records_adopted_and_rejected_advice() -> None:
    note = (SKILL / "references" / "research" / "hodos-37000-anki-tips.md").read_text(encoding="utf-8").lower()
    assert "complete spoken transcript was reviewed" in note
    assert "one primary sense/usage per card" in note
    assert "mnemonics can be useful scaffolding" in note
    assert "two-second rule" in note
    assert "on-screen timer" in note
    assert "monthly deck retirement" in note
    assert "automatic “doubled” cards" in note


def test_scheduling_reference_rejects_arbitrary_speed_failures() -> None:
    ref = (SKILL / "references" / "anki" / "07-scheduling-fsrs-study-options.md").read_text(encoding="utf-8")
    assert "Response latency is not a fixed fail threshold" in ref
    assert "Do not turn a correct answer into **Again**" in ref
    assert "## Timers" in ref
    assert "time does not influence scheduling by itself" in ref
    assert "Auto Advance" in ref
    assert "## Deck continuity" in ref


def test_readme_documents_hodos_refinements() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "hodos-37000-anki-tips.md" in readme
    assert "One primary sense per card" in readme
    assert "Mnemonics are selective scaffolding" in readme
    assert "Correct-but-slow recall is **not** automatically a failure" in readme


def test_justin_sung_refinements_preserve_atomicity_and_transfer() -> None:
    rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()

    assert "atomic does not mean isolated" in rules
    assert "avoid learning the card wording instead of the language" in rules
    assert "graduate redundant scaffolds when mastery evidence exists" in rules
    assert "single contrast/relationship can be the primary retrieval target" in pedagogy
    assert "avoid cue overfitting" in pedagogy
    assert "contrast/relationship may be one primary retrieval target" in skill
    assert "never infer mastery from age alone" in skill


def test_justin_sung_research_note_records_adaptation_and_rejections() -> None:
    note = (SKILL / "references" / "research" / "justin-sung-anki-pro.md").read_text(encoding="utf-8").lower()
    assert "complete spoken transcript was reviewed" in note
    assert "atomic retrieval can still be relational" in note
    assert "avoid memorizing the card rather than the language" in note
    assert "graduate redundant scaffolds" in note
    assert "mega flashcards" in note
    assert "three correct / three incorrect" in note
    assert "100–150 flashcards per week" in note
    assert "no schema, builder, media provider, deck architecture, installer, or ankiconnect implementation change" in note


def test_readme_documents_justin_sung_transfer_refinements() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "justin-sung-anki-pro.md" in readme
    assert "Atomic can be relational" in readme
    assert "Avoid cue overfitting" in readme
    assert "Graduate redundant scaffolds carefully" in readme


def test_corinna_vocabulary_refinements_are_explicit_and_selective() -> None:
    rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()

    assert "preserve comprehension flow before extraction" in rules
    assert "meaning-first pass" in rules
    assert "stable mnemonics for grammatical attributes" in rules
    assert "do not hard-code one universal mapping" in rules
    assert "meaning-first pass" in skill
    assert "gender/noun class" in skill
    assert "stable concrete mnemonic code" in pedagogy


def test_corinna_vocabulary_research_note_records_adoptions_and_rejections() -> None:
    note = (SKILL / "references" / "research" / "corinna-anki-wrong-vocabulary.md").read_text(encoding="utf-8").lower()
    assert "complete spoken transcript was reviewed" in note
    assert "meaning-first pass before intensive extraction" in note
    assert "stable concrete mnemonic coding for grammatical gender/noun class" in note
    assert "translation ban" in note
    assert "automatic forward + reverse cards" in note
    assert "google images for every vocabulary item" in note
    assert "no schema, builder, deck architecture, media provider, installer, or ankiconnect implementation change" in note


def test_readme_documents_corinna_vocabulary_refinements() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "corinna-anki-wrong-vocabulary.md" in readme
    assert "Preserve comprehension flow" in readme
    assert "Grammar-attribute mnemonics are secondary" in readme
