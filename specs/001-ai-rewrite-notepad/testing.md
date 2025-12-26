# Testing Strategy — Desktop Notepad with AI Rewrite Assistant

Overview
--------
Testing focuses on separating UI from core logic so storage and AI behavior can be unit tested deterministically.

Unit Tests
----------
- `storage`:
  - Use in-memory SQLite for fast tests.
  - Test CRUD, tag normalization, autosave debounce logic (simulate repeated updates), and FTS5 vs fallback behavior.

- `ai`:
  - Inject a mock transport into the `ai.client` to simulate Azure responses, timeouts, and errors.
  - Test retry/backoff, timeout handling, and graceful degradation paths that surface errors to the caller.

- `config`:
  - Test env var loading and OS keyring fallback using mocks.

Integration & UI Tests
----------------------
- Minimal smoke tests to ensure the app starts, creates a note, autosaves, and triggers an AI rewrite flow using a mocked AI client.
- End-to-end tests can be run locally with a test DB and a local mock server for AI.

CI Recommendations
------------------
- Run `pytest` and `ruff`/`black` on pull requests.
- Do not include real secrets in CI; use secret variables and mock AI endpoints.

Tools
-----
- `pytest`, `pytest-mock` or `unittest.mock`, `sqlite3` (std lib), optional `pytest-qt` if Qt chosen later.
