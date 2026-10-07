# 13 — Platforms, Mobile, and Compatibility

## Ecosystem

The official Anki ecosystem includes:
- Anki Desktop;
- AnkiWeb;
- AnkiMobile (iPhone/iPad);
- AnkiDroid (Android, separately maintained).

## Cross-platform card templates

When generating decks intended for multiple clients:

- keep HTML/CSS simple;
- avoid unsupported browser APIs;
- test responsive layout;
- avoid desktop-only assumptions;
- verify custom fonts/media;
- consider RTL text;
- avoid JavaScript unless the feature genuinely requires it.

## TTS compatibility

Native Anki `{{tts}}` support depends on client/platform voices.

Desktop:
- Windows/macOS can use OS voices;
- Linux generally requires a TTS player/add-on.

AnkiMobile supports template TTS.

AnkiDroid supports TTS but has its own implementation and configuration details. If exact cross-device pronunciation is required, embedded audio is more predictable than relying on local voices.

## FSRS compatibility

Official desktop documentation states native FSRS support in modern Anki, AnkiWeb, AnkiMobile, and AnkiDroid 2.17+.

If a user has an older client, verify compatibility before enabling/changing FSRS.

## Media

Media should be synchronized/downloaded on all clients. A note can arrive before all media completes syncing.

## Custom templates

AnkiDroid documents custom card layouts and generally follows Anki template concepts, but complex JavaScript/CSS may behave differently.

## Platform-specific documentation

Official index:
- https://docs.ankiweb.net/llms.txt

AnkiMobile:
- https://docs.ankiweb.net/ankimobile/intro

AnkiDroid:
- https://docs.ankidroid.org/manual.html

## Project rule

Generated APKG templates should target the common denominator unless the user explicitly requests platform-specific behavior.
