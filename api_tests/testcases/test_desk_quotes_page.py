"""桌面行情页：GET /terminal/desk/quotes/（HTML，需登录）。"""

import httpx
import pytest

from api_tests.auth.token_provider import TokenProvider
from api_tests.config.settings import settings
from api_tests.core.auth_headers import auth_headers_for_token
from api_tests.core.response import is_unauthorized_body
from api_tests.core.transport import httpx_verify


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.desk
def test_desk_quotes_page_loads(token_provider: TokenProvider) -> None:
    def fetch() -> httpx.Response:
        token = token_provider.get_token()
        return httpx.get(
            settings.desk_quotes_page_url,
            headers=auth_headers_for_token(token),
            timeout=settings.timeout,
            verify=httpx_verify(),
            follow_redirects=True,
        )

    resp = fetch()
    if "application/json" in resp.headers.get("content-type", "").lower():
        try:
            if is_unauthorized_body(resp.json()):
                token_provider.invalidate()
                resp = fetch()
        except ValueError:
            pass
    assert resp.status_code == 200, resp.text[:300]
    content_type = resp.headers.get("content-type", "").lower()
    assert "text/html" in content_type, f"期望 HTML，实际 Content-Type: {content_type}"

    snippet = resp.text[:800].lower()
    assert "<html" in snippet or "<!doctype html" in snippet, "响应应为 HTML 页面"
