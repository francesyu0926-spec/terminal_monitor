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
