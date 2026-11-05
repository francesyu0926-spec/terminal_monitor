from __future__ import annotations

from api_tests.config.settings import settings


def httpx_verify() -> bool | str:
    return settings.verify_ssl
