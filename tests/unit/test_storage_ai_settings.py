import sqlite3
from storage import db


def get_in_memory_conn():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    # Apply initial migration SQL from migrations module
    from storage.migrations import INITIAL_SQL

    cur = conn.cursor()
    cur.executescript(INITIAL_SQL)
    # Add our tables that migrations would normally add
    from storage.migrations import apply_initial_migration

    apply_initial_migration(conn)
    return conn


def test_connection_settings_crud():
    conn = get_in_memory_conn()
    settings = db.ConnectionSettings(endpoint='https://example', deployment_id='d1', api_version='2024-10-01', timeout=7, retry_prefs={'retries': 1})
    db.save_connection_settings(conn, settings)
    loaded = db.load_connection_settings(conn)
    assert loaded is not None
    assert loaded.endpoint == settings.endpoint
    assert loaded.timeout == 7


def test_rewrite_modes_crud_and_seed():
    conn = get_in_memory_conn()
    # seed built-ins
    db.seed_builtin_modes(conn)
    modes = db.list_rewrite_modes(conn)
    assert len(modes) >= 2

    # create a new mode
    new_mode = db.RewriteMode(id=None, name='Test Mode', instruction_template='Do X: {text}', enabled=True, order=10, applies_to='selection-only')
    saved = db.save_rewrite_mode(conn, new_mode)
    assert saved.id is not None

    # list and find
    modes = db.list_rewrite_modes(conn)
    assert any(m.name == 'Test Mode' for m in modes)

    # delete
    db.delete_rewrite_mode(conn, saved.id)
    modes = db.list_rewrite_modes(conn)
    assert not any(m.name == 'Test Mode' for m in modes)
