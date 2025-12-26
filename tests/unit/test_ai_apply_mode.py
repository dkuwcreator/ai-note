from ai.client import AIClient
from storage.db import RewriteMode


def test_apply_rewrite_mode_uses_mode_template(monkeypatch):
    # emulate a transport that returns a successful chat response
    class Resp:
        def __init__(self):
            self.status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "REWRITTEN"}}]}

    def transport(url, headers, json, timeout):
        # ensure prompt contains the input text substituted
        assert "Hello world" in json["messages"][0]["content"]
        return Resp()

    client = AIClient(transport=transport, timeout=1.0, max_retries=0)
    mode = RewriteMode(id=1, name="Test Mode", instruction_template="Rewrite THIS: {text}", enabled=True, order=1, applies_to='selection-only', builtin=False, advanced_settings=None)
    out = client.apply_rewrite_mode(mode, "Hello world")
    assert out == "REWRITTEN"
