"""Database connection helpers."""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Iterator
from .migrations import migrate
import json
from dataclasses import dataclass, asdict
from typing import Optional, List


@dataclass
class ConnectionSettings:
    endpoint: str
    deployment_id: str
    api_version: Optional[str] = None
    timeout: int = 6
    retry_prefs: Optional[dict] = None


@dataclass
class RewriteMode:
    id: Optional[int]
    name: str
    instruction_template: str
    enabled: bool = True
    order: int = 0
    applies_to: str = "selection-only"
    builtin: bool = False
    advanced_settings: Optional[dict] = None


def seed_builtin_modes(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) as c FROM rewrite_modes WHERE builtin=1")
    row = cur.fetchone()
    if row and row['c'] > 0:
        return

    builtins = [
        ("Make more formal", "Rewrite formally: {text}", 1, 'whole-note-default', 1),
        ("Simplify", "Simplify: {text}", 1, 'selection-only', 2),
    ]
    for name, instr, enabled, applies_to, order in builtins:
        cur.execute(
            "INSERT OR IGNORE INTO rewrite_modes (name, instruction_template, enabled, applies_to, \"order\", builtin) VALUES (?, ?, ?, ?, ?, 1)",
            (name, instr, enabled, applies_to, order),
        )
    conn.commit()


def save_connection_settings(conn: sqlite3.Connection, settings: ConnectionSettings) -> None:
    cur = conn.cursor()
    retry_json = json.dumps(settings.retry_prefs) if settings.retry_prefs is not None else None
    # Singleton row with id=1
    cur.execute(
        "INSERT INTO connection_settings (id, endpoint, deployment_id, api_version, timeout, retry_prefs, updated_at) VALUES (1, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP) ON CONFLICT(id) DO UPDATE SET endpoint=excluded.endpoint, deployment_id=excluded.deployment_id, api_version=excluded.api_version, timeout=excluded.timeout, retry_prefs=excluded.retry_prefs, updated_at=CURRENT_TIMESTAMP",
        (settings.endpoint, settings.deployment_id, settings.api_version, settings.timeout, retry_json),
    )
    conn.commit()


def load_connection_settings(conn: sqlite3.Connection) -> Optional[ConnectionSettings]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM connection_settings WHERE id=1")
    row = cur.fetchone()
    if not row:
        return None
    retry = json.loads(row['retry_prefs']) if row['retry_prefs'] else None
    return ConnectionSettings(
        endpoint=row['endpoint'],
        deployment_id=row['deployment_id'],
        api_version=row['api_version'],
        timeout=row['timeout'],
        retry_prefs=retry,
    )


def list_rewrite_modes(conn: sqlite3.Connection) -> List[RewriteMode]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM rewrite_modes ORDER BY \"order\" ASC")
    rows = cur.fetchall()
    modes: List[RewriteMode] = []
    for r in rows:
        adv = json.loads(r['advanced_settings']) if r['advanced_settings'] else None
        modes.append(
            RewriteMode(
                id=r['id'],
                name=r['name'],
                instruction_template=r['instruction_template'],
                enabled=bool(r['enabled']),
                order=int(r['order']),
                applies_to=r['applies_to'],
                builtin=bool(r['builtin']),
                advanced_settings=adv,
            )
        )
    return modes


def save_rewrite_mode(conn: sqlite3.Connection, mode: RewriteMode) -> RewriteMode:
    cur = conn.cursor()
    adv_json = json.dumps(mode.advanced_settings) if mode.advanced_settings is not None else None
    if mode.id is None:
        cur.execute(
            "INSERT INTO rewrite_modes (name, instruction_template, enabled, \"order\", applies_to, builtin, advanced_settings) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (mode.name, mode.instruction_template, int(mode.enabled), mode.order, mode.applies_to, int(mode.builtin), adv_json),
        )
        mode.id = cur.lastrowid
    else:
        cur.execute(
            "UPDATE rewrite_modes SET name=?, instruction_template=?, enabled=?, \"order\"=?, applies_to=?, advanced_settings=? WHERE id=? AND builtin=0",
            (mode.name, mode.instruction_template, int(mode.enabled), mode.order, mode.applies_to, adv_json, mode.id),
        )
    conn.commit()
    return mode


def delete_rewrite_mode(conn: sqlite3.Connection, mode_id: int) -> None:
    cur = conn.cursor()
    # Prevent deleting built-in modes
    cur.execute("DELETE FROM rewrite_modes WHERE id=? AND builtin=0", (mode_id,))
    conn.commit()


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
