# Implementation Notes: In-app AI Settings & Rewrite Modes

This document contains engineering and provider-specific guidance that is intentionally separated from the user-facing specification.

- Secrets storage: Prefer using OS-managed secure storage (keyring/credential store) on each platform. If a secure store is unavailable, use an encrypted local store behind explicit user consent and document the tradeoffs.
- Persistence: Persist non-secret settings and rewrite mode metadata in the existing local preferences store. Add a migration that is idempotent and reversible where feasible.
- Test Connection: Use a minimal validation request appropriate for the configured provider to verify authentication and deployment availability. Categorize failures as auth, deployment-not-found, network/timeout, or other.
- Presets: Provide built-in rewrite mode presets in code or as distribution assets; allow users to duplicate and edit them without modifying the originals.
- Security & Git: Provide a recommended `.gitignore` snippet in Settings help and avoid committing any files that contain secrets.
- Backward compatibility: Feature must not change note file formats or interfere with editor flows when AI is not configured.

Provider-specific environment variable names and SDK usage should be documented here if needed for implementation; however, implementation choices must not be exposed in the user-facing spec.
