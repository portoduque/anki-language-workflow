# 06 — Model / Note-Type / Field / Template Actions

AnkiConnect calls Anki note types **models**.

These actions inspect and mutate fields, templates, and CSS.

Prefer a namespaced workflow-owned model rather than rewriting a user's model; field/template removals are destructive.

## Supported actions

| Action | Main documented params | Purpose |
| --- | --- | --- |
| `modelNames` | — | See upstream documentation. |
| `modelNamesAndIds` | — | See upstream documentation. |
| `findModelsById` | — | See upstream documentation. |
| `findModelsByName` | — | See upstream documentation. |
| `modelFieldNames` | — | See upstream documentation. |
| `modelFieldDescriptions` | — | See upstream documentation. |
| `modelFieldFonts` | — | See upstream documentation. |
| `modelFieldsOnTemplates` | — | See upstream documentation. |
| `createModel` | — | See upstream documentation. |
| `modelTemplates` | — | See upstream documentation. |
| `modelStyling` | — | See upstream documentation. |
| `updateModelTemplates` | — | See upstream documentation. |
| `updateModelStyling` | — | See upstream documentation. |
| `findAndReplaceInModels` | — | See upstream documentation. |
| `modelTemplateRename` | — | See upstream documentation. |
| `modelTemplateReposition` | — | See upstream documentation. |
| `modelTemplateAdd` | — | See upstream documentation. |
| `modelTemplateRemove` | — | See upstream documentation. |
| `modelFieldRename` | — | See upstream documentation. |
| `modelFieldReposition` | — | See upstream documentation. |
| `modelFieldAdd` | — | See upstream documentation. |
| `modelFieldRemove` | — | See upstream documentation. |
| `modelFieldSetFont` | — | See upstream documentation. |
| `modelFieldSetFontSize` | — | See upstream documentation. |
| `modelFieldSetDescription` | — | See upstream documentation. |

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect. The local catalog is a curated snapshot, not a substitute for runtime capability discovery.

## Source

- https://github.com/ankiultimate/anki-connect/blob/master/README.md
