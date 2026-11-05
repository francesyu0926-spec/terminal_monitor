"""搜索 REST：/terminal/rest/esSearch/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import assert_es_search_page_success, parse_json_response
from api_tests.schemas.es_search import ES_SEARCH_ITEM_SCHEMA
from api_tests.services.rest_api import RestApi

ES_SEARCH_CATEGORY = 14
ES_SEARCH_PAGE_SIZE = 20


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_es_search_searchkey_page(rest_api: RestApi) -> None:
    resp = rest_api.es_search_searchkey_page(
        category=ES_SEARCH_CATEGORY,
        keyword="",
        page_size=ES_SEARCH_PAGE_SIZE,
    )
    body = assert_es_search_page_success(parse_json_response(resp), page_size=ES_SEARCH_PAGE_SIZE)
    assert_json_schema(body["data"][0], ES_SEARCH_ITEM_SCHEMA)
