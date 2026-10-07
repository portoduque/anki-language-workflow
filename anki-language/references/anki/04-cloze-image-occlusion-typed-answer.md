# 04 — Cloze, Image Occlusion, and Typed Answers

## Cloze

Anki's Cloze note type uses syntax like:

`{{c1::answer}}`

Multiple deletions can be created on one note.

Technical capability does **not** override this project's pedagogical rule: blind or ambiguous cloze is forbidden. A cloze must still clearly constrain the intended retrieval target.

Use cloze when:
- the sentence itself is important context;
- the hidden item is the natural retrieval target;
- the cue/lemma/function makes the answer sufficiently constrained.

Avoid cloze when:
- many answers fit;
- the learner must infer what the card author intended;
- a direct production prompt is clearer.

## Image Occlusion

Anki 23.10+ includes native Image Occlusion.

It can mask regions using shapes and supports modes such as hiding multiple regions while asking for one.

Use it for material where spatial/visual position is the learning target, such as:
- anatomy;
- maps;
- diagrams;
- labeled equipment;
- UI screenshots.

For normal language vocabulary, prefer ordinary image cards unless spatial masking itself adds learning value.

## Typed answers

Typed-answer cards are useful when exact spelling/form matters.

Examples:
- difficult orthography;
- inflected forms;
- short production;
- audio → spelling.

Do not use typed answers for long free-form sentences with many equivalent valid outputs.

## Source

- https://docs.ankiweb.net/manual/editing
- https://docs.ankiweb.net/manual/templates/fields
