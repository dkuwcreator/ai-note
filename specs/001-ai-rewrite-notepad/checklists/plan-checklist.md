# Plan Verification Checklist — Desktop Notepad with AI Rewrite Assistant

Purpose: Unit-test the quality of `plan.md` (requirements alignment, architecture clarity, storage/search strategy, UX flows, AI behavior, autosave, security, testing, packaging).

**Notes**: Items are objectively verifiable yes/no checks. Each item lists how to verify and whether it is Must (MVP blocker) or Nice-to-have.

## 1) Plan Completeness & Alignment

- [x] CHK001 - Does `plan.md` explicitly reference and align with the feature `spec.md` non-negotiables (Local-First Storage, Azure-Only AI, Privacy By Default)? [Must]
  - How to verify: Open `specs/001-ai-rewrite-notepad/spec.md` and `plan.md` and confirm the three principles are present verbatim or paraphrased in plan; answer yes/no.

- [x] CHK002 - Are module boundaries for `desktop_app`, `storage`, `ai`, and `config` clearly declared with responsibilities in `plan.md`? [Must]
- How to verify: Confirm `plan.md` lists modules and contains responsibility bullets for each; answer yes/no.

- [x] CHK003 - Does the plan include measurable acceptance criteria mapping to the spec's success criteria (e.g., rewrite <5s, search <1s for <=1000 notes)? [Must]
- How to verify: Search `plan.md` for numeric targets matching `spec.md` SC-002/SC-003/SC-004; answer yes/no.

- [x] CHK004 - Are documentation/mirroring tasks (README.md and AGENT_INSTRUCTION.md updates) required for each impacted module in the plan? [Must]
- How to verify: Check `plan.md` for a "Module Documentation Tasks" or "Meaning Parity" section mentioning README.md/AGENT_INSTRUCTION.md; answer yes/no.

- [x] CHK005 - Does the plan specify clear API boundaries (methods or service contracts) between `desktop_app` ↔ `storage` and `desktop_app` ↔ `ai`? [Must]
- How to verify: Look for explicit example interfaces (e.g., `repository.save_note(note)`, `ai.client.rewrite(text, preset)`) or an interface description in `plan.md`; answer yes/no.

- [x] CHK006 - Are data flow and dependency directions documented (which module calls which)? [Must]
- How to verify: Confirm the plan shows dependency arrows or text describing that `desktop_app` depends on `storage` and `ai`, and `ai` depends on `config`; answer yes/no.

- [x] CHK007 - Are required module-level docs and update responsibilities listed (who updates README/AGENT_INSTRUCTION when code changes)? [Nice-to-have]
- How to verify: Check the plan for a "Module Documentation Tasks" checklist; answer yes/no.

- [x] CHK017 - Does the plan address large-note behavior and selection vs whole-note rewrite rules and warnings? [Nice-to-have]
- How to verify: Look for note-size thresholds or user guidance for large notes in `plan.md`; answer yes/no.

- [x] CHK006 - Are data flow and dependency directions documented (which module calls which)? [Must]
- How to verify: Confirm the plan shows dependency arrows or text describing that `desktop_app` depends on `storage` and `ai`, and `ai` depends on `config`; answer yes/no.

## 3) Storage & Search

- [x] CHK008 - Is the SQLite schema defined or referenced in `data-model.md` (tables for notebooks, notes, tags, note_tags, recent)? [Must]
  - How to verify: Open `data-model.md` and confirm required tables are present; answer yes/no.

- [x] CHK009 - Does the plan require schema versioning and migrations (e.g., `pragma user_version` + migrations module)? [Must]
  - How to verify: Confirm `plan.md` or `data-model.md` mentions `migrations.py`, `pragma user_version`, or similar; answer yes/no.

- [x] CHK010 - Is FTS5 the primary search approach with an explicit automatic fallback to LIKE when FTS5 is unavailable? [Must]
  - How to verify: Verify `plan.md` and `data-model.md` describe creating an FTS5 virtual table and describe the fallback; answer yes/no.

- [x] CHK011 - Are necessary indexes listed (e.g., indexes on `notes.notebook_id`, `notes.updated_at`, `tags.name`)? [Nice-to-have]
  - How to verify: Check `data-model.md` for `CREATE INDEX` entries; answer yes/no.

- [x] CHK012 - Is the Recent/MRU storage behavior specified and mapped to schema? [Nice-to-have]
  - How to verify: Confirm `data-model.md` includes a `recent` table or an explained mechanism; answer yes/no.

## 4) UI Flows & UX

- [x] CHK013 - Does the plan describe the create/edit/save flow, including explicit Save / Save As actions and autosave behavior? [Must]
  - How to verify: Confirm `plan.md` describes New Note, editor, autosave debounce, and explicit Save/Save As; answer yes/no.

- [x] CHK014 - Are notebook and tag creation, assignment, and filtering flows described? [Must]
  - How to verify: Check `plan.md` for sidebar behavior: notebooks, tags, and filtering by tag/notebook; answer yes/no.

- [x] CHK015 - Is the quick search UI flow described (search box, expected interaction, result ordering)? [Must]
  - How to verify: Confirm `plan.md` lists quick search in sidebar and expected result ordering (e.g., by recent activity); answer yes/no.

- [x] CHK016 - Is the rewrite UX specified as side-by-side diff preview with explicit Accept/Cancel semantics? [Must]
  - How to verify: Verify `plan.md` contains a "Rewrite UX" section describing side-by-side diff and explicit confirmation; answer yes/no.

- [x] CHK017 - Does the plan address large-note behavior and selection vs whole-note rewrite rules and warnings? [Nice-to-have]
  - How to verify: Look for note-size thresholds or user guidance for large notes in `plan.md`; answer yes/no.

## 5) Non-blocking Behavior

- [x] CHK018 - Does the plan mandate that UI thread must not perform blocking DB or network I/O? [Must]
  - How to verify: Confirm `plan.md` contains an explicit invariant that UI must not block and recommends background workers; answer yes/no.

- [x] CHK019 - Is a threading model proposed and mapped to chosen UI toolkit (e.g., `ThreadPoolExecutor` + guidance for `tkinter`/`Qt`)? [Must]
  - How to verify: Check `plan.md` and `research.md` for threading model details and toolkit guidance; answer yes/no.

- [x] CHK020 - Are AI calls cancellable/time-limited and do they surface non-blocking UI feedback (progress/toast)? [Must]
  - How to verify: Confirm `plan.md` describes timeouts (6s), retries and non-blocking progress UI; answer yes/no.

## 6) AI Integration

- [x] CHK021 - Does the plan enforce Azure OpenAI only (no public OpenAI fallback) and list required env vars? [Must]
  - How to verify: Confirm `plan.md` and `research.md` state "Azure-only" and `quickstart.md` or `.env.template` lists `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`, `AZURE_OPENAI_API_KEY`; answer yes/no.

- [x] CHK022 - Is the default timeout (6s) and retry policy (exponential backoff: 500ms, 1500ms, max 2 retries) documented? [Must]
  - How to verify: Check `plan.md` for the timeout and retry policy; answer yes/no.

- [x] CHK023 - Does the plan specify structured error handling for AI failures (error type, message, retry hint) and UI fallback options? [Must]
  - How to verify: Look for an error handling section describing error shapes and UI options (retry, copy original, informative toast); answer yes/no.

- [x] CHK024 - Are prompts/responses treated as ephemeral and not persisted by default? [Must]
  - How to verify: Confirm `plan.md` and `constitution.md` say prompts/responses are not persisted unless user explicitly saves them; answer yes/no.

## 7) Autosave & Persistence

- [x] CHK025 - Is autosave debounce set to ~2s and described clearly (coalescing changes to reduce write frequency)? [Must]
  - How to verify: Check `plan.md` for autosave debounce value, wording about coalescing writes; answer yes/no.

- [x] CHK026 - Are error scenarios for DB write failures specified (e.g., DB locked -> temporary autosave file)? [Nice-to-have]
  - How to verify: Verify `plan.md` or `data-model.md` describes fallback behavior for DB locks or failures; answer yes/no.

- [x] CHK027 - Does the plan require explicit Save and Save As actions in addition to autosave? [Must]
  - How to verify: Confirm `plan.md` lists Save and Save As capabilities; answer yes/no.

## 8) Security & Privacy

- [x] CHK028 - Does the plan require secrets not be committed and provide `.env.template` without secrets? [Must]
  - How to verify: Confirm `.env.template` exists in feature folder and contains placeholders but no secrets; answer yes/no.

- [x] CHK029 - Is optional OS keyring usage documented as an alternative to env vars? [Nice-to-have]
  - How to verify: Look for keyring mention in `plan.md` or `research.md`; answer yes/no.

- [x] CHK030 - Is telemetry disabled by default and any collection explicitly opt-in? [Must]
  - How to verify: Confirm `constitution.md` and `plan.md` state privacy-by-default and no telemetry unless opt-in; answer yes/no.

## 9) Observability

- [x] CHK031 - Does the plan require local logging for failures and AI errors (log file or local console) for diagnosis? [Must]
  - How to verify: Check `plan.md` for logging requirements and suggested log locations; answer yes/no.

- [x] CHK032 - Are latency tracking and simple failure counters suggested for AI & search components? [Nice-to-have]
  - How to verify: Look for instrumentation suggestions in `plan.md` or `testing.md`; answer yes/no.

- [x] CHK033 - Is explicit guidance included to avoid sending logs/prompts to external telemetry by default? [Must]
  - How to verify: Confirm `plan.md` and `constitution.md` restrict external telemetry and require opt-in; answer yes/no.

## 10) Testing & Packaging Readiness

- [x] CHK034 - Does the plan specify unit tests for `storage` (in-memory SQLite) and `ai` (mocked transport) and include test guidance? [Must]
  - How to verify: Confirm `testing.md` mentions in-memory SQLite tests and mocking the AI client; answer yes/no.

- [x] CHK035 - Is there a `quickstart.md` with setup and packaging notes and a `.env.template` for devs? [Must]
  - How to verify: Verify `quickstart.md` and `.env.template` exist in the feature folder; answer yes/no.

- [x] CHK036 - Does the plan provide a PyInstaller packaging path or build script for the Windows MVP (command example and notes about secrets)? [Must]
  - How to verify: Confirm `quickstart.md` or `plan.md` includes a `pyinstaller` build command or `build/` script; answer yes/no.

## Plan Gaps vs spec.md (flagged issues)

- Toolkit choice clarity: `research.md` recommends `tkinter`, but `plan.md` phrases it as a suggestion. If the project requires a firm UI toolkit decision before implementation, this is a gap. [Flag]
- Migration function and API shapes: `plan.md` indicates migrations required but does not provide a minimal migration API contract (e.g., `migrate(conn, from_version)`); beneficial to add. [Flag]
- Concrete AI error schema: plan references showing errors and retries but does not define a structured error response shape (fields: `code`, `message`, `transient:boolean`, `retry_after_ms`). Recommend adding. [Flag]
- Packaging script absence: `quickstart.md` has a `pyinstaller` example, but no checked-in `build/` script or `build.ps1`. Add as blocker for reproducible packaging. [Flag]
- Threading integration for chosen toolkit: plan suggests `ThreadPoolExecutor` but lacks concrete guidance for integrating with `tkinter` event loop (e.g., `after()` scheduling). Recommend adding per-toolkit examples. [Flag]

## Top 5 Blockers (items that block /speckit.tasks if not addressed)

1. Missing concrete AI error schema and handling contract (see CHK023) — Must.
2. No checked-in packaging/build script for PyInstaller (see CHK036) — Must.
3. Migration API contract not defined (see CHK009) — Must.
4. Threading integration guidance per chosen UI toolkit not fully specified (see CHK019) — Must.
5. Enforcement language for Azure-only AI is present, but verification tests and CI checks to prevent accidental public OpenAI usage are not defined — Must.

## Go/No-Go Gate for starting /speckit.tasks

- Gate Rule: All Must items above (every CHK marked [Must]) must be YES to Go. Any NO → No-Go.
- Current assessment: Multiple Must items are present across the checklist. If any of the following remain NO: CHK001, CHK002, CHK003, CHK005, CHK008, CHK009, CHK010, CHK013, CHK014, CHK015, CHK016, CHK018, CHK019, CHK020, CHK021, CHK022, CHK023, CHK024, CHK025, CHK027, CHK028, CHK030, CHK031, CHK033, CHK034, CHK035, CHK036 — then the plan should not move to `/speckit.tasks` until those are YES.

Create Date: 2025-12-25
Checklist File: `specs/001-ai-rewrite-notepad/checklists/plan-checklist.md`
