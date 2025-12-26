# Quickstart — Desktop Notepad with AI Rewrite Assistant (MVP)

This quickstart shows how to set up a developer environment for the Windows MVP.

Prerequisites
-------------
- Python 3.11+ installed and on PATH
- Virtual environment tool (venv)
- `pip` available

Setup
-----
1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
```

2. Install dependencies (example minimal requirements)

```powershell
pip install -r requirements.txt
```

3. Provide Azure OpenAI configuration via environment variables or OS keyring. Copy the provided template:

```powershell
copy .\specs\001-ai-rewrite-notepad\.env.template .env
# Edit .env to add your endpoint/deployment/key (do NOT commit)
```

Environment variables required (documented in `.env.template`):
- `AZURE_OPENAI_ENDPOINT` — Your Azure OpenAI endpoint (https://...)
- `AZURE_OPENAI_DEPLOYMENT` — Deployment name
- `AZURE_OPENAI_API_KEY` — API key (optional if using OS keyring)

Running the app (dev)
---------------------
- Development run will be provided by `desktop_app/main.py` once implemented. Example:

```powershell
python -m desktop_app.main
```

Testing
-------
- Run unit tests:

```powershell
pytest -q
```

Testing Strategy
----------------
- Unit tests: use `pytest` with an in-memory SQLite database for `storage` tests. Mock the Azure OpenAI client for `ai` module using `pytest-mock` or `unittest.mock`.
- Integration tests (optional): run the app against a local test DB and a mocked AI server to validate end-to-end flows.
- CI: run `ruff`/`black` checks and `pytest` on PRs.

Packaging (Windows MVP)
-----------------------
- Use `PyInstaller` to build a single-folder or one-file executable. Example command (run from repo root):

```powershell
pip install pyinstaller
pyinstaller --noconfirm --clean --onefile -n ai_notepad -p . desktop_app/main.py
```

- Ensure that the runtime finds configuration from environment or OS keyring; do not bundle secrets.

Notes
-----
- Do not commit `.env` or any secrets. Use the OS keyring integration for convenience or CI secret storage for packaging.
