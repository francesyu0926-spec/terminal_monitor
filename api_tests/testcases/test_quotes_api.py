"""行情相关接口：/terminal/desk/quotes/api（health 仍走 /terminal/quotes/api/health）。"""

import httpx
import pytest

from api_tests.config.settings import settings
from api_tests.core.transport import httpx_verify

from api_tests.auth.login import login_with_password
from api_tests.auth.token_provider import TokenProvider
from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_dayk_success,
    assert_desk_status_success,
    assert_line_chart_success,
    assert_sector_multiple_sort_success,
    assert_ohlc_success,
    assert_quote_success,
    assert_newsharescal_success,
    assert_subnew_quote_success,
    parse_json_response,
)
from api_tests.schemas.astocksquote import ASTOCKSQUOTE_RESPONSE_SCHEMA
from api_tests.schemas.importantindex import (
    IMPORTANTINDEX_RESPONSE_SCHEMA,
    PROBALSHEETNEW_RESPONSE_SCHEMA,
    PROCSTATEMENTNEW_RESPONSE_SCHEMA,
    PROINCSTATEMENTNEW_RESPONSE_SCHEMA,
    PROFINMAININDEX_RESPONSE_SCHEMA,
)
from api_tests.schemas.sector_multiple_sort import SECTOR_MULTIPLE_SORT_RESPONSE_SCHEMA
from api_tests.schemas.newsharescal import NEWSHARESCAL_RESPONSE_SCHEMA
from api_tests.schemas.subnewstockranking import SUBNEWSTOCKRANKING_RESPONSE_SCHEMA
from api_tests.schemas.dayk import DAYK_RESPONSE_SCHEMA, OHLC_ITEM_SCHEMA
from api_tests.schemas.line5d import LINE5D_RESPONSE_SCHEMA
from api_tests.schemas.quote import QUOTE_ITEMS_LIST_SCHEMA, QUOTE_RESPONSE_SCHEMA
from api_tests.services.quotes_api import BAR_INTERVALS, BarInterval, QuotesApi


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


# --- GET /terminal/quotes/api/health（未迁移至 desk） ---


@pytest.mark.health
@pytest.mark.quote
def test_quotes_api_health() -> None:
    resp = httpx.get(settings.quotes_health_url, timeout=settings.timeout, verify=httpx_verify())
    assert resp.status_code == 200, resp.text


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


# --- POST /line、/line5d ---


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.quote
def test_line_chart(quotes_api: QuotesApi, line5d_request_payload: dict) -> None:
    resp = quotes_api.line(line5d_request_payload)
    body = assert_line_chart_success(parse_json_response(resp))
    assert_json_schema(body, LINE5D_RESPONSE_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.quote
def test_line5d_chart(quotes_api: QuotesApi, line5d_request_payload: dict) -> None:
    resp = quotes_api.line5d(line5d_request_payload)
    body = assert_line_chart_success(parse_json_response(resp))
    assert_json_schema(body, LINE5D_RESPONSE_SCHEMA)


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


# --- POST /m1|m5|m15|m30|m60|m120 ---


@pytest.mark.regression
@pytest.mark.quote
@pytest.mark.parametrize("interval", BAR_INTERVALS)
def test_desk_intraday_ohlc_series(
    quotes_api: QuotesApi,
    desk_intraday_request_payload: dict,
    interval: BarInterval,
) -> None:
    resp = quotes_api.bars(interval, desk_intraday_request_payload)
    body = assert_ohlc_success(parse_json_response(resp))
    items = body["OHLCItems"]
    assert_json_schema(items[0], OHLC_ITEM_SCHEMA)
    start_date = desk_intraday_request_payload["datetime"][:8]
    for bar in (items[0], items[-1]):
        assert bar["date"] >= start_date
        assert bar.get("time"), f"{interval} K线缺少 time"
        assert bar["highPrice"] >= bar["lowPrice"]

    assert (items[-1]["date"], items[-1]["time"]) >= (items[0]["date"], items[0]["time"])


# --- POST /astocksquote ---


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.quote
def test_desk_astocksquote(
    quotes_api: QuotesApi,
    astocksquote_request_payload: dict,
) -> None:
    resp = quotes_api.astocksquote(astocksquote_request_payload)
    body = assert_desk_status_success(parse_json_response(resp))
    assert_json_schema(body, ASTOCKSQUOTE_RESPONSE_SCHEMA)

    assert body.get("message") == "ok"
    assert isinstance(body.get("list"), list) and body["list"]
    for key in ("tTime", "tUp", "tDown", "tEqual", "tLimitUp", "tLimitDown"):
        assert key in body, f"缺少字段 {key}"


# --- POST /sectorMultipleSort ---


@pytest.mark.regression
@pytest.mark.quote
def test_desk_sector_multiple_sort(
    quotes_api: QuotesApi,
    sector_multiple_sort_request_payload: dict,
) -> None:
    resp = quotes_api.sector_multiple_sort(sector_multiple_sort_request_payload)
    body = assert_sector_multiple_sort_success(
        parse_json_response(resp),
        sector_multiple_sort_request_payload,
    )
    assert_json_schema(body, SECTOR_MULTIPLE_SORT_RESPONSE_SCHEMA)


# --- POST /importantindex ---


@pytest.mark.regression
@pytest.mark.quote
def test_desk_importantindex(
    quotes_api: QuotesApi,
    importantindex_request_payload: dict,
) -> None:
    resp = quotes_api.importantindex(importantindex_request_payload)
    body = assert_desk_status_success(parse_json_response(resp))
    assert_json_schema(body, IMPORTANTINDEX_RESPONSE_SCHEMA)

    data = body["data"]
    assert isinstance(data, dict) and data
    for value in data.values():
        assert isinstance(value, str) and value


# --- POST /profinmainindex ---


@pytest.mark.regression
@pytest.mark.quote
def test_desk_profinmainindex(
    quotes_api: QuotesApi,
    profinmainindex_request_payload: dict,
) -> None:
    resp = quotes_api.profinmainindex(profinmainindex_request_payload)
    body = assert_desk_status_success(parse_json_response(resp))
    assert_json_schema(body, PROFINMAININDEX_RESPONSE_SCHEMA)

    data = body["data"]
    assert isinstance(data, dict) and data
    assert "REPORTTITLE" in data


# --- POST /proincstatementnew ---


@pytest.mark.regression
@pytest.mark.quote
def test_desk_proincstatementnew(
    quotes_api: QuotesApi,
    proincstatementnew_request_payload: dict,
) -> None:
    resp = quotes_api.proincstatementnew(proincstatementnew_request_payload)
    body = assert_desk_status_success(parse_json_response(resp))
    assert_json_schema(body, PROINCSTATEMENTNEW_RESPONSE_SCHEMA)

    data = body["data"]
    assert isinstance(data, dict) and data
    for value in data.values():
        assert isinstance(value, str) and value


# --- POST /probalsheetnew ---


@pytest.mark.regression
@pytest.mark.quote
def test_desk_probalsheetnew(
    quotes_api: QuotesApi,
    probalsheetnew_request_payload: dict,
) -> None:
    resp = quotes_api.probalsheetnew(probalsheetnew_request_payload)
    body = assert_desk_status_success(parse_json_response(resp))
    assert_json_schema(body, PROBALSHEETNEW_RESPONSE_SCHEMA)

    data = body["data"]
    assert isinstance(data, dict) and data
    assert "TOTLIAB" in data or "PARESHARRIGH" in data


# --- POST /procfstatementnew ---


@pytest.mark.regression
@pytest.mark.quote
def test_desk_procfstatementnew(
    quotes_api: QuotesApi,
    procfstatementnew_request_payload: dict,
) -> None:
    resp = quotes_api.procfstatementnew(procfstatementnew_request_payload)
    body = assert_desk_status_success(parse_json_response(resp))
    assert_json_schema(body, PROCSTATEMENTNEW_RESPONSE_SCHEMA)

    data = body["data"]
    assert isinstance(data, dict) and data
    assert "MANANETR" in data or "INVNETCASHFLOW" in data


# --- POST /subnewstockranking ---


@pytest.mark.regression
@pytest.mark.quote
def test_desk_subnewstockranking(
    quotes_api: QuotesApi,
    subnewstockranking_request_payload: dict,
) -> None:
    resp = quotes_api.subnewstockranking(subnewstockranking_request_payload)
    body = assert_subnew_quote_success(
        parse_json_response(resp),
        page_size=subnewstockranking_request_payload["pageSize"],
    )
    assert_json_schema(body, SUBNEWSTOCKRANKING_RESPONSE_SCHEMA)

    item = body["subnewQuoteItems"][0]
    assert item.get("code") and item.get("name")
    assert "IPODate" in item


# --- POST /newsharescal ---


@pytest.mark.regression
@pytest.mark.quote
def test_desk_newsharescal(
    quotes_api: QuotesApi,
    newsharescal_request_payload: dict,
) -> None:
    resp = quotes_api.newsharescal(newsharescal_request_payload)
    body = assert_newsharescal_success(
        parse_json_response(resp),
        page_size=newsharescal_request_payload["pageSize"],
    )
    assert_json_schema(body, NEWSHARESCAL_RESPONSE_SCHEMA)

    wsslist = body["data"]["wsslist"]
    if wsslist:
        assert wsslist[0].get("TRADINGCODE")
