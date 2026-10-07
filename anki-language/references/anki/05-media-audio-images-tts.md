# 05 — Media, Audio, Images, and TTS

## Media references

Anki field content commonly references:

- images: `<img src="file.jpg">`
- audio: `[sound:file.mp3]`

For text-file imports, referenced files must already be present in the collection media folder.

For APKG packages, media should be bundled in the package and referenced by exact basename.

## Filename rules for automation

For deterministic package generation:

- use unique basenames;
- avoid collisions;
- keep filenames portable across operating systems;
- avoid unnecessary subdirectories;
- validate every reference before package delivery.

This project already performs basename collision and missing-media validation.

## Audio choice

Project priority:

1. original user-provided audio;
2. permitted native-speaker recording;
3. permitted high-quality TTS;
4. native Anki template TTS when appropriate.

Use embedded audio when exact sound should travel with the deck. Use native TTS when dynamic platform speech is acceptable and smaller packages are preferred.

## Image choice

Use images when they encode meaning or useful context. Avoid decorative images and ambiguous representations.

## Media checking

Anki provides media checking/cleanup functionality. Static template media should be named with an underscore prefix when necessary so Anki recognizes it as template media during export/checking.

## Cross-device considerations

Media sync can take longer than text/card sync. Missing media may reflect incomplete sync rather than missing notes.

## Sources

- https://docs.ankiweb.net/manual/media
- https://docs.ankiweb.net/manual/importing/text-files
- https://docs.ankiweb.net/manual/templates/fields
- https://docs.ankiweb.net/manual/syncing
