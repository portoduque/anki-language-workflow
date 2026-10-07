# 14 — Troubleshooting, Security, Performance, and Version-Sensitive Decisions

## Troubleshooting order

When a deck/package behaves unexpectedly:

1. identify Anki version and client/platform;
2. reproduce with add-ons disabled when relevant;
3. inspect note type/templates;
4. verify media filenames/references;
5. check package/import behavior;
6. check sync/media sync state;
7. consult current official FAQ/manual page;
8. only then use community workarounds.

## Add-ons

Add-ons can break after Anki updates because they may modify internal behavior.

If an issue starts after an Anki update:
- update add-ons;
- disable suspicious add-ons;
- test without add-ons;
- check author/support thread.

## Media problems

Common causes:
- file not packaged;
- wrong basename;
- filename collision;
- template-generated dynamic media filename;
- incomplete media sync;
- unsupported format/client;
- deleted/orphaned media.

## Template problems

Check:
- exact field-name capitalization;
- special/reserved fields;
- invalid HTML/CSS;
- front template accidentally revealing answer;
- conditional sections;
- missing fields;
- unsupported JS/client-specific behavior.

## Import problems

Check:
- UTF-8 encoding;
- separator/column mapping;
- note type;
- deck override;
- duplicate matching;
- GUID/first-field behavior;
- HTML import option;
- media files/references.

## Scheduling/FSRS problems

Check:
- whether forgotten cards are graded Again rather than Hard;
- current FSRS parameters;
- last optimization;
- desired retention;
- incompatible scheduling add-ons;
- excessive manual rescheduling;
- different material mixed into one preset when difficulty differs drastically.

## Backups before risky operations

Before:
- mass note-type conversion;
- collection-wide find/replace;
- rescheduling large sets;
- importing a collection package;
- changing many templates programmatically;

ensure a usable backup exists.

## Version-sensitive policy

For any claim involving:
- “current Anki”;
- supported add-on versions;
- FSRS behavior;
- release-specific options;
- mobile compatibility;
- package behavior changes;

consult current official docs/release notes instead of relying solely on this local summary.

Official exhaustive index:
- https://docs.ankiweb.net/llms.txt

Release notes:
- https://docs.ankiweb.net/releases/changes/changes/intro

Known issues:
- https://docs.ankiweb.net/releases/changes/known-issues

## Security

Treat:
- add-ons as executable code;
- imported packages as untrusted content;
- external media as potentially licensed/restricted;
- AnkiConnect/network APIs as local services that should not be unnecessarily exposed.

## Sources

- https://docs.ankiweb.net/manual/troubleshooting
- https://docs.ankiweb.net/faqs/intro
- https://docs.ankiweb.net/manual/addons
- https://docs.ankiweb.net/manual/backups
