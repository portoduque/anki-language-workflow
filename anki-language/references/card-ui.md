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
3. prompt
4. optional hint
5. optional front audio

The target field is still not rendered directly on pronunciation fronts.

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
- new workflow-generated cards receive the v5 UI automatically;
- any future migration of old cards must be explicit and separate.

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
