# 03 — Card and Scheduling Actions

Card actions work on generated review cards, scheduling state, suspension, due dates, positions, and review answers.

Use read-only inspection first. Scheduling mutations can materially change FSRS/review behavior and should require a clear user goal.

## Important behavior

- `findCards` uses normal Anki search syntax.
- `cardsInfo` returns rendered question/answer plus card metadata.
- `getIntervals` returns recent/all intervals; documented negative intervals are seconds and positive intervals are days.
- `answerCards` grades cards with ease 1–4 (Again→Easy).
- `gradeNow` and `repositionNewCards` are in the recent 2026 mirror and are marked version-sensitive; verify them with `apiReflect` before use.
- `setDueDate`, `forgetCards`, `relearnCards`, `repositionNewCards`, and `setSpecificValueOfCard` can change scheduling materially.
- `setSpecificValueOfCard` is low-level and can damage scheduling/database semantics if used carelessly.

## Complete current catalog

| Action | Exact source signature | Risk | Purpose |
| --- | --- | --- | --- |
| `getEaseFactors` | `self, cards` | `read` | Returns an array with the ease factor for each of the given cards (in the same order). |
| `setEaseFactors` | `self, cards, easeFactors` | `write` | Sets ease factor of cards by card ID; returns `true` if successful (all cards existed) or `false` otherwise. |
| `setSpecificValueOfCard` | `self, card, keys, newValues, warning_check=False` | `destructive` | Sets specific value of a single card. |
| `suspend` | `self, cards, suspend=True` | `write` | Suspend cards by card ID; returns `true` if successful (at least one card wasn't already suspended) or `false` otherwise. |
| `unsuspend` | `self, cards` | `write` | Unsuspend cards by card ID; returns `true` if successful (at least one card was previously suspended) or `false` otherwise. |
| `suspended` | `self, card` | `write` | Check if card is suspended by its ID. |
| `areSuspended` | `self, cards` | `read` | Returns an array indicating whether each of the given cards is suspended (in the same order). |
| `areDue` | `self, cards` | `read` | Returns an array indicating whether each of the given cards is due (in the same order). |
| `getIntervals` | `self, cards, complete=False` | `read` | Returns an array of the most recent intervals for each given card ID, or a 2-dimensional array of all the intervals for each given card ID when `complete` is `true`. |
| `findCards` | `self, query=None, fields=None, noteFields=None` | `read` | Returns an array of card IDs for a given query. |
| `cardsToNotes` | `self, cards` | `read` | Returns an unordered array of note IDs for the given card IDs. |
| `cardsModTime` | `self, cards` | `read` | Returns a list of objects containings for each card ID the modification time. |
| `cardsInfo` | `self, cards, fields=None, noteFields=None, retrieved_info_mode='ALL'` | `read` | Returns a list of objects containing for each card ID the card fields, front and back sides including CSS, note type, the note that the card belongs to, and deck name, last modification timestamp as well as ease and interval. |
| `forgetCards` | `self, cards` | `destructive` | Forget cards, making the cards new again. |
| `relearnCards` | `self, cards` | `destructive` | Make cards be "relearning". |
| `answerCards` | `self, answers` | `write` | Answer cards. |
| `setDueDate` | `self, cards, days` | `destructive` | Set Due Date. |
| `gradeNow` | `self, cards, ease` | `write` | Grades cards immediately using the same rating scale as review answers. |
| `repositionNewCards` | `self, orderedCardIds, startPosition, step, shift` | `destructive` | Repositions eligible new cards using Anki native reposition logic while preserving caller order. |

For full examples/edge cases, use the action's `source_anchor` in `ACTION_CATALOG.json` and confirm live support with `version` + `apiReflect`.
