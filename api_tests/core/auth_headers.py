from __future__ import annotations

from api_tests.config.settings import settings


def auth_headers_for_token(token: str) -> dict[str, str]:
    value = f"{settings.token_prefix}{token}"
    headers: dict[str, str] = {}
    for name in settings.auth_header_names:
        headers[name] = value
    return headers
