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


def assert_desk_status_success(body: dict[str, Any]) -> dict[str, Any]:
    """桌面端部分接口使用 status/message 而非 code/msg。"""
    if is_unauthorized_body(body):
        raise AssertionError(f"未登录 code={body.get('code')} msg={body.get('msg')}")
    status = body.get("status")
    assert status == 200, f"业务失败 status={status} message={body.get('message')}"
    return body
