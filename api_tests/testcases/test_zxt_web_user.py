"""用户：/terminal/zxt-web/user/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_user_check_matketing_auth_success,
    assert_user_market_guide_success,
    assert_user_view_detail_success,
    parse_json_response,
)
from api_tests.schemas.zxt_user import USER_MARKET_GUIDE_SCHEMA, USER_VIEW_DETAIL_SCHEMA
from api_tests.services.zxt_web_api import ZxtWebApi


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_user_view_detail(zxt_web_api: ZxtWebApi) -> None:
    resp = zxt_web_api.user_view_detail()
    body = assert_user_view_detail_success(parse_json_response(resp))
    assert_json_schema(body["data"], USER_VIEW_DETAIL_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_user_market_guide(zxt_web_api: ZxtWebApi) -> None:
    resp = zxt_web_api.user_market_guide()
    body = assert_user_market_guide_success(parse_json_response(resp))
    assert_json_schema(body["data"], USER_MARKET_GUIDE_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_user_check_matketing_auth(zxt_web_api: ZxtWebApi) -> None:
    resp = zxt_web_api.user_check_matketing_auth()
    assert_user_check_matketing_auth_success(parse_json_response(resp))
