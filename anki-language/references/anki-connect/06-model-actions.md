# 06 — Model / Note-Type / Field / Template Actions

AnkiConnect calls Anki note types **models**.

These actions inspect and mutate fields, templates, and CSS.

Prefer a namespaced workflow-owned model rather than rewriting a user's model; field/template removals are destructive.

## Supported actions

| Action | Status | Main documented params | Purpose |
| --- | --- | --- | --- |
| `modelNames` | baseline | — | Gets the complete list of model names for the current user. |
| `modelNamesAndIds` | baseline | — | Gets the complete list of model names and their corresponding IDs for the current user. |
| `findModelsById` | baseline | `modelIds` | Gets a list of models  for the provided model IDs from the current user. |
| `findModelsByName` | baseline | `modelNames` | Gets a list of models for the provided model names from the current user. |
| `modelFieldNames` | baseline | `modelName` | Gets the complete list of field names for the provided model name. |
| `modelFieldDescriptions` | baseline | `modelName` | Gets the complete list of field descriptions (the text seen in the gui editor when a field is empty) for the provided model name. |
| `modelFieldFonts` | baseline | `modelName` | Gets the complete list of fonts along with their font sizes. |
| `modelFieldsOnTemplates` | baseline | `modelName` | Returns an object indicating the fields on the question and answer side of each card template for the given model |
| `createModel` | baseline | `modelName`, `inOrderFields`, `css`, `isCloze`, `cardTemplates` | Creates a new model to be used in Anki. User must provide the `modelName`, `inOrderFields` and `cardTemplates` to be |
| `modelTemplates` | baseline | `modelName` | Returns an object indicating the template content for each card connected to the provided model by name. |
| `modelStyling` | baseline | `modelName` | Gets the CSS styling for the provided model by name. |
| `updateModelTemplates` | baseline | `model` | Modify the templates of an existing model by name. Only specifies cards and specified sides will be modified. |
| `updateModelStyling` | baseline | `model` | Modify the CSS styling of an existing model by name. |
| `findAndReplaceInModels` | baseline | `model` | Find and replace string in existing model by model name. Customise to replace in front, back or css by setting to true/false. |
| `modelTemplateRename` | baseline | `modelName`, `oldTemplateName`, `newTemplateName` | Renames a template in an existing model. |
| `modelTemplateReposition` | baseline | `modelName`, `templateName`, `index` | Repositions a template in an existing model. |
| `modelTemplateAdd` | baseline | `modelName`, `template` | Adds a template to an existing model by name. If you want to update an existing template, use `updateModelTemplates`. |
| `modelTemplateRemove` | baseline | `modelName`, `templateName` | Removes a template from an existing model. |
| `modelFieldRename` | baseline | `modelName`, `oldFieldName`, `newFieldName` | Rename the field name of a given model. |
| `modelFieldReposition` | baseline | `modelName`, `fieldName`, `index` | Reposition the field within the field list of a given model. |
| `modelFieldAdd` | baseline | `modelName`, `fieldName`, `index` | Creates a new field within a given model. |
| `modelFieldRemove` | baseline | `modelName`, `fieldName` | Deletes a field within a given model. |
| `modelFieldSetFont` | baseline | `modelName`, `fieldName`, `font` | Sets the font for a field within a given model. |
| `modelFieldSetFontSize` | baseline | `modelName`, `fieldName`, `fontSize` | Sets the font size for a field within a given model. |
| `modelFieldSetDescription` | baseline | `modelName`, `fieldName`, `description` | Sets the description (the text seen in the gui editor when a field is empty) for a field within a given model. |

## Status policy

- **baseline**: present in the baseline public standard documentation snapshot.
- **extended / verify via `apiReflect`**: present in a newer upstream-tracking mirror but absent from the baseline mirror; verify the user's installed AnkiConnect before invoking.

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect.

## Sources

- https://github.com/ankiultimate/anki-connect
- https://github.com/JSchoreels/anki-connect
