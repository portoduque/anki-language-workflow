# 16 — Language-Specific Rendering: RTL, Furigana, Fonts, Dictionaries

## Right-to-left languages

For Arabic, Hebrew, and other RTL languages:

- editing direction and review rendering are separate concerns;
- template HTML/CSS may require `dir="rtl"` or CSS `direction: rtl`;
- test punctuation and mixed LTR/RTL text on the target clients.

## Furigana / ruby text

Anki supports ruby-style annotations and template filters such as:
- `furigana`;
- `kana`;
- `kanji`.

This can be useful for Japanese reading cards.

Do not expose pronunciation hints on the front when the card is specifically testing reading of the unannotated form.

## Custom fonts

Fonts can be bundled as media for portability, but:
- increase package size;
- may behave differently across clients;
- require correct CSS/media naming;
- should be used only when needed for script rendering or deliberate design.

Prefer common system fonts when possible.

## Dictionary links

Templates can build dictionary lookup links from fields.

When field text may contain HTML formatting, use text-stripping filters as documented by Anki so formatting markup is not injected into the query.

External dictionary links are an optional convenience; they should not be required for a card to be answerable.

## Diacritics/case in typed answers

Anki supports typed-answer modes that can ignore diacritics and/or capitalization.

Use these only when accents/case are **not** part of the learning target.

## TTS locale

Choose the TTS locale/voice to match the target variety when pronunciation matters. Do not assume language code alone captures the intended accent/register.

## Sources

- https://docs.ankiweb.net/manual/templates/fields
- https://docs.ankiweb.net/manual/templates/styling
- https://docs.ankiweb.net/ankimobile/custom-fonts
- https://docs.ankidroid.org/manual.html
