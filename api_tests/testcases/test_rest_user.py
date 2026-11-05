"""用户 REST：/terminal/rest/user/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_advertise_classify_list_success,
    assert_advertise_list_success,
    parse_json_response,
)
from api_tests.schemas.advertise import ADVERTISE_LIST_ITEM_SCHEMA
from api_tests.schemas.advertise_classify import ADVERTISE_CLASSIFY_ITEM_SCHEMA
from api_tests.services.rest_api import RestApi

ADVERTISE_CLASSIFY_ID = 1
ADVERTISE_LIST_PAGE_SIZE = 10


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_advertise_classify_list(rest_api: RestApi) -> None:
    resp = rest_api.advertise_classify_list()
    body = assert_advertise_classify_list_success(parse_json_response(resp))
    assert_json_schema(body["data"][0], ADVERTISE_CLASSIFY_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_advertise_list(rest_api: RestApi) -> None:
    resp = rest_api.advertise_list(
        classify_id=ADVERTISE_CLASSIFY_ID,
        page_size=ADVERTISE_LIST_PAGE_SIZE,
    )
    body = assert_advertise_list_success(
        parse_json_response(resp),
        page_size=ADVERTISE_LIST_PAGE_SIZE,
    )
    if body["data"]:
        assert_json_schema(body["data"][0], ADVERTISE_LIST_ITEM_SCHEMA)
