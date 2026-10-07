# 03 — Card and Scheduling Actions

Card actions work on generated review cards, scheduling state, suspension, due dates, and review answers.

Use read-only inspection first. Scheduling mutations can materially change FSRS/review behavior and should require a clear user goal.

## Important behavior

- `findCards` uses normal Anki search syntax.
- `cardsInfo` returns rendered question/answer plus card metadata.
- `getIntervals` returns recent/all intervals; negative intervals represent seconds and positive intervals days in the documented API.
- `answerCards` grades cards with ease 1–4 (Again→Easy).
- `gradeNow` is present in the recent 2026 mirror and should be runtime-verified before use.
- `setDueDate`, `forgetCards`, `relearnCards`, `repositionNewCards`, and `setSpecificValueOfCard` can change scheduling materially.
- `setSpecificValueOfCard` is low-level and can damage scheduling/database semantics if used carelessly.

## Current catalog

| Action | Source signature | Risk |
| --- | --- | --- |
| `getEaseFactors` | `self, cards` | `read` |
| `setEaseFactors` | `self, cards, easeFactors` | `write` |
| `setSpecificValueOfCard` | `self, card, keys, newValues, warning_check=False` | `destructive` |
| `suspend` | `self, cards, suspend=True` | `write` |
| `unsuspend` | `self, cards` | `write` |
| `suspended` | `self, card` | `write` |
| `areSuspended` | `self, cards` | `read` |
| `areDue` | `self, cards` | `read` |
| `getIntervals` | `self, cards, complete=False` | `read` |
| `findCards` | `self, query=None, fields=None, noteFields=None` | `read` |
| `cardsToNotes` | `self, cards` | `read` |
| `cardsModTime` | `self, cards` | `read` |
| `cardsInfo` | `self, cards, fields=None, noteFields=None, retrieved_info_mode='ALL'` | `read` |
| `forgetCards` | `self, cards` | `destructive` |
| `relearnCards` | `self, cards` | `destructive` |
| `answerCards` | `self, answers` | `write` |
| `gradeNow` | `self, cards, ease` | `write` |
| `setDueDate` | `self, cards, days` | `destructive` |
| `repositionNewCards` | `self, orderedCardIds, startPosition, step, shift` | `destructive` |

For exact examples/edge cases, use the action's `source_anchor` in `ACTION_CATALOG.json` and confirm live support with `apiReflect`.
