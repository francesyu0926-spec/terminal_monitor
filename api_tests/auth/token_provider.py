from __future__ import annotations

import json
import threading
import time
from pathlib import Path

from api_tests.auth.login import LoginError, login_with_password
from api_tests.config.settings import settings

_CACHE_DIR = Path(__file__).resolve().parents[2] / ".cache"
_CACHE_FILE = _CACHE_DIR / "api_token.json"


class TokenProvider:
    """登录 token 缓存：默认 12 小时内复用，过期后自动重新登录。"""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._token: str | None = None
        self._expires_at: float = 0.0
        self._load_cache()

    def get_token(self) -> str:
        if settings.api_token:
            return settings.api_token

        with self._lock:
            if self._token and time.time() < self._expires_at:
                return self._token
            token = login_with_password()
            self._set_token(token)
            return token

    def invalidate(self) -> None:
        with self._lock:
            self._token = None
            self._expires_at = 0.0
            if _CACHE_FILE.exists():
                _CACHE_FILE.unlink(missing_ok=True)

    def _set_token(self, token: str) -> None:
        self._token = token
        self._expires_at = time.time() + settings.token_ttl_seconds
        self._save_cache()

    def _load_cache(self) -> None:
        if settings.api_token or not _CACHE_FILE.exists():
            return
        try:
            payload = json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
            token = payload.get("token")
            expires_at = float(payload.get("expires_at", 0))
            if token and time.time() < expires_at:
                self._token = str(token)
                self._expires_at = expires_at
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            return

    def _save_cache(self) -> None:
        if settings.api_token or not self._token:
            return
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _CACHE_FILE.write_text(
            json.dumps({"token": self._token, "expires_at": self._expires_at}, ensure_ascii=False),
            encoding="utf-8",
        )


def ensure_authenticated() -> str:
    try:
        return TokenProvider().get_token()
    except LoginError as exc:
        raise RuntimeError(str(exc)) from exc
