"""Configuration loader for Azure OpenAI settings.

This app supports configuring settings via:
- OS environment variables
- a local `.env` file (loaded at runtime)
- persisted DB settings saved from the Settings dialog

Precedence: explicit environment variables > DB settings.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional


def _load_dotenv() -> None:
    """Best-effort load of `.env`.

    This matters for PyInstaller onefile builds because the process working
    directory may not be the repo root.
    """

    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return

    candidates: list[Path] = []
    try:
        candidates.append(Path.cwd() / ".env")
    except Exception:
        pass

    # Repo root during normal development.
    try:
        candidates.append(Path(__file__).resolve().parents[1] / ".env")
    except Exception:
        pass

    # Directory containing the executable for frozen apps.
    try:
        if getattr(sys, "frozen", False):
            candidates.append(Path(sys.executable).resolve().parent / ".env")
    except Exception:
        pass

    for p in candidates:
        if p.exists():
            # override=True so editing `.env` actually affects the app.
            load_dotenv(dotenv_path=str(p), override=True)
            return

class Settings:
    def __init__(self) -> None:
        self.azure_openai_endpoint: Optional[str] = None
        self.azure_openai_deployment: Optional[str] = None
        self.azure_openai_api_version: Optional[str] = None
        self.azure_openai_timeout: Optional[float] = None
        self.azure_openai_api_key: Optional[str] = None

        # Load dotenv first so `os.environ.get(...)` sees it.
        _load_dotenv()

        # Best-effort DB settings (saved via Settings dialog)
        db_settings = None
        try:
            from storage import db as storage_db

            conn = storage_db.get_connection()
            try:
                db_settings = storage_db.load_connection_settings(conn)
            finally:
                conn.close()
        except Exception:
            db_settings = None

        # Start with DB values (if any)
        if db_settings is not None:
            self.azure_openai_endpoint = db_settings.endpoint
            self.azure_openai_deployment = db_settings.deployment_id
            self.azure_openai_api_version = db_settings.api_version
            try:
                self.azure_openai_timeout = float(db_settings.timeout)
            except Exception:
                self.azure_openai_timeout = None

        # Env overrides
        self.azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT") or self.azure_openai_endpoint
        self.azure_openai_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT") or self.azure_openai_deployment
        self.azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION") or self.azure_openai_api_version

        # Timeout can be set via env; DB timeout is already applied above.
        env_timeout = os.environ.get("AZURE_OPENAI_TIMEOUT")
        if env_timeout:
            try:
                self.azure_openai_timeout = float(env_timeout)
            except Exception:
                pass

        # API key: env > keyring (if available)
        self.azure_openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        if not self.azure_openai_api_key:
            try:
                from storage.utils import get_api_key

                self.azure_openai_api_key = get_api_key("ai_notepad", "default")
            except Exception:
                self.azure_openai_api_key = None

    def validate(self) -> None:
        if not self.azure_openai_endpoint or not self.azure_openai_deployment:
            raise RuntimeError("Azure OpenAI endpoint and deployment must be configured")

def get_settings() -> Settings:
    return Settings()
