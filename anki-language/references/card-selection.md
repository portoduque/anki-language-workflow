# Card Creation Rules

These rules are normative. They define what the workflow is allowed to turn into an Anki card.

## 1. Optimize for useful retrieval, not card count

The goal is the **smallest sustainable set of cards that produces useful retrieval practice**. **Cards must be quick to create, answer, and check during review.** Source length does not dictate card length: even if every supplied sentence is long, actively search within it for shorter, meaningful, independently valuable chunks before considering a full-sentence card.

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

### Reveal non-target dimensions when that isolates the skill

Do not accidentally test two skills at once merely because both pieces of information exist.

If a piece of information is **not** the retrieval target, it may be shown as support when doing so makes the intended task cleaner without giving away the answer.

Examples:
- a meaning/recognition task may show a reading/pronunciation aid when decoding is not being tested;
- a script-decoding/pronunciation task may show the meaning/context while hiding the reading aid;
- a Production task may show the semantic situation while hiding the target-language wording.

The same field can therefore be support in one card and the answer in another. Keep the front minimal and never reveal the actual target.

### Atomic does not mean isolated

A relationship or contrast can itself be **one primary retrieval target**.

Useful relational cards include:
- choosing between two confusable forms because the distinction is the knowledge being trained;
- identifying why one tense/aspect/preposition fits a specific context instead of its competitor;
- discriminating near-synonyms, collocations, or grammatical patterns when isolated cards are causing interference.

The card must still ask for one decision/relationship. Do not turn this into a "mega card" that demands several independent facts, conjugations, translations, or explanations at once.

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

### Choose grammar card format from retrieval intent

Before choosing cloze, direct Q/A, Reading, or Production for a grammar item, decide what the learner actually needs to retrieve:

- **rule recall** — state/identify a concise declarative rule itself;
- **recognition/discrimination** — recognize which structure/form/function is present or which competing form fits a context;
- **application/production** — select or produce the correct grammatical form in context.

Create a direct declarative grammar-rule card only when recalling the rule itself is independently useful. Do not memorize a rule merely because a textbook stated it.

Prefer contextual Reading/contrast cards when recognition or discrimination is the real target. Prefer constrained Production or a clear cloze when application is the real target.

Keep each card to one primary grammatical decision/form. Do not dump a full paradigm/table onto one card merely because the source presents the grammar that way.

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

For a learner who can comfortably understand the explanation, a concise **target-language definition** may replace or supplement a base-language gloss when it clarifies meaning without adding several new unknowns. Do not force monolingual definitions merely to avoid translation.

Do not create Reading cards for material the learner already understands reliably.

### Inspect polysemy before deciding the card

When a target word/expression appears to have multiple senses or productive uses, inspect several trustworthy contexts before selecting cards. The purpose of those extra contexts is to understand the target's semantic range, not to make the learner read a wall of examples on every review.

Prefer:

- **one primary sense/usage per card** when a single gloss would otherwise collapse several meanings into one overloaded answer;
- one clear primary context on the front;
- at most a small number of concise supporting examples on the back when they materially clarify usage;
- separate cards only for distinct, useful senses that deserve independent retrieval.

Do not require the learner to recall a dictionary-style list of several translations/senses on one card. Let context carry secondary nuance unless another sense independently deserves its own retrieval target.

Do **not** copy six or ten example sentences onto the front merely to show every possible use. Context exploration belongs mainly in analysis; review cards must remain fast.

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

### Production targets need a higher naturalness bar

When the learner is expected to actively reproduce a full sentence or chunk, prefer language that is **attested in user/native material** or independently verified as natural for the intended variety/register.

An AI-generated sentence may be used as a production target only when its naturalness and intended meaning have been validated sufficiently. If that confidence is missing, prefer an attested source sentence or a direct semantic production prompt instead of training a potentially unnatural phrase.

Reading/listening examples may tolerate generated support material more readily, but they still must be correct and natural enough not to teach bad language.

Choose between full-sentence production and guided expression production based on what the learner actually needs to retrieve.

### Keep Production focused and independently gradable

Before creating a Production card from a longer dialogue line, identify the **smallest useful phrase, collocation, or grammatical construction** the learner actually needs to retrieve. Prefer a short contextual prompt testing that expression rather than requiring a verbatim long sentence just because the source contains one.

When a full sentence itself is the real goal (e.g., a high-value practical utterance), keep it, but constrain the situation/register sufficiently and accept other natural correct formulations unless **exact wording** is explicitly the target. Do not silently grade a valid paraphrase as wrong. A card whose front could elicit many unrelated answers needs a better cue or should be omitted.

Do not require an exact full sentence when many natural translations would be equally correct unless the prompt explicitly constrains the wording.

### Semantic success over exact example reproduction

When a card's goal is to demonstrate **meaning or valid usage**, score the underlying retrieval, not whether the learner reproduced the stored example verbatim.

For example, if the task is to recall a valid context for a target word/form, another natural sentence that demonstrates the same meaning/form can count as correct.

Only require the exact stored wording when exact wording, collocation, spelling, morphology, or word order is itself the learning target.

This does **not** permit vague prompts. The front must still make clear what knowledge is being tested.

## 10. Pronunciation & Sounds cards

Create these only when sound is genuinely worth training.

Supported purposes:

- **pronunciation production:** written target -> learner says it -> audio/IPA on back;
- **minimal pair / sound discrimination:** audio on front -> identify which sound/word was heard -> written answer on back;
- **spelling-sound:** orthography -> sound or audio -> spelling, when the relationship is genuinely difficult/useful.

Never show the written answer on the front of a sound-discrimination/minimal-pair card.

**Answerability gate:** the front must contain enough information to know *what* to pronounce or discriminate before revealing the answer. A generic instruction such as "Say this naturally in French" with no written phrase and no front audio is not a valid card.

- For pronunciation production (`standard`) and spelling-to-sound (`spelling-sound`), display the written target on the front; use audio/IPA as feedback on the back.
- For audio identification (`minimal-pair`, `sound-discrimination`, `audio-to-spelling`), play audio on the front, keep the written answer on the back, and use a concise, task-specific prompt when needed.
- A pronunciation card must target a **real sound, stress, rhythm, linking, or spelling-sound difficulty**; do not convert every sentence of a dialogue into a redundant read-aloud card. A short difficult segment is usually better than a full multi-clause sentence.
- If the recording contains a longer utterance than the target, verify the alignment; provide a focused segment when the extra context interferes with the comparison.


For minimal-pair/sound-discrimination material, prefer recordings produced by the **same speaker/voice under similar recording conditions** when feasible. This reduces irrelevant speaker, loudness, microphone, and prosody cues so the learner must discriminate the target sound itself. Different speakers are acceptable when matched recordings are unavailable; do not block a useful card solely for that reason.

Do not generate large minimal-pair or spelling decks automatically. Create them when the language or learner difficulty makes them useful.

### Fade out spelling/sound scaffolding

Spelling and spelling↔sound cards are scaffolding, not a permanent quota.

Create them when orthography or grapheme↔sound mapping is still effortful. Once the learner can handle representative examples reliably and the cards have become trivial, stop generating new cards of that subtype unless a genuinely difficult spelling/sound pattern appears.

The Fluent Forever Gallery mentions roughly the first 100–300 words as a historical personal heuristic for this transition. Treat that as an example, **not a hard threshold**. The workflow should use demonstrated difficulty/automaticity instead of a fixed word count.

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

### Long-source to short-card chunk mining — mandatory selection step

**Treat each long sentence, paragraph, screenshot transcript, and dialogue turn as a source of candidate chunks, not a mandatory full-sentence flashcard.** This applies even if **all** of the user's material consists of long sentences. The workflow must actively identify shorter, reusable units in the supplied source before deciding which cards are worth creating.

For each long source passage:

1. **Understand the complete source first.** Preserve the intended meaning and speaker context; do not mechanically cut by punctuation, word count, or line length.
2. **Mine natural, meaningful candidates:** useful phrases, collocations, verb+preposition combinations, pragmatic expressions, and small grammatical frames with enough context to stand alone. A candidate may be a short phrase rather than a complete sentence.
3. **Prioritize the most useful candidates, not every fragment.** Choose zero, one, or several **distinct** chunks from the same long source only when each tests a separate worthwhile target. Skip obvious, already-known, incidental, ambiguous, and overlapping fragments; do not generate a card for every clause or word.
4. **Give each selected chunk its own short retrieval task.** Use a precise base-language meaning/situation for Production, an intelligible focused target for Reading, or an independently justified Listening/Pronunciation operation. Avoid asking for the entire original sentence when only the chunk is being learned.
5. **Retain just enough context.** Add a minimal contextual cue if the chunk alone has multiple meanings, and preserve the full source locator/verified example as optional back-side support. Do not paste the complete long sentence onto the front by default.
6. **Match media to the chosen chunk.** For long native recordings, use `audio_clip` with verified timestamps or conservative alignment so the audio on a short card does not play an unrelated full dialogue. Never guess cut boundaries.

**Illustrative extraction (not a quota):** From *« Vous pouvez me suivre, c'est à deux minutes d'ici. »*, the useful units might be *« vous pouvez me suivre »* (inviting someone to follow) and *« à deux minutes d'ici »* (distance/time from here). Produce **two separate short cards only if both are new and useful**. If just one is needed, create one; if both are already known, create none. Do not create a third card merely to memorize the full source sentence.

**Exceptions:** retain a complete sentence when its precise whole-utterance meaning, grammar, prosody, or conversational function is the actual learning target, and the resulting card is still quick to answer and verify. Never force all material into short fragments when splitting would damage the idiom, dependency, meaning, or naturalness.

**Fast-review gate:** Mentally simulate one review. Can the learner identify the task immediately, retrieve **one** target without reconstructing several clauses, and check it at a glance? If not, shorten/refocus the card, split into independently valuable candidates, use a clearer cue, or omit it. No universal word-count, number-of-chunks, or seconds-per-card quota applies; perceived effort and retrieval clarity matter more.

## 12. Sentence mining must be selective

Do not convert every sentence in the source into a card.

A mined sentence is a good candidate when it is:

- natural;
- understandable enough that the focus item stands out;
- useful or likely to recur;
- not overloaded with several unknown elements;
- a good context for one primary target.

Prefer sentences close to the learner's current level rather than dense sentences that require learning many things at once.

### Prefer near-i+1 sentence mining

A strong default is a sentence where the learner already understands essentially everything except the **one primary target**.

One incidental item that is immediately inferable and does not compete with the target may be acceptable, but do not use a sentence that requires learning several independent unknown words/forms at once.

If multiple unknowns each demand attention, choose a cleaner sentence, split the learning targets, or skip the sentence.

### Preserve comprehension flow before extraction

For continuous natural material such as a story, article, episode, video, or podcast, prefer a **meaning-first pass** before intensive lookup/card extraction when overall comprehension is still possible.

On that first pass:
- focus on understanding the message;
- do not stop for every unfamiliar item;
- note/mark only what is needed to avoid losing the source context.

On a later pass, or after the current passage/clip, inspect the unknowns and decide which ones deserve lookup and cards.

This is a preference, not a ritual. Skip the extra pass when the source is already short/isolated, when an unknown blocks comprehension, or when another workflow is clearly more efficient.

### Capture candidates first; commit to cards second

When useful material is encountered while reading, watching, listening, or studying, it is acceptable to collect words/phrases/sentences as **candidates** first and decide later which ones deserve cards.

Do not equate “unknown item encountered” with “create a card now.”

When practical, preserve enough local context (sentence, timestamp, paragraph, source) and batch the selection decision after the current passage/chapter/clip. This reduces interruption, preserves context, and gives the workflow enough evidence to discard trivial, redundant, low-frequency, or low-value items.

Immediate card creation is still fine when the item is clearly high-value and context is already sufficient.

### Account for expected natural re-encounter frequency

A useful candidate can become **more** valuable to SRS when natural exposure is unlikely to reinforce it again soon.

Consider expected natural re-encounter frequency together with usefulness, clarity/context, distinctness, and future review cost:

- a useful low-frequency or domain-specific item may deserve deliberate review precisely because it may not recur naturally for a long time;
- a very frequent/easy item that the learner already encounters constantly may not need a card if natural exposure is already reinforcing it sufficiently;
- rarity alone never justifies a card — obscure low-value material should still be skipped;
- do not use a fixed corpus-frequency cutoff or vocabulary-count threshold.

The question is not “Is this rare?” but:

> **Is this useful enough that natural exposure is unlikely to revisit it soon enough without deliberate review?**

### Clarify the target before scheduling it

A scheduled review should normally test retrieval of a target whose intended meaning, form, or usage has already been **clarified enough to encode**. Do not rely on repeated failed reviews to perform first-time semantic discovery.

Before promoting a candidate to a card:

- confirm the intended sense/form/context well enough that the answer is meaningful and gradeable;
- resolve ambiguity that would change what the learner is supposed to retrieve;
- allow first exposure or clarification immediately before card creation — prior mastery is not required;
- keep an unresolved item as a candidate when its meaning, register, transcription, or intended usage is still uncertain.

This does not ban beginner bootstrap material or require a separate pre-study ritual. It means the card should reinforce/retrieve a sufficiently understood target rather than asking the learner to discover what the card means during future reviews.

## 13. Images are selective

Use an image when it encodes or disambiguates meaning better than text, especially for concrete nouns, objects, actions, or visually distinctive concepts.

A genuine personal association supplied by the user may be used when it makes a concrete cue more distinctive or memorable. Never invent personal associations or add them merely to imitate a method.

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

## 15. Mnemonics are optional scaffolding

A mnemonic may be added when a word/form is genuinely hard to retrieve and a short association materially reduces learning friction.

Useful forms include:

- a verified cognate/etymological connection to a language the learner already knows;
- a keyword/sound-alike association;
- a concise image or verbal association.

Rules:

- **Do not add mnemonics to every card.** They are scaffolding for difficult items, not a quota.
- Put the mnemonic in secondary/back-side information so it does not replace the actual retrieval target.
- If claiming a real cognate, borrowing, or etymological relationship, verify it from a trustworthy source before presenting it as fact.
- If the link is merely an invented sound-alike/keyword, label it as a mnemonic rather than pretending it is etymology.
- Avoid a mnemonic that is more complicated, misleading, or memorable than the target in a way that creates interference.
- AI may propose mnemonic candidates, but it must not fabricate linguistic ancestry or false-friend relationships.

### Stable mnemonics for grammatical attributes

When an arbitrary lexical attribute repeatedly causes errors — especially grammatical gender or noun class — a **consistent concrete mnemonic code** may be used as secondary scaffolding.

Examples of possible codes include:
- a stable action/transformation assigned to each gender/class;
- a stable color or visual motif;
- another simple, user-understandable mapping.

Rules:
- prefer learning the real target form/chunk first (for example, determiner + noun) rather than memorizing an abstract label alone;
- keep the same mnemonic mapping consistent within the language/deck;
- use it only when the grammatical attribute is genuinely difficult or arbitrary enough to justify the extra cue;
- the mnemonic is secondary support, not the answer itself;
- do not create extra cards solely to display the mnemonic;
- avoid a visual/code that obscures the noun meaning or creates interference.

Do not hard-code one universal mapping such as “sparkling = feminine.” The workflow may adopt a mapping only when it is explicitly chosen/understood for that learner or material.

## 16. Avoid redundancy and interference

Do not create near-duplicate cards that test essentially the same retrieval.

Before making a second/third card from one dialogue line, articulate the **independent retrieval operation** for each skill (e.g. recognizing a phrase by ear vs actively producing a reusable chunk). If the alleged Pronunciation card simply asks to repeat the already-familiar whole sentence without a distinct difficulty, omit it. Repetition of the same text in different decks is not itself evidence of independent value.


Avoid introducing large batches of very similar new synonyms, near-synonyms, or semantic siblings when that would make them harder to discriminate.

If two cards are easily confused because the prompt does not distinguish them, improve the context instead of accepting ambiguity.

### Avoid learning the card wording instead of the language

Repeatedly seeing the same surface cue can make the learner recognize the **card** without being able to use the knowledge in a new context.

When flexible transfer matters:
- do not rely on a stereotyped preamble or accidental clue that uniquely predicts the answer;
- prefer natural contextual cues that require the intended semantic/grammatical distinction;
- when multiple cards are independently justified, vary the natural context or retrieval direction instead of creating near-duplicate copies;
- do not manufacture extra variants solely for volume.

The goal is retrieval of the language knowledge, not memorization of the card's visual/verbal fingerprint.

### Graduate redundant scaffolds when mastery evidence exists

When maintaining an existing collection and there is reliable evidence that a simple scaffold is already automatic, do not keep accumulating easier cards if a richer contextual card now covers the same retrieval adequately.

Prefer to retire/suspend the redundant scaffold **only when**:
- the learner/user or review history provides evidence of reliable mastery;
- the richer card genuinely covers the old learning target;
- removing the scaffold does not create a meaningful skill gap.

Do not infer mastery from card age alone, and do not delete user cards without permission.

### Review history is evidence, not an automatic diagnosis

When maintaining an existing live collection, use actual review history to decide **which cards deserve inspection**, not to let an agent silently rewrite the collection.

A repeated-failure pattern may come from:
- an ambiguous or overloaded prompt;
- insufficient context;
- confusable items;
- a missing prerequisite/bridge concept;
- malformed or incorrect content;
- a genuinely difficult but useful target;
- or a low-value item that no longer deserves review cost.

Inspect the actual card and source context before deciding what the pattern means. Prefer the smallest justified repair.

Start with read-only inspection. Any mutation of existing notes/cards or scheduling — rewriting fields, suspending/deleting cards, changing due dates, reprioritizing queues, or resetting learning state — requires a clear user goal and explicit approval for that action.

## 17. Target language-specific features selectively

Do not force the same lexical card pattern onto every language.

During source analysis, identify language-specific dimensions that materially affect comprehension or production, such as:

- grammatical gender or noun class;
- irregular/non-obvious plural formation;
- case, agreement, classifier/counter, or other inflectional choices;
- irregular tense/aspect/conjugated forms;
- script/orthographic variants;
- other high-value form distinctions that the learner actually needs.

A language-specific feature is a **candidate retrieval target**, not an automatic card.

Create a dedicated card only when that feature is useful, independently difficult or non-obvious enough to deserve review, and not already adequately covered. Keep one primary form/feature per card and reveal other known dimensions when that isolates the task.

Examples:
- test determiner+noun for a useful noun whose gender is genuinely difficult;
- test an irregular plural separately only when active recall of that plural matters;
- test one problematic verb form instead of dumping the entire paradigm onto one card;
- skip predictable/automatic morphology that adds little learning value.

Keep these cards inside the existing skill architecture (usually Reading or Production) and classify linguistic content with fields/tags rather than language-specific microdecks.

## 18. Store distinct linguistic data in distinct fields when useful

When a language item has distinct auxiliary information, keep it structured instead of collapsing everything into one generic notes blob.

Useful optional fields include:
- `reading` — pinyin, kana, romanization, or another reading aid;
- `variant` — alternate script/spelling/orthographic form;
- `grammar` — concise grammatical attribute such as gender, noun class, part of speech, or form.

Populate them only when they help the selected card. A populated field is **not** a reason to generate another card.

For writing-heavy languages, handwriting/written recall may be represented as a Production card when active written output is independently worth training. Do not create handwriting cards by default.

## 19. Keep answers concise and reviews fast

**Fast retrieval is a default requirement, not a cosmetic preference.** The front should not require memorizing a whole multi-clause sentence merely to demonstrate one phrase, and the back should let the learner judge the response at a glance. Prefer the shortest natural chunk that preserves the intended knowledge; the full source sentence can remain secondary context when useful. Do not create more chunks than the user's future review workload justifies.

The answer should expose the information needed to verify recall quickly.

Extra explanations belong below the answer and should remain concise.

For grammar, morphology, conjugation, or word-order cards, a brief back-side explanation may be added when it answers **why this form is correct** or prevents a predictable future confusion. Prefer one short rule or contrast over a pasted conjugation table or long AI-generated breakdown.

Do not turn the back of every card into a lesson, paragraph, or reference article.

## 20. Use the user's material as the primary source

Prefer the user's phrase, sentence, audio, image, or context when it is suitable.

Personally encountered material usually has stronger context than a random list or generic shared deck. Shared decks, frequency lists, and word lists may be mined as **candidate sources**, but their entries must still pass the same usefulness/context/review-cost test before becoming cards.

### Beginner bootstrap exception

For an **absolute beginner** who has too little comprehensible personal material to mine effectively, a well-constructed frequency/shared deck can be a useful bootstrap **candidate source**.

Before adopting items from it, inspect whether the source has useful fields such as target form, clear meaning/context, appropriate script/reading information, and trustworthy audio where relevant. Prefer a smaller/clearer representation over an overloaded note with many fields that do not serve the learner.

Do not blindly import the whole shared deck into the workflow. Select useful items, then progressively shift toward personally encountered/context-rich material as the learner gains enough language to mine it.

### Let candidate sources evolve with learner evidence

Do not treat one source strategy as optimal forever.

Prefer source candidates according to the learner's actual evidence and goals:

- when there is too little comprehensible personal material, vetted frequency/shared material may bootstrap candidates;
- once useful natural input becomes comprehensible, personally encountered/context-rich items should usually outrank generic lists;
- when listening is the evidenced bottleneck, audio-first source evidence may justify Listening cards;
- when real speaking/writing/domain activity exposes a recurring useful gap, that gap may become a candidate for targeted verification and Production.

Do not hard-code external roadmap phases or vocabulary-count milestones as mandatory switching thresholds.

### Output/domain gaps are candidates, not literal translations

If the learner repeatedly cannot express a useful idea during speaking/writing or within a target domain:

1. capture the intended meaning/situation/domain as a candidate;
2. verify a natural target-language expression for the intended variety/register from trustworthy/attested material when possible;
3. clarify the useful sense/form;
4. create a Production card only when the gap is useful enough to justify future review;
5. preserve the verified context/source when practical.

Do not turn a base-language thought directly into an unverified target-language Production answer.

Do not replace the user's material with generic material merely because generic examples are easier to generate.

It is acceptable to create a clearer example when the original material is unsuitable, but preserve the intended meaning and do not invent uncertain facts.

### Preserve precise source locators when available

When the source has a stable location, keep that locator in `source` so the learner can reopen the exact context later.

Useful examples include:
- a video/audio timestamp;
- page number;
- chapter/section;
- transcript segment;
- another stable source anchor.

Prefer a directly reopenable locator when possible. Do not invent precision the source does not provide. Prefer a directly openable URL, timestamp, page, or document/section reference over a screenshot filename that will not be included with the exported deck. Add an image only when the visual itself helps retrieval; do not embed screenshots solely to decorate provenance. A source locator is provenance/support, not an extra retrieval target.

## 21. Ask before guessing when ambiguity affects card quality

Stop and ask the user when uncertainty materially affects:

- the intended meaning;
- the correct target expression;
- whether an audio transcription is reliable;
- which language variety/register is intended;
- whether two plausible answers should be accepted;
- media rights/provenance;
- or another decision that changes the learning target.

Minor formatting decisions do not require interruption.

## 22. Decks classify skill; tags classify linguistic content

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

## 23. Creation effort must also earn its keep

Review cost is not the only cost. Card creation/customization also consumes time.

Do not spend disproportionate effort on decorative formatting, searching for the “perfect” image, collecting multiple redundant pronunciations, or writing long explanations when a simpler card would train the same retrieval just as well.

Use automation/media enrichment when it adds value, but keep the workflow biased toward **fast capture, selective enrichment, and more time learning/reviewing than decorating cards**.

## 24. Final decision test

Before accepting any card, verify all five:

1. **Useful:** Is this worth remembering?
2. **Distinct:** Does it test something not already adequately covered?
3. **Clear:** Can the learner know exactly what to retrieve?
4. **Atomic:** Is there one primary retrieval target?
5. **Fast:** Can the learner identify the target, answer, and verify it quickly **without reconstructing an unnecessarily long sentence**?

If any answer is no, revise or discard the card.
