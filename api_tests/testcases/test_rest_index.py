"""指数 REST：/terminal/rest/index/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_index_emotion_success,
    assert_index_trend_success,
    parse_json_response,
)
from api_tests.schemas.index_emotion import INDEX_EMOTION_DATA_SCHEMA
from api_tests.schemas.index_trend import INDEX_TREND_DATA_SCHEMA
from api_tests.services.rest_api import RestApi


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_index_emotion(rest_api: RestApi) -> None:
    resp = rest_api.index_emotion()
    body = assert_index_emotion_success(parse_json_response(resp))
    assert_json_schema(body["data"], INDEX_EMOTION_DATA_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_index_trend_1(rest_api: RestApi) -> None:
    resp = rest_api.index_trend(1)
    body = assert_index_trend_success(parse_json_response(resp))
    assert_json_schema(body["data"], INDEX_TREND_DATA_SCHEMA)
