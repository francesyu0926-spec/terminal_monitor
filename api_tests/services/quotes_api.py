from __future__ import annotations

from typing import Any, Sequence

import httpx

from api_tests.core.http_client import ApiClient


class QuotesApi:
    """行情接口：POST /quote、POST /catesorting 等"""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def quote(self, code: str, fields: Sequence[str]) -> httpx.Response:
        return self._client.post(
            "/quote",
            json={"code": code, "fields": list(fields)},
        )

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
