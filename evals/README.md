# Skill behavior evals

These cases exercise the judgment layer that deterministic tests cannot fully measure.

Use them when changing `SKILL.md`, card-selection rules, or media rules. Run the same cases with the target agent/model and compare behavior against `expected`.

Key questions:

1. Does the skill trigger for relevant language-learning requests?
2. Does it avoid unnecessary cards?
3. Does it keep English as the support language by default?
4. Does it avoid ambiguous cloze prompts?
5. Does it place audio on the correct side for the trained skill?
6. Does it avoid revealing a minimal-pair/sound-discrimination answer on the front?

The deterministic CI suite separately validates package structure and scripts.