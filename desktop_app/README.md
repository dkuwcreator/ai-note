Desktop app module

- Purpose: Tkinter-based minimal UI for editing notes and using the AI rewrite assistant.
- Key files: `main.py`, `ui.py`, `editor.py`.
- Invariants: UI must not block on disk or network operations; use worker threads.
# desktop_app

Minimal Tkinter UI for AI Notepad. Contains editor, sidebar, and UI wiring.
