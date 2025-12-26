AI module

- Purpose: Wrap Azure OpenAI calls with timeouts and retry logic.
- Key files: `client.py`, `presets.py`, `retry.py`.
- Notes: Azure-only by default; `AIClient` provides an in-memory `AIRequestLog` for diagnostics.
