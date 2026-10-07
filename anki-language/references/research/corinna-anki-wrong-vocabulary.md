# Corinna Languages — “You’re using Anki wrong (learn vocabulary faster)” — Selective Adaptation Note

Source analyzed:

- YouTube: https://youtu.be/yOQR1XYC--o
- Channel: Corinna Languages
- Published: 2026-03-24
- Duration: ~12:16

The complete spoken transcript was reviewed from start to finish, including:

- choosing interesting comprehensible material;
- first-pass familiarization before deeper vocabulary work;
- capturing unknown words from books/videos/podcasts;
- criticism of isolated translation-only cards;
- Fluent Forever image-based vocabulary cards;
- personal photos/associations;
- forward + reverse cards;
- original sentence/context fields;
- pronunciation audio / Forvo;
- grammatical-gender imagery;
- mobile review / consistency advice.

## What already matched this project

### Personal/context-rich source material

The video prefers vocabulary encountered in meaningful books, shows, podcasts, or videos instead of random lists.

Already covered:
- user/source material is preferred;
- unknown items are candidates, not automatic cards;
- sentence/source/timestamp context is preserved;
- near-i+1 mining is preferred.

### Personal images and associations

Already covered:
- concrete images are useful when they improve retrieval;
- genuine user-supplied personal associations may be used;
- decorative/ambiguous images are rejected.

### Audio when pronunciation matters

Already covered:
- audio is selective;
- original/source audio is preferred, then permitted native audio, then validated TTS;
- Forvo is optional, not a core automation dependency.

### Context sentence on the card

Already covered:
- preserve useful source context;
- one primary retrieval target;
- extra examples remain secondary.

## Useful ideas adopted

### 1. Preserve a meaning-first pass before intensive extraction

The video first reads/watches the material for familiarity and comprehension, then returns for a deeper pass where unknown words are marked and investigated.

This is useful because card extraction should not constantly interrupt meaningful language exposure.

Adaptation:
- for continuous natural input (story/article/video/podcast), prefer a first **meaning-first** pass when comprehension remains possible;
- do not stop for every unfamiliar item;
- on a later pass or after the passage/clip, inspect unknowns and decide which deserve lookup/cards;
- skip this extra pass when the source is already short/isolated or an unknown blocks comprehension.

This is a workflow preference, not a rigid “always read twice” rule.

Supporting evidence:
- L2 reading research has found that indiscriminate dictionary lookup can be detrimental and that selective lookup based on relevance/context is more effective;
- dictionary search itself can add extraneous cognitive load and disrupt reading flow.

References:
- Prichard (2021), TESOL Quarterly: https://doi.org/10.1002/tesq.3005
- Prichard (2008), Reading in a Foreign Language: https://eric.ed.gov/?id=EJ815122
- Dang et al., RoLo dictionary-interface work on lookup cognitive load.

### 2. Stable concrete mnemonic coding for grammatical gender/noun class

The video demonstrates a Fluent Forever technique that assigns a consistent action to each grammatical gender, then imagines the noun image undergoing that action.

The exact mapping is arbitrary; the useful principle is **recoding an abstract grammatical tag into a stable concrete cue**.

Adaptation:
- allow a stable action/color/visual motif for difficult arbitrary attributes such as grammatical gender or noun class;
- keep the actual linguistic form primary (for example determiner + noun), not the mnemonic label;
- use the mnemonic only when the attribute genuinely causes learning difficulty;
- keep the mapping consistent within the language/deck;
- do not create extra cards just to show the mnemonic;
- do not hard-code one universal mapping for all learners.

Evidence:
- Desrochers, Gélinas & Wieland (1989) found a modified keyword method with concrete recoding improved acquisition of German noun meaning and gender.
- Desrochers, Wieland & Coté (1991) found that explicit concrete recoding incorporated into imagery facilitated grammatical-gender recall.
- Santos (2015) found image-based gender coding produced the best observed results among several mnemonic conditions for German noun gender.

This supports the mechanism without requiring Corinna/Wyner’s specific “sparkling/exploding/freezing” choices.

## Ideas intentionally NOT adopted

### Translation ban

The video presents avoiding native-language translation as a central benefit.

Not adopted:
- the configured base language remains valid when it is the clearest/fastest cue;
- translation is a tool, not a default requirement or a forbidden technique;
- image-only encoding is unsuitable for many abstract words and expressions.

### Google Images for every vocabulary item

Not adopted:
- images remain selective;
- the automated pipeline uses licensed/provenance-aware image sources;
- image search does not justify adding visual media to abstract items where text/context is clearer.

### Automatic forward + reverse cards for every word

The video explicitly recommends forward and reverse generation.

Not adopted:
- recognition and production are distinct;
- create both only when both are independently useful;
- every additional card must justify future review cost.

### User-generated example sentences without naturalness validation

The video suggests creating your own sentence and adding it to the card.

Adaptation:
- this can be a useful exercise outside the card contract;
- if that sentence becomes an exact Production target, it must pass the project’s stronger naturalness/register validation rule.

### Forvo / Forvo add-on as primary automation

Not adopted. Existing provider-independent media pipeline remains preferable.

### Fixed “review five words on hard days” habit trick

Potentially useful motivational advice, but outside card-generation behavior.

### Fixed review-duration expectations

The speaker reports ~10–20 minute review sessions personally.

Not adopted as a workload target or scheduling rule.

### “Images are always remembered better than words”

The video uses broad imagery-memory claims.

The project keeps the narrower evidence-aligned rule:
- imagery can help concrete vocabulary and some arbitrary grammatical features;
- it is not universally superior for every language target.

## Net changes justified by this source

1. Add **meaning-first source pass before intensive vocabulary extraction** for continuous natural material when practical.
2. Add **stable concrete mnemonic coding for difficult grammatical gender/noun-class attributes**, with the real linguistic form kept primary.
3. Explicitly reject universal gender-action mappings, automatic reverse cards, and image/translation absolutism.

No schema, builder, deck architecture, media provider, installer, or AnkiConnect implementation change is justified by this source.
