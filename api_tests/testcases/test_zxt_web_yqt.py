"""舆情通 SSO：/terminal/zxt-web/yqt/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import assert_yqt_sso_token_success, parse_json_response
from api_tests.schemas.yqt import YQT_SSO_TOKEN_SCHEMA
from api_tests.services.zxt_web_api import ZxtWebApi


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_yqt_sso_token(zxt_web_api: ZxtWebApi) -> None:
    resp = zxt_web_api.yqt_sso_token()
    body = assert_yqt_sso_token_success(parse_json_response(resp))
    assert_json_schema(body["data"], YQT_SSO_TOKEN_SCHEMA)
