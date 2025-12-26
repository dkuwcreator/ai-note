import sqlite3
from storage import migrations
from storage import db


def test_rewrite_modes_crud_and_ordering(tmp_path):
    db_file = tmp_path / "modes.db"
    migrations.migrate(db_file)
    conn = sqlite3.connect(str(db_file))
    conn.row_factory = sqlite3.Row
    try:
        # seed builtins
        db.seed_builtin_modes(conn)
        modes = db.list_rewrite_modes(conn)
        assert len(modes) >= 2

        # add a new mode
        new_mode = db.RewriteMode(id=None, name="MyMode", instruction_template="Do: {text}", enabled=True, order=99, applies_to='selection-only', builtin=False)
        saved = db.save_rewrite_mode(conn, new_mode)
        assert saved.id is not None

        # load and check
        modes = db.list_rewrite_modes(conn)
        assert any(m.name == "MyMode" for m in modes)

        # reorder: move new mode to top by setting order 0 and save
        saved.order = 0
        db.save_rewrite_mode(conn, saved)
        modes = db.list_rewrite_modes(conn)
        assert modes[0].name == "MyMode"

        # delete mode
        db.delete_rewrite_mode(conn, saved.id)
        modes = db.list_rewrite_modes(conn)
        assert not any(m.name == "MyMode" for m in modes)
    finally:
        conn.close()
