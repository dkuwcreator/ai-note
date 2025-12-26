# Feature Specification: In-app AI Settings & Rewrite Modes

**Feature Branch**: `003-add-ai-settings`  
**Created**: 2025-12-26  
**Status**: Draft  
**Input**: User description: "Add an in-app Settings feature to AI Notepad that lets the user configure AI connection details and manage multiple rewrite modes."

## Semantic Scope *(Required)*

### Modules In Scope

- **UI (settings dialog + editor controls)**:
  - **Responsibility**: Present settings and rewrite mode controls to the user.
  - **Impact**: Add a `Settings` menu item and dialogs for `Connection` and `Rewrite Modes`; surface rewrite modes in the editor UI.

-- **AI configuration & presets (runtime layer)**:
  - **Responsibility**: Load runtime connection values and provide rewrite mode presets to the editor.
  - **Impact**: Expose a lightweight `Test Connection` operation at runtime and make available the list of rewrite modes to the editor UI.

- **Local preferences storage**:
  - **Responsibility**: Persist user preferences and rewrite mode metadata across restarts.
  - **Impact**: Persist non-secret settings and rewrite mode metadata; ensure editor continues to function if AI settings are absent.


### Constitution Alignment

- Local-First Storage: Persist preferences locally; include migration notes where storage schema changes are required. Secrets must not be stored in plaintext or committed to the repository.
- AI Provider Policy: The settings UI will request the connection information required by the supported provider; discovery or browsing of third-party models is out of scope.
- Privacy By Default: AI prompts and responses are ephemeral and not persisted by default. Only rewrite mode metadata and non-secret settings are saved.
- Security: Secrets (API keys) must be handled securely and not committed to the repository. The UI will explain recommended secure storage practices to the user.

### Modules Explicitly Out Of Scope

- **Auth / user accounts**: This feature does not add multi-user or cloud-synced accounts.
- **Model browsing**: Browsing available models or deployments beyond the configured deployment is out of scope.

### Cross-Module Impacts

**Module Dependencies**:

- The UI depends on the application's preferences storage to read and write settings and rewrite mode definitions.
- The runtime AI integration depends on preferences storage and secure secret storage to load connection settings at startup.

**Compatibility Requirements**:

- Backward compatibility: If no AI settings are configured the editor must continue to function normally (editing, saving, searching unaffected).
- No breaking changes to existing note file formats.

**Migration Notes**:

- Add a migration to introduce persistent storage for user-defined rewrite modes and any new preference keys. Existing built-in presets should remain available and unaffected by the migration.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Configure & Test AI Connection (Priority: P1)

As a user, I want to enter my AI provider connection details in the app, test the connection, and save the settings so I can use AI-powered rewrites without editing environment variables.

**Why this priority**: This directly enables the core user goal of configuring AI from the app — without this, rewrite modes cannot call the AI.

**Independent Test**: Open Settings → Connection, enter provider address and deployment identifier (or equivalent), optionally provider version and timeout, paste API key, click `Test Connection`. The app shows a success message (with basic info) or a clear failure message (auth error, deployment not found, network timeout).

**Acceptance Scenarios**:

1. **Given** the Settings dialog is open, **When** I provide a valid provider address/deployment identifier/API key and click `Test Connection`, **Then** I see a green success indicator and the test result summary.
2. **Given** I enter an invalid API key, **When** I click `Test Connection`, **Then** I receive a clear authentication error message and guidance to re-enter the key.
3. **Given** the network is unreachable or timeout occurs, **When** I click `Test Connection`, **Then** I receive a timeout/network error with retry guidance.

---

### User Story 2 - Create & Use Rewrite Mode (Priority: P1)

As a user, I want to create a rewrite mode with a name and instruction so I can apply it to my notes from the editor.

**Why this priority**: Core to the feature — users must be able to create custom rewrite behaviors.

**Independent Test**: Open Settings → Rewrite Modes, create a new mode named `Make it concise` with an instruction. Save. In the editor, select text (or leave cursor in note), choose `Make it concise` from the rewrite menu, and the note is rewritten according to the instruction.

**Acceptance Scenarios**:

1. **Given** no custom modes exist, **When** I create a new mode and save, **Then** the mode appears in the rewrite modes list and in the editor UI.
2. **Given** a selection in the editor and a mode configured as `selection-only`, **When** I apply the mode, **Then** only the selection is rewritten.

---

### User Story 3 - Manage Presets (Priority: P2)

As a user, I want to edit, duplicate, enable/disable, reorder, and delete rewrite modes — and have a set of built-in presets available to duplicate.

**Why this priority**: Enhances usability and discovers use patterns; not required for MVP but expected.

**Independent Test**: From Rewrite Modes settings: duplicate a built-in preset, rename it, reorder it in the list, disable it. Confirm changes reflected in editor menu order.

**Acceptance Scenarios**:

1. **Given** built-in presets are present, **When** I duplicate `Make more formal`, **Then** I can edit and save the duplicate without changing the original.
2. **Given** I reorder modes, **When** I open the editor rewrite menu, **Then** modes appear in the updated order.

---

### Edge Cases

- Test Connection with slow networks: ensure `Timeout seconds` setting is respected and user gets a descriptive timeout message.
- Partial configuration: if required connection fields are missing, `Test Connection` should refuse to run and prompt which fields are required.
- Keyring unavailable: if OS keyring is not accessible, present secure-storage fallback options and a clear warning about storing secrets.
- Apply mode when AI is not configured: the editor shows a prompt to configure AI (links to Settings) but editing remains functional.


## Implementation notes

Engineering-level implementation notes and provider-specific details are captured in a separate document: [implementation.md](implementation.md). These notes are not part of the user-facing specification.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The app MUST provide a `Settings` UI entry reachable from the main menu.
- **FR-002**: The app MUST provide a `Connection` panel to enter required connection fields and optional timeout/retry settings.
- **FR-003**: The app MUST provide an `API Key` input field that masks input and supports paste/update.
 - **FR-004**: The app MUST provide a `Test Connection` button that performs a lightweight validation call and returns a clear, categorized result (success, auth error, deployment not found, network timeout/error). The validation call for MVP SHOULD be a tiny rewrite ping using a fixed short test prompt; the request MUST complete within the configured timeout (default 6 seconds).
- **FR-005**: The app MUST persist non-secret connection fields and rewrite mode metadata across restarts.
-- **FR-006**: The app SHOULD store API keys in the OS keyring when available; if not available, the app MUST provide an encrypted local storage fallback (app-managed encryption using a user-provided passphrase or securely derived key) after explicit consent and with a clear warning.
**FR-006 Acceptance**: Given the OS provides a keyring, when a user saves an API key, then the key is stored in the keyring and a non-secret reference is persisted in app settings. Given no keyring is available, when a user chooses to store the key locally, then the app stores it encrypted using app-managed encryption (protected by a user-provided passphrase or securely derived key); explicit consent and a prominent warning are required in Settings.

**FR-004 Acceptance**: Given valid connection fields and credentials, when the user clicks `Test Connection`, then the app sends a tiny rewrite ping (fixed short prompt) and reports success if the provider returns a valid completion within the configured timeout (default 6 seconds). Given authentication or routing errors, the app returns an auth or deployment-not-found result. Given no response within the timeout, the app reports a network timeout and suggests retrying or increasing the timeout.
- **FR-007**: The app MUST provide a `Rewrite Modes` management UI where users can create, edit, duplicate, enable/disable, delete, and reorder modes.
- **FR-008**: A rewrite mode MUST include: `Name`, `Instruction` (prompt template), `Applies To` flag (`selection-only` vs `whole-note-default`), and optional `Output Style Hints`.
 - **FR-008**: A rewrite mode (MVP) MUST include the following fields: `name` (string), `instruction_template` (string), `enabled` (bool), `order` (integer), and `applies_to` (enum: `selection-only` | `whole-note-default`). Optional metadata such as `output_style_hints` may be included but are not required for MVP.
 - **FR-013**: The `Rewrite Modes` UI MUST expose an `Advanced Settings` section for each mode containing optional fields (e.g., `temperature`, `max_tokens`, `system_prompt_override`), but this section MUST be collapsed/hidden by default and require an explicit user action to reveal (MVP: advanced fields are non-default and not required to create/save a mode).
- **FR-009**: The editor UI MUST display available rewrite modes (built-in + user) and apply a selected mode to either the selection or whole note based on the mode setting.
- **FR-010**: The app MUST NOT persist raw AI responses to disk.
- **FR-011**: The app MUST ensure API keys and secrets are excluded from source control and provide documentation/guidance in the Settings UI about secure storage and gitignore practices.
- **FR-012**: The app MUST support a single persistent connection profile (MVP). Support for multiple connection profiles is out of scope for the MVP and may be considered in later iterations.
 - **FR-014**: The app WILL use PySide6 (Qt) for the Settings and Rewrite Modes UI implementation in this iteration to enable richer dialogs, lists, and collapsible advanced sections. If PySide6 cannot be used in a later iteration, the UI toolkit decision may be revisited.

### Acceptance Criteria for Security & Storage FRs

- **FR-006 Acceptance**: Given the OS provides a keyring, when a user saves an API key, then the key is stored in the keyring and a non-secret reference is persisted in app settings. Given no keyring is available, when a user chooses to store the key locally, then the app stores it only after explicit consent and shows a warning in Settings.

- **FR-011 Acceptance**: Given the repository is present, when the feature is installed, then documentation warns about secrets and a recommended `.gitignore` snippet is provided in the Settings help link; local secret storage files are excluded from commits by default where feasible.

*Marked Clarifications (none required)*

### Key Entities *(include if feature involves data)*

- **Settings**: Persisted non-secret connection and preference fields such as provider address, deployment identifier (or equivalent), optional provider version, timeout and retry preferences.
- **Secret**: The API key or token required to authenticate with the configured provider — must be stored securely and not committed to the repository.
- **Rewrite Mode**: A user-defined or built-in mode with attributes: `id`, `name`, `instruction`, `applies_to` (selection-only | whole-note-default), `enabled`, `order`, `output_style_hints`, and `builtin` (bool).
 - **Rewrite Mode**: A user-defined or built-in mode with attributes: `id`, `name`, `instruction_template`, `applies_to` (selection-only | whole-note-default), `enabled`, `order`, `output_style_hints`, `builtin` (bool). Optional `advanced_settings` (object) MAY include provider-specific tuning fields such as `temperature`, `max_tokens`, and `system_prompt_override`; `advanced_settings` are hidden by default in the UI and are not required for MVP behavior.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-- **SC-001**: Users can configure provider address, deployment identifier (or equivalent), and API key and receive a definitive `Test Connection` success or failure message in under 10 seconds for valid network conditions.
- **SC-002**: Users can create, save, and use at least 3 custom rewrite modes from the editor, with correct behavior for selection-only vs whole-note modes.
- **SC-003**: If AI is not configured, core editor functionality (edit/save/search) continues to work with no errors.
- **SC-004**: API keys are not written to source-controlled files and users are warned in the UI if a non-keyring fallback is used.

## Clarifications

### Session 2025-12-26

- Q: Secrets persistence fallback when OS keyring unavailable → A: Encrypted local storage (user passphrase) — store API keys encrypted locally using app-managed encryption protected by a user-provided passphrase or securely derived key; require explicit consent and show a prominent warning in Settings.
- Q: Single connection profile vs multiple → A: Single connection profile (MVP). Multiple profiles are deferred to future work.
- Q: Rewrite mode schema fields and advanced settings visibility → A: MVP required fields: `name`, `instruction_template`, `enabled`, `order`, `applies_to`. Advanced settings (`temperature`, `max_tokens`, `system_prompt_override`) exist but are hidden/collapsed by default and optional.
- Q: Test Connection semantics and timeout → A: Tiny rewrite ping with fixed short prompt; consider success if valid completion returns within configured timeout (default 6s).
- Q: UI toolkit for settings dialog → A: PySide6 (recommended) — use PySide6 for richer UI widgets and collapsible advanced sections.
