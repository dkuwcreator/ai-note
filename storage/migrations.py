"""Simple migration runner for initial schema."""
from __future__ import annotations
import sqlite3
from pathlib import Path

INITIAL_SQL = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS notebooks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  notebook_id INTEGER REFERENCES notebooks(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  ai_generated_title INTEGER DEFAULT 0,
  generated_title TEXT,
  generated_summary TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS note_tags (
  note_id INTEGER REFERENCES notes(id) ON DELETE CASCADE,
  tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (note_id, tag_id)
);
CREATE TABLE IF NOT EXISTS recent (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  note_id INTEGER REFERENCES notes(id) ON DELETE CASCADE,
  last_opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS connection_settings (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  endpoint TEXT NOT NULL,
  deployment_id TEXT NOT NULL,
  api_version TEXT,
  timeout INTEGER DEFAULT 6,
  retry_prefs TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rewrite_modes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  instruction_template TEXT NOT NULL,
  enabled INTEGER DEFAULT 1,
  "order" INTEGER NOT NULL,
  applies_to TEXT CHECK(applies_to IN ('selection-only','whole-note-default')) DEFAULT 'selection-only',
  builtin INTEGER DEFAULT 0,
  advanced_settings TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- FTS5 virtual table created conditionally in code if supported
"""

def apply_initial_migration(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.executescript(INITIAL_SQL)
    conn.commit()
    # Try to create FTS5 virtual table if SQLite supports it. Fail gracefully if not.
    try:
        cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(title, body, content='notes', content_rowid='id')")
        # Create triggers to keep notes_fts in sync
        cur.executescript("""
        CREATE TRIGGER IF NOT EXISTS notes_ai_after_insert AFTER INSERT ON notes BEGIN
          INSERT INTO notes_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
        END;
        CREATE TRIGGER IF NOT EXISTS notes_ai_after_update AFTER UPDATE ON notes BEGIN
          INSERT INTO notes_fts(notes_fts, rowid, title, body) VALUES('delete', old.id, old.title, old.body);
          INSERT INTO notes_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
        END;
        CREATE TRIGGER IF NOT EXISTS notes_ai_after_delete AFTER DELETE ON notes BEGIN
          INSERT INTO notes_fts(notes_fts, rowid, title, body) VALUES('delete', old.id, old.title, old.body);
        END;
        """)
        conn.commit()
    except Exception:
        # Older SQLite builds may not support FTS5; continue without it.
        pass

def migrate(db_path: str | Path) -> None:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    try:
        apply_initial_migration(conn)
    finally:
        conn.close()
