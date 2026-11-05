"""公告法规：/terminal/zxt-web/pubnote/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_laws_detail_success,
    assert_laws_query_success,
    assert_laws_type_query_success,
    parse_json_response,
)
from api_tests.schemas.pubnote import (
    LAWS_DETAIL_SCHEMA,
    LAWS_QUERY_ITEM_SCHEMA,
    LAWS_TYPE_QUERY_SCHEMA,
)
from api_tests.services.zxt_web_api import ZxtWebApi


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_laws_type_query(zxt_web_api: ZxtWebApi) -> None:
    resp = zxt_web_api.laws_type_query()
    body = assert_laws_type_query_success(parse_json_response(resp))
    assert_json_schema(body["data"], LAWS_TYPE_QUERY_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_laws_query(zxt_web_api: ZxtWebApi) -> None:
    resp = zxt_web_api.laws_query(page_no=1, page_size=20, query_type=1)
    body = assert_laws_query_success(parse_json_response(resp), page_size=20)
    assert_json_schema(body["data"][0], LAWS_QUERY_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_laws_detail(zxt_web_api: ZxtWebApi) -> None:
    list_resp = zxt_web_api.laws_query(page_no=1, page_size=20, query_type=1)
    list_body = assert_laws_query_success(parse_json_response(list_resp), page_size=20)
    seq = int(list_body["data"][0]["seq"])

    resp = zxt_web_api.laws_detail(seq)
    body = assert_laws_detail_success(parse_json_response(resp), seq=seq)
    assert_json_schema(body["data"], LAWS_DETAIL_SCHEMA)
