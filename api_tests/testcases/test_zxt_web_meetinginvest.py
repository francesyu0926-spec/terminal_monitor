"""会议调研：/terminal/zxt-web/meetinginvest/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_meetinginvest_industries_success,
    assert_meetinginvest_page_success,
    parse_json_response,
)
from api_tests.schemas.meetinginvest import MEETING_INVEST_INDUSTRY_SCHEMA
from api_tests.services.zxt_web_api import ZxtWebApi


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_meetinginvest_industries(zxt_web_api: ZxtWebApi) -> None:
    resp = zxt_web_api.meetinginvest_industries()
    body = parse_json_response(resp)
    try:
        body = assert_meetinginvest_industries_success(body)
    except PermissionError as exc:
        pytest.skip(f"跳过：{exc}")

    assert_json_schema(body["data"][0], MEETING_INVEST_INDUSTRY_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_meetinginvest_page(zxt_web_api: ZxtWebApi) -> None:
    resp = zxt_web_api.meetinginvest_page(page_no=1, page_size=10)
    body = parse_json_response(resp)
    try:
        body = assert_meetinginvest_page_success(body, page_size=10)
    except PermissionError as exc:
        pytest.skip(f"跳过：{exc}")

    first = body["data"][0]
    assert isinstance(first, dict) and first
