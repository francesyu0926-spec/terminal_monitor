"""舆情 REST：/terminal/rest/emotion/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_emotion_solution_q_success,
    assert_emotion_solution_view_list_success,
    parse_json_response,
)
from api_tests.schemas.emotion import EMOTION_SOLUTION_VIEW_ITEM_SCHEMA
from api_tests.schemas.monitor import MONITOR_GROUP_SEARCH_ITEM_SCHEMA
from api_tests.services.rest_api import RestApi

EMOTION_SOLUTION_PAGE_SIZE = 10


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_emotion_solution_view_list(rest_api: RestApi) -> None:
    resp = rest_api.emotion_solution_view_list()
    body = assert_emotion_solution_view_list_success(parse_json_response(resp))
    if body["data"]:
        assert_json_schema(body["data"][0], EMOTION_SOLUTION_VIEW_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_emotion_solution_q(rest_api: RestApi) -> None:
    resp = rest_api.emotion_solution_q(page_size=EMOTION_SOLUTION_PAGE_SIZE)
    body = assert_emotion_solution_q_success(
        parse_json_response(resp),
        page_size=EMOTION_SOLUTION_PAGE_SIZE,
    )
    assert_json_schema(body["data"][0], MONITOR_GROUP_SEARCH_ITEM_SCHEMA)
