# 07 — Scheduling, Study Options, and FSRS

## Source-of-truth rule

Scheduling advice is version-sensitive. Prefer the **current official Anki documentation and the learner's own review data** over fixed presets copied from videos, old guides, or another person's collection.

Start close to current defaults unless there is a concrete reason to change them, and understand the option before changing it.

## Answer buttons

The learner grades recall with:

- **Again** — the information was not recalled correctly.
- **Hard** — the information was recalled correctly, but with substantial hesitation/effort.
- **Good** — the information was recalled correctly with ordinary mental effort.
- **Easy** — the information was recalled correctly with little or no effort.

With FSRS, **Hard is a passing grade**. If the answer was forgotten, use **Again**, not Hard. Consistently using Hard for forgotten cards teaches FSRS the wrong signal and can produce intervals that are too long.

## FSRS

Modern Anki includes FSRS natively.

Important official guidance:

- FSRS can be enabled globally;
- all clients used for the same collection must support FSRS;
- learning/relearning steps should generally be shorter than one day and completable on the same day;
- keep short-term steps minimal rather than copying a universal sequence;
- optimize parameters from the learner's own review history;
- do not manually copy FSRS parameters from someone else;
- desired retention is the most important user-facing FSRS setting;
- default desired retention is around 0.90;
- workload rises sharply as desired retention approaches 1.0;
- keeping desired retention below about 0.97 is generally recommended;
- parameter optimization does not need to be run constantly; monthly is enough for most users.

When review histories differ greatly by material difficulty, separate presets may be useful.

### Desired retention should be workload-aware

Do not hard-code a universal desired-retention value merely because a creator uses it.

The default around 0.90 is a reasonable starting point. When current Anki offers **Help Me Decide / simulator** functionality, prefer the learner's realistic review-time/reviews-per-day budget and the simulated retention↔workload trade-off.

## Learning/relearning steps

Do not prescribe a universal `10m`, `1m 10m`, or other copied sequence.

For FSRS:

- keep steps short and below one day;
- use the current official defaults/guidance unless there is a learner-specific reason to change them;
- understand that short-term scheduling behavior has changed across Anki versions.

A YouTube recommendation to delete the one-minute step or keep only ten minutes is therefore a **personal preset**, not a project rule.

## New cards and review limits

New cards create future workload.

Official Anki documentation notes that studying about 20 new cards every day can lead to roughly 200 reviews/day as an illustrative workload example. This is **not** a required 10× ratio.

Project guidance:

- choose new-card intake based on sustainable review workload;
- reduce new cards when review burden grows too high;
- if there is a meaningful review backlog, prioritize catching up before introducing more new cards;
- do not prescribe fixed `20`, `50`, or other universal new-card limits.

### Maximum reviews/day

A review limit can smooth occasional workload peaks. Setting it extremely high removes that protection and may be appropriate for a learner who deliberately wants to clear every due card, but it is not a universal recommendation.

Do not hard-code `9999` or any other effectively unlimited value.

## Display order

Do not copy a creator's display-order preset without checking current Anki semantics.

Current official guidance:

- **Due date, then random** is the default/recommended review sort when the learner is up to date or has only a small backlog.
- For a large backlog, the legacy idea of showing cards most likely to be forgotten first maps under FSRS to **Ascending retrievability** — lower recall probability first.

Do **not** claim that **Descending retrievability** prioritizes the cards most at risk of forgetting; that direction does the opposite.

New/review/interday ordering is preference- and workflow-sensitive. Keep defaults unless there is a concrete reason to change them.

## Burying and siblings

In Anki, sibling burying applies to **multiple cards generated from the same note**, such as a forward/reverse pair or adjacent cloze cards.

This distinction matters for this repository:

- the current builder creates **one Anki note per planned card**;
- a Reading card and a Production card derived from the same source item are therefore separate notes;
- native Anki sibling-burying settings will **not automatically space those cross-skill cards**.

Burying can still be useful for true siblings in user-created/external note types, but do not claim it solves cross-skill spacing for this workflow.

If future versions intentionally group multiple generated cards under one note, revisit this rule and add regression tests for sibling behavior.

## Easy Days

Easy Days shifts future due dates by a small amount so selected weekdays can be lighter. It **redistributes** workload; it does not eliminate the underlying reviews.

Do not interpret a low/minimum day as "zero Anki work" or as a replacement for sustainable new-card intake.

## Leeches

Repeated failures are a signal to inspect the card, not merely to keep drilling it forever.

When a card becomes a leech or repeatedly fails:

- check whether the prompt is ambiguous;
- simplify or split overloaded knowledge;
- add missing context;
- verify the answer/media;
- suspend/delete low-value cards when appropriate.

## Add-on compatibility

Scheduling/interval-changing add-ons can conflict with FSRS. Before recommending one, verify current compatibility.

## Rescheduling

Changing FSRS settings does not need to immediately reschedule every existing card. Immediate rescheduling can create a large due-card spike.

## Statistics

With FSRS enabled, true retention over meaningful time windows should roughly track desired retention. Monthly data is more informative than a single day.

## Sources

- https://docs.ankiweb.net/manual/deck-options
- https://docs.ankiweb.net/manual/studying
- https://docs.ankiweb.net/manual/stats
- https://docs.ankiweb.net/faqs/frequently-asked-questions-about-fsrs
