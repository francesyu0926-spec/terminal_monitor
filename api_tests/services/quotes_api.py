from __future__ import annotations

from typing import Any, Literal, Sequence

import httpx

from api_tests.core.http_client import ApiClient

BarInterval = Literal["m1", "m5", "m15", "m30", "m60", "m120"]

BAR_INTERVALS: tuple[BarInterval, ...] = ("m1", "m5", "m15", "m30", "m60", "m120")

# 兼容旧名称
DeskBarInterval = BarInterval
DESK_BAR_INTERVALS = BAR_INTERVALS


class QuotesApi:
    """行情接口：POST /terminal/desk/quotes/api/*（health 除外，见 settings.quotes_health_url）"""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def quote(self, code: str, fields: Sequence[str]) -> httpx.Response:
        return self._client.post("/quote", json={"code": code, "fields": list(fields)})

    def quote_payload(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/quote", json=payload)

    def catesorting(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/catesorting", json=payload)

    def dayk(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/dayk", json=payload)

    def weekk(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/weekk", json=payload)

    def monthk(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/monthk", json=payload)

    def yeark(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/yeark", json=payload)

    def bars(self, interval: BarInterval, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post(f"/{interval}", json=payload)

    def astocksquote(self, payload: dict[str, Any] | None = None) -> httpx.Response:
        return self._client.post("/astocksquote", json=payload or {})

    def sector_multiple_sort(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/sectorMultipleSort", json=payload)

    def importantindex(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/importantindex", json=payload)

    def profinmainindex(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/profinmainindex", json=payload)

    def proincstatementnew(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/proincstatementnew", json=payload)

    def probalsheetnew(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/probalsheetnew", json=payload)

    def procfstatementnew(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/procfstatementnew", json=payload)

    def subnewstockranking(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/subnewstockranking", json=payload)

    def newsharescal(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post("/newsharescal", json=payload)


DeskQuotesApi = QuotesApi
