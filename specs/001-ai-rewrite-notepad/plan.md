# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  

# Desktop Notepad with AI Rewrite Assistant — Implementation Plan

Overview
--------

Small, modular Python desktop app (Windows MVP) that stores notes in a single local SQLite file and offers an Azure OpenAI-powered rewrite assistant. Priorities: simplicity, local-first storage, Azure-only AI, responsiveness, and testability.

Top-level Modules (mapped to repo locations)
-------------------------------------------

- `desktop_app/` — UI layer (main window, editor, sidebar, menus, dialogs)
  - Files to add: `desktop_app/__init__.py`, `desktop_app/main.py`, `desktop_app/ui.py`, `desktop_app/editor.py`
  - Responsibilities: present notes list, create/edit notes, notebook/tag filters, quick search UI, recent notes, rewrite controls, side-by-side diff preview.
  - Invariants: UI must not perform blocking network or disk I/O on the main thread.

- `storage/` — Local persistence and search
  - Files to add: `storage/__init__.py`, `storage/db.py`, `storage/migrations.py`, `storage/repository.py`
  - Responsibilities: manage SQLite DB file, schema migrations, CRUD for notebooks/notes/tags, autosave API with debounce, recent view, search API with FTS5 and fallback.
  - Invariants: provide an abstracted interface usable off-UI thread; support in-memory DB for tests.

- `ai/` — AI client and request orchestration
  - Files to add: `ai/__init__.py`, `ai/client.py`, `ai/presets.py`, `ai/retry.py`
  - Responsibilities: wrap Azure OpenAI deployment, implement timeouts (default 6s), retries (exponential backoff: 500ms, 1500ms), cancellation hooks, and safe error handling.
  - Invariants: enforce Azure-only endpoints from config; never persist prompts/responses by default.

- `config/` — Configuration loader and secrets
  - Files to add: `config/__init__.py`, `config/settings.py`
  - Responsibilities: load `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`, `AZURE_OPENAI_API_KEY` from environment or OS keyring (optional); expose typed settings.
  - Invariants: secrets must not be printed or stored in repo; provide a `.env.template` for developer convenience.

Module Documentation Tasks
--------------------------

- Each module must include `README.md` and `AGENT_INSTRUCTION.md` when implementation changes are introduced (Meaning Parity requirement).

UI Flow (happy path)
--------------------

1. App starts — storage initializes DB file in user app-data folder; recent notes loaded.
2. Left sidebar: notebooks, tags, Recent, Search box.
3. Click note or "New Note" — opens editor (center pane). Title editable inline.
4. Typing triggers autosave with a 2s debounce to storage repository (background thread/task).
5. User selects text (or none) and clicks AI -> chooses preset (e.g., "Rewrite clearer").
6. UI shows non-blocking modal/progress, sends request via `ai.client` with 6s timeout. Network call runs off-main thread; result returns to UI thread.
7. Result displayed in side-by-side diff preview; user Accepts (replace selection/whole note) or Cancels.

Rewrite UX
----------

- Side-by-side diff preview with simple inline highlighting.
- If no selection, treat as whole-note rewrite (but warn if note > 50KB; suggest selecting a snippet).
- User must explicitly confirm Accept for replacing content; Cancel leaves original unchanged.

Concurrency & Threading Model
----------------------------

- UI thread (main): only UI updates and input handling.
- Worker thread(s) / executor: run disk writes (autosave), DB reads/writes for search, and AI network calls.
- Use `concurrent.futures.ThreadPoolExecutor` or `QThread`/`asyncio` depending on UI toolkit (suggestion: `tkinter` for minimal deps or `PySide6` for richer UI; keep decision in research.md).
- All async network calls must support cancellation and timeout; ensure UI displays friendly messages and lets user continue editing.

Storage & Autosave Behavior
--------------------------

- Autosave: debounce 2s on editor change; persist to SQLite via repository API. Also provide explicit Save / Save As.
- If DB file is locked/unavailable, write to a temporary autosave file and show a non-blocking warning.

AI Behavior & Resilience
------------------------

- Azure-only OpenAI: configured via env/keyring.
- Default timeout: 6s; retries: up to 2 retries with backoff (500ms then 1500ms).
- If AI fails or times out: show error toast, allow Retry or Copy Original; never block local save/edit.
- Do not persist raw prompts/responses unless user explicitly chooses to save the result into the note.

Search Strategy
---------------

- Primary: SQLite FTS5 virtual table (notes_fts) indexing title and body.
- Fallback: if SQLite lacks FTS5 support, fallback to indexed LIKE search across title and body columns; repository exposes a `search(query)` that picks best available backend.

Packaging & Distribution
------------------------

- Windows-only MVP using `PyInstaller`. Include a `build/` script demonstrating the build command.
- Ensure packaging step reads secrets from env/keyring at runtime; do not bake secrets into the binary.

Testing Strategy (short)
------------------------

- Unit tests: `pytest` for `storage` (in-memory SQLite), `ai` (mocked HTTP/SDK), and `config` (env/keyring mocks).
- UI tests: smoke tests using a lightweight UI automation or manual checklist for MVP. Prefer to keep UI logic thin to facilitate unit tests of controller code.

Deliverables (created in this feature)
-------------------------------------

- `specs/001-ai-rewrite-notepad/plan.md` (this file) — updated
- `specs/001-ai-rewrite-notepad/data-model.md` — SQL schema and search strategy
- `specs/001-ai-rewrite-notepad/quickstart.md` — setup, env, packaging
- `specs/001-ai-rewrite-notepad/research.md` — short decisions and alternatives

Next Implementation Steps
-------------------------

1. Implement `storage` module and schema (create DB, repository API, migration hooks).
2. Implement `ai` client wrapper that supports Azure OpenAI, timeouts, and retries (mockable transport).
3. Implement minimal `desktop_app` UI wired to storage and ai modules with autosave and rewrite flow.
4. Add tests and CI job skeleton (pytest + ruff/black).
5. Build Windows executable with `PyInstaller` and verify runtime behavior.

- [Module A] now depends on [Library/Module B] for [capability]

Success Criteria (mapped from spec)
----------------------------------

- **SC-001**: Users can create a new note and assign it to a notebook within 2 clicks from the main screen.
- **SC-002**: Search returns relevant results for small datasets (<= 1,000 notes) within 1 second on a typical development machine.
- **SC-003**: Rewriting selected text via the AI assistant returns a result within ~5 seconds under normal network and service conditions (default AI timeout 6s; retry policy documented).
- **SC-004**: The app continues to allow note creation, editing, and saving even when AI services are unavailable (no data loss beyond last autosave).

API Contracts (examples)
------------------------

Define minimal example interfaces here so implementation teams have clear contracts between layers. These are suggestions and should be kept stable or versioned if changed.

- Storage repository (sync/worker-safe):
  - `create_note(title: str, body: str, notebook_id: Optional[int] = None) -> int`
  - `get_note(note_id: int) -> Optional[Dict[str, Any]]`
  - `update_note(note_id: int, title: str, body: str) -> bool`
  - `delete_note(note_id: int) -> bool`
  - `search(query: str) -> List[Dict[str, Any]]`
  - `create_tag(name: str) -> int`, `add_tag_to_note(note_id: int, tag_name: str)`

- AI client (network, injectable transport):
  - `AIClient.rewrite(prompt: str, deployment: Optional[str] = None) -> str`  # may raise RuntimeError on failure
  - `AIClient.log` ephemeral in-memory `AIRequestLog` for diagnostics

- Desktop app (UI-facing controller):
  - `open_note(note_id: int)`, `save_note_async(note_id: int)` — these call `repository` APIs on a worker thread and marshal results to UI thread.

Module Documentation Responsibilities
-------------------------------------

To retain meaning parity and reduce drift, the implementer who modifies a module's public surface (functions, classes, data model) must update that module's `README.md` and `AGENT_INSTRUCTION.md` with:

- A short summary of the change and why it was made.
- Public API changes (signatures, return shapes) and migration notes if applicable.
- Test cases or pointers to relevant tests added/updated.

This ensures module documentation stays in sync with code and helps future maintainers and agents.
