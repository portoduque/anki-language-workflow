# 10 — Statistics and Review-History Actions

Statistic actions expose review counts, collection stats, and review history.

Use them primarily for analytics/inspection.

`insertReviews` mutates review history and is high risk.

## Supported actions

| Action | Status | Main documented params | Purpose |
| --- | --- | --- | --- |
| `getNumCardsReviewedToday` | baseline | — | Gets the count of cards that have been reviewed in the current day (with day start time as configured by user in anki) |
| `getNumCardsReviewedByDay` | baseline | — | Gets the number of cards reviewed as a list of pairs of `(dateString, number)` |
| `getCollectionStatsHTML` | baseline | `wholeCollection` | Gets the collection statistics report |
| `cardReviews` | baseline | `deck`, `startID` | Requests all card reviews for a specified deck after a certain time. |
| `getReviewsOfCards` | baseline | `cards` | Requests all card reviews for each card ID. |
| `getLatestReviewID` | baseline | `deck` | Returns the unix time of the latest review for the given deck. 0 if no review has ever been made for the deck. |
| `insertReviews` | baseline | `reviews` | Inserts the given reviews into the database. Required format: list of 9-tuples `(reviewTime, cardID, usn, buttonPressed, newInterval, previousInterval, newFactor, reviewDuration, reviewType)` |

## Status policy

- **baseline**: present in the baseline public standard documentation snapshot.
- **extended / verify via `apiReflect`**: present in a newer upstream-tracking mirror but absent from the baseline mirror; verify the user's installed AnkiConnect before invoking.

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect.

## Sources

- https://github.com/ankiultimate/anki-connect
- https://github.com/JSchoreels/anki-connect
