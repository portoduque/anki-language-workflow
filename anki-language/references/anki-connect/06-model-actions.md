# 06 — Model / Note-Type / Field / Template Actions

AnkiConnect uses the term **model** for an Anki note type.

These actions inspect or mutate fields, card templates, and CSS.

## Recommended policy

- inspect `modelNames`, fields, templates, and styling before writing;
- prefer a workflow-owned namespaced model instead of rewriting arbitrary user models;
- treat field/template removal as destructive;
- preserve user customizations unless the user explicitly wants them replaced.

## Common workflows

- `modelFieldNames` → discover valid fields.
- `modelTemplates` / `modelStyling` → inspect current card design.
- `createModel` → create a new note type with fields/templates/CSS.
- `updateModelTemplates` / `updateModelStyling` → controlled updates.
- field/template add/rename/reposition/remove → schema maintenance.

## Current catalog

| Action | Source signature | Risk |
| --- | --- | --- |
| `modelNames` | `self` | `read` |
| `modelNamesAndIds` | `self` | `read` |
| `findModelsById` | `self, modelIds` | `read` |
| `findModelsByName` | `self, modelNames` | `read` |
| `modelFieldNames` | `self, modelName` | `read` |
| `modelFieldDescriptions` | `self, modelName` | `read` |
| `modelFieldFonts` | `self, modelName` | `read` |
| `modelFieldsOnTemplates` | `self, modelName` | `read` |
| `createModel` | `self, modelName, inOrderFields, cardTemplates, css = None, isCloze = False` | `write` |
| `modelTemplates` | `self, modelName` | `read` |
| `modelStyling` | `self, modelName` | `read` |
| `updateModelTemplates` | `self, model` | `write` |
| `updateModelStyling` | `self, model` | `write` |
| `findAndReplaceInModels` | `self, modelName, findText, replaceText, front=True, back=True, css=True` | `read` |
| `modelTemplateRename` | `self, modelName, oldTemplateName, newTemplateName` | `read` |
| `modelTemplateReposition` | `self, modelName, templateName, index` | `read` |
| `modelTemplateAdd` | `self, modelName, template` | `read` |
| `modelTemplateRemove` | `self, modelName, templateName` | `destructive` |
| `modelFieldRename` | `self, modelName, oldFieldName, newFieldName` | `read` |
| `modelFieldReposition` | `self, modelName, fieldName, index` | `read` |
| `modelFieldAdd` | `self, modelName, fieldName, index=None` | `read` |
| `modelFieldRemove` | `self, modelName, fieldName` | `destructive` |
| `modelFieldSetFont` | `self, modelName, fieldName, font` | `read` |
| `modelFieldSetFontSize` | `self, modelName, fieldName, fontSize` | `read` |
| `modelFieldSetDescription` | `self, modelName, fieldName, description` | `read` |

Model changes can affect many existing cards at once; back up before broad schema mutations.
