Desktop app module

- Purpose: Tkinter-based minimal UI for editing notes and using the AI rewrite assistant.
- Key files: `main.py`, `ui.py`, `editor.py`.
- Invariants: UI must not block on disk or network operations; use worker threads.
# desktop_app

Minimal Tkinter UI for AI Notepad. Contains editor, sidebar, and UI wiring.

Settings
--------
- Provides a Settings dialog (Qt-based if PySide6 available) for configuring the Azure OpenAI connection and managing rewrite modes.
- Non-secret fields (endpoint, deployment id, api version, timeout) are saved in SQLite via `storage.db`.
- API keys are saved to the OS keyring when available; otherwise the dialog supports an encrypted local fallback protected by a passphrase.
