# Card Creation Rules

These rules are normative. They define what the workflow is allowed to turn into an Anki card.

## 1. Optimize for useful retrieval, not card count

The goal is the **smallest sustainable set of cards that produces useful retrieval practice**.

For every source unit, the valid outcome is:

- **0 cards** when the item is already known, trivial, redundant, low-value, too ambiguous, or not worth future review cost;
- **1 card** when one retrieval skill is enough;
- **2+ cards** only when each card trains a genuinely different skill.

There is no quota and no requirement to fill every deck type.

Never create Reading + Listening + Production + Pronunciation versions automatically.

### Selective multi-card reuse of the same source

The **same source unit** — a sentence, word, expression, audio clip, image, or short passage — may legitimately generate cards in multiple skill decks.

Examples:

- one audio sentence may justify a **Listening** card because the learner needs to understand it by ear;
- the same sentence may also justify a **Production** card because a useful chunk should become actively retrievable;
- the same word may additionally justify a **Pronunciation & Sounds** card when its sound is genuinely difficult;
- the same written sentence may justify a **Reading** card when written recognition is independently useful.

This is not duplication when the cards require **different retrieval operations**.

However, each extra card creates future review cost. Before creating a sibling card from the same source, ask:

1. Does this card train a skill not already covered by the existing card(s)?
2. Is that skill useful enough to deserve repeated future reviews?
3. Does this card materially improve retention, comprehension, production, listening, or pronunciation?
4. Would removing this card leave a meaningful learning gap?

Create the additional card only when the answer is **yes** to the relevant questions.

The governing principle is:

> **Learning benefit must exceed future review cost.**

Do not maximize the number of cards extracted from a source. Maximize **memory efficiency per review minute**.

## 2. One primary retrieval target per card

Each card should answer one clear question:

> What exact knowledge or skill must the learner retrieve now?

Do not combine several unrelated questions, several independent blanks, or multiple concepts that could be reviewed separately.

A note may contain rich metadata, examples, audio, images, explanations, and provenance, but each generated card must still have one primary retrieval target.

## 3. Every front must be immediately understandable in a mixed review

The learner may review cards from many languages, topics, and skills in one session.

Every front must therefore provide short context that identifies at least:

- the configured **target language**; and
- the trained skill: **Reading**, **Listening**, **Production**, or **Pronunciation & Sounds**.

The context must orient the learner without revealing the answer.

The deterministic templates render this as:

`<TargetLanguage> — <Skill>`

Additional wording may identify the task or grammar function when it helps, but must not leak the target answer.

## 4. Never make the learner guess what the card author wanted

A correct card has a constrained retrieval target.

Bad:

`J'ai ___ rester chez moi.`

Many answers could fit. This tests guessing.

Good:

`Complete with the expression meaning "to end up doing something": J'ai ___ rester chez moi.`

The cue identifies the intended semantic target without revealing its target-language form.

This rule applies to cloze, fill-in-the-blank, grammar, vocabulary, chunks, collocations, and production cards.

## 5. Cloze is optional, never the default

Do not use cloze merely because Anki supports it.

Use a gap only when:

- the target is naturally tested inside a sentence;
- the prompt makes the intended answer unambiguous;
- the sentence provides useful context; and
- the card is faster or clearer than a direct production prompt.

Prefer guided production over blind cloze.

For grammar, a provided lemma or explicit function is often appropriate:

`Complete with the correct form of aller: Nous ___ au cinéma hier.`

## 6. Recognition and production are different skills

Do not create automatic reverse cards.

A recognition card is justified when the learner needs to understand the target form.

A production card is justified when the learner needs to actively retrieve/use the target form.

Create both only when both abilities are useful enough to justify separate future reviews.

Translation from the configured base language is allowed when it is the clearest and fastest cue. The workflow does not ban translation.

## 7. Reading cards

Use Reading when the target is written recognition/comprehension.

Typical front:

- natural target-language word, chunk, or sentence in sufficient context;
- short task/context label.

Typical back:

- meaning/explanation in the configured base language when useful;
- concise note about the focus item;
- optional audio if hearing the item adds value.

Prefer contextual words/chunks over decontextualized memorization when context helps.

Do not create Reading cards for material the learner already understands reliably.

## 8. Listening cards

Use Listening only when spoken comprehension is actually a learning target.

Front:

- audio first;
- no transcript or text that gives away what was said.

Back:

- target-language transcript;
- meaning/explanation in the configured base language when useful;
- concise notes only when they clarify a relevant sound, reduction, chunk, or structure.

If a long recording contains several useful utterances, segment it into meaningful clips when feasible. Do not make one listening card require recalling several unrelated sentences.

Audio priority is defined in `media.md`.

## 9. Production cards

Use Production when the learner should be able to actively say/write the target item.

Front:

- a precise situation, meaning, semantic cue, or constrained sentence in the configured base language;
- enough context to make the intended answer clear;
- never the target-language answer itself.

Back:

- target-language answer;
- natural full sentence when useful;
- audio normally on the back so it does not reveal the answer before retrieval;
- concise explanation only when needed.

Choose between full-sentence production and guided expression production based on what the learner actually needs to retrieve.

Do not require an exact full sentence when many natural translations would be equally correct unless the prompt explicitly constrains the wording.

## 10. Pronunciation & Sounds cards

Create these only when sound is genuinely worth training.

Supported purposes:

- **pronunciation production:** written target -> learner says it -> audio/IPA on back;
- **minimal pair / sound discrimination:** audio on front -> identify which sound/word was heard -> written answer on back;
- **spelling-sound:** orthography -> sound or audio -> spelling, when the relationship is genuinely difficult/useful.

Never show the written answer on the front of a sound-discrimination/minimal-pair card.

Do not generate large minimal-pair or spelling decks automatically. Create them when the language or learner difficulty makes them useful.

## 11. Prefer chunks, collocations, and useful patterns when they improve usable language

Words are not the only unit worth learning.

Prefer a chunk/collocation/expression over an isolated word when the useful knowledge is the combination itself.

Examples include:

- fixed expressions;
- verb + preposition patterns;
- common collocations;
- phrasal verbs;
- productive grammatical frames.

Do not split a useful chunk into isolated-word cards if doing so destroys the knowledge the learner needs.

## 12. Sentence mining must be selective

Do not convert every sentence in the source into a card.

A mined sentence is a good candidate when it is:

- natural;
- understandable enough that the focus item stands out;
- useful or likely to recur;
- not overloaded with several unknown elements;
- a good context for one primary target.

Prefer sentences close to the learner's current level rather than dense sentences that require learning many things at once.

## 13. Images are selective

Use an image when it encodes or disambiguates meaning better than text, especially for concrete nouns, objects, actions, or visually distinctive concepts.

An image may even replace a base-language translation when the concept is obvious from the image.

Do not add images merely to decorate cards.

Avoid ambiguous images for abstract connectors, grammar, or expressions when text/context is clearer.

## 14. Audio is selective and skill-dependent

Audio is not mandatory on every card.

Add it when it improves listening, pronunciation, or memory of a useful spoken form.

Preferred order:

1. original audio supplied by the user;
2. permitted native-speaker recording;
3. high-quality permitted TTS.

Do not scrape or embed media without permission. Preserve provenance when known.

## 15. Avoid redundancy and interference

Do not create near-duplicate cards that test essentially the same retrieval.

Avoid introducing large batches of very similar new synonyms, near-synonyms, or semantic siblings when that would make them harder to discriminate.

If two cards are easily confused because the prompt does not distinguish them, improve the context instead of accepting ambiguity.

## 16. Keep answers concise and reviews fast

The answer should expose the information needed to verify recall quickly.

Extra explanations belong below the answer and should remain concise.

Do not turn the back of every card into a lesson, paragraph, or reference article.

## 17. Use the user's material as the primary source

Prefer the user's phrase, sentence, audio, image, or context when it is suitable.

Do not replace it with generic material merely because generic examples are easier to generate.

It is acceptable to create a clearer example when the original material is unsuitable, but preserve the intended meaning and do not invent uncertain facts.

## 18. Ask before guessing when ambiguity affects card quality

Stop and ask the user when uncertainty materially affects:

- the intended meaning;
- the correct target expression;
- whether an audio transcription is reliable;
- which language variety/register is intended;
- whether two plausible answers should be accepted;
- media rights/provenance;
- or another decision that changes the learning target.

Minor formatting decisions do not require interruption.

## 19. Decks classify skill; tags classify linguistic content

Use the four skill subdecks:

- `01 Reading`
- `02 Listening`
- `03 Production`
- `04 Pronunciation & Sounds`

Use sparse tags for dimensions such as:

- `vocabulary`
- `chunk`
- `collocation`
- `grammar`
- `word-form`
- `word-order`
- `expression`
- `spelling`
- `minimal-pair`
- `sentence-mining`

Do not create many micro-decks for those categories.

## 20. Final decision test

Before accepting any card, verify all five:

1. **Useful:** Is this worth remembering?
2. **Distinct:** Does it test something not already adequately covered?
3. **Clear:** Can the learner know exactly what to retrieve?
4. **Atomic:** Is there one primary retrieval target?
5. **Fast:** Can the learner answer and verify it efficiently?

If any answer is no, revise or discard the card.
