"""公司 REST：/terminal/rest/company/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_company_notice_detail_success,
    assert_company_notice_success,
    parse_json_response,
)
from api_tests.schemas.company_notice import COMPANY_NOTICE_ITEM_SCHEMA
from api_tests.schemas.company_notice_detail import COMPANY_NOTICE_DETAIL_SCHEMA
from api_tests.services.rest_api import RestApi

NOTICE_PAGE_SIZE = 20


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_company_notice(rest_api: RestApi) -> None:
    resp = rest_api.company_notice(page_no=1, page_size=NOTICE_PAGE_SIZE)
    body = assert_company_notice_success(parse_json_response(resp), page_size=NOTICE_PAGE_SIZE)
    assert_json_schema(body["data"][0], COMPANY_NOTICE_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_company_notice_detail(rest_api: RestApi) -> None:
    list_resp = rest_api.company_notice(page_no=1, page_size=NOTICE_PAGE_SIZE)
    list_body = assert_company_notice_success(parse_json_response(list_resp), page_size=NOTICE_PAGE_SIZE)
    notice_id = int(list_body["data"][0]["id"])

    resp = rest_api.company_notice_detail(notice_id)
    body = assert_company_notice_detail_success(parse_json_response(resp), notice_id=notice_id)
    assert_json_schema(body["data"], COMPANY_NOTICE_DETAIL_SCHEMA)
