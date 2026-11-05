"""海外研报：/terminal/zxt-web/overseasReport/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_overseas_report_realtime_read_success,
    assert_overseas_report_realtime_search_success,
    parse_json_response,
)
from api_tests.schemas.overseas_report import OVERSEAS_REPORT_RECORD_SCHEMA
from api_tests.services.zxt_web_api import ZxtWebApi

OVERSEAS_REPORT_PAGE_SIZE = 20
OVERSEAS_REPORT_READ_PAGE_SIZE = 2


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_overseas_report_realtime_search(zxt_web_api: ZxtWebApi) -> None:
    resp = zxt_web_api.overseas_report_realtime_search()
    body = assert_overseas_report_realtime_search_success(
        parse_json_response(resp),
        page_size=OVERSEAS_REPORT_PAGE_SIZE,
    )
    assert_json_schema(body["data"]["records"][0], OVERSEAS_REPORT_RECORD_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_overseas_report_realtime_read(zxt_web_api: ZxtWebApi) -> None:
    list_resp = zxt_web_api.overseas_report_realtime_search()
    list_body = assert_overseas_report_realtime_search_success(
        parse_json_response(list_resp),
        page_size=OVERSEAS_REPORT_PAGE_SIZE,
    )
    report_id = int(list_body["data"]["records"][0]["id"])

    resp = zxt_web_api.overseas_report_realtime_read(
        report_id,
        page_size=OVERSEAS_REPORT_READ_PAGE_SIZE,
    )
    body = parse_json_response(resp)
    try:
        assert_overseas_report_realtime_read_success(
            body,
            report_id=report_id,
            page_size=OVERSEAS_REPORT_READ_PAGE_SIZE,
        )
    except PermissionError as exc:
        pytest.skip(f"跳过：{exc}")
