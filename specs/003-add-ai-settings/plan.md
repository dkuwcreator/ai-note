# Implementation Plan: In-app AI Settings & Rewrite Modes

**Branch**: `003-add-ai-settings` | **Date**: 2025-12-26 | **Spec**: [spec.md](spec.md)

## Summary

This feature introduces an in-app settings dialog for configuring AI connection details and managing rewrite modes. It includes a `Connection` panel for AI provider settings and a `Rewrite Modes` panel for managing rewrite templates. The implementation ensures secure storage of secrets, non-blocking UI operations, and adherence to privacy and security principles.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: PySide6, keyring, cryptography  
**Storage**: SQLite for non-secret settings; OS keyring or encrypted local storage for secrets  
**Testing**: pytest with mocks for AI client and storage  
**Target Platform**: Desktop (Windows, macOS, Linux)  
**Project Type**: Single desktop application  
**Performance Goals**: Non-blocking UI; `Test Connection` completes within 10 seconds  
**Constraints**: Local-first storage; Azure-only AI integration  
**Scale/Scope**: Single connection profile; CRUD for rewrite modes

## Constitution Check

- **Simplicity**: UI and storage changes are minimal and modular.
- **Local-First Storage**: SQLite for preferences; secrets stored securely.
- **Azure-Only AI**: Connection settings target Azure OpenAI.
- **Privacy By Default**: No raw AI responses are persisted.
- **Security**: Secrets excluded from source control; secure storage enforced.
- **Testability**: Core logic is unit-tested with mocks.
- **Maintainability**: Clear module boundaries and documentation updates.

## Semantic Architecture Plan

### Semantic Map

**Clusters**:
- **UI**: Settings dialog and editor controls.
- **Runtime**: AI connection and rewrite mode management.
- **Storage**: Preferences and secrets storage.

**Modules**:
- **Settings UI** (`desktop_app/ui.py`):
  - **Responsibility**: Render settings dialog with `Connection` and `Rewrite Modes` panels.
  - **Boundaries**: UI logic only; delegates storage and runtime operations.
  - **Interfaces**: Calls storage and runtime modules.
- **AI Runtime** (`ai/client.py`):
  - **Responsibility**: Manage AI connection and rewrite operations.
  - **Boundaries**: No direct UI interaction; uses stored settings.
  - **Interfaces**: Provides `Test Connection` and rewrite APIs.
- **Preferences Storage** (`storage/db.py`):
  - **Responsibility**: Persist non-secret settings and rewrite modes.
  - **Boundaries**: No direct UI or runtime logic.
  - **Interfaces**: CRUD for settings and modes.
- **Secrets Storage** (`storage/utils.py`):
  - **Responsibility**: Securely store API keys.
  - **Boundaries**: No direct UI interaction; integrates with keyring or local encryption.

### Modules Impacted

- **desktop_app/ui.py**:
  - **Planned Changes**: Add `Settings` dialog with `Connection` and `Rewrite Modes` panels.
  - **Files Affected**: `desktop_app/ui.py`, `desktop_app/main.py`
- **ai/client.py**:
  - **Planned Changes**: Add `Test Connection` API; support rewrite mode execution.
  - **Files Affected**: `ai/client.py`
- **storage/db.py**:
  - **Planned Changes**: Add schema for rewrite modes and preferences.
  - **Files Affected**: `storage/db.py`, `storage/migrations.py`
- **storage/utils.py**:
  - **Planned Changes**: Add keyring and encryption support for secrets.
  - **Files Affected**: `storage/utils.py`

### Invariants to Preserve

- **UI**: Non-blocking operations; no raw AI responses persisted.
- **Storage**: Secrets never stored in plaintext.
- **Runtime**: Editor remains functional without AI configuration.

### Interfaces & Dependencies Touched

**New Interfaces**:
- `ai/client.py`: `test_connection()` API.
- `storage/db.py`: CRUD for rewrite modes.
- `storage/utils.py`: Secure storage APIs.

**Modified Interfaces**:
- `desktop_app/ui.py`: Add settings dialog.

### Meaning Parity Updates Required

#### README.md Updates
- **desktop_app/**: Document settings dialog responsibilities.
- **ai/**: Document `test_connection()` API.
- **storage/**: Document preferences and secrets storage.

#### AGENT_INSTRUCTION.md Updates
- **desktop_app/**: Update allowed edits for UI changes.
- **ai/**: Add testing requirements for `test_connection()`.
- **storage/**: Add constraints for secure storage.

#### Other Documentation
- **quickstart.md**: Add settings configuration steps.
- **.env.template**: Add example environment variables.
- **gitignore**: Exclude local secrets storage files.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| None      |            |                                      |
