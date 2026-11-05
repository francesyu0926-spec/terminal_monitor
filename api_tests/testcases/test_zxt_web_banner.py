"""终端 Web：/terminal/zxt-web/banner/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import assert_banner_list_success, parse_json_response
from api_tests.schemas.banner import BANNER_ITEM_SCHEMA
from api_tests.services.zxt_web_api import ZxtWebApi

BANNER_POSITION = 4


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_banner_list(zxt_web_api: ZxtWebApi) -> None:
    resp = zxt_web_api.banner_list(position=BANNER_POSITION)
    body = assert_banner_list_success(parse_json_response(resp))
    assert_json_schema(body["data"][0], BANNER_ITEM_SCHEMA)
