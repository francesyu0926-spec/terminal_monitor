"""资讯栏目 REST：/terminal/rest/info/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_info_column_success,
    assert_info_detail_success,
    assert_info_page_success,
    parse_json_response,
)
from api_tests.schemas.info_column import INFO_COLUMN_ITEM_SCHEMA
from api_tests.schemas.info_detail import INFO_DETAIL_SCHEMA
from api_tests.schemas.info_page import INFO_PAGE_ITEM_SCHEMA
from api_tests.services.rest_api import RestApi

INFO_PAGE_SIZE = 20
INFO_SUBCAT = 20


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_info_column(rest_api: RestApi) -> None:
    resp = rest_api.info_column()
    body = assert_info_column_success(parse_json_response(resp))
    assert_json_schema(body["data"][0], INFO_COLUMN_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_info_page(rest_api: RestApi) -> None:
    resp = rest_api.info_page(forward=False, page_size=INFO_PAGE_SIZE, subcat=INFO_SUBCAT)
    body = assert_info_page_success(parse_json_response(resp), page_size=INFO_PAGE_SIZE)
    assert_json_schema(body["data"][0], INFO_PAGE_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_info_detail(rest_api: RestApi) -> None:
    list_resp = rest_api.info_page(forward=False, page_size=INFO_PAGE_SIZE, subcat=INFO_SUBCAT)
    list_body = assert_info_page_success(parse_json_response(list_resp), page_size=INFO_PAGE_SIZE)
    article_id = int(list_body["data"][0]["id"])

    resp = rest_api.info_detail(article_id)
    body = assert_info_detail_success(parse_json_response(resp), article_id=article_id)
    assert_json_schema(body["data"], INFO_DETAIL_SCHEMA)
