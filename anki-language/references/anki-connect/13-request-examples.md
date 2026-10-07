# 13 — Request Examples and Payload Patterns

These examples are intentionally small. Replace deck/model/field names with values discovered from the user's live collection.

## Health check

```json
{
  "action": "version",
  "version": 6
}
```

## Discover supported actions

```json
{
  "action": "apiReflect",
  "version": 6,
  "params": {
    "scopes": ["actions"],
    "actions": null
  }
}
```

## Request browser-origin permission

```json
{
  "action": "requestPermission",
  "version": 6
}
```

A granted response includes permission status, whether an API key is required, and API version.

## List decks and note types

```json
{"action":"deckNames","version":6}
```

```json
{"action":"modelNames","version":6}
```

## Create a deck

```json
{
  "action": "createDeck",
  "version": 6,
  "params": {
    "deck": "French::02 Listening"
  }
}
```

## Create a model / note type

```json
{
  "action": "createModel",
  "version": 6,
  "params": {
    "modelName": "Anki Language - Listening",
    "inOrderFields": [
      "Context",
      "Prompt",
      "TargetLanguage",
      "Target",
      "BaseLanguage",
      "Base",
      "FrontAudio",
      "BackAudio",
      "Notes"
    ],
    "css": ".card { font-family: Arial; font-size: 20px; }",
    "isCloze": false,
    "cardTemplates": [
      {
        "Name": "Listening",
        "Front": "{{Context}}<br>{{FrontAudio}}",
        "Back": "{{FrontSide}}<hr>{{Target}}<br>{{Base}}<br>{{BackAudio}}"
      }
    ]
  }
}
```

Use `modelNames` first. Do not recreate an existing model blindly.

## Preflight a note

```json
{
  "action": "canAddNotesWithErrorDetail",
  "version": 6,
  "params": {
    "notes": [
      {
        "deckName": "French::03 Production",
        "modelName": "Anki Language - Production",
        "fields": {
          "Context": "French — Production",
          "Prompt": "Express the idea: to end up doing something",
          "Target": "finir par"
        },
        "tags": ["chunk", "production"]
      }
    ]
  }
}
```

## Add a note

```json
{
  "action": "addNote",
  "version": 6,
  "params": {
    "note": {
      "deckName": "French::03 Production",
      "modelName": "Anki Language - Production",
      "fields": {
        "Context": "French — Production",
        "Prompt": "Express the idea: to end up doing something",
        "TargetLanguage": "French",
        "Target": "finir par",
        "BaseLanguage": "English",
        "Base": "to end up doing something"
      },
      "options": {
        "allowDuplicate": false,
        "duplicateScope": "deck",
        "duplicateScopeOptions": {
          "deckName": "French::03 Production",
          "checkChildren": false,
          "checkAllModels": false
        }
      },
      "tags": ["chunk", "production"]
    }
  }
}
```

### Duplicate controls

Current documented note options include:

- `allowDuplicate`;
- `duplicateScope` (for example, `deck`);
- `duplicateScopeOptions.deckName`;
- `duplicateScopeOptions.checkChildren`;
- `duplicateScopeOptions.checkAllModels`.

Use these deliberately. Do not enable duplicates just to silence validation failures.

## Add a note with audio

```json
{
  "action": "addNote",
  "version": 6,
  "params": {
    "note": {
      "deckName": "French::02 Listening",
      "modelName": "Anki Language - Listening",
      "fields": {
        "Context": "French — Listening",
        "Target": "Je suis ici."
      },
      "audio": [
        {
          "url": "https://example.invalid/phrase.mp3",
          "filename": "fr_phrase_001.mp3",
          "fields": ["FrontAudio"]
        }
      ]
    }
  }
}
```

Media entries require a `filename` plus one source:
- `data` (base64);
- `path`;
- `url`.

Optional documented controls include:
- `skipHash` to reject known undesired content by MD5;
- `deleteExisting` in current media-storage implementations;
- `fields` to append the generated media markup to specified note fields.

Never use an example URL as if it grants redistribution rights.

## Store media separately

Base64:

```json
{
  "action": "storeMediaFile",
  "version": 6,
  "params": {
    "filename": "fr_phrase_001.mp3",
    "data": "<BASE64>"
  }
}
```

Path:

```json
{
  "action": "storeMediaFile",
  "version": 6,
  "params": {
    "filename": "fr_phrase_001.mp3",
    "path": "/absolute/path/fr_phrase_001.mp3"
  }
}
```

URL:

```json
{
  "action": "storeMediaFile",
  "version": 6,
  "params": {
    "filename": "fr_phrase_001.mp3",
    "url": "https://example.invalid/fr_phrase_001.mp3"
  }
}
```

The returned filename is the authoritative media basename to reference.

## Find notes

```json
{
  "action": "findNotes",
  "version": 6,
  "params": {
    "query": "tag:anki-language"
  }
}
```

Search syntax comes from Anki itself.

## Inspect notes

```json
{
  "action": "notesInfo",
  "version": 6,
  "params": {
    "notes": [1234567890]
  }
}
```

## Update fields

```json
{
  "action": "updateNoteFields",
  "version": 6,
  "params": {
    "note": {
      "id": 1234567890,
      "fields": {
        "Base": "updated explanation"
      }
    }
  }
}
```

Current upstream docs warn that updating a note while it is actively open/viewed in Anki Browser can prevent the field update from applying as expected.

## Add/remove tags

```json
{
  "action": "addTags",
  "version": 6,
  "params": {
    "notes": [1234567890],
    "tags": "anki-language generated"
  }
}
```

## Find cards and inspect rendered content

```json
{
  "action": "findCards",
  "version": 6,
  "params": {
    "query": "deck:\"French::02 Listening\""
  }
}
```

```json
{
  "action": "cardsInfo",
  "version": 6,
  "params": {
    "cards": [1234567891]
  }
}
```

## Open Browser for human verification

```json
{
  "action": "guiBrowse",
  "version": 6,
  "params": {
    "query": "tag:anki-language"
  }
}
```

## Batch independent calls with multi

```json
{
  "action": "multi",
  "version": 6,
  "params": {
    "actions": [
      {"action": "deckNames", "version": 6},
      {"action": "modelNames", "version": 6},
      {"action": "getTags", "version": 6}
    ]
  }
}
```

Nested responses retain each nested action's success/error behavior.

## Export APKG from live Anki

```json
{
  "action": "exportPackage",
  "version": 6,
  "params": {
    "deck": "French",
    "path": "/absolute/path/French.apkg",
    "includeSched": false
  }
}
```

For a shareable learning deck, scheduling is normally not included unless the user explicitly wants review state.

## Import APKG

```json
{
  "action": "importPackage",
  "version": 6,
  "params": {
    "path": "/path/to/French.apkg"
  }
}
```

Path behavior can be version/implementation-sensitive; verify current upstream docs and the user's environment.

## API key

When configured, add to the root request:

```json
{
  "action": "deckNames",
  "version": 6,
  "key": "SECRET"
}
```

Never commit real API keys to this repository or generated reports.
