"""参数 REST：/terminal/rest/param/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import assert_param_addr_success, parse_json_response
from api_tests.schemas.param import PARAM_ADDR_NODE_SCHEMA
from api_tests.services.rest_api import RestApi


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_param_addr(rest_api: RestApi) -> None:
    resp = rest_api.param_addr()
    body = assert_param_addr_success(parse_json_response(resp))
    assert_json_schema(body["data"][0], PARAM_ADDR_NODE_SCHEMA)
