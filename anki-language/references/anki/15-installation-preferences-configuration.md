# 15 — Installation, Preferences, Interface, and General Configuration

## Installation and upgrades

Use the official platform-specific documentation for current installation instructions:

- Windows;
- macOS;
- Linux.

Do not hardcode old installer steps into automation because packaging/distribution can change across releases.

Official discovery:
- https://docs.ankiweb.net/llms.txt

## Preferences vs deck options

Keep these concepts separate:

- **Preferences** affect application-wide/user-interface behavior.
- **Deck Options / presets** affect scheduling/study behavior.

For scheduling questions, consult the FSRS/deck-options reference rather than assuming a Preferences setting controls it.

## Common preference areas

Depending on Anki version, preferences can include behavior related to:
- interface;
- editing;
- reviewing;
- scheduling/display;
- audio replay;
- backups/sync;
- language/interface.

Always verify current labels/locations in the official Preferences page when giving exact UI instructions.

## Interface language

Changing Anki's interface language is different from:
- target language;
- base language;
- card template language;
- TTS voice.

Do not conflate them.

## Keyboard shortcuts

Shortcuts can change or be overridden by add-ons/platform behavior. For a current shortcut, consult the current manual/UI rather than relying on memorized old shortcuts.

## Updates and add-ons

Before a major Anki upgrade, users with important add-ons should verify compatibility. Anki add-ons can break when internal APIs/UI change.

## Sources

- https://docs.ankiweb.net/manual/preferences
- https://docs.ankiweb.net/manual/getting-started
- https://docs.ankiweb.net/manual/platform/intro
- https://docs.ankiweb.net/llms.txt
