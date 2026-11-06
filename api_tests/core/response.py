from __future__ import annotations

from typing import Any

import httpx


def parse_json_response(resp: httpx.Response) -> dict[str, Any]:
    assert resp.status_code == 200, f"HTTP {resp.status_code}: {resp.text[:300]}"
    body = resp.json()
    assert isinstance(body, dict), "响应体应为 JSON 对象"
    return body


def is_unauthorized_body(body: dict[str, Any]) -> bool:
    code = body.get("code")
    msg = str(body.get("msg", ""))
    return code == 401 or msg in ("未登录", "未登錄")


def response_indicates_unauthorized(resp: httpx.Response) -> bool:
    if resp.status_code == 401:
        return True
    try:
        body = resp.json()
    except ValueError:
        return False
    return isinstance(body, dict) and is_unauthorized_body(body)


def assert_business_success(body: dict[str, Any]) -> dict[str, Any]:
    if is_unauthorized_body(body):
        raise AssertionError(f"未登录 code={body.get('code')} msg={body.get('msg')}")
    code = body.get("code")
    assert code == 200, f"业务失败 code={code} msg={body.get('msg')}"
    return body


def assert_subnew_quote_success(body: dict[str, Any], *, page_size: int | None = None) -> dict[str, Any]:
    if is_unauthorized_body(body):
        raise AssertionError(f"未登录 code={body.get('code')} msg={body.get('msg')}")
    assert "subnewQuoteItems" in body, f"响应缺少 subnewQuoteItems: {list(body.keys())}"
    items = body["subnewQuoteItems"]
    assert isinstance(items, list) and items, "subnewQuoteItems 应为非空数组"
    if page_size is not None:
        assert len(items) <= page_size
    return body


def assert_line_chart_success(body: dict[str, Any]) -> dict[str, Any]:
    if is_unauthorized_body(body):
        raise AssertionError(f"未登录 code={body.get('code')} msg={body.get('msg')}")
    assert "chartItems" in body, f"响应缺少 chartItems: {list(body.keys())}"
    items = body["chartItems"]
    assert isinstance(items, list) and items, "chartItems 应为非空数组"
    assert "tradeDates" in body, "响应缺少 tradeDates"
    first = items[0]
    assert first.get("datetime") is not None, "chartItems[0] 应包含 datetime"
    assert first.get("price") not in (None, ""), "chartItems[0] 应包含 price"
    return body


assert_line5d_success = assert_line_chart_success


def assert_quote_success(body: dict[str, Any]) -> dict[str, Any]:
    if is_unauthorized_body(body):
        raise AssertionError(f"未登录 code={body.get('code')} msg={body.get('msg')}")
    assert "quoteItems" in body, f"行情响应缺少 quoteItems: {list(body.keys())}"
    items = body["quoteItems"]
    assert isinstance(items, list) and items, "quoteItems 应为非空数组"
    return body


def assert_ohlc_success(body: dict[str, Any]) -> dict[str, Any]:
    if is_unauthorized_body(body):
        raise AssertionError(f"未登录 code={body.get('code')} msg={body.get('msg')}")
    assert "OHLCItems" in body, f"K线响应缺少 OHLCItems: {list(body.keys())}"
    items = body["OHLCItems"]
    assert isinstance(items, list) and items, "OHLCItems 应为非空数组"
    return body


def assert_dayk_success(body: dict[str, Any]) -> dict[str, Any]:
    return assert_ohlc_success(body)


def assert_sector_multiple_sort_success(
    body: dict[str, Any],
    request: dict[str, Any],
) -> dict[str, Any]:
    if is_unauthorized_body(body):
        raise AssertionError(f"未登录 code={body.get('code')} msg={body.get('msg')}")
    page_size = int(request.get("pageSize", 10))
    sectors = request.get("sectors") or []
    assert sectors, "请求 sectors 不能为空"
    for sector in sectors:
        identifier = sector["identifier"]
        assert identifier in body, f"响应缺少榜单 {identifier}"
        items = body[identifier]
        assert isinstance(items, list) and items, f"{identifier} 应为非空数组"
        assert len(items) <= page_size, f"{identifier} 条数超过 pageSize"
        for field in sector.get("fields") or []:
            assert field in items[0], f"{identifier}[0] 缺少字段 {field}"
    return body


def assert_newsharescal_success(body: dict[str, Any], *, page_size: int | None = None) -> dict[str, Any]:
    body = assert_desk_status_success(body)
    data = body.get("data") or {}
    wsslist = data.get("wsslist")
    assert isinstance(wsslist, list), "data.wsslist 应为数组"
    if page_size is not None:
        assert len(wsslist) <= page_size
    return body


def article_flash_items(body: dict[str, Any]) -> list[Any]:
    data = body.get("data")
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("list", "records", "rows", "articles", "items"):
            value = data.get(key)
            if isinstance(value, list):
                return value
    for key in ("list", "records", "rows", "articles", "items"):
        value = body.get(key)
        if isinstance(value, list):
            return value
    raise AssertionError(f"无法解析快讯列表，响应键: {list(body.keys())}")


def assert_group_with_stocks_tree_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    tree = data.get("tree")
    assert isinstance(tree, list) and tree, "data.tree 应为非空数组"
    root = tree[0]
    assert isinstance(root, dict), "tree[0] 应为对象"
    assert root.get("gid") is not None, "分组应包含 gid"
    assert str(root.get("gnm") or "").strip(), "分组应包含非空 gnm"
    assert isinstance(root.get("stks"), list), "stks 应为数组"
    return body


def assert_laws_detail_success(body: dict[str, Any], *, seq: int | None = None) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    assert data.get("seq") is not None, "应包含 seq"
    if seq is not None:
        assert data.get("seq") == seq, f"seq 不一致: {data.get('seq')} != {seq}"
    assert str(data.get("lawsTitle") or "").strip(), "应包含非空 lawsTitle"
    assert str(data.get("lawsContent") or "").strip(), "应包含非空 lawsContent"
    return body


def assert_laws_query_success(body: dict[str, Any], *, page_size: int | None = None) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    if page_size is not None:
        assert len(data) <= page_size, f"条数 {len(data)} 超过 pageSize {page_size}"
    first = data[0]
    assert isinstance(first, dict), "法规条目应为对象"
    assert first.get("seq") is not None, "应包含 seq"
    assert str(first.get("lawsTitle") or "").strip(), "应包含非空 lawsTitle"
    assert str(first.get("lawsType") or "").strip(), "应包含 lawsType"
    return body


def _assert_meetinginvest_business(body: dict[str, Any]) -> dict[str, Any]:
    if is_unauthorized_body(body):
        raise AssertionError(f"未登录 code={body.get('code')} msg={body.get('msg')}")
    code = body.get("code")
    if code == 5002:
        raise PermissionError(str(body.get("msg") or "meetinginvest 权限未开通"))
    return assert_business_success(body)


def assert_meetinginvest_industries_success(body: dict[str, Any]) -> dict[str, Any]:
    body = _assert_meetinginvest_business(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    first = data[0]
    assert isinstance(first, dict), "行业条目应为对象"
    name = first.get("name") or first.get("industryName") or first.get("code")
    assert str(name or "").strip(), "行业条目应包含 name/industryName/code"
    return body


def assert_meetinginvest_page_success(body: dict[str, Any], *, page_size: int | None = None) -> dict[str, Any]:
    body = _assert_meetinginvest_business(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    if page_size is not None:
        assert len(data) <= page_size, f"条数 {len(data)} 超过 pageSize {page_size}"
    first = data[0]
    assert isinstance(first, dict), "会议条目应为对象"
    title = first.get("title") or first.get("meetingTitle") or first.get("name")
    assert str(title or "").strip() or first.get("id") is not None, "会议条目应含 title 或 id"
    return body


def assert_laws_type_query_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空字符串数组"
    assert all(isinstance(item, str) and item.strip() for item in data), "data 元素应为非空字符串"
    return body


def _overseas_report_read_permission_denied(body: dict[str, Any]) -> bool:
    if is_unauthorized_body(body):
        return False
    code = body.get("code")
    msg = str(body.get("msg") or "")
    return code in (500, 5002) and "开通权限" in msg


def _assert_overseas_report_read_business(body: dict[str, Any]) -> dict[str, Any]:
    if is_unauthorized_body(body):
        raise AssertionError(f"未登录 code={body.get('code')} msg={body.get('msg')}")
    if _overseas_report_read_permission_denied(body):
        raise PermissionError(str(body.get("msg") or "overseasReport read 权限未开通"))
    return assert_business_success(body)


def assert_overseas_report_realtime_read_success(
    body: dict[str, Any],
    *,
    report_id: int | None = None,
    page_size: int | None = None,
) -> dict[str, Any]:
    body = _assert_overseas_report_read_business(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    if report_id is not None and data.get("id") is not None:
        assert data.get("id") == report_id, f"id 不一致: {data.get('id')} != {report_id}"
    title = str(data.get("title") or "").strip()
    content = str(data.get("content") or data.get("html") or data.get("text") or "").strip()
    pages = data.get("pages") or data.get("pageList") or data.get("records")
    has_pages = isinstance(pages, list) and bool(pages)
    if page_size is not None and has_pages:
        assert len(pages) <= page_size, f"页数 {len(pages)} 超过 pageSize {page_size}"
    assert title or content or has_pages, "详情应包含 title、正文或分页内容"
    return body


def assert_overseas_report_realtime_search_success(
    body: dict[str, Any],
    *,
    page_size: int | None = None,
) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    records = data.get("records")
    assert isinstance(records, list) and records, "data.records 应为非空数组"
    if page_size is not None:
        assert len(records) <= page_size, f"条数 {len(records)} 超过 pageSize {page_size}"
    total = data.get("total")
    if not isinstance(total, int) or total <= 0:
        top_total = body.get("total")
        assert isinstance(top_total, int) and top_total > 0, "total 应为正整数"
    first = records[0]
    assert isinstance(first, dict), "研报条目应为对象"
    assert first.get("id") is not None, "应包含 id"
    assert str(first.get("title") or "").strip(), "应包含非空 title"
    return body


def assert_mongo_query_success(
    body: dict[str, Any],
    *,
    page_size: int | None = None,
) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    if page_size is not None:
        assert len(data) <= page_size, f"条数 {len(data)} 超过 pagination.size {page_size}"
    first = data[0]
    assert isinstance(first, dict), "查询结果行应为对象"
    assert str(first.get("SYMBOL") or "").strip(), "应包含非空 SYMBOL"
    assert str(first.get("SESNAME") or "").strip(), "应包含非空 SESNAME"
    return body


def assert_mongo_view_details_success(
    body: dict[str, Any],
    *,
    view_id: int | None = None,
) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    assert data.get("objVwId") is not None, "应包含 objVwId"
    if view_id is not None:
        assert data.get("objVwId") == view_id, f"objVwId 不一致: {data.get('objVwId')} != {view_id}"
    configs = data.get("objectViewConfig")
    assert isinstance(configs, list) and configs, "objectViewConfig 应为非空数组"
    first = configs[0]
    assert isinstance(first, dict), "列配置应为对象"
    assert str(first.get("obj_prop_cap") or "").strip(), "应包含非空 obj_prop_cap"
    assert str(first.get("obj_prop_name") or "").strip(), "应包含非空 obj_prop_name"
    view_config = data.get("viewConfig")
    assert isinstance(view_config, list), "viewConfig 应为数组"
    return body


def assert_mongo_view_themes_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    first = data[0]
    assert isinstance(first, dict), "主题节点应为对象"
    assert first.get("id") is not None, "应包含 id"
    assert str(first.get("node_cap") or "").strip(), "应包含非空 node_cap"
    assert first.get("node_code") is not None, "应包含 node_code"
    return body


def assert_yqt_sso_token_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    for key in (
        "timeStamp",
        "systemId",
        "clientUserName",
        "channel",
        "directUrl",
        "encryptCode",
        "accessToken",
    ):
        value = data.get(key)
        if key == "timeStamp":
            assert isinstance(value, int) and value > 0, f"{key} 应为正整数"
        else:
            assert str(value or "").strip(), f"应包含非空 {key}"
    return body


def assert_user_check_matketing_auth_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_business_success(body)
    assert isinstance(body.get("data"), bool), "data 应为布尔值"
    return body


def assert_user_market_guide_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    is_guide = data.get("is_guide")
    assert is_guide in (0, 1), f"is_guide 应为 0 或 1: {is_guide!r}"
    return body


def assert_user_view_detail_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    assert data.get("userId") is not None, "应包含 userId"
    assert str(data.get("nickName") or "").strip(), "应包含非空 nickName"
    assert str(data.get("loginCode") or "").strip(), "应包含非空 loginCode"
    assert data.get("userStatus") is not None, "应包含 userStatus"
    return body


def assert_banner_list_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    first = data[0]
    assert isinstance(first, dict), "banner 条目应为对象"
    assert first.get("id") is not None, "banner 应包含 id"
    assert str(first.get("title") or "").strip(), "banner 应包含非空 title"
    assert first.get("status") is not None, "banner 应包含 status"
    return body


def assert_theme_stock_articles_success(
    body: dict[str, Any],
    *,
    page_size: int | None = None,
) -> dict[str, Any]:
    body = assert_business_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    if page_size is not None:
        assert len(data) <= page_size, f"条数 {len(data)} 超过 pageSize {page_size}"
    first = data[0]
    assert isinstance(first, dict), "文章条目应为对象"
    assert first.get("articleId") is not None, "应包含 articleId"
    assert str(first.get("title") or "").strip(), "应包含非空 title"
    return body


def assert_theme_fund_list_success(
    body: dict[str, Any],
    *,
    page_size: int | None = None,
    require_items: bool = False,
) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list), f"data 应为数组: {type(data).__name__}"
    if page_size is not None:
        assert len(data) <= page_size, f"条数 {len(data)} 超过 pageSize {page_size}"
    if require_items:
        assert data, "data 不应为空"
        first = data[0]
        assert isinstance(first, dict), "基金条目应为对象"
        assert str(first.get("fundCode") or "").strip(), "应包含 fundCode"
        assert str(first.get("fundName") or "").strip(), "应包含 fundName"
    return body


def assert_theme_recomend_success(body: dict[str, Any], *, page_size: int | None = None) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    if page_size is not None:
        assert len(data) <= page_size, f"条数 {len(data)} 超过 pageSize {page_size}"
    first = data[0]
    assert isinstance(first, dict), "主题条目应为对象"
    assert first.get("theme_id") is not None, "应包含 theme_id"
    assert str(first.get("theme_name") or "").strip(), "应包含非空 theme_name"
    stocks = first.get("themeStocksVOS")
    assert isinstance(stocks, list) and stocks, "themeStocksVOS 应为非空数组"
    return body


def assert_company_notice_detail_success(body: dict[str, Any], *, notice_id: int | None = None) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    assert data.get("id") is not None, "应包含 id"
    if notice_id is not None:
        assert data.get("id") == notice_id, f"id 不一致: {data.get('id')} != {notice_id}"
    assert str(data.get("infoTitle") or "").strip(), "应包含非空 infoTitle"
    assert str(data.get("content") or "").strip(), (
        f"应包含非空 content（接口 code={body.get('code')} msg={body.get('msg')}）"
    )
    return body


def assert_company_notice_success(body: dict[str, Any], *, page_size: int | None = None) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    if page_size is not None:
        assert len(data) <= page_size, f"条数 {len(data)} 超过 pageSize {page_size}"
    first = data[0]
    assert isinstance(first, dict), "公告条目应为对象"
    assert first.get("id") is not None, "应包含 id"
    assert str(first.get("infoTitle") or "").strip(), "应包含非空 infoTitle"
    assert str(first.get("secuCode") or "").strip(), "应包含 secuCode"
    return body


def assert_es_search_page_success(body: dict[str, Any], *, page_size: int | None = None) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    if page_size is not None:
        assert len(data) <= page_size, f"条数 {len(data)} 超过 pageSize {page_size}"
    total = body.get("total")
    assert isinstance(total, int) and total > 0, "total 应为正整数"
    first = data[0]
    assert isinstance(first, dict), "搜索结果应为对象"
    assert first.get("id") is not None, "应包含 id"
    assert str(first.get("report_title") or "").strip(), "应包含非空 report_title"
    return body


def assert_organization_report_detail_success(body: dict[str, Any], *, pid: int | None = None) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    if pid is not None:
        assert data.get("pid") == pid, f"pid 不一致: {data.get('pid')} != {pid}"
    assert str(data.get("title") or "").strip(), "应包含非空 title"
    assert str(data.get("contentType") or "").strip(), "应包含 contentType"
    content = data.get("content")
    assert content is not None and str(content).strip(), "应包含 content"
    return body


def assert_organization_content_types_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    first = data[0]
    assert isinstance(first, dict), "条目应为对象"
    assert str(first.get("contentType") or "").strip(), "应包含非空 contentType"
    return body


def assert_advertise_list_success(
    body: dict[str, Any],
    *,
    page_size: int | None = None,
) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list), f"data 应为数组: {type(data).__name__}"
    total = body.get("total")
    assert isinstance(total, int) and total >= 0, "total 应为非负整数"
    if page_size is not None:
        assert len(data) <= page_size, f"条数 {len(data)} 超过 pageSize {page_size}"
    if data:
        first = data[0]
        assert isinstance(first, dict), "广告条目应为对象"
        assert first.get("id") is not None, "应包含 id"
        label = first.get("title") or first.get("name")
        assert str(label or "").strip(), "应包含非空 title 或 name"
    return body


def assert_advertise_classify_list_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    first = data[0]
    assert isinstance(first, dict), "分类条目应为对象"
    assert first.get("id") is not None, "应包含 id"
    assert str(first.get("name") or "").strip(), "应包含非空 name"
    return body


def assert_param_addr_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    first = data[0]
    assert isinstance(first, dict), "地区节点应为对象"
    assert str(first.get("code") or "").strip(), "应包含非空 code"
    assert str(first.get("zhsname") or "").strip(), "应包含非空 zhsname"
    child = first.get("childAddr")
    assert isinstance(child, list) and child, "childAddr 应为非空数组"
    return body


def assert_monitor_scheme_view_detail_success(
    body: dict[str, Any],
    *,
    scheme_id: int | None = None,
) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    assert data.get("schemeId") is not None, "应包含 schemeId"
    if scheme_id is not None:
        assert data.get("schemeId") == scheme_id, f"schemeId 不一致: {data.get('schemeId')} != {scheme_id}"
    assert str(data.get("schemeName") or "").strip(), "应包含非空 schemeName"
    assert data.get("userId") is not None, "应包含 userId"
    for key in ("bonds", "companies", "funds"):
        value = data.get(key)
        assert isinstance(value, list), f"{key} 应为数组"
    return body


def assert_emotion_solution_view_list_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list), f"data 应为数组: {type(data).__name__}"
    if not data:
        return body
    first = data[0]
    assert isinstance(first, dict), "方案条目应为对象"
    solution_id = first.get("solutionId") or first.get("schemeId") or first.get("id")
    assert solution_id is not None, "应包含 solutionId/schemeId/id"
    name = first.get("solutionName") or first.get("schemeName") or first.get("name")
    assert str(name or "").strip(), "应包含非空方案名称"
    return body


def assert_emotion_solution_q_success(
    body: dict[str, Any],
    *,
    page_size: int | None = None,
) -> dict[str, Any]:
    return assert_monitor_group_search_success(body, page_size=page_size)


def assert_monitor_group_search_success(
    body: dict[str, Any],
    *,
    page_size: int | None = None,
    allow_empty: bool = False,
) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list), "data 应为数组"
    if page_size is not None:
        assert len(data) <= page_size, f"条数 {len(data)} 超过 pageSize {page_size}"
    total = body.get("total")
    assert isinstance(total, int) and total >= 0, "total 应为非负整数"
    if not data:
        assert allow_empty, "data 应为非空数组"
        assert total == 0, "空结果时 total 应为 0"
        return body
    assert total > 0, "有数据时 total 应为正整数"
    first = data[0]
    assert isinstance(first, dict), "舆情条目应为对象"
    assert first.get("id") is not None, "应包含 id"
    assert str(first.get("title") or "").strip(), "应包含非空 title"
    return body


def assert_monitor_scheme_view_list_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    first = data[0]
    assert isinstance(first, dict), "方案视图条目应为对象"
    assert first.get("schemeId") is not None, "应包含 schemeId"
    assert str(first.get("schemeName") or "").strip(), "应包含非空 schemeName"
    assert first.get("userId") is not None, "应包含 userId"
    return body


def assert_hot_info_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    hot_info = data.get("hotInfo")
    assert isinstance(hot_info, list) and hot_info, "data.hotInfo 应为非空数组"
    first = hot_info[0]
    assert isinstance(first, dict), "hotInfo[0] 应为对象"
    assert first.get("id") is not None, "热点应包含 id"
    assert str(first.get("title") or "").strip(), "热点应包含非空 title"
    return body


def assert_info_page_success(body: dict[str, Any], *, page_size: int | None = None) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    if page_size is not None:
        assert len(data) <= page_size, f"条数 {len(data)} 超过 pageSize {page_size}"
    first = data[0]
    assert isinstance(first, dict), "资讯条目应为对象"
    assert first.get("id") is not None, "应包含 id"
    assert str(first.get("title") or "").strip(), "应包含非空 title"
    return body


def assert_info_detail_success(body: dict[str, Any], *, article_id: int | None = None) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    assert data.get("id") is not None, "应包含 id"
    if article_id is not None:
        assert data.get("id") == article_id, f"id 不一致: {data.get('id')} != {article_id}"
    assert str(data.get("title") or "").strip(), "应包含非空 title"
    content = str(data.get("content") or "").strip()
    assert content, "应包含非空 content"
    return body


def assert_info_column_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    names = [str(item.get("positionName") or "") for item in data if isinstance(item, dict)]
    assert "ETF观察" in names, f"栏目列表缺少「ETF观察」，当前: {names}"
    return body


def assert_rest_success(body: dict[str, Any]) -> dict[str, Any]:
    """/terminal/rest 多数接口：code=0 表示成功。"""
    if is_unauthorized_body(body):
        raise AssertionError(f"未登录 code={body.get('code')} msg={body.get('msg')}")
    code = body.get("code")
    assert code == 0, f"业务失败 code={code} msg={body.get('msg')}"
    return body


_EMOTION_KEYS = ("today", "yesterday", "weekAgo", "monthAgo", "yearAgo")


def assert_index_trend_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    assert str(data.get("scope") or "").strip(), "data.scope 不应为空"
    assert str(data.get("updateDate") or "").strip(), "data.updateDate 不应为空"
    trend = data.get("trend")
    assert isinstance(trend, list) and trend, "data.trend 应为非空数组"
    point = trend[0]
    assert isinstance(point, dict), "trend[0] 应为对象"
    assert str(point.get("date") or "").strip(), "trend[0].date 不应为空"
    value = point.get("value")
    assert isinstance(value, (int, float)), "trend[0].value 应为数值"
    assert 0 <= float(value) <= 100, "trend[0].value 应在 0~100 内"
    return body


def assert_index_emotion_success(body: dict[str, Any]) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    assert str(data.get("updateDate") or "").strip(), "data.updateDate 不应为空"
    for key in _EMOTION_KEYS:
        point = data.get(key)
        assert isinstance(point, dict), f"data.{key} 应为对象"
        assert str(point.get("desc") or "").strip(), f"data.{key}.desc 不应为空"
        ranker = point.get("ranker")
        assert isinstance(ranker, int) and ranker > 0, f"data.{key}.ranker 无效"
        value = point.get("value")
        assert isinstance(value, (int, float)), f"data.{key}.value 应为数值"
        assert 0 <= float(value) <= 100, f"data.{key}.value 应在 0~100 内"
    return body


def _assert_article_list(body: dict[str, Any], *, page_size: int | None, label: str) -> list[Any]:
    body = assert_rest_success(body)
    items = article_flash_items(body)
    assert items, f"{label}列表不应为空"
    if page_size is not None:
        assert len(items) <= page_size, f"条数 {len(items)} 超过 pageSize {page_size}"
    first = items[0]
    assert isinstance(first, dict), f"{label}条目应为对象"
    return items


def assert_article_flash_success(body: dict[str, Any], *, page_size: int | None = None) -> dict[str, Any]:
    items = _assert_article_list(body, page_size=page_size, label="快讯")
    first = items[0]
    has_title = bool(str(first.get("title") or "").strip())
    has_content = bool(str(first.get("content") or "").strip())
    assert has_title or has_content, "快讯首条应包含 title 或 content"
    return body


def assert_article_share_system_list_success(
    body: dict[str, Any],
    *,
    page_size: int | None = None,
) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, list) and data, "data 应为非空数组"
    if page_size is not None:
        assert len(data) <= page_size, f"条数 {len(data)} 超过 pageSize {page_size}"
    total = body.get("total")
    assert isinstance(total, int) and total > 0, "total 应为正整数"
    first = data[0]
    assert isinstance(first, dict), "分享条目应为对象"
    assert first.get("id") is not None, "应包含 id"
    assert str(first.get("title") or "").strip(), "应包含非空 title"
    assert first.get("status") is not None, "应包含 status"
    return body


def assert_article_detail_success(
    body: dict[str, Any],
    *,
    article_id: int | None = None,
) -> dict[str, Any]:
    body = assert_rest_success(body)
    data = body.get("data")
    assert isinstance(data, dict), f"data 应为对象: {type(data).__name__}"
    assert data.get("id") is not None, "应包含 id"
    if article_id is not None:
        assert data.get("id") == article_id, f"id 不一致: {data.get('id')} != {article_id}"
    assert str(data.get("title") or "").strip(), "应包含非空 title"
    content = str(data.get("content") or "").strip()
    summary = str(data.get("summary") or "").strip()
    assert content or summary, "应包含 content 或 summary"
    return body


def assert_article_recent_success(body: dict[str, Any], *, page_size: int | None = None) -> dict[str, Any]:
    items = _assert_article_list(body, page_size=page_size, label="资讯")
    first = items[0]
    assert first.get("articleId") is not None, "资讯首条应包含 articleId"
    assert str(first.get("title") or "").strip(), "资讯首条应包含非空 title"
    assert first.get("publishTime") is not None, "资讯首条应包含 publishTime"
    return body


def assert_desk_status_success(body: dict[str, Any]) -> dict[str, Any]:
    """桌面端部分接口使用 status/message 而非 code/msg。"""
    if is_unauthorized_body(body):
        raise AssertionError(f"未登录 code={body.get('code')} msg={body.get('msg')}")
    status = body.get("status")
    assert status == 200, f"业务失败 status={status} message={body.get('message')}"
    return body


def assert_search_v2_success(body: dict[str, Any], *, size: int | None = None) -> dict[str, Any]:
    body = assert_desk_status_success(body)
    results = body.get("searchResults")
    assert isinstance(results, list), "searchResults 应为数组"
    if size is not None:
        assert len(results) <= size, f"结果条数 {len(results)} 超过 size {size}"
    assert results, "searchResults 应为非空数组"
    first = results[0]
    assert isinstance(first, dict), "搜索结果条目应为对象"
    assert str(first.get("code") or "").strip(), "应包含 code"
    assert str(first.get("name") or "").strip(), "应包含 name"
    return body
