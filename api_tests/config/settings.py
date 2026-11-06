from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from api_tests.config.monitor_policy import load_monitor_policy

_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_ROOT / ".env")
_MONITOR_POLICY = load_monitor_policy()


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
    auth_header_names: tuple[str, ...]
    quotes_api_base: str
    quotes_health_api_base: str
    quotes_user_stock_base: str
    rest_api_base: str
    desk_quotes_page_url: str
    zxt_desktop_news_detail_url: str
    zxt_desktop_theme_index_url: str
    quotes_api_call_window_enabled: bool
    quotes_api_call_timezone: str
    quotes_api_call_start: str
    quotes_api_call_end: str
    wework_notify_failure_only_after: str
    verify_ssl: bool

    @property
    def quotes_health_url(self) -> str:
        base = self.quotes_health_api_base.rstrip("/")
        return f"{base}/health"

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


def _parse_auth_header_names() -> tuple[str, ...]:
    combined = _env("AUTH_HEADERS", "Secret,Token")
    if combined:
        return tuple(part.strip() for part in combined.split(",") if part.strip())
    single = _env("TOKEN_HEADER", "")
    return (single,) if single else ()


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
    token_header=_env("TOKEN_HEADER", ""),
    token_prefix=_env("TOKEN_PREFIX", ""),
    auth_header_names=_parse_auth_header_names(),
    quotes_api_base=_env(
        "QUOTES_API_BASE",
        "https://terminal.sfccn.com/terminal/desk/quotes/api",
    ),
    quotes_health_api_base=_env(
        "QUOTES_HEALTH_API_BASE",
        "https://terminal.sfccn.com/terminal/quotes/api",
    ),
    quotes_user_stock_base=_env(
        "QUOTES_USER_STOCK_BASE",
        "https://terminal.sfccn.com/terminal/quotes",
    ),
    rest_api_base=_env(
        "REST_API_BASE",
        "https://terminal.sfccn.com/terminal/rest",
    ),
    desk_quotes_page_url=_env(
        "DESK_QUOTES_PAGE_URL",
        "https://terminal.sfccn.com/terminal/desk/quotes/",
    ),
    zxt_desktop_news_detail_url=_env(
        "ZXT_DESKTOP_NEWS_DETAIL_URL",
        "https://zxt.sfccn.com/desktop/news/details/1021804",
    ),
    zxt_desktop_theme_index_url=_env(
        "ZXT_DESKTOP_THEME_INDEX_URL",
        "https://zxt.sfccn.com/desktop/theme/index",
    ),
    quotes_api_call_window_enabled=_env_bool("QUOTES_API_CALL_WINDOW_ENABLED", True),
    quotes_api_call_timezone=_env("QUOTES_API_CALL_TIMEZONE", "Asia/Shanghai"),
    quotes_api_call_start=_env("QUOTES_API_CALL_START", "09:30"),
    quotes_api_call_end=_env("QUOTES_API_CALL_END", "23:39"),
    wework_notify_failure_only_after=_MONITOR_POLICY.wework_notify_failure_only_after,
    verify_ssl=_env_bool("VERIFY_SSL", True),
)
