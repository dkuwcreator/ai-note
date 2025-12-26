Storage module

- Purpose: Provide SQLite-backed persistence for notebooks, notes, tags, and recent activity.
- Key files: `db.py`, `migrations.py`, `repository.py`, `utils.py`.
- Invariants: Tags normalized; FTS5 preferred for search with LIKE fallback.
 
## New schema additions for AI Settings feature

- `connection_settings` (singleton row storing non-secret connection fields)
- `rewrite_modes` (user and built-in rewrite mode metadata)

Migration: Run `storage.migrations.migrate(db_path)` to ensure new tables exist. Built-in rewrite modes are seeded by the migration or on first-run health check.

APIs
----
- `save_connection_settings(conn, ConnectionSettings)` and `load_connection_settings(conn)` manage non-secret AI connection configuration.
- `save_rewrite_mode(conn, RewriteMode)`, `list_rewrite_modes(conn)`, and `delete_rewrite_mode(conn, id)` manage rewrite mode CRUD. Built-in modes are protected from edits/deletes.
