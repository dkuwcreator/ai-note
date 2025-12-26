import tempfile
from pathlib import Path
import importlib

from storage import utils


def test_encrypted_fallback_roundtrip(tmp_path):
    secret = "supersecret"
    path = tmp_path / "secret.json"
    method = utils.store_api_key("ai_notepad", "default", secret, fallback_path=path, passphrase="pw123")
    assert method in ("file", "keyring")
    if method == "file":
        loaded = utils.get_api_key("ai_notepad", "default", fallback_path=path, passphrase="pw123")
        assert loaded == secret
        assert utils.delete_api_key("ai_notepad", "default", fallback_path=path)
        assert not path.exists()
    else:
        # keyring path: ensure retrieval and deletion succeed via keyring APIs
        loaded = utils.get_api_key("ai_notepad", "default")
        assert loaded == secret
        assert utils.delete_api_key("ai_notepad", "default")


def test_keyring_mocked(monkeypatch):
    class DummyKR:
        storage = {}

        @staticmethod
        def set_password(s, u, p):
            DummyKR.storage[(s, u)] = p

        @staticmethod
        def get_password(s, u):
            return DummyKR.storage.get((s, u))

        @staticmethod
        def delete_password(s, u):
            DummyKR.storage.pop((s, u), None)

    monkeypatch.setattr(utils, "keyring", DummyKR)
    # reload keyring availability function if necessary
    importlib.reload(utils)
    secret = "kr-secret"
    method = utils.store_api_key("svc", "u", secret)
    assert method == "keyring"
    assert utils.get_api_key("svc", "u") == secret
    assert utils.delete_api_key("svc", "u")
