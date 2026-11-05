"""Mongo 视图：/terminal/zxt-web/mongo/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import (
    assert_mongo_query_success,
    assert_mongo_view_details_success,
    assert_mongo_view_themes_success,
    parse_json_response,
)
from api_tests.schemas.mongo import (
    MONGO_OBJECT_VIEW_CONFIG_SCHEMA,
    MONGO_QUERY_ROW_SCHEMA,
    MONGO_VIEW_THEME_NODE_SCHEMA,
)
from api_tests.services.zxt_web_api import ZxtWebApi

MONGO_QUERY_PAGE_SIZE = 10


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_mongo_view_themes(zxt_web_api: ZxtWebApi) -> None:
    resp = zxt_web_api.mongo_view_themes()
    body = assert_mongo_view_themes_success(parse_json_response(resp))
    assert_json_schema(body["data"][0], MONGO_VIEW_THEME_NODE_SCHEMA)


def _first_obj_view_id(themes: list) -> int:
    for node in themes:
        if not isinstance(node, dict):
            continue
        obj_vw_id = node.get("obj_vw_id")
        if obj_vw_id is not None:
            return int(obj_vw_id)
    raise AssertionError("viewThemes 中未找到 obj_vw_id")


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_mongo_view_details(zxt_web_api: ZxtWebApi) -> None:
    themes_resp = zxt_web_api.mongo_view_themes()
    themes_body = assert_mongo_view_themes_success(parse_json_response(themes_resp))
    view_id = _first_obj_view_id(themes_body["data"])

    resp = zxt_web_api.mongo_view_details(view_id)
    body = assert_mongo_view_details_success(parse_json_response(resp), view_id=view_id)
    assert_json_schema(body["data"]["objectViewConfig"][0], MONGO_OBJECT_VIEW_CONFIG_SCHEMA)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.zxt_web
def test_mongo_query(zxt_web_api: ZxtWebApi) -> None:
    resp = zxt_web_api.mongo_query()
    body = assert_mongo_query_success(parse_json_response(resp), page_size=MONGO_QUERY_PAGE_SIZE)
    assert_json_schema(body["data"][0], MONGO_QUERY_ROW_SCHEMA)
