Config module

- Purpose: Load configuration and secrets from environment or OS keyring.
- Key files: `settings.py`.
- Invariants: Do not print or persist secrets; provide `.env.template` for developer convenience.
