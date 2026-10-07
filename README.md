# Anki Language Workflow

AI-agnostic and language-agnostic workflow that turns study material into a small, selective Anki deck with automatic audio/image enrichment, strict media validation, and delivery as `.apkg`, directly to a running Anki through AnkiConnect, or both.

**The repository has no default language and no required AI provider.** Codex, Claude Code, and Google Antigravity have ready-made adapters, while any other AI can use the same canonical `SKILL.md` and deterministic Python pipeline.

## What happens on first use

Every workspace starts unconfigured. Before the AI analyzes the first material, it must ask you two questions:

1. **Target language** — the language you are learning, such as French, Japanese, Spanish, German, Arabic, etc.
2. **Base language** — the language that should explain, translate, cue, and guide the target language, such as English, Portuguese, Spanish, etc.

There is **no default** for either value. The answers are stored in `anki-language.config.json` in that workspace and reused on later runs until you change them.

Examples of valid configurations:

- target French / base English;
- target Japanese / base Portuguese;
- target German / base Spanish;
- target English / base French.

## What the workflow creates

The AI first decides whether each source item deserves a card at all. A source item may create zero, one, or several cards, but multiple cards are allowed only when they train genuinely different skills.

Deck hierarchy:

- `<TargetLanguage>::01 Reading`
- `<TargetLanguage>::02 Listening`
- `<TargetLanguage>::03 Production`
- `<TargetLanguage>::04 Pronunciation & Sounds`

Vocabulary, grammar, chunks, collocations, word forms, minimal pairs, source names, and similar dimensions are stored as tags instead of extra micro-decks.

Core rules:

- no card is created just because a template exists;
- no blind or ambiguous cloze;
- listening normally places audio on the front;
- production normally places audio on the back;
- images are added only when they improve retrieval;
- original/native permitted audio is preferred over TTS;
- explanations and cues use the configured base language;
- all generated APKG files pass deterministic validation before delivery.

## Official card-creation rules

These are product rules, not suggestions. The complete normative specification lives in `anki-language/references/card-selection.md`.

1. **Minimum useful set:** each source unit may generate 0, 1, or several cards.
2. **Selective multi-card reuse:** the same sentence, word, expression, audio, image, or passage may appear in multiple skill decks when each card trains a genuinely different and worthwhile retrieval operation.
3. **Marginal-benefit rule:** every extra sibling card must add enough learning value to justify its future review cost. Optimize **memory efficiency per review minute**, not card volume.
4. **No quotas:** never create Reading + Listening + Production + Pronunciation automatically.
5. **One retrieval target:** each card tests one primary piece of knowledge or skill.
6. **Self-orienting front:** every front identifies `<TargetLanguage> — <Skill>` so mixed reviews never show a contextless question.
7. **No guessing the author's intention:** prompts must make the intended retrieval clear without revealing the answer.
8. **No blind cloze:** a blank is used only when a semantic/function cue, lemma, or other constraint makes the intended answer sufficiently unambiguous.
9. **No automatic reverse cards:** recognition and production are different skills and get separate cards only when both matter.
10. **Translation is allowed:** the configured base language may be used when it is the clearest/fastest cue; translation is not banned on principle.
11. **Reading is selective:** use natural written context for useful recognition; skip material already understood reliably.
12. **Listening is audio-first:** do not reveal the transcript on the front; put transcript/base-language meaning on the back.
13. **Production is constrained:** front uses a precise base-language meaning/situation/context; answer and normally audio stay on the back.
14. **Pronunciation/Sounds is targeted:** use pronunciation, minimal pairs, sound discrimination, or spelling-sound cards only when sound is worth training; never reveal the written answer on a discrimination front.
15. **Prefer useful chunks/collocations/patterns:** do not reduce a useful expression to isolated words when the combination is the knowledge that matters.
16. **Sentence mining is selective:** do not turn every source sentence into a card; prefer natural, useful, comprehensible context with one main focus.
17. **Images are functional, not decorative:** prioritize concrete/visual concepts; skip ambiguous images that do not improve retrieval.
18. **Audio is functional, not mandatory:** prefer user-supplied original audio, then permitted native-speaker audio, then permitted high-quality TTS.
19. **Avoid redundancy/interference:** skip near-duplicate cards and improve prompts that make similar answers confusable.
20. **Fast reviews:** answers should be concise enough to verify recall quickly; extra explanation is secondary.
21. **Prefer the user's material:** preserve useful source sentences/audio/context instead of replacing them with generic content without reason.
22. **Ask instead of guessing:** if uncertainty changes meaning, target expression, transcription, register, acceptable answers, or media rights, ask the user before building.

A source reused across multiple decks is valid only when each card covers a real additional skill gap. If the extra card mostly repeats the same retrieval, discard it.

Final acceptance test for every card: **useful, distinct, clear, atomic, fast**. If one fails, revise or discard the card.

## Complete Anki technical reference library

The skill includes a dedicated Anki reference layer under `anki-language/references/anki/`. It is intentionally split by topic so an agent can retrieve only what it needs instead of loading a giant manual into context.

Included coverage:

- Anki's note/card/field/deck mental model;
- built-in and custom note/card types;
- templates, field replacement, HTML, CSS, RTL, TTS, hints, typed answers;
- Cloze and native Image Occlusion;
- audio/images/media packaging and filename rules;
- decks, tags, flags, Browser, search, filtered decks;
- scheduling and FSRS;
- import/export, CSV/TSV, APKG and COLPKG;
- sync, backups, profiles and collection files;
- statistics, true retention and leeches;
- curated useful add-ons with compatibility/security cautions;
- AnkiConnect, add-on development and APIs;
- AnkiMobile/AnkiDroid/platform compatibility;
- troubleshooting, security and version-sensitive behavior;
- authoritative source map and live documentation discovery.

### Fast reference routing

Agents with shell access can run:

`python anki-language/scripts/find_anki_reference.py "FSRS desired retention"`

or:

`python anki-language/scripts/find_anki_reference.py "APKG audio media"`

The router returns only the most relevant local files.

The official Anki documentation now exposes a complete machine-readable documentation index at:

https://docs.ankiweb.net/llms.txt

The workflow uses that as the live fallback for current/version-sensitive details instead of assuming the local summaries are permanently current.

### Consultation policy

The AI should consult the Anki library when the task depends on Anki implementation details, configuration, package/media behavior, scheduling, add-ons, APIs, compatibility, or troubleshooting.

It should **not** load the whole library during ordinary language/card pedagogy. Card-selection policy remains separate and authoritative in `references/card-selection.md`.

## Complete AnkiConnect reference library

For workflows that need to interact with a **running Anki Desktop collection**, the project includes a dedicated AnkiConnect knowledge base under:

`anki-language/references/anki-connect/`

It covers:

- installation with add-on code `2055492159`;
- configuration and defaults (`apiKey`, bind address/port, CORS origins, logging);
- HTTP request/response protocol and API versioning;
- permission negotiation, authentication and security;
- **114 baseline/common documented actions plus 4 newer/version-sensitive actions, for 118 cataloged entries total**;
- card/scheduling actions;
- deck/config actions;
- note/tag actions;
- model/note-type/field/template/CSS actions;
- media upload/retrieval/deletion;
- Browser/Reviewer/GUI automation;
- profiles, sync, batching, APKG import/export;
- review statistics/history;
- concrete JSON payload examples;
- language-workflow integration recipes;
- troubleshooting and destructive-operation cautions;
- source authority and version-drift policy.

### Fast AnkiConnect routing

Use:

`python anki-language/scripts/find_ankiconnect_reference.py "addNote audio duplicate"`

or:

`python anki-language/scripts/find_ankiconnect_reference.py "createModel templates css"`

or an exact action:

`python anki-language/scripts/find_ankiconnect_reference.py "storeMediaFile"`

The router returns only the most relevant guides plus matching actions from `ACTION_CATALOG.json`. Natural-language lookup uses action descriptions, exact Python signatures, parameters, category and risk metadata, so the caller does not need to know an action name in advance. Newer actions that are not present in every mirror are marked version-sensitive and must be confirmed with `apiReflect` before use.

### Runtime truth over stale documentation

For a live installation, the AI should use AnkiConnect's own:

- `version`
- `apiReflect`

to verify supported capabilities when an action is uncertain or version-sensitive.

The original `FooSoft/anki-connect` GitHub repository was archived and points to the author's SourceHut project. The local source map preserves that authoritative lineage. Because SourceHut is not always machine-readable to agents, the curated 2026 action snapshot is cross-checked against a recent public mirror, while **the user's running AnkiConnect remains capability truth** through `version` + `apiReflect`.

The recent snapshot includes four actions beyond the older 114-action baseline: `gradeNow`, `repositionNewCards`, `guiAddNoteSetData`, and `guiPlayAudio`. They are explicitly marked version-sensitive and are never assumed to exist without runtime verification.

AnkiConnect remains **optional**. If the task is simply to create a portable deck, the default architecture is still:

`card-plan.json → validated APKG`

Live AnkiConnect operations are used only when they add real value.

## Automatic audio, images, and delivery

The workflow can now resolve missing media automatically **after** card selection and **before** packaging/upload.

The AI still decides whether media adds learning value. The automation does not generate an image/audio file for every card merely because it can.

### Automatic audio

For a text-only card that should have audio, the plan can contain:

```json
{
  "audio_request": {
    "mode": "auto",
    "text": "J'ai fini par rester chez moi.",
    "provider": "auto"
  }
}
```

The built-in automatic TTS provider is **Piper**:

1. reads the current Piper voice catalog;
2. matches the configured target-language code;
3. selects a deterministic voice (medium quality preferred for the default efficiency/quality balance);
4. downloads the voice model if necessary;
5. synthesizes WAV audio locally;
6. decodes the produced audio;
7. verifies positive duration and records SHA-256;
8. only then allows the media to continue to APKG/AnkiConnect delivery.

The one-command installer installs Piper media support by default. Use `--skip-media-deps` only for a minimal installation.

Forvo is **not** a core provider. Its Anki add-ons run inside Anki and are not a stable cross-agent automation API. The workflow never scrapes Forvo. A Forvo pronunciation may only be used through a permitted API/license/workflow that allows the intended storage/embedding.

### Automatic images

For a visual concept:

```json
{
  "image_request": {
    "mode": "auto",
    "query": "red squirrel",
    "provider": "auto",
    "licenses": ["cc0", "pdm"]
  }
}
```

Automatic order:

1. **Openverse**
2. **Wikimedia Commons** fallback

The default allowlist is deliberately strict: CC0 and Public Domain Mark. Openverse is searched with mature content disabled and dead links filtered. Wikimedia fallback reads machine-readable Commons license metadata.

Downloaded images are normalized to WebP, constrained to 1600×1600, then decoded again before acceptance. Provenance stores provider/source/license/license URL/attribution when available.

### Mandatory validation before any upload

This is a hard project rule:

> **An audio or image file must be functionally validated before it may be packaged or uploaded into an Anki card.**

Validation checks:

- audio is a real decodable stream;
- audio duration is positive;
- image fully decodes;
- image dimensions are usable;
- file size is non-trivial;
- SHA-256 is recorded;
- if the file changes after validation, build/live delivery rejects it.

Useful direct checks:

`python anki-language/scripts/media_validate.py audio /path/to/file.wav`

`python anki-language/scripts/media_validate.py image /path/to/file.webp`

Required-media failure blocks delivery. Optional-media failure is recorded in `media_issues` and the card continues without the broken media.

### Delivery modes

The same resolved plan supports:

- **`apkg`** — validated portable package;
- **`live`** — direct insertion into a running Anki with AnkiConnect;
- **`both`** — live insertion plus APKG.

End-to-end:

`python anki-language/scripts/run_pipeline.py card-plan.json --delivery apkg`

Direct Anki:

`python anki-language/scripts/run_pipeline.py card-plan.json --delivery live`

Both:

`python anki-language/scripts/run_pipeline.py card-plan.json --delivery both --output French.apkg`

### Live AnkiConnect verification

Live mode does not stop at “the API returned success”.

Before `addNotes`:
- local audio/images are decoded and hashed;
- AnkiConnect capability is checked with `version` + `apiReflect`;
- notes are preflighted using `canAddNotesWithErrorDetail`.

After `addNotes`:
- `notesInfo` must show the media filename in the expected field;
- `retrieveMediaFile` downloads the file back from Anki;
- downloaded bytes must match the prevalidated local SHA-256.

Only then is the media reported as successfully delivered.

### Why AnkiConnect helps

AnkiConnect is the delivery/integration layer, not the media generator. It lets the workflow:

- create required decks/note types when absent;
- attach local audio/images directly during note creation;
- avoid manual copying into `collection.media`;
- verify the created note;
- retrieve uploaded media for byte-for-byte validation.

Automatic media generation/search remains provider-independent from AnkiConnect.

## Requirements

- Git;
- Python 3.11+;
- an AI coding/agent environment with filesystem and Python execution for fully automatic APKG/live generation;
- network access when automatic Piper voice download or image search is requested;
- Anki Desktop + AnkiConnect only for `live`/`both` delivery.

A chat-only AI can still follow the pedagogical rules and produce `card-plan.json`, but building the final `.apkg` requires a runtime capable of executing the included Python scripts.

## Installation from zero

### 1. Clone the repository

`git clone https://github.com/portoduque/anki-language-workflow.git`

`cd anki-language-workflow`

### 2. Install for your AI with one command

Choose exactly one:

**Codex**

`python install.py codex`

**Claude Code**

`python install.py claude`

**Google Antigravity IDE**

`python install.py antigravity`

**Antigravity CLI**

`python install.py antigravity-cli`

**Any other Agent-Skills-compatible AI**

`python install.py generic --dest /path/to/your-ai/skills/anki-language`

The one-command installer installs the core dependencies **and automatic Piper media support** and copies the canonical skill to the correct user-level location. Use `--skip-deps` to manage everything yourself, or `--skip-media-deps` to install the workflow without automatic Piper TTS.

To install only inside one project/workspace instead of globally, add:

`--scope project --project /path/to/workspace`

## How to use after installation

Open the workspace containing your language-learning material.

### Codex

Invoke:

`$anki-language`

Then provide or point to the material. On the first run, Codex asks for target language and base language before doing anything else.

### Claude Code

Invoke:

`/anki-language <material>`

Example:

`/anki-language ./materials/lesson-01/`

On the first run, Claude asks for target language and base language.

### Google Antigravity

Invoke:

`/anki-language <material>`

The installer adds both the skill and a thin Antigravity workflow. On the first run, Antigravity asks for target language and base language.

### Any other AI

If it supports Agent Skills, invoke the installed skill through that product's normal skill mechanism. If it does not, instruct the AI:

`Read anki-language/SKILL.md and follow it as the workflow contract for this material.`

## First-run configuration details

After the user answers the two language questions, the agent persists them with the included helper:

`python scripts/configure.py --target-name French --target-code fr --base-name English --base-code en --output ./anki-language.config.json`

The exact values are examples only; no language is preferred by the project.

To switch languages later, ask the AI to change the target/base configuration or run the helper again with new values.

## End-to-end workflow

1. User invokes the skill/workflow and provides material.
2. If this is the first run in the workspace, the AI asks for target language and base language and saves them.
3. AI inspects all source material.
4. AI selects only useful learning units.
5. AI assigns Reading, Listening, Production, or Pronunciation & Sounds.
6. AI decides whether audio/image actually adds value.
7. AI creates `card-plan.json`; missing worthwhile media is expressed with `audio_request` / `image_request`.
8. Media Enricher preserves existing media or generates/fetches missing media.
9. **Every actual audio/image is functionally decoded and hashed before it can continue.**
10. The resolved plan is delivered as `apkg`, `live`, or `both`.
11. APKG mode validates ZIP/media manifest/internal Anki database.
12. Live mode preflights notes, inserts them through AnkiConnect, then retrieves uploaded media and verifies SHA-256 + note-field references.
13. AI returns the resolved plan and delivery reports; failed validation is never reported as success.

## Deterministic build

Preferred complete pipeline:

`python scripts/run_pipeline.py /path/to/card-plan.json --delivery apkg --output /path/to/Language.apkg`

If media is already resolved and validated, direct APKG build remains available:

`python scripts/build.py /path/to/card-plan.resolved.json --output /path/to/Language.apkg`

The workflow checks JSON Schema, semantic rules, actual media decoding/hashes, media collisions, APKG ZIP/media manifest, embedded Anki SQLite database, note/card counts, and expected subdecks. Live delivery additionally validates the media after AnkiConnect upload.

## Repository architecture

- `anki-language/SKILL.md` — canonical provider-independent workflow.
- `anki-language/references/` — pedagogy, card selection, media, output contract.
- `anki-language/schemas/` — workspace configuration and card-plan schemas.
- `anki-language/scripts/` — configuration, media enrichment/validation, APKG build, AnkiConnect delivery, install, and validation scripts.
- `anki-language/assets/` — thin provider-specific assets such as the Antigravity workflow.
- `anki-language/agents/openai.yaml` — optional OpenAI/Codex interface metadata.
- `adapters/` — usage notes for specific AIs plus a generic adapter.
- `evals/` — behavioral evaluation cases.
- `tests/` — deterministic regression tests.

## AI-agnostic design rule

The canonical behavior must stay in `anki-language/SKILL.md`, `references/`, `schemas/`, and `scripts/`. Provider-specific files must remain thin adapters. A feature must not require one particular model/vendor unless it is explicitly optional.

## README maintenance rule

**Every repository change must update this README when the change affects behavior, installation, usage, architecture, configuration, dependencies, commands, outputs, or supported agents.**

To make that rule enforceable, pull-request CI checks that code/project changes include a `README.md` update. The README is treated as part of the product, not an afterthought.

## Validation and development

Validate the Agent Skill bundle:

`python anki-language/scripts/validate_skill.py anki-language`

Run tests:

`pytest -q`

## Output

A normal successful run produces:

- `card-plan.resolved.json`;
- validated local media when requested;
- `<TargetLanguage>.apkg` + report for `apkg`/`both`;
- live Anki note IDs + post-upload verification report for `live`/`both`.

Media is included only when useful, permitted, and functionally validated.