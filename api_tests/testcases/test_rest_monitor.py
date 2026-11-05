"""监控 REST：/terminal/rest/monitor/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_monitor_group_search_success,
    assert_monitor_scheme_view_detail_success,
    assert_monitor_scheme_view_list_success,
    parse_json_response,
)
from api_tests.schemas.monitor import (
    MONITOR_GROUP_SEARCH_ITEM_SCHEMA,
    MONITOR_SCHEME_VIEW_DETAIL_SCHEMA,
    MONITOR_SCHEME_VIEW_ITEM_SCHEMA,
)
from api_tests.services.rest_api import RestApi

MONITOR_SCHEME_ID = 1018653
MONITOR_GROUP_PAGE_SIZE = 10
MONITOR_GROUP_FILTER = '["0","1","2"]'


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_monitor_scheme_view_list(rest_api: RestApi) -> None:
    resp = rest_api.monitor_scheme_view_list()
    body = assert_monitor_scheme_view_list_success(parse_json_response(resp))
    assert_json_schema(body["data"][0], MONITOR_SCHEME_VIEW_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_monitor_scheme_view_detail(rest_api: RestApi) -> None:
    resp = rest_api.monitor_scheme_view_detail(MONITOR_SCHEME_ID)
    body = assert_monitor_scheme_view_detail_success(
        parse_json_response(resp),
        scheme_id=MONITOR_SCHEME_ID,
    )
    assert_json_schema(body["data"], MONITOR_SCHEME_VIEW_DETAIL_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_monitor_group_search(rest_api: RestApi) -> None:
    resp = rest_api.monitor_group_search(
        scheme_id=MONITOR_SCHEME_ID,
        relevance=MONITOR_GROUP_FILTER,
        emotion=MONITOR_GROUP_FILTER,
        page_size=MONITOR_GROUP_PAGE_SIZE,
    )
    body = assert_monitor_group_search_success(
        parse_json_response(resp),
        page_size=MONITOR_GROUP_PAGE_SIZE,
    )
    assert_json_schema(body["data"][0], MONITOR_GROUP_SEARCH_ITEM_SCHEMA)
