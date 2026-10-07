# Skill behavior evals

These cases exercise the judgment layer that deterministic tests cannot fully measure.

Use them when changing `SKILL.md`, card-selection rules, media rules, or language configuration. Run the same cases with the target agent/model and compare behavior against `expected`.

Key questions:

1. Does the skill trigger for relevant language-learning requests?
2. On first use, does it ask for both target language and base language before analysis?
3. Does it avoid assuming any default language?
4. Does it avoid unnecessary cards?
5. Does it avoid ambiguous cloze prompts?
6. Does it use the configured base language for explanations and cues?
7. Does it place audio on the correct side for the trained skill?
8. Does it avoid revealing a minimal-pair/sound-discrimination answer on the front?

The deterministic CI suite separately validates package structure, scripts, installation paths, and arbitrary language pairs.