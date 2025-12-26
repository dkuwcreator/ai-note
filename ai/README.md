AI module

- Purpose: Wrap Azure OpenAI calls with timeouts and retry logic.
- Key files: `client.py`, `presets.py`, `retry.py`.
- Notes: Azure-only by default; `AIClient` provides an in-memory `AIRequestLog` for diagnostics.

Additional features
-------------------
- `AIClient.test_connection()` provides a lightweight categorized health check (ok/auth_error/timeout/other) for UI integration.
- Rewrite modes are applied by building prompts via `ai.presets` and invoking `AIClient.rewrite()`.
