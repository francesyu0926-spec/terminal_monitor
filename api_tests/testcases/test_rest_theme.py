"""主题 REST：/terminal/rest/theme/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_theme_fund_list_success,
    assert_theme_recomend_success,
    assert_theme_stock_articles_success,
    parse_json_response,
)
from api_tests.schemas.theme_fund import THEME_FUND_ITEM_SCHEMA
from api_tests.schemas.theme_recomend import THEME_RECOMEND_ITEM_SCHEMA
from api_tests.schemas.theme_stock_articles import THEME_STOCK_ARTICLE_ITEM_SCHEMA
from api_tests.services.rest_api import RestApi

THEME_PAGE_SIZE = 10
# 主题推荐接口返回的 theme_id（如黄金主题），用于 fund/list 联调
THEME_FUND_THEME_ID = 13311271
THEME_STOCK_CODE = "000609.SZ"
THEME_STOCK_ARTICLE_PAGE_SIZE = 50


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_theme_recomend_type2(rest_api: RestApi) -> None:
    resp = rest_api.theme_recomend(theme_type=2, page_size=THEME_PAGE_SIZE)
    body = assert_theme_recomend_success(parse_json_response(resp), page_size=THEME_PAGE_SIZE)
    assert_json_schema(body["data"][0], THEME_RECOMEND_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_theme_recomend_type3(rest_api: RestApi) -> None:
    resp = rest_api.theme_recomend(theme_type=3, page_size=THEME_PAGE_SIZE)
    body = assert_theme_recomend_success(parse_json_response(resp), page_size=THEME_PAGE_SIZE)
    assert_json_schema(body["data"][0], THEME_RECOMEND_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_theme_fund_list(rest_api: RestApi) -> None:
    resp = rest_api.theme_fund_list(page_size=THEME_PAGE_SIZE)
    body = assert_theme_fund_list_success(parse_json_response(resp), page_size=THEME_PAGE_SIZE)
    items = body["data"]
    if items:
        first = items[0]
        assert isinstance(first, dict), "基金主题条目应为对象"
        assert_json_schema(first, THEME_FUND_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_theme_fund_list_by_theme_id(rest_api: RestApi) -> None:
    resp = rest_api.theme_fund_list(theme_id=THEME_FUND_THEME_ID, page_size=THEME_PAGE_SIZE)
    body = assert_theme_fund_list_success(
        parse_json_response(resp),
        page_size=THEME_PAGE_SIZE,
        require_items=True,
    )
    assert_json_schema(body["data"][0], THEME_FUND_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_theme_stock_articles(rest_api: RestApi) -> None:
    resp = rest_api.theme_stock_articles(
        stock_code=THEME_STOCK_CODE,
        page_no=1,
        article_type=1,
        page_size=THEME_STOCK_ARTICLE_PAGE_SIZE,
    )
    body = assert_theme_stock_articles_success(
        parse_json_response(resp),
        page_size=THEME_STOCK_ARTICLE_PAGE_SIZE,
    )
    assert_json_schema(body["data"][0], THEME_STOCK_ARTICLE_ITEM_SCHEMA)
