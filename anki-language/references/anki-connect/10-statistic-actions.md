# 10 — Statistics and Review-History Actions

Statistic actions expose review counts, collection stats, and review history.

Use them primarily for analytics/inspection.

`insertReviews` mutates review history and is high risk.

## Supported actions

| Action | Main documented params | Purpose |
| --- | --- | --- |
| `getNumCardsReviewedToday` | — | See upstream documentation. |
| `getNumCardsReviewedByDay` | — | See upstream documentation. |
| `getCollectionStatsHTML` | — | See upstream documentation. |
| `cardReviews` | — | See upstream documentation. |
| `getReviewsOfCards` | — | See upstream documentation. |
| `getLatestReviewID` | — | See upstream documentation. |
| `insertReviews` | — | See upstream documentation. |

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect. The local catalog is a curated snapshot, not a substitute for runtime capability discovery.

## Source

- https://github.com/ankiultimate/anki-connect/blob/master/README.md
