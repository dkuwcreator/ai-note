# Data Model: In-app AI Settings & Rewrite Modes

## Entities

### Connection Settings
- **endpoint**: string (required)
- **deployment_id**: string (required)
- **api_version**: string (optional)
- **timeout**: integer (default: 6)
- **retry_prefs**: object (optional)

### Rewrite Mode
- **id**: integer (primary key)
- **name**: string (required)
- **instruction_template**: string (required)
- **enabled**: boolean (default: true)
- **order**: integer (required)
- **applies_to**: enum (`selection-only`, `whole-note-default`)
- **builtin**: boolean (default: false)
- **advanced_settings**: object (optional, collapsed by default)

## Relationships

- **Connection Settings**: Singleton; only one profile is persisted.
- **Rewrite Modes**: Many-to-one relationship with the application; built-in modes are immutable.

## Validation Rules

- **Connection Settings**:
  - `endpoint` and `deployment_id` are required.
  - `timeout` must be a positive integer.
- **Rewrite Modes**:
  - `name` must be unique.
  - `order` determines display priority; no duplicates allowed.

## Migration Strategy

1. **Initial Migration**:
   - Add `connection_settings` table with fields for endpoint, deployment_id, api_version, timeout, and retry_prefs.
   - Add `rewrite_modes` table with fields for id, name, instruction_template, enabled, order, applies_to, builtin, and advanced_settings.
2. **Seed Defaults**:
   - Populate `rewrite_modes` with built-in presets (e.g., `Make more formal`, `Simplify`).
3. **Backward Compatibility**:
   - Ensure existing functionality remains unaffected if no settings are configured.

## Seed Data

### Built-in Rewrite Modes

| ID  | Name              | Instruction Template       | Enabled | Order | Applies To       | Built-in |
|-----|-------------------|----------------------------|---------|-------|------------------|----------|
| 1   | Make more formal  | "Rewrite formally: {text}"| true    | 1     | whole-note-default | true     |
| 2   | Simplify          | "Simplify: {text}"        | true    | 2     | selection-only    | true     |

## Notes

- Built-in modes are immutable and cannot be deleted or edited.
- User-defined modes can be created, edited, reordered, enabled/disabled, and deleted.