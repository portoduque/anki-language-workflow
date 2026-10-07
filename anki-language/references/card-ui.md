# Card UI — Anki Language v5

The workflow owns the visual presentation of every newly generated card. The goal is not decorative complexity; it is fast orientation, low visual friction, and a consistent review experience across desktop/mobile and light/night mode.

## Design principles

1. **Immediate orientation**
   - every front shows the target language and skill;
   - each skill has a stable accent color and label;
   - the retrieval target remains visually dominant.

2. **One hierarchy across all cards**
   - compact skill/language header;
   - large primary prompt/target;
   - optional cue/hint/media in secondary surfaces;
   - answer area with one dominant answer and clearly separated support blocks.

3. **Skill-specific UX without changing pedagogy**
   - Reading: target text is dominant on the front; base-language meaning is dominant on the answer.
   - Listening: audio is the dominant front interaction; transcript becomes the main answer.
   - Production: learner-facing prompt is dominant; the target-language production is the main answer.
   - Pronunciation & Sounds: prompt/audio is dominant; written target stays hidden on the front when it could leak the answer.
- Writing: short contextual sentence with one gap + native typed input; full sentence is shown on the answer.

4. **Support stays visually subordinate**
   - Focus, IPA, Reading, Variant, Grammar, Notes, and Source never compete with the primary retrieval target.
   - Source stays on the answer side only.

5. **Portable and inspectable**
   - plain Anki HTML/CSS/field replacement only;
   - no JavaScript;
   - no remote fonts, icons, or web assets;
   - local packaged media only.

6. **Accessibility and robustness**
   - responsive mobile layout;
   - night-mode palette;
   - `dir="auto"` and logical alignment for RTL/mixed-direction scripts;
   - large readable type and restrained line lengths;
   - color is never the only source of meaning: skill names remain textual;
   - no animation dependency.

## Visual language

### Shared surfaces

- neutral page background;
- elevated white/dark card surface;
- rounded 22px shell;
- thin border and restrained shadow;
- 5px skill accent bar;
- pill-shaped skill and language chips;
- soft support panels instead of dense text blocks.

### Skill accents

- Reading — indigo
- Listening — teal
- Production — amber
- Pronunciation & Sounds — rose
- Writing — blue

The same semantic accent remains recognizable in night mode with adjusted contrast.

## Front behavior

### Reading

Front hierarchy:
1. Reading + language header
2. “Read” stage label
3. large target text
4. optional cue
5. optional audio

### Listening

Front hierarchy:
1. Listening + language header
2. “Listen” stage label
3. optional cue
4. centered audio interaction

### Production

Front hierarchy:
1. Production + language header
2. “Produce” stage label
3. large learner-facing prompt
4. optional hint
5. optional image

### Pronunciation & Sounds

Front hierarchy:
1. Pronunciation & Sounds + language header
2. “Pronounce / identify” stage label
3. task-specific prompt
4. **written FrontCue** for `standard` (read-aloud) and `spelling-sound`, or **front audio** for `minimal-pair`, `sound-discrimination`, and `audio-to-spelling`
5. optional hint

The target/answer field is never inserted directly on pronunciation fronts. Only the deterministic `FrontCue` is populated when the written form is the prompt, so sound-identification cards still hide the answer. A generic "say this" prompt without a visible target or front audio is not a usable retrieval task.

### Writing

Front hierarchy:
1. Writing + target-language header
2. “Write the missing part” label
3. short natural sentence with exactly one visual gap; the rest stays visible
4. optional concise semantic/grammar cue
5. one native Anki `{{type:WritingAnswer}}` input — no custom JavaScript, cloze model, or auto-generated siblings

Back hierarchy:
1. `{{FrontSide}}` triggers Anki's typed-answer comparison
2. entire completed sentence and exact missing chunk
3. optional base-language meaning, grammar/notes and answer audio

The v5 design is shared with the other skills; Writing receives its own blue accent and readable typing input. This does not mutate existing note models. Typing input is not available in AnkiWeb/preview; representative reviews should be checked in the intended client.

## Answer behavior

The answer uses a second consistent shell below Anki's answer anchor.

- Reading promotes the base-language meaning first and keeps the original target as reference.
- Listening, Production, and Pronunciation promote the target-language answer first.
- Support metadata uses smaller bordered blocks.
- Audio/media remain centered.
- Notes use muted copy.
- Source is a small footer below a divider.

## Versioning rule

The visual redesign is introduced as **Anki Language v5** rather than mutating v4 in place.

This matters because:
- existing user cards keep their current styling;
- customized v4 templates are not overwritten;
- new workflow-generated cards receive the same v5 visual design automatically; Pronunciation uses a v6 note type for its internal FrontCue, while the other three skills stay v5;
- any future migration of old cards must be explicit and separate.

The v6 Pronunciation change does **not** restyle or migrate existing v5 Pronunciation cards. To fix already-imported v5 cards, regenerate/import corrected cards after reviewing potential identity/duplication implications, or edit them explicitly in Anki with user approval.

## Rendering validation

Deterministic tests check the HTML/CSS contract, but Anki itself remains the final rendering authority.

After this model migration, representative spot-checks should include:
- Reading, Listening, Production, and Pronunciation cards;
- light and night mode;
- desktop and mobile;
- long text;
- RTL or mixed-direction text when relevant;
- audio;
- image;
- empty optional fields.
