# 11 — Useful Add-ons and Extensions

Add-ons are optional programs that can modify arbitrary parts of Anki. Do **not** install or recommend many add-ons by default.

## Decision rule

Recommend an add-on only when:

1. native Anki does not already solve the need well;
2. the feature materially reduces friction or improves learning/automation;
3. current Anki-version compatibility has been checked;
4. it does not conflict with FSRS/scheduling;
5. the source is trustworthy enough for the user's risk tolerance.

Before giving an installation code, verify the current AnkiWeb listing.

## High-value candidates for this project

### AnkiConnect

- Purpose: local HTTP API for external automation.
- AnkiWeb code: `2055492159`.
- Useful for: querying collection data, creating/updating notes, managing decks/tags/media from external tools.
- Requirement: Anki must be running.
- Security: default localhost binding is safer; do not expose it to the network casually.
- This workflow's APKG builder does **not** require AnkiConnect.

Sources:
- https://ankiweb.net/shared/info/2055492159
- https://github.com/ankiultimate/anki-connect

### HyperTTS

- Purpose: generate/add TTS audio to notes/cards.
- AnkiWeb code: `111623432`.
- Modern successor to AwesomeTTS.
- Useful when native OS TTS is insufficient or persistent generated audio is desired.
- Service availability/cost/licensing varies by provider.

Sources:
- https://ankiweb.net/shared/info/111623432
- https://github.com/Vocab-Apps/anki-hyper-tts

### FSRS Helper

- Purpose: optional FSRS utilities such as load balancing, postpone/advance, easy days, sibling dispersion, flattening.
- AnkiWeb code: `759844606`.
- Native Anki already includes FSRS; the Helper is an optional companion, not a requirement.
- Its own documentation describes it as an added bonus and not something to use extensively.
- Avoid unrelated scheduling add-ons that modify intervals while FSRS is active.

Sources:
- https://ankiweb.net/shared/info/759844606
- https://github.com/open-spaced-repetition/fsrs4anki-helper

### Review Heatmap

- Purpose: visualize review activity/streaks.
- AnkiWeb code: `1771074083`.
- Useful for motivation/consistency; does not improve card scheduling by itself.
- Verify compatibility with the user's current Anki build before recommending because UI add-ons can lag behind Anki updates.

Sources:
- https://ankiweb.net/shared/info/1771074083
- https://github.com/glutanimate/review-heatmap

### Advanced Browser / maintained forks

- Purpose: additional sortable/searchable columns and browser tooling.
- Original listing historically used `874215009`.
- A 2026-maintained fork is listed as **Advanced Browser - mod kaiu 2026**, code `1334324384`.
- Verify which listing is current before recommending.

Source:
- https://forums.ankiweb.net/t/advanced-browser-mod-kaiu-2026-official-support/68382

### AnkiMorphs

- Purpose: language-learning morphology/frequency analysis and sentence-mining support.
- AnkiWeb code: `472573498`.
- Useful for some immersion/sentence-mining workflows, especially when prioritizing unknown morphs.
- Not required for ordinary language cards.

Sources:
- https://ankiweb.net/shared/info/472573498
- https://github.com/mortii/anki-morphs

### AJT Media Converter

- Purpose: convert/compress media formats such as WebP/AVIF/Opus.
- AnkiWeb code: `1151815987`.
- Useful for large media-heavy collections.
- Verify device/client support before choosing aggressive formats.

Source:
- https://ankiweb.net/shared/info/1151815987

### Forvo pronunciation downloaders

A current AnkiWeb listing in 2026 includes **Forvo Pronunciation Downloader (Fixed by Shige)**, observed with add-on id `1784714388`.

Use only when the audio source's license/API/terms permit the intended download, storage, and redistribution. A browser-playable pronunciation is not automatically permission to bundle it inside a shared APKG.

For automated language-deck generation, prefer:
1. user-provided audio;
2. clearly permitted native-source audio;
3. permitted TTS.

### Linux TTS player / gTTS

Anki's native `{{tts}}` tags depend on an available TTS player. Official Anki documentation notes that Linux does not ship an Anki TTS engine and points to a sample gTTS add-on (`391644525`). Current community alternatives also exist.

Use this only when native template TTS is desired; generated embedded audio is a different workflow.

## Add-ons usually unnecessary for this project

### AwesomeTTS

Its current AnkiWeb page recommends switching to HyperTTS and states HyperTTS is the modern successor.

### Image Occlusion Enhanced

Modern Anki (23.10+) has native Image Occlusion. Prefer native IO unless an add-on provides a specific missing feature that is verified to work on the user's version.

### Interval/ease manipulation add-ons under FSRS

Avoid by default. FSRS documentation warns that add-ons affecting intervals/scheduling can conflict with FSRS.

## Security and maintenance

Anki's manual explicitly warns that add-ons are programs downloaded from the internet and can execute code. Treat them like software, not harmless templates.

Before recommending an add-on:
- check the current AnkiWeb page;
- check supported Anki versions;
- check recent update/support status;
- review source repository when available;
- avoid abandoned add-ons when native functionality exists;
- prefer minimal add-on count.

## Live discovery

- Official directory: https://ankiweb.net/shared/addons
- Add-on support forum: https://forums.ankiweb.net/c/anki/add-ons/11
- Official add-on user docs: https://docs.ankiweb.net/manual/addons
