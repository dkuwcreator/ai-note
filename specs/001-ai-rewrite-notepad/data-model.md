# Data Model — Desktop Notepad with AI Rewrite Assistant

Overview
--------
Single-file SQLite database storing notebooks, notes, tags, and recent activity. Primary search via FTS5 virtual table for `title` and `body`. If FTS5 unavailable, repository falls back to LIKE-based indexed search.

Tables
------

1. `notebooks`
   - `id` INTEGER PRIMARY KEY AUTOINCREMENT
   - `name` TEXT NOT NULL
   - `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   - `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

2. `notes`
   - `id` INTEGER PRIMARY KEY AUTOINCREMENT
   - `notebook_id` INTEGER REFERENCES notebooks(id) ON DELETE SET NULL
   - `title` TEXT NOT NULL
   - `body` TEXT NOT NULL
   - `ai_generated_title` BOOLEAN DEFAULT 0
   - `generated_title` TEXT NULL
   - `generated_summary` TEXT NULL
   - `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   - `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

3. `tags`
   - `id` INTEGER PRIMARY KEY AUTOINCREMENT
   - `name` TEXT NOT NULL UNIQUE -- stored normalized (trim, collapse spaces, lower)

4. `note_tags` (many-to-many)
   - `note_id` INTEGER REFERENCES notes(id) ON DELETE CASCADE
   - `tag_id` INTEGER REFERENCES tags(id) ON DELETE CASCADE
   - PRIMARY KEY (`note_id`, `tag_id`)

5. `recent` (lightweight MRU list)
   - `id` INTEGER PRIMARY KEY AUTOINCREMENT
   - `note_id` INTEGER REFERENCES notes(id) ON DELETE CASCADE
   - `last_opened_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Full-Text Search Strategy
-------------------------
- Preferred: FTS5 virtual table `notes_fts` with `content='notes'` and external content synchronization or triggers. Indexes on `title` and `body`.
- FTS5 schema example:

  CREATE VIRTUAL TABLE notes_fts USING fts5(title, body, content='notes', content_rowid='id');

- Synchronization: on insert/update/delete of `notes`, update `notes_fts` via triggers or through repository logic.

Fallback Strategy (if FTS5 not available)
----------------------------------------
- Use indexed LIKE searches. Create indexes on `title` and `updated_at` and use `WHERE title LIKE ? OR body LIKE ?` with parameterized queries.
- Because `body` is often large, consider searching only the first N characters or use `instr(body, ?) > 0` for faster short-circuit checks.

Indexes
-------
- `CREATE INDEX idx_notes_notebook ON notes(notebook_id);`
- `CREATE INDEX idx_notes_updated_at ON notes(updated_at);`
- `CREATE INDEX idx_tags_name ON tags(name);`
- `CREATE INDEX idx_recent_note ON recent(note_id);`

Migration Notes
---------------
- Schema versioning: store a `pragma user_version` and provide `storage/migrations.py` that applies incremental migrations.
- Initial migration: create tables above and FTS5 virtual table if the runtime SQLite supports it.

Invariants
----------
- Tags must be normalized before insertion (trim, collapse spaces, lowercase).
- `notes` updates must update `updated_at` and synchronize `notes_fts` if present.
- Autosave writes should be idempotent and safe to call concurrently from worker threads.

Testing Notes
-------------
- Use in-memory SQLite (`sqlite://:memory:`) for unit tests.
- For FTS5 tests, ensure the runtime SQLite linked to the test environment supports FTS5; otherwise, test fallback logic explicitly.
