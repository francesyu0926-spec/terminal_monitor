"""terminal/quotes/api 相关接口：登录鉴权 + quote / catesorting / dayk / weekk。"""

import pytest

from api_tests.auth.login import login_with_password
from api_tests.auth.token_provider import TokenProvider
from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_dayk_success,
    assert_ohlc_success,
    assert_quote_success,
    parse_json_response,
)
from api_tests.schemas.dayk import DAYK_RESPONSE_SCHEMA
from api_tests.schemas.quote import QUOTE_ITEMS_LIST_SCHEMA, QUOTE_RESPONSE_SCHEMA
from api_tests.services.quotes_api import QuotesApi


# --- 登录 / Token ---


@pytest.mark.smoke
@pytest.mark.auth
@pytest.mark.quote
def test_login_returns_jwt_token() -> None:
    token = login_with_password()
    assert isinstance(token, str)
    assert token.count(".") >= 2


@pytest.mark.smoke
@pytest.mark.auth
@pytest.mark.quote
def test_token_provider_reuses_cached_token(token_provider: TokenProvider) -> None:
    first = token_provider.get_token()
    second = token_provider.get_token()
    assert first == second


# --- POST /quote ---


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.quote
def test_quote_single_symbol(quotes_api: QuotesApi, quote_request_payload: dict) -> None:
    resp = quotes_api.quote_payload(quote_request_payload)
    body = assert_quote_success(parse_json_response(resp))
    assert_json_schema(body, QUOTE_RESPONSE_SCHEMA)

    item = body["quoteItems"][0]
    assert item.get("code") == quote_request_payload["code"]
    for field in quote_request_payload["fields"]:
        assert field in item, f"quoteItems[0] 缺少字段 {field}"


# --- POST /catesorting ---


@pytest.mark.regression
@pytest.mark.quote
def test_catesorting_paged_list(quotes_api: QuotesApi, catesorting_request_payload: dict) -> None:
    resp = quotes_api.catesorting(catesorting_request_payload)
    body = assert_quote_success(parse_json_response(resp))
    assert_json_schema(body, QUOTE_ITEMS_LIST_SCHEMA)

    items = body["quoteItems"]
    page_size = catesorting_request_payload["pageSize"]
    assert len(items) <= page_size
    assert len(items) > 0

    for field in ("code", "name", "spe"):
        assert field in items[0], f"quoteItems[0] 缺少字段 {field}"


# --- POST /dayk ---


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.quote
def test_dayk_ohlc_series(quotes_api: QuotesApi, dayk_request_payload: dict) -> None:
    resp = quotes_api.dayk(dayk_request_payload)
    body = assert_dayk_success(parse_json_response(resp))
    assert_json_schema(body, DAYK_RESPONSE_SCHEMA)

    items = body["OHLCItems"]
    start = dayk_request_payload["datetime"]
    for bar in items:
        assert bar["date"] >= start, f"K线日期 {bar['date']} 早于请求起点 {start}"
        assert bar["highPrice"] >= bar["lowPrice"]
    assert items[0]["date"] >= start
    assert items[-1]["date"] >= items[0]["date"]


# --- POST /weekk ---


@pytest.mark.regression
@pytest.mark.quote
def test_weekk_ohlc_series(quotes_api: QuotesApi, weekk_request_payload: dict) -> None:
    resp = quotes_api.weekk(weekk_request_payload)
    body = assert_ohlc_success(parse_json_response(resp))
    assert_json_schema(body, DAYK_RESPONSE_SCHEMA)

    items = body["OHLCItems"]
    start = weekk_request_payload["datetime"]
    for bar in items:
        assert bar["date"] >= start, f"周K日期 {bar['date']} 早于请求起点 {start}"
        assert bar["highPrice"] >= bar["lowPrice"]
    assert items[0]["date"] >= start
    assert items[-1]["date"] >= items[0]["date"]


# --- POST /monthk ---


@pytest.mark.regression
@pytest.mark.quote
def test_monthk_ohlc_series(quotes_api: QuotesApi, monthk_request_payload: dict) -> None:
    resp = quotes_api.monthk(monthk_request_payload)
    body = assert_ohlc_success(parse_json_response(resp))
    assert_json_schema(body, DAYK_RESPONSE_SCHEMA)

    items = body["OHLCItems"]
    start = monthk_request_payload["datetime"]
    for bar in items:
        assert bar["date"] >= start, f"月K日期 {bar['date']} 早于请求起点 {start}"
        assert bar["highPrice"] >= bar["lowPrice"]
    assert items[0]["date"] >= start
    assert items[-1]["date"] >= items[0]["date"]


# --- POST /yeark ---


@pytest.mark.regression
@pytest.mark.quote
def test_yeark_ohlc_series(quotes_api: QuotesApi, yeark_request_payload: dict) -> None:
    resp = quotes_api.yeark(yeark_request_payload)
    body = assert_ohlc_success(parse_json_response(resp))
    assert_json_schema(body, DAYK_RESPONSE_SCHEMA)

    items = body["OHLCItems"]
    start = yeark_request_payload["datetime"]
    for bar in items:
        assert bar["date"] >= start, f"年K日期 {bar['date']} 早于请求起点 {start}"
        assert bar["highPrice"] >= bar["lowPrice"]
    assert items[0]["date"] >= start
    assert items[-1]["date"] >= items[0]["date"]
