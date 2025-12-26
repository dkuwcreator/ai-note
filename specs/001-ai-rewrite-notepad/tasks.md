---
description: "Auto-generated tasks for Desktop Notepad with AI Rewrite Assistant"
---

# Tasks: Desktop Notepad with AI Rewrite Assistant

**Input**: Design documents from `/specs/001-ai-rewrite-notepad/`

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 [Setup] Create project structure in Build Space: add directories `desktop_app/`, `storage/`, `ai/`, `config/`, `tests/` and placeholder __init__ files
- [X] T002 [Setup] Initialize Python project files: create `pyproject.toml`, `requirements.txt`, and `.env.template` in repository root
 - [X] T003 [P] [Setup] Configure linters and formatters: add `ruff` and `black` configs and pre-commit hook files

---

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T004 [Setup] Add storage schema migration script `storage/migrations.py` and initial migration SQL for SQLite (create tables defined in data-model.md)
- [X] T005 [P] [Config] Implement `config/settings.py` to load `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`, `AZURE_OPENAI_API_KEY` from environment and optionally OS keyring (file path: config/settings.py) (update docs)
-- [X] T006 [P] [AI] Implement `ai/client.py` skeleton with injectable transport and timeout/retry policy (file: ai/client.py) (update docs)
- [X] T007 [P] [Storage] Implement `storage/db.py` to create/open SQLite DB, apply migrations, and expose connection factory (file: storage/db.py) (update docs)
- [X] T008 [P] [Storage] Implement `storage/repository.py` with CRUD for notebooks, notes, tags, note_tags, recent, and search API with FTS5 fallback logic (file: storage/repository.py) (update docs)
- [X] T009 [P] [AI] Implement `ai/retry.py` with exponential backoff utility used by `ai/client.py` (file: ai/retry.py)
- [X] T010 [P] [ModuleDocs] Add README.md and AGENT_INSTRUCTION.md placeholders for modules: `desktop_app/`, `storage/`, `ai/`, `config/` (files in each module)

---

## Phase 3: User Story 1 - Create and Edit Notes (Priority: P1) 🎯 MVP

**Goal**: Provide the main editor with create/edit/save and autosave behavior using local SQLite storage.

**Independent Test**: Launch minimal UI, create a new note, type text, and verify persistence after restart.

- [X] T011 [P] [Models] [US1] Implement DB models and schema in `storage/migrations.py` matching `data-model.md` (file: storage/migrations.py) (update docs)
- [X] T012 [P] [Storage] [US1] Add `Note` and `Notebook` CRUD functions in `storage/repository.py` (file: storage/repository.py) (update docs)
- [X] T013 [P] [DesktopApp] [US1] Implement minimal `desktop_app/main.py` and `desktop_app/ui.py` with `tkinter` main window and editor pane (files: desktop_app/main.py, desktop_app/ui.py) (update docs)
- [X] T014 [P] [DesktopApp] [US1] Implement autosave debounce in `desktop_app/editor.py` that calls `storage/repository.py` (file: desktop_app/editor.py)
- [ ] T015 [DesktopApp] [US1] Wire UI to storage: load recent notes and notebooks on startup (file: desktop_app/main.py)
 - [X] T015 [DesktopApp] [US1] Wire UI to storage: load recent notes and notebooks on startup (file: desktop_app/main.py)
 - [X] T015 [DesktopApp] [US1] Wire UI to storage: load recent notes and notebooks on startup (file: desktop_app/main.py)
- [X] T016 [P] [Tests] [US1] Add unit tests for storage CRUD using in-memory SQLite in `tests/unit/test_storage.py` (file: tests/unit/test_storage.py)

---

## Phase 4: User Story 2 - Organize Notes by Notebooks & Tags (Priority: P1)

**Goal**: Allow creating notebooks and tags, and filtering notes by notebook or tag in the sidebar.

**Independent Test**: Create notebooks and tags, add notes, filter by notebook and tag.

 - [X] T017 [P] [Models] [US2] Implement `tags` and `note_tags` CRUD in `storage/repository.py` (file: storage/repository.py) (update docs)
 - [X] T018 [P] [DesktopApp] [US2] Add sidebar UI for notebooks and tag filters in `desktop_app/ui.py` (file: desktop_app/ui.py)
 - [X] T019 [P] [Storage] [US2] Add tag normalization utility in `storage/repository.py` or `storage/utils.py` (file: storage/utils.py) (update docs)
 - [X] T020 [P] [Tests] [US2] Add unit tests for tag normalization and filtering in `tests/unit/test_tags.py` (file: tests/unit/test_tags.py)

---

## Phase 5: User Story 3 - Quick Search Across All Notes (Priority: P1)

**Goal**: Provide a quick search that uses FTS5 or a LIKE fallback.

**Independent Test**: Add notes with unique phrases and verify search returns correct results.

 - [X] T021 [P] [Storage] [US3] Implement FTS5 `notes_fts` creation and synchronization (file: storage/repository.py) (update docs)
 - [X] T022 [P] [DesktopApp] [US3] Add search box to sidebar and wire to `storage/repository.search(query)` (file: desktop_app/ui.py)
 - [X] T023 [P] [Tests] [US3] Add search unit tests in `tests/unit/test_search.py` covering FTS5 and fallback logic (file: tests/unit/test_search.py)

---

## Phase 6: User Story 4 - AI Rewrite Assistant (Priority: P1)

**Goal**: Allow selecting text or whole note and requesting rewrite presets; show result in side-by-side diff preview and allow replace/copy.

**Independent Test**: Select text, request a rewrite, and verify returned text appears within ~5s and can replace original text.

- [ ] T024 [AI] [US4] Implement `ai/presets.py` with rewrite prompt templates for presets (file: ai/presets.py) (update docs)
 - [X] T024 [AI] [US4] Implement `ai/presets.py` with rewrite prompt templates for presets (file: ai/presets.py) (update docs)
- [ ] T025 [P] [AI] [US4] Implement `ai/client.py` to call Azure OpenAI deployment with timeout=6s and retry policy (file: ai/client.py) (update docs)
- [ ] T026 [DesktopApp] [US4] Add rewrite UI control and side-by-side diff preview in `desktop_app/ui.py` and `desktop_app/editor.py` (files: desktop_app/ui.py, desktop_app/editor.py)
 - [X] T025 [P] [AI] [US4] Implement `ai/client.py` to call Azure OpenAI deployment with timeout=6s and retry policy (file: ai/client.py) (update docs)
 - [X] T026 [DesktopApp] [US4] Add rewrite UI control and side-by-side diff preview in `desktop_app/ui.py` and `desktop_app/editor.py` (files: desktop_app/ui.py, desktop_app/editor.py)
 - [X] T027 [P] [AI] [US4] Add ephemeral `AIRequestLog` in `ai/client.py` for retry handling (in-memory only) (file: ai/client.py)
 - [X] T024 [AI] [US4] Implement `ai/presets.py` with rewrite prompt templates for presets (file: ai/presets.py) (update docs)
 - [X] T025 [P] [AI] [US4] Implement `ai/client.py` to call Azure OpenAI deployment with timeout=6s and retry policy (file: ai/client.py) (update docs)
 - [X] T026 [DesktopApp] [US4] Add rewrite UI control and side-by-side diff preview in `desktop_app/ui.py` and `desktop_app/editor.py` (files: desktop_app/ui.py, desktop_app/editor.py)
 - [X] T028 [P] [Tests] [US4] Add unit tests mocking AI transport in `tests/unit/test_ai_client.py` (file: tests/unit/test_ai_client.py)
 - [X] T028 [P] [Tests] [US4] Add unit tests mocking AI transport in `tests/unit/test_ai_client.py` (file: tests/unit/test_ai_client.py)

---

## Phase 7: User Story 5 - Save, Rename, Delete Notes + Recent View (Priority: P2)

**Goal**: Provide manual save, rename, delete and Recent list.

**Independent Test**: Rename and delete notes and verify Recent ordering.

 - [X] T029 [Storage] [US5] Implement rename and delete functions in `storage/repository.py` (file: storage/repository.py) (update docs)
 - [X] T030 [DesktopApp] [US5] Add rename/delete UI actions and Recent view in `desktop_app/ui.py` (file: desktop_app/ui.py)
 - [X] T031 [Tests] [US5] Add unit tests for rename/delete and recent ordering in `tests/unit/test_notes_crud.py` (file: tests/unit/test_notes_crud.py)

---

## Phase N: Semantic Architecture Compliance (Required)

 - [X] T032 [P] [ModuleDocs] Update `desktop_app/README.md` and `desktop_app/AGENT_INSTRUCTION.md` to reflect actual UI behavior (files: desktop_app/README.md, desktop_app/AGENT_INSTRUCTION.md)
 - [X] T033 [P] [ModuleDocs] Update `storage/README.md` and `storage/AGENT_INSTRUCTION.md` documenting schema, invariants, and migration steps (files: storage/README.md, storage/AGENT_INSTRUCTION.md)
 - [X] T034 [P] [ModuleDocs] Update `ai/README.md` and `ai/AGENT_INSTRUCTION.md` documenting Azure-only constraint, retry/timeouts, and test injection points (files: ai/README.md, ai/AGENT_INSTRUCTION.md)
 - [X] T035 [P] [ModuleDocs] Update `config/README.md` documenting env vars and keyring usage (file: config/README.md)
 - [X] T032 [P] [ModuleDocs] Update `desktop_app/README.md` and `desktop_app/AGENT_INSTRUCTION.md` to reflect actual UI behavior (files: desktop_app/README.md, desktop_app/AGENT_INSTRUCTION.md)
 - [X] T033 [P] [ModuleDocs] Update `storage/README.md` and `storage/AGENT_INSTRUCTION.md` documenting schema, invariants, and migration steps (files: storage/README.md, storage/AGENT_INSTRUCTION.md)
 - [X] T034 [P] [ModuleDocs] Update `ai/README.md` and `ai/AGENT_INSTRUCTION.md` documenting Azure-only constraint, retry/timeouts, and test injection points (files: ai/README.md, ai/AGENT_INSTRUCTION.md)
 - [X] T035 [P] [ModuleDocs] Update `config/README.md` documenting env vars and keyring usage (file: config/README.md)
- [X] T036 [P] [Semantic] Verify spec ↔ plan ↔ tasks alignment and flag boundary-violating tasks (file targets across Build Space)

---

## Phase N+1: Polish & Cross-Cutting Concerns

 - [X] T037 [P] [Docs] Update `quickstart.md` with run/build steps and env configuration (file: quickstart.md)
 - [X] T038 [P] [CI] Add basic CI skeleton in `.github/workflows/ci.yml` to run unit tests and linting (file: .github/workflows/ci.yml)
 - [X] T039 [P] [Polish] Add packaging `scripts/build_windows.ps1` using PyInstaller to build a Windows exe (file: scripts/build_windows.ps1)

---

## Dependencies & Execution Order

- Foundational tasks (T004-T010) MUST complete before User Story phases begin.
- User stories (T011-T031) are ordered by priority but can be executed in parallel after foundational completion.

## Summary

- Total tasks: 39
- P1 stories: US1, US2, US3, US4 (primary MVP)
- Suggested MVP scope: Complete Phases 1-3 (Setup + Foundational + User Story 1) to have a runnable minimal app; include US4 AI stubs for mock testing.
