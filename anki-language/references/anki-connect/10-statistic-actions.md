# 10 — Statistics and Review-History Actions

These actions inspect review counts/history and can also insert raw review records.

## Read-only analytics

- `getNumCardsReviewedToday`
- `getNumCardsReviewedByDay`
- `getCollectionStatsHTML`
- `cardReviews`
- `getReviewsOfCards`
- `getLatestReviewID`

Use these for progress/behavior analysis when the user requests it.

## `insertReviews`

High-risk mutation of review history. It accepts raw review tuples and can affect scheduling/statistics integrity.

Project rule: do not use `insertReviews` unless the user explicitly needs review-history insertion/migration and the semantics have been verified against the current Anki version.

## Current catalog

| Action | Source signature | Risk |
| --- | --- | --- |
| `getNumCardsReviewedToday` | `self` | `read` |
| `getNumCardsReviewedByDay` | `self` | `read` |
| `getCollectionStatsHTML` | `self, wholeCollection=True` | `read` |
| `cardReviews` | `self, deck, startID` | `read` |
| `getReviewsOfCards` | `self, cards` | `read` |
| `getLatestReviewID` | `self, deck` | `read` |
| `insertReviews` | `self, reviews` | `destructive` |
