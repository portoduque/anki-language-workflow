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


def test_redchamber_refinements_are_explicit_and_selective() -> None:
    rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()

    assert "reveal non-target dimensions when that isolates the skill" in rules
    assert "store distinct linguistic data in distinct fields when useful" in rules
    assert "`reading`" in rules
    assert "`variant`" in rules
    assert "`grammar`" in rules
    assert "handwriting/written recall" in rules
    assert "reveal non-target information" in skill
    assert "structured optional fields" in skill
    assert "information that is not being tested may be revealed" in pedagogy


def test_redchamber_research_note_records_architecture_tradeoff() -> None:
    note = (SKILL / "references" / "research" / "redchamber-optimize-anki-language.md").read_text(encoding="utf-8").lower()
    assert "complete spoken transcript was reviewed" in note
    assert "distinct linguistic data deserves distinct structured fields" in note
    assert "reveal non-target information to isolate one skill" in note
    assert "active handwriting can be treated as production" in note
    assert "why this repository is not switching to multi-card notes yet" in note
    assert "automatic generation of six skill cards" in note
    assert "anki language v3" in note


def test_anki_reference_documents_current_note_card_tradeoff() -> None:
    ref = (SKILL / "references" / "anki" / "02-notes-fields-card-types.md").read_text(encoding="utf-8")
    assert "Anki can use conditional replacement" in ref
    assert "Deck Override" in ref
    assert "one Anki note per selected planned card" in ref
    assert "`Reading`" in ref and "`Variant`" in ref and "`Grammar`" in ref


def test_readme_documents_structured_fields_and_current_models() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Structured language fields" in readme
    assert '"reading": "xuéxí"' in readme
    assert '"variant": "学习"' in readme
    assert '"grammar": "verb"' in readme
    assert "Anki Language v4" in readme
    assert "redchamber-optimize-anki-language.md" in readme
    assert "Reveal only non-target support" in readme
    assert "Keep distinct linguistic data structured" in readme


def test_jeremiah_refinements_clarify_before_scheduling() -> None:
    rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    note = (SKILL / "references" / "research" / "jeremiah-seven-rules-anki.md").read_text(encoding="utf-8").lower()

    assert "clarify the target before scheduling it" in rules
    assert "first-time semantic discovery" in rules
    assert "prior mastery is not required" in rules
    assert "first-time semantic discovery" in pedagogy
    assert "before promoting a candidate to a scheduled card" in skill
    assert "universal audio-only fronts" in note
    assert "automatic retirement after roughly six months" in note
    assert "deleting the deck after ordinary breaks" in note


def test_readme_documents_jeremiah_selective_refinements() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "jeremiah-seven-rules-anki.md" in readme
    assert "Clarify before scheduling" in readme
    assert "Pass/Fail add-on is not required" in readme
    assert "After a long break" in readme


def test_alemayhu_language_specific_feature_targeting_is_selective() -> None:
    rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    note = (SKILL / "references" / "research" / "alemayhu-custom-language-card-types.md").read_text(encoding="utf-8").lower()

    assert "target language-specific features selectively" in rules
    assert "never generate a full paradigm merely because it exists" in pedagogy
    assert "target-language-specific features" in skill
    assert "complete spoken transcript was reviewed" in note
    assert "one custom note type/template family per language" in note
    assert "automatic card generation for every available field" in note
    assert "no schema, anki note model, deck architecture, builder, media provider, installer, or ankiconnect implementation change" in note


def test_readme_documents_alemayhu_selective_refinement() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "alemayhu-custom-language-card-types.md" in readme
    assert "Target language-specific features selectively" in readme
    assert "never generate a full paradigm merely because it exists" in readme


def test_feedback_loop_refinements_are_selective_and_safe() -> None:
    rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    contract = (SKILL / "references" / "output-contract.md").read_text(encoding="utf-8").lower()
    note = (SKILL / "references" / "research" / "claude-code-anki-feedback-loop.md").read_text(encoding="utf-8").lower()

    assert "review history is evidence, not an automatic diagnosis" in rules
    assert "start with read-only inspection" in rules
    assert "preserve precise source locators when available" in rules
    assert "review history is evidence for diagnosis" in pedagogy
    assert "preserve precise source locators" in pedagogy
    assert "optional live maintenance / feedback audit" in skill
    assert "audit_live.py" in skill
    assert "explicit user approval" in skill
    assert "stable locator" in contract
    assert "complete spoken transcript was reviewed from start to finish" in note
    assert "automatic scheduling reprioritization from ai guesses" in note
    assert "automatic deletion of “low-value” cards" in note
    assert "no card-plan schema, note model, deck architecture, scheduler, media provider, installer, or live-delivery semantics need to change" in note


def test_readme_documents_feedback_audit_and_source_locators() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "claude-code-anki-feedback-loop.md" in readme
    assert "Preserve precise source locators" in readme
    assert "Maintenance starts read-only" in readme
    assert "audit_live.py" in readme
    assert "There is deliberately no universal “bad card” threshold" in readme


def test_refold_candidate_source_progression_is_evidence_driven() -> None:
    rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    note = (SKILL / "references" / "research" / "refold-learning-words-roadmap.md").read_text(encoding="utf-8").lower()

    assert "let candidate sources evolve with learner evidence" in rules
    assert "output/domain gaps are candidates, not literal translations" in rules
    assert "do not hard-code external roadmap phases or vocabulary-count milestones" in rules
    assert "let candidate sources evolve with learner evidence" in pedagogy
    assert "repeated real speaking/writing/domain gaps" in skill
    assert "never hard-code an external roadmap phase, corpus-frequency cutoff, or vocabulary-count milestone" in skill
    assert "roadmap sidebar/submenus were also expanded" in note
    assert "fixed 5 to 10 new cards/day" in note
    assert "no schema, config, deck, note-model, media, scheduler, installer, or ankiconnect change" in note


def test_readme_documents_refold_selective_adaptation() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "refold-learning-words-roadmap.md" in readme
    assert "Candidate sources evolve with learner evidence" in readme
    assert "external roadmap phase labels" in readme


def test_anki_forum_grammar_retrieval_intent_is_selective() -> None:
    rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    note = (SKILL / "references" / "research" / "anki-forum-language-card-structure.md").read_text(encoding="utf-8").lower()

    assert "choose grammar card format from retrieval intent" in rules
    assert "rule recall" in rules
    assert "recognition/discrimination" in rules
    assert "application/production" in rules
    assert "do not dump a full paradigm/table onto one card" in rules
    assert "choose the card format from the intended retrieval operation" in pedagogy
    assert "for grammar, choose the card format from the retrieval intent" in skill
    assert "supplied `/4` link points to the automatic system-closure post" in note
    assert "audio as structured data" in note
    assert "separate language study by time/location/background music" in note
    assert "no schema, note model, deck architecture, media provider, scheduler, installer, or ankiconnect change" in note


def test_readme_documents_anki_forum_selective_refinement() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "anki-forum-language-card-structure.md" in readme
    assert "Grammar format follows retrieval intent" in readme
    assert "automatic reversed grammar/vocabulary cards" in readme


def test_keiffenheim_reencounter_scarcity_is_selective() -> None:
    rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    note = (SKILL / "references" / "research" / "keiffenheim-flashcards-language-learning.md").read_text(encoding="utf-8").lower()

    assert "account for expected natural re-encounter frequency" in rules
    assert "rarity alone never justifies a card" in rules
    assert "natural re-encounter frequency" in pedagogy
    assert "expected natural re-encounter frequency" in skill
    assert "publicly accessible portion was reviewed in full" in note
    assert "not inferred, reconstructed, or treated as source evidence" in note
    assert "fixed 2,000–3,000-word threshold" in note
    assert "no schema, note model, deck architecture, media provider, scheduler, installer, or ankiconnect change" in note


def test_readme_documents_keiffenheim_selective_refinement() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "keiffenheim-flashcards-language-learning.md" in readme
    assert "Natural re-encounter scarcity matters" in readme
    assert "inaccessible paywalled article headings" in readme


def test_vidtoanki_refinement_is_technical_and_selective() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    contract = (SKILL / "references" / "output-contract.md").read_text(encoding="utf-8").lower()
    note = (SKILL / "references" / "research" / "vidtoanki-card-format-ecosystem.md").read_text(encoding="utf-8").lower()

    assert "structural validation, not proof of cross-client rendering" in skill
    assert "anki client rendering is the final authority" in contract
    assert "generated templates were not fully portable across night mode and bidirectional scripts" in note
    assert "anki language v4" in note
    assert "one rich note → several optional card types" in note
    assert "no card-plan schema, deck hierarchy, media provider, scheduler, installer, or ankiconnect protocol change" in note


def test_readme_documents_vidtoanki_portability_refinement() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "vidtoanki-card-format-ecosystem.md" in readme
    assert "Anki Language v4" in readme
    assert "spot-check representative cards in Anki" in readme


def test_vidtoanki_free_template_audit_avoids_schema_copying() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    contract = (SKILL / "references" / "output-contract.md").read_text(encoding="utf-8").lower()
    note = (SKILL / "references" / "research" / "vidtoanki-card-format-ecosystem.md").read_text(encoding="utf-8").lower()

    assert "prompt" in contract
    assert "situational/scene cue" in contract
    assert "essential card behavior may not depend on javascript or remote web assets" in contract
    assert "essential card behavior must not depend on javascript or remote web assets" in skill
    assert "exact free-template pack audit" in note
    assert "seven semantic fields" in note
    assert "why this repository is not copying the seven-field schema" in note
    assert "renaming the current `context` field or adding another schema field" in note
    assert "generated templates must not depend on javascript or remote web assets" in note


def test_readme_documents_free_template_transparency_decision() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "exact free-template pack files" in readme
    assert "no JavaScript or remote web assets required" in readme
    assert "scene/situation can live in `prompt`" in readme
