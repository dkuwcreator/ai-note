"""Database connection helpers."""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Iterator
from .migrations import migrate

DEFAULT_DB = Path.home().joinpath('.local', 'share', 'ai_notepad', 'notes.db')

def get_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    db_path = Path(db_path) if db_path else DEFAULT_DB
    migrate(db_path)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def connection_context(db_path: str | Path | None = None) -> Iterator[sqlite3.Connection]:
    conn = get_connection(db_path)
    try:
        yield conn
    finally:
        conn.close()
