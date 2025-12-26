Storage module

- Purpose: Provide SQLite-backed persistence for notebooks, notes, tags, and recent activity.
- Key files: `db.py`, `migrations.py`, `repository.py`, `utils.py`.
- Invariants: Tags normalized; FTS5 preferred for search with LIKE fallback.
