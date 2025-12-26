# Research & Decisions — Desktop Notepad with AI Rewrite Assistant

Purpose
-------
Record decisions and alternatives for technical unknowns described in the spec.

Decisions
---------

- Decision: Use Python 3.11+ for MVP
  - Rationale: Modern standard library, wide platform support, typing improvements.
  - Alternatives: Lower Python versions (rejected due to typing/runtime improvements).

- Decision: UI toolkit — `tkinter` for MVP
  - Rationale: Ships with Python, minimal dependencies, easier packaging with PyInstaller. Provides adequate widgets for a simple editor and side-by-side preview.
  - Alternatives: `PySide6` / `PyQt` (richer UI, heavier deps) — deferred to post-MVP.

- Decision: Threading model — `concurrent.futures.ThreadPoolExecutor`
  - Rationale: Simple, integrates well with blocking DB and network calls; avoids full async rewrite for UI.
  - Alternatives: `asyncio` + async UI toolkit (more complexity), `QThread` if using Qt.

- Decision: SQLite FTS5 primary, fallback to LIKE
  - Rationale: FTS5 offers best relevance and speed; fallback avoids hard dependency on SQLite build flags.

- Decision: Azure OpenAI only
  - Rationale: Constitution and spec require Azure-only AI.

- Decision: Default AI timeout 6s + retries
  - Rationale: Matches spec; retry policy: exponential backoff starting at 500ms then 1500ms, max 2 retries.

Open Questions (NEEDS CLARIFICATION)
-----------------------------------

- Whether to include a small telemetry opt-in for anonymous usage stats (default: NO — privacy-first).
- Whether to support rich text formatting beyond plaintext/bullets in MVP (default: NO).

Next Steps
----------
- Implement storage schema and repository.
- Implement AI client with injectable transport for easy mocking.
- Build minimal `tkinter`-based UI wiring autosave and rewrite flow.
