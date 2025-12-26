Agent instructions for `storage/` module

- Use `pragma user_version` for schema versioning and incremental migrations.
- Keep repository functions thread-safe when opening new connections per call.
- Use in-memory SQLite for unit tests; test both FTS5 and LIKE fallback paths.
