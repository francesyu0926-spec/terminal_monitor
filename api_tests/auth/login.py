from __future__ import annotations

import httpx

from api_tests.config.settings import settings
from api_tests.core.transport import httpx_verify


class LoginError(RuntimeError):
    pass


def login_with_password() -> str:
    """密码登录，返回 JWT token。"""
    if not settings.login_code or not settings.login_password:
        raise LoginError("请在 .env 中配置 LOGIN_CODE 与 LOGIN_PASSWORD")

    url = settings.login_url
    resp = httpx.post(
        url,
        data={
            "loginCode": settings.login_code,
            "password": settings.login_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=settings.timeout,
        verify=httpx_verify(),
    )
    if resp.status_code != 200:
        raise LoginError(f"登录 HTTP 失败: {resp.status_code} {resp.text[:300]}")

    body = resp.json()
    if body.get("code") != 200:
        raise LoginError(f"登录业务失败: code={body.get('code')} msg={body.get('msg')}")

    data = body.get("data") or {}
    token = data.get("token")
    if not token:
        raise LoginError("登录响应中缺少 data.token")

    return str(token)
