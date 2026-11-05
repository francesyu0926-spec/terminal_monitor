"""机构 REST：/terminal/rest/organization/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_organization_content_types_success,
    assert_organization_report_detail_success,
    parse_json_response,
)
from api_tests.schemas.organization import CONTENT_TYPE_ITEM_SCHEMA, ORGANIZATION_REPORT_DETAIL_SCHEMA
from api_tests.services.rest_api import RestApi

# 稳定存在的研报 pid（用于详情接口巡检）
ORGANIZATION_REPORT_PID = 9229039


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_organization_get_content_type(rest_api: RestApi) -> None:
    resp = rest_api.organization_get_content_type()
    body = assert_organization_content_types_success(parse_json_response(resp))
    assert_json_schema(body["data"][0], CONTENT_TYPE_ITEM_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.rest
def test_organization_report_detail(rest_api: RestApi) -> None:
    resp = rest_api.organization_report_detail(ORGANIZATION_REPORT_PID)
    body = assert_organization_report_detail_success(
        parse_json_response(resp),
        pid=ORGANIZATION_REPORT_PID,
    )
    assert_json_schema(body["data"], ORGANIZATION_REPORT_DETAIL_SCHEMA)
