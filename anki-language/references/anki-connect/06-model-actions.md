# 06 — Model / Note-Type / Field / Template Actions

AnkiConnect uses the term **model** for an Anki note type.

These actions inspect or mutate fields, card templates, and CSS.

## Recommended policy

- inspect `modelNames`, fields, templates, and styling before writing;
- prefer a workflow-owned namespaced model instead of rewriting arbitrary user models;
- treat field/template removal as destructive;
- preserve user customizations unless the user explicitly wants them replaced.

## Complete current catalog

| Action | Exact source signature | Risk | Purpose |
| --- | --- | --- | --- |
| `modelNames` | `self` | `read` | Gets the complete list of model names for the current user. |
| `modelNamesAndIds` | `self` | `read` | Gets the complete list of model names and their corresponding IDs for the current user. |
| `findModelsById` | `self, modelIds` | `read` | Gets a list of models for the provided model IDs from the current user. |
| `findModelsByName` | `self, modelNames` | `read` | Gets a list of models for the provided model names from the current user. |
| `modelFieldNames` | `self, modelName` | `read` | Gets the complete list of field names for the provided model name. |
| `modelFieldDescriptions` | `self, modelName` | `read` | Gets the complete list of field descriptions (the text seen in the gui editor when a field is empty) for the provided model name. |
| `modelFieldFonts` | `self, modelName` | `read` | Gets the complete list of fonts along with their font sizes. |
| `modelFieldsOnTemplates` | `self, modelName` | `read` | Returns an object indicating the fields on the question and answer side of each card template for the given model name. |
| `createModel` | `self, modelName, inOrderFields, cardTemplates, css = None, isCloze = False` | `write` | Creates a new model to be used in Anki. |
| `modelTemplates` | `self, modelName` | `read` | Returns an object indicating the template content for each card connected to the provided model by name. |
| `modelStyling` | `self, modelName` | `read` | Gets the CSS styling for the provided model by name. |
| `updateModelTemplates` | `self, model` | `write` | Modify the templates of an existing model by name. |
| `updateModelStyling` | `self, model` | `write` | Modify the CSS styling of an existing model by name. |
| `findAndReplaceInModels` | `self, modelName, findText, replaceText, front=True, back=True, css=True` | `read` | Find and replace string in existing model by model name. |
| `modelTemplateRename` | `self, modelName, oldTemplateName, newTemplateName` | `read` | Renames a template in an existing model. |
| `modelTemplateReposition` | `self, modelName, templateName, index` | `read` | Repositions a template in an existing model. |
| `modelTemplateAdd` | `self, modelName, template` | `read` | Adds a template to an existing model by name. |
| `modelTemplateRemove` | `self, modelName, templateName` | `destructive` | Removes a template from an existing model. |
| `modelFieldRename` | `self, modelName, oldFieldName, newFieldName` | `read` | Rename the field name of a given model. |
| `modelFieldReposition` | `self, modelName, fieldName, index` | `read` | Reposition the field within the field list of a given model. |
| `modelFieldAdd` | `self, modelName, fieldName, index=None` | `read` | Creates a new field within a given model. |
| `modelFieldRemove` | `self, modelName, fieldName` | `destructive` | Deletes a field within a given model. |
| `modelFieldSetFont` | `self, modelName, fieldName, font` | `read` | Sets the font for a field within a given model. |
| `modelFieldSetFontSize` | `self, modelName, fieldName, fontSize` | `read` | Sets the font size for a field within a given model. |
| `modelFieldSetDescription` | `self, modelName, fieldName, description` | `read` | Sets the description (the text seen in the gui editor when a field is empty) for a field within a given model. |

Model changes can affect many existing cards at once; back up before broad schema mutations.
