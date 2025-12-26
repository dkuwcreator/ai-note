import sqlite3
from storage import migrations, repository

def test_search_fallback(tmp_path):
    db_file = tmp_path / "test.db"
    migrations.migrate(db_file)
    conn = sqlite3.connect(str(db_file))
    conn.row_factory = sqlite3.Row
    try:
        nid = repository.create_note("Hello", "This is a unique phrase: purple unicorn", conn=conn)
        results = repository.search("purple unicorn", conn=conn)
        assert any("purple unicorn" in (r.get("body") or "") for r in results)
    finally:
        conn.close()
