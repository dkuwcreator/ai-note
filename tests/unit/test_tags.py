import sqlite3
from storage import migrations, repository, utils

def test_normalize_tags():
    names = ["  Foo ", "foo", "Bar Baz", "bar   baz"]
    norm = utils.normalize_tags(names)
    assert norm == ["foo", "bar baz"]

def test_tag_crud(tmp_path):
    db_file = tmp_path / "test.db"
    migrations.migrate(db_file)
    conn = sqlite3.connect(str(db_file))
    try:
        nid = repository.create_note("T", "B", conn=conn)
        repository.add_tag_to_note(nid, "  Foo ", conn=conn)
        tags = repository.get_tags_for_note(nid, conn=conn)
        assert tags == ["foo"]
    finally:
        conn.close()
