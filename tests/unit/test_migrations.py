import tempfile
from storage import migrations


def test_migrate_creates_db(tmp_path):
    db_file = tmp_path / "test.db"
    migrations.migrate(str(db_file))
    assert db_file.exists()
