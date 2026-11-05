from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Generator

import httpx
import pytest

from api_tests.auth.login import LoginError
from api_tests.auth.token_provider import TokenProvider
from api_tests.config.settings import settings
from api_tests.core.http_client import ApiClient
from api_tests.services.quotes_api import QuotesApi
from api_tests.services.rest_api import RestApi
from api_tests.services.terminal_api import TerminalApi
from api_tests.services.user_stock_api import UserStockApi
from api_tests.services.zxt_web_api import ZxtWebApi

_DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def token_provider() -> TokenProvider:
    return TokenProvider()


@pytest.fixture(scope="session")
def api_client(token_provider: TokenProvider) -> Generator[ApiClient, None, None]:
    client = ApiClient(token_provider=token_provider)
    yield client
    client.close()


@pytest.fixture(scope="session")
def terminal_api(api_client: ApiClient) -> TerminalApi:
    return TerminalApi(api_client)


@pytest.fixture(scope="session")
def zxt_web_api(api_client: ApiClient) -> ZxtWebApi:
    return ZxtWebApi(api_client)


@pytest.fixture(scope="session")
def user_stock_client(token_provider: TokenProvider) -> Generator[ApiClient, None, None]:
    client = ApiClient(base_url=settings.quotes_user_stock_base, token_provider=token_provider)
    yield client
    client.close()


@pytest.fixture(scope="session")
def user_stock_api(user_stock_client: ApiClient) -> UserStockApi:
    return UserStockApi(user_stock_client)


@pytest.fixture(scope="session")
def quotes_client(token_provider: TokenProvider) -> Generator[ApiClient, None, None]:
    client = ApiClient(base_url=settings.quotes_api_base, token_provider=token_provider)
    yield client
    client.close()


@pytest.fixture(scope="session")
def quotes_api(quotes_client: ApiClient) -> QuotesApi:
    return QuotesApi(quotes_client)


@pytest.fixture(scope="session")
def rest_client(token_provider: TokenProvider) -> Generator[ApiClient, None, None]:
    client = ApiClient(
        base_url=settings.rest_api_base,
        token_provider=token_provider,
        headers={"Accept": "*/*"},
    )
    if "Content-Type" in client._client.headers:
        del client._client.headers["Content-Type"]
    yield client
    client.close()


@pytest.fixture(scope="session")
def rest_api(rest_client: ApiClient) -> RestApi:
    return RestApi(rest_client)


@pytest.fixture
def quote_request_payload() -> dict[str, Any]:
    return load_json("quote_request.json")


@pytest.fixture
def catesorting_request_payload() -> dict[str, Any]:
    return load_json("catesorting_request.json")


@pytest.fixture
def dayk_request_payload() -> dict[str, Any]:
    return load_json("dayk_request.json")


@pytest.fixture
def line5d_request_payload() -> dict[str, Any]:
    return load_json("line5d_request.json")


@pytest.fixture
def weekk_request_payload() -> dict[str, Any]:
    return load_json("weekk_request.json")


@pytest.fixture
def monthk_request_payload() -> dict[str, Any]:
    return load_json("monthk_request.json")


@pytest.fixture
def yeark_request_payload() -> dict[str, Any]:
    return load_json("yeark_request.json")


@pytest.fixture
def desk_intraday_request_payload() -> dict[str, Any]:
    return load_json("desk_intraday_request.json")


@pytest.fixture
def astocksquote_request_payload() -> dict[str, Any]:
    return load_json("astocksquote_request.json")


@pytest.fixture
def search_v2_request_payload() -> dict[str, Any]:
    return load_json("search_v2_request.json")


@pytest.fixture
def sector_multiple_sort_request_payload() -> dict[str, Any]:
    return load_json("sector_multiple_sort_request.json")


@pytest.fixture
def importantindex_request_payload() -> dict[str, Any]:
    return load_json("importantindex_request.json")


@pytest.fixture
def profinmainindex_request_payload() -> dict[str, Any]:
    return load_json("profinmainindex_request.json")


@pytest.fixture
def proincstatementnew_request_payload() -> dict[str, Any]:
    return load_json("proincstatementnew_request.json")


@pytest.fixture
def probalsheetnew_request_payload() -> dict[str, Any]:
    return load_json("probalsheetnew_request.json")


@pytest.fixture
def procfstatementnew_request_payload() -> dict[str, Any]:
    return load_json("procfstatementnew_request.json")


@pytest.fixture
def subnewstockranking_request_payload() -> dict[str, Any]:
    return load_json("subnewstockranking_request.json")


@pytest.fixture
def newsharescal_request_payload() -> dict[str, Any]:
    return load_json("newsharescal_request.json")


@pytest.fixture(scope="session")
def auth_token(token_provider: TokenProvider) -> str:
    try:
        return token_provider.get_token()
    except LoginError as exc:
        pytest.skip(str(exc))


@pytest.fixture(scope="session", autouse=True)
def _ensure_login_or_skip(token_provider: TokenProvider) -> None:
    if settings.api_token:
        return
    if not settings.login_code or not settings.login_password:
        pytest.skip("未配置 LOGIN_CODE / LOGIN_PASSWORD，且未设置静态 API_TOKEN")
    try:
        token_provider.get_token()
    except LoginError as exc:
        pytest.skip(str(exc))
    except httpx.HTTPError as exc:
        pytest.skip(f"登录请求失败: {exc}")


def load_json(name: str) -> dict[str, Any]:
    path = _DATA_DIR / name
    with path.open(encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def terminal_create_payload() -> dict[str, Any]:
    data = load_json("terminal_create.json")
    data["name"] = f"{data['name']}-{uuid.uuid4().hex[:8]}"
    return data


@pytest.fixture
def created_terminal(terminal_api: TerminalApi, terminal_create_payload: dict[str, Any]) -> Generator[str, None, None]:
    """创建终端并在用例结束后尝试删除。"""
    resp = terminal_api.create(terminal_create_payload)
    if resp.status_code not in (200, 201):
        pytest.skip(f"无法创建测试终端，HTTP {resp.status_code}: {resp.text[:200]}")

    body = resp.json()
    terminal_id = body.get("id") or body.get("data", {}).get("id")
    if terminal_id is None:
        pytest.skip("创建响应中未找到 id 字段，请核对接口契约")

    yield str(terminal_id)

    terminal_api.delete(terminal_id)
