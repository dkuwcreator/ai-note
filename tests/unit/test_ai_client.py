import pytest

from ai.client import AIClient
from ai.presets import build_prompt


class DummyResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json = json_data or {"choices": [{"text": "ok"}]}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("http error")

    def json(self):
        return self._json


def test_build_prompt_known():
    p = build_prompt("fix_grammar", "This is a test.")
    assert "Fix grammar" in p or "Fix" in p


def test_ai_client_success_on_first_try(monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.azure.com")
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "test-deploy")

    def transport(url, headers, json, timeout):
        return DummyResponse()

    client = AIClient(transport=transport, timeout=1.0, max_retries=2)
    out = client.rewrite("hello world")
    assert out == "ok"


def test_ai_client_retries_then_success(monkeypatch):
    calls = {"n": 0}
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.azure.com")
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "test-deploy")

    def transport(url, headers, json, timeout):
        calls["n"] += 1
        if calls["n"] < 2:
            # simulate transient error
            raise Exception("transient")
        return DummyResponse()

    client = AIClient(transport=transport, timeout=1.0, max_retries=2)
    out = client.rewrite("hello world")
    assert out == "ok"
    assert calls["n"] >= 2


def test_ai_client_fail_all_retries():
    def transport(url, headers, json, timeout):
        raise Exception("down")

    client = AIClient(transport=transport, timeout=0.1, max_retries=1)
    with pytest.raises(RuntimeError):
        client.rewrite("x")
import json
from ai.client import AIClient

class DummyResp:
    def __init__(self, status=200, data=None):
        self.status = status
        self._data = data or {"choices": [{"text": "revised text"}]}

    def raise_for_status(self):
        if self.status >= 400:
            raise Exception("HTTP error")

    def json(self):
        return self._data

def test_client_success(monkeypatch):
    def transport(url, headers, json, timeout):
        return DummyResp()

    client = AIClient(transport=transport, timeout=0.1, max_retries=0)
    # configure minimal settings via env
    import os
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://example"
    os.environ["AZURE_OPENAI_DEPLOYMENT"] = "test"
    res = client.rewrite("hello")
    assert "revised text" in res
    assert len(client.log.entries) >= 1

def test_client_retries(monkeypatch):
    calls = {"n": 0}

    def transport(url, headers, json, timeout):
        calls["n"] += 1
        if calls["n"] < 2:
            raise Exception("transient")
        return DummyResp()

    import os
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://example"
    os.environ["AZURE_OPENAI_DEPLOYMENT"] = "test"

    client = AIClient(transport=transport, timeout=0.1, max_retries=2)
    res = client.rewrite("hello")
    assert "revised text" in res
    assert any(not e.get("success", True) for e in client.log.entries) is True
