"""资讯 REST：/terminal/rest/article/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    article_flash_items,
    assert_article_detail_success,
    assert_article_flash_success,
    assert_article_recent_success,
    assert_article_share_system_list_success,
    parse_json_response,
)
from api_tests.schemas.article_detail import ARTICLE_DETAIL_SCHEMA
from api_tests.schemas.article_share import ARTICLE_SHARE_SYSTEM_ITEM_SCHEMA
from api_tests.schemas.article_flash import ARTICLE_FLASH_ITEM_SCHEMA
from api_tests.schemas.article_recent import ARTICLE_RECENT_ITEM_SCHEMA
from api_tests.services.rest_api import RestApi

FLASH_PAGE_SIZE = 8
RECENT_PAGE_SIZE = 30
ARTICLE_DETAIL_CATALOG_ID = 5
ARTICLE_DETAIL_ID = 6493133
ARTICLE_SHARE_SYSTEM_PAGE_SIZE = 10


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_article_flash_list(rest_api: RestApi) -> None:
    resp = rest_api.article_flash(page_size=FLASH_PAGE_SIZE)
    body = assert_article_flash_success(parse_json_response(resp), page_size=FLASH_PAGE_SIZE)

    items = article_flash_items(body)

    assert_json_schema(items[0], ARTICLE_FLASH_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_article_recent_list(rest_api: RestApi) -> None:
    resp = rest_api.article_recent(forward=False, page_size=RECENT_PAGE_SIZE)
    body = assert_article_recent_success(parse_json_response(resp), page_size=RECENT_PAGE_SIZE)

    items = article_flash_items(body)
    assert_json_schema(items[0], ARTICLE_RECENT_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_article_detail(rest_api: RestApi) -> None:
    resp = rest_api.article_detail(ARTICLE_DETAIL_CATALOG_ID, ARTICLE_DETAIL_ID)
    body = assert_article_detail_success(
        parse_json_response(resp),
        article_id=ARTICLE_DETAIL_ID,
    )
    assert_json_schema(body["data"], ARTICLE_DETAIL_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_article_share_system_list(rest_api: RestApi) -> None:
    resp = rest_api.article_share_system_list(page_size=ARTICLE_SHARE_SYSTEM_PAGE_SIZE)
    body = assert_article_share_system_list_success(
        parse_json_response(resp),
        page_size=ARTICLE_SHARE_SYSTEM_PAGE_SIZE,
    )
    assert_json_schema(body["data"][0], ARTICLE_SHARE_SYSTEM_ITEM_SCHEMA)
