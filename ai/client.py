"""Minimal AI client wrapper for Azure OpenAI with timeout, retries, and an in-memory request log."""
from __future__ import annotations
import time
from typing import Any, Callable, Optional, List, Dict
import requests
from requests import Response
from config.settings import get_settings
from .retry import retry_loop


class AIRequestLog:
    """Ephemeral in-memory log of AI request attempts for diagnostics and retry handling."""

    def __init__(self) -> None:
        self.entries: List[Dict[str, Any]] = []

    def record(self, prompt: str, attempt: int, success: bool, error: Optional[str] = None) -> None:
        self.entries.append({"prompt": prompt, "attempt": attempt, "success": success, "error": error, "ts": time.time()})


class AIClient:
    def __init__(self, transport: Optional[Callable[..., Response]] = None, timeout: float = 6.0, max_retries: int = 2) -> None:
        self.transport = transport or self._default_transport
        self.timeout = timeout
        self.max_retries = max_retries
        self.settings = get_settings()
        self.log = AIRequestLog()

    def _default_transport(self, url: str, headers: dict, json: dict, timeout: float) -> Response:
        return requests.post(url, headers=headers, json=json, timeout=timeout)

    def _build_urls_and_headers(self, deployment: str) -> (str, dict):
        endpoint = self.settings.azure_openai_endpoint
        api_key = self.settings.azure_openai_api_key
        if not endpoint or not deployment:
            raise RuntimeError("Azure OpenAI endpoint and deployment must be configured")
        # Prefer chat completions route; if not available consumer can use completions path
        chat_url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment}/chat/completions"
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["api-key"] = api_key
        return chat_url, headers

    def rewrite(self, prompt: str, deployment: Optional[str] = None) -> str:
        self.settings = get_settings()
        deployment = deployment or self.settings.azure_openai_deployment
        url, headers = self._build_urls_and_headers(deployment)

        # Build chat-style payload (works with Azure chat completions)
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,
            "temperature": 0.2,
        }

        last_exc: Optional[Exception] = None
        attempt = 0
        # Try initial + retries
        try:
            for delay in retry_loop(self.max_retries):
                attempt += 1
                try:
                    resp = self.transport(url, headers=headers, json=payload, timeout=self.timeout)
                    resp.raise_for_status()
                    data = resp.json()
                    # Azure Chat response shape: {choices: [{message:{content: "..."}}]}
                    if isinstance(data, dict):
                        choices = data.get("choices")
                        if choices and isinstance(choices, list):
                            # try chat message first
                            msg = choices[0].get("message") or {}
                            text = msg.get("content") or choices[0].get("text")
                            result = (text or "").strip()
                            self.log.record(prompt, attempt, True)
                            return result
                        # fallback
                        text = data.get("text") or ""
                        self.log.record(prompt, attempt, True)
                        return text
                except Exception as e:
                    last_exc = e
                    self.log.record(prompt, attempt, False, error=str(e))
                    time.sleep(delay)
            # final attempt without sleeping
            attempt += 1
            resp = self.transport(url, headers=headers, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict):
                choices = data.get("choices")
                if choices and isinstance(choices, list):
                    msg = choices[0].get("message") or {}
                    text = msg.get("content") or choices[0].get("text")
                    result = (text or "").strip()
                    self.log.record(prompt, attempt, True)
                    return result
                text = data.get("text") or ""
                self.log.record(prompt, attempt, True)
                return text
        except Exception as e:
            self.log.record(prompt, attempt or 0, False, error=str(e))
            raise RuntimeError("AI request failed") from (e or last_exc)
