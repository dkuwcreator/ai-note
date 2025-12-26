"""Minimal repository implementation for notes and notebooks."""
from __future__ import annotations
import sqlite3
from typing import List, Optional, Dict, Any
from .db import get_connection
from .utils import normalize_tag, normalize_tags

def create_notebook(name: str, conn: Optional[sqlite3.Connection] = None) -> int:
    own = conn is None
    if own:
        conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notebooks (name) VALUES (?)", (name,))
    conn.commit()
    nid = cur.lastrowid
    if own:
        conn.close()
    return nid

def list_notebooks(conn: Optional[sqlite3.Connection] = None) -> List[Dict[str, Any]]:
    own = conn is None
    if own:
        conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at, updated_at FROM notebooks ORDER BY name")
    rows = [dict(r) for r in cur.fetchall()]
    if own:
        conn.close()
    return rows

def create_note(title: str, body: str, notebook_id: Optional[int] = None, conn: Optional[sqlite3.Connection] = None) -> int:
    own = conn is None
    if own:
        conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notes (notebook_id, title, body) VALUES (?, ?, ?)",
        (notebook_id, title, body),
    )
    conn.commit()
    nid = cur.lastrowid
    if own:
        conn.close()
    return nid

def get_note(note_id: int, conn: Optional[sqlite3.Connection] = None) -> Optional[Dict[str, Any]]:
    own = conn is None
    if own:
        conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cur.fetchone()
    if own:
        conn.close()
    return dict(row) if row else None

def delete_note(note_id: int, conn: Optional[sqlite3.Connection] = None) -> bool:
    own = conn is None
    if own:
        conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    changed = cur.rowcount > 0
    if own:
        conn.close()
    return changed

def rename_note(note_id: int, new_title: str, conn: Optional[sqlite3.Connection] = None) -> bool:
    return update_note(note_id, new_title, get_note(note_id)["body"], conn=conn)

def touch_recent(note_id: int, conn: Optional[sqlite3.Connection] = None) -> None:
    own = conn is None
    if own:
        conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO recent (note_id, last_opened_at) VALUES (?, CURRENT_TIMESTAMP)", (note_id,))
    conn.commit()
    if own:
        conn.close()

def list_recent(limit: int = 20, conn: Optional[sqlite3.Connection] = None) -> List[Dict[str, Any]]:
    own = conn is None
    if own:
        conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT note_id, last_opened_at FROM recent ORDER BY last_opened_at DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cur.fetchall()]
    if own:
        conn.close()
    return rows

def create_tag(name: str, conn: Optional[sqlite3.Connection] = None) -> int:
    name = normalize_tag(name)
    own = conn is None
    if own:
        conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO tags (name) VALUES (?)", (name,))
        conn.commit()
        tid = cur.lastrowid
    except sqlite3.IntegrityError:
        cur.execute("SELECT id FROM tags WHERE name = ?", (name,))
        tid = cur.fetchone()[0]
    if own:
        conn.close()
    return tid

def add_tag_to_note(note_id: int, tag_name: str, conn: Optional[sqlite3.Connection] = None) -> None:
    tid = create_tag(tag_name, conn=conn)
    own = conn is None
    if own:
        conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)", (note_id, tid))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    if own:
        conn.close()

def get_tags_for_note(note_id: int, conn: Optional[sqlite3.Connection] = None) -> List[str]:
    own = conn is None
    if own:
        conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT t.name FROM tags t JOIN note_tags nt ON t.id = nt.tag_id WHERE nt.note_id = ? ORDER BY t.name", (note_id,))
    rows = [r[0] for r in cur.fetchall()]
    if own:
        conn.close()
    return rows

def update_note(note_id: int, title: str, body: str, conn: Optional[sqlite3.Connection] = None) -> bool:
    own = conn is None
    if own:
        conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE notes SET title = ?, body = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (title, body, note_id),
    )
    conn.commit()
    changed = cur.rowcount > 0
    if own:
        conn.close()
    return changed

def search(query: str, conn: Optional[sqlite3.Connection] = None) -> List[Dict[str, Any]]:
    """Search titles and bodies with FTS5 preferred, fallback to LIKE."""
    own = conn is None
    if own:
        conn = get_connection()
    cur = conn.cursor()
    # Check if notes_fts exists
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notes_fts'")
        if cur.fetchone():
            cur.execute("SELECT notes.id, notes.title, notes.body FROM notes JOIN notes_fts ON notes.rowid = notes_fts.rowid WHERE notes_fts MATCH ? LIMIT 50", (query,))
            rows = [dict(r) for r in cur.fetchall()]
            if own:
                conn.close()
            return rows
    except Exception:
        # fall through to LIKE fallback
        pass

    likeq = f"%{query}%"
    cur.execute("SELECT id, title, body FROM notes WHERE title LIKE ? OR body LIKE ? LIMIT 50", (likeq, likeq))
    rows = [dict(r) for r in cur.fetchall()]
    if own:
        conn.close()
    return rows
