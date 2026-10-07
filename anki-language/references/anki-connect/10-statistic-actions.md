# 10 — Statistics and Review-History Actions

These actions inspect review counts/history and can also insert raw review records.

## Read-only analytics

Use review/statistics actions for progress/behavior analysis when the user requests it.

## `insertReviews`

This is a high-risk review-history mutation. It accepts raw review tuples and can affect scheduling/statistics integrity.

Project rule: do not use `insertReviews` unless the user explicitly needs review-history insertion/migration and the semantics have been verified against the current Anki version.

## Complete current catalog

| Action | Exact source signature | Risk | Purpose |
| --- | --- | --- | --- |
| `getNumCardsReviewedToday` | `self` | `read` | Gets the count of cards that have been reviewed in the current day (with day start time as configured by user in anki) |
| `getNumCardsReviewedByDay` | `self` | `read` | Gets the number of cards reviewed as a list of pairs of `(dateString, number)` |
| `getCollectionStatsHTML` | `self, wholeCollection=True` | `read` | Gets the collection statistics report |
| `cardReviews` | `self, deck, startID` | `read` | Requests all card reviews for a specified deck after a certain time. |
| `getReviewsOfCards` | `self, cards` | `read` | Requests all card reviews for each card ID. |
| `getLatestReviewID` | `self, deck` | `read` | Returns the unix time of the latest review for the given deck. |
| `insertReviews` | `self, reviews` | `destructive` | Inserts the given reviews into the database. |
