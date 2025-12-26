import sqlite3
from storage import migrations, repository

def test_create_and_get_note(tmp_path):
    db_file = tmp_path / "test.db"
    migrations.migrate(db_file)
    conn = sqlite3.connect(str(db_file))
    conn.row_factory = sqlite3.Row
    try:
        nid = repository.create_note("Title", "Body", conn=conn)
        note = repository.get_note(nid, conn=conn)
        assert note is not None
        assert note["title"] == "Title"
        assert note["body"] == "Body"
    finally:
        conn.close()


def test_connection_settings_crud(tmp_path):
    db_file = tmp_path / "conn.db"
    # run migrations to create tables
    migrations.migrate(db_file)
    conn = sqlite3.connect(str(db_file))
    conn.row_factory = sqlite3.Row
    try:
        from storage.db import ConnectionSettings, save_connection_settings, load_connection_settings

        cs = ConnectionSettings(endpoint="https://ex", deployment_id="deploy1", api_version="v1", timeout=10, retry_prefs={"r":1})
        save_connection_settings(conn, cs)
        loaded = load_connection_settings(conn)
        assert loaded is not None
        assert loaded.endpoint == cs.endpoint
        assert loaded.deployment_id == cs.deployment_id
        assert loaded.api_version == cs.api_version
        assert loaded.timeout == cs.timeout
        assert loaded.retry_prefs == cs.retry_prefs
    finally:
        conn.close()


def test_settings_dialog_save_flow(monkeypatch, tmp_path):
    # Avoid importing Qt if not available in test env; import the dialog class directly
    from desktop_app.settings_dialog import SettingsDialog
    from PySide6 import QtWidgets

    # Create a dialog instance (no parent)
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    dlg = SettingsDialog()

    # Fill inputs
    dlg.endpoint_input.setText("https://example")
    dlg.deployment_input.setText("deploy")
    dlg.api_version_input.setText("v1")
    dlg.timeout_input.setValue(5)
    dlg.api_key_input.setText("secret-key-123")

    # Monkeypatch storage_utils to force file fallback path and avoid interactive dialogs
    import storage.utils as su

    class DummySU:
        @staticmethod
        def keyring_available():
            return False

        @staticmethod
        def store_api_key(service, username, api_key, fallback_path=None, passphrase=None):
            # ensure path is provided and passphrase given
            assert fallback_path is not None
            assert passphrase
            # write a small marker file
            fallback_path.write_text('ok')
            return 'file'

    monkeypatch.setattr(su, 'keyring_available', DummySU.keyring_available)
    monkeypatch.setattr(su, 'store_api_key', DummySU.store_api_key)

    # Monkeypatch the message boxes and input dialog to auto-consent and provide passphrase
    monkeypatch.setattr(QtWidgets.QMessageBox, 'question', lambda *a, **k: QtWidgets.QMessageBox.Yes)
    monkeypatch.setattr(QtWidgets.QInputDialog, 'getText', lambda *a, **k: ("pw123", True))
    monkeypatch.setattr(QtWidgets.QMessageBox, 'information', lambda *a, **k: None)
    monkeypatch.setattr(QtWidgets.QMessageBox, 'critical', lambda *a, **k: None)
    monkeypatch.setattr(QtWidgets.QMessageBox, 'warning', lambda *a, **k: None)

    # Ensure DB migrations run on a temp DB path under tmp_path
    db_file = tmp_path / 'settings.db'
    monkeypatch.setattr('storage.db.DEFAULT_DB', db_file)

    # Call save (will use monkeypatched storage utils and dialogs)
    dlg._on_save()

    # Verify DB row saved
    import sqlite3
    conn = sqlite3.connect(str(db_file))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM connection_settings WHERE id=1')
    row = cur.fetchone()
    assert row is not None
    assert row['endpoint'] == 'https://example'
    conn.close()
