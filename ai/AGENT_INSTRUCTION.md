Agent instructions for `ai/` module

- Keep AI requests Azure-only and avoid logging secrets.
- Ensure network calls are easily mockable via the `transport` argument to `AIClient`.
- Respect a default timeout of 6s and at most 2 retries with exponential backoff.
