from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_ROOT / ".env")


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


@dataclass(frozen=True)
class Settings:
    base_url: str
    api_prefix: str
    timeout: float
    api_token: str
    health_path: str
    login_code: str
    login_password: str
    login_path: str
    token_ttl_seconds: int
    token_header: str
    token_prefix: str
    verify_ssl: bool

    @property
    def api_root(self) -> str:
        base = self.base_url.rstrip("/")
        prefix = self.api_prefix if self.api_prefix.startswith("/") else f"/{self.api_prefix}"
        prefix = prefix.rstrip("/")
        return f"{base}{prefix}"

    @property
    def login_url(self) -> str:
        path = self.login_path if self.login_path.startswith("/") else f"/{self.login_path}"
        return f"{self.api_root}{path}"


def _env_bool(name: str, default: bool = True) -> bool:
    raw = _env(name, "true" if default else "false").lower()
    return raw in ("1", "true", "yes", "on")


settings = Settings(
    base_url=_env("API_BASE_URL", "https://terminal.sfccn.com"),
    api_prefix=_env("API_PREFIX", "/terminal/zxt-web"),
    timeout=float(_env("API_TIMEOUT", "30")),
    api_token=_env("API_TOKEN", ""),
    health_path=_env("HEALTH_PATH", ""),
    login_code=_env("LOGIN_CODE", ""),
    login_password=_env("LOGIN_PASSWORD", ""),
    login_path=_env("LOGIN_PATH", "/login/pwd"),
    token_ttl_seconds=int(_env("TOKEN_TTL_SECONDS", str(12 * 3600))),
    token_header=_env("TOKEN_HEADER", "token"),
    token_prefix=_env("TOKEN_PREFIX", ""),
    verify_ssl=_env_bool("VERIFY_SSL", True),
)
