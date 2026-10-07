# 09 — Sync, Backups, Profiles, and Files

## AnkiWeb sync

Anki clients can sync collection data through AnkiWeb.

Card/note data and media sync are related but media transfer can continue separately and take longer.

When troubleshooting missing audio/images across devices, verify media sync completion before assuming the package or note is broken.

## Full syncs

Certain structural changes or conflicts may require a one-way upload/download. Treat full-sync decisions carefully because choosing the wrong direction can overwrite newer data.

## Backups

Anki creates automatic backups of collection data. Backups are an important recovery path for:
- accidental deletion;
- destructive note-type/template changes;
- scheduling mistakes;
- corrupted or unwanted imports.

Before recommending risky collection-wide changes, advise a backup.

## Profiles

Profiles separate collections/settings within one Anki installation. Sync behavior and add-on configuration may interact with profiles.

## Files

Anki's user-data directory contains collection/database, media, backups, add-ons, and configuration files.

Do not teach users to manually mutate the live SQLite database as a normal workflow. Prefer:
- Anki UI;
- supported import/export;
- AnkiConnect;
- add-on APIs;
- validated packages.

## Sources

- https://docs.ankiweb.net/manual/syncing
- https://docs.ankiweb.net/manual/backups
- https://docs.ankiweb.net/manual/profiles
- https://docs.ankiweb.net/manual/files
