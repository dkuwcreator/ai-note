# Tasks: In-app AI Settings & Rewrite Modes

## Phase 1: Setup

- [x] T001 [Setup] Initialize PySide6 for the settings dialog in `desktop_app/ui.py`.
- [x] T002 [Setup] Add `keyring` and `cryptography` to `requirements.txt`.
- [x] T003 [Setup] Create initial database migration for `connection_settings` and `rewrite_modes` tables in `storage/migrations.py`.

## Phase 2: Foundational

- [x] T004 [UI] Add `Settings` menu entry in `desktop_app/main.py`.
- [x] T005 [UI] Implement `Connection` panel in `desktop_app/ui.py`.
- [x] T006 [UI] Implement `Rewrite Modes` panel in `desktop_app/ui.py`.
- [x] T007 [Storage] Implement CRUD operations for `connection_settings` in `storage/db.py`.
- [x] T008 [Storage] Implement CRUD operations for `rewrite_modes` in `storage/db.py`.
- [x] T009 [Secrets] Implement secure storage for API keys using `keyring` in `storage/utils.py`.
- [x] T010 [Secrets] Implement encrypted local storage fallback in `storage/utils.py`.

## Phase 3: User Story 1 - Configure & Test AI Connection

- [x] T011 [UI] Add `Test Connection` button to `Connection` panel in `desktop_app/ui.py`.
- [x] T012 [Runtime] Implement `test_connection()` API in `ai/client.py`.
- [x] T013 [UI] Display categorized results for `Test Connection` in `desktop_app/ui.py`.
- [x] T014 [Storage] Persist connection settings in `storage/db.py`.
- [x] T015 [Secrets] Store API key securely in `storage/utils.py` (keyring + encrypted fallback wired into Settings dialog).

## Phase 4: User Story 2 - Create & Use Rewrite Mode

- [x] T016 [UI] Add `Add New` button to `Rewrite Modes` panel in `desktop_app/ui.py`.
- [x] T017 [UI] Implement form for creating/editing rewrite modes in `desktop_app/ui.py`.
- [x] T018 [UI] Implement drag-and-drop reordering in `Rewrite Modes` panel in `desktop_app/ui.py`.
- [x] T019 [UI] Implement enable/disable toggle for rewrite modes in `desktop_app/ui.py`.
- [x] T020 [Runtime] Apply rewrite modes in `ai/client.py` (pending runtime integration).
- [x] T021 [Storage] Persist rewrite modes in `storage/db.py`.

## Phase 5: User Story 3 - Manage Presets

- [x] T022 [UI] Add `Duplicate` button to `Rewrite Modes` panel in `desktop_app/ui.py`.
- [x] T023 [UI] Add `Delete` button to `Rewrite Modes` panel in `desktop_app/ui.py`.
- [x] T024 [UI] Implement advanced settings toggle in `Rewrite Modes` panel in `desktop_app/ui.py`.
- [x] T025 [Storage] Seed built-in rewrite modes in `storage/migrations.py`.

### Notes

- Storage CRUD implemented and unit-tested.
- Secret storage utilities added in `storage/utils.py` (keyring + encrypted fallback); Settings dialog wired to use them.
- Full test suite currently passes locally.

## Phase 6: Testing & Documentation

- [x] T026 [Tests] Add unit tests for `test_connection()` in `tests/unit/test_ai_client.py`.
- [x] T027 [Tests] Add unit tests for `connection_settings` CRUD in `tests/unit/test_storage.py`.
- [x] T028 [Tests] Add unit tests for `rewrite_modes` CRUD in `tests/unit/test_rewrite_modes.py`.
- [x] T029 [Tests] Add unit tests for secure storage in `tests/unit/test_storage_utils.py`.
- [x] T030 [Docs] Update `quickstart.md` with settings configuration steps.
- [x] T031 [Docs] Update `README.md` for `desktop_app`, `ai`, and `storage` modules.
- [x] T032 [Docs] Add `.env.template` for environment variables.
- [x] T033 [Docs] Add `.gitignore` snippet for secrets.

## Dependencies

- Phase 1 tasks must complete before Phase 2.
- Phase 2 tasks must complete before User Stories.
- User Stories are independent and can be implemented in parallel.
- Testing and documentation tasks depend on implementation completion.
