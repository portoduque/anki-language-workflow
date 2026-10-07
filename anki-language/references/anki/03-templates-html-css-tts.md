# 03 — Templates, HTML, CSS, Field Replacement, TTS

## Field replacement

Use `{{FieldName}}` to insert a field.

Useful special fields include:

- `{{FrontSide}}`
- `{{Tags}}`
- `{{Type}}`
- `{{Deck}}`
- `{{Subdeck}}`
- `{{Card}}`
- `{{CardFlag}}`

Field names are case-sensitive.

## Conditional rendering

Use Anki conditional sections when optional data should appear only if a field is populated:

`{{#Field}}...{{Field}}...{{/Field}}`

Use negative conditionals when needed:

`{{^Field}}...{{/Field}}`

This is preferable to creating separate note types merely because one field is optional.

## Styling

Card templates are HTML/CSS. Prefer simple, responsive CSS.

Important considerations:

- mobile screens are narrower;
- images should have safe max dimensions;
- dark/night mode should remain legible;
- RTL languages may require `direction: rtl` or `dir=rtl`;
- bundled fonts require additional media handling and should not be added casually.

## Native TTS

Anki supports template TTS, for example:

`{{tts fr_FR:Field}}`

and multi-field/static-text TTS with `[anki:tts ...][/anki:tts]` in supported clients.

Native TTS depends on platform voices. Linux may require a TTS player/add-on.

For generated APKGs, native TTS is attractive when portability is acceptable and embedded audio is unnecessary. Embedded audio is preferable when pronunciation must be fixed/reproducible across devices.

## Hints

`{{hint:Field}}` can hide auxiliary information until requested.

Hints should not make retrieval artificially easy. This project prefers prompts that are clear by design rather than relying on optional hints to repair ambiguous cards.

## Type-answer

`{{type:Field}}` compares typed input with a field.

Modifiers documented by Anki include:
- `type:nc` — ignore diacritics;
- `type:ci` — ignore capitalization;
- combinations with cloze are possible.

Typed-answer comparison does not grade the card automatically; the learner still chooses Again/Hard/Good/Easy.

## Media in templates

Do not build dynamic media filenames like:

`[sound:{{Word}}.mp3]`

or

`<img src="{{Word}}.jpg">`

Anki recommends putting actual media references inside fields. Static template media should use filenames beginning with underscore so package/export tooling knows they are template resources.

## Sources

- https://docs.ankiweb.net/manual/templates/fields
- https://docs.ankiweb.net/manual/templates/styling
- https://docs.ankiweb.net/manual/templates/generation
