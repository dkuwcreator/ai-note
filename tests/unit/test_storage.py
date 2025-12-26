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
