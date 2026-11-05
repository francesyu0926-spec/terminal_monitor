import httpx
import pytest

from api_tests.config.settings import settings


@pytest.mark.health
def test_health_returns_ok() -> None:
    if not settings.health_path:
        pytest.skip("未配置 HEALTH_PATH，已跳过健康检查用例")

    url = f"{settings.base_url.rstrip('/')}{settings.health_path}"
    resp = httpx.get(url, timeout=settings.timeout)
    assert resp.status_code == 200, resp.text
    if resp.headers.get("content-type", "").startswith("application/json"):
        body = resp.json()
        assert body.get("status") in ("ok", "UP", "healthy", True, None) or "status" in body
