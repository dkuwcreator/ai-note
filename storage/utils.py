from __future__ import annotations

import os
import json
import base64
import re
from pathlib import Path
from typing import Optional, List

try:
    import keyring
except Exception:  # pragma: no cover - keyring may be absent in some environments
    keyring = None  # type: ignore

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


_whitespace_re = re.compile(r"\s+")


def normalize_tag(name: str) -> str:
    s = name.strip()
    s = _whitespace_re.sub(" ", s)
    return s.lower()


def normalize_tags(names: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for n in names:
        nn = normalize_tag(n)
        if nn and nn not in seen:
            seen.add(nn)
            out.append(nn)
    return out


def keyring_available() -> bool:
    return keyring is not None and hasattr(keyring, "get_password")


def _derive_key(passphrase: str, salt: bytes, iterations: int = 390000) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations, backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))
    return key


def store_api_key(
    service: str,
    username: str,
    api_key: str,
    fallback_path: Optional[Path] = None,
    passphrase: Optional[str] = None,
) -> str:
    """Store API key using keyring if available, else use encrypted local fallback.

    Returns the storage method used: 'keyring' or 'file'.
    """
    if keyring_available():
        keyring.set_password(service, username, api_key)
        return "keyring"

    if fallback_path is None or passphrase is None:
        raise RuntimeError("Keyring unavailable and no fallback path/passphrase provided")
    _store_encrypted_file(fallback_path, api_key, passphrase)
    return "file"


def get_api_key(service: str, username: str, fallback_path: Optional[Path] = None, passphrase: Optional[str] = None) -> Optional[str]:
    if keyring_available():
        return keyring.get_password(service, username)
    if fallback_path is None or passphrase is None:
        return None
    return _load_encrypted_file(fallback_path, passphrase)


def delete_api_key(service: str, username: str, fallback_path: Optional[Path] = None) -> bool:
    if keyring_available():
        try:
            keyring.delete_password(service, username)
            return True
        except Exception:
            return False
    if fallback_path and Path(fallback_path).exists():
        try:
            Path(fallback_path).unlink()
            return True
        except Exception:
            return False
    return False


def _store_encrypted_file(path: Path, secret: str, passphrase: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    salt = os.urandom(16)
    key = _derive_key(passphrase, salt)
    f = Fernet(key)
    token = f.encrypt(secret.encode("utf-8"))
    payload = {"salt": base64.b64encode(salt).decode("ascii"), "token": base64.b64encode(token).decode("ascii")}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh)


def _load_encrypted_file(path: Path, passphrase: str) -> Optional[str]:
    path = Path(path)
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    salt = base64.b64decode(payload["salt"])
    token = base64.b64decode(payload["token"])
    key = _derive_key(passphrase, salt)
    f = Fernet(key)
    try:
        secret = f.decrypt(token)
        return secret.decode("utf-8")
    except Exception:
        return None
