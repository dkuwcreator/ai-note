# Feature Specification: Desktop Notepad with AI Rewrite Assistant

**Feature Branch**: `001-ai-rewrite-notepad`  
**Created**: 2025-12-24  
**Status**: Draft  
**Input**: User description: "Build a very simple desktop notepad application with an AI rewrite assistant and organized storage. Target user: a single user who wants to write snippets/notes and organize them quickly. Core UX: create/edit notes, organize by notebooks and tags, quick search, AI rewrite assistant with presets, save/rename/delete, auto-save, recent notes. Constraints: Desktop Python app, AI must use Azure OpenAI deployment, local organized storage (not loose txt files), MVP small and fast to implement. Success: notes create/organize/search in 2 clicks, rewrite returns <5s, graceful degradation if AI fails, no secrets in source control."

## Semantic Scope *(Required)*

<!--
  CRITICAL: Define the semantic boundaries for this feature to enable safe Human-AI collaboration.
  This section enforces bounded context principles and prevents unintended cross-module changes.
  
  Reference: https://github.com/dkuwcreator/Semantic-Architecture
-->

### Modules In Scope

- **desktop_app/**
  - **Responsibility**: The UI layer for the desktop application (main editor, sidebar, menus).
  - **Impact**: Add note editor view, left sidebar with notebooks/tags, quick search UI, recent notes view, and AI rewrite controls.

- **storage/**
  - **Responsibility**: Local persistence for notes and metadata.
  - **Impact**: Add a lightweight local storage module (SQLite) with a simple schema for notebooks, notes, tags, and recent items. Provide migration notes.

- **ai/**
  - **Responsibility**: Abstraction layer for AI interactions.
  - **Impact**: Implement Azure OpenAI client wrapper that sends rewrite requests to a configured Azure deployment and handles timeouts, retries, and graceful degradation.

- **config/**
  - **Responsibility**: Load runtime configuration and secrets from environment or OS keyring.
  - **Impact**: Add configuration keys for `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`, and `AZURE_OPENAI_API_KEY` (read-only at runtime). Ensure secrets are never checked into source control.

### Constitution Alignment

- Local-First Storage: Notes and metadata will be stored locally using SQLite (single-file DB) with migration notes included in the storage module.
- Azure-Only AI: All AI calls will be made to an Azure OpenAI deployment. Required configuration keys: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`, `AZURE_OPENAI_API_KEY`. Public OpenAI endpoints are disallowed in this spec.
- Privacy By Default: Prompts and AI responses are treated as ephemeral — not persisted by default. The app may store derived user preferences (e.g., last used rewrite preset) but not raw prompts/responses unless explicitly approved by the user.
- Security: Secrets are loaded from environment variables or the OS keyring. The codebase will include example config loading but must not include any real secrets in source control.

### Modules Explicitly Out Of Scope

- **sync/**: Sync, cloud storage, or user account management are out of scope for MVP.
- **media/**: Images, attachments, and rich media support are out of scope.
- **collaboration/**: Sharing, multi-user, and real-time collaboration are out of scope.

### Cross-Module Impacts

**Module Dependencies**:

- `desktop_app` depends on `storage` for note persistence and `ai` for rewrite operations.
- `ai` depends on `config` for secure endpoint and deployment configuration.

**Compatibility Requirements**:

- Storage schema changes must include a migration function; initial schema will be simple and backwards compatible for small changes.

**Migration Notes**:

- Initial MVP uses a single SQLite file stored in the user's application data folder. If future versions change schema, the storage module should provide a migration path.

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

## Clarifications

### Session 2025-12-24

## User Scenarios & Testing

- Q: Tags model → A: Free-form tags with normalization (accepted) — Rationale: lowest friction for users; storage normalizes tags and UI offers suggestions from existing tags.
- Q: Search approach → A: SQLite FTS5 full-text search (accepted) — Rationale: FTS5 provides better full-text relevance and scales well for note bodies; fall back to LIKE when FTS5 is unavailable.

- Q: Version history → A: No version history in MVP (accepted) — Rationale: keep MVP storage and UX simple; consider snapshot history in a later iteration.

- Q: Rewrite UX → A: Side-by-side diff with user confirmation to replace (accepted) — Rationale: non-destructive preview gives users control; replace only after explicit confirmation.

- Q: Secret handling → A: Environment variables + optional OS keyring (accepted) — Rationale: secure, no secrets in source control; document both methods in README.
- Q: Packaging target → A: Windows-only MVP with cross-platform plan (accepted) — Rationale: simplifies initial packaging and testing; cross-platform support planned after MVP.

### User Story 1 - Create and Edit Notes (Priority: P1)

As a user, I can create a new note, edit it in the main editor, and save it to a chosen notebook so I can organize my snippets quickly.

**Why this priority**: Core value — without create/edit/save the app is not useful.

**Independent Test**: Open the app, click "New Note", type text, assign a notebook, and save. Verify the note appears in the notebook list and persists after restart.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** the user clicks "New Note", **Then** a blank editor opens and a note record is created in storage (auto-save enabled).
2. **Given** a note is open, **When** the user types and then closes the app, **Then** the latest content is preserved via auto-save and visible on next launch.

---

### User Story 2 - Organize Notes by Notebooks & Tags (Priority: P1)

As a user, I can create notebooks (folders) and add tags to notes. I can view notes filtered by notebook or tag from the left sidebar.

**Why this priority**: Organization is a core requirement for discoverability and quick access.

**Independent Test**: Create a notebook, add several notes and tags, then filter by notebook and by tag to confirm correct lists.

**Acceptance Scenarios**:

1. **Given** a set of notes with notebooks/tags, **When** the user selects a notebook, **Then** only notes in that notebook are shown.
2. **Given** notes have tags, **When** the user clicks a tag, **Then** only notes containing that tag are shown.

---

### User Story 3 - Quick Search Across All Notes (Priority: P1)

As a user, I can run a quick search from the sidebar that searches note titles and bodies and returns results within 2 clicks.

**Why this priority**: Search enables quick retrieval — critical for the stated success criteria.

**Independent Test**: Add notes with unique phrases and run a search for the phrase. Verify results are accurate and returned quickly.

**Acceptance Scenarios**:

1. **Given** multiple notes, **When** the user enters a search term and presses Enter, **Then** matching notes are shown ordered by recent activity.

---

### User Story 4 - AI Rewrite Assistant (Priority: P1)

As a user, I can select text (or whole note) and choose a rewrite action ("Rewrite clearer", "Shorten", "Make more formal", "Fix grammar", "Bullet points"). The assistant returns rewritten text which I can insert or copy.

**Why this priority**: This is the primary differentiator of the app (value-add).

**Independent Test**: Select text, choose a rewrite action, and verify the app displays a transformed text result within ~5s and allows replace/copy.

**Acceptance Scenarios**:

1. **Given** valid text selected, **When** the user requests a rewrite action, **Then** the app sends the request to Azure OpenAI and, on success, displays rewritten text.
2. **Given** the AI call fails or times out, **When** the user attempts a rewrite, **Then** the app shows an informative error and allows retry or copy original text.

---

### User Story 5 - Save, Rename, Delete Notes + Recent View (Priority: P2)

As a user, I can manually save, rename, delete notes, and view a list of recent notes for quick access.

**Why this priority**: Secondary but necessary for basic file management.

**Independent Test**: Create notes, rename one, delete one, and open the Recent list to confirm ordering.

**Acceptance Scenarios**:

1. **Given** a note exists, **When** the user renames it, **Then** the new name is persisted.
2. **Given** a note is deleted, **When** the user confirms deletion, **Then** the note is removed from storage and lists.

---

### Edge Cases

- AI request returns an error or times out: app shows error toast, logs the failure, and preserves note state for retry.
- Storage file is locked or unavailable: app warns user and attempts to save to a temporary autosave file.
- User performs rewrite with empty selection: app treats it as whole-note rewrite.
- Large notes (>100KB): warn about possible AI latency and allow partial-selection rewrite.

## Requirements *(mandatory)*

### Functional Requirements (consolidated)

- **FR-001**: The system MUST provide a main text editor where users can create and edit notes (supports plain text and basic formatting like newlines and bullets).
- **FR-002**: The system MUST allow users to create, rename, and delete notebooks (folders) and assign notes to notebooks.
- **FR-003**: The system MUST support tags for notes and allow filtering by tag. Tags are free-form strings by default; the storage layer MUST normalize tags (trim whitespace, collapse internal whitespace, lowercase) and de-duplicate them at assignment time. The UI SHOULD offer suggestions from existing tags when adding tags.
- **FR-004**: The system MUST persist notes, notebooks, tags, and metadata locally in a single SQLite database file.
- **FR-005**: The system MUST provide a quick search that searches note titles and bodies and returns results within acceptable latency for small datasets (sub-second typical on modern machines). The storage/search implementation SHOULD use SQLite FTS5 full-text search for note bodies and titles by default to provide better relevance and performance; if FTS5 is unavailable on a target platform, the system MUST fall back to a simple indexed LIKE search.
- **FR-006**: The system MUST provide an AI rewrite assistant accessible from the editor with the predefined actions: "Rewrite clearer", "Shorten", "Make more formal", "Fix grammar", "Bullet points".
- **FR-007**: The AI rewrite assistant MUST call an Azure OpenAI deployment using configuration from environment or OS keyring and must include a configurable timeout (default 6s) and retry behavior. Retry policy: exponential backoff starting at 500ms, then 1500ms; max 2 retries.
- **FR-008**: The system MUST autosave note edits by default (on change with a short debounce, e.g., 2s) and also provide explicit `Save` and `Save As` actions. Autosave MUST persist to the local SQLite store to avoid data loss.
- **FR-009**: The system MUST provide a Recent view listing recently opened/edited notes.
- **FR-010**: The system MUST gracefully handle AI failures by showing an error and allowing the user to continue editing and saving notes locally.
- **FR-011**: The system SHOULD attempt to generate an AI-derived title and basic metadata (summary and suggested tags) on first save using the AI rewrite/assistant pipeline. Generated title/metadata MUST be editable by the user before finalizing. If AI generation fails or times out, the system MUST fall back to a user-editable placeholder title (e.g., "Untitled") and leave metadata blank.
- **FR-012**: The system SHOULD NOT implement persistent version history in the MVP. Versioning (snapshots or diffs) may be introduced in a later release as an optional feature.
- **FR-013**: The system MUST display AI rewrite results in a side-by-side diff preview; after review the user may accept to replace selection or cancel (rewrite UX).
- **FR-014**: Secrets for Azure OpenAI configuration MUST be loadable from environment variables (`AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`, `AZURE_OPENAI_API_KEY`). The system SHOULD optionally support reading secrets from the OS keyring for convenience. The README MUST document both approaches.
- **FR-015**: Packaging target: The MVP SHALL target Windows packaging (for example using PyInstaller) to simplify distribution and testing. The project MUST include documentation and a migration plan for adding macOS and Linux packaging in a subsequent release.

### Key Entities

- **Notebook**: Represents a collection of notes. Attributes: id, name, created_at, updated_at.
- **Note**: Represents a single note. Attributes: id, notebook_id, title, body, tags (many-to-many), created_at, updated_at.
- **Tag**: Label attached to notes. Attributes: id, name. Tags are free-form (user-entered) and stored normalized; future work may add an optional controlled vocabulary feature.
- **AIRequestLog (ephemeral)**: Non-persisted runtime entry used for retry/timeout handling; not stored by default.

-- Additional Note attributes added for AI metadata:

- **Note (extended attrs)**: `generated_title` (nullable string), `ai_generated_title` (boolean), `generated_summary` (nullable string). These fields record AI-proposed title/summary and whether they were generated; user edits update `title` and set `ai_generated_title` to false.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can create a new note and assign it to a notebook within 2 clicks from the main screen.
- **SC-002**: Search returns relevant results for small datasets (<= 1,000 notes) within 1 second on a typical development machine.
- **SC-003**: Rewriting selected text via the AI assistant returns a result within ~5 seconds under normal network and service conditions (default AI timeout 6s, with graceful fallback if exceeded).
- **SC-004**: The app continues to allow note creation, editing, and saving even when AI services are unavailable (no data loss beyond last autosave).
