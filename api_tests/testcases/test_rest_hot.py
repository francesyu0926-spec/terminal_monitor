"""热点 REST：/terminal/rest/hot/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import assert_hot_info_success, parse_json_response
from api_tests.schemas.hot_info import HOT_INFO_DATA_SCHEMA
from api_tests.services.rest_api import RestApi


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_hot_info(rest_api: RestApi) -> None:
    resp = rest_api.hot_info()
    body = assert_hot_info_success(parse_json_response(resp))
    assert_json_schema(body["data"], HOT_INFO_DATA_SCHEMA)
